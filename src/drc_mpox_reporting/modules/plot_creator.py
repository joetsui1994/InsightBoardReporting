import os
import base64
from drc_mpox_reporting.plots.time_series_barplot.preprocess import (
    preprocess_time_series_data,
)
from drc_mpox_reporting.plots.time_series_barplot.plot import plot_time_series_barplot
from drc_mpox_reporting.plots.province_map.preprocess import (
    preprocess_province_map_data,
)
from drc_mpox_reporting.plots.province_map.plot import plot_province_map_matplotlib
from drc_mpox_reporting.plots.age_sex_pyramid_plot.preprocess import (
    preprocess_pyramid_data,
)
from drc_mpox_reporting.plots.age_sex_pyramid_plot.plot import plot_pyramid
from drc_mpox_reporting.plots.zone_sante_map.preprocess import (
    preprocess_zone_sante_map_data,
)
from drc_mpox_reporting.plots.zone_sante_map.plot import plot_zone_sante_map_matplotlib
from drc_mpox_reporting.plots.multi_province_time_series_barplot.preprocess import (
    preprocess_multi_province_time_series_data,
)
from drc_mpox_reporting.plots.multi_province_time_series_barplot.plot import (
    plot_multi_province_time_series_barplot,
)
from drc_mpox_reporting.plots.multi_province_age_sex_pyramid_plot.preprocess import (
    preprocess_multi_province_pyramid_data,
)
from drc_mpox_reporting.plots.multi_province_age_sex_pyramid_plot.plot import (
    plot_multi_province_pyramid,
)
from drc_mpox_reporting.plots.multi_week_province_map.preprocess import (
    preprocess_multi_week_province_map_data,
)
from drc_mpox_reporting.plots.multi_week_province_map.plot import (
    plot_multi_week_province_map_matplotlib,
)
from drc_mpox_reporting.plots.multi_week_zone_sante_map.preprocess import (
    preprocess_multi_week_zone_sante_map_data,
)
from drc_mpox_reporting.plots.multi_week_zone_sante_map.plot import (
    plot_multi_week_zone_sante_map_matplotlib,
)


def create_plot(data, graph_config):
    plot_type = graph_config["type"]
    parameters = graph_config.get("parameters", {})

    plot_functions = {
        "time-series-barplot": {
            "preprocess": preprocess_time_series_data,
            "plot": plot_time_series_barplot,
        },
        "multi-province-time-series-barplot": {
            "preprocess": preprocess_multi_province_time_series_data,
            "plot": plot_multi_province_time_series_barplot,
        },
        "province-map": {
            "preprocess": preprocess_province_map_data,
            "plot": plot_province_map_matplotlib,
        },
        "multi-week-province-map": {
            "preprocess": preprocess_multi_week_province_map_data,
            "plot": plot_multi_week_province_map_matplotlib,
        },
        "age-sex-pyramid-plot": {
            "preprocess": preprocess_pyramid_data,
            "plot": plot_pyramid,
        },
        "multi-province-age-sex-pyramid-plot": {
            "preprocess": preprocess_multi_province_pyramid_data,
            "plot": plot_multi_province_pyramid,
        },
        "zone-sante-map": {
            "preprocess": preprocess_zone_sante_map_data,
            "plot": plot_zone_sante_map_matplotlib,
        },
        "multi-week-zone-sante-map": {
            "preprocess": preprocess_multi_week_zone_sante_map_data,
            "plot": plot_multi_week_zone_sante_map_matplotlib,
        },
    }

    # check if the plot type is supported
    if plot_type not in plot_functions:
        raise ValueError(f"Plot type '{plot_type}' is not supported.")

    # preprocess the data
    preprocess = plot_functions[plot_type]["preprocess"]
    plot_data = preprocess(data, parameters.get("data", {}))

    # generate the plot
    plot = plot_functions[plot_type]["plot"]
    plot_output = plot(plot_data, parameters.get("graphics", {}))

    # now convertion to HTML handled in plot, so just return the output
    return plot_output