import os
from plots.time_series_barplot.preprocess import preprocess_time_series_data
from plots.time_series_barplot.plot import plot_time_series_barplot
from plots.province_map.preprocess import preprocess_province_map_data
from plots.province_map.plot import plot_province_map_matplotlib

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
            'plot': plot_province_map_matplotlib
        },
    }

    if plot_type not in plot_functions:
        raise ValueError(f"Plot type '{plot_type}' is not supported.")

    # preprocess the data
    preprocess = plot_functions[plot_type]['preprocess']
    plot_data = preprocess(data, parameters.get('data', {}))

    # generate the plot
    plot = plot_functions[plot_type]['plot']
    plot_output = plot(plot_data, parameters.get('graphics', {}))

    # handle Matplotlib plots (image file paths)
    if isinstance(plot_output, str):  # if a file path is returned, generate absolute path for <img> tag
        absolute_path = os.path.abspath(plot_output)  # convert to absolute path
        plot_html = f'<img src="{absolute_path}" alt="Generated Map Plot" />'
    else:  # Handle Plotly plots
        plot_html = plot_output.to_html(full_html=False, include_plotlyjs=False)

    return plot_html