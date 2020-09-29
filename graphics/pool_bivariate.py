"""
Placeholder functions for looking up bivariate plots.

Functions for bivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs

# BIVARIATE GRAPHICS POOL


def pairplot_hist_diag_scatter(response, user_data):
    """Return a pair grid of point plots."""
    if 'functions' in response:
        return gs.pairplot_hist_diag_scatter(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            indep[0]['category'] == "float" and
            indep[1]['category'] == "float"
            )


def countplot_bi_grid_1cat_2cat(response, user_data):
    """Return a grid of countplots."""
    if 'functions' in response:
        return gs.countplot_bi_grid_1cat_2cat(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            indep[0]['category'] in categories and
            indep[1]['category'] in categories
            )


def heatmap_bi_grid_1float_2float(response, user_data):
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
