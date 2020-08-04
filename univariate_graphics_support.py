"""Graphic functions for exploratory analysis."""

import io
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

from main import get_longnames


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

    buf = io.BytesIO()
    output = buf
    pickle.dump(fig, output)
    plt.close(fig)
    return buf


def float_horizontal_frequency(parameters, pisa_df, inputs, switcher):
    """Return a subplot of scatterplots of these float type varibles."""
    var_list, max_ylim = parameters[1], 0

    if switcher == "float_yes_kde":
        switcher = True
        first_y_name = "Frequency"
    elif switcher == "float_no_kde":
        switcher = False
        first_y_name = "Count"

    elif switcher == "categorical":
        first_y_name = "Count"
        switcher = inputs[1][parameters[2]]

    for first_pass in [True, False]:
        # initialize figure
        # width 5*n_vars, height 5, force close to 1:1 aspect ratio
        if first_pass:
            fig = plt.figure(figsize=(5 * len(var_list), 5))
        else:
            # discard first draft
            plt.close(fig)
            del fig
            fig = plt.figure(figsize=(5 * len(var_list), 5))

        # for each var create axis and titles
        for var_index, var_name in enumerate(var_list):
            # add a subplot for each var_name in var_list
            axis = fig.add_subplot(1, len(var_list), var_index + 1)

            if isinstance(switcher, list):
                sns.countplot(
                    pisa_df[var_name],
                    order=switcher,
                    color=sns.color_palette()[0]
                    )

            else:
                # seaborn distribution plot
                sns.distplot(
                    pisa_df[var_name],
                    kde=switcher, hist_kws={
                        "rwidth": 0.75, 'edgecolor': 'black', 'alpha': 1.0}
                    )

            # Customize axis properties:
            # Get max y limit on first pass
            if first_pass:
                axis = plt.gca()
                new_ylim = axis.get_ylim()[1]
                if new_ylim > max_ylim:
                    max_ylim = new_ylim
                axis.get_ylim()

            # Apply max y lim to all subplots on second pass
            else:
                # only display y label on first subplot
                if var_index == 0:
                    yname = first_y_name
                else:
                    yname = None

                # subbplot x label longnames if available
                xname = str(var_list[var_index])
                if get_longnames([var_list[var_index]]):
                    xname = xname + ': ' + str(
                        get_longnames([var_list[var_index]])[0])

                # set axis limits and titles
                axis.set(
                    ylim=(0, max_ylim),
                    xlabel=xname,
                    ylabel=yname
                    )

    buf = io.BytesIO()
    output = buf
    pickle.dump(fig, output)
    plt.close(fig)
    return buf
