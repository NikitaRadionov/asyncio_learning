import asyncio

# Знакомство с задачами
# Все ожидающие задачи начинают своё выполнение при встрече первого предложения await после объявления задачи.
# В этом коде мы создадим три обертки для сопрограммы delay т.е три задачи delay и будем исполнять их конкурентно.
# Общее время работы их займет не более 3 секунд

async def delay(delay_seconds):
    print(f'Братишка, я пока подремлю, не обессуть, дорогой, {delay_seconds} сек')
    await asyncio.sleep(delay_seconds)
    print(f'Вааааайааа, асаламалекум !!')
    return "Че за тяги такие бархатные ? Уффф... Кефтеме !"

async def main():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))

    await sleep_for_three
    await sleep_again
    await sleep_once_more


if __name__ == "__main__":
    asyncio.run(main())