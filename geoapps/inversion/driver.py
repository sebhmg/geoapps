#  Copyright (c) 2023 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from geoapps.inversion import InversionBaseParams

import multiprocessing
import os
import sys
from datetime import datetime, timedelta
from multiprocessing.pool import ThreadPool
from time import time

import numpy as np
from dask import config as dconf
from geoh5py.ui_json import InputFile
from SimPEG import (
    directives,
    inverse_problem,
    inversion,
    maps,
    optimization,
    regularization,
)

from geoapps.driver_base.driver import BaseDriver
from geoapps.inversion.components import (
    InversionData,
    InversionMesh,
    InversionModelCollection,
    InversionTopography,
    InversionWindow,
)
from geoapps.inversion.components.factories import DirectivesFactory, MisfitFactory, SaveIterationGeoh5Factory
from geoapps.inversion.params import InversionBaseParams
from geoapps.inversion.utils import tile_locations

DRIVER_MAP = {
    "direct current 3d": (
        "geoapps.inversion.electricals.direct_current.three_dimensions.driver",
        "DirectCurrent3DDriver",
    ),
    "direct current 2d": (
        "geoapps.inversion.electricals.direct_current.two_dimensions.driver",
        "DirectCurrent2DDriver",
    ),
    "direct current pseudo 3d": (
        "geoapps.inversion.electricals.direct_current.pseudo_three_dimensions.driver",
        "DirectCurrentPseudo3DDriver",
    ),
    "induced polarization 3d": (
        "geoapps.inversion.electricals.induced_polarization.three_dimensions.driver",
        "InducedPolarization3DDriver",
    ),
    "induced polarization 2d": (
        "geoapps.inversion.electricals.induced_polarization.two_dimensions.driver",
        "InducedPolarization2DDriver",
    ),
    "induced polarization pseudo 3d": (
        "geoapps.inversion.electricals.induced_polarization.pseudo_three_dimensions.driver",
        "InducedPolarizationPseudo3DDriver",
    ),
    "joint single property": (
        "geoapps.inversion.joint.single_property.driver",
        "JointSingleDriver",
    ),
    "tdem": (
        "geoapps.inversion.airborne_electromagnetics.time_domain.driver",
        "TimeDomainElectromagneticsDriver",
    ),
    "magnetotellurics": (
        "geoapps.inversion.natural_sources.magnetotellurics.driver",
        "MagnetotelluricsDriver",
    ),
    "tipper": ("geoapps.inversion.natural_sources.tipper.driver", "TipperDriver"),
    "gravity": ("geoapps.inversion.potential_fields.gravity.driver", "GravityDriver"),
    "magnetic scalar": (
        "geoapps.inversion.potential_fields.magnetic_scalar.driver",
        "MagneticScalarDriver",
    ),
    "magnetic vector": (
        "geoapps.inversion.potential_fields.magnetic_vector.driver",
        "MagneticVectorDriver",
    ),
}


