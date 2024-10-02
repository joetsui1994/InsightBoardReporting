from drc_mpox_reporting.plots.add_tabs import generate_tab_html
import plotly.graph_objects as go
import pandas as pd
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
    Plots population pyramids for multiple provinces using Plotly.
    Generates individual plots for each province and creates a tabbed HTML interface.
    Assumes plot_data contains columns: 'age_group', 'sex', 'province', and 'count'.
    """
    title = parameters.get("title", "Population Pyramid")
    x_label = parameters.get("x_label", "Population")
    y_label = parameters.get("y_label", "Age Group")
    male_color = parameters.get("male_color", "#1A5632")
    female_color = parameters.get("female_color", "#9F2241")
    fig_width = parameters.get("fig_width", 800)  # in pixels
    fig_height = parameters.get("fig_height", 600)  # in pixels
    export = parameters.get("export", True)
    filestem = parameters.get("filename", "population_pyramid")

    provinces = plot_data["province"].unique()
    figs = []

    # Loop through each province and create individual plots
    for province in provinces:
        province_data = plot_data[plot_data["province"] == province]

        # Pivot the data to have 'male' and 'female' counts side by side
        province_pivot = province_data.pivot_table(
            index="age_group", columns="sex", values="count", fill_value=0
        ).reset_index()

        # Map age groups to nice labels
        province_pivot["age_group_labels"] = province_pivot["age_group"].apply(
            get_nice_age_label
        )

        # Ensure 'male' and 'female' columns exist
        if 'male' not in province_pivot.columns:
            province_pivot['male'] = 0
        if 'female' not in province_pivot.columns:
            province_pivot['female'] = 0

        # Create the pyramid plot
        fig = go.Figure()

        # Add male bars
        fig.add_trace(go.Bar(
            y=province_pivot["age_group_labels"].astype(str),
            x=province_pivot["male"],
            name="Male",
            orientation='h',
            marker=dict(color=male_color),
            hoverinfo='x+y',
        ))

        # Add female bars
        fig.add_trace(go.Bar(
            y=province_pivot["age_group_labels"].astype(str),
            x=province_pivot["female"],
            name="Female",
            orientation='h',
            marker=dict(color=female_color),
            hoverinfo='x+y',
        ))

        # Calculate the maximum count for x-axis scaling
        max_count = max(-province_pivot['male'].min(), province_pivot['female'].max())

        # Create nice x-axis ticks
        num_divs = 4
        tick_step = get_nice_round_number(max_count / num_divs)
        max_tick = tick_step * num_divs
        ticks = [-max_tick + i * tick_step for i in range(2 * num_divs + 1)]
        tick_labels = [str(abs(tick)) for tick in ticks]

        # Update layout
        fig.update_layout(
            title='',
            barmode='overlay',
            bargap=0.1,
            bargroupgap=0,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title_text=x_label,
                tickvals=ticks,
                ticktext=tick_labels,
            ),
            yaxis=dict(
                title_text=y_label,
                categoryorder='array',
                categoryarray=province_pivot["age_group_labels"].astype(str),
            ),
            legend=dict(x=0.8, y=0.9),
            margin=dict(l=0, r=0, b=0, t=50),
            autosize=True,
        )

        # Convert figure to HTML string
        fig_html = fig.to_html(full_html=False, include_plotlyjs=False, config={'responsive': True})
        # Ensure the root div has class 'plotly-graph-div' for resizing
        fig_html = fig_html.replace('<div ', '<div class="plotly-graph-div" ', 1)

        # Append to figs list
        figs.append((fig_html, province))

        # Export plot if specified
        if export:
            pdf_filename = os.path.join(OUTPUT_DIR, f"{filestem}_{province}.pdf")
            counter = 0
            while os.path.exists(pdf_filename):
                counter += 1
                pdf_filename = os.path.join(OUTPUT_DIR, f"{filestem}_{province}.{counter}.pdf")

            # Save figure as PDF
            fig.write_image(pdf_filename, format='pdf', width=fig_width, height=fig_height)

    # Generate tabbed HTML
    fig_html_output = generate_tab_html("multi-province-pyramid", figs)

    return fig_html_output
