"""Graphic functions supporting exploratory pisa2012 analysis."""

import io
import pickle

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import main.definitions as definitions


# =============================================================================
# %% HELPER

LONGNAMES = pd.read_csv(
        'pisadict2012.csv',
        sep=',', encoding='latin-1', error_bad_lines=False,
        dtype='unicode', index_col=False).rename(
            columns={'Unnamed: 0': 'varname', 'x': 'description'})


def get_longnames(names):
    """
    Return PISA 2012 long names given short names.

    Return list of PISA variable descriptions corresponding to variable
    shortnames given by list name.
    Resource is read from local copy of pisadict2012.csv
    """
    names = list(names)
    return list(LONGNAMES.query("varname in @names")['description'])


def get_longest_title(var_name):
    """Return given string with longname if available."""
    longest_title = var_name
    if get_longnames([var_name]):
        longest_title = (
            var_name + ': ' + str(get_longnames([var_name])[0]))
    return longest_title


def concise_reponse_info(response):
    """Expand and return response information."""
    return (
        response['dependent_selection'],
        response['independent_selection'],
        definitions.KNOWN_CATEGORIES
        )


def pickle_buffer(fig):
    """Given an object, return pickled version as io.BytesIO object."""
    buf = io.BytesIO()
    output = buf
    pickle.dump(fig, output)
    plt.close(fig)
    return buf


def close_figures(figures='all'):
    """."""
    plt.close(figures)


# =============================================================================
# %% MULIVARIATE

def single_heatmap_facted(response, user_data):
    """."""
    def hist2dgrid(x, y, **kwargs):
        palette = kwargs.pop('color')
        plt.hist2d(x, y, cmap=palette, cmin=0.5)

    return pickle_buffer(
        sns.FacetGrid(
            data=user_data['custom_dataframe'],
            col=response['independent_groups'][1]['variable_names'][0]
            ).map(
                hist2dgrid,
                response['independent_groups'][0]['variable_names'][0],
                response['dependent_groups'][0]['variable_names'][1],
                color='inferno_r'
                ).fig)


def heatmap_grid_float(response, user_data):
    """."""
    numeric_vars = response['dependent_groups'][0]['variable_names'].copy()
    for indep_group in response['independent_groups']:
        numeric_vars += indep_group['variable_names']

    # correlation plot
    fig = plt.figure(figsize=[8, 5])
    sns.heatmap(user_data['custom_dataframe'][numeric_vars].corr(),
                annot=True, fmt='.3f', cmap='vlag_r', center=0)

    return pickle_buffer(fig)





# =============================================================================
# %% BIVARIATE

def pairplot_hist_diag_scatter(response, user_data):
    """Return paried grid of scatter plots with hist plots on the diagonal."""
    custom_dataframe = user_data['custom_dataframe']

    numeric_vars = response['independent_groups'][0]['variable_names'].copy()
    numeric_vars += response['independent_groups'][1]['variable_names']

    g = sns.pairplot(
        data=custom_dataframe,
        vars=numeric_vars)
    g.map_diag(plt.hist, bins=20)
    g.map_offdiag(plt.scatter)

    return pickle_buffer(g.fig)


