"""
Placeholder functions for looking up bivariate plots.

Functions for bivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics_ as gs


def float_hcomp_distribution(group_info, user_data):
    """Return a subplot of distributions for float type varibles."""
    return gs.horizontalcomparion_violin_catfloat(
        group_info, user_data, "float_no_kde")
