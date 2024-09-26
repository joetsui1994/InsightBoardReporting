import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import os

# filepath to provincial shapefile
PROVINCES_SHAPEFILE = './data/geoBoundaries-COD-ADM1-all/'
DISSOLVED_PROVINCES_SHAPEFILE = './data/geoBoundaries-COD-ADM1-all_dissolved/'
SHAPEFILE_COLUMN = 'shapeISO'
OUTPUT_DIR = './output/'

def plot_province_map_matplotlib(geo_data, parameters):
    """
    Plots a provincial-level map using GeoPandas and Matplotlib, then saves it as a PNG file.
    """
    title = parameters.get('title', '')
    fig_width = parameters.get('fig_width', 10)
    fig_height = parameters.get('fig_height', 10)
    png_dpi = parameters.get('png_dpi', 300)

    # create figure and axes
    fig, ax = plt.subplots(1, figsize=(fig_width, fig_height))

    # load shapefile
    provinces_gdf = gpd.read_file(PROVINCES_SHAPEFILE)
    provinces_gdf = provinces_gdf[[SHAPEFILE_COLUMN, 'geometry']]
    if provinces_gdf.crs != 'EPSG:4326':
        provinces_gdf = provinces_gdf.to_crs('EPSG:4326')

    # merge data with geographic data
    geo_data = provinces_gdf.merge(geo_data, left_on=SHAPEFILE_COLUMN, right_on='province', how='left')

    # create custom colourmap
    custom_cmap = LinearSegmentedColormap.from_list("red_blue", ['#c9c9c9', '#a16272', '#9F2241'])

    # plot provinces with the 'count' column as color
    geo_data_plot = geo_data.plot(column='count', ax=ax, legend=False, cmap=custom_cmap)
    # plot transparent polygons as borders
    provinces_gdf.boundary.plot(ax=ax, color='white', linewidth=0.3, alpha=0.4)

    ###########
    gdf_dissolved = gpd.read_file(DISSOLVED_PROVINCES_SHAPEFILE)
    gdf_dissolved.plot(ax=ax, color='none', edgecolor='#484848', linewidth=3, alpha=0.8)

    # add title
    ax.set_axis_off()
    ax.text(0.5, -0.1, title, ha='center', va='center', transform=ax.transAxes, fontsize=20)

    # adjust colorbar dimensions
    cbar = geo_data_plot.get_figure().colorbar(geo_data_plot.collections[0], ax=ax, shrink=0.7, aspect=20)
    # Adjust the fontsize of the colorbar tick labels
    cbar.ax.tick_params(labelsize=16)

    # set background transparent
    fig.patch.set_alpha(0)

    # tight layout
    plt.tight_layout()

    # generate a unique filename for the plot in the output directory
    png_filename = os.path.join(OUTPUT_DIR, 'province_map.png')
    counter = 0
    while os.path.exists(png_filename):
        counter += 1
        png_filename = os.path.join(OUTPUT_DIR, f'province_map_{counter}.png')

    # save plot as PNG
    plt.savefig(png_filename, dpi=png_dpi)
    # save plot as PDF
    plt.savefig(png_filename.replace('.png', '.pdf'))

    # close plot to free memory
    plt.close(fig)

    return png_filename
