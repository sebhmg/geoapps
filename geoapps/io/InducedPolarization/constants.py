#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from uuid import UUID

import numpy as np
from geoh5py.data import FloatData
from geoh5py.objects import Octree
from geoh5py.objects.surveys.direct_current import PotentialElectrode

from geoapps.io.Inversion.constants import default_ui_json as base_default_ui_json
from geoapps.io.Inversion.constants import validations as base_validations

inversion_defaults = {
    "title": "SimPEG Induced Polarization Inversion",
    "inversion_type": "induced polarization",
    "geoh5": None,  # Must remain at top of list for notebook app initialization
    "forward_only": False,
    "topography_object": None,
    "topography": None,
    "data_object": None,
    "chargeability_channel": None,
    "chargeability_uncertainty": 1.0,
    "conductivity_model_object": None,
    "conductivity_model": None,
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
    "inversion_style": "voxel",
    "chi_factor": 1.0,
    "sens_wts_threshold": 1e-3,
    "every_iteration_bool": False,
    "f_min_change": 1e-4,
    "minGNiter": 1,
    "beta_tol": 0.5,
    "prctile": 50,
    "coolingRate": 1,
    "coolEps_q": True,
    "coolEpsFact": 1.2,
    "beta_search": False,
    "starting_chi_factor": None,
    "max_iterations": 25,
    "max_line_search_iterations": 20,
    "max_cg_iterations": 30,
    "max_global_iterations": 100,
    "initial_beta_ratio": 1e1,
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
    "reference_model": None,
    "gradient_type": "total",
    "lower_bound_object": None,
    "lower_bound": None,
    "upper_bound_object": None,
    "upper_bound": None,
    "parallelized": True,
    "n_cpu": None,
    "max_ram": None,
    "out_group": "InducedPolarizationInversion",
    "no_data_value": None,
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "run_command": "geoapps.drivers.induced_polarization_inversion",
    "run_command_boolean": False,
    "conda_environment": "geoapps",
    "distributed_workers": None,
    "chargeability_channel_bool": True,
}

forward_defaults = {
    "title": "SimPEG Induced Polarization Forward",
    "inversion_type": "induced polarization",
    "geoh5": None,  # Must remain at top of list for notebook app initialization
    "forward_only": True,
    "topography_object": None,
    "topography": None,
    "data_object": None,
    "chargeability_channel_bool": True,
    "conductivity_model_object": None,
    "conductivity_model": None,
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
    "out_group": "InducedPolarizationForward",
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "run_command": "geoapps.drivers.induced_polarization_inversion",
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
    "chargeability_channel_bool": True,
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
    "title": "SimPEG Induced Polarization Inversion",
    "inversion_type": "induced polarization",
    "data_object": {
        "main": True,
        "group": "Data",
        "label": "Object",
        "meshType": "{275ecee9-9c24-4378-bf94-65f3c5fbe163}",
        "value": None,
    },
    "chargeability_channel_bool": True,
    "chargeability_channel": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "label": "Chargeability channel",
        "parent": "data_object",
        "value": None,
    },
    "chargeability_uncertainty": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Data",
        "main": True,
        "isValue": True,
        "label": "Chargeability uncertainty",
        "parent": "data_object",
        "property": None,
        "value": 1.0,
    },
    "starting_model_object": {
        "group": "Starting Models",
        "main": True,
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
            "{b020a277-90e2-4cd7-84d6-612ee3f25051}",
            "{4ea87376-3ece-438b-bf12-3479733ded46}",
        ],
        "label": "Chargeability object",
        "value": None,
    },
    "starting_model": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Starting Models",
        "main": True,
        "isValue": False,
        "parent": "starting_model_object",
        "label": "Chargeability (V/V)",
        "property": None,
        "value": 0.0,
    },
    "conductivity_model_object": {
        "group": "Starting Models",
        "main": True,
        "meshType": [
            "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
            "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
            "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
            "{48F5054A-1C5C-4CA4-9048-80F36DC60A06}",
            "{b020a277-90e2-4cd7-84d6-612ee3f25051}",
            "{4EA87376-3ECE-438B-BF12-3479733DED46}",
        ],
        "label": "Conductivity object",
        "value": None,
    },
    "conductivity_model": {
        "association": ["Cell", "Vertex"],
        "dataType": "Float",
        "group": "Starting Models",
        "main": True,
        "isValue": False,
        "parent": "conductivity_model_object",
        "label": "Conductivity (Siemens/m)",
        "property": None,
        "value": 0.0,
    },
    "out_group": {"label": "Results group name", "value": "InducedPolarization"},
}

default_ui_json = dict(base_default_ui_json, **default_ui_json)


################ Validations ##################

validations = {
    "inversion_type": {
        "required": True,
        "values": ["induced polarization"],
    },
    "data_object": {"types": [UUID, PotentialElectrode]},
    "chargeability_channel_bool": {"types": [bool]},
    "chargeability_channel": {
        "types": [str, UUID, FloatData, type(None)],
    },
    "chargeability_uncertainty": {
        "types": [str, int, float, UUID, FloatData, type(None)]
    },
    "conductivity_model_object": {
        "types": [str, UUID, Octree],
    },
    "conductivity_model": {
        "required": True,
        "types": [str, UUID, FloatData, int, float],
    },
}

validations = dict(base_validations, **validations)

app_initializer = {
    "geoh5": "../../assets/FlinFlon_dcip.geoh5",
    "data_object": UUID("{6e14de2c-9c2f-4976-84c2-b330d869cb82}"),
    "chargeability_channel_bool": True,
    "chargeability_channel": UUID("{162320e6-2b80-4877-9ec1-a8f5b6a13673}"),
    "chargeability_uncertainty": 0.001,
    "starting_model": 1e-4,
    "conductivity_model": 0.1,
    "u_cell_size": 25.0,
    "v_cell_size": 25.0,
    "w_cell_size": 25.0,
    "resolution": 25,
    "window_center_x": None,
    "window_center_y": None,
    "window_width": None,
    "window_height": None,
    "window_azimuth": None,
    "octree_levels_topo": [16, 8, 4, 2],
    "octree_levels_obs": [4, 4, 4, 4],
    "depth_core": 1200.0,
    "horizontal_padding": 1000.0,
    "vertical_padding": 1000.0,
    "s_norm": 0.0,
    "x_norm": 2.0,
    "y_norm": 2.0,
    "z_norm": 2.0,
    "max_iterations": 25,
    "topography_object": UUID("{ab3c2083-6ea8-4d31-9230-7aad3ec09525}"),
    "topography": UUID("{a603a762-f6cb-4b21-afda-3160e725bf7d}"),
    "z_from_topo": True,
    "receivers_offset_x": 0,
    "receivers_offset_y": 0,
    "receivers_offset_z": 0,
    "out_group": "InducedPolarizationInversion",
}
