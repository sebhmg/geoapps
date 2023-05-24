#  Copyright (c) 2023 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from __future__ import annotations

from uuid import UUID

from geoh5py.objects import Curve, Grid2D, Points, Surface

import geoapps

default_ui_json = {
    "forward_only": False,
    "topography_object": {
        "main": True,
        "group": "Topography",
        "label": "Topography",
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
        "association": ["Vertex", "Cell"],
        "dataType": "Float",
        "group": "Topography",
        "main": True,
        "optional": True,
        "enabled": False,
        "label": "Elevation channel",
        "tooltip": "Set elevation from channel",
        "parent": "topography_object",
        "value": "",
        "verbose": 2,
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
        ],
        "value": None,
    },
    "starting_model": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Mesh and models",
        "main": True,
        "isValue": True,
        "parent": "mesh",
        "label": "Initial Density (g/cc)",
        "property": None,
        "value": 1e-4,
    },
    "tile_spatial": {
        "group": "Compute",
        "label": "Number of tiles",
        "parent": "data_object",
        "isValue": True,
        "property": None,
        "value": 1,
        "min": 1,
        "max": 1000,
        "verbose": 2,
    },
    "output_tile_files": False,
    "z_from_topo": {
        "group": "Data pre-processing",
        "label": "Take z from topography",
        "tooltip": "Sets survey elevation to topography before any offsets are applied.",
        "value": False,
        "verbose": 3,
    },
    "receivers_offset_z": {
        "group": "Data pre-processing",
        "label": "Z static offset",
        "optional": True,
        "enabled": False,
        "value": 0.0,
        "verbose": 3,
    },
    "receivers_radar_drape": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data pre-processing",
        "label": "Z radar offset",
        "tooltip": "Apply a non-homogeneous offset to survey object from radar channel.",
        "optional": True,
        "parent": "data_object",
        "value": None,
        "enabled": False,
        "verbose": 3,
    },
    "gps_receivers_offset": None,
    "ignore_values": {
        "group": "Data pre-processing",
        "optional": True,
        "enabled": False,
        "label": "Values to ignore",
        "value": None,
        "verbose": 3,
    },
    "resolution": {
        "min": 0.0,
        "group": "Data pre-processing",
        "optional": True,
        "enabled": False,
        "label": "Downsampling resolution",
        "value": 0.0,
        "verbose": 3,
    },
    "detrend_order": {
        "min": 0,
        "group": "Data pre-processing",
        "enabled": False,
        "dependencyType": "enabled",
        "label": "Detrend order",
        "optional": True,
        "value": 0,
        "verbose": 3,
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
        "verbose": 3,
    },
    "mesh": {
        "group": "Mesh and models",
        "main": True,
        "label": "Mesh",
        "meshType": "4EA87376-3ECE-438B-BF12-3479733DED46",
        "value": None,
    },
    "window_center_x": {
        "group": "Data window",
        "enabled": False,
        "groupOptional": True,
        "label": "Window center easting",
        "value": 0.0,
        "verbose": 3,
    },
    "window_center_y": {
        "group": "Data window",
        "enabled": False,
        "label": "Window center northing",
        "value": 0.0,
        "verbose": 3,
    },
    "window_width": {
        "min": 0.0,
        "group": "Data window",
        "enabled": False,
        "label": "Window width",
        "value": 0.0,
        "verbose": 3,
    },
    "window_height": {
        "min": 0.0,
        "group": "Data window",
        "enabled": False,
        "label": "Window height",
        "value": 0.0,
        "verbose": 3,
    },
    "window_azimuth": {
        "min": -180,
        "max": 180,
        "group": "Data window",
        "enabled": False,
        "label": "Window azimuth",
        "value": 0.0,
        "verbose": 3,
    },
    "inversion_style": "voxel",
    "chi_factor": {
        "min": 0.1,
        "max": 20.0,
        "precision": 1,
        "lineEdit": False,
        "group": "Optimization",
        "label": "Chi factor",
        "value": 1.0,
        "enabled": True,
    },
    "sens_wts_threshold": {
        "group": "Update sensitivity weights directive",
        "tooltip": "Update sensitivity weight threshold",
        "label": "Threshold (%)",
        "value": 0.001,
        "max": 1.0,
        "min": 0.0,
        "precision": 4,
        "lineEdit": False,
        "verbose": 2,
    },
    "every_iteration_bool": {
        "group": "Update sensitivity weights directive",
        "tooltip": "Update weights at every iteration",
        "label": "Every iteration",
        "value": False,
        "verbose": 2,
    },
    "f_min_change": {
        "group": "Update IRLS directive",
        "label": "f min change",
        "value": 1e-4,
        "min": 1e-6,
        "verbose": 3,
    },
    "beta_tol": {
        "group": "Update IRLS directive",
        "label": "Beta tolerance",
        "value": 0.5,
        "min": 0.0001,
        "verbose": 3,
    },
    "prctile": {
        "group": "Update IRLS directive",
        "label": "Percentile",
        "value": 95,
        "max": 100,
        "min": 5,
        "verbose": 3,
    },
    "coolEps_q": {
        "group": "Update IRLS directive",
        "label": "Cool epsilon q",
        "value": True,
        "verbose": 3,
    },
    "coolEpsFact": {
        "group": "Update IRLS directive",
        "label": "Cool epsilon fact",
        "value": 1.2,
        "verbose": 3,
    },
    "beta_search": {
        "group": "Update IRLS directive",
        "label": "Perform beta search",
        "value": False,
        "verbose": 3,
    },
    "starting_chi_factor": {
        "group": "Update IRLS directive",
        "label": "IRLS start chi factor",
        "optional": True,
        "enabled": False,
        "value": 1.0,
        "tooltip": "This chi factor will be used to determine the misfit"
        " threshold after which IRLS iterations begin.",
        "verbose": 3,
    },
    "max_global_iterations": {
        "min": 1,
        "lineEdit": False,
        "group": "Optimization",
        "label": "Maximum iterations",
        "tooltip": "Number of L2 and IRLS iterations combined",
        "value": 100,
        "enabled": True,
    },
    "max_irls_iterations": {
        "min": 0,
        "group": "Update IRLS directive",
        "label": "Maximum number of IRLS iterations",
        "tooltip": "Incomplete Re-weighted Least Squares iterations for non-L2 problems",
        "value": 25,
        "enabled": True,
        "verbose": 2,
    },
    "coolingRate": {
        "group": "Optimization",
        "label": "Iterations per beta",
        "value": 2,
        "min": 1,
        "LineEdit": False,
        "max": 10,
        "precision": 1,
        "verbose": 2,
    },
    "coolingFactor": {
        "group": "Optimization",
        "label": "Beta cooling factor",
        "tooltip": "Each beta cooling step will be calculated by dividing the current beta by this factor.",
        "value": 2.0,
        "min": 1.1,
        "max": 100,
        "precision": 1,
        "lineEdit": False,
        "verbose": 2,
    },
    "max_line_search_iterations": {
        "group": "Optimization",
        "label": "Maximum number of line searches",
        "value": 20,
        "min": 1,
        "enabled": True,
        "verbose": 3,
    },
    "max_cg_iterations": {
        "min": 0,
        "group": "Optimization",
        "label": "Maximum CG iterations",
        "value": 30,
        "enabled": True,
        "verbose": 2,
    },
    "initial_beta_ratio": {
        "min": 0.0,
        "precision": 2,
        "group": "Optimization",
        "optional": True,
        "enabled": True,
        "label": "Initial beta ratio",
        "value": 100.0,
        "verbose": 2,
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
        "verbose": 2,
    },
    "tol_cg": {
        "min": 0,
        "group": "Optimization",
        "label": "Conjugate gradient tolerance",
        "value": 1e-4,
        "enabled": True,
        "verbose": 3,
    },
    "alpha_s": {
        "min": 0.0,
        "group": "Regularization",
        "label": "Smallness weight",
        "value": 1.0,
        "tooltip": "Constant ratio compared to other weights. Larger values result in models that remain close to the reference model",
        "enabled": True,
    },
    "alpha_x": {
        "min": 0.0,
        "group": "Regularization",
        "label": "X-smoothness weight",
        "tooltip": "Larger values relative to other smoothness weights will result in x biased smoothness",
        "value": 1.0,
        "enabled": True,
    },
    "alpha_y": {
        "min": 0.0,
        "group": "Regularization",
        "label": "Y-smoothness weight",
        "tooltip": "Larger values relative to other smoothness weights will result in y biased smoothness",
        "value": 1.0,
        "enabled": True,
    },
    "alpha_z": {
        "min": 0.0,
        "group": "Regularization",
        "label": "Z-smoothness weight",
        "tooltip": "Larger values relative to other smoothness weights will result in z biased smoothess",
        "value": 1.0,
        "enabled": True,
    },
    "s_norm": {
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "label": "Smallness norm",
        "value": 0.0,
        "precision": 2,
        "lineEdit": False,
        "enabled": True,
    },
    "x_norm": {
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "label": "X-smoothness norm",
        "value": 2.0,
        "precision": 2,
        "lineEdit": False,
        "enabled": True,
    },
    "y_norm": {
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "label": "Y-smoothness norm",
        "value": 2.0,
        "precision": 2,
        "lineEdit": False,
        "enabled": True,
    },
    "z_norm": {
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "label": "Z-smoothness norm",
        "value": 2.0,
        "precision": 2,
        "lineEdit": False,
        "enabled": True,
    },
    "reference_model": {
        "association": ["Cell", "Vertex"],
        "main": True,
        "dataType": "Float",
        "group": "Mesh and models",
        "isValue": True,
        "parent": "mesh",
        "label": "Reference",
        "property": None,
        "value": 0.0,
    },
    "gradient_type": {
        "choiceList": ["total", "components"],
        "group": "Regularization",
        "label": "Gradient type",
        "value": "total",
        "verbose": 3,
    },
    "lower_bound": {
        "association": ["Cell", "Vertex"],
        "main": True,
        "dataType": "Float",
        "group": "Mesh and models",
        "isValue": True,
        "parent": "mesh",
        "label": "Lower bound",
        "property": None,
        "optional": True,
        "value": -10.0,
        "enabled": False,
    },
    "upper_bound": {
        "association": ["Cell", "Vertex"],
        "main": True,
        "dataType": "Float",
        "group": "Mesh and models",
        "isValue": True,
        "parent": "mesh",
        "label": "Upper bound",
        "property": None,
        "optional": True,
        "value": 10.0,
        "enabled": False,
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
        "label": "Number of CPUs",
        "value": 1,
    },
    "store_sensitivities": {
        "choiceList": ["disk", "ram"],
        "group": "Compute",
        "label": "Storage device",
        "tooltip": "Use disk on a fast local SSD, and RAM elsewhere",
        "value": "ram",
    },
    "max_chunk_size": {
        "min": 0,
        "group": "Compute",
        "optional": True,
        "enabled": True,
        "label": "Maximum chunk size",
        "value": 128,
        "verbose": 3,
    },
    "chunk_by_rows": {
        "group": "Compute",
        "label": "Chunk by rows",
        "value": True,
        "verbose": 3,
    },
    "generate_sweep": {
        "label": "Generate sweep file",
        "group": "Python run preferences",
        "main": True,
        "value": False,
    },
    "max_ram": None,
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "geoh5": None,
    "run_command": "geoapps.inversion.driver",
    "run_command_boolean": None,
    "conda_environment": "geoapps",
    "distributed_workers": None,
    "version": geoapps.__version__,
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
    "distributed_workers": {"types": [str, type(None)]},
    "version": {
        "types": [
            str,
        ]
    },
}
