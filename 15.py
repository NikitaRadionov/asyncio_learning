import asyncio
import aiohttp
from aiohttp import ClientSession

# При работе с веб-запросами используется понятие сеанса.
# Внутри сеанса хранится много открытых подключений, их можно при необходимости использовать повторно. Это множество подключений называется пулом подключений.
# В большинстве приложений на базе aiohttp создается один сеанс для всего приложения.
# Объект сеанса передается методам.
# У объекта сеанса есть методы для отправки веб-запросов, в том числе GET, PUT и POST.
# Для создания сеанса используется синтаксис async with и асинхронный контекстный менеджер aiohttp.ClientSession

async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


async def main():
    async with aiohttp.ClientSession() as session: # Открыть сессию (сеанс). Сессия (сеанс) позволяет создавать подключения. По умолчанию можно создать не более 100 подключений. Чтобы изменить максимальное количество подключений, нужно посмотреть на TCPConnector
        url = 'https://www.example.com'
        status = await fetch_status(session, url)
        print(f'status code for {url} is {status}')

asyncio.run(main())