import asyncio
import logging
from google.genai import types
from src.services.gemini import send_message_to_gemini, create_user_chat_session
from src.services.db import get_user

def register_ai_handlers(bot, ai_client, user_chats, user_states):
    def get_or_create_chat_session(chat_id, msg_from_user):
        if chat_id not in user_chats:
            user_data = get_user(chat_id)
            if not user_data:
                user_data = {
                    'name': msg_from_user.first_name or "Usuário",
                    'default_city': None,
                    'preferred_currency': 'USD',
                    'role': 'user'
                }
            user_chats[chat_id] = create_user_chat_session(ai_client, user_data)
        return user_chats[chat_id]

    @bot.message_handler(func=lambda msg: user_states.get(msg.chat.id) is None, content_types=['text'])
    async def handle_gemini_chat(msg):
        await bot.send_chat_action(msg.chat.id, 'typing')
        chat_id = msg.chat.id
        chat_session = get_or_create_chat_session(chat_id, msg.from_user)

        try:
            loop = asyncio.get_running_loop()
            response_text = await loop.run_in_executor(
                None, 
                lambda: send_message_to_gemini(chat_session, msg.text)
            )
            await bot.reply_to(msg, response_text, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Erro no chat do Gemini: {e}")
            await bot.reply_to(
                msg, 
                "Houve um erro ao processar sua mensagem. Por favor, tente novamente mais tarde."
            )

    @bot.message_handler(content_types=['voice'])
    async def handle_gemini_voice(msg):
        await bot.send_chat_action(msg.chat.id, 'typing')
        chat_id = msg.chat.id
        chat_session = get_or_create_chat_session(chat_id, msg.from_user)

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
            logging.error(f"Erro no chat de voz do Gemini: {e}")
            await bot.reply_to(
                msg, 
                "Houve um erro ao processar sua mensagem de voz. Por favor, tente novamente mais tarde."
            )