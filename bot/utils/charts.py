import plotly.graph_objects as go


def get_water_chart(logged_water: dict[str, int], water_goal: int) -> None:
    ''' Докстринга '''

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(logged_water.keys()), y=list(logged_water.values()),
                         marker_color='CornflowerBlue', text=list(logged_water.values())))
    fig.update_layout(title_text='Кол-во выпитой воды за последние 7 дней.',
                      xaxis_title='Дата', yaxis_title='Выпито воды в мл', 
                      yaxis_range=[0, water_goal + 1000], plot_bgcolor='AliceBlue',
                      autosize=False, width=800, height=500, 
                      margin={'l': 10, 'r': 10, 'b': 25, 't': 50})
    fig.add_hline(y=water_goal, line_color='red', annotation_text=water_goal)
    chart = fig.to_image(format='png')

    return chart


def get_kalories_chart(logged_kalories: dict[str, int], burned_kalories: dict[str, int], 
                       kalories_goal: int) -> bytes:
    ''' Докстринга '''

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(logged_kalories.keys()), y=list(logged_kalories.values()),
                         marker_color='Crimson', text=list(logged_kalories.values()),
                         name='Полученные калории'))
    fig.add_trace(go.Bar(x=list(burned_kalories.keys()), y=list(burned_kalories.values()),
                         marker_color='Orange', text=list(burned_kalories.values()),
                         name='Сожженные калории'))
    fig.update_layout(title_text='Баланс калорий за последние 7 дней.',
                      xaxis_title='Дата', yaxis_title='Калории', 
                      yaxis_range=[0, kalories_goal + 1000], plot_bgcolor='AliceBlue',
                      autosize=False, width=800, height=500, 
                      margin={'l': 10, 'r': 10, 'b': 25, 't': 50})
    fig.add_hline(y=kalories_goal, line_color='Red', annotation_text=kalories_goal)
    chart = fig.to_image(format='png')

    return chart
