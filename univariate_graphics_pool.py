"""Functions with verbose names to be caught by keyword."""

import matplotlib.pyplot as plt
import seaborn as sns

import univariate_graphics_support as u
from main import get_longnames


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


def binary_counts_singleplot(parameters, pisa_df, inputs):
    """Return binary group summary as counts bar chart."""
    (independent_groups, dependent_groups) = inputs[2:]
    (group_name, var_list, category) = parameters

    base_color = sns.color_palette()[0]
    # fig = plt.figure()
    fig = plt.figure()
    sns.barplot(
        y=pisa_df[var_list].sum().values,
        # x = ['Mother', 'Father', 'Brothers', 'Sisters', 'Grandparents'],
        x=get_longnames(var_list),
        color=base_color
        )
    plt.xticks(rotation=30, ha='right')
    plt.ylabel('count')
    plt.close(fig)
    return fig


def float_means_singleplot(parameters, pisa_df, inputs):
    """Return mean distribution."""
    return u.float_horizontal_frequency(
        parameters, pisa_df, inputs, "float_no_kde")
