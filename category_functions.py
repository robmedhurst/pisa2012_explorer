# handle independent and dependent variables seperately
 
### text_response
def text_response_group_post_wrangle(group_name, pisa_df, inputs):
    """
    apply text only group operations:
    """
    pass

### integer
def integer_group_post_wrangle(group_name, pisa_df, inputs):
    """
    apply integer group operations:
        - None
    """
    pass

### float
def float_group_post_wrangle(group_name, pisa_df, inputs):
    """
    apply float group operations:
        - create mean value column
    """
    independent_groups, dependent_groups = inputs[2:4]
    def create_mean(nm, grp):
        pisa_df[nm + '_mean'] = pisa_df[grp].transpose().mean().astype(float)

    # handle dependent and independent variable groups seperately
    if group_name in independent_groups:
        if len(independent_groups[group_name]) > 1:
            create_mean(group_name, independent_groups[group_name])
    elif group_name in dependent_groups:
        if len(dependent_groups[group_name]) > 1:
            create_mean(group_name, dependent_groups[group_name])

### binary_yn
def binary_yn_group_post_wrangle(group_name, pisa_df, inputs):
    """
    apply binary_yn group operations:
        - create total column for binary group given
    """
    independent_groups, dependent_groups = inputs[2:4]
    def create_count(nm, grp):
        pisa_df[nm + '_count'] = pisa_df[grp].transpose().sum().astype(int)

    # handle dependent and independent variable groups seperately
    if group_name in independent_groups:
        create_count(group_name, independent_groups[group_name])
    elif group_name in dependent_groups:
        create_count(group_name, dependent_groups[group_name])
