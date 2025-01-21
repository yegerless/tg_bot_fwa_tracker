from aiogram import Router, F
from aiogram.types import Message 
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from storage import storage
from middleware.middleware import LoguruMiddleware
from utils.utils import get_city_temp, get_water_norm, get_kallories_norm


# Содание роутера и прикрепление к нему логгера
profile_router = Router()
profile_router.message.middleware(LoguruMiddleware(router_name='profile_router'))



class CreatingProfile(StatesGroup):
    '''
        Класс-группа состояний для конечного автомата по созданию профиля пользователя
    '''

    input_height = State()
    input_weight = State()
    input_age = State()
    input_activity = State()
    input_city = State()
    input_calories_goal = State()


@profile_router.message(StateFilter(None), Command('set_profile'))
async def cmd_set_profile(message: Message, state: FSMContext):
    '''
        Обработчик команды '/set_profile'. 
        Запускает конечный автомат по созданию профиля пользователя.
        Запрашивает у пользователя значение его роста в см.
        Устанавливает состояние input_height.
    '''

    await message.answer(text='Введите ваш рост в см, округляя до целого (например: 176)')
    await state.set_state(CreatingProfile.input_height)


@profile_router.message(CreatingProfile.input_height, F.text)
async def input_height(message: Message, state: FSMContext):
    '''
        Обработчик состояния конечного автомата input_height.
        Принимает значение роста пользователя в см и валидирует его.
        При неудачной валидации запрашивает значение роста еще раз, 
            при успешной валидации устанавливает значение конечного
            автомата input_weight и запрашивает вес пользователя в кг.
    '''

    user_id = message.from_user.id
    # Валидация роста
    try:
        height = int(message.text)
        # Мин и макс рост человека по данным гугла
        if height < 59 or height > 251:
            raise ValueError
    except (ValueError, TypeError):
        await message.answer(text=('Вы ввели некорректное значение роста. '
                                   'Введите ваш рост в см, округляя до целого (например: 70)')
                             )
        return None

    # При успешной валидации сохранение роста и запрос значения веса
    storage[user_id] = {'height': height}
    await message.answer(text=f'Введите ваш вес в кг с точность до 0.1 (например: 60.5)')
    await state.set_state(CreatingProfile.input_weight)


@profile_router.message(CreatingProfile.input_weight, F.text)
async def input_weight(message: Message, state: FSMContext):
    '''
        Обработчик состояния конечного автомата input_weight.
        Принимает значение веса пользователя в кг и валидирует его.
        При неудачной валидации запрашивает вес еще раз, при успешной
            валидации устанавливает состояние input_age и запрашивает
            возраст пользователя в полных годах.
    '''

    user_id = message.from_user.id
    # Валидация веса
    try:
        weight = float(message.text)
        # Мин и макс вес человека по данным гугла
        if weight < 14.5 or weight > 645:
            raise ValueError
    except (ValueError, TypeError):
        await message.answer(text=('Вы ввели некорректное значение веса. '
                             'Введите ваш вес в кг с точность до 0.1 (например: 60.5)')
                             )
        return None

    # После успешной валидации сохранение веса и запрос значения возраста
    storage[user_id]['weight'] = weight
    await message.answer(text=f'Напишите, сколько вам полных лет? (например: 25)')
    await state.set_state(CreatingProfile.input_age)


@profile_router.message(CreatingProfile.input_age, F.text)
async def input_age(message: Message, state: FSMContext):
    '''
        Обработчик состояния конечного автомата input_age.
        Принимает значение возраста пользователя в полных годах
            и валидирует его.
        При неудачной валидации запрашивает значение роста еще раз,
            при успешной валидации устанавливает состояние input_activity
            и запрашивает уровень физической активности пользователя в
            минутах в день.
    '''

    user_id = message.from_user.id
    # Валидация возраста
    try:
        age = int(message.text)
        # Будем считать, что теоретически родители могут сделать профиль для своего ребенка 
        # возрастом 0 лет. Верхняя граница - максимальный достигнутый человеком возраст по
        # данным википедии
        if age < 0 or age > 122:
            raise ValueError
    except (ValueError, TypeError):
        await message.answer(text=('Вы ввели некорректный возраст. '
                                   'Напишите, сколько вам полных лет? (например: 25)')
                             )
        return None

    # После успешной валидации сохранение возраста и запрос физической активности
    storage[user_id]['age'] = age
    await message.answer(text=f'Введите ваш уровень физической активности в минутах в день (например: 60)')
    await state.set_state(CreatingProfile.input_activity)