class InversionDriver(BaseDriver):
    _params_class = InversionBaseParams  # pylint: disable=E0601
    _validations = None

    def __init__(self, params: InversionBaseParams, warmstart=False):
        super().__init__(params)

        self.params = params
        self.warmstart = warmstart
        self.workspace = params.geoh5
        self.inversion_type = params.inversion_type
        self._data_misfit: DataMisfit | None = None
        self._directives: list[directives.InversionDirective] | None = None
        self._inverse_problem: inverse_problem.BaseInvProblem | None = None
        self._inversion: inversion.BaseInversion | None = None
        self._inversion_data: InversionData | None = None
        self._inversion_models: InversionModelCollection | None = None
        self._inversion_mesh: InversionMesh | None = None
        self._inversion_topography: InversionTopography | None = None
        self._optimization: optimization.ProjectedGNCG | None = None
        self._regularization: None = None
        self._window = None

        self.logger = InversionLogger("SimPEG.log", self)
        sys.stdout = self.logger
        self.logger.start()
        self.configure_dask()

    @property
    def data_misfit(self):
        if getattr(self, "_data_misfit", None) is None:
            self._data_misfit = DataMisfit(self)

        return self._data_misfit

    @property
    def directives(self):
        if getattr(self, "_directives", None) is None:
            self._directives = DirectivesFactory(self.params).build(
                self.inversion_data,
                self.inversion_mesh,
                self.inversion_models.active_cells,
                np.argsort(np.hstack(self.data_misfit.sorting)),
                self.data_misfit.ordering,
                self.data_misfit.objective_function,
                self.regularization,
            )
        return self._directives

    @property
    def inversion_data(self):
        """Inversion data"""
        if getattr(self, "_inversion_data", None) is None:
            self._inversion_data = InversionData(
                self.workspace, self.params, self.window()
            )

        return self._inversion_data

    @property
    def inversion_topography(self):
        """Inversion topography"""
        if getattr(self, "_inversion_topography", None) is None:
            self._inversion_topography = InversionTopography(
                self.workspace, self.params, self.inversion_data, self.window()
            )
        return self._inversion_topography

    @property
    def inverse_problem(self):
        if getattr(self, "_inverse_problem", None) is None:
            self._inverse_problem = inverse_problem.BaseInvProblem(
                self.data_misfit.objective_function,
                self.regularization,
                self.optimization,
                beta=self.params.initial_beta,
            )

        return self._inverse_problem

    @property
    def inversion(self):
        if getattr(self, "_inversion", None) is None:
            self._inversion = inversion.BaseInversion(
                self.inverse_problem, directiveList=self.directives
            )
        return self._inversion

    @property
    def inversion_mesh(self):
        """Inversion mesh"""
        if getattr(self, "_inversion_mesh", None) is None:
            self._inversion_mesh = InversionMesh(
                self.workspace,
                self.params,
                self.inversion_data,
                self.inversion_topography,
            )
        return self._inversion_mesh

    @property
    def inversion_models(self):
        """Inversion models"""
        if getattr(self, "_inversion_models", None) is None:
            self._inversion_models = InversionModelCollection(
                self.workspace, self.params, self.inversion_mesh
            )
            # Build active cells array and reduce models active set
            if self.inversion_mesh is not None and self.inversion_data is not None:
                self._inversion_models.active_cells = (
                    self.inversion_topography.active_cells(
                        self.inversion_mesh, self.inversion_data
                    )
                )

        return self._inversion_models

    @property
    def optimization(self):
        if getattr(self, "_optimization", None) is None:
            self._optimization = optimization.ProjectedGNCG(
                maxIter=self.params.max_global_iterations,
                lower=self.inversion_models.lower_bound,
                upper=self.inversion_models.upper_bound,
                maxIterLS=self.params.max_line_search_iterations,
                maxIterCG=self.params.max_cg_iterations,
                tolCG=self.params.tol_cg,
                stepOffBoundsFact=1e-8,
                LSshorten=0.25,
            )
        return self._optimization

    @property
    def regularization(self):
        if getattr(self, "_regularization", None) is None:
            self._regularization = self.get_regularization()

        return self._regularization

    @property
    def window(self):
        """Inversion window"""
        if getattr(self, "_window", None) is None:
            self._window = InversionWindow(self.workspace, self.params)
        return self._window

    def run(self):
        """Run inversion from params"""

        if self.params.forward_only:
            print("Running the forward simulation ...")
            dpred = inverse_problem.get_dpred(
                self.inversion_models.starting, compute_J=False
            )

            save_directive = SaveIterationGeoh5Factory(self.params).build(
                inversion_object=self.inversion_data,
                sorting=np.argsort(np.hstack(self.data_misfit.sorting)),
                ordering=self.data_misfit.ordering,
            )
            save_directive.save_components(0, dpred)

            self.logger.end()
            sys.stdout = self.logger.terminal
            self.logger.log.close()
            return

        # Run the inversion
        self.start_inversion_message()
        self.inversion.run(self.inversion_models.starting)
        self.logger.end()
        sys.stdout = self.logger.terminal
        self.logger.log.close()

    def start_inversion_message(self):
        # SimPEG reports half phi_d, so we scale to match
        has_chi_start = self.params.starting_chi_factor is not None
        chi_start = (
            self.params.starting_chi_factor if has_chi_start else self.params.chi_factor
        )
        print(
            "Target Misfit: {:.2e} ({} data with chifact = {}) / 2".format(
                0.5 * self.params.chi_factor * len(self.inversion_data.survey.std),
                len(self.inversion_data.survey.std),
                self.params.chi_factor,
            )
        )
        print(
            "IRLS Start Misfit: {:.2e} ({} data with chifact = {}) / 2".format(
                0.5 * chi_start * len(self.inversion_data.survey.std),
                len(self.inversion_data.survey.std),
                chi_start,
            )
        )

    def get_regularization(self):
        n_cells = int(np.sum(self.inversion_models.active_cells))

        if self.inversion_type == "magnetic vector":
            wires = maps.Wires(("p", n_cells), ("s", n_cells), ("t", n_cells))

            reg_p = regularization.Sparse(
                self.inversion_mesh.mesh,
                indActive=self.inversion_models.active_cells,
                mapping=wires.p,  # pylint: disable=no-member
                gradientType=self.params.gradient_type,
                alpha_s=self.params.alpha_s,
                alpha_x=self.params.alpha_x,
                alpha_y=self.params.alpha_y,
                alpha_z=self.params.alpha_z,
                norms=self.params.model_norms(),
                mref=self.inversion_models.reference,
            )
            reg_s = regularization.Sparse(
                self.inversion_mesh.mesh,
                indActive=self.inversion_models.active_cells,
                mapping=wires.s,  # pylint: disable=no-member
                gradientType=self.params.gradient_type,
                alpha_s=self.params.alpha_s,
                alpha_x=self.params.alpha_x,
                alpha_y=self.params.alpha_y,
                alpha_z=self.params.alpha_z,
                norms=self.params.model_norms(),
                mref=self.inversion_models.reference,
            )

            reg_t = regularization.Sparse(
                self.inversion_mesh.mesh,
                indActive=self.inversion_models.active_cells,
                mapping=wires.t,  # pylint: disable=no-member
                gradientType=self.params.gradient_type,
                alpha_s=self.params.alpha_s,
                alpha_x=self.params.alpha_x,
                alpha_y=self.params.alpha_y,
                alpha_z=self.params.alpha_z,
                norms=self.params.model_norms(),
                mref=self.inversion_models.reference,
            )

            # Assemble the 3-component regularizations
            reg = reg_p + reg_s + reg_t
            reg.mref = self.inversion_models.reference

        else:
            reg = regularization.Sparse(
                self.inversion_mesh.mesh,
                indActive=self.inversion_models.active_cells,
                mapping=maps.IdentityMap(nP=n_cells),
                gradientType=self.params.gradient_type,
                alpha_s=self.params.alpha_s,
                alpha_x=self.params.alpha_x,
                alpha_y=self.params.alpha_y,
                alpha_z=self.params.alpha_z,
                norms=self.params.model_norms(),
                mref=self.inversion_models.reference,
            )

        return reg

    def get_tiles(self):
        if self.params.inversion_type in [
            "direct current 3d",
            "induced polarization 3d",
        ]:
            tiles = []
            potential_electrodes = self.inversion_data.entity
            current_electrodes = potential_electrodes.current_electrodes
            line_split = np.array_split(
                current_electrodes.unique_parts, self.params.tile_spatial
            )
            for split in line_split:
                split_ind = []
                for line in split:
                    electrode_ind = current_electrodes.parts == line
                    cells_ind = np.where(
                        np.any(electrode_ind[current_electrodes.cells], axis=1)
                    )[0]
                    split_ind.append(cells_ind)
                # Fetch all receivers attached to the currents
                logical = np.zeros(current_electrodes.n_cells, dtype="bool")
                if len(split_ind) > 0:
                    logical[np.hstack(split_ind)] = True
                    tiles.append(
                        np.where(logical[potential_electrodes.ab_cell_id.values - 1])[0]
                    )

            # TODO Figure out how to handle a tile_spatial object to replace above

        elif "2d" in self.params.inversion_type:
            tiles = [self.inversion_data.indices]

        # elif self.params.inversion_type in ["tdem"]:
        #     transmitters = self.inversion_data.entity.transmitters
        #     transmitter_id = transmitters.get_data("Transmitter ID")
        #     if transmitter_id:
        #         tiles = [np.array([k]) for k in np.unique(transmitter_id[0].values)]
        #     else:
        #         tiles = [np.array([k]) for k in range(transmitters.n_vertices)]
        else:
            tiles = tile_locations(
                self.inversion_data.locations,
                self.params.tile_spatial,
                method="kmeans",
            )

        return tiles

    def configure_dask(self):
        """Sets Dask config settings."""

        if self.params.parallelized:
            if self.params.n_cpu is None:
                self.params.n_cpu = int(multiprocessing.cpu_count() / 2)

            dconf.set({"array.chunk-size": str(self.params.max_chunk_size) + "MiB"})
            dconf.set(scheduler="threads", pool=ThreadPool(self.params.n_cpu))

    @classmethod
    def start(cls, filepath, driver_class=None):
        _ = driver_class

        ifile = InputFile.read_ui_json(filepath)
        inversion_type = ifile.data["inversion_type"]
        if inversion_type not in DRIVER_MAP:
            msg = f"Inversion type {inversion_type} is not supported."
            msg += f" Valid inversions are: {*list(DRIVER_MAP),}."
            raise NotImplementedError(msg)

        mod_name, class_name = DRIVER_MAP.get(inversion_type)
        module = __import__(mod_name, fromlist=[class_name])
        inversion_driver = getattr(module, class_name)
        driver = BaseDriver.start(filepath, driver_class=inversion_driver)
        return driver


