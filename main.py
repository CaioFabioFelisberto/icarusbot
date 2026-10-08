import asyncio
import os
import logging
import dotenv

from telebot.async_telebot import AsyncTeleBot
from google import genai

from src.services import setup_logger
from src.handlers import register_all_handlers
from src.services import start_scheduler

dotenv.load_dotenv()

setup_logger()

bot = AsyncTeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
ai_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

user_states = {}
user_chats = {}

register_all_handlers(bot, ai_client, user_chats, user_states)

async def main():
    logging.info("IcarusBot v2.1 iniciado com sucesso!")
    asyncio.create_task(start_scheduler(bot))
    await bot.polling(non_stop=True)

if __name__ == "__main__":
    asyncio.run(main())