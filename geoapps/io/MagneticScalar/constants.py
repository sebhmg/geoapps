#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from uuid import UUID

from geoh5py.data import FloatData
from geoh5py.groups import ContainerGroup
from geoh5py.objects import Grid2D, Points, Surface

from geoapps.io.Inversion.constants import default_ui_json as base_default_ui_json
from geoapps.io.Inversion.constants import validations as base_validations

################# defaults ##################

inversion_defaults = {
    "title": "SimPEG Magnetic Susceptibility Inversion",
    "inversion_type": "magnetic scalar",
    "geoh5": None,  # Must remain at top of list for notebook app initialization
    "forward_only": False,
    "inducing_field_strength": 50000.0,
    "inducing_field_inclination": 90.0,
    "inducing_field_declination": 0.0,
    "topography_object": None,
    "topography": None,
    "data_object": None,
    "tmi_channel": None,
    "tmi_uncertainty": 1.0,
    "bxx_channel": None,
    "bxx_uncertainty": 1.0,
    "bxy_channel": None,
    "bxy_uncertainty": 1.0,
    "bxz_channel": None,
    "bxz_uncertainty": 1.0,
    "byy_channel": None,
    "byy_uncertainty": 1.0,
    "byz_channel": None,
    "byz_uncertainty": 1.0,
    "bzz_channel": None,
    "bzz_uncertainty": 1.0,
    "bx_channel": None,
    "bx_uncertainty": 1.0,
    "by_channel": None,
    "by_uncertainty": 1.0,
    "bz_channel": None,
    "bz_uncertainty": 1.0,
    "starting_model_object": None,
    "starting_model": None,
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
    "sens_wts_threshold": 0.0,
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
    "initial_beta_ratio": 10.0,
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
    "reference_model": 0.0,
    "gradient_type": "total",
    "lower_bound_object": None,
    "lower_bound": None,
    "upper_bound_object": None,
    "upper_bound": None,
    "parallelized": True,
    "n_cpu": None,
    "max_ram": None,
    "out_group": "SusceptibilityInversion",
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "run_command": "geoapps.drivers.magnetic_scalar_inversion",
    "run_command_boolean": False,
    "conda_environment": "geoapps",
    "distributed_workers": None,
    "tmi_channel_bool": False,
    "bxx_channel_bool": False,
    "bxy_channel_bool": False,
    "bxz_channel_bool": False,
    "byy_channel_bool": False,
    "byz_channel_bool": False,
    "bzz_channel_bool": False,
    "bx_channel_bool": False,
    "by_channel_bool": False,
    "bz_channel_bool": False,
}
forward_defaults = {
    "title": "SimPEG Magnetic Susceptibility Forward",
    "inversion_type": "magnetic scalar",
    "geoh5": None,  # Must remain at top of list for notebook app initialization
    "forward_only": True,
    "inducing_field_strength": 50000.0,
    "inducing_field_inclination": 90.0,
    "inducing_field_declination": 0.0,
    "topography_object": None,
    "topography": None,
    "data_object": None,
    "tmi_channel_bool": False,
    "bxx_channel_bool": False,
    "bxy_channel_bool": False,
    "bxz_channel_bool": False,
    "byy_channel_bool": False,
    "byz_channel_bool": False,
    "bzz_channel_bool": False,
    "bx_channel_bool": False,
    "by_channel_bool": False,
    "bz_channel_bool": False,
    "starting_model_object": None,
    "starting_model": None,
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
    "parallelized": True,
    "n_cpu": None,
    "out_group": "MagneticScalarForward",
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "run_command": "geoapps.drivers.magnetic_scalar_inversion",
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
    "tmi_channel_bool": False,
    "bxx_channel_bool": False,
    "bxy_channel_bool": False,
    "bxz_channel_bool": False,
    "byy_channel_bool": False,
    "byz_channel_bool": False,
    "bzz_channel_bool": False,
    "bx_channel_bool": False,
    "by_channel_bool": False,
    "bz_channel_bool": False,
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
    "title": "SimPEG Magnetic Susceptibility Inversion",
    "inversion_type": "magnetic scalar",
    "inducing_field_strength": {
        "min": 0.0,
        "main": True,
        "group": "Inducing Field",
        "label": "Strength",
        "value": 50000.0,
    },
    "inducing_field_inclination": {
        "min": 0.0,
        "main": True,
        "group": "Inducing Field",
        "label": "Inclination",
        "value": 90.0,
    },
    "inducing_field_declination": {
        "min": 0.0,
        "main": True,
        "group": "Inducing Field",
        "label": "Declination",
        "value": 0.0,
    },
    "tmi_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use TMI",
        "value": False,
    },
    "tmi_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "TMI channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "tmi_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "TMI uncertainty",
        "parent": "data_object",
        "dependency": "tmi_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "bxx_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Bxx",
        "value": False,
    },
    "bxx_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Bxx channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "bxx_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Bxx uncertainty",
        "parent": "data_object",
        "dependency": "bxx_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "bxy_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Bxy",
        "value": False,
    },
    "bxy_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Bxy channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "bxy_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Bxy uncertainty",
        "parent": "data_object",
        "dependency": "bxy_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "bxz_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Bxz",
        "value": False,
    },
    "bxz_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Bxz channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "bxz_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Bxz uncertainty",
        "parent": "data_object",
        "dependency": "bxz_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "byy_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Byy",
        "value": False,
    },
    "byy_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Byy channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "byy_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Byy uncertainty",
        "parent": "data_object",
        "dependency": "byy_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "byz_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Byz",
        "value": False,
    },
    "byz_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Byz channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "byz_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Byz uncertainty",
        "parent": "data_object",
        "dependency": "byz_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "bzz_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Bzz",
        "value": False,
    },
    "bzz_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Bzz channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "bzz_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Bzz uncertainty",
        "parent": "data_object",
        "dependency": "bzz_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "bx_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Bx",
        "value": False,
    },
    "bx_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Bx channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "bx_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Bx uncertainty",
        "parent": "data_object",
        "dependency": "bx_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "by_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use By",
        "value": False,
    },
    "by_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "By channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "by_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "By uncertainty",
        "parent": "data_object",
        "dependency": "by_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "bz_channel_bool": {
        "group": "Data",
        "main": True,
        "label": "Use Bz",
        "value": False,
    },
    "bz_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Bz channel",
        "parent": "data_object",
        "optional": True,
        "enabled": False,
        "value": None,
    },
    "bz_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Bz uncertainty",
        "parent": "data_object",
        "dependency": "bz_channel",
        "dependencyType": "enabled",
        "property": None,
        "value": 1.0,
    },
    "starting_model": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Starting Model",
        "main": True,
        "isValue": False,
        "parent": "starting_model_object",
        "label": "Susceptibility (SI)",
        "property": None,
        "value": 0.0,
    },
    "out_group": {"label": "Results group name", "value": "SusceptibilityInversion"},
}

