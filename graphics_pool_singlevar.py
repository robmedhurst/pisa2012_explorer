"""
Functions for single varible group plotting.

Functions for single varible group plotting with verbose names to be
caught by keyword.
"""

import graphics_ as gs


def distplot_single_row_float_nokde(group_info, user_data):
    """Return a subplot of distributions for float type varibles."""
    return gs.distplot_single_row_float(group_info, user_data, "float_no_kde")


def distplot_single_row_float_kde(group_info, user_data):
    """Return a subplot of frequencies with kde for float type groups."""
    return gs.distplot_single_row_float(group_info, user_data, "float_yes_kde")


def countplot_single_row_cat(group_info, user_data):
    """Return a subplot of counts for categorical type groups."""
    return gs.countplot_single_row_cat(group_info, user_data)


def barplot_single_single_binary(group_info, user_data):
    """Return binary group summary as counts bar chart."""
    return gs.barplot_single_single_binary(group_info, user_data)