import plotly.graph_objects as go


def get_water_chart(logged_water: dict[str, int], water_goal: int) -> bytes:
    '''
        Функция get_water_chart - принимает данные о выпитой воде по 
            дням и цель по выпитой воде в день, возвращает изображение
            графика выпитой воды по дням в формате png в виде байтового
            объекта (который затем можно отправить пользователю).
        Аргументы:
            logged_water (dict(str: int)) - данные о выпитой воде по дням в
                виде словаря в формате {день: кол-во воды в мл}.
            water_goal (int) - цель пользователя по выпитой воде в день в мл.
    '''

    # Создание бар-чарта
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(logged_water.keys()), y=list(logged_water.values()),
                         marker_color='CornflowerBlue', text=list(logged_water.values())))
    # Настройка шаблона графика (подписи, размер и тд)
    fig.update_layout(title_text='Кол-во выпитой воды за последние 7 дней.',
                      xaxis_title='Дата', yaxis_title='Выпито воды в мл', 
                      yaxis_range=[0, water_goal + 1000], plot_bgcolor='AliceBlue',
                      autosize=False, width=800, height=500, 
                      margin={'l': 10, 'r': 10, 'b': 25, 't': 50})
    # Добавление целевой линии
    fig.add_hline(y=water_goal, line_color='red', annotation_text=water_goal)
    # Конфертация графика изображение в формате png в виде байтового объекта
    chart = fig.to_image(format='png')

    return chart


def get_calories_chart(logged_calories: dict[str, int], burned_calories: dict[str, int], 
                       calories_goal: int) -> bytes:
    '''
        Функция get_calories_chart - принимает данные о полученных и 
            сожженных калориях по дням и цель по калориям в день, 
            возвращает изображение графика полученных и потраченных
            калорий по дням в формате png в виде байтового
            объекта (который затем можно отправить пользователю).
        Аргументы:
            logged_calories (dict(str: int)) - данные о полученных калориях 
                по дням в виде словаря в формате {день: кол-во калорий}.
            burned_calories (dict(str: int)) - данные о сожженных калориях
                по дням в виде словаря в формате {день: кол-во калорий}.
            water_goal (int) - цель пользователя по калориям в день.
    '''

    # Создание бар-чарта
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(logged_calories.keys()), y=list(logged_calories.values()),
                         marker_color='Crimson', text=list(logged_calories.values()),
                         name='Полученные калории'))
    # Создание второго бар-чарта, который застакается с первым
    fig.add_trace(go.Bar(x=list(burned_calories.keys()), y=list(burned_calories.values()),
                         marker_color='Orange', text=list(burned_calories.values()),
                         name='Сожженные калории'))
    # Настройка шаблона графика (подписи, размер и тд)
    fig.update_layout(title_text='Баланс калорий за последние 7 дней.',
                      xaxis_title='Дата', yaxis_title='Калории', 
                      yaxis_range=[0, calories_goal + 1000], plot_bgcolor='AliceBlue',
                      autosize=False, width=800, height=500, 
                      margin={'l': 10, 'r': 10, 'b': 25, 't': 50})
    # Добавление целевой линии
    fig.add_hline(y=calories_goal, line_color='Red', annotation_text=calories_goal)
    # Конфертация графика изображение в формате png в виде байтового объекта
    chart = fig.to_image(format='png')

    return chart
