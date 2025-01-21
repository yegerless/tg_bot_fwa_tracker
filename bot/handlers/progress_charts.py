from datetime import datetime, timedelta
from aiogram import Router
from aiogram.types import Message, BufferedInputFile 
from aiogram.filters import Command

from storage import storage
from middleware.middleware import LoguruMiddleware
from utils.charts import get_water_chart, get_calories_chart


# Содание роутера и прикрепление к нему логгера
charts_router = Router()
charts_router.message.middleware(LoguruMiddleware(router_name='charts_router'))


@charts_router.message(Command('water_chart'))
async def water_chart(message: Message):
    '''
        Обработчик команды '/water_chart'.
        Отправляет пользователю изображение с графиком
            выпитой им воды за последние 7 дней. 
    '''

    # Получение списка дат последних 7 дней
    dates = []
    for i in range(0, 7):
        dates.append((datetime.today() - timedelta(days=i)).strftime('%d-%m-%Y'))

    # Получение данных пользователя по id
    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if user_data:
        # Извлечение из хранилища данных по воде за последние 7 дней, 
        # с расчетом суммы по дням
        logged_water = {}
        for date in dates:
            if date in user_data.get('logged_water'):
                logged_water[date] = sum(user_data.get('logged_water').get(date).values())
            else:
                logged_water[date] = 0
    else:
        # Если профиля пользователя нет в хранилище, то предлагаем создать профиль
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    # Создание графика и отправка картинки пользователю
    chart = get_water_chart(logged_water, user_data.get('water_goal'))
    chart = await message.answer_photo(
        BufferedInputFile(chart, filename='water_chart.png'),
        caption='*если значение за день 0, значит вы не сохраняли данные в этот день.',
    )


@charts_router.message(Command('calories_chart'))
async def calories_chart(message: Message):
    '''
        Обработчик команды '/calories_chart'
        Отправляет пользователю изображение с графиком
            полученных из еды и сожженных физической 
            активностью калорий за последние 7 дней. 
    '''

    # Получение списка дат последних 7 дней
    dates = []
    for i in range(0, 7):
        dates.append((datetime.today() - timedelta(days=i)).strftime('%d-%m-%Y'))

    # Получение данных пользователя по id
    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if user_data:
        # Извлечение из хранилища данных по калориям за последние 7 дней, 
        # с расчетом суммы по дням
        logged_calories = {}
        burned_calories = {}
        for date in dates:
            if date in user_data.get('logged_calories'):
                logged_calories[date] = sum(user_data.get('logged_calories').get(date).values())
            else:
                logged_calories[date] = 0
            if date in user_data.get('burned_calories'):
                burned_calories[date] = sum(user_data.get('burned_calories').get(date).values())
            else:
                burned_calories[date] = 0
    else:
        # Если профиля пользователя нет в хранилище, то предлагаем создать профиль
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    # Создание графика и отправка картинки пользователю
    chart = get_calories_chart(logged_calories, burned_calories, user_data.get('calories_goal'))
    chart = await message.answer_photo(
        BufferedInputFile(chart, filename='calories_chart.png'),
        caption='*если значение за день 0, значит вы не сохраняли данные в этот день.')
