import asyncio

# Знакомство с сопрограммой asyncio.sleep()
# Использование синтаксиса async/await не равно асинхронности (конкурентности)
# async def создает сопрограмму (корутину), которая основана на генераторе
# await это то же самое что и yield from в генераторе, это выражение передает управление подгенератору (подкорутине), и вернет управление только тогда, когда
# код в подгенераторе будет исполнен (а он может зависнуть или долго выполняться )
# await используется внутри сопрограммы, при его использовании сопрограмма приостанавливает свое выполнение полностью, пока await не вернет управление обратно.


async def to_sleep(seconds):
    await asyncio.sleep(seconds)
    return f'I was sleeping {seconds} seconds'

async def add_one(a:int) -> int:
    return a + 1

async def main():
    string = await to_sleep(3) # Приостановить main до возврата из to_sleep(3)
    result = await add_one(10) # Приостановить main до возврата из add_one(10)

    print(string)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())