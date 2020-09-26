"""
Placeholder functions for looking up bivariate plots.

Functions for bivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs


def countplot_bi_grid_1cat_2cat(response_info, user_data):
    """Return a grid of countplots."""
    if 'functions' in response_info:
        return gs.countplot_bi_grid_1cat_2cat(response_info, user_data)


def heatmap_bi_grid_1float_2float(response, user_data):
    """Return a correlation matrix with heatmap."""
    if 'functions' in response:
        return gs.heatmap_grid_float(response, user_data)
    else:
        return (
            response['dependent_selection'][0]['category'] == 'float' and
            response['independent_selection'][0]['category'] == 'float' and
            response['independent_selection'][1]['category'] == 'float')
