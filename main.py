"""
PISA2012_EXPLORER.

This project aims to develop tools to assist with the wrangling and
exploration of the PISA 2012 dataset. Specifically, groups of similar
variables are explored concurrently.
"""

import zipfile
# import warnings

import pandas as pd

from wrangle import wrangle as wrangler
import post_wrangling
import category_definitions
import test_groupings
import univariate_graphics_pool


# Dataset can take a few minutes to load on some systems.
# Load once and only work on copy.
# Try to laod from csv then from zip.
def load_original(reload=False, integrity_check=False):
    """
    Load original PISA2012 dataset from file and return it as an DataFrame.

    Does not load if already in memory.
    Forces reload on parameter 'reload=True'.
    Checks datastructure if parameter 'integrety_check=True'.
    """
    def confirm_pisa_df():
        """
        Placehold function.

        Will implement hash check on the csv and/or zip files.
        """
        if integrity_check:
            print("Checking file integrity(this may take a few minutes)...\n")
            # TODO: implement integrity check
            #
            # do the check here
            #
            #
            #
            #
            #
            passed = True    # result of check
            # return if test passed, raise error if failed
            if passed:
                print("Dataframe passed integrity check.\n")
                return pisa_df
            raise FileExistsError("Datafrane failed integrity check!")
        return pisa_df
    if 'PISA2012' not in globals():
        print("PISA2012 original not in locals, attempting to load",
              "(this may take a few minutes)...\n")
    elif reload:
        print("PISA2012 original exists, attempting to reload",
              "(this may take a few minutes)...\n")
    else:
        print("Variable with name PISA2012 already in memory.\n")
        pisa_df = PISA2012
        return confirm_pisa_df()
    # load, check, raise error if needed
    if ('PISA2012' not in globals()) or (reload):
        # global PISA2012
        try:    # loading directly from csv
            pisa_df = pd.read_csv(
                'pisa2012.csv', sep=',', encoding='latin-1',
                error_bad_lines=False, dtype='unicode', index_col=False)
            print("Loaded from csv.\n")
            return confirm_pisa_df()
        except FileNotFoundError:
            try:    # loading directly from zip
                pisa_df = pd.read_csv(
                    zipfile.ZipFile(
                        'pisa2012.csv.zip', 'r').open('pisa2012.csv'),
                    sep=',', encoding='latin-1', error_bad_lines=False,
                    dtype='unicode', index_col=False)
                print("Loaded from zip.\n")
                return confirm_pisa_df()
            except FileNotFoundError:    # loading failed
                raise FileNotFoundError("PISA2012 not in local directory.")


def get_longnames(names):
    """
    Return PISA2012 long names given short names.

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


def post_wrangle(pisa_df, inputs, group_category_matches):
    """Apply category specific post wrangle functions."""
    # group_category_matches holds indep and dependent groups seperately
    for subset in group_category_matches:
        # iterate group category matches
        for group_name in group_category_matches[subset]:
            category = group_category_matches[subset][group_name]

            # check if associated post wrangling group actions are available
            if category + "_group_post_wrangle" in dir(post_wrangling):
                # function call using getattr
                getattr(
                    post_wrangling,
                    (category + "_group_post_wrangle"))(
                        group_name, pisa_df, inputs)
    return pisa_df, inputs, group_category_matches


def initialize(pisa_df, inputs=None):
    """Wrap function calls."""
    # use test inputs if none given
    if inputs is None:
        inputs = [
            category_definitions.KNOWN_CATEGORIES,
            category_definitions.PREFERRED_NAMING,
            test_groupings.INDEP_TEST_GROUPING01,
            test_groupings.DEPEN_TEST_GROUPING01]
    # returns pisa_df, inputs, categories_found, and graphics_objects
    return (
        univariate_graphics(
            *post_wrangle(
                *wrangler(
                    pisa_df, inputs))))


def univariate_graphics(pisa_df, inputs, group_category_matches):
    """
    Call category specific graphics functions.

    undesired_graphics, is a list of strings to ignore when searching for
    graphics functions.
    """
    (independent_groups, dependent_groups) = inputs[2:]

    def get_vars(group_name):
        """Get list of variable names for group of vars, group_name."""
        v_list = []
        if group_name in independent_groups:
            v_list = independent_groups[group_name]
        elif group_name in dependent_groups:
            v_list = dependent_groups[group_name]
        return v_list

    def get_univariate_graphic():
        print("calling:  ", function_name)
        return getattr(
            univariate_graphics_pool,
            (function_name))(
                group_specific_parameters, pisa_df, inputs)

    graphic_objects = []
    # iterate group category matches
    for subset in group_category_matches:
        print("\n\n", list(group_category_matches[subset]))
        for group_name in group_category_matches[subset]:

            # group specific parameters:
            category = group_category_matches[subset][group_name]
            group_specific_parameters = (
                group_name, get_vars(group_name), category)
            print("\n", group_name, " -  ", category)
            # univariate_graphics_pool contains univariate graphics functions
            for function_name in dir(univariate_graphics_pool)[8:]:

                if category in function_name:
                    graphic_objects.append(get_univariate_graphic())

                if category in inputs[0] and "categorical" in function_name:
                    graphic_objects.append(get_univariate_graphic())

            if category in inputs[0] and len(inputs[0][category]) == 2:
                function_name = "binary_counts_singleplot"
                group_specific_parameters = (
                    group_name, get_vars(group_name), category)
                graphic_objects.append(get_univariate_graphic())

            if category == "float" and len(get_vars(group_name)) > 1:
                function_name = "float_means_singleplot"
                group_specific_parameters = (
                    group_name, [group_name + "_mean"], category)
                graphic_objects.append(get_univariate_graphic())

    return pisa_df, inputs, group_category_matches, graphic_objects


# %%


if __name__ == '__main__':
    PISA2012 = load_original(reload=False, integrity_check=False)
    PISA_SAMPLE = PISA2012.sample(500)
    OUTPUT = initialize(PISA_SAMPLE.copy(),
                        [category_definitions.KNOWN_CATEGORIES,
                         category_definitions.PREFERRED_NAMING,
                         test_groupings.INDEP_TEST_GROUPING01,
                         test_groupings.DEPEN_TEST_GROUPING01]
                        )


OUTPUT[3][0]
OUTPUT[3][1]
OUTPUT[3][2]
OUTPUT[3][3]
OUTPUT[3][4]
OUTPUT[3][5]
OUTPUT[3][6]
OUTPUT[3][7]
OUTPUT[3][8]
OUTPUT[3][9]
OUTPUT[3][10]
OUTPUT[3][11]
OUTPUT[3][12]
OUTPUT[3][13]
OUTPUT[3][14]