default_ui_json = dict(base_default_ui_json, **default_ui_json)


################ Validations #################

validations = {
    "inversion_type": {
        "required": True,
        "values": ["magnetic scalar"],
    },
    "data_object": {"types": [str, UUID, Points, Surface, Grid2D]},
}

validations = dict(base_validations, **validations)

app_initializer = {
    "geoh5": "../../assets/FlinFlon.geoh5",
    "forward_only": False,
    "data_object": UUID("{538a7eb1-2218-4bec-98cc-0a759aa0ef4f}"),
    "tmi_channel_bool": True,
    "tmi_channel": UUID("{44822654-b6ae-45b0-8886-2d845f80f422}"),
    "tmi_uncertainty": 10,
    "inducing_field_strength": 60000.0,
    "inducing_field_inclination": 79.0,
    "inducing_field_declination": 11.0,
    "u_cell_size": 25.0,
    "v_cell_size": 25.0,
    "w_cell_size": 25.0,
    "resolution": 50.0,
    "octree_levels_topo": [0, 0, 4, 4],
    "octree_levels_obs": [4, 4, 4, 4],
    "depth_core": 500.0,
    "horizontal_padding": 1000.0,
    "vertical_padding": 1000.0,
    "window_center_x": 314600.0,
    "window_center_y": 6072300.0,
    "window_width": 1000.0,
    "window_height": 1500.0,
    "window_azimuth": 0.0,
    "s_norm": 0.0,
    "x_norm": 2.0,
    "y_norm": 2.0,
    "z_norm": 2.0,
    "starting_model": 1e-4,
    "max_iterations": 25,
    "topography_object": UUID("{ab3c2083-6ea8-4d31-9230-7aad3ec09525}"),
    "topography": UUID("{a603a762-f6cb-4b21-afda-3160e725bf7d}"),
    "z_from_topo": True,
    "receivers_offset_x": 0.0,
    "receivers_offset_y": 0.0,
    "receivers_offset_z": 60.0,
    "out_group": "ScalarInversion",
}
