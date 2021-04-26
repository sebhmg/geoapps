#  Copyright (c) 2021 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

import numpy as np

required_parameters = [
    "inversion_type",
    "workspace",
    "out_group",
    "data",
    "mesh",
    "topography",
]

default_ui_json = {
    "forward_only": {
        "default": False,
        "main": True,
        "label": "forward model only?",
        "value": False,
        "enabled": True,
    },
    "inducing_field_strength": {
        "association": "Vertex",
        "dataType": "Float",
        "default": None,
        "min": 0.0,
        "main": True,
        "group": "Inducing Field",
        "enabled": True,
        "isValue": True,
        "label": "Strength",
        "parent": "data_object",
        "property": None,
        "value": 50000.0,
    },
    "inducing_field_inclination": {
        "association": "Vertex",
        "dataType": "Float",
        "default": None,
        "min": 0.0,
        "main": True,
        "group": "Inducing Field",
        "enabled": True,
        "isValue": True,
        "label": "Inclination",
        "parent": "data_object",
        "property": "",
        "value": 90.0,
    },
    "inducing_field_declination": {
        "association": "Vertex",
        "dataType": "Float",
        "default": None,
        "min": 0.0,
        "main": True,
        "group": "Inducing Field",
        "enabled": True,
        "isValue": True,
        "parent": "data_object",
        "label": "Declination",
        "property": "",
        "value": 0.0,
    },
    "topography_object": {
        "default": None,
        "enabled": True,
        "main": True,
        "group": "Topography",
        "label": "Object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
        ],
        "value": None,
    },
    "topography": {
        "association": "Vertex",
        "dataType": "Float",
        "default": None,
        "group": "Topography",
        "enabled": True,
        "main": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "isValue": False,
        "label": "Elevation",
        "parent": "topography_object",
        "property": None,
        "value": 0.0,
    },
    "data_object": {
        "default": None,
        "enabled": True,
        "main": True,
        "group": "Receivers",
        "label": "Object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
        ],
        "value": None,
    },
    "data_channel": {
        "association": "Vertex",
        "dataType": "Float",
        "default": None,
        "group": "Data",
        "main": True,
        "enabled": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "Channel",
        "parent": "data_object",
        "value": None,
    },
    "uncertainty": {
        "association": "Vertex",
        "dataType": "Float",
        "default": None,
        "group": "Data",
        "main": True,
        "enabled": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "isValue": True,
        "label": "Uncertainty",
        "parent": "data_object",
        "property": None,
        "value": 1.0,
    },
    "starting_model_object": {
        "default": "",
        "group": "Starting Model",
        "enabled": True,
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
        ],
        "label": "starting model object",
        "value": "",
    },
    "starting_inclination_object": {
        "default": "",
        "group": "Starting Model",
        "enabled": True,
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
        ],
        "label": "starting inclination object",
        "value": "",
    },
    "starting_declination_object": {
        "default": "",
        "group": "Starting Model",
        "enabled": True,
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
        ],
        "label": "starting declination object",
        "value": "",
    },
    "starting_model": {
        "association": "Cell",
        "dataType": "Float",
        "default": 0.0,
        "group": "Starting Model",
        "enabled": True,
        "isValue": False,
        "parent": "starting_model_object",
        "label": "starting model value",
        "property": "",
        "value": 0.0,
    },
    "starting_inclination": {
        "association": "Cell",
        "dataType": "Float",
        "default": 0.0,
        "group": "Starting Model",
        "enabled": True,
        "isValue": False,
        "parent": "starting_inclination_object",
        "label": "starting inclination value",
        "property": "",
        "value": 0.0,
    },
    "starting_declination": {
        "association": "Cell",
        "dataType": "Float",
        "default": 0.0,
        "group": "Starting Model",
        "enabled": True,
        "isValue": False,
        "parent": "starting_declination_object",
        "label": "starting declination value",
        "property": "",
        "value": 0.0,
    },
    "receivers_radar_drape": {
        "association": "Vertex",
        "dataType": "Float",
        "default": None,
        "main": True,
        "group": "Receivers Options",
        "enabled": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "drape receivers with radar channel",
        "parent": "data_object",
        "value": None,
    },
    "receivers_offset": {
        "default": None,
        "group": "Receivers Options",
        "main": True,
        "optional": True,
        "enabled": False,
        "visible": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "constant receiver offset",
        "value": 0,
    },
    "gps_receivers_offset": {
        "association": "Vertex",
        "dataType": "Float",
        "default": None,
        "group": "Receivers Options",
        "enabled": False,
        "visible": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "isValue": True,
        "label": "set data offsets",
        "parent": "data_object",
        "property": None,
        "value": 0.0,
    },
    "ignore_values": {
        "default": None,
        "group": "Data Options",
        "optional": True,
        "enabled": False,
        "visible": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "values to ignore",
        "value": None,
    },
    "resolution": {
        "min": 0.0,
        "default": None,
        "group": "Data Options",
        "optional": True,
        "enabled": False,
        "visible": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "resolution",
        "value": 0.0,
    },
    "detrend_order": {
        "choiceList": [0, 1, 2],
        "default": 0,
        "optional": True,
        "enabled": False,
        "visible": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "group": "Data Options",
        "label": "detrend order",
        "value": 0,
    },
    "detrend_type": {
        "choiceList": ["all", "corners"],
        "default": "all",
        "group": "Data Options",
        "dependency": "detrend_order",
        "dependencyType": "show",
        "enabled": True,
        "visible": False,
        "label": "detrend type",
        "value": "all",
    },
    "max_chunk_size": {
        "default": 128,
        "min": 0,
        "group": "Data Options",
        "optional": True,
        "enabled": False,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "maximum chunk size",
        "value": 128,
    },
    "chunk_by_rows": {
        "default": False,
        "group": "Data Options",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "chunk by rows?",
        "value": False,
    },
    "output_tile_files": {
        "default": False,
        "group": "Data Options",
        "enabled": True,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "output tile files?",
        "value": False,
    },
    "mesh": {
        "default": None,
        "enabled": True,
        "group": "Mesh",
        "label": "mesh",
        "meshType": "4EA87376-3ECE-438B-BF12-3479733DED46",
        "value": None,
    },
    "mesh_from_params": {
        "default": False,
        "group": "Mesh",
        "enabled": True,
        "label": "build from parameters?",
        "value": False,
    },
    "core_cell_size": {
        "default": None,
        "min": 0,
        "group": "Mesh",
        "enabled": True,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "label": "core cell size",
        "value": 2,
    },
    "octree_levels_topo": {
        "default": [0, 1],
        "group": "Mesh",
        "enabled": False,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "optional": True,
        "label": "octree levels topography",
        "value": [0, 1],
    },
    "octree_levels_obs": {
        "default": [5, 5],
        "group": "Mesh",
        "enabled": False,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "optional": True,
        "label": "octree levels observations",
        "value": [5, 5],
    },
    "octree_levels_padding": {
        "default": [2, 2],
        "group": "Mesh",
        "enabled": False,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "optional": True,
        "label": "octree levels padding",
        "value": [2, 2],
    },
    "depth_core": {
        "default": 100,
        "min": 0,
        "group": "Mesh",
        "enabled": False,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "optional": True,
        "label": "depth of core refinement volume",
        "value": 0,
    },
    "max_distance": {
        "default": np.inf,
        "min": 0,
        "group": "Mesh",
        "enabled": False,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "optional": True,
        "label": "maximum padding distance",
        "value": np.inf,
    },
    "padding_distance_x": {
        "default": [0, 0],
        "group": "Mesh",
        "enabled": False,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "label": "padding distance in x",
        "optional": True,
        "value": [0, 0],
    },
    "padding_distance_y": {
        "default": [0, 0],
        "group": "Mesh",
        "enabled": False,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "label": "padding distance in y",
        "optional": True,
        "value": [0, 0],
    },
    "padding_distance_z": {
        "default": [0, 0],
        "group": "Mesh",
        "enabled": False,
        "visible": False,
        "dependency": "mesh_from_params",
        "dependencyType": "show",
        "label": "padding distance in z",
        "optional": True,
        "value": [0, 0],
    },
    "window_center_x": {
        "default": 0,
        "group": "window",
        "visible": False,
        "enabled": False,
        "label": "window center easting",
        "value": 0,
    },
    "window_center_y": {
        "default": 0,
        "group": "window",
        "visible": False,
        "enabled": False,
        "label": "window center northing",
        "value": 0,
    },
    "window_width": {
        "default": 0,
        "min": 0,
        "group": "window",
        "visible": False,
        "enabled": False,
        "label": "window width",
        "value": 0,
    },
    "window_height": {
        "default": 0,
        "min": 0,
        "group": "window",
        "visible": False,
        "enabled": False,
        "label": "window height",
        "value": 0,
    },
    "window_azimuth": {
        "default": 0,
        "group": "window",
        "visible": False,
        "enabled": False,
        "label": "window azimuth",
        "value": 0,
    },
    "inversion_style": {
        "choiceList": ["voxel"],
        "group": "Optimization",
        "default": "voxel",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "inversion style",
        "value": "voxel",
    },
    "chi_factor": {
        "default": 1.0,
        "min": 0.0,
        "max": 1.0,
        "group": "Optimization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "chi factor",
        "value": 1.0,
    },
    "max_iterations": {
        "default": 10,
        "min": 0,
        "group": "Optimization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "max iteration count",
        "value": 10,
    },
    "max_cg_iterations": {
        "default": 30,
        "min": 0,
        "group": "Optimization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "max conjugate gradient iteration count",
        "value": 30,
    },
    "max_global_iterations": {
        "default": 100,
        "min": 0,
        "group": "Optimization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "max global iteration count",
        "value": 100,
    },
    "initial_beta": {
        "default": 0.0,
        "min": 0.0,
        "group": "Optimization",
        "optional": True,
        "enabled": False,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "initial beta",
        "value": 0.0,
    },
    "initial_beta_ratio": {
        "default": 1e2,
        "min": 0,
        "group": "Optimization",
        "enabled": True,
        "dependency": "initial_beta",
        "dependencyType": "disabled",
        "label": "initial beta ratio",
        "value": 1e2,
    },
    "tol_cg": {
        "default": 1e-4,
        "min": 0,
        "group": "Optimization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "conjugate gradient tolerance",
        "value": 1e-4,
    },
    "alpha_s": {
        "default": 1.0,
        "min": 0.0,
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "smallness weight",
        "value": 1.0,
    },
    "alpha_x": {
        "default": 1.0,
        "min": 0.0,
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "x-smoothness weight",
        "value": 1.0,
    },
    "alpha_y": {
        "default": 1.0,
        "min": 0.0,
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "y-smoothness weight",
        "value": 1.0,
    },
    "alpha_z": {
        "default": 1.0,
        "min": 0.0,
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "z-smoothness weight",
        "value": 1.0,
    },
    "smallness_norm": {
        "default": 2.0,
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "smallness norm",
        "value": 2.0,
    },
    "x_norm": {
        "default": 2.0,
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "x-smoothness norm",
        "value": 2.0,
    },
    "y_norm": {
        "default": 2.0,
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "y-smoothness norm",
        "value": 2.0,
    },
    "z_norm": {
        "default": 2.0,
        "min": 0.0,
        "max": 2.0,
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "z-smoothness norm",
        "value": 2.0,
    },
    "reference_model_object": {
        "default": "",
        "group": "Models",
        "enabled": True,
        "visible": False,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "reference model object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
        ],
        "value": "",
    },
    "reference_inclination_object": {
        "default": "",
        "group": "Models",
        "enabled": True,
        "visible": False,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "reference inclination object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
        ],
        "value": "",
    },
    "reference_declination_object": {
        "enabled": True,
        "group": "Models",
        "visible": False,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "reference declination object",
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
        ],
        "value": "",
    },
    "reference_model": {
        "association": "Cell",
        "dataType": "Float",
        "default": 0.0,
        "group": "Models",
        "enabled": True,
        "isValue": False,
        "visible": False,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "reference model value",
        "parent": "reference_model_object",
        "property": "",
        "value": 0.0,
    },
    "reference_inclination": {
        "association": "Cell",
        "dataType": "Float",
        "default": 0.0,
        "group": "Models",
        "enabled": True,
        "isValue": False,
        "visible": False,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "reference inclination value",
        "parent": "reference_inclination_object",
        "property": "",
        "value": 0.0,
    },
    "reference_declination": {
        "association": "Cell",
        "dataType": "Float",
        "default": 0.0,
        "group": "Models",
        "enabled": True,
        "isValue": False,
        "visible": False,
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "reference declination value",
        "parent": "reference_declination_object",
        "property": "",
        "value": 0.0,
    },
    "gradient_type": {
        "choiceList": ["total", "components"],
        "default": "total",
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "gradient type",
        "value": "total",
    },
    "lower_bound": {
        "default": "-inf",
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "lower bound on model",
        "value": "-inf",
    },
    "upper_bound": {
        "default": "inf",
        "group": "Regularization",
        "dependency": "forward_only",
        "dependencyType": "hide",
        "label": "upper bound on model",
        "value": "inf",
    },
    "parallelized": {
        "default": True,
        "group": "Compute",
        "label": "use parallelization",
        "value": True,
    },
    "n_cpu": {
        "default": 1,
        "min": 1,
        "group": "Compute",
        "dependency": "parallelized",
        "dependencyType": "enabled",
        "optional": True,
        "enabled": False,
        "label": "number of cpu",
        "value": 1,
    },
    "max_ram": {
        "default": 2,
        "min": 0,
        "group": "Compute",
        "dependency": "parallelized",
        "dependencyType": "enabled",
        "optional": True,
        "enabled": False,
        "label": "set RAM limit",
        "value": 2,
    },
    "inversion_type": {
        "default": "mvi",
        "visible": False,
        "enabled": False,
        "label": "inversion Type",
        "value": "mvi",
    },
    "workspace": {
        "default": None,
        "visible": False,
        "enabled": False,
        "label": "path to workspace",
        "value": None,
    },
    "output_geoh5": {
        "default": None,
        "visible": False,
        "enabled": False,
        "label": "path to results geoh5py file",
        "value": None,
    },
    "out_group": {
        "default": None,
        "visible": False,
        "enabled": False,
        "label": "results group name",
        "value": None,
    },
    "no_data_value": {
        "default": None,
        "group": "Data Options",
        "optional": True,
        "enabled": False,
        "visible": False,
        "label": "no data value",
        "value": 0,
    },
    "monitoring_directory": "",
    "workspace_geoh5": "",
    "geoh5": "",
}

