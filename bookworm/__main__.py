import signal
import asyncio


async def shutdown():  # pylint: disable=unused-argument
    """Try to shut down gracefully"""
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks)


async def main() -> int:
    while True:
        print("!!!")
        await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    signal.signal(signal.SIGINT, lambda _, __: asyncio.create_task(shutdown()))
    signal.signal(signal.SIGTERM, lambda _, __: asyncio.create_task(shutdown()))
    loop.call_later(0.3, lambda: print("###"))
    loop.run_until_complete(main())
