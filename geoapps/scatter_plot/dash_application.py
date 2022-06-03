#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).
import base64
import io
import os
import webbrowser
from os import environ

import dash
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask, send_from_directory
from geoh5py.objects.object_base import ObjectBase
from geoh5py.ui_json import InputFile
from geoh5py.workspace import Workspace

from geoapps.base.selection import ObjectDataSelection
from geoapps.scatter_plot.constants import app_initializer
from geoapps.scatter_plot.driver import ScatterPlotDriver
from geoapps.scatter_plot.params import ScatterPlotParams


class ScatterPlots(ObjectDataSelection):
    _param_class = ScatterPlotParams
    _select_multiple = True
    _add_groups = False
    _downsampling = None
    _color = None
    _x = None
    _y = None
    _z = None
    _size = None

    def __init__(self, ui_json=None, **kwargs):
        app_initializer.update(kwargs)
        if ui_json is not None and os.path.exists(ui_json):
            self.params = self._param_class(InputFile(ui_json))
        else:
            self.params = self._param_class(**app_initializer)

        self.defaults = {}
        for key, value in self.params.to_dict().items():
            self.defaults[key] = value

        self.data_channels = {}

        super().__init__(**self.defaults)

        # https://community.plotly.com/t/putting-a-dash-instance-inside-a-class/6097/5
        external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
        server = Flask(__name__)
        self.app = dash.Dash(
            server=server,
            url_base_pathname=environ.get("JUPYTERHUB_SERVICE_PREFIX", "/"),
            external_stylesheets=external_stylesheets,
        )

        self.app.layout = html.Div(
            [
                html.Div(
                    [
                        dcc.Markdown(
                            """
                            ### Scatter Plots\n
                            \n
                            This application lets users visualize up to 5D of data pulled from any Geoscience ANALYST objects. The application uses the rich [Plotly](https://plotly.com/) graphical interface.\n
                            \n
                            New user? Visit the [**Getting Started**](https://geoapps.readthedocs.io/en/latest/content/installation.html) page.\n
                            \n
                            [**Online Documentation**](https://geoapps.readthedocs.io/en/latest/content/applications/scatter.html)\n
                            """
                        ),
                    ],
                    style={
                        "width": "100%",
                        "margin-bottom": "20px",
                    },
                ),
                html.Div(
                    [
                        dcc.Upload(
                            id="upload",
                            children=html.Button("Change Workspace"),
                            style={"margin-bottom": "20px"},
                        ),
                        dcc.Dropdown(
                            id="objects",
                            options=[],
                            value="",
                            style={"margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """Population Downsampling (%): """,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Slider(
                                    id="downsampling",
                                    value=100,
                                    min=1,
                                    max=100,
                                    step=1,
                                    marks=None,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={"margin-bottom": "20px"},
                        ),
                        dcc.Dropdown(
                            id="axes_pannels",
                            options=[
                                {"label": "X-axis", "value": "x"},
                                {"label": "Y-axis", "value": "y"},
                                {"label": "Z-axis", "value": "z"},
                                {"label": "Color", "value": "color"},
                                {"label": "Size", "value": "size"},
                            ],
                            value="x",
                            style={"margin-bottom": "20px"},
                        ),
                    ],
                    style={"width": "40%", "display": "block", "vertical-align": "top"},
                ),
                html.Div(
                    id="x_div",
                    children=[
                        dcc.Markdown("""Data: """),
                        dcc.Dropdown(
                            id="x",
                            options=[],
                            value="",
                            style={"width": "63.3%", "margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Threshold: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="x_thresh",
                                    type="number",
                                    value=0.1,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Checklist(
                                    id="x_log",
                                    options=["Log10"],
                                    value=["Log10"],
                                    style={"display": "inline-block"},
                                ),
                            ],
                            style={"margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Min: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="x_min",
                                    type="number",
                                    value=-17,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Markdown(
                                    "Max: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="x_max",
                                    type="number",
                                    value=25.5,
                                    style={"display": "inline-block"},
                                ),
                            ],
                        ),
                    ],
                    style={
                        "display": "block",
                        "width": "40%",
                        "vertical-align": "top",
                        "margin-bottom": "20px",
                    },
                ),
                html.Div(
                    id="y_div",
                    children=[
                        dcc.Markdown("""Data: """),
                        dcc.Dropdown(
                            id="y",
                            options=[],
                            value="",
                            style={"width": "63.3%", "margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Threshold: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="y_thresh",
                                    type="number",
                                    value=0.1,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Checklist(
                                    id="y_log",
                                    options=["Log10"],
                                    value=["Log10"],
                                    style={"display": "inline-block"},
                                ),
                            ],
                            style={"margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Min: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="y_min",
                                    type="number",
                                    value=-17,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Markdown(
                                    "Max: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="y_max",
                                    type="number",
                                    value=25.5,
                                    style={"display": "inline-block"},
                                ),
                            ],
                        ),
                    ],
                    style={
                        "display": "block",
                        "width": "40%",
                        "vertical-align": "top",
                        "margin-bottom": "20px",
                    },
                ),
                html.Div(
                    id="z_div",
                    children=[
                        dcc.Markdown("""Data: """),
                        dcc.Dropdown(
                            id="z",
                            options=[],
                            value="",
                            style={"width": "63.3%", "margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Threshold: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="z_thresh",
                                    type="number",
                                    value=0.1,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Checklist(
                                    id="z_log",
                                    options=["Log10"],
                                    value=["Log10"],
                                    style={"display": "inline-block"},
                                ),
                            ],
                            style={"margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Min: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="z_min",
                                    type="number",
                                    value=-17,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Markdown(
                                    "Max: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="z_max",
                                    type="number",
                                    value=25.5,
                                    style={"display": "inline-block"},
                                ),
                            ],
                        ),
                    ],
                    style={
                        "display": "block",
                        "width": "40%",
                        "vertical-align": "top",
                        "margin-bottom": "20px",
                    },
                ),
                html.Div(
                    id="color_div",
                    children=[
                        dcc.Markdown("""Data: """),
                        dcc.Dropdown(
                            id="color",
                            options=[],
                            value="",
                            style={"width": "63.3%", "margin-bottom": "20px"},
                        ),
                        dcc.Dropdown(
                            id="color_maps",
                            options=px.colors.named_colorscales(),
                            value="viridis",
                            style={"width": "63.3%", "margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Threshold: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="color_thresh",
                                    type="number",
                                    value=0.1,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Checklist(
                                    id="color_log",
                                    options=["Log10"],
                                    value=["Log10"],
                                    style={"display": "inline-block"},
                                ),
                            ],
                            style={"margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Min: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="color_min",
                                    type="number",
                                    value=-17,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Markdown(
                                    "Max: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="color_max",
                                    type="number",
                                    value=25.5,
                                    style={"display": "inline-block"},
                                ),
                            ],
                        ),
                    ],
                    style={
                        "display": "block",
                        "width": "40%",
                        "vertical-align": "top",
                        "margin-bottom": "20px",
                    },
                ),
                html.Div(
                    id="size_div",
                    children=[
                        dcc.Markdown("""Data: """),
                        dcc.Dropdown(
                            id="size",
                            options=[],
                            value="",
                            style={"width": "63.3%", "margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    """Marker Size: """,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Slider(
                                    id="size_markers",
                                    value=20,
                                    min=1,
                                    max=100,
                                    step=1,
                                    marks=None,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ],
                            style={"width": "40%", "margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Threshold: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="size_thresh",
                                    type="number",
                                    value=0.1,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Checklist(
                                    id="size_log",
                                    options=["Log10"],
                                    value=["Log10"],
                                    style={"display": "inline-block"},
                                ),
                            ],
                            style={"margin-bottom": "20px"},
                        ),
                        html.Div(
                            [
                                dcc.Markdown(
                                    "Min: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="size_min",
                                    type="number",
                                    value=-17,
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "20px",
                                    },
                                ),
                                dcc.Markdown(
                                    "Max: ",
                                    style={
                                        "display": "inline-block",
                                        "margin-right": "5px",
                                    },
                                ),
                                dcc.Input(
                                    id="size_max",
                                    type="number",
                                    value=25.5,
                                    style={"display": "inline-block"},
                                ),
                            ],
                        ),
                    ],
                    style={
                        "display": "block",
                        "width": "40%",
                        "vertical-align": "top",
                        "margin-bottom": "20px",
                    },
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="plot",
                        ),
                        html.A(
                            html.Button("Download as HTML"),
                            id="download",
                            download="Crossplot.html",
                        ),
                    ],
                    style={"width": "80%", "display": "block", "margin-bottom": "20px"},
                ),
                dcc.Markdown(
                    """
                    Need help? Contact us at support@mirageoscience.com\n
                    """
                ),
            ],
            style={"width": "100%", "margin-left": "50px"},
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
            Output(component_id="x_min", component_property="value"),
            Output(component_id="x_max", component_property="value"),
            Output(component_id="y_min", component_property="value"),
            Output(component_id="y_max", component_property="value"),
            Output(component_id="z_min", component_property="value"),
            Output(component_id="z_max", component_property="value"),
            Output(component_id="color_min", component_property="value"),
            Output(component_id="color_max", component_property="value"),
            Output(component_id="size_min", component_property="value"),
            Output(component_id="size_max", component_property="value"),
            Input(component_id="x", component_property="value"),
            Input(component_id="y", component_property="value"),
            Input(component_id="z", component_property="value"),
            Input(component_id="color", component_property="value"),
            Input(component_id="size", component_property="value"),
        )(self.set_channel_bounds)
        self.app.callback(
            Output(component_id="plot", component_property="figure"),
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
            Input(component_id="size", component_property="value"),
            Input(component_id="size_log", component_property="value"),
            Input(component_id="size_thresh", component_property="value"),
            Input(component_id="size_min", component_property="value"),
            Input(component_id="size_max", component_property="value"),
            Input(component_id="size_markers", component_property="value"),
        )(self.plot_selection)
        self.app.callback(
            Output(component_id="objects", component_property="options"),
            Output(component_id="objects", component_property="value"),
            Input(component_id="upload", component_property="contents"),
        )(self.update_object_options)
        self.app.callback(
            Output(component_id="x", component_property="options"),
            Output(component_id="y", component_property="options"),
            Output(component_id="z", component_property="options"),
            Output(component_id="color", component_property="options"),
            Output(component_id="size", component_property="options"),
            Output(component_id="x", component_property="value"),
            Output(component_id="y", component_property="value"),
            Output(component_id="z", component_property="value"),
            Output(component_id="color", component_property="value"),
            Output(component_id="size", component_property="value"),
            Input(component_id="objects", component_property="value"),
        )(self.update_data_options)
        self.app.callback(
            Output(component_id="download", component_property="href"),
            Input(component_id="plot", component_property="figure"),
        )(self.save_figure)

    # https://stackoverflow.com/questions/50213761/changing-visibility-of-a-dash-component-by-updating-other-component
    def update_visibility(self, axis):
        if axis == "x":
            return (
                {"display": "block"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )
        elif axis == "y":
            return (
                {"display": "none"},
                {"display": "block"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )
        elif axis == "z":
            return (
                {"display": "none"},
                {"display": "none"},
                {"display": "block"},
                {"display": "none"},
                {"display": "none"},
            )
        elif axis == "color":
            return (
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "block"},
                {"display": "none"},
            )
        elif axis == "size":
            return (
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "block"},
            )

    def get_channel(self, channel):
        obj, _ = self.get_selected_entities()

        if channel is None:
            return None

        if channel not in self.data_channels.keys():
            if channel == "None":
                data = None
            elif self.workspace.get_entity(channel):
                data = self.workspace.get_entity(channel)[0]
            else:
                return

            self.data_channels[channel] = data

    def get_channel_bounds(self, channel):
        """
        Set the min and max values for the given axis channel
        """
        self.refresh.value = False

        # channel = getattr(self, "_" + name).value
        self.get_channel(channel)

        cmin, cmax = 0, 0
        if (channel in self.data_channels.keys()) & (channel != "None"):
            values = self.data_channels[channel].values
            values = values[~np.isnan(values)]
            cmin = f"{np.min(values):.2e}"
            cmax = f"{np.max(values):.2e}"

        self.refresh.value = True
        return cmin, cmax

    def set_channel_bounds(self, x, y, z, color, size):
        self.refresh.value = False
        x_min, x_max = self.get_channel_bounds(x)
        y_min, y_max = self.get_channel_bounds(y)
        z_min, z_max = self.get_channel_bounds(z)
        color_min, color_max = self.get_channel_bounds(color)
        size_min, size_max = self.get_channel_bounds(size)
        self.refresh.value = True
        return (
            x_min,
            x_max,
            y_min,
            y_max,
            z_min,
            z_max,
            color_min,
            color_max,
            size_min,
            size_max,
        )

    def plot_selection(
        self,
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
    ):
        if not self.refresh.value:
            return None

        new_params_dict = {}
        for key, value in self.params.to_dict().items():
            # param = getattr(scatter, key, None)

            if key in locals():
                param = locals()[key]
            else:
                param = None

            if param is None:
                new_params_dict[key] = value
            elif (
                (key == "x")
                | (key == "y")
                | (key == "z")
                | (key == "color")
                | (key == "size")
            ):
                if (param != "None") & (param in self.data_channels.keys()):
                    new_params_dict[key] = self.data_channels[param]
                else:
                    new_params_dict[key] = None
            else:
                new_params_dict[key] = param

        ifile = InputFile(
            ui_json=self.params.input_file.ui_json,
            validation_options={"disabled": True},
        )

        ifile.data = new_params_dict
        new_params = ScatterPlotParams(input_file=ifile)

        driver = ScatterPlotDriver(new_params)
        figure = go.FigureWidget(driver.run())

        return figure

    def update_object_options(self, contents):
        # print(self.params.geoh5)
        # self.workspace = Workspace(self.params.geoh5)

        if contents is not None:
            # print(contents)
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            print(Workspace(decoded).objects)
            self.workspace = Workspace(decoded)
        obj_list = self.workspace.objects

        # options = [["", None]] + [
        #    [obj.parent.name + "/" + obj.name, obj.uid] for obj in obj_list
        # ]

        # options = ["None"]
        options = [
            {"label": obj.parent.name + "/" + obj.name, "value": obj.name}
            for obj in obj_list
        ]
        if len(options) > 0:
            value = options[0]["value"]
        else:
            value = None

        return options, value

    def update_data_options(self, object):
        self.refresh.value = False
        # obj, _ = self.get_selected_entities()
        obj = None
        if getattr(self, "workspace", None) is not None and self.workspace.get_entity(
            object
        ):
            for entity in self.workspace.get_entity(object):
                if isinstance(entity, ObjectBase):
                    obj = entity

        channel_list = ["None"]
        channel_list.extend(obj.get_data_list())

        if "Visual Parameters" in channel_list:
            channel_list.remove("Visual Parameters")

        for channel in channel_list:
            self.get_channel(channel)

        options = list(self.data_channels.keys())
        self.refresh.value = True

        return (
            options,
            options,
            options,
            options,
            options,
            "None",
            "None",
            "None",
            "None",
            "None",
        )

    # https://plotly.com/python/interactive-html-export/
    def save_figure(self, fig):
        buffer = io.StringIO()
        go.Figure(fig).write_html(buffer)
        html_bytes = buffer.getvalue().encode()
        encoded = base64.b64encode(html_bytes).decode()
        href = "data:text/html;base64," + encoded

        return href

    def run(self):
        # The reloader has not yet run - open the browser
        if not environ.get("WERKZEUG_RUN_MAIN"):
            webbrowser.open_new("http://127.0.0.1:8050/")

        # Otherwise, continue as normal
        self.app.run_server(host="127.0.0.1", port=8050, debug=True)
