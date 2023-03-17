import asyncio
import aiohttp
import logging
from aiohttp import ClientSession
from util import async_timed




# Пока мы ждем завершения сопрограмм, может возникнуть сколько угодно исключений, но мы их не увидим, пока все задачи не
# завершатся. Это может стать проблемой, если после первого же исключения следует снять все остальные выполняющиеся запросы.
# Чтобы эту проблему решить, нужно установить параметр return_when функции asyncio.wait в значение FIRST_EXCEPTION
# Если return_when=FIRST_EXCEPTION, то мы получаем два разных поведения в зависимости от того, возникает в какой-то задаче исключение или нет.

# 1. Ни один Awaitable obj не возбудил исключения:
# Если ни в одной задаче не было исключений, то этот режим эквивалентен
# ALL_COMPLETED. Мы дождемся завершения всех задач, после чего множество done будет содержать все задачи,
# а множество pending останется пустым.

# 2. В одной или нескольких задачах возникло исключение:
# Если хотя бы в одной задаче возникло исключение, то wait немедленно
# возвращается. Множество done будет содержать как задачи, завершившиеся успешно, так и те, в которых имело место исключение.
# Гарантируется, что done будет содержать как минимум одну задачу – завершившуюся
# ошибкой, но может содержать и  какие-то успешно завершившиеся задачи.
# Множество pending может быть пустым, а может содержать задачи, которые продолжают выполняться. Мы можем использовать его для
# управления выполняемыми задачами по своему усмотрению



async def fetch_status(session: ClientSession, url: str, delay=0):
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'python://bad.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3)),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3))
        ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("При выполнении запроса возникло исключение", exc_info=done_task.exception())

        for pending_task in pending:
            pending_task.cancel()

asyncio.run(main())


# Приложение не заняло почти никакого времени, потому что мы быстро отреагировали на то, что один из запросов возбудил исключение;
# прелесть этого режима в том, что реализуется тактика быстрого отказа, т. е. быстрой реакции на возникающие проблемы.