import os
import pandas as pd
import plotly.graph_objects as go

from modules.data_filtering import apply_filters
from plotting_modules.add_tabs import generate_tabbed_html


def preprocess(data, config):
    """
    Preprocesses data for pyramid plot.
    """
    filtering_config = config.get("filtering", [])
    age_column = config.get("age_column", "age")
    age_groups = config.get(
        "age_groups", [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    )
    sex_column = config.get("sex_column", "sex")
    group_by = config.get("group_by", None)

    # apply filters
    filtered_data = apply_filters(data, filtering_config)
    # return empty dataframe if no data left after filtering
    if filtered_data.empty:
        return pd.DataFrame()

    # create a copy of relevant column
    plot_data = filtered_data.copy()

    # check that age_column is in data
    if age_column not in plot_data.columns:
        raise ValueError(f"Column '{age_column}' not found in data.")
    # check that sex_column is in data
    if sex_column not in plot_data.columns:
        raise ValueError(f"Column '{sex_column}' not found in data.")

    # check also group_by column
    if group_by and group_by not in plot_data.columns:
        raise ValueError(f"Column '{group_by}' not found in data.")
    elif group_by is None:  # add a dummy column
        plot_data["group"] = 0
    else:  # rename group_by column to group
        plot_data.rename(columns={group_by: "group"}, inplace=True)

    # add inf to the last age group
    age_groups.append(float("inf"))

    # take only rows with sex_column matching "male" and "female"
    plot_data = plot_data[plot_data[sex_column].isin(["male", "female"])]

    # create age bins
    plot_data[age_column] = plot_data[age_column].apply(
        lambda x: 0 if pd.isnull(x) else int(x)
    )
    plot_data["age_group"] = pd.cut(plot_data[age_column], bins=age_groups, right=False)
    # group by age and sex
    plot_data = (
        plot_data.groupby(["group", "age_group", sex_column], observed=False)
        .size()
        .unstack(sex_column, fill_value=0)
        .reset_index()
    )

    # ensure 'male' and 'female' columns exist
    if "male" not in plot_data.columns:
        plot_data["male"] = 0
    if "female" not in plot_data.columns:
        plot_data["female"] = 0

    # set first category to negative for pyramid plot
    plot_data["male"] = -plot_data["male"]

    return plot_data


def get_nice_round_number(value):
    scale = 10 ** (len(str(int(value))) - 1)
    nice_values = [1, 2, 5, 10]
    return scale * min(nice_values, key=lambda x: abs(value / scale - x))


def get_nice_age_label(age_interval):
    if age_interval.right == float("inf"):
        return f"{int(age_interval.left)}+"
    return f"{int(age_interval.left)}-{int(age_interval.right - 1)}"


def plot(plot_data, config, out_dir):
    """
    Plots pyramid plot using Plotly.
    """
    # if no data, return html that says so
    if plot_data.empty:
        return "<h4>%s (no data available)</h4>"

    # get plot parameters
    title = config.get("title", "Population Pyramid")
    x_label = config.get("x_label", "Population")
    y_label = config.get("y_label", "Age Group")
    fig_width = config.get("fig_width", 1200)
    fig_height = config.get("fig_height", 500)
    export = config.get("export", True)
    filestem = config.get("filestem", "age_sex_pyramid_plot")

    # map age groups to nice labels
    plot_data["age_group_labels"] = plot_data["age_group"].apply(get_nice_age_label)

    # get unique groups
    seen = set()
    groups = []
    for item in plot_data["group"].unique():
        lower_item = item.lower()
        if lower_item not in seen:
            seen.add(lower_item)
            groups.append(item)
    # create list to store figs
    figs_html = []
    # loop through groups and create plots
    for group in groups:
        group_data = plot_data[plot_data["group"] == group]

        # create figure
        fig = go.Figure()

        # add trace for males
        fig.add_trace(
            go.Bar(
                y=group_data["age_group_labels"].astype(
                    str
                ),  # age groups as strings for proper labeling
                x=group_data["male"],
                name="Male",
                orientation="h",
                marker=dict(color="#1A5632"),
                opacity=0.9,
            )
        )

        # add trace for females
        fig.add_trace(
            go.Bar(
                y=group_data["age_group_labels"].astype(str),
                x=group_data["female"],
                name="Female",
                orientation="h",
                marker=dict(color="#9F2241"),
                opacity=0.9,
            )
        )

        # create nice x-axis ticks
        num_divs = 4
        max_population = max(
            group_data["male"].abs().max(), group_data["female"].abs().max()
        )
        tick_step = get_nice_round_number(max_population / num_divs)
        max_tick = tick_step * 5  # round up to a multiple of tick_step
        ticks = list(range(-max_tick, max_tick + 1, tick_step))
        tick_labels = [str(abs(tick)) for tick in ticks]

        # update layout
        fig.update_layout(
            title=title,
            xaxis=dict(
                title=x_label,
                tickvals=ticks,
                ticktext=tick_labels,
                gridcolor="rgba(200,200,200,0.5)",
            ),
            yaxis=dict(
                title=y_label, categoryorder="array", gridcolor="rgba(200,200,200,0.5)"
            ),
            barmode="overlay",
            bargap=0.1,
            bargroupgap=0,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=60, r=20, b=60, t=50),
        )

        # convert figure to HTML string
        fig_html = fig.to_html(full_html=False, include_plotlyjs=False)
        fig_html = fig_html.replace("<div ", '<div class="plotly-graph-div" ')
        figs_html.append((fig_html, group))

        # export plot if specified
        if export:
            pdf_filename = os.path.join(out_dir, f"{filestem}_{group}.pdf")
            counter = 0
            while os.path.exists(pdf_filename):
                counter += 1
                pdf_filename = os.path.join(
                    out_dir, f"{filestem}_{group}.{counter}.pdf"
                )

            # create layout object
            fig.write_image(
                pdf_filename, format="pdf", width=fig_width, height=fig_height
            )

    # if multiple groups, return tabbed display
    if len(groups) > 1:
        return generate_tabbed_html(filestem, figs_html)
    else:
        return figs_html[0][0]
