import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import os

OUTPUT_DIR = "./output/"


def get_nice_round_number(value):
    scale = 10 ** (len(str(int(value))) - 1)
    nice_values = [1, 2, 5, 10]
    return scale * min(nice_values, key=lambda x: abs(value / scale - x))


def get_nice_age_label(age_interval):
    if age_interval.right == float("inf"):
        return f"{int(age_interval.left)}+"
    return f"{int(age_interval.left)}-{int(age_interval.right - 1)}"


def plot_multi_province_pyramid(plot_data, parameters):
    """
    Plots population pyramids for multiple provinces using Plotly, with subplots for each province.
    Assumes plot_data contains columns: 'age_group', 'sex', 'province', and 'count'.
    """
    title = parameters.get("title", "Population Pyramid")
    x_label = parameters.get("x_label", "Population")
    y_label = parameters.get("y_label", "Age Group")
    male_color = parameters.get("male_color", "#1A5632")
    female_color = parameters.get("female_color", "#9F2241")
    fig_width = parameters.get("fig_width", 300)
    fig_height = parameters.get("fig_height", 500)
    export = parameters.get("export", True)
    filename = parameters.get("filename", "population_pyramids.pdf")

    provinces = plot_data["province"].unique()
    num_provinces = len(provinces)
    num_cols = 2  # number of columns in subplots
    num_rows = (
        num_provinces + num_cols - 1
    ) // num_cols  # calculate the number of rows needed

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

    # loop through each province and create a subplot for each
    for i, province in enumerate(provinces):
        province_data = plot_data[plot_data["province"] == province]

        # pivot the data so that we can plot male and female counts in the same graph
        province_pivot = province_data.pivot_table(
            index="age_group", columns="sex", values="count", fill_value=0
        ).reset_index()

        # map age groups to nice labels
        province_pivot["age_group_labels"] = province_pivot["age_group"].apply(
            get_nice_age_label
        )

        # add trace for males
        male_trace = go.Bar(
            y=province_pivot["age_group_labels"].astype(
                str
            ),  # age groups as strings for proper labeling
            x=province_pivot.get("male", 0),  # get 'male' values or 0 if missing
            name="Male",
            orientation="h",
            marker=dict(color=male_color),
            opacity=0.9,
            showlegend=False,
        )

        # add trace for females
        female_trace = go.Bar(
            y=province_pivot["age_group_labels"].astype(str),
            x=province_pivot.get("female", 0),  # get 'female' values or 0 if missing
            name="Female",
            orientation="h",
            marker=dict(color=female_color),
            opacity=0.9,
            showlegend=False,
        )

        # add traces to the appropriate subplot
        row = (i // num_cols) + 1
        col = (i % num_cols) + 1
        fig.add_trace(male_trace, row=row, col=col)
        fig.add_trace(female_trace, row=row, col=col)

        # create nice x-axis ticks
        num_divs = 4
        max_population = max(
            province_pivot["male"].abs().max(), province_pivot["female"].abs().max()
        )
        tick_step = get_nice_round_number(max_population / num_divs)
        max_tick = tick_step * (num_divs + 1)
        ticks = list(range(-max_tick, max_tick + 1, tick_step))
        tick_labels = [str(abs(tick)) for tick in ticks]

        # update x-axis for each subplot
        fig.update_xaxes(
            title_text=x_label, tickvals=ticks, ticktext=tick_labels, row=row, col=col
        )

        # update y-axis for each subplot
        fig.update_yaxes(title_text=y_label, categoryorder="array", row=row, col=col)

    # update layout for all subplots
    fig.update_layout(
        height=fig_height * num_rows * 0.7,
        title_text=title,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        barmode="overlay",
        bargap=0.1,
        bargroupgap=0,
    )

    # remove excess margins
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
            pdf_filename, format="pdf", width=fig_width, height=fig_height * num_rows
        )

    return fig
