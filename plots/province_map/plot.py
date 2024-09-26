import plotly.express as px
import geopandas as gpd
import json
import os

# filepath to provincial shapefile
PROVINCES_SHAPEFILE = './data/geoBoundaries-COD-ADM1-all/'
SHAPEFILE_COLUMN = 'shapeISO'

def plot_province_map(geo_data, parameters):
    """
    Creates a provincial-level map using preprocessed geospatial data.
    """
    legend = parameters.get('legend', True)
    mask_missing_tiles = parameters.get('mask_missing_tiles', True)
    title = parameters.get('title', '')
    caption = parameters.get('caption', '')

    # load shapefile
    provinces_gdf = gpd.read_file(PROVINCES_SHAPEFILE)
    # provinces_gdf = provinces_gdf[[SHAPEFILE_COLUMN, 'geometry']]
    if provinces_gdf.crs != 'EPSG:4326':
        provinces_gdf = provinces_gdf.to_crs('EPSG:4326')

    # merge data with geographic data
    geo_data = provinces_gdf.merge(geo_data, left_on=SHAPEFILE_COLUMN, right_on='province', how='left')

    # fill missing values
    geo_data['count'].fillna(0, inplace=True)

    # read GeoJSON
    geo_data_json = json.loads(geo_data.to_json())

    # create map
    fig = px.choropleth(
        geo_data,
        geojson=geo_data_json,
        locations=SHAPEFILE_COLUMN,
        color='count',
        hover_name=SHAPEFILE_COLUMN,
        color_continuous_scale="OrRd",
        range_color=(0, geo_data['count'].max()),
        labels={ 'count': 'Number of Cases' },
        title=title
    )

    # adjust layout
    fig.update_geos(
        visible=False,
        resolution=50,
        showcountries=True,
        lataxis_range=[-13.5, 5],  # Latitude range for the DRC
        lonaxis_range=[12, 32],    # Longitude range for the DRC
    )

    # add caption if provided
    if caption:
        fig.add_annotation(
            text=caption,
            xref="paper",
            yref="paper",
            x=0,
            y=-0.1,
            showarrow=False,
            font=dict(size=12)
        )
    # fig.show()

    return fig
