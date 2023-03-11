import asyncio
from asyncio import CancelledError
from util import delay

# Снятие задач
# У каждого объекта задачи есть метод cancel, который можно вызвать, если требуется остановить задачу.
# В результате снятия задача возбудит исключение CancelledError, когда мы ждем её с помощью await.
# Важно отметить, что исключение CancelledError может быть возбуждено только внутри предложения await.
# Если вызвать метод cancel, когда задача исполняет Python код, этот код будет продолжать работать, пока не встретится следующее предложение await
# и только тогда будет возбуждено исключение CancelledError.
# Вызов cancel не прерывает задачу, делающую своё дело. Он снимает её, только если она уже находится в точке ожидания или когда дойдет до следующей такой точки.

# Для того, чтобы понять что здесь написано, попробуйте запустить сначала main(), затем main1(), после main2()


async def main():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0

    while not long_task.done():
        print('Задача не закончилась, следующая проверка через секунду.')
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 5:
            long_task.cancel()

    try:
        await long_task
    except CancelledError:
        print('Наша задача была снята')


async def main1():
    long_task = asyncio.create_task(delay(10))

    await asyncio.sleep(2)

    long_task.cancel()

    await long_task


async def main2():
    long_task = asyncio.create_task(delay(10))

    # await asyncio.sleep(2)

    long_task.cancel()

    await long_task




asyncio.run(main())
# asyncio.run(main1())
# asyncio.run(main2())