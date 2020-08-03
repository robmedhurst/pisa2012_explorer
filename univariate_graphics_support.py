"""Graphic functions for exploratory analysis."""

import matplotlib.pyplot as plt
import seaborn as sns
from main import get_longnames


# def float_horizontal_frequency(parameters, pisa_df, inputs):
#     return float_horizontal_frequency(parameters, pisa_df, inputs)


def float_horizontal_frequency(parameters, pisa_df, inputs, kde):
    """Return a subplot of scatterplots of these float type varibles."""
    (independent_groups, dependent_groups) = inputs[2:]
    (group_name, var_list) = parameters

    max_ylim = 0
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
        for n, var_name in enumerate(var_list):
            # add a subplot for each var_name in var_list
            ax = fig.add_subplot(1, len(var_list), n + 1)

            # seaborn distribution plot
            ax = sns.distplot(
                pisa_df[var_name],
                kde=kde,
                hist_kws={"rwidth": 0.75, 'edgecolor': 'black', 'alpha': 1.0}
                )

            # Customize axis properties:
            # Get max y limit on first pass
            if first_pass:
                axis = plt.gca()
                new_ylim = axis.get_ylim()[1]
                if new_ylim > max_ylim:
                    max_ylim = new_ylim
                print(axis.get_ylim())

            # Apply max y lim to all subplots on second pass
            if not first_pass:
                # only display y label on first subplot
                if n == 0 and kde == 1:
                    yname = "Frequency"
                elif n == 0 and kde == 0:
                    yname = "Count"
                else:
                    yname = None

                # subbplot x label longnames if available
                xname = str(var_list[n])
                if get_longnames([var_list[n]]):
                    xname = xname + ': ' + str(get_longnames([var_list[n]])[0])

                # set axis limits and titles
                ax.set(
                    ylim=(0, max_ylim),
                    xlabel=xname,
                    ylabel=yname
                    )

    plt.close(fig)

    return fig
