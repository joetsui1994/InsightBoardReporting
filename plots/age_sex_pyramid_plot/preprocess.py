import pandas as pd

def preprocess_pyramid_data(data, parameters):
    """
    Preprocesses data for the pyramid plot.
    """
    age_col = parameters.get('age_col')
    age_groups = parameters.get('age_groups')
    sex_col = parameters.get('sex_col')

    # add inf to the last age group
    age_groups.append(float('inf'))

    # create a copy of relevant columns
    plot_data = data[[age_col, sex_col]].copy()

    # bin ages into groups
    plot_data[age_col] = plot_data[age_col].apply(lambda x: 0 if pd.isnull(x) else int(x))
    plot_data['age_group'] = pd.cut(plot_data[age_col], bins=age_groups, right=False)
    # group by age and sex
    plot_data = plot_data.groupby(['age_group', sex_col]).size().unstack(fill_value=0).reset_index()

    # make the male counts negative for pyramid plot
    if 'male' in plot_data.columns:
        plot_data['male'] = -plot_data['male']

    return plot_data