def countplot_bi_grid_1cat_2cat(response, user_data):
    """."""
    pisa_df = user_data['custom_dataframe']

    # names of selected independent group variables
    primary_var_names = response[
        'independent_groups'][0]['variable_names']
    secondary_var_names = response[
        'independent_groups'][0]['variable_names']

    # size of primary group
    total_rows = len(primary_var_names)
    # size of secondary group
    total_cols = len(secondary_var_names)

    # two passes: one to get information about the plots, another to use it
    y_limits = {}
    # TODO: sharey sharex rather than two passes
    for first_pass in [True, False]:
        # allow a 5x5 space for each supplot
        if first_pass:
            fig = plt.figure(figsize=(5 * total_rows, 5 * total_cols))
        else:
            # discard first draft
            plt.close(fig)
            fig = plt.figure(figsize=(5 * total_rows, 5 * total_cols))

        # iterate over primary and secondary independent variables
        for index1, primary_var in enumerate(primary_var_names):
            for index2, secondary_var in enumerate(secondary_var_names):

                # set subfigure
                subfig_position = (index1 * total_cols) + index2 + 1
                fig.add_subplot(
                    total_rows, total_cols, subfig_position)
                # do subfigure
                sns.countplot(data=pisa_df,
                              x=primary_var,
                              hue=secondary_var,
                              palette='Blues')

                # Get y limits on first pass
                if first_pass:
                    new_ymin, new_ymax = plt.gca().get_ylim()[0:2]
                    if index2 == 0:
                        y_limits['min'], y_limits['max'] = new_ymin, new_ymax
                    else:
                        if new_ymax > y_limits['max']:
                            y_limits['max'] = new_ymax
                        if new_ymin < y_limits['min']:
                            y_limits['min'] = new_ymin

                # Apply subplot formatting on second pass
                if not first_pass:
                    x_lab, y_lab = None, None
                    # use x and y-axis labels only in first column
                    if index2 == 0:
                        y_lab = "Count"
                        x_lab = primary_var
                        # use longnames if available
                        if get_longnames([primary_var]):
                            x_lab = (primary_var + ': ' +
                                     get_longnames([primary_var])[0])

                    # use legend only in first row
                    if index1 == 0:
                        # use longnames if available
                        if get_longnames([secondary_var]):
                            legend_label = (
                                get_longnames([secondary_var])[0] +
                                "\n" + secondary_var
                                )
                        plt.gca().legend(title=legend_label)
                    else:
                        plt.gca().legend_.remove()

                    # set axis limits and titles
                    plt.gca().set(
                        ylim=(y_limits['min'], y_limits['max']),
                        xlabel=x_lab,
                        ylabel=y_lab
                        )

    figure_title = str(response['independent_groups'][1]['name'] +
                       " vs " +
                       response['independent_groups'][0]['name'])
    fig.suptitle(figure_title, fontsize=16)

    return pickle_buffer(fig)


# ============================================================================
# %% UNIVARIATE

def violinplot_uni_row_1cat(response, user_data):
    """Placeholer function."""
    # gather readable varaibles
    pisa_df = user_data['custom_dataframe']
    var_list = response['independent_groups'][0]['variable_names']
    category_order = (
        definitions.PREFERRED_NAMING[
            response['independent_groups'][0]['category']])
    dep_var = response['dependent_groups'][0]['name'] + "_mean"
    max_ylim, min_ylim = 0, 0
    # first generate subplots and extract max y limit,then apply y limit
    for first_pass in [True, False]:
        # initialize figure
        # width 5*n_vars, heighty5, force close to 1:1 aspect ratio
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
            # Get y limits on first pass
            if first_pass:
                axis = plt.gca()
                new_ymin, new_ymax = axis.get_ylim()[0:2]
                if new_ymax > max_ylim:
                    max_ylim = new_ymax
                if new_ymin < min_ylim:
                    min_ylim = new_ymin
                axis.get_ylim()

            # Apply max y lim to all subplots on second pass
            else:
                # only display y label on first subplot
                if var_index == 0:
                    try:
                        yname = get_longnames([dep_var])[0]
                    except IndexError:
                        yname = dep_var
                else:
                    yname = None
                # subbplot x label longnames if available
                xname = str(var_list[var_index])
                if get_longnames([var_list[var_index]]):
                    xname = xname + ': ' + str(
                        get_longnames([var_list[var_index]])[0])
                # set axis limits and titles
                axis.set(
                    ylim=(min_ylim, max_ylim),
                    xlabel=xname,
                    ylabel=yname
                    )

    return pickle_buffer(fig)


