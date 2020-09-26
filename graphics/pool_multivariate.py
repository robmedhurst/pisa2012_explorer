"""
Placeholder functions for looking up multivariate plots.

Functions for multivariate group plotting with verbose names to be
caught by keyword.
"""

import graphics.graphics as gs


def heatmap_multi_grid_1float_2float_3float(response, user_data):
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
