from src.keyboards.menu import get_main_menu_markup, get_back_markup
from src.services.weather import get_weather
from src.services.money import get_financial_summary
from src.services.news import get_latest_news

def register_menu_handlers(bot, user_states):
    @bot.message_handler(commands=['menu'])
    async def show_menu(msg):
        await bot.send_message(
            msg.chat.id, 
            "Escolha uma opção:", 
            reply_markup=get_main_menu_markup()
        )

    @bot.callback_query_handler(func=lambda call: call.data in ["opt_1", "opt_2", "opt_3", "btn_back"])
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