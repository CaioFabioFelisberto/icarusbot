import time
import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from google import genai
from google.genai import types

from src.keyboards.menu import get_main_menu_markup, get_back_markup, build_todo_keyboard
from src.services.weather import get_weather
from src.services.money import get_financial_summary
from src.services.news import get_latest_news
from src.services.gemini import send_message_to_gemini
from src.services.todo import add_task, get_tasks, toggle_task, delete_task

import dotenv
import os

dotenv.load_dotenv()

bot = AsyncTeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
ai_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

user_states = {}
user_chats = {}


@bot.message_handler(commands=['start'])
async def start(msg):
    await bot.reply_to(msg, "Olá! Eu sou um bot amigável que pode conversar e fornecer diversas informações. Use o comando /menu para ver as opções disponíveis.")

@bot.message_handler(commands=['help'])
async def help(msg):
    await bot.reply_to(msg, "Aqui estão os comandos disponíveis:\n\n"
                       "/start - Inicia o bot e mostra uma mensagem de boas-vindas.\n"
                       "/help - Exibe esta mensagem de ajuda.\n"
                       "/menu - Mostra o menu principal com as opções disponíveis.\n"
                       "/task <descrição> - Adiciona uma nova tarefa.\n"
                       "/tasks - Exibe a lista de tarefas.")

@bot.message_handler(commands=['menu'])
async def show_menu(msg):
    await bot.send_message(
        msg.chat.id, 
        "Escolha uma opção:", 
        reply_markup=get_main_menu_markup()
    )

@bot.message_handler(commands=['task','tarefa'])
async def handle_add_task(msg):
    """Adiciona uma nova tarefa para o usuário."""
    task_text = msg.text.replace('/task', '').replace('/tarefa', '').strip()

    if not task_text:
        await bot.reply_to(msg, "Por favor, forneça a descrição da tarefa após o comando. Exemplo: /task Comprar leite")
        return
    add_task(msg.chat.id, task_text)
    await bot.reply_to(msg, f"Tarefa adicionada: {task_text}")

@bot.message_handler(commands=['tasks', 'tarefas'])
async def handle_list_tasks(msg):
    """Exibe a lista interativa de tarefas do usuário."""
    chat_id = msg.chat.id
    tasks = get_tasks(chat_id)
    
    if not tasks:
        await bot.reply_to(msg, "🎉 Você não tem tarefas pendentes! Use `/task <descrição>` para adicionar uma.", parse_mode="Markdown")
        return
        
    markup = build_todo_keyboard(chat_id)
    await bot.send_message(
        chat_id, 
        "📝 **Sua Lista de Tarefas:**\nClique para alternar o status ou ❌ para excluir.", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('todo_'))
async def handle_todo_callbacks(call):
    chat_id = call.message.chat.id
    await bot.answer_callback_query(call.id)
    
    action, idx_str = call.data.replace('todo_', '').split('_')
    idx = int(idx_str)
    
    if action == 'toggle':
        toggle_task(chat_id, idx)
    elif action == 'del':
        delete_task(chat_id, idx)
        
    # Atualiza a mensagem com a lista renovada
    tasks = get_tasks(chat_id)
    if tasks:
        markup = build_todo_keyboard(chat_id)
        await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=markup)
    else:
        await bot.edit_message_text("🎉 Todas as tarefas foram concluídas ou removidas!", chat_id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: True)
async def callback_listener(call):
    await bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "opt_1":
        user_states[chat_id] = 'awaiting_city'
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Digite o nome da cidade para ver a previsão do clima:",
            reply_markup=get_back_markup()
        )

    elif call.data == "opt_2":
        financial_summary = get_financial_summary()
        await bot.send_chat_action(chat_id, 'typing')
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=financial_summary,
            parse_mode='Markdown',
            reply_markup=get_back_markup()
        )

    elif call.data == "opt_3":
        news_info = await get_latest_news()
        await bot.send_chat_action(chat_id, 'typing')
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=news_info,
            parse_mode='Markdown',
            reply_markup=get_back_markup()
        )

    elif call.data == "btn_back":
        # Cancela o estado de espera por cidade se o utilizador clicar em voltar
        user_states.pop(chat_id, None)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Escolha uma opção:",
            reply_markup=get_main_menu_markup()
        )


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

@bot.message_handler(content_types=['voice'])
async def handle_gemini_voice(msg):
    await bot.send_chat_action(msg.chat.id, 'typing')

    chat_id = msg.chat.id

    if chat_id not in user_chats:
        user_chats[chat_id] = ai_client.chats.create(model='gemini-2.5-flash')

    chat_session = user_chats[chat_id]

    try:
        file_info = await bot.get_file(msg.voice.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        audio_part = types.Part.from_bytes(
            data=downloaded_file,
            mime_type="audio/ogg"
        )
        
        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(
            None,
            lambda: send_message_to_gemini(chat_session, [audio_part])
        )
        
        await bot.reply_to(msg, response_text, parse_mode='Markdown')
    except Exception as e:
        print(f"Erro no chat de voz do Gemini: {e}")
        await bot.reply_to(
            msg, 
            "Houve um erro ao processar sua mensagem de voz. Por favor, tente novamente mais tarde."
        )


if __name__ == "__main__":
    asyncio.run(bot.polling(non_stop=True))
