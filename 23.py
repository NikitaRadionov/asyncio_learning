import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


# Описанный подход в 22.py позволяет реагировать, как только завершится первая задача.
# Но что, если мы хотим обработать и остальные результаты по мере поступления, как при использовании as_completed?
# Предыдущий пример легко можно модифицировать, так чтобы задачи из множества pending обрабатывались в цикле, пока там ничего не
# останется. Тогда мы получим поведение, аналогичное as_completed, с тем дополнительным преимуществом, что на каждом шаге точно
# знаем, какие задачи завершились, а какие еще работают.

async def fetch_status(session: ClientSession, url: str):
    async with session.get(url) as result:
        return result.status



@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]

        while pending:
            done, pending = await asyncio.wait(pending,
                                               return_when=asyncio.FIRST_COMPLETED)

            print(f'Число завершившихся задач: {len(done)}')
            print(f'Число ожидающих задач: {len(pending)}')

            for done_task in done:
                print(await done_task)

asyncio.run(main())


# Здесь мы создаем множество pending и инициализируем его задачами, которые хотим выполнить.
# Цикл while выполняется, пока в pending остаются элементы, и на каждой итерации мы вызываем
# wait для этого множества. Получив результат от wait, мы обновляем
# множества done и pending, а затем печатаем завершившиеся задачи.
# Получается поведение, похожее на as_completed, с тем отличием, что
# теперь мы лучше знаем, какие задачи завершились, а какие продолжают работат