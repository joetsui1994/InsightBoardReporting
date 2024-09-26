import pandas as pd

def preprocess_data(data, config):
    """
    Preprocesses the data according to configuration.
    """
    reporting = config.get('reporting', {})
    use_date = reporting.get('use_date', 'date_notification')
    data_range = reporting.get('data_range_inclusive', {})
    start_date = data_range.get('start_date')
    end_date = data_range.get('end_date')

    # check that use_date column is in datetime format
    if use_date in data.columns:
        data[use_date] = pd.to_datetime(data[use_date])
    else:
        raise KeyError("Data does not contain a 'date' column.")

    # filter by date range
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (data[use_date] >= start_date) & (data[use_date] <= end_date)
        data = data.loc[mask]

    # filter by provinces
    provinces = reporting.get('provinces', {})
    include_provinces = provinces.get('include')
    exclude_provinces = provinces.get('exclude')

    if include_provinces:
        data = data[data['province'].isin(include_provinces)]
    if exclude_provinces:
        data = data[~data['province'].isin(exclude_provinces)]

    # filter by zones_sante
    zones_sante = reporting.get('zones_sante', {})
    include_zones = zones_sante.get('include')
    exclude_zones = zones_sante.get('exclude')

    if include_zones:
        data = data[data['zones_sante'].isin(include_zones)]
    if exclude_zones:
        data = data[~data['zones_sante'].isin(exclude_zones)]

    # filter by aires_sante
    aires_sante = reporting.get('aires_sante', {})
    include_aires = aires_sante.get('include')
    exclude_aires = aires_sante.get('exclude')

    if include_aires:
        data = data[data['aires_sante'].isin(include_aires)]
    if exclude_aires:
        data = data[~data['aires_sante'].isin(exclude_aires)]

    return data
