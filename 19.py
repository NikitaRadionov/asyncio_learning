import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed

# В 18.py было обсуждение timeout у  asyncio.as_completed()
# Первый недостаток asycnio.as_completed заключается в том, что мы не можем ассоциировать результаты работы с задачами
# Второй недостаток заключается в том, что после истечения тайм-аута, все созданные задачи продолжат работать в фоновом режиме

# Поэтому нам нужный более точный контроль выполнения.
# gather и as_completed имеют сложности со снятием задач, работавших в момент исключения.
# as_completed свойственен недетерминированный порядок получения результатов, из-за чего трудно понять, какая именно задача завершилась.
# Нам нужно точно знать, какие awaitable objects уже завершились, а какие ещё нет, а также мы хотим ассоциировать результаты работы задач с самими задачами.
# Для этих целей asyncio предоставляет функцию wait

# функция asyncio.wait возвращает два множества: задачи, завершившиеся успешно или в результате исключения, а также задачи, которые продолжают выполняться.
# стандартный вызов:
# asyncio.wait(awaitable_objects, timeout=..., return_when=[ALL_COMPLETED, FIRST_COMPLETED, FIRST_EXCEPTION,])
# по умолчанию return_when = ALL_COMPLETED

# Если return_when = ALL_COMPLETED то asyncio.wait ждет завершения всех задач и только потом возвращает управление.


async def fetch_status(session: ClientSession, url: str):
    async with session.get(url) as result:
        return result.status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'https://example.com')),
            asyncio.create_task(fetch_status(session, 'https://example.com')),
        ]
        done, pending = await asyncio.wait(fetchers)

        print(f'Число завершившихся задач: {len(done)}')
        print(f'Список done: {done}')
        print()
        print(f'Число ожидающих задач: {len(pending)}')
        print(f'Список pending: {pending}')

        for done_task in done:
            result = await done_task
            print(result)

asyncio.run(main())

# Здесь мы конкурентно выполняем два веб-запроса, передавая wait
# список задач. Предложение await wait вернет управление, когда все
# запросы завершатся, и мы получим два множества: завершившиеся задачи и еще работающие задачи.
# Множество done содержит все задачи, которые завершились успешно или в  результате исключения,
# а множество pending – еще не завершившиеся задачи. В данном случае мы задали режим ALL_COMPLETED,
# поэтому множество pending будет пустым, так как asyncio.wait не вернется, пока все не завершится.

# Если в одном из запросов возникнет исключение, то asyncio.wait не возбудит его, как asyncio.gather.
# Мы получим оба множества done и pending, но не увидим исключения, пока не применим await к той задаче из done, где имела место ошибка.