class InversionLogger:
    def __init__(self, logfile, driver):
        self.driver = driver
        self.terminal = sys.stdout
        self.log = open(self.get_path(logfile), "w", encoding="utf8")
        self.initial_time = time()

    def start(self):
        date_time = datetime.now().strftime("%b-%d-%Y:%H:%M:%S")
        self.write(
            f"SimPEG {self.driver.inversion_type} inversion started {date_time}\n"
        )

    def end(self):
        elapsed_time = timedelta(seconds=time() - self.initial_time).seconds
        days, hours, minutes, seconds = self.format_seconds(elapsed_time)
        self.write(
            f"Total runtime: {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.\n"
        )

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    @staticmethod
    def format_seconds(seconds):
        days = seconds // (24 * 3600)
        seconds = seconds % (24 * 3600)
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60
        return days, hours, minutes, seconds

    def close(self):
        self.terminal.close()

    def flush(self):
        pass

    def get_path(self, filepath):
        root_directory = os.path.dirname(self.driver.workspace.h5file)
        return os.path.join(root_directory, filepath)


class DataMisfit:
    """Class handling the data misfit function."""

    def __init__(self, driver: InversionDriver):
        # Tile locations
        tiles = (
            driver.get_tiles()
        )  # [np.arange(len(self.inversion_data.survey.source_list))]#
        print(f"Setting up {len(tiles)} tile(s) . . .")
        # Build tiled misfits and combine to form global misfit

        self._objective_function, self._sorting, self._ordering = MisfitFactory(
            driver.params, models=driver.inversion_models
        ).build(
            tiles,
            driver.inversion_data,
            driver.inversion_mesh.mesh,
            driver.inversion_models.active_cells,
        )
        print("Done.")

    @property
    def objective_function(self):
        """The Simpeg.data_misfit class"""
        return self._objective_function

    @property
    def sorting(self):
        """List of arrays for sorting of data from tiles."""
        return self._sorting

    @property
    def ordering(self):
        """List of ordering of the data."""
        return self._ordering


if __name__ == "__main__":
    file = os.path.abspath(sys.argv[1])
    InversionDriver.start(file)
    sys.stdout.close()
