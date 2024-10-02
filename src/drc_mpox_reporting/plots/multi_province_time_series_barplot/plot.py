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
    filename = parameters.get("filename", "time_series_barplot.pdf")

    # extract parameters for moving average
    ma_params = parameters.get("moving_average", False)
    ma_show = ma_params.get("show", False)
    ma_lw = ma_params.get("linewidth", 2)
    ma_colour = ma_params.get("colour", "#B4A269")

    # check if 'province' column exists for subplots
    if "province" in plot_data.columns:
        provinces = plot_data["province"].unique()
        num_provinces = len(provinces)
        num_cols = 2
        num_rows = (num_provinces + num_cols - 1) // num_cols

        # create subplots with the required number of rows and columns
        fig = make_subplots(
            rows=num_rows,
            cols=num_cols,
            subplot_titles=[f"Province: {province}" for province in provinces],
            shared_xaxes=False,
            shared_yaxes=False,
            horizontal_spacing=0.05,
            vertical_spacing=0.03,
        )

        # loop through each province and add a subplot
        for i, province in enumerate(provinces):
            province_data = plot_data[plot_data["province"] == province]

            # create bar plot for the specific province
            bar_trace = go.Bar(
                x=province_data["date"],
                y=province_data["count"],
                name=f"Province: {province}",
                marker_color="#1A5632",
                opacity=0.9,
                showlegend=False,
            )

            # add bar trace to the appropriate subplot
            row = (i // num_cols) + 1
            col = (i % num_cols) + 1
            fig.add_trace(bar_trace, row=row, col=col)

            # add moving average line if specified
            if ma_show:
                ma_trace = go.Scatter(
                    x=province_data["date"],
                    y=province_data["moving_average"],
                    mode="lines",
                    name=f"Moving Average: {province}",
                    line=dict(color=ma_colour, width=ma_lw),
                    showlegend=False,
                )
                fig.add_trace(ma_trace, row=row, col=col)

        # update layout for all subplots
        fig.update_layout(
            height=fig_height
            * num_rows
            * 0.7,  # adjust height according to number of rows
            title_text=title,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(200,200,200,0.5)"),
            yaxis=dict(gridcolor="rgba(200,200,200,0.5)"),
        )
    else:
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

        # add moving average line if specified
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

    # remove margin
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=50))

    # export plot if specified
    if export:
        pdf_filename = os.path.join(OUTPUT_DIR, filename)
        counter = 0
        while os.path.exists(pdf_filename):
            counter += 1
            pdf_filename = os.path.join(
                OUTPUT_DIR, "%s.%d.pdf" % (Path(filename).stem, counter)
            )

        # export to PDF
        fig.write_image(
            pdf_filename,
            format="pdf",
            width=fig_width,
            height=fig_height * num_rows * 0.7,
        )

    # convert plot to HTML
    fig_html = fig.to_html(full_html=False, include_plotlyjs=False)

    return fig_html