#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

import os
import uuid

import numpy as np
from geoh5py.objects import Grid2D
from geoh5py.shared import Entity
from geoh5py.ui_json import InputFile
from ipywidgets import Button, FloatSlider, HBox, IntSlider, Layout, Text, VBox, Widget
from matplotlib import collections

from geoapps import PlotSelection2D
from geoapps.edge_detection.constants import app_initializer
from geoapps.edge_detection.driver import EdgeDetectionDriver
from geoapps.edge_detection.params import EdgeDetectionParams


class EdgeDetectionApp(PlotSelection2D):
    """
    Widget for Grid2D objects for the automated detection of line features.
    The application relies on the Canny and Hough transforms from the
    Scikit-Image library.

    :param grid: Grid2D object
    :param data: Children data object for the provided grid

    Optional
    --------

    :param sigma [Canny]: standard deviation of the Gaussian filter
    :param threshold [Hough]: Value threshold
    :param line_length [Hough]: Minimum accepted pixel length of detected lines
    :param line_gap [Hough]: Maximum gap between pixels to still form a line.
    """

    _object_types = (Grid2D,)
    _param_class = EdgeDetectionParams

    def __init__(self, ui_json=None, **kwargs):
        app_initializer.update(kwargs)
        if ui_json is not None and os.path.exists(ui_json):
            self.params = self._param_class(InputFile(ui_json))
        else:
            self.params = self._param_class(**app_initializer)

        self.defaults = {}
        for key, value in self.params.to_dict().items():
            if isinstance(value, Entity):
                self.defaults[key] = value.uid
            else:
                self.defaults[key] = value

        self._compute = Button(
            description="Compute",
            button_style="warning",
        )
        self._export_as = Text(
            value="Edges",
            description="Save as:",
            disabled=False,
        )
        self._line_length = IntSlider(
            min=1,
            max=100,
            step=1,
            value=1,
            continuous_update=False,
            description="Line Length",
        )
        self._line_gap = IntSlider(
            min=1,
            max=100,
            step=1,
            value=1,
            continuous_update=False,
            description="Line Gap",
        )
        self._sigma = FloatSlider(
            min=0.0,
            max=10,
            step=0.1,
            value=1.0,
            continuous_update=False,
            description="Sigma",
        )
        self._threshold = IntSlider(
            min=1,
            max=100,
            step=1,
            value=1,
            continuous_update=False,
            description="Threshold",
        )
        self._window_size = IntSlider(
            min=16,
            max=512,
            value=64,
            continuous_update=False,
            description="Window size",
        )
        self.data.observe(self.update_name, names="value")
        self.compute.on_click(self.compute_trigger)
        self._unique_object = {}
        super().__init__(**self.defaults)

        # Make changes to trigger warning color
        self.trigger.description = "Export"
        self.trigger.on_click(self.trigger_click)
        self.trigger.button_style = "success"

        self.compute.click()

    @property
    def compute(self):
        """ToggleButton"""
        return self._compute

    @property
    def export_as(self):
        """Text"""
        return self._export_as

    @property
    def line_length(self):
        """IntSlider"""
        return self._line_length

    @property
    def line_gap(self):
        """IntSlider"""
        return self._line_gap

    @property
    def main(self):
        if self._main is None:
            self._main = VBox(
                [
                    self.project_panel,
                    HBox(
                        [
                            VBox(
                                [
                                    self.data_panel,
                                    self.window_selection,
                                ]
                            ),
                            VBox(
                                [
                                    self.sigma,
                                    self.threshold,
                                    self.line_length,
                                    self.line_gap,
                                    self.window_size,
                                    self.compute,
                                    self.export_as,
                                    self.output_panel,
                                ],
                                layout=Layout(width="50%"),
                            ),
                        ]
                    ),
                ]
            )
        return self._main

    @property
    def sigma(self):
        """FloatSlider"""
        return self._sigma

    @property
    def threshold(self):
        """IntSlider"""
        return self._threshold

    @property
    def window_size(self):
        """IntSlider"""
        return self._window_size

    def trigger_click(self, _):
        driver = EdgeDetectionDriver(self.params)
        self.refresh.value = False
        driver.run()
        self.refresh.value = True

    def update_name(self, _):
        if self.data.value is not None:
            self.export_as.value = self.data.uid_name_map[self.data.value]
        else:
            self.export_as.value = "Edges"

    def compute_trigger(self, _):
        param_dict = {}
        for key in self.__dict__:
            try:
                if isinstance(getattr(self, key), Widget) and hasattr(self.params, key):
                    value = getattr(self, key).value
                    if key[0] == "_":
                        key = key[1:]

                    if (
                        isinstance(value, uuid.UUID)
                        and self.workspace.get_entity(value)[0] is not None
                    ):
                        value = self.workspace.get_entity(value)[0]

                    param_dict[key] = value

            except AttributeError:
                continue

        param_dict["geoh5"] = self.params.geoh5

        new_params = EdgeDetectionParams(**param_dict)

        self.refresh.value = False

        _, _, xy = EdgeDetectionDriver.get_edges(
            new_params.objects,
            new_params.data,
            new_params.sigma,
            new_params.line_length,
            new_params.threshold,
            new_params.line_gap,
            new_params.window_size,
            new_params.window_center_x,
            new_params.window_center_y,
            new_params.window_width,
            new_params.window_height,
            new_params.window_azimuth,
            new_params.resolution,
        )

        self.collections = [
            collections.LineCollection(
                np.reshape(xy, (-1, 2, 2)), colors="k", linewidths=2
            )
        ]
        self.refresh.value = True
