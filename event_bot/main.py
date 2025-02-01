import logging
import asyncio
from bot import dp,bot

logging.basicConfig(level=logging.INFO)

#main function to start the bot
async def main():
    try:
        await dp.start_polling(bot)
        logging.info("Polling...")
    except Exception as e:
        logging.error(f"Error: {e}")


#check if the script is run directly
if __name__ == "__main__":
    asyncio.run(main())