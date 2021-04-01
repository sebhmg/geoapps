#  Copyright (c) 2021 Mira Geoscience Ltd.
#
#  This file is part of geoapps.
#
#  geoapps is distributed under the terms and conditions of the MIT License
#  (see LICENSE file at the root of this source code package).

valid_parameters = [
    "out_group",
    "workspace",
    "save_to_geoh5",
    "inversion_type",
    "inversion_style",
    "forward_only",
    "inducing_field_aid",
    "core_cell_size",
    "octree_levels_topo",
    "octree_levels_obs",
    "depth_core",
    "max_distance",
    "padding_distance",
    "chi_factor",
    "max_iterations",
    "max_cg_iterations",
    "n_cpu",
    "max_ram",
    "initial_beta_ratio",
    "tol_cg",
    "ignore_values",
    "no_data_value",
    "resolution",
    "window",
    "alphas",
    "reference_model",
    "starting_model",
    "model_norms",
    "data",
    "uncertainty_mode",
    "receivers_offset",
    "topography",
]


valid_parameter_values = {
    "inversion_type": ["gravity", "magnetics", "mvi", "mvic"],
    "inversion_style": ["voxel"],
    "forward_only": [True, False],
}
