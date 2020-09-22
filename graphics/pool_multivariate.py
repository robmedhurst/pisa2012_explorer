"""
Placeholder functions for looking up multivariate plots.

Functions for multivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs


def heatmap_multi_grid_1float_2float_3float(response_info, user_data):
    """Return a correlation matrix with heatmap."""
    return gs.heatmap_grid_float(response_info, user_data)