defaults = {
    "inversion_type": None,
    "workspace": None,
    "out_group": None,
    "data": None,
    "mesh": None,
    "topography": None,
    "inversion_style": "voxel",
    "forward_only": False,
    "inducing_field_aid": None,
    "core_cell_size": None,
    "octree_levels_topo": [0, 1],
    "octree_levels_obs": [5, 5],
    "octree_levels_padding": [2, 2],
    "depth_core": None,
    "max_distance": np.inf,
    "padding_distance": [[0, 0]] * 3,
    "chi_factor": 1,
    "max_iterations": 10,
    "max_cg_iterations": 30,
    "max_global_iterations": 100,
    "n_cpu": None,
    "max_ram": 2,
    "initial_beta": None,
    "initial_beta_ratio": 1e2,
    "tol_cg": 1e-4,
    "ignore_values": None,
    "no_data_value": 0,
    "resolution": 0,
    "window": None,
    "alphas": [1] * 12,
    "reference_model": None,
    "reference_inclination": None,
    "reference_declination": None,
    "starting_model": None,
    "starting_inclination": None,
    "starting_declination": None,
    "model_norms": [2] * 4,
    "detrend": None,
    "new_uncert": None,
    "output_geoh5": None,
    "receivers_offset": None,
    "gradient_type": "total",
    "lower_bound": -np.inf,
    "upper_bound": np.inf,
    "max_chunk_size": 128,
    "chunk_by_rows": False,
    "output_tile_files": False,
    "parallelized": True,
}


