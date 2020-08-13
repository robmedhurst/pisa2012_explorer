"""Graphic functions supporting exploratory pisa2012 analysis."""

import io
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

import main_definitions as definitions
from main_ import get_longnames


def pickle_buffer(fig):
    """Given an object, return pickled version as io.BytesIO object."""
    buf = io.BytesIO()
    output = buf
    pickle.dump(fig, output)
    plt.close(fig)
    return buf


def violinplot_bi_row_float_cat(parameters, pisa_df, inputs):
    """Placeholer function."""
    (group_name, var_list, category, category_order, dep_var) = parameters
    max_ylim = 0

    for first_pass in [True, False]:
        # initialize figure
        # width 5*n_vars, height 5, force close to 1:1 aspect ratio
        if first_pass:
            fig = plt.figure(figsize=(5 * len(var_list), 5))
        else:
            # discard first draft
            plt.close(fig)
            fig = plt.figure(figsize=(5 * len(var_list), 5))

        for var_index, var_name in enumerate(var_list):
            # add a subplot for each var_name in var_list
            axis = fig.add_subplot(1, len(var_list), var_index + 1)

            sns.violinplot(data=pisa_df, x=var_name, y=dep_var,
                           color=sns.color_palette()[0], order=category_order)

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
                    yname = get_longnames([dep_var])[0]
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

    return pickle_buffer(fig)


def barplot_uni_single_binary(group_info, user_data):
    """Return binary group summary as counts bar chart."""
    pisa_df = user_data['custom_dataframe']
    var_list = group_info['variables']

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

    return pickle_buffer(fig)


def countplot_uni_row_cat(group_info, user_data):
    """."""
    pisa_df = user_data['custom_dataframe']
    var_list = group_info['variables']
    category = group_info['category']
    max_ylim = 0

    for first_pass in [True, False]:
        # initialize figure
        # width 5*n_vars, height 5, force close to 1:1 aspect ratio
        if first_pass:
            fig = plt.figure(figsize=(5 * len(var_list), 5))
        else:
            # discard first draft
            plt.close(fig)
            fig = plt.figure(figsize=(5 * len(var_list), 5))

        # for each var create axis and titles
        for var_index, var_name in enumerate(var_list):
            # add a subplot for each var_name in var_list
            axis = fig.add_subplot(1, len(var_list), var_index + 1)

            sns.countplot(
                pisa_df[var_name],
                order=definitions.PREFERRED_NAMING[category],
                color=sns.color_palette()[0]
                )

            # Get plot information (max y limit) on first pass
            if first_pass:
                axis = plt.gca()
                new_ylim = axis.get_ylim()[1]
                if new_ylim > max_ylim:
                    max_ylim = new_ylim

            # Apply formatting on second pass
            else:
                # only display y label on first subplot
                if var_index == 0:
                    yname = "Count"
                else:
                    yname = None

                # use long names on x axis if available
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

    return pickle_buffer(fig)


def distplot_uni_row_float(group_info, user_data, kde):
    """Return a subplot of scatterplots of these float type varibles."""
    pisa_df = user_data['custom_dataframe']
    var_list = group_info['variables']
    max_ylim = 0

    if kde == "float_yes_kde":
        kde = True
        first_y_name = "Frequency"
    elif kde == "float_no_kde":
        kde = False
        first_y_name = "Count"

    for first_pass in [True, False]:
        # initialize figure
        # width 5*n_vars, height 5, force close to 1:1 aspect ratio
        if first_pass:
            fig = plt.figure(figsize=(5 * len(var_list), 5))
        else:
            # discard first draft
            plt.close(fig)
            fig = plt.figure(figsize=(5 * len(var_list), 5))

        # for each var create axis and titles
        for var_index, var_name in enumerate(var_list):
            # add a subplot for each var_name in var_list
            axis = fig.add_subplot(1, len(var_list), var_index + 1)

            # seaborn distribution plot
            sns.distplot(
                pisa_df[var_name], kde=kde, hist_kws={
                    "rwidth": 0.75, 'edgecolor': 'black', 'alpha': 1.0})

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
                    xlabel=xname, ylabel=yname)

    return pickle_buffer(fig)
