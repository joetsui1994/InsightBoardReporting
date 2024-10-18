import io
import os
import base64
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.colors import LinearSegmentedColormap

from modules.data_filtering import apply_filters
from plotting_modules.add_tabs import generate_tabbed_html


def preprocess(data, config):
    """
    Preprocesses data for the spatial-map plot.
    """
    filtering_config = config.get("filtering", [])
    loc_column = config.get("loc_column")
    aggregation_config = config.get("aggregation", {})

    # apply filters
    filtered_data = apply_filters(data, filtering_config)
    # return empty dataframe if no data left after filtering
    if filtered_data.empty:
        return pd.DataFrame()

    # create a copy of relevant column
    plot_data = filtered_data.copy()

    # check that loc_column is in data
    if loc_column not in plot_data.columns:
        raise ValueError(f"Column '{loc_column}' not found in data.")

    # if aggregation is not specified, then group by loc_column
    aggregate_by_epiweek = aggregation_config.get("by_epiweek", False)
    if not aggregate_by_epiweek:
        plot_data = plot_data.groupby(loc_column).size().reset_index(name="count")
        # add dummy date column
        plot_data["date"] = datetime.strptime("2020-01-01", "%Y-%m-%d")
    else:  # aggregate by epiweek
        # get the time column
        time_column = aggregation_config.get("time_column")
        # check that time_column is in data
        if time_column not in plot_data.columns:
            raise ValueError(f"Column '{time_column}' not found in data.")

        # convert time_col to datetime
        plot_data[time_column] = pd.to_datetime(plot_data[time_column])

        # extract epiweek from the date using the isocalendar() method
        plot_data["year"], plot_data["epiweek"], _ = (
            plot_data[time_column].dt.isocalendar().values.T
        )
        plot_data = (
            plot_data.groupby(["year", "epiweek", loc_column])
            .size()
            .reset_index(name="count")
        )

        # add start of each epiweek as date
        plot_data["date"] = plot_data.apply(
            lambda x: datetime.strptime(
                "%d-W%d-1" % (x["year"], x["epiweek"]), "%G-W%V-%u"
            )
            - timedelta(days=1),
            axis=1,
        )

        # add 0 count for missing dates
        all_dates = pd.date_range(
            plot_data["date"].min(), plot_data["date"].max(), freq="W"
        )
        all_dates_df = pd.DataFrame(all_dates.date, columns=["date"])
        all_dates_df["date"] = pd.to_datetime(all_dates_df["date"]).dt.date
        # merge
        plot_data["date"] = pd.to_datetime(plot_data["date"]).dt.date
        plot_data = all_dates_df.merge(plot_data, how="left", on="date")
        plot_data["count"] = plot_data["count"].fillna(0)
        # sort
        plot_data.sort_values("date", inplace=True)

    # rename loc_column to 'loc_column'
    plot_data.rename(columns={loc_column: "loc_column"}, inplace=True)

    return plot_data


def plot(plot_data, config, out_dir):
    if len(plot_data) == 0:
        return "<p>No data available for the selected filters.</p>"

    # extract config parameters
    shapefile = config.get("shapefile")
    id_column = config.get("id_column")
    boundary_shapefile = config.get("boundary_shapefile")
    title = config.get("title")
    fig_width = config.get("fig_width", 10)
    fig_height = config.get("fig_height", 10)
    export = config.get("export", True)
    filestem = config.get("filestem", "spatial-map")

    # load shapefile
    gdf = gpd.read_file(shapefile)
    gdf = gdf[[id_column, "geometry"]]
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    # load shapefile for country boundary if specified
    if boundary_shapefile:
        gdf_boundary = gpd.read_file(boundary_shapefile)

    # create custom color map
    custom_cmap = LinearSegmentedColormap.from_list(
        "red_blue", ["#9db09f", "#a16272", "#9F2241"]
    )

    # get unique dates
    dates = plot_data["date"].unique()
    # create list to store figs
    figs_html = []
    # iterate over dates and plot each map
    for date in dates:
        # filter data for the specific date
        date_data = plot_data[plot_data["date"] == date]

        # merge data with geographic data
        geo_data = gdf.merge(
            date_data, left_on=id_column, right_on="loc_column", how="left"
        )

        # fill NaN values with 0
        geo_data["count"] = geo_data["count"].fillna(0)

        # plot map
        fig, ax = plt.subplots(1, figsize=(fig_width, fig_height))
        geo_data_plot = geo_data.plot(
            column="count", ax=ax, legend=False, cmap=custom_cmap
        )

        # plot transparent polygons as borders
        gdf.boundary.plot(color="white", linewidth=0.3, alpha=0.4)

        # plot country boundary if specified
        if boundary_shapefile:
            gdf_boundary.plot(
                color="none", ax=ax, edgecolor="#484848", linewidth=3, alpha=0.8
            )

        # add title (use date as title if len(dates) > 1)
        ax.set_axis_off()
        ax.text(
            0.5,
            -0.1,
            title if len(dates) == 1 else f"Date: {date}",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=20,
        )

        # adjust margin
        fig.subplots_adjust(left=0.05, right=0.95, top=1, bottom=0)

        # adjust colorbar dimensions
        cbar = geo_data_plot.get_figure().colorbar(
            geo_data_plot.collections[0], ax=ax, shrink=0.7, aspect=20
        )
        # adjust the fontsize of the colorbar tick labels
        cbar.ax.tick_params(labelsize=16)

        # set background transparent
        fig.patch.set_alpha(0)

        # tight layout
        plt.tight_layout()

        # encode plot as base64
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)  # rewind the buffer to the beginning

        # encode the BytesIO object to base64 string
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        img_base64_url = f"data:image/png;base64,{img_base64}"

        # create a download link for the image
        download_link = f'<a href="{img_base64_url}" class="download-link" download="{filestem}_{date}.png">Download Figure (.png)</a>'

        # embed the base64 string in an HTML img tag
        fig_html = f"""
            <div>
                <img src="{img_base64_url}" alt="figure" />
                {download_link}
            </div>
        """

        # save plot as PDF if export is True
        if export:
            pdf_filename = os.path.join(out_dir, f"{filestem}_{date}.pdf")
            counter = 0
            while os.path.exists(pdf_filename):
                counter += 1
                pdf_filename = os.path.join(out_dir, f"{filestem}_{date}.{counter}.pdf")

            # save plot as PDF
            plt.gcf().set_size_inches(fig_width, fig_height)
            plt.savefig(pdf_filename, format="pdf", bbox_inches="tight")

        figs_html.append((fig_html, str(date)))

    # if multiple dates, return tabbed display
    if len(dates) > 1:
        return generate_tabbed_html(filestem, figs_html)
    else:
        return figs_html[0][0]
