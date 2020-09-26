"""
Placeholder functions for looking up bivariate plots.

Functions for bivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs


def violinplot_uni_row_1cat(response_info, user_data):
    """Return a row of violin plots."""
    if 'functions' in response_info:
        return gs.violinplot_uni_row_1cat(response_info, user_data)


def boxplot_uni_row_1cat(response_info, user_data):
    """Return a row of box plots."""
    if 'functions' in response_info:
        return gs.boxplot_uni_row_1cat(response_info, user_data)


def heatmap_uni_grid_1float(response_info, user_data):
    """Return a correlation matrix with heatmap."""
    if 'functions' in response_info:
        return gs.heatmap_grid_float(response_info, user_data)
