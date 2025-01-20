import aiohttp
from loguru import logger
import asyncio
from googletrans import Translator


from config import OW_API_KEY, NINJAS_API_KEY, EDAMAM_APP_ID, EDAMAM_API_KEY

logger.add("logs.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO", rotation="100 MB")

async def get_city_temp(city: str) -> float | None:
    ''' Докстринга '''

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OW_API_KEY}&units=metric'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                current_temp = await response.json()
                logger.info(f'Success request to OpenWeather API with city={city}')
                return current_temp.get('main').get('temp')
            else:
                logger.error(f'OpenWeather API return code {response.status}')
            return None


def get_water_norm(weight: float, activity: int, city_temp: float | None = None) -> int:
    ''' Докстринга '''

    if city_temp:
        water_norm = int(weight * 30 + activity / 30 * 500 + [0, 500][city_temp > 25])
    else:
        water_norm = int(weight * 30 + activity / 30 * 500)

    return water_norm


def get_kallories_norm(weight: float, height: int, age: int, activity: int = 0) -> int:
    ''' Докстринга '''

    kallories_norm = int(10 * weight + 6.25 * height - 5 * age + 5 * activity)
    return kallories_norm


async def get_food_kalories(food: str) -> int:
    ''' Докстринга '''

    async with Translator() as translator:
        food = await translator.translate(food)
        food = food.text + ' 100g'

    url = f'https://api.edamam.com/api/nutrition-data'
    params = {'app_id': EDAMAM_APP_ID, 'app_key': EDAMAM_API_KEY, 
              'nutrition-type': 'logging', 'ingr': food}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                kalories = await response.json()
                logger.info(f'Success request to Edamam API with food={food}')
                return kalories.get('calories')
            else:
                logger.error(f'Edamam API return code {response.status}')
            return None

'''
async def get_workout(activity: str, duration: int, weight: int = 70) -> int:
    base_url = f'https://api.api-ninjas.com/v1/caloriesburned?activity={activity}&weight={weight}&duration={duration}'
    headers = {'X-Api-Key': NINJAS_API_KEY}

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            workout = await response.json()
            # burned_calor/=ies = int(workout)
            print(workout)

    return workout#burned_calories
'''
