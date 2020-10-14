"""
Functions for looking up bivariate plots.

If 'functions' already exists in given 'response', return associated plot.
Else, if 'response' meets criteria, check warnings, then return true.

For graphing functions themselves, see   main.graphics.graphics.py
"""

import graphics.graphics as gs

# BIVARIATE GRAPHICS POOL


def scatter_grid_hist_diagonal_floats(response, user_data):
    """Return a grid of point plots with histograms on the diagonal."""
    if 'functions' in response:
        return gs.pairplot_hist_diag_scatter(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            indep[0]['category'] == "float" and
            indep[1]['category'] == "float"
            )


def count_grid_categoricals(response, user_data):
    """Return a grid of count bar plots."""
    if 'functions' in response:
        return gs.countplot_bi_grid_1cat_2cat(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            indep[0]['category'] in categories and
            indep[1]['category'] in categories
            )


def heatmap_single_floats(response, user_data):
    """Return a correlation matrix with heatmap."""
    if 'functions' in response:
        return gs.heatmap_grid_float(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            dep[0]['category'] == 'float' and
            indep[0]['category'] == 'float' and
            indep[1]['category'] == 'float'
            )
