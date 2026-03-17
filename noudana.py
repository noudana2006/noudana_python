import asyncio
import time
from functools import wraps

# ---- Retry Decorator ----
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    await asyncio.sleep(delay)
        return wrapper
    return decorator


# ---- Simple Async Cache ----
class AsyncCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        value = self.cache.get(key)
        if value and value["expiry"] > time.time():
            return value["data"]
        return None

    def set(self, key, data, ttl=5):
        self.cache[key] = {
            "data": data,
            "expiry": time.time() + ttl
        }


# ---- Task Scheduler ----
class TaskScheduler:
    def __init__(self, workers=3):
        self.queue = asyncio.Queue()
        self.workers = workers
        self.cache = AsyncCache()

    async def worker(self, worker_id):
        while True:
            task_name, coro, args = await self.queue.get()
            print(f"[Worker {worker_id}] Running {task_name}")

            try:
                result = await coro(*args)
                print(f"[Worker {worker_id}] Result: {result}")
            except Exception as e:
                print(f"[Worker {worker_id}] Failed: {e}")

            self.queue.task_done()

    async def run(self):
        workers = [
            asyncio.create_task(self.worker(i))
            for i in range(self.workers)
        ]
        await self.queue.join()
        for w in workers:
            w.cancel()

    async def schedule(self, name, coro, *args):
        cache_key = f"{name}:{args}"
        cached = self.cache.get(cache_key)

        if cached:
            print(f"[CACHE HIT] {cache_key} -> {cached}")
            return cached

        async def wrapper(*args):
            result = await coro(*args)
            self.cache.set(cache_key, result)
            return result

        await self.queue.put((name, wrapper, args))


# ---- Example Tasks ----
@retry(max_attempts=3, delay=1)
async def unstable_task(x):
    await asyncio.sleep(1)
    if x % 2 == 0:
        raise ValueError("Random failure for even numbers")
    return x * x


async def slow_fibonacci(n):
    await asyncio.sleep(0.5)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ---- Main Execution ----
async def main():
    scheduler = TaskScheduler(workers=3)

    tasks = [
        scheduler.schedule("square", unstable_task, i)
        for i in range(6)
    ]

    tasks += [
        scheduler.schedule("fib", slow_fibonacci, i)
        for i in range(8)
    ]

    await asyncio.gather(*tasks)
    await scheduler.run()


if __name__ == "__main__":
    asyncio.run(main())