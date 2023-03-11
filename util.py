import asyncio
import time
import functools
from typing import Callable, Any

async def delay(delay_seconds):
    print(f'Братишка, я пока подремлю, не обессуть, дорогой, {delay_seconds} сек')
    await asyncio.sleep(delay_seconds)
    print(f'Вааааайааа, асаламалекум !!')
    return "Че за тяги такие бархатные ? Уффф... Кефтеме !"



def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"выполняется {func} c аргументами {args} {kwargs}")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f"{func} завершилась за {total:.4f} c")
        return wrapped

    return wrapper