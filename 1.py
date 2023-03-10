import asyncio

# creating base couroutine
# Создание первой сопрограммы (корутины) с использованием синтаксиса async/await

async def my_first_coroutine(a: int) -> int:
    return a ** 2

print(type(my_first_coroutine)) # <class 'function'>
object = my_first_coroutine(4)
print(type(object)) # <class 'coroutine'>

result = asyncio.run(my_first_coroutine(4))
print(result)



# asyncio.run(my_first_coroutine(4))