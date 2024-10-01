import pandas as pd


def preprocess_pyramid_data(data, parameters):
    """
    Preprocesses data for the pyramid plot.
    """
    age_col = parameters.get("age_col")
    age_groups = parameters.get("age_groups")
    sex_col = parameters.get("sex_col")
    deaths_only = parameters.get("deaths_only", False)
    time_col = parameters.get("time_col")
    date_range = parameters.get("date_range_inclusive", {})
    start_date = date_range.get("start_date")
    end_date = date_range.get("end_date")

    # check that time_col is in data
    if time_col not in data.columns:
        raise ValueError(f"Column '{time_col}' not found in data.")

    # filter by date range
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (data[time_col] >= start_date) & (data[time_col] <= end_date)
        data = data.loc[mask]

    # add inf to the last age group
    age_groups.append(float("inf"))

    # filter out non-death data if specified
    if deaths_only:
        data = data[data["status"] == "died"]

    # filter by provinces
    provinces = parameters.get("provinces", {})
    include_provinces = provinces.get("include")
    exclude_provinces = provinces.get("exclude")

    if include_provinces:
        data = data[data["province"].isin(include_provinces)]
    if exclude_provinces:
        data = data[~data["province"].isin(exclude_provinces)]

    # filter by zones_sante
    zones_sante = parameters.get("zones_sante", {})
    include_zones = zones_sante.get("include")
    exclude_zones = zones_sante.get("exclude")

    if include_zones:
        data = data[data["zones_sante"].isin(include_zones)]
    if exclude_zones:
        data = data[~data["zones_sante"].isin(exclude_zones)]

    # filter by aires_sante
    aires_sante = parameters.get("aires_sante", {})
    include_aires = aires_sante.get("include")
    exclude_aires = aires_sante.get("exclude")

    if include_aires:
        data = data[data["aires_sante"].isin(include_aires)]
    if exclude_aires:
        data = data[~data["aires_sante"].isin(exclude_aires)]

    # create a copy of relevant columns
    plot_data = data[[age_col, sex_col]].copy()

    # bin ages into groups
    plot_data[age_col] = plot_data[age_col].apply(
        lambda x: 0 if pd.isnull(x) else int(x)
    )
    plot_data["age_group"] = pd.cut(plot_data[age_col], bins=age_groups, right=False)
    # group by age and sex
    plot_data = (
        plot_data.groupby(["age_group", sex_col])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # make the male counts negative for pyramid plot
    if "male" in plot_data.columns:
        plot_data["male"] = -plot_data["male"]

    return plot_data
