import pandas as pd

def preprocess_time_series_data(data, parameters):
    """
    Preprocesses data for the time-series bar plot.
    """
    time_col = parameters.get('time_col')
    moving_average_window = parameters.get('moving_average_window', 1)

    # validate moving_average_window
    try:
        moving_average_window = int(moving_average_window)
        if moving_average_window < 1:
            print(f"Invalid moving_average_window '{moving_average_window}'. Defaulting to 1.")
            moving_average_window = 1
    except (ValueError, TypeError):
        print(f"Invalid moving_average_window '{moving_average_window}'. Defaulting to 1.")
        moving_average_window = 1

    # check that time_col is in data
    if time_col not in data.columns:
        raise ValueError(f"Column '{time_col}' not found in data.")

    # create a copy of relevant column
    plot_data = data[[time_col]].copy()

    # convert time_col to datetime and extract date
    try:
        plot_data['date'] = pd.to_datetime(plot_data[time_col]).dt.date
    except Exception as e:
        raise ValueError(f"Error converting '{time_col}' to datetime: {e}")
    plot_data = plot_data.groupby('date').size().reset_index(name='count')

    # add 0 count for missing dates
    all_dates = pd.date_range(plot_data['date'].min(), plot_data['date'].max(), freq='D')
    all_dates = all_dates.date
    all_dates_df = pd.DataFrame(all_dates, columns=['date'])
    # merge
    plot_data = all_dates_df.merge(plot_data, how='left', on='date')
    plot_data['count'].fillna(0, inplace=True)
    # sort
    plot_data.sort_values('date', inplace=True)

    # calculate moving average if specified
    effective_window = min(moving_average_window, len(plot_data))
    plot_data['moving_average'] = plot_data['count'].rolling(window=effective_window).mean()

    return plot_data
