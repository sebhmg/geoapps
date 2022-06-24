#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from __future__ import annotations

import os
import sys
import time
import webbrowser
from os import environ, makedirs, path

import dash_daq as daq
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback_context, dash_table, dcc, html, no_update
from dash.dependencies import Input, Output
from flask import Flask
from geoh5py.ui_json import InputFile
from geoh5py.workspace import Workspace
from jupyter_dash import JupyterDash
from scipy.spatial import cKDTree
from sklearn.cluster import KMeans

from geoapps.clustering.constants import app_initializer
from geoapps.clustering.params import ClusteringParams
from geoapps.scatter_plot.application import ScatterPlots
from geoapps.shared_utils.utils import colors, hex_to_rgb
from geoapps.utils.statistics import random_sampling


class Clustering(ScatterPlots):
    _param_class = ClusteringParams

    def __init__(self, ui_json=None, **kwargs):
        app_initializer.update(kwargs)
        if ui_json is not None and os.path.exists(ui_json.path):
            self.params = self._param_class(ui_json)
        else:
            self.params = self._param_class(**app_initializer)

        self.clusters = {}
        self.data_channels = {}
        self.kmeans = None
        self.indices = []
        self.mapping = None
        self.color_pickers = colors
        # self.defaults = {}
        # Initial values for the dash components
        super().__init__(**self.params.to_dict())
        self.defaults.update(self.get_cluster_defaults())

        external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
        server = Flask(__name__)
        self.app = JupyterDash(
            server=server,
            url_base_pathname=environ.get("JUPYTERHUB_SERVICE_PREFIX", "/"),
            external_stylesheets=external_stylesheets,
        )

        self.norm_tabs_layout = html.Div(
            id="norm_tabs",
            children=[
                dcc.Tabs(
                    [
                        dcc.Tab(
                            label="Histogram",
                            children=[
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dcc.Markdown("Data: "),
                                                dcc.Dropdown(
                                                    id="channel",
                                                    value=self.defaults["channel"],
                                                    options=self.defaults["channels"],
                                                ),
                                                dcc.Markdown("Scale: "),
                                                dcc.Slider(
                                                    id="scale",
                                                    min=1,
                                                    max=10,
                                                    step=1,
                                                    value=self.defaults["scale"],
                                                    marks=None,
                                                    tooltip={
                                                        "placement": "bottom",
                                                        "always_visible": True,
                                                    },
                                                ),
                                                dcc.Markdown("Lower bound: "),
                                                dcc.Input(
                                                    id="lower_bounds",
                                                    value=self.defaults["lower_bounds"],
                                                ),
                                                dcc.Markdown("Upper bound: "),
                                                dcc.Input(
                                                    id="upper_bounds",
                                                    value=self.defaults["upper_bounds"],
                                                ),
                                            ],
                                            style={
                                                "width": "200px",
                                                "display": "inline-block",
                                                "vertical-align": "middle",
                                                "margin-right": "50px",
                                            },
                                        ),
                                        dcc.Graph(
                                            id="histogram",
                                            style={
                                                "width": "70%",
                                                "display": "inline-block",
                                                "vertical-align": "middle",
                                            },
                                        ),
                                    ]
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Statistics",
                            children=[
                                html.Div(
                                    [
                                        dash_table.DataTable(
                                            id="stats_table",
                                            style_data={
                                                "color": "black",
                                                "backgroundColor": "white",
                                            },
                                            style_data_conditional=[
                                                {
                                                    "if": {"row_index": "odd"},
                                                    "backgroundColor": "rgb(220, 220, 220)",
                                                }
                                            ],
                                            style_header={
                                                "backgroundColor": "rgb(210, 210, 210)",
                                                "color": "black",
                                                "fontWeight": "bold",
                                            },
                                        )
                                    ],
                                    style={"margin-top": "20px"},
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Confusion Matrix",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="matrix",
                                        ),
                                    ],
                                    style={"width": "50%", "margin": "auto"},
                                )
                            ],
                        ),
                    ]
                )
            ],
        )

        self.cluster_tabs_layout = html.Div(
            [
                dcc.Tabs(
                    [
                        dcc.Tab(
                            label="Crossplot",
                            children=[
                                html.Div(
                                    [self.axis_layout],
                                    style={
                                        "width": "45%",
                                        "display": "inline-block",
                                        "vertical-align": "middle",
                                    },
                                ),
                                html.Div(
                                    [
                                        self.plot_layout,
                                    ],
                                    style={
                                        "width": "55%",
                                        "display": "inline-block",
                                        "vertical-align": "middle",
                                    },
                                ),
                            ],
                        ),
                        dcc.Tab(
                            label="Boxplot",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="boxplot",
                                        )
                                    ],
                                    style={"width": "50%", "margin": "auto"},
                                )
                            ],
                        ),
                        dcc.Tab(
                            label="Inertia",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="inertia",
                                        )
                                    ],
                                    style={"width": "50%", "margin": "auto"},
                                )
                            ],
                        ),
                    ]
                )
            ]
        )

        self.app.layout = html.Div(
            [
                html.Div(
                    [
                        self.workspace_layout,
                        dcc.Markdown("Data subset: "),
                        dcc.Dropdown(
                            id="channels",
                            value=self.defaults["channels"],
                            options=self.defaults["channels_options"],
                            multi=True,
                        ),
                    ],
                    style={
                        "width": "40%",
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-right": "50px",
                        "margin-bottom": "20px",
                    },
                ),
                html.Div(
                    [
                        dcc.Markdown("Number of clusters: "),
                        dcc.Slider(
                            id="n_clusters",
                            min=2,
                            max=100,
                            step=1,
                            value=self.defaults["n_clusters"],
                            marks=None,
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True,
                            },
                        ),
                        dcc.Checklist(
                            id="show_color_picker",
                            options=["Select cluster color"],
                            value=[],
                        ),
                        dcc.Checklist(
                            id="live_link",
                            options=["Geoscience ANALYST Pro - Live link"],
                            value=[],
                        ),
                        dcc.Input(id="ga_group", value="test"),
                        html.Button("Export", id="export"),
                        dcc.Markdown(id="export_message"),
                    ],
                    style={
                        "width": "25%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                html.Div(
                    id="color_select_div",
                    children=[
                        dcc.Markdown("Cluster: "),
                        dcc.Dropdown(
                            id="select_cluster",
                            options=np.arange(0, 101, 1),
                            value=0,
                            style={"margin-bottom": "20px"},
                        ),
                        daq.ColorPicker(
                            id="color_picker",
                            value=dict(hex="#000000"),
                        ),
                    ],
                    style={
                        "width": "25%",
                        "display": "inline-block",
                        "vertical-align": "top",
                    },
                ),
                dcc.Checklist(
                    id="show_norm_tabs",
                    options=["Data Normalization"],
                    value=[],
                ),
                self.norm_tabs_layout,
                self.cluster_tabs_layout,
                dcc.Store(id="dataframe", data={}),
                dcc.Store(id="full_scales", data=self.defaults["full_scales"]),
                dcc.Store(
                    id="full_lower_bounds", data=self.defaults["full_lower_bounds"]
                ),
                dcc.Store(
                    id="full_upper_bounds", data=self.defaults["full_upper_bounds"]
                ),
            ],
            style={"width": "70%", "margin-left": "50px", "margin-top": "30px"},
        )

        self.app.callback(
            Output(component_id="x_div", component_property="style"),
            Output(component_id="y_div", component_property="style"),
            Output(component_id="z_div", component_property="style"),
            Output(component_id="color_div", component_property="style"),
            Output(component_id="size_div", component_property="style"),
            Input(component_id="axes_pannels", component_property="value"),
        )(self.update_visibility)
        self.app.callback(
            Output(component_id="color_select_div", component_property="style"),
            Input(component_id="show_color_picker", component_property="value"),
        )(self.update_color_select)
        self.app.callback(
            Output(component_id="norm_tabs", component_property="style"),
            Input(component_id="show_norm_tabs", component_property="value"),
        )(self.update_norm_tabs)

        self.app.callback(
            Output(component_id="objects", component_property="options"),
            Output(component_id="objects", component_property="value"),
            Output(component_id="downsampling", component_property="value"),
            Output(component_id="x", component_property="options"),
            Output(component_id="x", component_property="value"),
            Output(component_id="x_log", component_property="value"),
            Output(component_id="x_thresh", component_property="value"),
            Output(component_id="x_min", component_property="value"),
            Output(component_id="x_max", component_property="value"),
            Output(component_id="y", component_property="options"),
            Output(component_id="y", component_property="value"),
            Output(component_id="y_log", component_property="value"),
            Output(component_id="y_thresh", component_property="value"),
            Output(component_id="y_min", component_property="value"),
            Output(component_id="y_max", component_property="value"),
            Output(component_id="z", component_property="options"),
            Output(component_id="z", component_property="value"),
            Output(component_id="z_log", component_property="value"),
            Output(component_id="z_thresh", component_property="value"),
            Output(component_id="z_min", component_property="value"),
            Output(component_id="z_max", component_property="value"),
            Output(component_id="color", component_property="options"),
            Output(component_id="color", component_property="value"),
            Output(component_id="color_log", component_property="value"),
            Output(component_id="color_thresh", component_property="value"),
            Output(component_id="color_min", component_property="value"),
            Output(component_id="color_max", component_property="value"),
            Output(component_id="color_maps", component_property="value"),
            Output(component_id="size", component_property="options"),
            Output(component_id="size", component_property="value"),
            Output(component_id="size_log", component_property="value"),
            Output(component_id="size_thresh", component_property="value"),
            Output(component_id="size_min", component_property="value"),
            Output(component_id="size_max", component_property="value"),
            Output(component_id="size_markers", component_property="value"),
            Output(component_id="upload", component_property="filename"),
            Output(component_id="upload", component_property="contents"),
            Output(component_id="channel", component_property="options"),
            Output(component_id="channels", component_property="options"),
            Output(component_id="scale", component_property="value"),
            Output(component_id="lower_bounds", component_property="value"),
            Output(component_id="upper_bounds", component_property="value"),
            Output(component_id="color_maps", component_property="options"),
            Output(component_id="color_picker", component_property="value"),
            Output(component_id="dataframe", component_property="data"),
            Output(component_id="full_scales", component_property="data"),
            Output(component_id="full_lower_bounds", component_property="data"),
            Output(component_id="full_upper_bounds", component_property="data"),
            Input(component_id="upload", component_property="filename"),
            Input(component_id="upload", component_property="contents"),
            Input(component_id="objects", component_property="value"),
            Input(component_id="x", component_property="value"),
            Input(component_id="y", component_property="value"),
            Input(component_id="z", component_property="value"),
            Input(component_id="color", component_property="value"),
            Input(component_id="size", component_property="value"),
            Input(component_id="channel", component_property="value"),
            Input(component_id="channels", component_property="value"),
            Input(component_id="scale", component_property="value"),
            Input(component_id="lower_bounds", component_property="value"),
            Input(component_id="upper_bounds", component_property="value"),
            Input(component_id="downsampling", component_property="value"),
            Input(component_id="select_cluster", component_property="value"),
            Input(component_id="n_clusters", component_property="value"),
            Input(component_id="full_scales", component_property="data"),
            Input(component_id="full_lower_bounds", component_property="data"),
            Input(component_id="full_upper_bounds", component_property="data"),
            # prevent_initial_call=True,
        )(self.update_cluster_params)
        self.app.callback(
            Output(component_id="crossplot", component_property="figure"),
            Output(component_id="stats_table", component_property="data"),
            Output(component_id="matrix", component_property="figure"),
            Output(component_id="histogram", component_property="figure"),
            Output(component_id="boxplot", component_property="figure"),
            Output(component_id="inertia", component_property="figure"),
            Input(component_id="n_clusters", component_property="value"),
            Input(component_id="select_cluster", component_property="value"),
            Input(component_id="dataframe", component_property="data"),
            Input(component_id="channel", component_property="value"),
            Input(component_id="downsampling", component_property="value"),
            Input(component_id="x", component_property="value"),
            Input(component_id="x_log", component_property="value"),
            Input(component_id="x_thresh", component_property="value"),
            Input(component_id="x_min", component_property="value"),
            Input(component_id="x_max", component_property="value"),
            Input(component_id="y", component_property="value"),
            Input(component_id="y_log", component_property="value"),
            Input(component_id="y_thresh", component_property="value"),
            Input(component_id="y_min", component_property="value"),
            Input(component_id="y_max", component_property="value"),
            Input(component_id="z", component_property="value"),
            Input(component_id="z_log", component_property="value"),
            Input(component_id="z_thresh", component_property="value"),
            Input(component_id="z_min", component_property="value"),
            Input(component_id="z_max", component_property="value"),
            Input(component_id="color", component_property="value"),
            Input(component_id="color_log", component_property="value"),
            Input(component_id="color_thresh", component_property="value"),
            Input(component_id="color_min", component_property="value"),
            Input(component_id="color_max", component_property="value"),
            Input(component_id="color_maps", component_property="value"),
            Input(component_id="color_picker", component_property="value"),
            Input(component_id="size", component_property="value"),
            Input(component_id="size_log", component_property="value"),
            Input(component_id="size_thresh", component_property="value"),
            Input(component_id="size_min", component_property="value"),
            Input(component_id="size_max", component_property="value"),
            Input(component_id="size_markers", component_property="value"),
        )(self.update_plots)
        self.app.callback(
            Output(component_id="live_link", component_property="value"),
            Input(component_id="export", component_property="n_clicks"),
            Input(component_id="dataframe", component_property="data"),
            Input(component_id="objects", component_property="value"),
            Input(component_id="n_clusters", component_property="value"),
            Input(component_id="ga_group", component_property="value"),
            Input(component_id="live_link", component_property="value"),
            prevent_initial_call=True,
        )(self.export_clusters)

    def get_cluster_defaults(self):
        # Get initial values to initialize the dash components
        defaults = {}
        # If there is no default data subset list, set it from selected scatter plot data
        if self.params.channels is None:
            plot_data = [
                self.defaults["x_name"],
                self.defaults["y_name"],
                self.defaults["z_name"],
                self.defaults["color_name"],
                self.defaults["size_name"],
            ]
            defaults["channels"] = list(filter(None, plot_data))
        else:
            defaults["channels"] = self.params.channels

        if len(defaults["channels"]) > 0:
            defaults["channel"] = defaults["channels"][0]
        else:
            defaults["channel"] = None

        for key, value in self.params.to_dict().items():
            if key != "channels":
                if key == "objects":
                    if value is None:
                        defaults["channels_options"] = []
                    else:
                        channels_options = value.get_data_list()
                        if "Visual Parameters" in channels_options:
                            channels_options.remove("Visual Parameters")
                        defaults["channels_options"] = channels_options
                    for channel in defaults["channels_options"]:
                        self.get_channel(channel)
                elif key in ["full_scales", "full_lower_bounds", "full_upper_bounds"]:
                    out_dict = {}
                    for i in range(len(defaults["channels"])):
                        if getattr(self.params, key) is None:
                            if key == "full_scales":
                                out_dict[defaults["channels"][i]] = 1
                            else:
                                out_dict[defaults["channels"][i]] = None
                        else:
                            out_dict[defaults["channels"][i]] = getattr(
                                self.params, key
                            )[i]
                    defaults[key] = out_dict
                else:
                    defaults[key] = value

        return defaults

    def update_color_select(self, checkbox):
        if not checkbox:
            return {"display": "none"}
        else:
            return {"width": "25%", "display": "inline-block", "vertical-align": "top"}

    def update_norm_tabs(self, checkbox):
        if not checkbox:
            return {"display": "none"}
        else:
            return {"display": "block"}

    def get_data_channels(self, channels):
        data_channels = {}

        for channel in channels:
            if channel not in data_channels.keys():
                if channel == "None":
                    data_channels[channel] = None
                elif self.params.geoh5.get_entity(channel):
                    data_channels[channel] = self.params.geoh5.get_entity(channel)[0]

        return data_channels

    def update_channels(
        self, channel, channels, full_scales, full_lower_bounds, full_upper_bounds
    ):
        self.data_channels = self.get_data_channels(channels)
        channels = list(filter(None, channels))

        for channel in channels:
            dict = self.update_properties(
                channel, full_scales, full_lower_bounds, full_upper_bounds
            )
            full_scales = dict["full_scales"]
            full_lower_bounds = dict["full_lower_bounds"]
            full_upper_bounds = dict["full_upper_bounds"]

        new_scales = {}
        for channel, value in full_scales.items():
            if channel in channels:
                new_scales[channel] = value
        new_lower_bounds = {}
        for channel, value in full_lower_bounds.items():
            if channel in channels:
                new_lower_bounds[channel] = value
        new_upper_bounds = {}
        for channel, value in full_upper_bounds.items():
            if channel in channels:
                new_upper_bounds[channel] = value

        if channel not in channels:
            channel = None

        if self.kmeans is not None:
            data_options = channels + ["kmeans"]
            color_maps_options = px.colors.named_colorscales() + ["kmeans"]
            self.data_channels.update({"kmeans": KMeansData("kmeans", self.kmeans)})
        else:
            data_options = channels
            color_maps_options = px.colors.named_colorscales()
            self.data_channels.pop("kmeans", None)

        return {
            "channel_options": channels,
            "color_maps_options": color_maps_options,
            "data_options": data_options,
            "full_scales": new_scales,
            "full_lower_bounds": new_lower_bounds,
            "full_upper_bounds": new_upper_bounds,
            "channel": channel,
        }

    def update_properties(
        self, channel, full_scales, full_lower_bounds, full_upper_bounds
    ):

        if channel is not None:
            if channel not in full_scales.keys():
                full_scales[channel] = 1
            scale = full_scales[channel]

            if channel not in full_lower_bounds.keys():
                full_lower_bounds[channel] = np.nanmin(
                    self.data_channels[channel].values
                )
            lower_bounds = full_lower_bounds[channel]

            if channel not in full_upper_bounds.keys():
                full_upper_bounds[channel] = np.nanmax(
                    self.data_channels[channel].values
                )
            upper_bounds = full_upper_bounds[channel]
        else:
            scale, lower_bounds, upper_bounds = None, None, None

        return {
            "scale": scale,
            "lower_bounds": lower_bounds,
            "upper_bounds": upper_bounds,
            "full_scales": full_scales,
            "full_lower_bounds": full_lower_bounds,
            "full_upper_bounds": full_upper_bounds,
        }

    def update_cluster_params(
        self,
        filename,
        contents,
        objects,
        x,
        y,
        z,
        color,
        size,
        channel,
        channels,
        scale,
        lower_bounds,
        upper_bounds,
        downsampling,
        select_cluster,
        n_clusters,
        full_scales,
        full_lower_bounds,
        full_upper_bounds,
    ):
        param_list = [
            "objects_options",
            "objects_name",
            "downsampling",
            "data_options",
            "x_name",
            "x_log",
            "x_thresh",
            "x_min",
            "x_max",
            "data_options",
            "y_name",
            "y_log",
            "y_thresh",
            "y_min",
            "y_max",
            "data_options",
            "z_name",
            "z_log",
            "z_thresh",
            "z_min",
            "z_max",
            "data_options",
            "color_name",
            "color_log",
            "color_thresh",
            "color_min",
            "color_max",
            "color_maps",
            "data_options",
            "size_name",
            "size_log",
            "size_thresh",
            "size_min",
            "size_max",
            "size_markers",
            "filename",
            "contents",
            "channel_options",
            "channels_options",
            "scale",
            "lower_bounds",
            "upper_bounds",
            "color_maps_options",
            "color_picker",
            "dataframe",
            "full_scales",
            "full_lower_bounds",
            "full_upper_bounds",
        ]

        trigger = callback_context.triggered[0]["prop_id"].split(".")[0]
        if full_scales is None:
            full_scales = {}
        if full_lower_bounds is None:
            full_lower_bounds = {}
        if full_upper_bounds is None:
            full_upper_bounds = {}

        update_dict = {}
        if trigger == "upload":
            if filename.endswith(".ui.json"):
                # Update params from uploaded uijson
                update_dict = self.update_from_uijson(contents)
            elif filename.endswith(".geoh5"):
                # Update object and data subset options from uploaded workspace
                update_dict = self.update_object_options(contents)
                update_dict.update(
                    {
                        "channels_options": self.update_data_options(objects)[
                            "data_options"
                        ]
                    }
                )
            else:
                print("Uploaded file must be a workspace or ui.json.")
            update_dict["filename"] = None
            update_dict["contents"] = None

        elif trigger == "objects":
            # Update data subset options from object change
            update_dict = {
                "channels_options": self.update_data_options(objects)["data_options"]
            }

        elif trigger == "select_cluster":
            # Update color displayed by the dash colorpicker
            update_dict = self.update_color_picker(select_cluster)
            # Output(component_id="color_picker", component_property="value"),

        elif trigger in ["x", "y", "z", "color", "size"]:
            # Update min, max values in scatter plot
            update_dict = self.set_channel_bounds(x, y, z, color, size)

        elif trigger in [
            "downsampling",
            "channel",
            "channels",
            "scale",
            "lower_bounds",
            "upper_bounds",
            "",
        ]:
            update_dict = {}

            if trigger in ["scale", "lower_bounds", "upper_bounds"]:
                full_scales[channel] = scale
                full_lower_bounds[channel] = lower_bounds
                full_upper_bounds[channel] = upper_bounds
                update_dict.update(
                    {
                        "full_scales": full_scales,
                        "full_lower_bounds": full_lower_bounds,
                        "full_upper_bounds": full_upper_bounds,
                    }
                )
            elif trigger in ["channels", "downsampling", ""]:
                # Update data options from data subset
                update_dict.update(
                    self.update_channels(
                        channel,
                        channels,
                        full_scales,
                        full_lower_bounds,
                        full_upper_bounds,
                    )
                )
                update_dict.update(
                    {
                        "dataframe": self.update_dataframe(
                            downsampling, channels  # update_dict[""]
                        )
                    }
                )
                self.run_clustering(n_clusters, update_dict["dataframe"], full_scales)
                update_dict.update(
                    self.update_channels(
                        channel,
                        channels,
                        full_scales,
                        full_lower_bounds,
                        full_upper_bounds,
                    )
                )
            elif trigger == "channel":
                # Update displayed scale and bounds from stored values
                update_dict.update(
                    self.update_properties(
                        channel, full_scales, full_lower_bounds, full_upper_bounds
                    )
                )

        # self.update_param_dict(update_dict)

        outputs = []
        for param in param_list:
            if param in update_dict.keys():
                outputs.append(update_dict[param])
            else:
                outputs.append(no_update)

        return tuple(outputs)

    def update_param_dict(self, update_dict):
        for key, value in self.params.to_dict().items():
            if key in update_dict:
                if key in ["x", "y", "z", "color", "size", "channel"]:
                    if key in self.data_channels:
                        self.params.key = self.data_channels[key]
                    else:
                        self.params.key = None
                elif key in ["full_scales", "full_lower_bounds", "full_upper_bounds"]:
                    if "channels" in update_dict:
                        channels = update_dict["channels"]
                    else:
                        channels = self.params.channels
                    outlist = []
                    for channel in channels:
                        outlist.append(update_dict[key][channel])
                    setattr(self.params, key, outlist)
                else:
                    setattr(self.params, key, update_dict[key])

    def update_plots(
        self,
        n_clusters,
        select_cluster,
        dataframe_dict,
        channel,
        downsampling,
        x,
        x_log,
        x_thresh,
        x_min,
        x_max,
        y,
        y_log,
        y_thresh,
        y_min,
        y_max,
        z,
        z_log,
        z_thresh,
        z_min,
        z_max,
        color,
        color_log,
        color_thresh,
        color_min,
        color_max,
        color_maps,
        color_picker,
        size,
        size_log,
        size_thresh,
        size_min,
        size_max,
        size_markers,
    ):
        if dataframe_dict:
            dataframe = pd.DataFrame(dataframe_dict["dataframe"])
            if color_maps == "kmeans":
                color_maps = self.update_colormap(
                    n_clusters, color_picker, select_cluster
                )
            # make plotting data variables....??? pass those with no downsampling? or update object data.
            crossplot = self.update_plot(
                downsampling,
                x,
                x_log,
                x_thresh,
                x_min,
                x_max,
                y,
                y_log,
                y_thresh,
                y_min,
                y_max,
                z,
                z_log,
                z_thresh,
                z_min,
                z_max,
                color,
                color_log,
                color_thresh,
                color_min,
                color_max,
                color_maps,
                size,
                size_log,
                size_thresh,
                size_min,
                size_max,
                size_markers,
            )
            stats_table = self.make_stats_table(dataframe).to_dict("records")
            matrix = self.make_heatmap(dataframe)
            histogram = self.make_hist_plot(dataframe, channel)
            boxplot = self.make_boxplot(n_clusters, dataframe, channel)
            inertia = self.make_inertia_plot(n_clusters)

            return crossplot, stats_table, matrix, histogram, boxplot, inertia

        else:
            return None, None, None, None, None, None

    def update_color_picker(self, select_cluster):
        return {"color_picker": dict(hex=self.color_pickers[select_cluster])}

    def update_colormap(self, n_clusters, new_color, select_cluster):
        """
        Change the colormap for clusters
        """
        self.color_pickers[select_cluster] = new_color["hex"]
        colormap = {}
        for ii in range(n_clusters):
            colorpicker = self.color_pickers[ii]
            if "#" in colorpicker:
                color = colorpicker.lstrip("#")
                colormap[ii] = [
                    np.min([ii / (n_clusters - 1), 1]),
                    "rgb("
                    + ",".join([f"{int(color[i:i + 2], 16)}" for i in (0, 2, 4)])
                    + ")",
                ]
            else:
                colormap[ii] = [
                    np.min([ii / (n_clusters - 1), 1]),
                    colorpicker,
                ]

        # self.custom_colormap = list(self.colormap.values())
        return list(colormap.values())

    def run_clustering(self, n_clusters, dataframe_dict, full_scales):
        """
        Normalize the the selected data and perform the kmeans clustering.
        """
        if not dataframe_dict:
            return

        dataframe = pd.DataFrame(dataframe_dict["dataframe"])
        # Prime the app with clusters
        # Normalize values and run
        values = []
        for field in dataframe.columns:
            vals = dataframe[field].values.copy()

            nns = ~np.isnan(vals)
            vals[nns] = (
                (vals[nns] - min(vals[nns]))
                / (max(vals[nns]) - min(vals[nns]) + 1e-32)
                * full_scales[field]
            )
            values += [vals]

        for val in [2, 4, 8, 16, 32, n_clusters]:
            kmeans = KMeans(n_clusters=val, random_state=0).fit(np.vstack(values).T)
            self.clusters[val] = kmeans

        cluster_ids = self.clusters[n_clusters].labels_.astype(float)
        # self.data_channels["kmeans"] = cluster_ids[self.mapping]
        self.kmeans = cluster_ids[self.mapping]

        """
        self.update_axes(refresh_plot=False)
        self.color_max.value = self.n_clusters.value
        self.update_colormap(None, refresh_plot=False)
        self.color.value = "kmeans"
        self.color_active.value = True
        """

    def make_inertia_plot(self, n_clusters):
        """
        Generate an inertia plot
        """
        if n_clusters in self.clusters.keys():
            ind = np.sort(list(self.clusters.keys()))
            inertias = [self.clusters[ii].inertia_ for ii in ind]
            clusters = ind
            line = go.Scatter(x=clusters, y=inertias, mode="lines")
            point = go.Scatter(
                x=[n_clusters],
                y=[self.clusters[n_clusters].inertia_],
            )

            inertia_plot = go.Figure([line, point])

            inertia_plot.update_layout(
                {
                    "xaxis": {"title": "Number of clusters"},
                    "showlegend": False,
                }
            )
            return inertia_plot
        else:
            return None

    def make_hist_plot(self, dataframe, channel):
        """
        Generate an histogram plot for the selected data channel.
        """
        if (dataframe is not None) & (channel is not None):
            histogram = go.Figure(
                data=[
                    go.Histogram(
                        x=dataframe[channel].values,
                        histnorm="percent",
                        name=channel,
                    )
                ]
            )
            return histogram
        else:
            return None

    def make_boxplot(self, n_clusters, dataframe, channel):
        """
        Generate a box plot for each cluster.
        """
        if (
            (dataframe is not None)
            and (self.kmeans is not None)
            and (channel is not None)
        ):
            field = channel

            boxes = []
            for ii in range(n_clusters):

                cluster_ind = self.kmeans[self.indices] == ii
                x = np.ones(np.sum(cluster_ind)) * ii
                y = self.data_channels[field].values[self.indices][cluster_ind]

                boxes.append(
                    go.Box(
                        x=x,
                        y=y,
                        fillcolor=self.color_pickers[ii],
                        marker_color=self.color_pickers[ii],
                        line_color=self.color_pickers[ii],
                        showlegend=False,
                    )
                )

            boxplot = go.FigureWidget()

            boxplot.data = []
            for box in boxes:
                boxplot.add_trace(box)

            boxplot.update_layout(
                {
                    "xaxis": {"title": "Cluster #"},
                    "yaxis": {"title": field},
                    "height": 600,
                    "width": 600,
                }
            )
            return boxplot
        else:
            return None

    def make_stats_table(self, dataframe):
        """
        Generate a table of statistics using pandas
        """
        if dataframe is not None:
            stats_df = dataframe.describe(percentiles=None, include=None, exclude=None)
            stats_df.insert(0, "", stats_df.index)
            return stats_df
        else:
            return None

    def make_heatmap(self, dataframe):
        """
        Generate a confusion matrix
        """
        if dataframe is not None:
            df = dataframe.copy()
            corrs = df.corr()

            matrix = go.Figure(
                data=[
                    go.Heatmap(
                        x=list(corrs.columns),
                        y=list(corrs.index),
                        z=corrs.values,
                        type="heatmap",
                        colorscale="Viridis",
                        zsmooth=False,
                    )
                ]
            )

            matrix.update_scenes(aspectratio=dict(x=1, y=1, z=0.7), aspectmode="manual")
            matrix.update_layout(
                width=500,
                height=500,
                autosize=False,
                margin=dict(t=0, b=0, l=0, r=0),
                template="plotly_white",
                updatemenus=[
                    {
                        "buttons": [
                            {
                                "args": ["type", "heatmap"],
                                "label": "Heatmap",
                                "method": "restyle",
                            },
                            {
                                "args": ["type", "surface"],
                                "label": "3D Surface",
                                "method": "restyle",
                            },
                        ],
                        "direction": "down",
                        "pad": {"r": 10, "t": 10},
                        "showactive": True,
                        "x": 0.01,
                        "xanchor": "left",
                        "y": 1.15,
                        "yanchor": "top",
                    },
                    {
                        "buttons": [
                            {
                                "args": ["colorscale", label],
                                "label": label,
                                "method": "restyle",
                            }
                            for label in [
                                "Viridis",
                                "Rainbow",
                                "Cividis",
                                "Blues",
                                "Greens",
                            ]
                        ],
                        "direction": "down",
                        "pad": {"r": 10, "t": 10},
                        "showactive": True,
                        "x": 0.32,
                        "xanchor": "left",
                        "y": 1.15,
                        "yanchor": "top",
                    },
                ],
                yaxis={"autorange": "reversed"},
            )
            return matrix
        else:
            return None

    def update_dataframe(self, downsampling, channels):
        """
        Normalize the the selected data and perform the kmeans clustering.
        """
        self.kmeans = None
        self.indices, values = self.get_indices(channels, downsampling)
        n_values = values.shape[0]

        dataframe = pd.DataFrame(
            values[self.indices, :],
            columns=list(filter(None, channels)),
        )

        tree = cKDTree(dataframe.values)
        inactive_set = np.ones(n_values, dtype="bool")
        inactive_set[self.indices] = False
        out_values = values[inactive_set, :]
        for ii in range(values.shape[1]):
            out_values[np.isnan(out_values[:, ii]), ii] = np.mean(
                values[self.indices, ii]
            )

        _, ind_out = tree.query(out_values)
        del tree

        self.mapping = np.empty(n_values, dtype="int")
        self.mapping[inactive_set] = ind_out
        self.mapping[self.indices] = np.arange(len(self.indices))

        # self._inactive_set = np.where(np.all(np.isnan(values), axis=1))[0]
        # options = [[self.data.uid_name_map[key], key] for key in fields]
        # self.channels_plot_options.options = options
        return {"dataframe": dataframe.to_dict("records")}

    def get_indices(self, channels, downsampling):
        values = []
        non_nan = []
        for channel in channels:
            if channel is not None:
                values.append(
                    np.asarray(self.data_channels[channel].values, dtype=float)
                )
                non_nan.append(~np.isnan(self.data_channels[channel].values))

        values = np.vstack(values)
        non_nan = np.vstack(non_nan)

        percent = downsampling / 100

        # Number of values that are not nan along all three axes
        size = np.sum(np.all(non_nan, axis=0))

        indices = random_sampling(
            values.T,
            int(percent * size),
            bandwidth=2.0,
            rtol=1e0,
            method="histogram",
        )
        return indices, values.T

    def get_output_workspace(
        self, live_link, workpath: str = "./", name: str = "Temp.geoh5"
    ):
        """
        Create an active workspace with check for GA monitoring directory
        """
        if not name.endswith(".geoh5"):
            name += ".geoh5"

        workspace = Workspace(path.join(workpath, name))
        workspace.close()
        new_live_link = False
        time.sleep(1)
        # Check if GA digested the file already
        if not path.exists(workspace.h5file):
            workpath = path.join(workpath, ".working")
            if not path.exists(workpath):
                makedirs(workpath)
            workspace = Workspace(path.join(workpath, name))
            workspace.close()
            new_live_link = True
            if not live_link:
                print(
                    "ANALYST Pro active live link found. Switching to monitoring directory..."
                )
        elif live_link:
            print(
                "ANALYST Pro 'monitoring directory' inactive. Reverting to standalone mode..."
            )

        workspace.open()
        # return new live link
        return workspace, new_live_link

    def export_clusters(
        self, n_clicks, dataframe, objects, n_clusters, group_name, live_link
    ):
        """
        Write cluster groups to the target geoh5 object.
        """
        if (
            self.kmeans is not None
            and callback_context.triggered[0]["prop_id"].split(".")[0] == "export"
        ):
            obj = self.params.objects  # ***

            # Create reference values and color_map
            group_map, color_map = {}, []
            cluster_values = self.kmeans + 1
            # cluster_values = self.data_channels["kmeans"] + 1
            inactive_set = np.ones(len(cluster_values), dtype="bool")
            inactive_set[self.indices] = False
            cluster_values[inactive_set] = 0

            for ii in range(n_clusters):
                colorpicker = self.color_pickers[ii]
                color = colorpicker.lstrip("#")
                group_map[ii + 1] = f"Cluster_{ii}"
                color_map += [[ii + 1] + hex_to_rgb(color) + [1]]

            color_map = np.core.records.fromarrays(
                np.vstack(color_map).T,
                names=["Value", "Red", "Green", "Blue", "Alpha"],
            )

            # Create reference values and color_map
            group_map, color_map = {}, []
            for ii in range(n_clusters):
                colorpicker = self.color_pickers[ii]
                color = colorpicker.lstrip("#")
                group_map[ii + 1] = f"Cluster_{ii}"
                color_map += [[ii + 1] + hex_to_rgb(color) + [1]]

            color_map = np.core.records.fromarrays(
                np.vstack(color_map).T,
                names=["Value", "Red", "Green", "Blue", "Alpha"],
            )

            if self.params.monitoring_directory:
                output_path = self.params.monitoring_directory
                # monitored_directory_copy(self.export_directory.selected_path, obj)
            else:
                output_path = os.path.dirname(self.params.geoh5.h5file)

            # Write output uijson
            filename = "clustering"
            params = ClusteringParams(validate=False, **self.params.to_dict())
            params.write_input_file(name=filename, path=output_path, validate=False)

            temp_geoh5 = f"Clustering_{time.time():.3f}.geoh5"
            ws, live_link = self.get_output_workspace(
                live_link, output_path, temp_geoh5
            )

            with ws as workspace:
                obj = obj.copy(parent=workspace)
                cluster_groups = obj.add_data(
                    {
                        group_name: {
                            "type": "referenced",
                            "values": cluster_values,
                            "value_map": group_map,
                        }
                    }
                )
                cluster_groups.entity_type.color_map = {
                    "name": "Cluster Groups",
                    "values": color_map,
                }

            # return "Saved to " + output_path + "/" + temp_geoh5
            return live_link

    def run(self):
        # The reloader has not yet run - open the browser
        if not environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new("http://127.0.0.1:8050/")

        # Otherwise, continue as normal
        self.app.run_server(host="127.0.0.1", port=8050, debug=False)


class KMeansData:
    def __init__(self, name=None, values=None):
        self.name = name
        self.values = values


if __name__ == "__main__":
    print("Loading geoh5 file . . .")
    file = sys.argv[1]
    ifile = InputFile.read_ui_json(file)
    app = Clustering(ui_json=ifile)
    print("Loaded. Building the clustering app . . .")
    app.run()
    print("Done")
