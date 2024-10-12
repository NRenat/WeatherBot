import os

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from httpx import AsyncClient

from config import BASE_URL
from templates import HELLO_MESSAGE, WEATHER_ICONS, NOT_FOUND_LOCATION, SMTH_WRONG
from utils import degrees_to_direction

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(HELLO_MESSAGE)


async def get_weather(city):
    async with AsyncClient() as session:
        params = {
            'q': city,
            'APPID': os.getenv('OPEN_WEATHER_API'),
            'units': 'metric'
        }
        response = await session.get(BASE_URL, params=params)
        return response


@router.message()
async def get_weather_by_city(message: Message):
    response = await get_weather(message.text)
    weather = response.json()

    if weather.get('cod') == 200:
        weather_template = (
            f'<i>Today in <b>{weather.get('name')}</b>:</i>\n\n'
            f'{WEATHER_ICONS.get(weather.get('weather')[0].get('icon'))}'
            f' Weather: {weather.get('weather')[0].get('description').capitalize()}\n\n'
            f'🌡️ Temperature: {weather.get('main').get('temp')} °C\n'
            f'😳 Feels like {weather.get('main').get('feels_like')} °C\n'
            f'💧 Humidity: {weather.get('main').get('humidity')} %\n\n'
            f'💨 Wind speed: {weather.get('wind').get('speed')} m/s\n'
            f'🧭 Wind direction: {degrees_to_direction(weather.get('wind').get('deg'))}'
        )
        await message.answer(weather_template)
    elif int(weather.get('cod')) == 404:
        await message.answer(NOT_FOUND_LOCATION)
    else:
        await message.answer(SMTH_WRONG)
