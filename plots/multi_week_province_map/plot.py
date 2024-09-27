import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from pathlib import Path
from math import ceil
import os

# filepath to provincial shapefile
PROVINCES_SHAPEFILE = './data/geoBoundaries-COD-ADM1-all/'
COUNTRY_BOUNDARY_SHAPEFILE = './data/country-boundary/'
SHAPEFILE_COLUMN = 'shapeISO'
OUTPUT_DIR = './output/'
TMP_DIR = './tmp/'

def plot_multi_week_province_map_matplotlib(geo_data, parameters):
    """
    Plots a provincial-level map using GeoPandas and Matplotlib, creating a 2x2 grid of subplots,
    each corresponding to a different date provided in parameters.
    """
    title = parameters.get('title', '')
    fig_width = parameters.get('fig_width', 10)
    fig_height = parameters.get('fig_height', 10)
    export = parameters.get('export', True)
    filename = parameters.get('filename', 'province_map.pdf')

    # get number of unique dates
    dates = geo_data['date'].unique()

    # create grid of subplots
    num_cols = 2
    num_rows = ceil(len(dates) / num_cols)
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(fig_width, fig_height))
    axs = axs.flatten()

    # load shapefile
    provinces_gdf = gpd.read_file(PROVINCES_SHAPEFILE)
    provinces_gdf = provinces_gdf[[SHAPEFILE_COLUMN, 'geometry']]
    if provinces_gdf.crs != 'EPSG:4326':
        provinces_gdf = provinces_gdf.to_crs('EPSG:4326')

    # create custom color map
    custom_cmap = LinearSegmentedColormap.from_list("red_blue", ['#9db09f', '#a16272', '#9F2241'])

    # loop over dates and plot each map in a subplot
    count_min = 999999999
    for i, date in enumerate(dates):
        # filter geo_data for the specific date
        geo_data_filtered = geo_data[geo_data['date'] == date]

        # merge data with geographic data
        geo_data_merged = provinces_gdf.merge(geo_data_filtered, left_on=SHAPEFILE_COLUMN, right_on='province', how='left')
        # fill NaN values with 0
        geo_data_merged['count'] = geo_data_merged['count'].fillna(0)

        # plot the provinces with 'count' as color
        geo_data_plot = geo_data_merged.plot(column='count', ax=axs[i], legend=False, cmap=custom_cmap)
        # plot transparent polygons as borders
        provinces_gdf.boundary.plot(ax=axs[i], color='white', linewidth=0.3, alpha=0.4)

        # plot country boundary
        gdf_dissolved = gpd.read_file(COUNTRY_BOUNDARY_SHAPEFILE)
        gdf_dissolved.plot(ax=axs[i], color='none', edgecolor='#484848', linewidth=3, alpha=0.8)

        # add title for each panel (use the date as the title)
        axs[i].set_title(f'Date: {date}', fontsize=16)
        axs[i].set_axis_off()

        # update count_min
        count_min = geo_data_merged['count'].min() if geo_data_merged['count'].min() < count_min else count_min

    # set background transparent
    fig.patch.set_alpha(0)

    # tight layout
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    # add a single colorbar for all subplots
    cbar_ax = fig.add_axes([0.88, 0.3, 0.02, 0.4])  # Colorbar axes ([left, bottom, width, height])
    sm = plt.cm.ScalarMappable(cmap=custom_cmap,
                               norm=plt.Normalize(vmin=count_min, vmax=geo_data['count'].max()))
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.ax.tick_params(labelsize=16)

    # set the overall title
    plt.suptitle(title, fontsize=20, y=1.05)

    # generate a unique filename for PNG plot in TMP_DIR
    tmp_png_filename = os.path.join(TMP_DIR, '%d.png' % np.random.randint(1e9))
    while os.path.exists(tmp_png_filename):
        tmp_png_filename = os.path.join(TMP_DIR, '%d.png' % np.random.randint(1e9))
    
    # save plot as PNG in TMP_DIR for display in the HTML report
    plt.savefig(tmp_png_filename, dpi=300)

    # save plot as PDF if export is True
    if export:
        pdf_filename = os.path.join(OUTPUT_DIR, filename)
        counter = 0
        while os.path.exists(pdf_filename):
            counter += 1
            pdf_filename = os.path.join(OUTPUT_DIR, '%s.%d.pdf' % (Path(filename).stem, counter))
        plt.savefig(pdf_filename, format='pdf')

    # close plot to free memory
    plt.close(fig)

    return tmp_png_filename
