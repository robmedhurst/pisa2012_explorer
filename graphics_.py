"""Graphic functions supporting exploratory pisa2012 analysis."""

import io
import pickle

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import main_definitions as definitions
# from main_ import get_longnames


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def pickle_buffer(fig):
    """Given an object, return pickled version as io.BytesIO object."""
    buf = io.BytesIO()
    output = buf
    pickle.dump(fig, output)
    plt.close(fig)
    return buf


def get_longnames(names):
    """
    Return PISA 2012 long names given short names.

    Return list of PISA variable descriptions corresponding to variable
    shortnames given by list name.
    Resource is read from local copy of pisadict2012.csv
    """
    pisadict2012 = pd.read_csv(
        'pisadict2012.csv',
        sep=',', encoding='latin-1', error_bad_lines=False,
        dtype='unicode', index_col=False).rename(
            columns={'Unnamed: 0': 'varname', 'x': 'description'})
    names = list(names)
    return list(pisadict2012.query("varname in @names")['description'])


# =============================================================================
# BIVARIATE
# =============================================================================

def countplot_bi_column_1cat_2cat(response_info, user_data):
    """Placeholer function."""
    pisa_df = user_data['custom_dataframe']
    if len(response_info['dependent_groups']['variables']) > 1:
        dep_name = response_info['dependent_groups']['name'] + "_mean"
    else:
        dep_name = response_info['dependent_groups']['name']
    # TODO: utilize group members (0, 1 are arbitrary)
    indep1 = response_info['independent_groups'][0]['variables'][0]
    indep2 = response_info['independent_groups'][1]['variables'][0]
    # fig = plt.figure(figsize=(5 * len(var_list), 5))
    fig = plt.figure()
    sns.countplot(
        data = pisa_df, x = indep1, hue = indep2, palette = 'Blues')
    return pickle_buffer(fig)

    # var_list = response_info['independent_groups'][0]['variables']
    # category_order = (
    #     definitions.PREFERRED_NAMING[
    #         response_info['independent_groups'][0]['category']])
    # dep_var = response_info['dependent_groups']['name'] + "_mean"
    # max_ylim, min_ylim = 0, 0

    # will loop and create column , for now use first indep of primary
    # expect secondary indep group to be of length one (perhaps ignore the rest?)

    # # since there's only three subplots to create, using the full data should be fine.
    # plt.figure(figsize = [8, 8])
    # # subplot 1: color vs cut
    # plt.subplot(3, 1, 1)
    # sb.countplot(data = diamonds, x = 'color', hue = 'cut', palette = 'Blues')
    # # subplot 2: clarity vs. cut
    # ax = plt.subplot(3, 1, 2)
    # sb.countplot(data = diamonds, x = 'clarity', hue = 'cut', palette = 'Blues')
    # ax.legend(ncol = 2) # re-arrange legend to reduce overlapping
    # # subplot 3: clarity vs. color, use different color palette
    # ax = plt.subplot(3, 1, 3)
    # sb.countplot(data = diamonds, x = 'clarity', hue = 'color', palette = 'Greens')
    # ax.legend(loc = 1, ncol = 2) # re-arrange legend to remove overlapping
    # plt.show()



# =============================================================================
# UNIVARIATE
# =============================================================================

def violinplot_uni_row_1cat(response_info, user_data):
    """Placeholer function."""
    # gather readable varaibles
    pisa_df = user_data['custom_dataframe']
    var_list = response_info['independent_groups'][0]['variables']
    category_order = (
        definitions.PREFERRED_NAMING[
            response_info['independent_groups'][0]['category']])
    dep_var = response_info['dependent_groups']['name'] + "_mean"
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


def boxplot_uni_row_1cat(response_info, user_data):
    """."""
    # gather readable varaibles
    pisa_df = user_data['custom_dataframe']
    var_list = response_info['independent_groups'][0]['variables']
    category_order = (
        definitions.PREFERRED_NAMING[
            response_info['independent_groups'][0]['category']])
    dep_var = response_info['dependent_groups']['name'] + "_mean"
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

            sns.boxplot(data=pisa_df, x=var_name, y=dep_var,
                        color=sns.color_palette()[0], order=category_order)

            # Customize axis properties:
            # Get y limits on first pass
            if first_pass:
                axis = plt.gca()
                # start with max/min y values from first plot
                if var_index == 0:
                    min_ylim, max_ylim = axis.get_ylim()[0:2]
                    # max_ylim = 0
                    # min_ylim = 0
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
                    # ylim=(0, max_ylim),
                    ylim=(min_ylim, max_ylim),
                    xlabel=xname,
                    ylabel=yname
                    )

    return pickle_buffer(fig)


# =============================================================================
# SINGLE VARIBLE
# =============================================================================

def barplot_single_single_1binary(response, user_data):
    """Return binary group summary as counts bar chart."""
    pisa_df = user_data['custom_dataframe']
    var_list = response['independent_groups'][0]['variables']

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
    var_list = response['independent_groups'][0]['variables']
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
    var_list = response['independent_groups'][0]['variables']
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
