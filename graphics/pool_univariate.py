"""
Functions for looking up bivariate plots.

If 'functions' already exists in given 'response', return associated plot.
Else, if 'response' meets criteria, check warnings, then return true.

For graphing functions themselves, see   main.graphics.graphics.py
"""

import graphics.graphics as gs


def violin_row_categorical_dep_float(response, user_data):
    """Return a row of violin plots."""
    if 'functions' in response:
        return gs.violinplot_uni_row_1cat(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            dep[0]['category'] == 'float' and
            indep[0]['category'] in categories
            )


def boxplot_row_categorical_dep_float(response, user_data):
    """Return a row of box plots."""
    if 'functions' in response:
        return gs.boxplot_uni_row_1cat(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            dep[0]['category'] == 'float' and
            indep[0]['category'] in categories
            )


def boxplot_grid_categorical_dep_float(response, user_data):
    """Return a grid of box plots."""
    if 'functions' in response:
        return gs.boxplot_grid(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            dep[0]['category'] == 'float' and
            indep[0]['category'] in categories
            )


def heatmap_single_float(response, user_data):
    """Return a correlation matrix with heatmap."""
    if 'functions' in response:
        return gs.heatmap_grid_float(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            dep[0]['category'] == 'float' and
            indep[0]['category'] == 'float'
            )


def heatmap_uni_grid_1float(response, user_data):
    """Return a correlation matrix with heatmap."""
    if 'functions' in response:
        return gs.heatmap_grid_float(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            dep[0]['category'] == 'float' and
            indep[0]['category'] == 'float'
            )
