import asyncio
import requests
from util import async_timed


# Ловушки сопрограмм и задач, часть 1.
# Вторая ошибка на пути преобразования приложения в асинхронное - использование блокирующего API ввода-вывода, пренебрегая многопоточностью
# Большинство API, с  которыми мы обычно работаем, в  настоящее время являются блокирующими и без доработок работать с asyncio не будут
# Нужно использовать библиотеку, которая поддерживает сопрограммы и неблокирующие сокеты. А это значит, что если используемая вами библиотека не возвращает сопрограммы и
# вы не употребляете await в собственных сопрограммах, то, вероятно, совершаете блокирующий вызов.
# В данном примере мы использовали библиотеку requests, вместо неё нам следовало бы использовать библиотеку aiohttp, в которой используются неблокирующие сокеты и которая возвращает сопрограммы, тогда с конкурентностью было бы все нормально.


@async_timed()
async def get_example_status() -> int:
    return requests.get("http://www.example.com").status_code


@async_timed()
async def main():
    task_1 = asyncio.create_task(get_example_status())
    task_2 = asyncio.create_task(get_example_status())
    task_3 = asyncio.create_task(get_example_status())

    await task_1
    await task_2
    await task_3

asyncio.run(main())
