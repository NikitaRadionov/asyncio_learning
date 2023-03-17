import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed



# Обработка тайм-аутов с помощью asyncio.wait:

# Функция wait позволяет не только точнее контролировать порядок ожидания задач, но и задавать время,
# в течение которого все допускающие ожидание объекты должны завершиться. Для этого нужно
# задать параметр timeout, указав в нем максимальное время работы
# в секундах. Между обработкой тайм-аутов wait и ранее рассмотренными wait_for и as_completed есть два отличия.

# 1. Сопрограммы не снимаются.
# Если мы хотим снять спорграммы из-за тайм-аута, то должны явно обойти их и снять каждую

# 2. Исключения не возбуждаются.
# wait не возбуждает исключения в случае тайм-аута.
# Когда случается исключение, wait возвращает все завершившиеся заадчи, а также те, что ещё не завершились в момент тайм-аута.


# Например, рассмотрим случай, когда два запроса завершаются быстро, а третий занимает несколько секунд. Мы зададим в wait
# тайм-аут 1 с, чтобы понять, что происходит, когда задачи не успевают завершиться. Параметр return_when пусть принимает значение по
# умолчанию ALL_COMPLETED.


async def fetch_status(session: ClientSession, url: str, delay: int = 0):
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, delay=3)),
        ]

        done, pending = await asyncio.wait(fetchers, timeout=1)


        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)

asyncio.run(main())

# Здесь wait вернет множества done и pending через 1 с.
# В множестве done будет два быстрых запроса, поскольку они успевают завершиться
# за это время. А  медленный запрос еще работает, поэтому окажется
# в множестве pending. Затем мы ждем задачи из done с помощью await
# и получаем возвращенные ими значения. При желании можно было
# бы снять задачу, находящуюся в pending

# Задачи в множестве pending не сняты и продолжают работать, несмотря на тайм-аут.
# Если в конкретной ситуации требуется завершить еще выполняющиеся задачи, то следовало бы явно обойти множество pending
# и вызвать для каждой задачи cancel