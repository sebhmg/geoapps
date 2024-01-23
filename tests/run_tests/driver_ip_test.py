#  Copyright (c) 2023-2024 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from __future__ import annotations

from pathlib import Path

import numpy as np
from geoh5py.workspace import Workspace

from geoapps.inversion.components import InversionData
from geoapps.inversion.electricals.induced_polarization.three_dimensions import (
    InducedPolarization3DParams,
)
from geoapps.inversion.electricals.induced_polarization.three_dimensions.driver import (
    InducedPolarization3DDriver,
)
from geoapps.shared_utils.utils import get_inversion_output
from geoapps.utils.testing import check_target, setup_inversion_workspace

# To test the full run and validate the inversion.
# Move this file out of the test directory and run.

target_run = {"data_norm": 1.7320473900654279e-06, "phi_d": 1.371, "phi_m": 0.4521}

np.random.seed(0)


def test_ip_3d_fwr_run(
    tmp_path: Path,
    n_electrodes=4,
    n_lines=3,
    refinement=(4, 6),
):
    # Run the forward
    geoh5, _, model, survey, topography = setup_inversion_workspace(
        tmp_path,
        background=1e-6,
        anomaly=1e-1,
        n_electrodes=n_electrodes,
        n_lines=n_lines,
        refinement=refinement,
        drape_height=0.0,
        inversion_type="dcip",
        flatten=False,
    )
    params = InducedPolarization3DParams(
        forward_only=True,
        geoh5=geoh5,
        mesh=model.parent.uid,
        topography_object=topography.uid,
        z_from_topo=True,
        data_object=survey.uid,
        starting_model=model.uid,
        conductivity_model=1e-2,
    )
    params.workpath = tmp_path
    fwr_driver = InducedPolarization3DDriver(params)
    fwr_driver.run()


def test_ip_3d_run(
    tmp_path: Path,
    max_iterations=1,
    pytest=True,
    n_lines=3,
):
    workpath = tmp_path / "inversion_test.ui.geoh5"
    if pytest:
        workpath = tmp_path.parent / "test_ip_3d_fwr_run0" / "inversion_test.ui.geoh5"

    with Workspace(workpath) as geoh5:
        potential = geoh5.get_entity("Iteration_0_ip")[0]
        mesh = geoh5.get_entity("mesh")[0]
        topography = geoh5.get_entity("topography")[0]

        # Set some data as nan
        vals = potential.values
        vals[0] = np.nan
        potential.values = vals

        # Run the inverse
        np.random.seed(0)
        params = InducedPolarization3DParams(
            geoh5=geoh5,
            mesh=mesh.uid,
            topography_object=topography.uid,
            data_object=potential.parent.uid,
            conductivity_model=1e-2,
            reference_model=1e-6,
            starting_model=1e-6,
            s_norm=0.0,
            x_norm=0.0,
            y_norm=0.0,
            z_norm=0.0,
            gradient_type="components",
            chargeability_channel_bool=True,
            z_from_topo=False,
            chargeability_channel=potential.uid,
            chargeability_uncertainty=2e-4,
            max_global_iterations=max_iterations,
            initial_beta=None,
            initial_beta_ratio=1e0,
            prctile=100,
            upper_bound=0.1,
            tile_spatial=n_lines,
            store_sensitivities="ram",
            coolingRate=1,
        )
        params.write_input_file(path=tmp_path, name="Inv_run")

        data = InversionData(geoh5, params)
        survey = data.create_survey()
        assert survey[0].dobs[0] == survey[0].dummy
    driver = InducedPolarization3DDriver.start(str(tmp_path / "Inv_run.ui.json"))

    output = get_inversion_output(
        driver.params.geoh5.h5file, driver.params.out_group.uid
    )
    assert np.array([o is not np.nan for o in output["phi_d"]]).any()
    assert np.array([o is not np.nan for o in output["phi_m"]]).any()
    if geoh5.open():
        potential = [
            p
            for p in geoh5.get_entity("Data")
            if p.parent.name == "Induced polarization 3d Inversion"
        ][0]
        output["data"] = potential.get_data("Iteration_0_ip")[0].values

    if pytest:
        check_target(output, target_run)


if __name__ == "__main__":
    # Full run
    test_ip_3d_fwr_run(
        Path("./"),
        n_electrodes=20,
        n_lines=5,
        refinement=(4, 8),
    )
    test_ip_3d_run(
        Path("./"),
        n_lines=5,
        max_iterations=15,
        pytest=False,
    )
