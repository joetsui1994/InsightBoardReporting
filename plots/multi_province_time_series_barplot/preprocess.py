import pandas as pd
from datetime import datetime, timedelta

def preprocess_multi_province_time_series_data(data, parameters):
    """
    Preprocesses data for the time-series bar plot.
    """
    time_col = parameters.get('time_col')
    deaths_only = parameters.get('deaths_only', False)
    aggregate_by_epiweek = parameters.get('aggregate_by_epiweek', False)
    moving_average_window = parameters.get('moving_average_window')

    # check that time_col is in data
    if time_col not in data.columns:
        raise ValueError(f"Column '{time_col}' not found in data.")

    # filter out non-death data if specified
    if deaths_only:
        data = data[data['status'] == 'died']

    # filter by provinces
    provinces = parameters.get('provinces', {})
    include_provinces = provinces.get('include')
    exclude_provinces = provinces.get('exclude')

    if include_provinces:
        data = data[data['province'].isin(include_provinces)]
    if exclude_provinces:
        data = data[~data['province'].isin(exclude_provinces)]

    # filter by zones_sante
    zones_sante = parameters.get('zones_sante', {})
    include_zones = zones_sante.get('include')
    exclude_zones = zones_sante.get('exclude')

    if include_zones:
        data = data[data['zones_sante'].isin(include_zones)]
    if exclude_zones:
        data = data[~data['zones_sante'].isin(exclude_zones)]

    # filter by aires_sante
    aires_sante = parameters.get('aires_sante', {})
    include_aires = aires_sante.get('include')
    exclude_aires = aires_sante.get('exclude')

    if include_aires:
        data = data[data['aires_sante'].isin(include_aires)]
    if exclude_aires:
        data = data[~data['aires_sante'].isin(exclude_aires)]

    # create a copy of relevant column
    plot_data = data.copy()

    # convert time_col to datetime 
    plot_data[time_col] = pd.to_datetime(plot_data[time_col])

    # aggregate by epiweek if specified
    if aggregate_by_epiweek:
        # extract epiweek from the date using the isocalendar() method
        plot_data['year'], plot_data['epiweek'], _ = plot_data[time_col].dt.isocalendar().values.T
        plot_data = plot_data.groupby(['year', 'epiweek', 'province']).size().reset_index(name='count')
        # add start of each epiweek as date
        plot_data['date'] = plot_data.apply(lambda x: datetime.strptime('%d-W%d-1' % (x['year'], x['epiweek']), "%G-W%V-%u") - timedelta(days=1), axis=1)
    else:
        plot_data['date'] = pd.to_datetime(plot_data[time_col]).dt.date
        plot_data = plot_data.groupby(['date', 'province']).size().reset_index(name='count')

    # add 0 count for missing dates
    all_dates = pd.date_range(plot_data['date'].min(), plot_data['date'].max(), freq='D' if not aggregate_by_epiweek else 'W')
    all_dates_df = pd.DataFrame(all_dates.date, columns=['date'])
    all_dates_df['date'] = pd.to_datetime(all_dates_df['date']).dt.date
    # merge
    plot_data['date'] = pd.to_datetime(plot_data['date']).dt.date
    plot_data = all_dates_df.merge(plot_data, how='left', on='date')
    plot_data['count'].fillna(0, inplace=True)
    # sort
    plot_data.sort_values('date', inplace=True)

    # calculate moving average if specified
    effective_window = min(moving_average_window, len(plot_data))
    plot_data['moving_average'] = plot_data['count'].rolling(window=effective_window).mean()

    return plot_data
