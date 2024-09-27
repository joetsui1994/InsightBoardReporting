import pandas as pd
from datetime import datetime, timedelta

def preprocess_multi_week_province_map_data(data, parameters):
    """
    Preprocesses data for the province map plot.
    """
    time_col = parameters.get('time_col')
    deaths_only = parameters.get('deaths_only', False)
    weeks = parameters.get('weeks', [])
    
    # check that time_col is in data
    if time_col not in data.columns:
        raise ValueError(f"Column '{time_col}' not found in data.")

    # filter out non-death data if specified
    if deaths_only:
        data = data[data['status'] == 'died']

    # create a copy of relevant column
    plot_data = data.copy()

    # convert time_col to datetime 
    plot_data[time_col] = pd.to_datetime(plot_data[time_col])

    # aggregate by epiweek
    # extract epiweek from the date using the isocalendar() method
    plot_data['year'], plot_data['epiweek'], _ = plot_data[time_col].dt.isocalendar().values.T
    plot_data = plot_data.groupby(['year', 'epiweek', 'province']).size().reset_index(name='count')
    # add start of each epiweek as date
    plot_data['date'] = plot_data.apply(lambda x: datetime.strptime('%d-W%d-1' % (x['year'], x['epiweek']), "%G-W%V-%u") - timedelta(days=1), axis=1)

    # add 0 count for missing dates
    all_dates = pd.date_range(plot_data['date'].min(), plot_data['date'].max(), freq='W')
    all_dates_df = pd.DataFrame(all_dates.date, columns=['date'])
    all_dates_df['date'] = pd.to_datetime(all_dates_df['date']).dt.date
    # merge
    plot_data['date'] = pd.to_datetime(plot_data['date']).dt.date
    plot_data = all_dates_df.merge(plot_data, how='left', on='date')
    plot_data['count'].fillna(0, inplace=True)
    # sort
    plot_data.sort_values('date', inplace=True)

    # filter by weeks provided
    plot_data = plot_data[plot_data['date'].isin(pd.to_datetime(weeks).date)]

    # aggregate data at provincial level
    province_cases = plot_data.groupby(['province', 'date']).size().reset_index(name='count')

    return province_cases