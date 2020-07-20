# handle independent and dependent variables seperately

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
    pass

### binary_yn
def binary_yn_group_post_wrangle(group_name, pisa_df, inputs):
    """
    apply binary_yn group operations:
        - create total column for binary group given
    """
    independent_groups, dependent_groups = inputs[2:4]

    def apply_count(nm, grp):
        pisa_df[nm + 'Count'] = pisa_df[grp].transpose().sum().astype(int)

    if group_name in independent_groups:
        apply_count(group_name, independent_groups[group_name])
    elif group_name in dependent_groups:
        apply_count(group_name, dependent_groups[group_name])

### work_status
def work_status_group_post_wrangle(group_name, pisa_df, inputs):
    """
    apply work_status group operations:
        - None
    """
    pass
