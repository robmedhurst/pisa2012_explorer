"""
Wrangling functions for pisa2012_explorer project.

This tool aims to aid in the exploration of the PISA 2012 dataset,
allowing users to concurrently examine a group of similar variables.
"""

import category_definitions


# =============================================================================
# Wrangling Functions
# =============================================================================

def wrangle(user_data):
    """Wrap functions for wrangling. Return edited inputs."""
    known_categories = category_definitions.KNOWN_CATEGORIES
    preferred_naming = category_definitions.PREFERRED_NAMING

    pisa_df = user_data['pisa_sample'].copy()
    independent_groups = user_data['independent_groups']
    dependent_groups = user_data['dependent_groups']

    def select_columns_and_drop_nulls():
        """
        Discard unspecified columns and remove rows with Null values.

        Remove columns from that are not in any given groups.
        Remove observations containing nulls.
        """
        # drop unused columns
        pisa_df.drop(pisa_df.columns.difference(
            [var_name for sublist in list(independent_groups.values())
             for var_name in sublist] +
            [var_name for sublist in list(dependent_groups.values())
             for var_name in sublist]),
                     axis='columns', inplace=True)
        # drop nulls
        pisa_df.dropna(inplace=True)

    def get_category(pisa_group):
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
            for unique_val in set(pisa_df[variable_name].unique()):
                # trailing white spaces do occur in the dataset
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

    def apply_preferred_values(pisa_group, category_key):
        """
        Apply preferred values to groups of known category.

        Update strings to preferred values (ex: "Yes" == True) or
        raise ValueError if incomplete preferred values found.
        """
        # ignore numerical and text_response types
        if category_key in known_categories:
            # update to corresponding preferred values
            for var in pisa_group:

                # strip white space to match know_categories
                pisa_df[var] = pisa_df[var].map(lambda x: x.strip())

                # replace each known value
                for known, preferred in zip(
                        known_categories[category_key],
                        preferred_naming[category_key]):
                    pisa_df.loc[pisa_df[var] == known, var] = preferred

                # confirm values are from preferred_naming, none overlooked
                if not set(pisa_df[var].unique()).issubset(
                        preferred_naming[category_key]):
                    raise ValueError(var + ': incomplete preferred values.')

    def process_pisa_set_of_groups(pisa_set_of_groups):
        """
        Parse groups and convert to numeric type or determine category.

        Get category for each group.
        Set corresponding values for each group.
        Return dictionary containting found group/category key pairs.
        """
        matches = {}
        for group_name in pisa_set_of_groups:

            pisa_group = pisa_set_of_groups[group_name]
            # attempt to convert group to numeric

            try:
                pisa_df[pisa_group] = pisa_df[pisa_group].astype(int)
                category = "integer"

            except ValueError:
                try:
                    pisa_df[pisa_group] = pisa_df[pisa_group].astype(float)
                    category = "float"
                except ValueError:
                    category = None

            if not category:
                pisa_df[pisa_group] = pisa_df[pisa_group].astype(str)
                # attempt to match and update values to known PISA category
                category = get_category(pisa_group)
                apply_preferred_values(pisa_group, category)

            matches[group_name] = category
        return matches

    # CAUTION:    large sets of variables will reduce the sample size
    # Reason:     each variable has its own set of nulls
    # Solution:   reduce variable sets after finding interactions
    select_columns_and_drop_nulls()

    # group_category_matches = process_pisa_set_of_groups(
    #     {**independent_groups, **dependent_groups})

    # independent_groups_keys = process_pisa_set_of_groups(independent_groups)
    group_category_matches = {
        'independent_groups': process_pisa_set_of_groups(independent_groups),
        'dependent_groups': process_pisa_set_of_groups(dependent_groups)}

    # update and return user_data
    user_data['custom_dataframe'] = pisa_df
    user_data['group_category_matches'] = group_category_matches
    return user_data