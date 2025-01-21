import plotly.graph_objects as go


def get_water_chart(logged_water: dict[str, int], water_goal: int) -> None:
    ''' Докстринга '''

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(logged_water.keys()), y=list(logged_water.values()),
                         marker_color='CornflowerBlue', text=list(logged_water.values())))
    fig.update_layout(title_text='Кол-во выпитой воды за последние 7 дней.',
                      xaxis_title='Дата', yaxis_title='Выпито воды в мл', 
                      yaxis_range=[0, water_goal + 1000], plot_bgcolor='AliceBlue')
    fig.add_hline(y=water_goal, line_color='red', annotation_text=water_goal)
    chart = fig.to_image(format='png')

    return chart
    