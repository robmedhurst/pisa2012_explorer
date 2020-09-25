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

    def create_mean(variable_names):
        pisa_df[group_name + '_mean'] = pisa_df[variable_names].transpose(
            ).mean().astype(float)

    # handle dependent and independent variable groups seperately
    if group_name in independent_groups:
        variable_names = independent_groups[group_name]['variable_names']
    elif group_name in dependent_groups:
        variable_names = dependent_groups[group_name]['variable_names']

    if len(variable_names) > 1:
        create_mean(variable_names)


# binary_yn
def binary_yn1_post_wrangle(group_name, user_data):
    """
    Apply binary_yn group operations.

        - create total column for binary group given
    """
    pisa_df = user_data['custom_dataframe']
    independent_groups = user_data['independent_groups']
    dependent_groups = user_data['dependent_groups']

    def create_count(variables):
        pisa_df[group_name + '_count'] = pisa_df[variables].transpose(
            ).sum().astype(int)

    # handle dependent and independent variable groups seperately
    if len(independent_groups[group_name]['variable_names']) > 1:

        if group_name in independent_groups:
            create_count(independent_groups[group_name]['variable_names'])
        elif group_name in dependent_groups:
            create_count(dependent_groups[group_name]['variable_names'])
