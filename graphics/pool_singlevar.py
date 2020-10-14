"""
Functions for single varible group plotting.

If 'functions' already exists in given 'response', return associated plot.
Else, if 'response' meets criteria, check warnings, then return true.

For graphing functions themselves, see   main.graphics.graphics.py
"""

import graphics.graphics as gs


def distribution_nokde_row_float(response, user_data):
    """Return a row of distribution plots."""
    if 'functions' in response:
        return gs.distplot_single_row_1float(
            response, user_data, "float_no_kde")
    else:    # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            indep[0]['category'] == 'float'
            )


def distribution_kde_row_float(response, user_data):
    """Return a row of frequencies plots with kde."""
    if 'functions' in response:
        return gs.distplot_single_row_1float(
            response, user_data, "float_yes_kde")
    else:    # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            indep[0]['category'] == 'float'
            )


def count_row_categorical(response, user_data):
    """Return a row of count plots."""
    if 'functions' in response:
        return gs.countplot_single_row_1cat(response, user_data)
    else:    # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            indep[0]['category'] in categories
            )


def bar_binary_counts(response, user_data):
    """Return binary group summary as counts bar chart."""
    if 'functions' in response:
        return gs.barplot_single_single_1binary(response, user_data)
    else:    # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            indep[0]['category'] in categories and
            len(categories[indep[0]['category']]) == 2
            )
