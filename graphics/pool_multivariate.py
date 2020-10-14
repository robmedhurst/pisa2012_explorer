"""
Functions for looking up multivariate plots functions.

If 'functions' already exists in given 'response', return associated plot.
Else, if 'response' meets criteria, check warnings, then return true.
"""

import graphics.graphics as gs


def heatmap_grid_float(response, user_data):
    """Return a correlation matrix with heatmap."""
    if 'functions' in response:
        return gs.heatmap_grid_float(response, user_data)
    else:
        # do checks
        dep, indep, categories = gs.concise_reponse_info(response)
        return (
            dep[0]['category'] == 'float' and
            indep[0]['category'] == 'float' and
            indep[1]['category'] == 'float' and
            indep[2]['category'] == 'float'
            )


def single_heatmap_facted(response, user_data):
    """Return a heat map faceted by category."""
    if 'functions' in response:
        return gs.single_heatmap_facted(response, user_data)

    # get group information for selected groups
    deps, indeps, categories = gs.concise_reponse_info(response)

    # non-critical
    def do_warnings():
        def notifiy_user(warning_message):
            print(warning_message)
        # check group sizes are one; this plot uses only one variable
        message = ("Note: This plot uses one variable per group, ",
                   "only using first var from selected group.")
        if len(indeps[0]) > 1:
            notifiy_user(message)
        if len(indeps[1]) > 1:
            notifiy_user(message)

    # requirements
    def necessary_conditions_met():
        return (
            deps[0]['category'] == 'float' and
            indeps[0]['category'] == 'float' and
            indeps[1]['category'] in categories
            )

    if necessary_conditions_met():
        do_warnings()
        return True
