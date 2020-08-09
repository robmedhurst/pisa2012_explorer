"""
Functions for univariate group plotting.

Functions for univariate group plotting with verbose names to be
caught by keyword.
"""

import univariate_graphics_support as u


def float_horizontalcomparison_distribution(group_info, user_data):
    """Return a subplot of distributions for float type varibles."""
    return u.float_horizontal_frequency(
        group_info, user_data, "float_no_kde")


def float_horizontalcomparison_frequency_kde(group_info, user_data):
    """Return a subplot of frequencies with kde for float type groups."""
    return u.float_horizontal_frequency(
        group_info, user_data, "float_yes_kde")


def categorical_horizontalcomparison_counts(group_info, user_data):
    """Return a subplot of counts for categorical type groups."""
    return u.float_horizontal_frequency(
        group_info, user_data, "categorical")


def binary_counts_singleplot(group_info, user_data):
    """Return binary group summary as counts bar chart."""
    return u.binary_counts_singleplot(group_info, user_data)
