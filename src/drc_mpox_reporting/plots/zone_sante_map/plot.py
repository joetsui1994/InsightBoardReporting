import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from pathlib import Path
import io
import base64
import os

# filepath to zone-sante shapefile
REPORT_BASE_FOLDER = Path(__file__).parent.parent.parent
ZONE_SANTE_SHAPEFILE = str(REPORT_BASE_FOLDER / "data" / "rdc_zones-de-sante")
COUNTRY_BOUNDARY_SHAPEFILE = str(REPORT_BASE_FOLDER / "data" / "country-boundary")
SHAPEFILE_COLUMN = "Pcode"
OUTPUT_DIR = str(REPORT_BASE_FOLDER / "output")


def plot_zone_sante_map_matplotlib(geo_data, parameters):
    """
    Plots a zone-sante-level map using GeoPandas and Matplotlib, then saves it as a PNG file.
    """
    title = parameters.get("title", "")
    fig_width = parameters.get("fig_width", 10)
    fig_height = parameters.get("fig_height", 10)
    export = parameters.get("export", True)
    filename = parameters.get("filename", "zone_sante_map.pdf")

    # create figure and axes
    fig, ax = plt.subplots(1, figsize=(fig_width, fig_height))

    # load shapefile
    zone_sante_gdf = gpd.read_file(ZONE_SANTE_SHAPEFILE)
    zone_sante_gdf = zone_sante_gdf[[SHAPEFILE_COLUMN, "geometry"]]
    if zone_sante_gdf.crs != "EPSG:4326":
        zone_sante_gdf = zone_sante_gdf.to_crs("EPSG:4326")

    # merge data with geographic data
    geo_data = zone_sante_gdf.merge(
        geo_data, left_on=SHAPEFILE_COLUMN, right_on="zones_sante", how="left"
    )
    # fill NaN values with 0
    geo_data["count"] = geo_data["count"].fillna(0)

    # create custom colourmap
    custom_cmap = LinearSegmentedColormap.from_list(
        "red_blue", ["#9db09f", "#a16272", "#9F2241"]
    )

    # plot zone-sante with the 'count' column as color
    geo_data_plot = geo_data.plot(column="count", ax=ax, legend=False, cmap=custom_cmap)
    # plot transparent polygons as borders
    zone_sante_gdf.boundary.plot(ax=ax, color="white", linewidth=0.3, alpha=0.4)

    ###########
    gdf_dissolved = gpd.read_file(COUNTRY_BOUNDARY_SHAPEFILE)
    gdf_dissolved.plot(ax=ax, color="none", edgecolor="#484848", linewidth=3, alpha=0.8)

    # add title
    ax.set_axis_off()
    ax.text(
        0.5, -0.1, title, ha="center", va="center", transform=ax.transAxes, fontsize=20
    )

    # adjust colorbar dimensions
    cbar = geo_data_plot.get_figure().colorbar(
        geo_data_plot.collections[0], ax=ax, shrink=0.7, aspect=20
    )
    # Adjust the fontsize of the colorbar tick labels
    cbar.ax.tick_params(labelsize=16)

    # set background transparent
    fig.patch.set_alpha(0)

    # tight layout
    plt.tight_layout()

    # save figure to a BytesIO object
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)  # rewind the buffer to the beginning

    # encode the BytesIO object to base64 string
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # embed the base64 string in an HTML img tag
    fig_html = f'<img src="data:image/png;base64,{img_base64}" alt="zonte-sante-map" />'

    # save plot as PDF if export is True
    if export:
        pdf_filename = os.path.join(OUTPUT_DIR, filename)
        counter = 0
        while os.path.exists(pdf_filename):
            counter += 1
            pdf_filename = os.path.join(
                OUTPUT_DIR, "%s.%d.pdf" % (Path(filename).stem, counter)
            )
        plt.savefig(pdf_filename, format="pdf")

    # close plot to free memory
    plt.close(fig)

    return fig_html
