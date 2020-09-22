"""
Placeholder functions for looking up bivariate plots.

Functions for bivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs


def countplot_bi_grid_1cat_2cat(response_info, user_data):
    """Return a grid of countplots."""
    return gs.countplot_bi_grid_1cat_2cat(response_info, user_data)


def heatmap_bi_grid_1float_2float(response_info, user_data):
    """Return a correlation matrix with heatmap."""
    return gs.heatmap_grid_float(response_info, user_data)
