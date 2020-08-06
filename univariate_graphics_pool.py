"""
Functions for univariate group plotting.

Functions for univariate group plotting with verbose names to be
caught by keyword.
"""

import univariate_graphics_support as u


def float_horizontalcomparison_distribution(parameters, pisa_df, inputs):
    """Return a subplot of distributions for float type varibles."""
    return u.float_horizontal_frequency(
        parameters, pisa_df, inputs, "float_no_kde")


def float_horizontalcomparison_frequency_kde(parameters, pisa_df, inputs):
    """Return a subplot of frequencies with kde for float type groups."""
    return u.float_horizontal_frequency(
        parameters, pisa_df, inputs, "float_yes_kde")


def categorical_horizontalcomparison_counts(parameters, pisa_df, inputs):
    """Return a subplot of counts for categorical type groups."""
    return u.float_horizontal_frequency(
        parameters, pisa_df, inputs, "categorical")


def float_means_singleplot(parameters, pisa_df, inputs):
    """Return mean distribution."""
    return u.float_horizontal_frequency(
        parameters, pisa_df, inputs, "float_no_kde")


def binary_counts_singleplot(parameters, pisa_df, inputs):
    """Return binary group summary as counts bar chart."""
    return u.binary_counts_singleplot(parameters, pisa_df, inputs)
