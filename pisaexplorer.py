# This tool aims to aid in the exploration of the PISA 2012 dataset,
# allowing users to concurrently examine a group of similar variables.

import zipfile

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns



#%% Load CSVs

# unzip and load original csv data
PISA2012 = pd.read_csv(
    zipfile.ZipFile('pisa2012.csv.zip', 'r').open('pisa2012.csv'),
    sep=',', encoding='latin-1', error_bad_lines=False, 
    dtype='unicode', index_col=False)


# load csv pisa variable descriptions
PISADICT2012 = pd.read_csv(
    'pisadict2012.csv', 
    sep=',', encoding='latin-1', error_bad_lines=False, 
    dtype='unicode', index_col=False).rename(
        columns={'Unnamed: 0':'varname', 'x': 'description'})



#%% Define terms

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
# Dictionary containing lists. Each list is a group of variable names.
# The variables in a group must be numeric.
dependent_group = {}
