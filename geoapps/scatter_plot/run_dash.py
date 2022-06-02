#  Copyright (c) 2022 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).


from geoapps.scatter_plot.dash_application import ScatterPlots

app = ScatterPlots()
app.app.run_server(host="127.0.0.1", port=8050, debug=False)
