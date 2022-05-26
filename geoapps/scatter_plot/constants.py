#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from copy import deepcopy

import plotly.express as px
from geoh5py.ui_json.constants import default_ui_json as base_ui_json

defaults = {
    "title": "Scatter Plot",
    "geoh5": None,
    "objects": None,
    "downsampling": None,
    "x": None,
    "x_log": None,
    "x_min": None,
    "x_max": None,
    "x_thresh": None,
    "y": None,
    "y_log": None,
    "y_min": None,
    "y_max": None,
    "y_thresh": None,
    "z": None,
    "z_log": None,
    "z_min": None,
    "z_max": None,
    "z_thresh": None,
    "color": None,
    "color_log": None,
    "color_min": None,
    "color_max": None,
    "color_thresh": None,
    "color_maps": None,
    "size": None,
    "size_log": None,
    "size_min": None,
    "size_max": None,
    "size_thresh": None,
    "size_markers": None,
    "run_command": "geoapps.scatter_plot.driver",
    "run_command_boolean": False,
    "monitoring_directory": None,
    "workspace_geoh5": None,
    "conda_environment": "geoapps",
    "conda_environment_boolean": False,
}

default_ui_json = deepcopy(base_ui_json)
default_ui_json.update(
    {
        "title": "Scatter Plot",
        "geoh5": "",
        "objects": {
            "group": "Data Selection",
            "label": "Object",
            "main": True,
            "meshType": [
                "{202C5DB1-A56D-4004-9CAD-BAAFD8899406}",
                "{6A057FDC-B355-11E3-95BE-FD84A7FFCB88}",
                "{F26FEBA3-ADED-494B-B9E9-B2BBCBE298E1}",
                "{B020A277-90E2-4CD7-84D6-612EE3F25051}",
                "{48f5054a-1c5c-4ca4-9048-80f36dc60a06}",
                "{7CAEBF0E-D16E-11E3-BC69-E4632694AA37}",
            ],
            "value": None,
        },
        "downsampling": {
            "group": "Data Selection",
            "label": "Population Downsampling (%)",
            "main": True,
            "min": 1,
            "max": 100,
            "value": 100,
        },
        "x": {
            "association": ["Vertex"],
            "dataType": "Float",
            "group": "x axis",
            "label": "Data",
            "main": True,
            "parent": "objects",
            "value": None,
        },
        "x_min": {
            "group": "x axis",
            "label": "Min",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "x_max": {
            "group": "x axis",
            "label": "Max",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "x_log": {
            "group": "x axis",
            "label": "Log10",
            "main": True,
            "value": False,
        },
        "x_thresh": {
            "group": "x axis",
            "label": "Threshold",
            "main": True,
            "value": 0.1,
            "dependency": "x_log",
            "dependencyType": "enabled",
        },
        "y": {
            "association": ["Vertex"],
            "dataType": "Float",
            "group": "y axis",
            "label": "Data",
            "main": True,
            "parent": "objects",
            "value": None,
        },
        "y_min": {
            "group": "y axis",
            "label": "Min",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "y_max": {
            "group": "y axis",
            "label": "Max",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "y_log": {
            "group": "y axis",
            "label": "Log10",
            "main": True,
            "value": False,
        },
        "y_thresh": {
            "group": "y axis",
            "label": "Threshold",
            "main": True,
            "value": 0.1,
            "dependency": "y_log",
            "dependencyType": "enabled",
        },
        "z": {
            "association": ["Vertex"],
            "dataType": "Float",
            "group": "z axis",
            "optional": True,
            "enabled": False,
            "label": "Data",
            "main": True,
            "parent": "objects",
            "value": None,
        },
        "z_min": {
            "group": "z axis",
            "label": "Min",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "z_max": {
            "group": "z axis",
            "label": "Max",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "z_log": {
            "group": "z axis",
            "label": "Log10",
            "main": True,
            "value": False,
        },
        "z_thresh": {
            "group": "z axis",
            "label": "Threshold",
            "main": True,
            "value": 0.1,
            "dependency": "z_log",
            "dependencyType": "enabled",
        },
        "color": {
            "association": ["Vertex"],
            "dataType": "Float",
            "group": "Color",
            "optional": True,
            "enabled": False,
            "label": "Data",
            "main": True,
            "parent": "objects",
            "value": None,
        },
        "color_min": {
            "group": "Color",
            "label": "Min",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "color_max": {
            "group": "Color",
            "label": "Max",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "color_log": {
            "group": "Color",
            "label": "Log10",
            "main": True,
            "value": False,
        },
        "color_thresh": {
            "group": "Color",
            "label": "Threshold",
            "main": True,
            "value": 0.1,
            "dependency": "color_log",
            "dependencyType": "enabled",
        },
        "color_maps": {
            "choiceList": px.colors.named_colorscales(),
            "group": "Color",
            "label": "Colormaps",
            "main": True,
            "value": None,
            "enabled": False,
            "optional": True,
        },
        "size": {
            "association": ["Vertex"],
            "dataType": "Float",
            "group": "Size",
            "optional": True,
            "enabled": False,
            "label": "Data",
            "main": True,
            "parent": "objects",
            "value": None,
        },
        "size_min": {
            "group": "Size",
            "label": "Min",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "size_max": {
            "group": "Size",
            "label": "Max",
            "main": True,
            "optional": True,
            "enabled": False,
            "value": 0.0,
            "precision": 1,
            "lineEdit": False,
        },
        "size_log": {
            "group": "Size",
            "label": "Log10",
            "main": True,
            "value": False,
        },
        "size_thresh": {
            "group": "Size",
            "label": "Threshold",
            "main": True,
            "value": 0.1,
            "dependency": "size_log",
            "dependencyType": "enabled",
        },
        "size_markers": {
            "group": "Size",
            "label": "Marker Size",
            "main": True,
            "min": 1,
            "max": 100,
            "value": 1,
            "enabled": False,
            "optional": True,
        },
        "save": {
            "label": "Save as html",
            "main": True,
            "value": False,
            "group": "Python run preferences",
        },
        "conda_environment": "geoapps",
        "run_command": "geoapps.scatter_plot.driver",
    }
)

validations = {}

app_initializer = {
    "geoh5": "../../assets/FlinFlon.geoh5",
    "objects": "{79b719bc-d996-4f52-9af0-10aa9c7bb941}",
    "x": "{cdd7668a-4b5b-49ac-9365-c9ce4fddf733}",
    "x_log": False,
    "x_min": -17.0,
    "x_max": 25.5,
    "y": "{18c2560c-6161-468a-8571-5d9d59649535}",
    "y_log": True,
    "y_min": -17.0,
    "y_max": 29.8,
    "z": "{cb35da1c-7ea4-44f0-8817-e3d80e8ba98c}",
    "z_log": True,
    "z_min": -20.0,
    "z_max": 3200.0,
    "color": "{94a150e8-16d9-4784-a7aa-e6271df3a3ef}",
    "color_log": True,
    "color_min": -17.0,
    "color_max": 640.0,
    "color_maps": "inferno",
    "size": "{41d51965-3670-43ba-8a10-d399070689e3}",
    "size_log": False,
    "size_min": -17.0,
    "size_max": 24.8,
}
