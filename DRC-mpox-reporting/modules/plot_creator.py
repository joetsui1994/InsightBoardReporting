from plots.time_series_barplot.preprocess import preprocess_time_series_data
from plots.time_series_barplot.plot import plot_time_series_barplot
from plots.province_map.preprocess import preprocess_province_map_data
from plots.province_map.plot import plot_province_map

def create_plot(data, graph_config):
    plot_type = graph_config['type']
    parameters = graph_config.get('parameters', {})

    plot_functions = {
        'time-series-barplot': {
            'preprocess': preprocess_time_series_data,
            'plot': plot_time_series_barplot
        },
        'province-map': {
            'preprocess': preprocess_province_map_data,
            'plot': plot_province_map
        },
        # add more plot types here
    }

    if plot_type not in plot_functions:
        raise ValueError(f"Plot type '{plot_type}' is not supported.")

    # preprocess data
    preprocess = plot_functions[plot_type]['preprocess']
    plot_data = preprocess(data, parameters.get('data', {}))

    # generate plot
    plot = plot_functions[plot_type]['plot']
    fig = plot(plot_data, parameters.get('graphics', {}))

    return fig
