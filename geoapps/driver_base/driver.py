#  Copyright (c) 2023 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

from __future__ import annotations

import os
from abc import ABC, abstractmethod

from geoh5py import Workspace
from geoh5py.ui_json import InputFile
from param_sweeps.generate import generate

from geoapps.driver_base.params import BaseParams


class BaseDriver(ABC):
    _workspace: Workspace | None = None
    _params: BaseParams
    _params_class = BaseParams
    _validations = None

    def __init__(self, params: BaseParams):
        self.params = params

    @property
    def params(self):
        """Application parameters."""
        return self._params

    @params.setter
    def params(self, val):
        if not isinstance(val, self.params_class):
            raise TypeError(f"Parameters must be of type {self.params_class.__name__}.")
        self._params = val

    @property
    def workspace(self):
        """Application workspace."""
        if self._workspace is None and self._params is not None:
            self._workspace = self._params.geoh5

        return self._workspace

    @property
    def params_class(self):
        """Default parameter class."""
        return self._params_class

    @abstractmethod
    def run(self):
        """Run the application."""
        raise NotImplementedError

    @classmethod
    def start(cls, filepath: str, driver_class=None):
        """
        Run application specified by 'filepath' ui.json file.

        :param filepath: Path to valid ui.json file for the application driver.
        """

        if driver_class is None:
            driver_class = cls

        print("Loading input file . . .")
        filepath = os.path.abspath(filepath)
        ifile = InputFile.read_ui_json(
            filepath, validations=driver_class._validations  # pylint: disable=W0212
        )

        generate_sweep = ifile.data.get("generate_sweep", None)
        if generate_sweep:
            ifile.data["generate_sweep"] = False
            name = os.path.basename(filepath)
            path = os.path.dirname(filepath)
            ifile.write_ui_json(name=name, path=path)
            generate(  # pylint: disable=E1123
                filepath, update_values={"conda_environment": "geoapps"}
            )
        else:
            params = driver_class._params_class(ifile)  # pylint: disable=W0212
            print("Initializing application . . .")
            driver = driver_class(params)

            print("Running application . . .")
            driver.run()
            print(f"Results saved to {params.geoh5.h5file}")

            return driver
