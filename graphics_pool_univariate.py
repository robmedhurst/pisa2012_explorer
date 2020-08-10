"""
Functions for univariate group plotting.

Functions for univariate group plotting with verbose names to be
caught by keyword.
"""

import graphics_ as gs


def float_horizontalcomparison_distribution(group_info, user_data):
    """Return a subplot of distributions for float type varibles."""
    return gs.float_horizontal_frequency(
        group_info, user_data, "float_no_kde")


def float_horizontalcomparison_frequency_kde(group_info, user_data):
    """Return a subplot of frequencies with kde for float type groups."""
    return gs.float_horizontal_frequency(
        group_info, user_data, "float_yes_kde")


def categorical_horizontalcomparison_counts(group_info, user_data):
    """Return a subplot of counts for categorical type groups."""
    return gs.float_horizontal_frequency(
        group_info, user_data, "categorical")


def binary_counts_singleplot(group_info, user_data):
    """Return binary group summary as counts bar chart."""
    return gs.binary_counts_singleplot(group_info, user_data)
