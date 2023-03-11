import asyncio
from util import delay

# Задание тайм-аутов
# В 6.py мы каждую секунду проверяли состояние задачи, и если проходило более 5 секунд, то снимали задачу. Очевидно, это не самый простой способ задания тайм-аутов.
# В asyncio есть функция asyncio.wait_for . Она принимает объект сопрограммы (корутины) или задачи и тайм-аут в секундах и возвращает сопрограмму (корутину), к которой можно
# применить await . Если задача не завершилась в отведенное время, то возбуждается исключение TimeoutError и задача автоматически снимается.

async def main():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=3)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("Тайм-аут !")
        print(f"Задача была снята ? {delay_task.cancelled()}")


async def main1():
    delay_task = asyncio.create_task(delay(2))
    result = await asyncio.wait_for(delay_task, timeout=1)

asyncio.run(main())
# asyncio.run(main1())