def boxplot_uni_row_1cat(response, user_data):
    """."""
    # shortened variable names
    pisa_df = user_data['custom_dataframe']
    var_list = response['independent_groups'][0]['variable_names']
    category_order = (
        definitions.PREFERRED_NAMING[
            response['independent_groups'][0]['category']])
    dep_var = response['dependent_groups'][0]['name'] + "_mean"

    # Figure size 5 by (num_vars*5)
    fig = plt.figure(figsize=(5 * len(var_list), 5))

    # add a subplot for each var_name in var_list by subplot index
    for var_index, var_name in enumerate(var_list):
        subplot_index = int("1" + str(len(var_list)) + str(var_index + 1))

        # sequential subplots:
        yname = None
        if var_index == 0:
            axis = plt.subplot(subplot_index)    # no axis to share yet
            yname = dep_var    # only for first subplot since y is shared
        # following subplots:
        else:
            axis = plt.subplot(subplot_index, sharey=axis)    # share yaxis

        # populate subplot with sns boxplot
        sns.boxplot(data=pisa_df, x=var_name, y=dep_var,
                    color=sns.color_palette()[0], order=category_order)

        # set subfigure axis titles
        axis.set(xlabel=get_longest_title(var_name), ylabel=yname)

    # set figure title
    figure_title = (response['dependent_groups'][0]['name'] + "  vs  " +
                    response['independent_groups'][0]['name'])
    fig.suptitle(figure_title, fontsize=16)

    return pickle_buffer(fig)


def boxplot_grid(response, user_data):
    """."""
    def box_plot_placeholder(x, y, **kwargs):
        default_color = sns.color_palette()[0]
        sns.boxplot(x, y, color=default_color)
    boxplot_parigrid = sns.PairGrid(
        data=user_data['custom_dataframe'],
        y_vars=response['dependent_groups'][0]['variable_names'],
        x_vars=response['independent_groups'][0]['variable_names'],
        height=3, aspect=1.5)
    boxplot_parigrid.map(box_plot_placeholder)

    return pickle_buffer(boxplot_parigrid.fig)

    # # independent groups
    # for group_index, group in enumerate(response['independent_groups']):
    #     category_order = (definitions.PREFERRED_NAMING[group['category']])
    #     var_list = group['variable_names']
    #     # add group name to figure title
    #     if len(response['independent_groups']) == group_index + 1:
    #         figure_title = figure_title + group['name']
    #     else:
    #         figure_title += group['name'] + ", "

    #     # group variables
    #     for var_index, var_name in enumerate(var_list):
    #         subplot_index = int(
    #             str(group_index + 1) + str(len(var_list)) + str(var_index + 1)
    #             )

    #         # subplot and shared y axis
    #         if var_index == 0:    # shared across row
    #             axis = plt.subplot(subplot_index)    # no axis to share yet
    #         # # shared across grid
    #         # if group_index == 0 and var_index == 0:
    #         #     axis = plt.subplot(subplot_index)
    #         else:    # following subplots share y axis
    #             axis = plt.subplot(subplot_index, sharey=axis)

    #         # populate subplot with sns boxplot
    #         sns.boxplot(data=pisa_df, x=var_name, y=dep_var,
    #                     color=sns.color_palette()[0], order=category_order)

    #         # shared y labels
    #         yname = None    # default blank y lable
    #         if group_index == 0 and var_index == 0:    # one lable for grid
    #             yname = dep_var
    #         if var_index == 0:    # one lable per row
    #             yname = dep_var
    #         # set subfigure axis titles
    #         axis.set(xlabel=get_longest_title(var_name), ylabel=yname)
    # # set figure title
    # fig.suptitle(figure_title, fontsize=16)

    # return pickle_buffer(fig)


# =============================================================================
# %% SINGLEVARIBLE

def barplot_single_single_1binary(response, user_data):
    """Return binary group summary as counts bar chart."""
    pisa_df = user_data['custom_dataframe']
    var_list = response['independent_groups'][0]['variable_names']

    base_color = sns.color_palette()[0]
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


def countplot_single_row_1cat(response, user_data):
    """."""
    pisa_df = user_data['custom_dataframe']
    var_list = response['independent_groups'][0]['variable_names']
    category = response['independent_groups'][0]['category']
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


def distplot_single_row_1float(response, user_data, kde):
    """Return a subplot of scatterplots of these float type varibles."""
    pisa_df = user_data['custom_dataframe']
    var_list = response['independent_groups'][0]['variable_names']
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
