"""
Placeholder functions for looking up bivariate plots.

Functions for bivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics_ as gs


def violinplot_bi_row_float_cat(group_info, user_data):
    """Return a subplot of distributions for float type varibles."""
    return gs.violinplot_bi_row_float_cat(
        group_info, user_data, "float_no_kde")
