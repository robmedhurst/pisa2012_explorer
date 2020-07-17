# This tool aims to aid in the exploration of the PISA 2012 dataset,
# allowing users to concurrently examine a group of similar variables.


#%% Import Libraries

import zipfile

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


#%% FUNCTIONS


def initialize(pisa_df):
    """
    general wrapper
    """
    wrangle(pisa_df)

    # df is edited in place, return is for pipeline
    return pisa_df


#%%% Wrangling Functions

def wrangle(pisa_df):
    """
    wrangling wrapper
    """
    def select_columns_and_drop_nulls():
        ### drop unused columns
        ### drop nulls
        pass

    ### CAUTION:    large sets of variables will reduce the sample size
    ### Reason:     each variable has its own set of nulls
    ### Solution:   reduce variable sets after finding interactions
    select_columns_and_drop_nulls()

    # for pisa_group in (
    #         list(independent_groups.values()) +
    #         list(dependent_groups.values())):
    #     strings_to_known_categories(pisa_group, df)

    return pisa_df


def strings_to_known_categories(pisa_set, pisa_df):
    """
    Get variable type from of known_categories.
    Apply formatting if value types of group memebers is not mismatched.
    """
    def apply_preferred_values(category_key):
        """ \
        update strings to preferred values (ex: "Yes" == True)
        raise ValueError if incomplete preferred values found
        """
        # chek category_key member of preferred_values
        # one column at a time, update to corresponding preferred values
            # strip white space so values are uniform
            # replace each known value
        # confirm values are from preferred_naming, none overlooked
        # if unique_values not a subset of preferred_values[key]:
            # raise ValueError(var + ': incomplete preferred values.')

    ### Use try and execpt to test for numeric types
    # try convert int:
    # except: try: convert float
    # except: apply_preferred_values(get_category(pisa_set, pisa_df))

    return pisa_df


def get_category(pisa_set, pisa_df):
    """
    Determine if variables in pisa_set match a known categoy.
    Determine if variables in pisa_set each have same category.
    (Return category name) or (raise ValueError if mismatched).
    """
    category_key = "String"   # default to plain text

    ### check first variable against known categories
    # get and store unique values
    # check if those unique values are a subset of a known category
    ### if matched: category_key = known_key

    ### iterate over group
    # verify same category in each
    ### if not: raise ValueError("category mismatch in set " + pisa_set)

    return category_key



#%% MAIN


#%%% Load CSVs

### raw csv data
PISA2012 = pd.read_csv(
    zipfile.ZipFile('pisa2012.csv.zip', 'r').open('pisa2012.csv'),
    sep=',', encoding='latin-1', error_bad_lines=False,
    dtype='unicode', index_col=False)


### variable descriptions
PISADICT2012 = pd.read_csv(
    'pisadict2012.csv',
    sep=',', encoding='latin-1', error_bad_lines=False,
    dtype='unicode', index_col=False).rename(
        columns={'Unnamed: 0':'varname', 'x': 'description'})


#%%% Load Terms

### Known Categories
# Dictionary containing lists. Each list contains the values of known
# PISA variables. The key is a short string description of the category.
known_categories = {}

### Preferred Category Values
# Dictionary containing lists. Each list contains preferred values for
# known category associated with key.
prefered_naming = {}

### Groups of Indepenent Variables
# Dictionary containing lists. Each list is a group of variable names.
# The variables in a group must be of same type (float, y/, category X).
independent_groups = {}

### Groups of Depenent Variables
# Dictionary containing list. List is a group of variable names.
# The variables must be numeric.
dependent_group = {}


#%%% __main__

if __name__ == "__main__":

    sample_size = 500

    pisa_sample = PISA2012.sample(sample_size)

    initialize(pisa_sample)
