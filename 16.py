import asyncio
import aiohttp
from aiohttp import ClientSession
from util import async_timed


# Для правильного конкурентного выполнения допускающих ожидание (Awaitable) объектов широко используется функция asyncio.gather. Она принимает последовательность допускающих
# ожидание объектов и запускает их конкурентно всего в одной строке кода. Если среди объектов, переданных asyncio.gather() в качестве аргумента есть сопрограмма, то gather автоматически обертывает
# её задачей, чтобы гарантировать конкурентное выполнение.
# asyncio.gather возвращает Awaitable объект.
# используя конструкцию await asyncio.gather(objects) вызывающая сопрограмма приостановится до завершения работы сопрограмм в objects, до того момента
# когда asyncio.gather вернет список результатов работы.


# Есть одна проблема: при использовании gather могут возникнуть проблемы - вызов исключений.
# Обработка исключений при использовании gather:

#
#



async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls] # Сгенерировать список сопрограмм для каждого запроса, который мы хотим отправить
        status_codes = await asyncio.gather(*requests) # Ждать завершения всех запросов
        print(status_codes)


asyncio.run(main())
