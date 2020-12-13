import asyncio
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

async def waiter(seconds: int):
    await asyncio.sleep(seconds)
    return 42


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(waiter(5))

    while True:
        logging.info("Hello")
        time.sleep(1)


if __name__ == "__main__":
    main()
