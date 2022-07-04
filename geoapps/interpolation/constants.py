#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from copy import deepcopy

from geoh5py.ui_json.constants import default_ui_json as base_ui_json

defaults = {
    "title": "Data Transfer",
    "geoh5": None,
    "objects": None,
    "data": None,
    "method": None,
    "skew_angle": None,
    "skew_factor": None,
    "space": None,
    "max_distance": None,
    "xy_extent": None,
    "topography_options": None,
    "topography_objects": None,
    "topography_data": None,
    "topography_constant": None,
    "max_depth": None,
    "no_data_value": None,
    "out_object": None,
    "ga_group_name": None,
    "run_command": "geoapps.interpolation.driver",
    "run_command_boolean": False,
    "workspace_geoh5": None,
    "conda_environment": "geoapps",
    "conda_environment_boolean": False,
}

default_ui_json = deepcopy(base_ui_json)
default_ui_json.update(
    {
        "title": "Data Transfer",
        "geoh5": "",
        "run_command": "geoapps.interpolation.driver",
        "run_command_boolean": {
            "value": False,
            "label": "Run python module ",
            "tooltip": "Warning: launches process to run python model on save",
            "main": True,
        },
        "monitoring_directory": "",
        "conda_environment": "geoapps",
        "conda_environment_boolean": False,
        "objects": {
            "meshType": [
                "{2e814779-c35f-4da0-ad6a-39a6912361f9}",
                "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
                "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
                "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
                "{4EA87376-3ECE-438B-BF12-3479733DED46}",
                "{48f5054a-1c5c-4ca4-9048-80f36dc60a06}",
            ],
            "main": True,
            "group": "Data Selection",
            "label": "Object",
            "value": None,
        },
        "data": {
            "main": True,
            "group": "Data Selection",
            "association": ["Vertex", "Cell"],
            "dataType": "Float",
            "label": "Data",
            "parent": "objects",
            "value": None,
        },
        "method": {
            "main": False,
            "group": "Method",
            "groupOptional": True,
            "choiceList": ["Nearest", "Inverse Distance"],
            "value": "Inverse Distance",
            "label": "Method",
        },
        "skew_angle": {
            "main": False,
            "group": "Method",
            "groupOptional": True,
            "value": 0.0,
            "label": "Azimuth (d.dd)",
        },
        "skew_factor": {
            "main": False,
            "group": "Method",
            "groupOptional": True,
            "value": 1.0,
            "label": "Factor (>0)",
        },
        "space": {
            "main": False,
            "group": "Scaling",
            "groupOptional": True,
            "value": "Log",
            "choiceList": ["Linear", "Log"],
            "label": "Scaling",
        },
        "max_distance": {
            "main": False,
            "group": "Horizontal Extent",
            "groupOptional": True,
            "value": 0.0,
            "label": "Maximum distance (m)",
        },
        "xy_extent": {
            "meshType": [
                "{2e814779-c35f-4da0-ad6a-39a6912361f9}",
                "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
                "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
                "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
                "{4EA87376-3ECE-438B-BF12-3479733DED46}",
                "{48f5054a-1c5c-4ca4-9048-80f36dc60a06}",
            ],
            "main": False,
            "group": "Horizontal Extent",
            "label": "Object hull",
            "value": None,
        },
        "topography_options": {
            "main": False,
            "group": "Vertical Extent",
            "groupOptional": True,
            "choiceList": ["None", "Object", "Constant"],
            "value": "Object",
            "label": "Define by",
        },
        "topography_objects": {
            "meshType": [
                "{2e814779-c35f-4da0-ad6a-39a6912361f9}",
                "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
                "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
                "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
                "{4EA87376-3ECE-438B-BF12-3479733DED46}",
                "{48f5054a-1c5c-4ca4-9048-80f36dc60a06}",
            ],
            "main": False,
            "group": "Vertical Extent",
            "label": "Object",
            "value": None,
        },
        "topography_data": {
            "main": False,
            "group": "Vertical Extent",
            "association": ["Vertex", "Cell"],
            "dataType": "Float",
            "label": "Data",
            "parent": "topography_objects",
            "value": None,
        },
        "topography_constant": {
            "main": False,
            "group": "Vertical Extent",
            "value": 0.0,
            "label": "Elevation (m)",
        },
        "max_depth": {
            "main": False,
            "group": "Vertical Extent",
            "value": 0.0,
            "label": "Maximum depth (m)",
        },
        "no_data_value": {
            "main": False,
            "group": "No-data-value",
            "groupOptional": True,
            "value": 0.0,
            "label": "No-data-value",
        },
        "out_object": {
            "meshType": [
                "{2e814779-c35f-4da0-ad6a-39a6912361f9}",
                "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
                "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
                "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
                "{4EA87376-3ECE-438B-BF12-3479733DED46}",
                "{48f5054a-1c5c-4ca4-9048-80f36dc60a06}",
            ],
            "main": True,
            "group": "Data Selection",
            "label": "Destination",
            "value": None,
        },
        "ga_group_name": {
            "main": True,
            "label": "Output Label",
            "value": "_Interp",
            "group": "Python run preferences",
        },
    }
)

validations = {}

app_initializer = {
    "geoh5": "../../assets/FlinFlon.geoh5",
    "objects": "{2e814779-c35f-4da0-ad6a-39a6912361f9}",
    "data": ["{f3e36334-be0a-4210-b13e-06933279de25}"],
    "max_distance": 2e3,
    "max_depth": 1e3,
    "method": "Inverse Distance",
    "no_data_value": 1e-8,
    "out_object": "{7450be38-1327-4336-a9e4-5cff587b6715}",
    "skew_angle": 0,
    "skew_factor": 1.0,
    "space": "Log",
    "topography": {
        "options": "Object",
        "objects": "{ab3c2083-6ea8-4d31-9230-7aad3ec09525}",
        "data": "Z",
    },
}

# 3D grid
"""
"core_cell_size": "50, 50, 50",
"depth_core": 500,
"expansion_fact": 1.05,
"new_grid": "InterpGrid",
"out_mode": "To Object",
"padding_distance": "0, 0, 0, 0, 0, 0",
"""
