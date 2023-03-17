import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


# Тайм-ауты в сочетании с as_completed.
# Функция as_completed предоставляет возможность таймаутов для группы запросов с помощью необязательного параметра timeout, равного величине тайм-аута в секундах.
# timeout управляет временем работы as_completed. Если потребуется больше времени, чем задано в timeout, то каждый awaitable object, который не доработал до конца, возбудит исключение TimeoutException
# в точке ожидания с помощью await.

# @async_timed()
async def fetch_status(session, url, delay):
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://example.com', 1),
            fetch_status(session, 'https://example.com', 10),
            fetch_status(session, 'https://example.com', 10)
        ]
        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print("Произошел тайм-аут")

        for task in asyncio.tasks.all_tasks():
            print(task)

asyncio.run(main())


# as_completed справляется со своей задачей – возвращать результат по мере поступления,
# но она не лишена недостатков. Первый заключается в том, что хотя мы и получаем результаты в темпе их поступления,
# но невозможно сказать, какую сопрограмму или задачу мы ждем, поскольку порядок абсолютно не детерминирован
# Если порядок нас не волнует, то и ладно, но если требуется ассоциировать результаты с запросами, то возникает проблема

# Второй недостаток в том, что, хотя исключения по истечении таймаута возбуждаются как положено, все созданные задачи продолжают
# работать в  фоновом режиме. А  если мы захотим их снять, то будет
# трудно понять, какие задачи еще работают. Вот вам и еще одна проблема! Если эти проблемы требуется решить, то нужно точно знать,
# какие допускающие ожидание объекты уже завершились, а какие еще
# нет. Поэтому asyncio предоставляет функцию wait.