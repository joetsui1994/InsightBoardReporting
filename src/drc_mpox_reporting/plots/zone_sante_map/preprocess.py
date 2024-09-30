import pandas as pd


def preprocess_zone_sante_map_data(data, parameters):
    """
    Preprocesses data for the zone-sante map plot.
    """
    time_col = parameters.get("time_col")
    deaths_only = parameters.get("deaths_only", False)
    date_range = parameters.get("date_range_inclusive", {})
    start_date = date_range.get("start_date")
    end_date = date_range.get("end_date")

    # check that time_col is in data
    if time_col not in data.columns:
        raise ValueError(f"Column '{time_col}' not found in data.")

    # filter out non-death data if specified
    if deaths_only:
        data = data[data["status"] == "died"]

    # filter by date range
    if start_date and end_date:
        start_date = (
            pd.to_datetime(start_date) if start_date else pd.to_datetime("1900-01-01")
        )
        end_date = (
            pd.to_datetime(end_date) if end_date else pd.to_datetime("2100-01-01")
        )
        mask = (data[time_col] >= start_date) & (data[time_col] <= end_date)
        data = data.loc[mask]

    # aggregate data at zone-sante level
    zone_sante_cases = data.groupby("zones_sante").size().reset_index(name="count")

    return zone_sante_cases
