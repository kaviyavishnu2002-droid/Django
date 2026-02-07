import asyncio
import time
import threading
from multiprocessing import Process

from django.http import JsonResponse

# def task():
#     time.sleep(2)
#     print("Task completed")
# if __name__ == "__main__":
#     p1 = Process(target=task)
#     p2 = Process(target=task)
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

# def task1(name):
#     time.sleep(2)
#     print(f"{name} completed")
# t1 = threading.Thread(target=task1, args=("Task 1",))
# t2 = threading.Thread(target=task1, args=("Task 2",))
# t1.start()
# t2.start()
# t1.join()
# t2.join()

async def task2(name):
    print(f"{name} started")
    # time.sleep(3)   # BLOCKS event loop
    await asyncio.sleep(2)  # # Non-blocking
    print(f"{name} resumed")
    await asyncio.sleep(1)
    print(f"{name} finished")
# async def main():
#     await asyncio.gather(
#         task2("Task A"),
#         task2("Task B")
#         return_exceptions=True  #Error Handling with gather and Use in Django APIs to avoid crashing requests
#     )
#     t3 = asyncio.create_task(task2("Task C"))
#     t4 = asyncio.create_task(task2("Task D"))
#     await t3
#     await t4
# asyncio.run(main())
# asyncio.wait() (Advanced Control)

# Wait for tasks with fine-grained control.
# tasks = {asyncio.create_task(coro1()),
#          asyncio.create_task(coro2())}
# done, pending = await asyncio.wait(
#     task,
#     timeout=3,   # Maximum wait time
#     return_when=asyncio.FIRST_COMPLETED
# )
# FIRST_COMPLETED	Return when any one task finishes
# FIRST_EXCEPTION	Return when any task raises an exception
# ALL_COMPLETED	Return when all tasks finish (default)

async def slow():
    await asyncio.sleep(5)
async def fast():
    await asyncio.sleep(1)

async def main3():
    tasks = {
        asyncio.create_task(slow()),
        asyncio.create_task(fast())
    }
    done, pending = await asyncio.wait(
        tasks,
        timeout=3,
        return_when=asyncio.FIRST_COMPLETED
    )
    print(f"done is {done}")
    print(f"pending is {pending}")
asyncio.run(main3())

# try:
#     async with asyncio.TaskGroup() as tg:
#         tg.create_task(task2())
#         tg.create_task(task2())
# except* ValueError as eg:
#     print("Handled ValueError:", eg)

# Real Django Example (Safe Pattern)
async def dashboard_view(request):
    user_task = asyncio.create_task(task2())
    stats_task = asyncio.create_task(task2())

    user, stats = await asyncio.gather(user_task, stats_task)

    return JsonResponse({"user": user, "stats": stats})

'''
# ❌ Sequential (Slow)
await task1()
await task2()

✅ Concurrent (Fast)
await asyncio.gather(
    task1(),
    task2()
)
'''

async def main2():
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    loop.call_later(7, future.set_result, "Hello Future")

    result = await future
    print(result)

asyncio.run(main2())

# Cancelling Tasks
# task.cancel()

# Timeouts with Tasks
# await asyncio.wait_for(fetch(), timeout=3)

# async def api_view(request):
#     task1 = asyncio.create_task(fetch_user())
#     task2 = asyncio.create_task(fetch_orders())
#     user, orders = await asyncio.gather(task1, task2)
#     return JsonResponse({"user": user, "orders": orders})

