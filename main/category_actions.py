"""Functions specific to group types."""


# =============================================================================
# GROUP_POST_WRANGLE FUNCTIONS
# =============================================================================
# handle independent and dependent variables seperately


# float
def float_post_wrangle(group_name, user_data):
    """
    Apply float group operations.

        - create mean value column
    """
    pisa_df = user_data['custom_dataframe']
    independent_groups = user_data['independent_groups']
    dependent_groups = user_data['dependent_groups']

    def create_mean(name, grp):
        pisa_df[name + '_mean'] = pisa_df[grp].transpose(
            ).mean().astype(float)

    # handle dependent and independent variable groups seperately
    if group_name in independent_groups:
        if len(independent_groups[group_name]) > 1:
            create_mean(group_name, independent_groups[group_name])
    elif group_name in dependent_groups:
        if len(dependent_groups[group_name]) > 1:
            create_mean(group_name, dependent_groups[group_name])


# binary_yn
def binary_yn1_post_wrangle(group_name, user_data):
    """
    Apply binary_yn group operations.

        - create total column for binary group given
    """
    pisa_df = user_data['custom_dataframe']
    independent_groups = user_data['independent_groups']
    dependent_groups = user_data['dependent_groups']

    def create_count(name, grp):
        pisa_df[name + '_count'] = pisa_df[grp].transpose().sum().astype(int)

    # handle dependent and independent variable groups seperately
    if len(independent_groups[group_name]) > 1:
        if group_name in independent_groups:
            create_count(group_name, independent_groups[group_name])
        elif group_name in dependent_groups:
            create_count(group_name, dependent_groups[group_name])