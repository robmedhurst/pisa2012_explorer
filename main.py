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
def load_original(reload=False, integrity_check=False):
    """
    Load original PISA2012 dataset from file and return it as an DataFrame.
    Does not load if already in memory.
    Forces reload on parameter 'reload=True'.
    Checks datastructure if parameter 'integrety_check=True'.
    """
    def confirm_pisa_df():
        """
        Return DataFrame pisa_df if no error found or if no check requested.
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
                message = "No post wrangle funcion found for group: '" + \
                    group_name + "', category: '" + category + "'"
                warnings.warn(message)
    return pisa_df, inputs, group_category_matches

def initialize(given_sample=None, given_inputs=None):
    """
    general wrapper
    """
    # generate new sample if none given
    if given_sample is None:
        pisa_df = PISA2012.sample(500)
    else:
        pisa_df = given_sample
    # use test inputs if none given
    if given_inputs is None:
        inputs = [
            category_definitions.KNOWN_CATEGORIES,
            category_definitions.PREFERRED_NAMING,
            test_groupings.INDEP_test_grouping01,
            test_groupings.DEPEN_test_grouping01]
    else:
        inputs = given_inputs
    # returns pisa_df, inputs, categories_found
    return group_post_wrangle(*wrangle_and_get_categories(pisa_df, inputs))




PISA2012 = load_original(reload=False, integrity_check=False)



PISA_SAMPLE = PISA2012.sample(500)
TEMP_OUTPUT = initialize(PISA_SAMPLE)




### TEMPORARY
# A helper function to check each column against known categories
def completeness_check(pisadf, column_start, column_end, interest_in=None):
    """
    A helper function to check each column against known categories
    """
    check = {}
    for var in pisadf.columns[column_start:column_end]:
        check[str(var)] = [str(var)]
    indep_categories = initialize()[2]['indep_categories']
    if interest_in:
        for var_name in indep_categories:
            if indep_categories[var_name] == interest_in:
                print(var_name)

    return pd.DataFrame(
        list(indep_categories.values()),
        index=list(indep_categories.keys()))

# temporary testing vars, will delete before merging:
COMPLETENESS_CHECK = completeness_check(PISA2012, 0, 20, None)



# A helper function to view a list of categories extracted from PISA2012
# Can be used to create new category_definitons.
def get_all_unique_short_categories(pisadf, max_length=5,
                                    column_start=None, column_end=None):
    """
    Pull sets of unique values from PISA2012 dataset for building
    collection of known categories.
    """
    found_unique_sets = []
    for var in pisadf.columns[column_start:column_end]:

        # get unique_values, without nulls
        unique_values = set({})
        for unique_val in set(pisadf[var].unique()):
            if not pd.isnull(unique_val):
                unique_values.add(unique_val.strip())

        # check if already found, check length
        if (unique_values not in found_unique_sets
           ) and (1 < len(unique_values) < max_length):
            # check for subsets
            for past_match in found_unique_sets:
                # skip if subset of existing set
                if set(unique_values).issubset(past_match):
                    unique_values = False
                    break
                # remove existing set if superset of existing set
                if set(past_match).issubset(unique_values):
                    found_unique_sets.remove(past_match)
            if unique_values:
                found_unique_sets.append(unique_values)
    return found_unique_sets

SHORT_UNIQUES = get_all_unique_short_categories(PISA2012, 20, 0, 20)
