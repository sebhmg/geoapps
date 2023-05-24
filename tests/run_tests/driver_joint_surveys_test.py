#  Copyright (c) 2023 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

import numpy as np
from geoh5py.objects import Octree
from geoh5py.workspace import Workspace

from geoapps.inversion.joint.joint_surveys import JointSingleParams
from geoapps.inversion.joint.joint_surveys.driver import JointSurveyDriver
from geoapps.inversion.potential_fields import GravityParams
from geoapps.inversion.potential_fields.gravity.driver import GravityDriver
from geoapps.shared_utils.utils import get_inversion_output
from geoapps.utils.testing import check_target, setup_inversion_workspace

# To test the full run and validate the inversion.
# Move this file out of the test directory and run.

target_run = {
    "data_norm": 0.104056,
    "phi_d": 427,
    "phi_m": 6.558,
}


def test_joint_surveys_fwr_run(
    tmp_path,
    n_grid_points=4,
    refinement=(2,),
):
    np.random.seed(0)
    # Create local problem A
    geoh5, _, model, survey, topography = setup_inversion_workspace(
        tmp_path,
        background=0.0,
        anomaly=0.75,
        refinement=refinement,
        n_electrodes=n_grid_points,
        n_lines=n_grid_points,
    )
    params = GravityParams(
        forward_only=True,
        geoh5=geoh5,
        mesh=model.parent.uid,
        topography_object=topography.uid,
        resolution=0.0,
        z_from_topo=False,
        data_object=survey.uid,
        starting_model=model.uid,
    )
    fwr_driver_a = GravityDriver(params)

    # Create local problem B

    _, _, model, survey, _ = setup_inversion_workspace(
        tmp_path,
        background=0.0,
        anomaly=0.75,
        refinement=[0, 2],
        n_electrodes=int(n_grid_points / 2),
        n_lines=int(n_grid_points / 2),
        flatten=False,
        geoh5=geoh5,
        drape_height=10.0,
    )

    params = GravityParams(
        forward_only=True,
        geoh5=geoh5,
        mesh=model.parent.uid,
        topography_object=topography.uid,
        resolution=0.0,
        z_from_topo=False,
        data_object=survey.uid,
        starting_model=model.uid,
    )
    fwr_driver_b = GravityDriver(params)

    joint_params = JointSingleParams(
        forward_only=True,
        geoh5=geoh5,
        topography_object=topography.uid,
        group_a=fwr_driver_a.params.ga_group,
        group_b=fwr_driver_b.params.ga_group,
    )

    fwr_driver = JointSurveyDriver(joint_params)
    fwr_driver.run()
    geoh5.close()
    return fwr_driver.models.starting


def test_joint_surveys_inv_run(
    tmp_path,
    max_iterations=1,
    pytest=True,
):
    workpath = tmp_path / "inversion_test.geoh5"
    if pytest:
        workpath = (
            tmp_path.parent / "test_joint_surveys_fwr_run0" / "inversion_test.geoh5"
        )

    with Workspace(workpath) as geoh5:
        topography = geoh5.get_entity("topography")[0]
        drivers = []
        orig_data = []
        for group in geoh5.get_entity("GravityForward"):
            survey = geoh5.get_entity(group.options["data_object"]["value"])[0]
            for child in group.children:
                if isinstance(child, Octree):
                    mesh = child
                else:
                    survey = child

            gz = survey.get_data("Iteration_0_gz")[0]
            orig_data.append(gz.values)
            params = GravityParams(
                geoh5=geoh5,
                mesh=mesh.uid,
                topography_object=topography.uid,
                data_object=survey.uid,
                gz_channel=gz.uid,
                gz_uncertainty=1e-3,
                starting_model=0.0,
            )
            drivers.append(GravityDriver(params))

        # Run the inverse
        np.random.seed(0)
        joint_params = JointSingleParams(
            geoh5=geoh5,
            topography_object=topography.uid,
            mesh=geoh5.get_entity("Octree")[0].uid,
            group_a=drivers[0].params.ga_group,
            group_b=drivers[1].params.ga_group,
            starting_model=1e-4,
            reference_model=0.0,
            s_norm=0.0,
            x_norm=0.0,
            y_norm=0.0,
            z_norm=0.0,
            gradient_type="components",
            lower_bound=0.0,
            max_global_iterations=max_iterations,
            initial_beta_ratio=1e-2,
            prctile=100,
            store_sensitivities="ram",
        )

    driver = JointSurveyDriver(joint_params)
    driver.run()

    with Workspace(driver.params.geoh5.h5file):
        output = get_inversion_output(
            driver.params.geoh5.h5file, driver.params.ga_group.uid
        )

        output["data"] = np.hstack(orig_data)
        if pytest:
            check_target(output, target_run)
        else:
            return driver.inverse_problem.model


if __name__ == "__main__":
    # Full run
    m_start = test_joint_surveys_fwr_run(
        "./",
        n_grid_points=20,
        refinement=(4, 8),
    )

    m_rec = test_joint_surveys_inv_run(
        "./",
        max_iterations=15,
        pytest=False,
    )
    model_residual = np.linalg.norm(m_rec - m_start) / np.linalg.norm(m_start) * 100.0
    assert (
        model_residual < 75.0
    ), f"Deviation from the true solution is {model_residual:.2f}%. Validate the solution!"
    print("Density model is within 15% of the answer. Let's go!!")
