import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os

from modules.data_filtering import apply_filters
from plotting_modules.add_tabs import generate_tabbed_html


def preprocess(data, config):
    """
    Preprocesses data for the time-series bar plot.
    """
    filtering_config = config.get("filtering", [])
    time_column = config.get("time_column")
    by_epiweek = config.get("by_epiweek", False)
    moving_average_window = config.get("moving_average_window", None)
    group_by = config.get("group_by", None)
    group_by_age_config = config.get("group_by_age", {})

    # apply filters
    filtered_data = apply_filters(data, filtering_config)
    # return empty dataframe if no data left after filtering
    if filtered_data.empty:
        return pd.DataFrame()

    # create a copy of relevant column
    plot_data = filtered_data.copy()

    # check that time_column is in data
    if time_column not in plot_data.columns:
        raise ValueError(f"Column '{time_column}' not found in data.")
    
    # first check if group_by_age is active
    if group_by_age_config.get("active", False):
        age_column = group_by_age_config.get("age_column", "age")
        age_groups = group_by_age_config.get("age_groups", [0, 18, 45, 65])

        # check that age_column is in data
        if age_column not in plot_data.columns:
            raise ValueError(f"Column '{age_column}' not found in data.")
        
        # add inf to the last age group
        age_groups.append(float("inf"))

        # create age bins
        plot_data[age_column] = plot_data[age_column].apply(
            lambda x: 0 if pd.isnull(x) else int(x)
        )
        plot_data["age_group"] = pd.cut(plot_data[age_column], bins=age_groups, right=False)
        group_by = "age_group"

        # rename age_group to human readable format
        plot_data["age_group"] = plot_data["age_group"].apply(
            lambda x: "%d-%d" % (int(x.left), int(x.right)) if x.right != float("inf") else f"{int(x.left)}+"
        )

    # check also group_by column
    if group_by and group_by not in plot_data.columns:
        raise ValueError(f"Column '{group_by}' not found in data.")
    elif group_by is None: # add a dummy column
        plot_data["group"] = 0
    else: # rename group_by column to group
        plot_data.rename(columns={group_by: "group"}, inplace=True)

    # convert time_col to datetime
    plot_data[time_column] = pd.to_datetime(plot_data[time_column])

    # aggregate by epiweek if specified
    if by_epiweek:
        # extract epiweek from the date using the isocalendar() method
        plot_data["year"], plot_data["epiweek"], _ = (
            plot_data[time_column].dt.isocalendar().values.T
        )
        plot_data = (
            plot_data.groupby(["year", "epiweek", "group"], observed=False).size().reset_index(name="count")
        )
        # add start of each epiweek as date
        plot_data["date"] = plot_data.apply(
            lambda x: datetime.strptime(
                "%d-W%d-1" % (x["year"], x["epiweek"]), "%G-W%V-%u"
            ) - timedelta(days=1),
            axis=1,
        )
    else:
        plot_data["date"] = pd.to_datetime(plot_data[time_column]).dt.date
        plot_data = plot_data.groupby(["date", "group"], observed=False).size().reset_index(name="count")

    # add 0 count for missing dates
    all_dates = pd.date_range(
        plot_data["date"].min(),
        plot_data["date"].max(),
        freq="D" if not by_epiweek else "W",
    )

    # create combinations of all dates and unique groups
    unique_groups = plot_data["group"].unique()
    all_dates_df = pd.DataFrame(
        [(d, g) for d in all_dates.date for g in unique_groups], 
        columns=["date", "group"]
    )
    
    all_dates_df["date"] = pd.to_datetime(all_dates_df["date"]).dt.date
    
    # merge
    plot_data["date"] = pd.to_datetime(plot_data["date"]).dt.date
    plot_data = all_dates_df.merge(plot_data, how="left", on=["date", "group"])
    plot_data["count"] = plot_data["count"].fillna(0)
    # sort
    plot_data.sort_values(by=["date", "group"], inplace=True)

    # calculate moving average if specified
    if moving_average_window:
        plot_data["moving_average"] = plot_data.groupby("group")["count"].transform(
            lambda x: x.rolling(window=moving_average_window, min_periods=1).mean()
        )

    return plot_data


def plot(plot_data, config, out_dir):
    """
    Creates a time-series bar plot using preprocessed data.
    If group_by exists in config, create tabbed display.
    """
    # extract plot parameters
    x_label = config.get("x_label", "Time")
    y_label = config.get("y_label", "Count")
    title = config.get("title", "Plot Title")
    fig_width = config.get("fig_width", 300)
    fig_height = config.get("fig_height", 500)
    export = config.get("export", True)
    filestem = config.get("filestem", "time_series_barplot")

    # extract parameters for moving average
    ma_params = config.get("moving_average", {})
    ma_show = ma_params.get("show", False)
    ma_lw = ma_params.get("linewidth", 2)
    ma_colour = ma_params.get("colour", "#B4A269")

    # if no data, return html that says so
    if plot_data.empty:
        return "<h4>%s (no data available)</h4>" % title

    # get unique groups
    groups = plot_data["group"].unique()
    # create list to store figs
    figs_html = []
    # loop through groups and create plots
    for group in groups:
        group_data = plot_data[plot_data["group"] == group]

        # create plot
        fig = px.bar(
            group_data,
            x="date",
            y="count",
            labels={"date": x_label, "count": y_label},
            title=title,
            color_discrete_sequence=["#1A5632"],
            opacity=0.9,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(200,200,200,0.5)"),
            yaxis=dict(gridcolor="rgba(200,200,200,0.5)"),
            margin=dict(l=60, r=20, b=60, t=50), autosize=True
        )

        # add a moving average line if specified
        if ma_show:
            fig.add_trace(
                go.Scatter(
                    x=group_data["date"],
                    y=group_data["moving_average"],
                    mode="lines",
                    name="Moving Average",
                    line=dict(color=ma_colour, width=ma_lw),
                )
            )

        # convert figure to HTML string
        fig_html = fig.to_html(full_html=False, include_plotlyjs=False)
        fig_html = fig_html.replace('<div ', '<div class="plotly-graph-div" ')
        figs_html.append((fig_html, str(group)))

        # export plot if specified
        if export:
            pdf_filename = os.path.join(out_dir, f"{filestem}_{group}.pdf")
            counter = 0
            while os.path.exists(pdf_filename):
                counter += 1
                pdf_filename = os.path.join(
                    out_dir, f"{filestem}_{group}.{counter}.pdf"
                )

            # create layout object
            fig.write_image(pdf_filename, format="pdf", width=fig_width, height=fig_height)

    # if multiple groups, return tabbed display
    if len(groups) > 1:
        return generate_tabbed_html(filestem, figs_html)
    else:
        return figs_html[0][0]
    