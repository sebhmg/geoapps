#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from uuid import UUID

from geoh5py.objects.surveys.electromagnetics.tipper import TipperReceivers

from geoapps.inversion import default_ui_json as base_default_ui_json

################# defaults ##################

inversion_defaults = {
    "title": "SimPEG Tipper inversion",
    "inversion_type": "tipper",
    "geoh5": None,  # Must remain at top of list for notebook app initialization
    "forward_only": False,
    "topography_object": None,
    "topography": None,
    "data_object": None,
    "txz_real_channel": None,
    "txz_real_uncertainty": None,
    "txz_imag_channel": None,
    "txz_imag_uncertainty": None,
    "tyz_real_channel": None,
    "tyz_real_uncertainty": None,
    "tyz_imag_channel": None,
    "tyz_imag_uncertainty": None,
    "starting_model_object": None,
    "starting_model": None,
    "background_conductivity": 1e-5,
    "tile_spatial": 1,
    "output_tile_files": False,
    "z_from_topo": False,
    "receivers_radar_drape": None,
    "receivers_offset_x": 0.0,
    "receivers_offset_y": 0.0,
    "receivers_offset_z": 0.0,
    "gps_receivers_offset": None,
    "ignore_values": None,
    "resolution": None,
    "detrend_order": None,
    "detrend_type": None,
    "max_chunk_size": 128,
    "chunk_by_rows": True,
    "mesh": None,
    "u_cell_size": 25.0,
    "v_cell_size": 25.0,
    "w_cell_size": 25.0,
    "octree_levels_topo": [0, 0, 4, 4],
    "octree_levels_obs": [4, 4, 4, 4],
    "depth_core": 500.0,
    "max_distance": 5000.0,
    "horizontal_padding": 1000.0,
    "vertical_padding": 1000.0,
    "window_center_x": None,
    "window_center_y": None,
    "window_width": None,
    "window_height": None,
    "window_azimuth": None,
    "inversion_style": "voxel",
    "chi_factor": 1.0,
    "sens_wts_threshold": 60.0,
    "every_iteration_bool": False,
    "f_min_change": 1e-4,
    "minGNiter": 1,
    "beta_tol": 0.5,
    "prctile": 95,
    "coolingRate": 1,
    "coolEps_q": True,
    "coolEpsFact": 1.2,
    "beta_search": False,
    "starting_chi_factor": None,
    "max_iterations": 25,
    "max_line_search_iterations": 20,
    "max_cg_iterations": 30,
    "max_global_iterations": 100,
    "initial_beta_ratio": 1e2,
    "initial_beta": None,
    "tol_cg": 1e-4,
    "alpha_s": 1.0,
    "alpha_x": 1.0,
    "alpha_y": 1.0,
    "alpha_z": 1.0,
    "s_norm": 0.0,
    "x_norm": 2.0,
    "y_norm": 2.0,
    "z_norm": 2.0,
    "reference_model_object": None,
    "reference_model": 1e-3,
    "gradient_type": "total",
    "lower_bound_object": None,
    "lower_bound": None,
    "upper_bound_object": None,
    "upper_bound": None,
    "parallelized": True,
    "n_cpu": None,
    "max_ram": None,
    "out_group": "TipperInversion",
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "run_command": "geoapps.inversion.driver",
    "run_command_boolean": False,
    "conda_environment": "geoapps",
    "distributed_workers": None,
    "txz_real_channel_bool": False,
    "txz_imag_channel_bool": False,
    "tyz_real_channel_bool": False,
    "tyz_imag_channel_bool": False,
}

