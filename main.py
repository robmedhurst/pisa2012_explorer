import zipfile

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from wrangle import wrangle as wrangle_and_get_categories
import category_functions
import category_definitions
import test_groupings


# Dataset can take a few minutes to load on older sytems.
# Load once and only work on copy.
if 'PISA2012' not in locals():
    
    ### raw csv data
    PISA2012 = pd.read_csv(
        zipfile.ZipFile('pisa2012.csv.zip', 'r').open('pisa2012.csv'),
        sep=',', encoding='latin-1', error_bad_lines=False,
        dtype='unicode', index_col=False)


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
    raise ValueError if no corresponding function found
    """
    # group_category_matches holds indep and dependent groups seperately
    for subset in group_category_matches:
        # iterate group category matches
        for group_name in group_category_matches[subset]:
            category = group_category_matches[subset][group_name]
            # check if associated post wrangling group actions are available
            if (category + "_group_post_wrangle") in dir(category_functions):
    
                # function call using getattr
                getattr(
                    category_functions, (category + "_group_post_wrangle"))(
                        group_name, pisa_df, inputs)
            else:
                raise ValueError(
                    "No post wrangle funcion found for group: '" + \
                        group_category_matches[subset][group_name])

    return pisa_df, inputs, group_category_matches

returned_from_initialize = initialize(
    PISA2012.sample(500),
    [category_definitions.KNOWN_CATEGORIES,
      category_definitions.PREFERRED_NAMING,
      test_groupings.INDEP_test_grouping02,
      test_groupings.DEPEN_test_grouping02])




# a temporary helper function to check each column against known categories
def completeness_check(column_start, column_end, interest_in=None):
    
    check = {}
    for var in PISA2012.columns[column_start:column_end]:
        check[str(var)] = [str(var)]

    completeness = initialize(
        PISA2012.sample(500),
        [category_definitions.KNOWN_CATEGORIES,
          category_definitions.PREFERRED_NAMING,
          check,
          test_groupings.DEPEN_test_grouping01])[2]['indep_categories']

    if interest_in:
        for key in completeness:
            if completeness!= interest_in:
                print(key)

    return completeness

# check 100 at a time
completeness_check(0, 20, None)


def get_all_unique_short_categories(max_length=5,
                                    column_start=None, column_end=None):
    """
    Pull sets of unique values from PISA2012 dataset for building 
    collection of known categories.
    """
    found_unique_sets = []
    for var in PISA2012.columns[column_start:column_end]:

        # get unique_values, without nulls
        unique_values = set({})
        for unique_val in set(PISA2012[var].unique()):
            if not pd.isnull(unique_val):
                unique_values.add(unique_val.strip())

        # check if already found, check length
        if (unique_values not in found_unique_sets) and (1 < len(unique_values) < max_length):
            # check for subsets
            for past_match in found_unique_sets:
                # skip if subset of existing set
                if set(unique_values).issubset(past_match):
                    unique_values = False
                    break
                # remove existing set if superset of existing set
                elif set(past_match).issubset(unique_values):
                    found_unique_sets.remove(past_match)
            if unique_values:
                found_unique_sets.append(unique_values)

    return found_unique_sets

all_short_uniques = get_all_unique_short_categories(20)