@profile_router.message(CreatingProfile.input_activity, F.text)
async def input_activity(message: Message, state: FSMContext):
    '''
        Обработчик состояния конечного автомата input_activity.
        Принимает значение физической активности пользователя в 
            минутах в день и валидирует его.
        При неудачной валидации запрашивает уровень физической
            активности еще раз, при успешной валидации устанавливает
            состояние input_city и запрашивает название города, в котором
            живет пользователь.
    '''

    user_id = message.from_user.id
    # Валидация значения физической активности
    try:
        activity = int(message.text)
        # Кол-во минут активности не может быть отрицательным
        # и не может превышать кол-во минут в сутках
        if activity < 0 or activity > 1440:
            raise ValueError
    except (ValueError, TypeError):
        await message.answer(text=('Вы ввели некорректное значение физической активности. '
                                   'Введите ваш уровень физической активности в минутах в день (например: 60)')
                             )
        return None

    # После успешной валидации сохранение активности и запрос названия города
    storage[user_id]['activity'] = activity
    await message.answer(text=f'Введите название города, где вы живете (например: Москва)')
    await state.set_state(CreatingProfile.input_city)


@profile_router.message(CreatingProfile.input_city, F.text)
async def input_activity(message: Message, state: FSMContext):
    '''
        Обработчик состояния конечного автомата input_city.
        Принимает название города, в котором проживает пользователь.
        Отправляет запрос к OpenWeather API для получения текущей температуры
            в городе. Если значение температуры не удалось получить, то расчитывает
            норму воды для пользователя по формуле без учета температуры, если 
            удалось - то с учетом.
        Устанавливает состояние input_calories_goal и запрашивает у пользователя
            его цело по потребляемым калориям в день.
    '''

    user_id = message.from_user.id
    # Получение и сохранение города
    city =  message.text
    storage[user_id]['city'] = city

    # Запрос к OpenWeather Api
    temp = await get_city_temp(city=city)
    # Расчет нормы воды
    storage[user_id]['water_goal'] = get_water_norm(weight=storage[user_id]['weight'], 
                                activity=storage[user_id]['activity'],
                                city_temp = temp)

    # Проверка получена ли температура
    if not temp:
        await message.answer(text=('Не удалось получить значение температуры для введенного названия города. '
                                   'Норма воды расчитана без учета температуры.')
                             )

    # Запрос цели по калориям
    await message.answer(text=('Введите вашу цель по потребляемым калориям в день (например 2500) или напишите '
                               '"Рассчитать", если хотите получить автоматический расчет нормы калорий для Вас.')
                         )
    await state.set_state(CreatingProfile.input_calories_goal)


@profile_router.message(CreatingProfile.input_calories_goal, F.text)
async def input_calories_goal(message: Message, state: FSMContext):
    '''
        Обработчик состояния конечного автомата input_calories_goal.
        Принимает значение цели пользователя по калориям или сообщение
            'Рассчитать'. Во втором случае расчитывает цель по калориям
            для пользователя автоматически (по формуле).
        Возвращает сообщение о создании профиля и сбрасывает конечный
            автомат.
    '''

    user_id = message.from_user.id
    # Получение цели по калориям
    calories_goal =  message.text
    # Проверка полученного значения
    if calories_goal == 'Рассчитать':
        # Расчет и сохранение цели по формуле
        storage[user_id]['calories_goal'] = get_kallories_norm(weight=storage[user_id]['weight'], 
                                        height=storage[user_id]['height'],
                                        age=storage[user_id]['age'], 
                                        activity=storage[user_id]['activity'])
    else:
        # При получении значения отличного от 'Рассчитать'
        # валидация полученного значения и запрос заново при провале
        # или сохранение при успехе
        try:
            calories_goal = int(calories_goal)
            storage[user_id]['calories_goal'] = calories_goal
        except (ValueError, TypeError):
            await message.answer(text=('Вы ввели некорректное значение цели по каллориям. '
                                       'Введите вашу цель по потребляемым калориям в день '
                                       '(например 2500) или напишите "Рассчитать", '
                                       'если хотите получить автоматический расчет нормы калорий для Вас.')
                                 )
            return None

    # Заготовка для логирования воды, калорий и тренировок в хранилище
    storage[user_id]['logged_water'] = {}
    storage[user_id]['logged_calories'] = {}
    storage[user_id]['burned_calories'] = {}

    # Информационное сообщение об успешном создании профиля
    await message.answer(text=('Ваш профиль успешно создан. Цель по воде - '
                               f'{storage[user_id]['water_goal']} мл в день. '
                               f'Цель по калориям - {storage[user_id]['calories_goal']} ккал/день')
                         )
    await state.clear()
