import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

OUTPUT_DIR = "./output/"


def plot_time_series_barplot(plot_data, parameters):
    """
    Creates a time-series bar plot using preprocessed data.
    """
    x_label = parameters.get("x_label", "Time")
    y_label = parameters.get("y_label", "Count")
    title = parameters.get("title", "Plot Title")
    fig_width = parameters.get("fig_width", 300)
    fig_height = parameters.get("fig_height", 500)
    export = parameters.get("export", True)
    filename = parameters.get("filename", "time_series_barplot.pdf")

    # extract parameters for moving average
    ma_params = parameters.get("moving_average", False)
    ma_show = ma_params.get("show", False)
    ma_lw = ma_params.get("linewidth", 2)
    ma_colour = ma_params.get("colour", "#B4A269")

    # create plot
    fig = px.bar(
        plot_data,
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
    )

    # add a moving average line if specified
    if ma_show:
        fig.add_trace(
            go.Scatter(
                x=plot_data["date"],
                y=plot_data["moving_average"],
                mode="lines",
                name="Moving Average",
                line=dict(color=ma_colour, width=ma_lw),
            )
        )

    # export plot if specified
    if export:
        pdf_filename = os.path.join(OUTPUT_DIR, filename)
        counter = 0
        while os.path.exists(pdf_filename):
            counter += 1
            pdf_filename = os.path.join(
                OUTPUT_DIR, "%s.%d.pdf" % (Path(filename).stem, counter)
            )

        # create layout object
        fig.write_image(pdf_filename, format="pdf", width=fig_width, height=fig_height)

    # convert plot to HTML
    fig_html = fig.to_html(full_html=False, include_plotlyjs=False)

    return fig_html
