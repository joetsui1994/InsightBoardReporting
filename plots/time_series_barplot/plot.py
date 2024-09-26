import plotly.express as px
import plotly.graph_objects as go

def plot_time_series_barplot(plot_data, parameters):
    """
    Creates a time-series bar plot using preprocessed data.
    """
    x_label = parameters.get('x_label', 'Time')
    y_label = parameters.get('y_label', 'Count')
    title = parameters.get('title', 'Plot Title')

    # extract parameters for moving average
    ma_params = parameters.get('moving_average', False)
    ma_show = ma_params.get('show', False)
    ma_lw = ma_params.get('linewidth', 2)
    ma_colour = ma_params.get('colour', 'black')

    
    # create plot
    fig = px.bar(
        plot_data,
        x='date',
        y='count',
        labels={ 'date': x_label, 'count': y_label },
        title=title,
        color_discrete_sequence=['#278277']  # change bar colors
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='rgba(200,200,200,0.5)'),
        yaxis=dict(gridcolor='rgba(200,200,200,0.5)')
    )

    # add a moving average line if specified
    if ma_show:
        fig.add_trace(go.Scatter(
            x=plot_data['date'],
            y=plot_data['moving_average'],
            mode='lines',
            name='Moving Average',
            line=dict(color=ma_colour, width=ma_lw)
        ))

    return fig
