#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from uuid import UUID

from geoh5py.objects import Curve, Grid2D, Points, Surface

octree_defaults = {
    "title": "Inversion mesh creator",
    "geoh5": None,
    "objects": None,
    "u_cell_size": 25.0,
    "v_cell_size": 25.0,
    "w_cell_size": 25.0,
    "depth_core": 500.0,
    "horizontal_padding": 1000.0,
    "vertical_padding": 1000.0,
    "Refinement A object": None,
    "Refinement A levels": [4, 4, 4, 4],
    "Refinement A type": "radial",
    "Refinement A distance": 5000.0,
    "Refinement B object": None,
    "Refinement B levels": [0, 0, 4, 4],
    "Refinement B type": "surface",
    "Refinement B distance": 5000.0,
    "ga_group_name": "Inversion Mesh",
    "run_command": "geoapps.octree_creation.application",
    "run_command_boolean": False,
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "conda_environment": "geoapps",
    "conda_environment_boolean": False,
}


default_octree_ui_json = {
    "title": None,
    "geoh5": None,
    "objects": {
        "enabled": True,
        "group": "Mesh",
        "label": "Core hull extent",
        "main": True,
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
        ],
        "value": None,
    },
    "u_cell_size": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "label": "Easting core cell size (m)",
        "value": 25.0,
    },
    "v_cell_size": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "label": "Northing core cell size (m)",
        "value": 25.0,
    },
    "w_cell_size": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "label": "Vertical core cell size (m)",
        "value": 25.0,
    },
    "depth_core": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "label": "Depth of core refinement volume",
        "value": 500.0,
    },
    "horizontal_padding": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "label": "Horizontal padding",
        "value": 1000.0,
    },
    "vertical_padding": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "label": "Vertical padding",
        "value": 1000.0,
    },
    "Refinement A object": {
        "groupOptional": True,
        "enabled": True,
        "group": "Data refinement",
        "label": "Data object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
        ],
        "value": None,
    },
    "Refinement A levels": {
        "enabled": True,
        "group": "Data refinement",
        "label": "Levels",
        "value": "4, 4, 4, 4",
    },
    "Refinement A type": {
        "choiceList": ["surface", "radial"],
        "enabled": True,
        "group": "Data refinement",
        "label": "Type",
        "value": "radial",
    },
    "Refinement A distance": {
        "enabled": True,
        "group": "Data refinement",
        "label": "Distance",
        "value": 5000.0,
    },
    "Refinement B object": {
        "groupOptional": True,
        "enabled": True,
        "group": "Topography refinement",
        "label": "Topography object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
        ],
        "value": None,
    },
    "Refinement B levels": {
        "enabled": True,
        "group": "Topography refinement",
        "label": "Levels",
        "value": "0, 0, 4, 4",
    },
    "Refinement B type": {
        "choiceList": ["surface", "radial"],
        "enabled": True,
        "group": "Topography refinement",
        "label": "Type",
        "value": "surface",
    },
    "Refinement B distance": {
        "enabled": True,
        "group": "Topography refinement",
        "label": "Distance",
        "value": 5000.0,
    },
    "ga_group_name": {"enabled": True, "label": "Name:", "value": "Inversion Mesh"},
    "run_command": "geoapps.octree_creation.application",
    "run_command_boolean": {
        "value": False,
        "label": "Run python module ",
        "tooltip": "Warning: launches process to run python model on save",
        "main": True,
    },
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "conda_environment": "geoapps",
    "conda_environment_boolean": False,
}

