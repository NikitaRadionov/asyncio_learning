import time
import functools
from typing import Callable, Any

# Мы хотим измерять время работы корутины, с этой целью напишем декоратор и в деталях разберем как это делается.

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



# Перенесем его в файл util.py
