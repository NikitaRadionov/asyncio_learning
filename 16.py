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

# Детерменированность - определяемость.
# Детерминированность в решении какой-либо практической задачи или в алгоритме означает, что способ решения задачи определён однозначно в виде последовательности шагов.
# На любом шаге не допускаются никакие двусмысленности или недомолвки.

# Вызов asyncio.gather(a, b) недетерминирован. Потому что если a и b переданы именно в таком порядке, то это не означает что a завершится раньше чем b и наоборот.
# Но, независимо от того в каком порядке были переданы awaitable объекты a и b, результат гарантированно будет возвращен в том порядке, в каком объекты передавались.




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

# asyncio.run(main())

# Есть одна проблема: при использовании gather могут возникнуть проблемы - вызов исключений.
# Если с помощью gather мы будем делать запросы на сервер, то может случиться так, что сервер может оказаться недоступен, или может отказать в подключении. В таком случае
# возникнет исключение, которое нужно будет обработать.
# Обработка исключений при использовании gather:
#
# asyncio.gather() принимает необязательный параметр, return_exceptions, который позволяет указать, как мы хотим обрабатывать исключения от допускающих ожидание объектов.
# return_exceptions - булево значение.
# return_exceptions=False - режим по умолчанию. Если хотя бы одна сопрограмма возбуждает исключение, то gather возбуждает то же исключение в точке await.
# Но, даже если какая-то сопрограмма откажет, остальные не снимаются и продолжат работать при условии, что мы обработаем исключение и оно не приведет к остановке цикла событий и снятию задач.
# В точке await asyncio.gather() мы увидим только первое исключение.
#
# return_exceptions=True - в этом случае исключения возвращаются в том же списке, что результаты. Сам по себе вызов gather не возбуждает исключений, и мы можем обработать исключения как нам удобно.
# В этом случае будут возвращены все исключения, случившиеся во время выполнения сопрограмм.

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        tasks = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*tasks) # AssertionError
        print(status_codes)

# asyncio.run(main())


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        tasks = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f'Все результаты: {results}')
        print(f'Завершились успешно: {successful_results}')
        print(f'Завершились с исключением: {exceptions}')

asyncio.run(main())


# Как мы отмечали, первый недостаток asyncio.gather заключается в том, что нам не так просто отменить заданные задачи, если одна из них возбудила исключение.
# Если нам нужно отменить все запросы на сервер, если хотя бы один из них вызвал исключение, то использование gather не целесообразно.
# Второй недостаток gather заключается в том, что мы должны дождаться завершения всех сопрограмм, прежде чем можно будет приступить к обработке результатов.
# Если мы хотим обрабатывать результаты по мере поступления, то возникает проблема.
