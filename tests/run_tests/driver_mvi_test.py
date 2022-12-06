#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

import os

import numpy as np
from geoh5py.objects import Curve
from geoh5py.workspace import Workspace
from SimPEG import utils

from geoapps.inversion.potential_fields import MagneticVectorParams
from geoapps.inversion.potential_fields.magnetic_vector.driver import (
    MagneticVectorDriver,
)
from geoapps.shared_utils.utils import get_inversion_output
from geoapps.utils.testing import check_target, setup_inversion_workspace

# To test the full run and validate the inversion.
# Move this file out of the test directory and run.

target_mvi_run = {
    "data_norm": 8.0686,
    "phi_d": 0.006295,
    "phi_m": 3.798e-6,
}


def test_magnetic_vector_fwr_run(
    tmp_path,
    n_grid_points=2,
    refinement=(2,),
):
    np.random.seed(0)
    inducing_field = (50000.0, 90.0, 0.0)
    # Run the forward
    geoh5, _, model, points, topography = setup_inversion_workspace(
        tmp_path,
        background=0.0,
        anomaly=0.05,
        refinement=refinement,
        n_electrodes=n_grid_points,
        n_lines=n_grid_points,
    )

    # Unitest dealing with Curve
    survey = Curve.create(geoh5, name=points.name, vertices=points.vertices)
    geoh5.remove_entity(points)

    params = MagneticVectorParams(
        forward_only=True,
        geoh5=geoh5,
        mesh=model.parent.uid,
        topography_object=topography.uid,
        inducing_field_strength=inducing_field[0],
        inducing_field_inclination=inducing_field[1],
        inducing_field_declination=inducing_field[2],
        resolution=0.0,
        z_from_topo=False,
        data_object=survey.uid,
        starting_model_object=model.parent.uid,
        starting_model=model.uid,
        starting_inclination=45,
        starting_declination=270,
    )
    fwr_driver = MagneticVectorDriver(params)

    fwr_driver.run()
    return fwr_driver.starting_model


def test_magnetic_vector_run(
    tmp_path,
    max_iterations=1,
    pytest=True,
):
    workpath = os.path.join(tmp_path, "inversion_test.geoh5")
    if pytest:
        workpath = str(
            tmp_path / "../test_magnetic_vector_fwr_run0/inversion_test.geoh5"
        )

    with Workspace(workpath) as geoh5:
        tmi = geoh5.get_entity("Iteration_0_tmi")[0]
        orig_tmi = tmi.values.copy()
        mesh = geoh5.get_entity("mesh")[0]
        topography = geoh5.get_entity("topography")[0]
        inducing_field = (50000.0, 90.0, 0.0)

        # Run the inverse
        params = MagneticVectorParams(
            geoh5=geoh5,
            mesh=mesh.uid,
            topography_object=topography.uid,
            inducing_field_strength=inducing_field[0],
            inducing_field_inclination=inducing_field[1],
            inducing_field_declination=inducing_field[2],
            resolution=0.0,
            data_object=tmi.parent.uid,
            starting_model=1e-4,
            reference_model=0.0,
            s_norm=0.0,
            x_norm=1.0,
            y_norm=1.0,
            z_norm=1.0,
            gradient_type="components",
            tmi_channel_bool=True,
            z_from_topo=False,
            tmi_channel=tmi.uid,
            tmi_uncertainty=4.0,
            max_global_iterations=max_iterations,
            initial_beta_ratio=1e1,
            store_sensitivities="ram",
            prctile=100,
        )
        params.write_input_file(path=tmp_path, name="Inv_run")
        driver = MagneticVectorDriver.start(os.path.join(tmp_path, "Inv_run.ui.json"))

    with Workspace(driver.params.geoh5.h5file) as run_ws:

        # Re-open the workspace and get iterations
        output = get_inversion_output(
            driver.params.geoh5.h5file, driver.params.ga_group.uid
        )
        output["data"] = orig_tmi
        if pytest:
            check_target(output, target_mvi_run)
            nan_ind = np.isnan(
                run_ws.get_entity("Iteration_0_amplitude_model")[0].values
            )
            inactive_ind = run_ws.get_entity("active_cells")[0].values == 0
            assert np.all(nan_ind == inactive_ind)
        else:
            return utils.spherical2cartesian(driver.inverse_problem.model)


if __name__ == "__main__":
    # Full run
    m_start = test_magnetic_vector_fwr_run("./", n_grid_points=20, refinement=(4, 8))
    m_rec = test_magnetic_vector_run("./", max_iterations=30, pytest=False)
    residual = np.linalg.norm(m_rec - m_start) / np.linalg.norm(m_start) * 100.0
    assert (
        residual < 50.0
    ), f"Deviation from the true solution is {residual:.2f}%. Validate the solution!"
    print("MVI model is within 50% of the answer. Done!")