forward_defaults = {
    "title": "SimPEG Tipper Forward",
    "inversion_type": "tipper",
    "geoh5": None,  # Must remain at top of list for notebook app initialization
    "forward_only": True,
    "topography_object": None,
    "topography": None,
    "data_object": None,
    "txz_real_channel_bool": False,
    "txz_imag_channel_bool": False,
    "tyz_real_channel_bool": False,
    "tyz_imag_channel_bool": False,
    "starting_model_object": None,
    "starting_model": None,
    "background_conductivity": 1e-5,
    "tile_spatial": 1,
    "output_tile_files": False,
    "z_from_topo": False,
    "receivers_radar_drape": None,
    "receivers_offset_x": 0.0,
    "receivers_offset_y": 0.0,
    "receivers_offset_z": 0.0,
    "gps_receivers_offset": None,
    "resolution": None,
    "max_chunk_size": 128,
    "chunk_by_rows": True,
    "mesh": None,
    "u_cell_size": 25.0,
    "v_cell_size": 25.0,
    "w_cell_size": 25.0,
    "octree_levels_topo": [16, 8, 4, 2],
    "octree_levels_obs": [4, 4, 4, 4],
    "depth_core": 500.0,
    "max_distance": 5000.0,
    "horizontal_padding": 1000.0,
    "vertical_padding": 1000.0,
    "window_center_x": None,
    "window_center_y": None,
    "window_width": None,
    "window_height": None,
    "window_azimuth": None,
    "parallelized": True,
    "n_cpu": None,
    "out_group": "TipperForward",
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "run_command": "geoapps.inversion.driver",
    "run_command_boolean": False,
    "conda_environment": "geoapps",
    "distributed_workers": None,
    "gradient_type": "total",
    "alpha_s": 1.0,
    "alpha_x": 1.0,
    "alpha_y": 1.0,
    "alpha_z": 1.0,
    "s_norm": 0.0,
    "x_norm": 2.0,
    "y_norm": 2.0,
    "z_norm": 2.0,
}

inversion_ui_json = {
    "txz_real_channel_bool": False,
    "txz_imag_channel_bool": False,
    "tyz_real_channel_bool": False,
    "tyz_imag_channel_bool": False,
}

forward_ui_json = {
    "gradient_type": "total",
    "alpha_s": 1.0,
    "alpha_x": 1.0,
    "alpha_y": 1.0,
    "alpha_z": 1.0,
    "s_norm": 0.0,
    "x_norm": 2.0,
    "y_norm": 2.0,
    "z_norm": 2.0,
}

default_ui_json = {
    "title": "SimPEG Tipper inversion",
    "inversion_type": "tipper",
    "data_object": {
        "main": True,
        "group": "Data",
        "label": "Object",
        "meshType": "{0b639533-f35b-44d8-92a8-f70ecff3fd26}",
        "value": None,
    },
    "txz_real_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Txz real",
        "value": False,
    },
    "txz_real_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "dataGroupType": "Multi-element",
        "main": True,
        "label": "Txz real channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "txz_real_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "dataGroupType": "Multi-element",
        "main": True,
        "label": "Txz real uncertainty",
        "parent": "data_object",
        "dependency": "txz_real_channel",
        "dependencyType": "enabled",
        "value": None,
    },
    "txz_imag_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Txz imaginary",
        "value": False,
    },
    "txz_imag_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "dataGroupType": "Multi-element",
        "main": True,
        "label": "Txz imaginary channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "txz_imag_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "dataGroupType": "Multi-element",
        "main": True,
        "label": "Txz imaginary uncertainty",
        "parent": "data_object",
        "dependency": "txz_imag_channel",
        "dependencyType": "enabled",
        "value": None,
    },
    "tyz_real_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Tyz real",
        "value": False,
    },
    "tyz_real_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "dataGroupType": "Multi-element",
        "main": True,
        "label": "Tyz real channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "tyz_real_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "dataGroupType": "Multi-element",
        "main": True,
        "label": "Tyz real uncertainty",
        "parent": "data_object",
        "dependency": "tyz_real_channel",
        "dependencyType": "enabled",
        "value": None,
    },
    "tyz_imag_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Tyz imaginary",
        "value": False,
    },
    "tyz_imag_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "dataGroupType": "Multi-element",
        "main": True,
        "label": "Tyz imaginary channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "tyz_imag_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "dataGroupType": "Multi-element",
        "main": True,
        "label": "Tyz imaginary uncertainty",
        "parent": "data_object",
        "dependency": "tyz_imag_channel",
        "dependencyType": "enabled",
        "value": None,
    },
    "starting_model": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Starting Model",
        "main": True,
        "isValue": False,
        "parent": "starting_model_object",
        "label": "Conductivity (Siemens/m)",
        "property": None,
        "value": 0.0,
    },
    "background_conductivity": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Starting Model",
        "main": True,
        "isValue": True,
        "parent": "starting_model_object",
        "label": "Background conductivity (Siemens/m)",
        "property": None,
        "value": 0.0,
    },
    "out_group": {"label": "Results group name", "value": "TipperInversion"},
}

default_ui_json = dict(base_default_ui_json, **default_ui_json)


################ Validations #################


validations = {
    "inversion_type": {
        "required": True,
        "values": ["tipper"],
    },
    "data_object": {"required": True, "types": [str, UUID, TipperReceivers]},
}

app_initializer = {}
