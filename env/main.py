import asyncio
from Dispatcher import dispatcher
from TelegramBot import bot
import logging
import sys


async def main() -> None:
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    asyncio.run(main())
