import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


# Ранее мы говорили, что wait принимает любые Awaitable objects, но это не так.
# Каждую сопрограмму мы оборачивали в задачу и только лишь после этого мы передавали их функции asyncio.wait()
# Зачем оборачивать сопрограммы в задачи при использовании asyncio.wait ?

# Ответим на этот вопрос на примере:
# Пусть имеется два запроса к разным API, которые назовем API A и API B. Оба могут тормозить, но наше приложение может продолжить работу, не получив результата от API B,
# просто было бы хорошо его иметь. Мы хотим, чтобы приложение было отзывчивым, поэтому задаем для запросов тайм-аут в 1 с. Если по истечении тайм-аута запрос к API B еще работает, то
# мы отменяем его. Посмотрим, что произойдет, если реализовать эту идею, не обертывая сопрограммы задачами.




async def fetch_status(session: ClientSession, url: str, delay: int = 0):
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        api_a = fetch_status(session, url)
        api_b = fetch_status(session, url, delay=2)

        done, pending = await asyncio.wait([api_a, api_b], timeout=1)

        for task in pending:
            if task is api_b:
                print('API B слишком медленный, отмена')
                task.cancel()

asyncio.run(main())


# Мы ожидаем, что этот код напечатает «API B слишком медленный, отмена», но на самом деле мы его вообще не увидим.
# Такое может случиться, потому что, когда в wait передаются просто сопрограммы, они
# автоматически обертываются задачами, а возвращенные множества
# done и pending будут содержать эти задачи.
# Это значит, что сравнения на предмет присутствия задачи в множестве pending, как в предложении if task is api_b, неправомерны,
# потому что мы сравниваем разные объекты: сопрограмму и задачу.
# Но если обернуть fetch_status задачей, то новые объекты не создаются и сравнение if task is api_b
# будет работать, как мы и ожидаем