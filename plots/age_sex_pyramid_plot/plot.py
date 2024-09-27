import plotly.graph_objects as go
from pathlib import Path
import os

OUTPUT_DIR = './output/'

def get_nice_round_number(value):
    scale = 10 ** (len(str(int(value))) - 1)
    nice_values = [1, 2, 5, 10]
    return scale * min(nice_values, key=lambda x: abs(value / scale - x))

def get_nice_age_label(age_interval):
    if age_interval.right == float('inf'):
        return f'{int(age_interval.left)}+'
    return f'{int(age_interval.left)}-{int(age_interval.right - 1)}'

def plot_pyramid(plot_data, parameters):
    """
    Plots a population pyramid using Plotly.
    """
    title = parameters.get('title', 'Population Pyramid')
    x_label = parameters.get('x_label', 'Population')
    y_label = parameters.get('y_label', 'Age Group')
    male_color = parameters.get('male_color', '#1A5632')
    female_color = parameters.get('female_color', '#9F2241')
    fig_width = parameters.get('fig_width', 300)
    fig_height = parameters.get('fig_height', 500)
    export = parameters.get('export', True)
    filename = parameters.get('filename', 'time_series_barplot.pdf')

    # map age groups to nice labels
    plot_data['age_group_labels'] = plot_data['age_group'].apply(get_nice_age_label)

    # create figure
    fig = go.Figure()

    # add trace for males
    fig.add_trace(go.Bar(
        y=plot_data['age_group_labels'].astype(str),  # age groups as strings for proper labeling
        x=plot_data['male'],
        name='Male',
        orientation='h',
        marker=dict(color=male_color),
        opacity=0.9
    ))

    # add trace for females
    fig.add_trace(go.Bar(
        y=plot_data['age_group_labels'].astype(str),
        x=plot_data['female'],
        name='Female',
        orientation='h',
        marker=dict(color=female_color),
        opacity=0.9
    ))

    # create nice x-axis ticks
    num_divs = 4
    max_population = max(plot_data['male'].abs().max(), plot_data['female'].abs().max())
    tick_step = get_nice_round_number(max_population / num_divs)
    max_tick = (tick_step * 5)  # round up to a multiple of tick_step
    ticks = list(range(-max_tick, max_tick + 1, tick_step))
    tick_labels = [str(abs(tick)) for tick in ticks]

    # update layout
    fig.update_layout(
        title=title,
        xaxis=dict(
            title=x_label,
            tickvals=ticks,
            ticktext=tick_labels,
            gridcolor='rgba(200,200,200,0.5)'
        ),
        yaxis=dict(
            title=y_label,
            categoryorder='array',
            gridcolor='rgba(200,200,200,0.5)'
        ),
        barmode='overlay',
        bargap=0.1,
        bargroupgap=0,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    # export plot if specified
    if export:
        pdf_filename = os.path.join(OUTPUT_DIR, filename)
        counter = 0
        while os.path.exists(pdf_filename):
            counter += 1
            pdf_filename = os.path.join(OUTPUT_DIR, '%s.%d.pdf' % (Path(filename).stem, counter))

        # create layout object
        fig.write_image(pdf_filename, format='pdf', width=fig_width, height=fig_height)


    return fig
