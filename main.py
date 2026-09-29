import time
import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from google import genai

from src.services.weather import get_weather
from src.services.dollar import get_dollar_price
from src.services.news import get_latest_news
from src.services.gemini import send_message_to_gemini

import dotenv
import os

dotenv.load_dotenv()

bot = AsyncTeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
ai_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

user_states = {}
user_chats = {}


@bot.message_handler(commands=['start', 'help'])
async def start(msg):
    await bot.reply_to(msg, "Olá! Eu sou um bot amigável que pode conversar e fornecer diversas informações. Use o comando /menu para ver as opções disponíveis.")

@bot.message_handler(commands=['menu'])
async def show_menu(msg):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("Clima", callback_data="opt_1")
    btn2 = InlineKeyboardButton("Cotação do Dólar", callback_data="opt_2")
    btn3 = InlineKeyboardButton("Notícias", callback_data="opt_3")
    markup.add(btn1, btn2, btn3)
    await bot.send_message(msg.chat.id, "Escolha uma opção:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
async def callback_listener(call):
    await bot.answer_callback_query(call.id)
    if call.data == "opt_1":
        user_states[call.message.chat.id] = 'awaiting_city'
        await bot.send_message(
            call.message.chat.id, 
            "Digite o nome da cidade para ver a previsão do clima:"
        )
    elif call.data == "opt_2":
        dollar_info = get_dollar_price()
        await bot.send_message(call.message.chat.id, dollar_info, parse_mode='Markdown')
    elif call.data == "opt_3":
        await bot.send_message(call.message.chat.id, "Buscando as últimas notícias...")
        news_info = await get_latest_news()
        await bot.send_message(call.message.chat.id, news_info, parse_mode='Markdown')


@bot.message_handler(func=lambda msg: user_states.get(msg.chat.id) == 'awaiting_city')
async def process_weather_request(msg):
    user_states.pop(msg.chat.id, None)
    
    city = msg.text
    weather_info = get_weather(city)
    
    await bot.send_message(msg.chat.id, weather_info)

@bot.message_handler(func=lambda msg: True, content_types=['text'])
async def handle_gemini_chat(msg):
    await bot.send_chat_action(msg.chat.id, 'typing')

    chat_id = msg.chat.id

    if chat_id not in user_chats:
        user_chats[chat_id] = ai_client.chats.create(model='gemini-2.5-flash')

    chat_session = user_chats[chat_id]

    try:
        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(None, 
        lambda: send_message_to_gemini(chat_session, msg.text)
        )
        await bot.reply_to(msg, response_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Erro no chat do Gemini: {e}")
        await bot.reply_to(
            msg, 
            "Houve um erro ao processar sua mensagem. Por favor, tente novamente mais tarde."
        )


if __name__ == "__main__":
    asyncio.run(bot.polling(non_stop=True))
