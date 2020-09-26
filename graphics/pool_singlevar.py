"""
Functions for single varible group plotting.

Functions for single varible group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs


def distplot_nokde_single_row_1float(group_info, user_data):
    """Return a row of distribution plots."""
    if 'functions' in group_info:
        return gs.distplot_single_row_1float(
            group_info, user_data, "float_no_kde")
    else:
        return (len(group_info['dependent_selection']) == 0 and
                len(group_info['independent_selection']) == 1 and
                group_info['independent_selection'][0]['category'] == 'float')


def distplot_kde_single_row_1float(group_info, user_data):
    """Return a row of frequencies plots with kde."""
    if 'functions' in group_info:
        return gs.distplot_single_row_1float(
            group_info, user_data, "float_yes_kde")
    else:
        return (len(group_info['dependent_selection']) == 0 and
                len(group_info['independent_selection']) == 1 and
                group_info['independent_selection'][0]['category'] == 'float')


def countplot_single_row_1cat(group_info, user_data):
    """Return a row of count plots."""
    if 'functions' in group_info:
        return gs.countplot_single_row_1cat(group_info, user_data)
    else:
        return (len(group_info['dependent_selection']) == 0 and
                len(group_info['independent_selection']) == 1 and
                (group_info['independent_selection'][0]['category']
                 in gs.definitions.KNOWN_CATEGORIES))


def barplot_single_single_1binary(group_info, user_data):
    """Return binary group summary as counts bar chart."""
    if 'functions' in group_info:
        return gs.barplot_single_single_1binary(group_info, user_data)
    else:
        category = group_info['independent_selection'][0]['category']
        return (len(group_info['dependent_selection']) == 0 and
                len(group_info['independent_selection']) == 1 and
                (category in gs.definitions.KNOWN_CATEGORIES) and
                len(gs.definitions.KNOWN_CATEGORIES[category]) == 2)
