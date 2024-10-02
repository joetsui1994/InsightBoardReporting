from drc_mpox_reporting.plots.add_tabs import generate_tab_html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import os

OUTPUT_DIR = "./output/"


def plot_multi_province_time_series_barplot(plot_data, parameters):
    """
    Creates a time-series bar plot using preprocessed data.
    If province data is available, creates subplots for each province.
    """
    x_label = parameters.get("x_label", "Time")
    y_label = parameters.get("y_label", "Count")
    title = parameters.get("title", "Plot Title")
    fig_width = parameters.get("fig_width", 300)
    fig_height = parameters.get("fig_height", 500)
    export = parameters.get("export", True)
    filestem = parameters.get("filename", "time_series_barplot")

    # extract parameters for moving average
    ma_params = parameters.get("moving_average", False)
    ma_show = ma_params.get("show", False)
    ma_lw = ma_params.get("linewidth", 2)
    ma_colour = ma_params.get("colour", "#B4A269")

    # create plots
    provinces = plot_data["province"].unique()
    # list to store figs
    figs = []
    # loop through each province and add a subplot
    for province in provinces:
        province_data = plot_data[plot_data["province"] == province]

        # create plot
        fig = px.bar(
            province_data,
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
                    x=province_data["date"],
                    y=province_data["moving_average"],
                    mode="lines",
                    name="Moving Average",
                    line=dict(color=ma_colour, width=ma_lw),
                )
            )

        # remove margin
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=50),
                          autosize=True)


        # convert plot to HTML and add to list
        fig_html = fig.to_html(full_html=False, include_plotlyjs=False, config={'responsive': True})
        fig_html = fig_html.replace('<div ', '<div class="plotly-graph-div" ')
        figs.append((fig_html, province))

        # export plot if specified
        if export:
            pdf_filename = os.path.join(OUTPUT_DIR, f"{filestem}_{province}.pdf")
            counter = 0
            while os.path.exists(pdf_filename):
                counter += 1
                pdf_filename = os.path.join(
                    OUTPUT_DIR, f"{filestem}_{province}.{counter}.pdf"
                )

            # export to PDF
            fig.write_image(
                pdf_filename,
                format="pdf",
                width=fig_width,
                height=fig_height
            )

    # generate tabbed HTML
    fig_html = generate_tab_html("multi-province-time-series-barplot", figs)

    return fig_html