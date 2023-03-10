import asyncio

# Знакомство с задачами
# Все ожидающие задачи начинают своё выполнение при встрече первого предложения await после объявления задачи.
# Программа Python бездействует во время ожидания delay(3), поэтому мы запустим в это время сопрограмму hello_every_second()
# Общее время работы их займет не более 3 секунд

async def delay(delay_seconds):
    print(f'Братишка, я пока подремлю, не обессуть, дорогой, {delay_seconds} сек')
    await asyncio.sleep(delay_seconds)
    print(f'Вааааайааа, асаламалекум !!')
    return "Че за тяги такие бархатные ? Уффф... Кефтеме !"


async def hello_every_second():
    for i in range(2):
        await asyncio.sleep(1)
        print("пока я жду, исполняется другой код !")


async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))

    await hello_every_second()
    await first_delay
    await second_delay

# Также попробуйте запустить вот эти main корутины:

async def main1():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))

    await hello_every_second()
    # await first_delay
    # await second_delay


async def main2():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))

    await hello_every_second()
    await first_delay
    # await second_delay

if __name__ == "__main__":
    asyncio.run(main())