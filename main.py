import zipfile
import warnings

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
    raise warning if no corresponding function found
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
            # print warning if no category found 
            # TODO: remove print behavior
            else:
                warnings.warn(
                    "No post wrangle funcion found for group: '" + 
                    group_name + "    of category: " + category + "\n")
    return pisa_df, inputs, group_category_matches

returned_from_initialize = initialize(
    PISA2012.sample(500),
    [category_definitions.KNOWN_CATEGORIES,
      category_definitions.PREFERRED_NAMING,
      test_groupings.INDEP_test_grouping02,
      test_groupings.DEPEN_test_grouping02])


# temporary testing, will delete later:
test_groupings.completeness_check(PISA2012, 0, 20, None)
all_short_uniques = test_groupings.get_all_unique_short_categories(PISA2012, 20)
