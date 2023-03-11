import asyncio
from util import delay

# Иногда возникает необходимость в том, чтобы не снимать задачу по истечению тайм-аута.
# Чтобы это реализовать, нужно:
#  1. Ту сопрограмму (корутину), которую мы собираемся ожидать, необходимо обернуть в задачу (asyncio.create_task(coroutine()))
#  2. Передать в asyncio.wait_for не саму задачу, а задачу, обернутую в asyncio.shield()
#
# Таким образом мы защитим нашу задачу от снятия по завершению таймера и получим доступ к задаче task внутри блока except
# Обсуждение о том как это работает будет позже, на данный момент важно знать, что этот механизм просто есть.

async def main():
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5) # result = await asyncio.wait_for(asyncio.shield(task), timeout=5)
        print(result)
    except:
        print("Задача заняла более 5 c, скоро она закончится !")
        result = await task
        print(result)


asyncio.run(main())