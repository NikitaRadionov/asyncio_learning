import asyncio
from util import delay, async_timed


# Ловушки сопрограмм и задач, часть 1.
# Первая ошибка на пути преобразования приложения в асинхронное - попытка выполнить счетный код (код, который завязан на работе процессора) в задачах или сопрограммах, не прибегая к многопроцессорности
# Мы можем в этом убедться просто создав сопрограмму (корутину), которая будет просто считать счетчик. Обернуть эту корутину в задачу и попытаться как мы всегда стандартно делали исполнить эти задачи
# асинхронно путем встречи с первым предложением await.
# Как мы видим у нас будет выполнена сначала задача 1, а только затем будет выполнена задача 2.
# Значит время работы будет складываться из двух обращений к cpu_bound_work

@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter


@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    await task_one
    await task_two

asyncio.run(main())


# Если мы попробуем асинхронно выполнить io bound сопрограмму вместе с cpu bound сопрограммой, то никакой асинхронности мы не получим, и всего лишь
# задачи исполнятся последовательно.

@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work()) # cpu bound
    task_two = asyncio.create_task(cpu_bound_work()) # cpu bound
    delay_task = asyncio.create_task(delay(4)) # io bound

    await task_one
    await task_two
    await delay_task

asyncio.run(main())