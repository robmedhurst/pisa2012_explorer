"""
Functions for single varible group plotting.

Functions for single varible group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs


def distplot_nokde_single_row_1float(group_info, user_data):
    """Return a row of distribution plots."""
    def check_compatability():
        # here is where to check if requirements are met
        if 'requirements' in group_info:
            group_info['requirements'][0] != 'float'
            return False
        return True

    if 'functions' in group_info:
        return gs.distplot_single_row_1float(
            group_info, user_data, "float_no_kde")
    else:
        return check_compatability()


def distplot_kde_single_row_1float(group_info, user_data):
    """Return a row of frequencies plots with kde."""
    return gs.distplot_single_row_1float(
        group_info, user_data, "float_yes_kde")


def countplot_single_row_1cat(group_info, user_data):
    """Return a row of count plots."""
    return gs.countplot_single_row_1cat(group_info, user_data)


def barplot_single_single_1binary(group_info, user_data):
    """Return binary group summary as counts bar chart."""
    return gs.barplot_single_single_1binary(group_info, user_data)