default_ui_json = {
    "forward_only": False,
    "topography_object": {
        "main": True,
        "group": "Topography",
        "label": "Object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
            "{b020a277-90e2-4cd7-84d6-612ee3f25051}",
        ],
        "value": None,
    },
    "topography": {
        "association": "Vertex",
        "dataType": "Float",
        "group": "Topography",
        "main": True,
        "optional": True,
        "enabled": False,
        "isValue": False,
        "label": "Elevation",
        "parent": "topography_object",
        "property": None,
        "value": 0.0,
    },
    "data_object": {
        "main": True,
        "group": "Data",
        "label": "Object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
            "{b020a277-90e2-4cd7-84d6-612ee3f25051}",
            "{4ea87376-3ece-438b-bf12-3479733ded46}",
        ],
        "value": None,
    },
    "starting_model_object": {
        "group": "Starting Model",
        "main": True,
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
            "{b020a277-90e2-4cd7-84d6-612ee3f25051}",
            "{4ea87376-3ece-438b-bf12-3479733ded46}",
        ],
        "optional": True,
        "enabled": False,
        "label": "Object",
        "value": None,
    },
    "starting_model": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Starting Model",
        "main": True,
        "isValue": True,
        "parent": "starting_model_object",
        "label": "Value",
        "property": None,
        "value": 1e-4,
    },
    "tile_spatial": {
        "group": "Receivers location options",
        "label": "Number of tiles",
        "parent": "data_object",
        "isValue": True,
        "property": None,
        "value": 1,
        "min": 1,
        "max": 1000,
    },
    "output_tile_files": False,
    "z_from_topo": {
        "main": False,
        "group": "Receivers location options",
        "label": "Take z from topography",
        "value": False,
    },
    "receivers_radar_drape": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "main": False,
        "group": "Receivers location options",
        "label": "Drape receivers with radar channel",
        "optional": True,
        "parent": "data_object",
        "value": None,
        "enabled": False,
    },
    "receivers_offset_x": {
        "group": "Receivers location options",
        "main": False,
        "label": "Receiver X offset (m)",
        "value": 0.0,
        "enabled": True,
    },
    "receivers_offset_y": {
        "group": "Receivers location options",
        "main": False,
        "label": "Receiver Y offset (m)",
        "value": 0.0,
        "enabled": True,
    },
    "receivers_offset_z": {
        "group": "Receivers location options",
        "main": False,
        "label": "Receiver Z offset (m)",
        "value": 0.0,
        "enabled": True,
    },
    "gps_receivers_offset": None,
    "ignore_values": {
        "group": "Data pre-processing",
        "optional": True,
        "enabled": False,
        "label": "Values to ignore",
        "value": None,
    },
    "resolution": {
        "min": 0.0,
        "group": "Data pre-processing",
        "optional": True,
        "enabled": False,
        "label": "Downsampling resolution",
        "value": 0.0,
    },
    "detrend_order": {
        "min": 0,
        "group": "Data pre-processing",
        "enabled": False,
        "dependencyType": "enabled",
        "label": "Detrend order",
        "optional": True,
        "value": 0,
    },
    "detrend_type": {
        "choiceList": ["all", "perimeter"],
        "group": "Data pre-processing",
        "dependency": "detrend_order",
        "dependencyType": "enabled",
        "enabled": False,
        "optional": True,
        "label": "Detrend type",
        "value": "all",
    },
    "max_chunk_size": {
        "min": 0,
        "group": "Data pre-processing",
        "optional": True,
        "enabled": True,
        "label": "Maximum chunk size",
        "value": 128,
    },
    "chunk_by_rows": {
        "group": "Data pre-processing",
        "label": "Chunk by rows",
        "value": True,
    },
    "mesh": {
        "group": "Mesh",
        "main": True,
        "optional": True,
        "enabled": False,
        "dependency": "mesh_from_params",
        "dependencyType": "disabled",
        "label": "Mesh",
        "meshType": "4EA87376-3ECE-438B-BF12-3479733DED46",
        "value": None,
    },
    "u_cell_size": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "Easting core cell size (m)",
        "value": 25.0,
    },
    "v_cell_size": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "Northing core cell size (m)",
        "value": 25.0,
    },
    "w_cell_size": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "Vertical core cell size (m)",
        "value": 25.0,
    },
    "octree_levels_topo": {
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "octree levels topography",
        "value": [0, 0, 4, 4],
    },
    "octree_levels_obs": {
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "octree levels observations",
        "value": [4, 4, 4, 4],
    },
    "depth_core": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "Depth of core refinement volume",
        "value": 500.0,
    },
    "max_distance": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "Maximum padding distance",
        "value": 5000.0,
    },
    "horizontal_padding": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "Horizontal padding",
        "value": 1000.0,
    },
    "vertical_padding": {
        "min": 0.0,
        "group": "Mesh",
        "main": True,
        "enabled": True,
        "dependency": "mesh",
        "dependencyType": "disabled",
        "label": "Vertical padding",
        "value": 1000.0,
    },
    "window_center_x": {
        "group": "Data window",
        "enabled": True,
        "groupOptional": True,
        "label": "Window center easting",
        "value": 0.0,
    },
    "window_center_y": {
        "group": "Data window",
        "enabled": True,
        "label": "Window center northing",
        "value": 0.0,
    },
    "window_width": {
        "min": 0.0,
        "group": "Data window",
        "enabled": True,
        "label": "Window width",
        "value": 0.0,
    },
    "window_height": {
        "min": 0.0,
        "group": "Data window",
        "enabled": True,
        "label": "Window height",
        "value": 0.0,
    },
    "window_azimuth": {
        "min": -180,
        "max": 180,
        "group": "Data window",
        "enabled": True,
        "label": "Window azimuth",
        "value": 0.0,
    },
    "inversion_style": "voxel",
    "chi_factor": {
        "min": 0.0,
        "max": 1.0,
        "group": "Optimization",
        "label": "Chi factor",
        "value": 1.0,
        "enabled": True,
    },
    "sens_wts_threshold": {
        "group": "Update sensitivity weights directive",
        "label": "Update sensitivity weight threshold",
        "value": 0.0,
    },
    "every_iteration_bool": {
        "group": "Update sensitivity weights directive",
        "label": "Update every iteration",
        "value": False,
    },
    "f_min_change": {
        "group": "Update IRLS directive",
        "label": "f min change",
        "value": 1e-4,
    },
    "minGNiter": {
        "group": "Update IRLS directive",
        "label": "Minimum Gauss-Newton iterations",
        "value": 1,
    },
    "beta_tol": {
        "group": "Update IRLS directive",
        "label": "Beta tolerance",
        "value": 0.5,
    },
    "prctile": {
        "group": "Update IRLS directive",
        "label": "percentile",
        "value": 95,
    },
    "coolingRate": {
        "group": "Update IRLS directive",
        "label": "Beta cooling rate",
        "value": 1,
    },
    "coolEps_q": {
        "group": "Update IRLS directive",
        "label": "Cool epsilon q",
        "value": True,
    },
    "coolEpsFact": {
        "group": "Update IRLS directive",
        "label": "Cool epsilon fact",
        "value": 1.2,
    },
    "beta_search": {
        "group": "Update IRLS directive",
        "label": "Perform beta search",
        "value": False,
    },
    "starting_chi_factor": {
        "group": "Update IRLS directive",
        "label": "IRLS start chi factor",
        "optional": True,
        "enabled": False,
        "value": 1.0,
        "tooltip": "This chi factor will be used to determine the misfit"
        " threshold after which IRLS iterations begin.",
    },
    "max_iterations": {
        "min": 0,
        "group": "Optimization",
        "label": "Maximum number of IRLS iterations",
        "tooltip": "Incomplete Re-weighted Least Squares iterations for non-L2 problems",
        "value": 25,
        "enabled": True,
    },
    "max_global_iterations": {
        "min": 0,
        "group": "Optimization",
        "label": "Max iterations",
        "tooltip": "Number of L2 and IRLS iterations combined",
        "value": 100,
        "enabled": True,
    },
    "max_line_search_iterations": {
        "group": "Optimization",
        "label": "Maximum number of line searches",
        "value": 20,
        "enabled": True,
    },
    "max_cg_iterations": {
        "min": 0,
        "group": "Optimization",
        "label": "Maximum CG iterations",
        "value": 30,
        "enabled": True,
    },
    "initial_beta_ratio": {
        "min": 0.0,
        "group": "Optimization",
        "optional": True,
        "enabled": True,
        "dependency": "initial_beta",
        "dependencyType": "disabled",
        "label": "Initial beta ratio",
        "value": 100.0,
    },
    "initial_beta": {
        "min": 0.0,
        "group": "Optimization",
        "optional": True,
        "enabled": False,
        "dependency": "initial_beta_ratio",
        "dependencyType": "disabled",
        "label": "Initial beta",
        "value": 1.0,
    },
    "tol_cg": {
        "min": 0,
        "group": "Optimization",
        "label": "Conjugate gradient tolerance",
        "value": 1e-4,
        "enabled": True,
    },
    "alpha_s": {
        "min": 0.0,
        "group": "Regularization",
        "label": "Smallness weight",
        "value": 1.0,
        "enabled": True,
    },
    "alpha_x": {
        "min": 0.0,
        "group": "Regularization",
        "label": "X-smoothness weight",
        "value": 1.0,
        "enabled": True,
    },
    "alpha_y": {
        "min": 0.0,
        "group": "Regularization",
        "label": "Y-smoothness weight",
        "value": 1.0,
        "enabled": True,
    },
    "alpha_z": {
        "min": 0.0,
        "group": "Regularization",
        "label": "Z-smoothness weight",
        "value": 1.0,
        "enabled": True,
    },
    "s_norm": {
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "label": "Smallness norm",
        "value": 0.0,
        "enabled": True,
    },
    "x_norm": {
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "label": "X-smoothness norm",
        "value": 2.0,
        "enabled": True,
    },
    "y_norm": {
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "label": "Y-smoothness norm",
        "value": 2.0,
        "enabled": True,
    },
    "z_norm": {
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "label": "Z-smoothness norm",
        "value": 2.0,
        "enabled": True,
    },
    "reference_model_object": {
        "group": "Regularization",
        "label": "Reference model object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
            "{b020a277-90e2-4cd7-84d6-612ee3f25051}",
            "{4ea87376-3ece-438b-bf12-3479733ded46}",
        ],
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "reference_model": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Regularization",
        "isValue": True,
        "parent": "reference_model_object",
        "dependency": "reference_model_object",
        "dependencyType": "enabled",
        "label": "Reference model value",
        "property": None,
        "optional": True,
        "value": 0.0,
    },
    "gradient_type": {
        "choiceList": ["total", "components"],
        "group": "Regularization",
        "label": "Gradient type",
        "value": "total",
    },
    "lower_bound_object": {
        "group": "Regularization",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
            "{b020a277-90e2-4cd7-84d6-612ee3f25051}",
            "{4ea87376-3ece-438b-bf12-3479733ded46}",
        ],
        "label": "Lower bound object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "lower_bound": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Regularization",
        "isValue": False,
        "parent": "lower_bound_object",
        "dependency": "lower_bound_object",
        "dependencyType": "enabled",
        "label": "Lower bound",
        "property": None,
        "optional": True,
        "value": 0.0,
    },
    "upper_bound_object": {
        "group": "Regularization",
        "label": "Upper bound object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
            "{b020a277-90e2-4cd7-84d6-612ee3f25051}",
            "{4ea87376-3ece-438b-bf12-3479733ded46}",
        ],
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "upper_bound": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Regularization",
        "isValue": False,
        "parent": "upper_bound_object",
        "dependency": "lower_bound_object",
        "label": "Upper bound",
        "property": None,
        "optional": True,
        "value": 0.0,
    },
    "parallelized": {
        "group": "Compute",
        "label": "Use parallelization",
        "value": True,
    },
    "n_cpu": {
        "min": 1,
        "group": "Compute",
        "dependency": "parallelized",
        "dependencyType": "enabled",
        "optional": True,
        "enabled": False,
        "label": "Number of cpu",
        "value": 1,
    },
    "max_ram": None,
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "geoh5": None,
    "run_command": "geoapps.inversion.driver",
    "run_command_boolean": {
        "value": False,
        "label": "Run python module ",
        "tooltip": "Warning: launches process to run python model on save",
        "main": True,
    },
    "conda_environment": "geoapps",
    "distributed_workers": None,
}

######################## Validations ###########################

validations = {
    "topography_object": {
        "types": [str, UUID, Surface, Points, Grid2D, Curve],
    },
    "alpha_s": {"types": [int, float]},
    "alpha_x": {"types": [int, float]},
    "alpha_y": {"types": [int, float]},
    "alpha_z": {"types": [int, float]},
    "norm_s": {"types": [int, float]},
    "norm_x": {"types": [int, float]},
    "norm_y": {"types": [int, float]},
    "norm_z": {"types": [int, float]},
}
