import aiohttp
from loguru import logger

from config import OW_API_KEY

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