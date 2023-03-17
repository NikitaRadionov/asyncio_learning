import asyncio
import aiohttp
import logging
from aiohttp import ClientSession
from util import async_timed

# Обработка ошибок в asyncio.wait :

# у нас на выбор есть несколько способов обработать исключения.
# Можно выполнить await и дать возможность исключению распространиться выше,
# можно выполнить await, обернуть его в блок try/except, чтобы обработать исключение,
# можно воспользоваться методами task.result() и task.exception().
# Вызывать эти методы task.result() и task.exception()  безопасно,
# поскольку в множестве done гарантированно находятся завершенные задачи; иначе их вызов привел бы к исключению.
# Предположим, что мы не хотим возбуждать исключение и обрушивать свое приложение. Вместо этого мы хотим напечатать результат
# задачи, если он получен, или запротоколировать ошибку в случае исключения. В таком случае вполне подойдет использование методов
# объекта Task. Посмотрим, как их использовать для обработки исключений.

async def fetch_status(session: ClientSession, url: str):
    async with session.get(url) as result:
        return result.status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://www.example.com')
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [
            asyncio.create_task(good_request),
            asyncio.create_task(bad_request)
        ]

        done, pending = await asyncio.wait(fetchers)

        print(f"Число завершившихся задач: {len(done)}")
        print(f"Число ожидающих задач: {len(pending)}")

        for done_task in done:
            # result = await done_task
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("При выполнении запроса возникло исключение", exc_info=done_task.exception())

asyncio.run(main())


# Функция done_task.exception() проверяет, имело ли место исключение. Если нет, то можно получить результат из done_task методом result.
# Здесь также было бы безопасно написать result = await done_task, хотя при этом может возникнуть исключение, чего мы,
# возможно, не желаем. Если результат exception() не равен None, то в Awaitable obj возникло исключение и его можно
# обработать, как нам угодно. В данном случае просто печатаем стек вызовов в момент исключения.