validations = {
    "inversion_type": {
        "values": ["gravity", "magnetics", "mvi", "mvic"],
        "types": [str],
    },
    "data": {
        "types": [dict],
        "reqs": [("workspace",)],
        "name": {
            "types": [str],
        },
        "channels": {
            "types": [dict],
            "tmi": {
                "types": [dict],
                "name": {
                    "types": [str],
                },
                "uncertainties": {
                    "types": [int, float],
                    "shapes": (2,),
                },
                "offsets": {
                    "types": [int, float],
                    "shapes": (3,),
                },
            },
        },
    },
    "out_group": {
        "types": [str],
    },
    "workspace": {
        "types": [str],
    },
    "inversion_style": {
        "values": ["voxel"],
        "types": [str],
    },
    "forward_only": {"types": [bool], "reqs": [(True, "reference_model")]},
    "inducing_field_aid": {
        "types": [int, float],
        "shapes": (3,),
    },
    "core_cell_size": {
        "types": [int, float],
    },
    "octree_levels_topo": {
        "types": [int, float],
    },
    "octree_levels_obs": {
        "types": [int, float],
    },
    "octree_levels_padding": {
        "types": [int, float],
    },
    "depth_core": {
        "types": [dict],
        "value": {
            "types": [int, float],
        },
    },
    "max_distance": {
        "types": [int, float],
    },
    "padding_distance": {
        "types": [int, float],
        "shapes": (3, 2),
    },
    "chi_factor": {
        "types": [int, float],
    },
    "max_iterations": {
        "types": [int, float],
    },
    "max_cg_iterations": {
        "types": [int, float],
    },
    "max_global_iterations": {
        "types": [int, float],
    },
    "n_cpu": {
        "types": [int, float],
    },
    "max_ram": {
        "types": [int, float],
    },
    "initial_beta": {
        "types": [int, float],
    },
    "initial_beta_ratio": {
        "types": [float],
    },
    "tol_cg": {
        "types": [int, float],
    },
    "ignore_values": {
        "types": [str],
    },
    "no_data_value": {
        "types": [int, float],
    },
    "resolution": {
        "types": [int, float],
    },
    "window": {
        "types": [dict],
        "center_x": {
            "types": [int, float],
        },
        "center_y": {
            "types": [int, float],
        },
        "width": {
            "types": [int, float],
        },
        "height": {
            "types": [int, float],
        },
        "azimuth": {
            "types": [int, float],
        },
        "center": {
            "types": [int, float],
        },
        "size": {
            "types": [int, float],
        },
    },
    "alphas": {
        "types": [int, float],
    },
    "reference_model": {
        "types": [str, int, float],
    },
    "reference_inclination": {
        "types": [str, int, float],
    },
    "reference_declination": {
        "types": [str, int, float],
    },
    "starting_model": {
        "types": [str, int, float],
    },
    "starting_inclination": {
        "types": [str, int, float],
    },
    "starting_declination": {
        "types": [str, int, float],
    },
    "model_norms": {
        "types": [int, float],
    },
    "topography": {
        "types": [dict],
        "GA_object": {
            "types": [dict],
            "name": {
                "types": [str],
            },
            "data": {
                "types": [str],
            },
        },
        "constant": {
            "types": [int, float],
        },
        "draped": {
            "types": [int, float],
        },
        "file": {
            "types": [str],
        },
    },
    "detrend": {
        "types": [dict],
        "all": {
            "types": [int, float],
        },
        "corners": {
            "types": [int, float],
        },
    },
    "new_uncert": {"types": [int, float], "shapes": (2,)},
    "mesh": {
        "types": [str],
    },
    "output_geoh5": {
        "types": [str],
    },
    "receivers_offset": {
        "types": [dict],
        "constant": {
            "types": [int, float],
        },
        "constant_drape": {
            "types": [int, float],
        },
        "radar_drape": {
            "types": [int, float, str],
            "shapes": (4,),
        },
    },
    "gradient_type": {"values": ["total", "components"], "types": [str]},
    "lower_bound": {
        "types": [int, float],
    },
    "upper_bound": {
        "types": [int, float],
    },
    "max_chunk_size": {
        "types": [int, float],
    },
    "chunk_by_rows": {
        "types": [bool],
    },
    "output_tile_files": {
        "types": [bool],
    },
    "parallelized": {
        "types": [bool],
    },
}
