"""
This project aims to develop tools to assist with the wrangling and
exploration of the PISA 2012 dataset. Specifically, groups of similar
variables are explored concurrently.
"""


import zipfile
import warnings

import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns


from wrangle import wrangle as wrangle_and_get_categories
import category_functions
import category_definitions
import test_groupings


# Dataset can take a few minutes to load on some systems.
# Load once and only work on copy.
# Try to laod from csv then from zip.
def load_original(reload=True, integrity_check=False):
    """
    Load original PISA2012 dataset from file and return it as an DataFrame.
    Does not load if already in memory.
    Forces reload on parameter reload = True.
    """
    def pisa_confirmation(pisa_df):
        """
        Raise error if original csv or zip file being used fails hash check
        """
        print("Checking file integrity(this may take a few minutes)...\n")

        # TODO: implement integrity check
        passed = True

        # return if test passed, raise error if failed
        if passed:
            print(" Dataframe passed integrity check.\n")
        else:
            raise FileExistsError("Datafrane failed integrity check!")

    if 'PISA2012' not in globals():
        print("PISA2012 original not in locals, attempting to load",
              "(this may take a few minutes)...\n")
    elif reload:
        print("PISA2012 original exists, attempting to reload",
              "(this may take a few minutes)...\n")
    else:
        print("Variable with name PISA2012 already in memory.\n")

    # load, check, raise error if needed
    if ('PISA2012' not in globals()) or (reload):
        # global PISA2012
        try:    # loading directly from csv
            pisa_df = pd.read_csv(
                'pisa2012.csv', sep=',', encoding='latin-1',
                error_bad_lines=False, dtype='unicode', index_col=False)
            print("Loaded from csv.\n")
        except FileNotFoundError:
            try:    # loading directly from zip
                pisa_df = pd.read_csv(
                    zipfile.ZipFile(
                        'pisa2012.csv.zip', 'r').open('pisa2012.csv'),
                    sep=',', encoding='latin-1', error_bad_lines=False,
                    dtype='unicode', index_col=False)
                print("Loaded from zip.\n")
            except FileNotFoundError:    # loading failed
                raise FileNotFoundError("PISA2012 not in local directory.")
    if integrity_check:
        pisa_confirmation(pisa_df)
    return pisa_df

def initialize(pisa_df, inputs):
    """
    general wrapper
    """
    return group_post_wrangle(*wrangle_and_get_categories(pisa_df, inputs))

def get_longnames(names):
    """
    Return list of PISA variable descriptions corresponding to variable
    shortnames given by list name.
    Resource is read from local copy of pisadict2012.csv
    """
    pisadict2012 = pd.read_csv(
        'pisadict2012.csv',
        sep=',', encoding='latin-1', error_bad_lines=False,
        dtype='unicode', index_col=False).rename(
            columns={'Unnamed: 0':'varname', 'x': 'description'})
    names = list(names)
    return list(pisadict2012.query("varname in @names")['description'])

def group_post_wrangle(pisa_df, inputs, group_category_matches):
    """
    apply category specific actions for each group
    raise warning if no corresponding function found
    """
    # group_category_matches holds indep and dependent groups seperately
    for subset in group_category_matches:

        # iterate group category matches
        for group_name in group_category_matches[subset]:
            category = group_category_matches[subset][group_name]

            # check if associated post wrangling group actions are available
            if category + "_group_post_wrangle" in dir(category_functions):
                # function call using getattr
                getattr(
                    category_functions, (category + "_group_post_wrangle"))(
                        group_name, pisa_df, inputs)
            # print warning if no category found
            else:
                warnings.warn(
                    "No post wrangle funcion found for group: '" +
                    group_name + "    of category: " + category + "\n")
    return pisa_df, inputs, group_category_matches


PISA2012 = load_original(reload=False, integrity_check=False)

RETURNED_FROM_INITIALIZE = initialize(
    PISA2012.sample(500),
    [category_definitions.KNOWN_CATEGORIES,
     category_definitions.PREFERRED_NAMING,
     test_groupings.INDEP_test_grouping02,
     test_groupings.DEPEN_test_grouping02])
