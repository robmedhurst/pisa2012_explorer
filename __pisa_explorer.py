"""
PISA2012_EXPLORER.

This project aims to develop tools to assist with the wrangling and
exploration of the PISA 2012 dataset. Specifically, groups of similar
variables are explored concurrently.
"""

import ui.user_steps as user
import ui.wrangle as wrangle
import ui.save_load as save_load


# test_grouping01
# intial test set, no real meaning oustide of the study it emerged from
MY_PRESET = {
    'dependent_groups': {
        'math_result': [
            'PV1MATH', 'PV2MATH', 'PV3MATH', 'PV4MATH', 'PV5MATH'],
        'read_result': [
            'PV1READ', 'PV2READ', 'PV3READ', 'PV4READ', 'PV5READ']},
    'independent_groups': {
        'family_home': [
            'ST11Q01', 'ST11Q02', 'ST11Q03', 'ST11Q04', 'ST11Q05'],
        'parent_work': [
            'ST15Q01', 'ST19Q01'],
        'parent_isei': [
            'BFMJ2', 'BMMJ1', 'HISEI'],
        'HOMEPOS': [
            'HOMEPOS'],
        'person_item': [
            'ST26Q02', 'ST26Q03', 'ST26Q08', 'ST26Q09', 'ST26Q10', 'ST26Q11']},
    'pisa_sample': 1000}


def initialize(user_data=None, pisa2012=None):
    """Wrap function calls."""
    # returns pisa_df, inputs, categories_found, and graphics_objects
    return save_load.request_delivery(
        user.request_multivariate_graphics(
            user.request_bivariate_graphics(
                user.request_univariate_graphics(
                    user.single_variable_graphics(
                        wrangle.post_wrangle(
                            wrangle.wrangle(
                                user.initialize(user_data, pisa2012))))))))


def get_original(original_name='PISA2012_ORIGINAL'):
    """."""
    if original_name not in globals():
        return save_load.load_original_from_file()
    return original_name


if __name__ == '__main__':
    # load a global copy of original pisa data to avoid reloading
    PISA2012_ORIGINAL = get_original()

    # initialize with pisa data and variables of interest
    # without a preset, user may enter manually
    if 'OUTPUT' not in globals():
        OUTPUT = initialize(MY_PRESET, PISA2012_ORIGINAL)

    # initialize using previous output
    elif 'OUTPUT' in globals():
        OUTPUT = initialize(OUTPUT, PISA2012_ORIGINAL)

    # load previous output from file
    else:
        # TODO: retrieve_save should detect saves and prompt user selection
        OUTPUT = initialize(save_load.retrieve_save(), PISA2012_ORIGINAL)
