from datetime import datetime, timedelta
from aiogram import Router
from aiogram.types import Message, BufferedInputFile 
from aiogram.filters import Command

from storage import storage
from middleware.middleware import LoguruMiddleware
from utils.charts import get_water_chart, get_kalories_chart


# Содание роутера и прикрепление к нему логгера
charts_router = Router()
charts_router.message.middleware(LoguruMiddleware(router_name='charts_router'))


@charts_router.message(Command('water_chart'))
async def water_chart(message: Message):
    ''' Докстринга '''

    dates = []
    for i in range(0, 7):
        dates.append((datetime.today() - timedelta(days=i)).strftime('%d-%m-%Y'))

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if user_data:
        # Данные по воде за последние 7 дней, сразу рассчитывает сумму по дням
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

    # Только если данные есть данные по воде хотя бы за один день
    if logged_water:
        chart = get_water_chart(logged_water, user_data.get('water_goal'))
        chart = await message.answer_photo(
            BufferedInputFile(chart, filename='water_chart.png'),
            caption='График потребления воды',
            show_caption_above_media=True
        )
    else:
        await message.answer(text='Последние 7 дней вы не сохраняли данные о количестве выпитой воды.')


@charts_router.message(Command('calories_chart'))
async def calories_chart(message: Message):
    ''' Докстринга '''

    dates = []
    for i in range(0, 7):
        dates.append((datetime.today() - timedelta(days=i)).strftime('%d-%m-%Y'))

    user_id = message.from_user.id
    user_data = storage.get(user_id)
    if user_data:
        # Данные по воде за последние 7 дней, сразу рассчитывает сумму по дням
        logged_kalories = {}
        burned_kalories = {}
        for date in dates:
            if date in user_data.get('logged_calories'):
                logged_kalories[date] = sum(user_data.get('logged_calories').get(date).values())
            else:
                logged_kalories[date] = 0
            if date in user_data.get('burned_calories'):
                burned_kalories[date] = sum(user_data.get('burned_calories').get(date).values())
            else:
                burned_kalories[date] = 0
    else:
        # Если профиля пользователя нет в хранилище, то предлагаем создать профиль
        await message.answer(text='Пожалуйста создайте Ваш профиль при помощи команды /set_profile.')
        return None

    # Только если данные есть данные по воде хотя бы за один день
    if logged_kalories or burned_kalories:
        chart = get_kalories_chart(logged_kalories, burned_kalories, user_data.get('kalories_goal'))
        chart = await message.answer_photo(
            BufferedInputFile(chart, filename='kalories_chart.png'),
            caption='График полученных калорий',
            show_caption_above_media=True
        )
    else:
        await message.answer(text=('Последние 7 дней вы не сохраняли данные о '
                             'съеденных продуктах.')
                             )
