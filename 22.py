import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


# Продолжаем обсуждение режимов return_when функции asyncio.wait

# У режимов ALL_COMPLETED и FIRST_EXCEPTION есть недостаток: если задачи не возбуждают исключений, то мы должны ждать, пока все они завершатся.
# При таких режимах, если мы хотим отреагировать на успешное завершение задачи немедленно, то у нас ничего не получится.

# return_when=FIRST_COMPLETED
# В  этом режиме wait возвращает управление, как только получен хотя бы один результат.
# Это может быть как успешно завершившаяся задача, так и задача, в которой возникло исключение.
# Остальные задачи можно либо снять, либо дать им возможность продолжать работу

# Продемонстрируем этот режим, для чего отправим несколько веб-запросов и обработаем тот, что закончится первым.


async def fetch_status(session: ClientSession, url: str):
    async with session.get(url) as result:
        return result.status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]

        done, pending = await asyncio.wait(fetchers,
                                           return_when=asyncio.FIRST_COMPLETED)

        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')

        for done_task in done:
            print(await done_task)

asyncio.run(main())


# Здесь мы конкурентно отправляем три запроса. Сопрограмма wait
# вернет управление, как только завершится любой из них.
# Следовательно, в done будет один завершившийся запрос, а в pending – еще работающие