"""
PISA2012_EXPLORER.

This project aims to develop tools to assist with the wrangling and
exploration of the PISA 2012 dataset. Specifically, groups of similar
variables are explored concurrently.
"""

import main.interface.initialize as user_initialize
import main.interface.graphics as user_graphics
import main.interface.deliver as user_delivery
import main.interface.loaders as loaders

import main.wrangle as wrangle


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
    return user_delivery.request_delivery(
        user_graphics.request_multivariate(
            user_graphics.request_bivariate(
                user_graphics.request_univariate(
                    user_graphics.single_variable(
                        wrangle.post_wrangle(
                            wrangle.wrangle(
                                user_initialize.initialize(
                                    user_data, pisa2012))))))))


def get_original(original_name='PISA2012_ORIGINAL'):
    """."""
    if original_name not in globals():
        return loaders.original_from_file()
    return original_name


if __name__ == '__main__':
    # load a global copy of original pisa data to avoid reloading
    PISA2012_ORIGINAL = get_original()

    # initialize with pisa data and variables of interest
    if 'OUTPUT' not in globals():
        OUTPUT = initialize(MY_PRESET, PISA2012_ORIGINAL)

    # without a preset, user may enter manually
    elif 'OUTPUT' not in globals():
        OUTPUT = initialize(pisa2012=PISA2012_ORIGINAL)

    # initialize using previous output
    elif 'OUTPUT' in globals():
        OUTPUT = initialize(OUTPUT, PISA2012_ORIGINAL)

    # load previous output from file
    else:
        OUTPUT = initialize(loaders.retrieve_save(), PISA2012_ORIGINAL)
