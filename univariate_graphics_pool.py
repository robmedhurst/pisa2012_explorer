"""Functions with verbose names to be caught by keyword."""
import univariate_graphics_support as u


def float_horizontalcomparison_distribution(parameters, pisa_df, inputs):
    """Return a subplot of distributions for float type varibles."""
    return u.float_horizontal_frequency(parameters, pisa_df, inputs, kde=0)


def float_horizontalcomparison_frequency_kde(parameters, pisa_df, inputs):
    """Return a subplot of frequencies with kde for float type varibles."""
    return u.float_horizontal_frequency(parameters, pisa_df, inputs, kde=1)
