"""
Wrangling functions for pisa2012_explorer project.

This tool aims to aid in the exploration of the PISA 2012 dataset,
allowing users to concurrently examine a group of similar variables.
"""

import numpy as np

import main.definitions as category_definitions
import main.actions as category_actions


def post_wrangle(user_data):
    """Apply category specific post wrangle functions."""
    for target in ['dependent_groups', 'independent_groups']:
        for group in user_data[target].values():
            category = group['category']
            if category + "_post_wrangle" in dir(category_actions):
                getattr(category_actions, (
                    category + "_post_wrangle"))(group['name'], user_data)
    return user_data


def wrangle(user_data):
    """Wrap functions for wrangling. Return edited inputs."""
    def select_columns_and_drop_nulls():
        """
        Discard unspecified columns and remove rows with Null values.

        Remove columns from that are not in any given groups.
        Remove observations containing nulls.
        """
        pisa_df = user_data['pisa_sample'].copy()

        # drop unused columns
        def all_var_names():
            variable_list = []
            for target in ['dependent_groups', 'independent_groups']:
                for group in user_data[target].values():
                    variable_list.extend(group['variable_names'])
            return variable_list

        pisa_df.drop(pisa_df.columns.difference(all_var_names()),
                     axis='columns', inplace=True)
        # drop nulls
        pisa_df.dropna(inplace=True)

        # update user_data
        user_data['custom_dataframe'] = pisa_df

    def apply_preferred_values():
        """
        Apply preferred values to groups of known category.

        Update strings to preferred values (ex: "Yes" == True) or
        raise ValueError if incomplete preferred values found.
        """
        def do_know_category():
            # update to corresponding preferred values
            for var in group_var_list:

                # strip white space to match know_categories
                pisa_df[var] = pisa_df[var].map(lambda x: x.strip())

                # replace each known value
                for known, preferred in zip(
                        category_definitions.KNOWN_CATEGORIES[category_key],
                        category_definitions.PREFERRED_NAMING[category_key]):
                    pisa_df.loc[pisa_df[var] == known, var] = preferred

                # confirm values are from preferred_naming, none overlooked
                if not set(pisa_df[var].unique()).issubset(
                        category_definitions.PREFERRED_NAMING[category_key]):
                    raise ValueError(var + ': incomplete preferred values.')

        def do_float():
            pisa_df[group_var_list] = pisa_df[group_var_list].astype(float)

        def do_int():
            pisa_df[group_var_list] = pisa_df[group_var_list].astype(int)

        def do_str():
            pisa_df[group_var_list] = pisa_df[group_var_list].astype(str)

        pisa_df = user_data['custom_dataframe']

        for target in ['independent_groups', 'dependent_groups']:
            for group in user_data[target].values():
                group_var_list = group['variable_names']
                category_key = group['category']
                if category_key in category_definitions.KNOWN_CATEGORIES:
                    do_know_category()
                elif category_key == "float":
                    do_float()
                elif category_key == "integer":
                    do_int()
                else:
                    do_str()
    # CAUTION:    large sets of variables will reduce the sample size
    # Reason:     each variable has its own set of nulls
    # Solution:   reduce variable sets after finding interactions
    select_columns_and_drop_nulls()
    do_group_categories(user_data)
    apply_preferred_values()
    return user_data


def do_group_categories(user_data):
    """."""
    def get_known_category(pisa_group):
        """
        Fetch and return category associated with group.

        Determine if variables in pisa_group match a known categoy.
        Determine if variables in pisa_group each have same category.
        If consistent category found, return associated category_key.
        Otherwise returns "text_response", indicating group is
        treated as plain text responses rather than categoricals.
        """
        # default to text_response type
        category_key = 'text_response'
        for index, variable_name in enumerate(pisa_group):

            # gather unique values for this variable
            unique_values = set({})
            for unique_val in set(pisa_ref[variable_name].unique()):
                # trailing white spaces occur in the dataset
                if unique_val not in ['nan', np.nan]:
                    unique_values.add(unique_val.strip())

            # check first variable for potential group category will suffice
            if index == 0:
                for known_cat in known_categories:
                    if unique_values.issubset(known_categories[known_cat]):
                        category_key = known_cat
            # if any variable isnt in suspected category, group fails check
            if category_key != 'text_response':
                if not unique_values.issubset(known_categories[category_key]):
                    # how to handle a mismatched group:
                    #     treat as text_response type
                    category_key = 'text_response'
                    break
        return category_key

    def do_group_category():
        """
        Parse groups and convert to numeric type or determine category.

        Get category for each group.
        Set corresponding values for each group.
        Return dictionary containting found group/category key pairs.
        """
        pisa_group = group['variable_names']

        # TODO: Detect and return integer and float types without conversion
        try:
            pisa_ref[pisa_group].astype(int)
            category = "integer"
        except ValueError:
            try:
                pisa_ref[pisa_group].astype(float)
                category = "float"
            except ValueError:
                category = None

        if not category:
            # attempt to match values to known PISA category
            category = get_known_category(pisa_group)

        return category

    known_categories = category_definitions.KNOWN_CATEGORIES
    pisa_ref = user_data['pisa_sample'].copy()
    for target in ['independent_groups', 'dependent_groups']:
        for group_name, group in user_data[target].items():
            user_data[target][group_name]['category'] = do_group_category()

    return user_data
