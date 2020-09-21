"""
Placeholder functions for looking up bivariate plots.

Functions for bivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs


def violinplot_uni_row_1cat(response_info, user_data):
    """Return a row of violin plots."""
    return gs.violinplot_uni_row_1cat(response_info, user_data)


def boxplot_uni_row_1cat(response_info, user_data):
    """Return a row of box plots."""
    return gs.boxplot_uni_row_1cat(response_info, user_data)
