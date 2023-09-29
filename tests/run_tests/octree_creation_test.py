#  Copyright (c) 2023 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from discretize.utils import mesh_builder_xyz
from geoh5py.objects import Curve, Points
from geoh5py.shared.utils import compare_entities
from geoh5py.ui_json.utils import str2list
from geoh5py.workspace import Workspace

from geoapps.driver_base.utils import treemesh_2_octree
from geoapps.octree_creation.application import OctreeDriver, OctreeMesh
from geoapps.utils.testing import get_output_workspace

# pylint: disable=redefined-outer-name


@pytest.fixture
def setup_test_octree():
    """
    Create a circle of points and treemesh from extent.
    """
    refinement = "4, 4"
    minimum_level = 4
    cell_sizes = [5.0, 5.0, 5.0]
    n_data = 16
    degree = np.linspace(0, 2 * np.pi, n_data)
    locations = np.c_[
        np.cos(degree) * 200.0, np.sin(degree) * 200.0, np.sin(degree * 2.0) * 40.0
    ]
    # Add point at origin
    locations = np.r_[locations, np.zeros((1, 3))]
    depth_core = 400.0
    horizontal_padding = 500.0
    vertical_padding = 200.0
    paddings = [
        [horizontal_padding, horizontal_padding],
        [horizontal_padding, horizontal_padding],
        [vertical_padding, vertical_padding],
    ]
    # Create a tree mesh from discretize
    treemesh = mesh_builder_xyz(
        locations,
        cell_sizes,
        padding_distance=paddings,
        mesh_type="tree",
        depth_core=depth_core,
    )

    return (
        cell_sizes,
        depth_core,
        horizontal_padding,
        locations,
        minimum_level,
        refinement,
        treemesh,
        vertical_padding,
    )


def test_create_octree_radial(tmp_path: Path, setup_test_octree):
    (
        cell_sizes,
        depth_core,
        horizontal_padding,
        locations,
        minimum_level,
        refinement,
        treemesh,
        vertical_padding,
    ) = setup_test_octree

    with Workspace.create(tmp_path / "testOctree.geoh5") as workspace:
        points = Points.create(workspace, vertices=locations)
        treemesh.refine(treemesh.max_level - minimum_level + 1, finalize=False)
        treemesh = OctreeDriver.refine_tree_from_points(
            treemesh,
            points,
            str2list(refinement),
            finalize=True,
        )
        octree = treemesh_2_octree(workspace, treemesh, name="Octree_Mesh")

        # Hard-wire the expected result
        assert octree.n_cells == 164742

        assert OctreeDriver.cell_size_from_level(treemesh, 1) == 10.0

        # Repeat the creation using the app
        refinements = {
            "Refinement A object": points.uid,
            "Refinement A levels": refinement,
            "Refinement A type": "radial",
            "Refinement B object": None,
            "minimum_level": minimum_level,
        }
        app = OctreeMesh(
            geoh5=workspace,
            objects=str(points.uid),
            u_cell_size=cell_sizes[0],
            v_cell_size=cell_sizes[1],
            w_cell_size=cell_sizes[2],
            horizontal_padding=horizontal_padding,
            vertical_padding=vertical_padding,
            depth_core=depth_core,
            **refinements,
        )
        app.trigger_click(None)

        # Re-load the new mesh and compare
        with Workspace(get_output_workspace(tmp_path)) as workspace:
            rec_octree = workspace.get_entity("Octree_Mesh")[0]
            compare_entities(octree, rec_octree, ignore=["_uid"])


def test_create_octree_curve(tmp_path: Path, setup_test_octree):
    (
        cell_sizes,
        depth_core,
        horizontal_padding,
        locations,
        minimum_level,
        refinement,
        treemesh,
        vertical_padding,
    ) = setup_test_octree

    with Workspace.create(tmp_path / "testOctree.geoh5") as workspace:
        curve = Curve.create(workspace, vertices=locations)
        curve.remove_cells([-1])
        treemesh.refine(treemesh.max_level - minimum_level + 1, finalize=False)
        treemesh = OctreeDriver.refine_tree_from_curve(
            treemesh,
            curve,
            str2list(refinement),
            finalize=True,
        )
        octree = treemesh_2_octree(workspace, treemesh, name="Octree_Mesh")

        assert octree.n_cells == 176915

        # Repeat the creation using the app
        refinements = {
            "Refinement A object": curve.uid,
            "Refinement A levels": refinement,
            "Refinement A type": "radial",
            "Refinement B object": None,
            "minimum_level": minimum_level,
        }
        app = OctreeMesh(
            geoh5=workspace,
            objects=str(curve.uid),
            u_cell_size=cell_sizes[0],
            v_cell_size=cell_sizes[1],
            w_cell_size=cell_sizes[2],
            horizontal_padding=horizontal_padding,
            vertical_padding=vertical_padding,
            depth_core=depth_core,
            **refinements,
        )
        app.trigger_click(None)

        # Re-load the new mesh and compare
        with Workspace(get_output_workspace(tmp_path)) as workspace:
            rec_octree = workspace.get_entity("Octree_Mesh")[0]
            compare_entities(octree, rec_octree, ignore=["_uid"])


def test_create_octree_surface(tmp_path: Path, setup_test_octree):
    (
        cell_sizes,
        depth_core,
        horizontal_padding,
        locations,
        minimum_level,
        refinement,
        treemesh,
        vertical_padding,
    ) = setup_test_octree

    with Workspace.create(tmp_path / "testOctree.geoh5") as workspace:
        points = Points.create(workspace, vertices=locations)
        treemesh.refine(treemesh.max_level - minimum_level + 1, finalize=False)
        treemesh = OctreeDriver.refine_tree_from_surface(
            treemesh,
            points,
            str2list(refinement),
            finalize=True,
        )
        octree = treemesh_2_octree(workspace, treemesh, name="Octree_Mesh")

        assert octree.n_cells in [
            168627,
            168396,
        ]  # Different results on Linux and Windows

        # Repeat the creation using the app
        refinements = {
            "Refinement A object": points.uid,
            "Refinement A levels": refinement,
            "Refinement A type": "surface",
            "Refinement B object": None,
            "minimum_level": minimum_level,
        }
        app = OctreeMesh(
            geoh5=workspace,
            objects=str(points.uid),
            u_cell_size=cell_sizes[0],
            v_cell_size=cell_sizes[1],
            w_cell_size=cell_sizes[2],
            horizontal_padding=horizontal_padding,
            vertical_padding=vertical_padding,
            depth_core=depth_core,
            **refinements,
        )
        app.trigger_click(None)

        # Re-load the new mesh and compare
        with Workspace(get_output_workspace(tmp_path)) as workspace:
            rec_octree = workspace.get_entity("Octree_Mesh")[0]
            compare_entities(octree, rec_octree, ignore=["_uid"])


def test_create_octree_driver(tmp_path: Path):
    uijson_path = tmp_path.parent / "test_create_octree_curve0" / "Temp"
    json_file = next(uijson_path.glob("*.ui.json"))
    driver = OctreeDriver.start(str(json_file))

    with driver.params.geoh5.open(mode="r"):
        results = driver.params.geoh5.get_entity("Octree_Mesh")
        compare_entities(results[0], results[1], ignore=["_uid"])
