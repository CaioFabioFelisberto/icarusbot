from src.services import save_user, get_user
from src.services import send_daily_briefing
import logging

def register_command_handlers(bot, user_chats):
    @bot.message_handler(commands=['start'])
    async def start(msg):
        chat_id = msg.chat.id
        first_name = msg.from_user.first_name or "Usuário"

        user = get_user(chat_id)
        if not user:
            save_user(
                chat_id=chat_id,
                name=first_name,
                phone=None,
                city=None,
                currency="USD",
                role="user"
            )
            logging.info(f"Novo usuário cadastrado no SQLite: {first_name} ({chat_id})")

        welcome_message = (
            f"Olá, **{first_name}**! Bem-vindo ao **IcarusBot**.\n\n"
            f"O seu perfil inicial já foi criado!\n\n"
            f"Use /help para ver os comandos disponíveis. Use /menu para acessar o menu principal. Use /perfil para personalizar seu perfil."
        )
        await bot.reply_to(msg, welcome_message, parse_mode="Markdown")

    @bot.message_handler(commands=['perfil'])
    async def profile(msg):
        chat_id = msg.chat.id
        user = get_user(chat_id)

        if not user:
            await bot.reply_to(msg, "Perfil não encontrado. Use /start para iniciar o bot e criar seu perfil.")
            return

        profile_info = (
            "👤 **SEU PERFIL NO ICARUSBOT**\n"
            "───────────────────────────\n"
            f"• **Nome:** {user['name']}\n"
            f"• **Cidade Padrão:** {user['default_city'] or 'Não configurada'}\n"
            f"• **Moeda Preferida:** {user['preferred_currency']}\n"
            f"• **Nível de Acesso:** {user['role'].capitalize()}\n"
            "───────────────────────────\n"
            "Para alterar sua cidade padrão, use: `/setcidade <nome_da_cidade>`\n"
            "Para alterar sua moeda preferida, use: `/setmoeda <código_da_moeda>` (USD, BRL, EUR, etc.)\n"
            "Para alterar seu telefone, use: `/settelefone <número>`\n"
        )
        await bot.send_message(chat_id, profile_info, parse_mode="Markdown")

    @bot.message_handler(commands=['setcidade'])
    async def set_city(msg):
        chat_id = msg.chat.id
        city_name = msg.text.replace('/setcidade', '').strip()

        if not city_name:
            await bot.reply_to(msg, "Por favor, forneça o nome da cidade após o comando. Exemplo: /setcidade Anápolis")
            return
        
        user = get_user(chat_id)
        if user:
            save_user(
                chat_id=chat_id,
                name=user['name'],
                phone=user['phone'],
                city=city_name,
                currency=user['preferred_currency'],
                role=user['role']
            )
            user_chats.pop(chat_id, None)
            await bot.reply_to(msg, f"Sua cidade padrão foi atualizada para: **{city_name}**", parse_mode="Markdown")

    @bot.message_handler(commands=['setmoeda'])
    async def set_currency(msg):
        chat_id = msg.chat.id
        currency_code = msg.text.replace('/setmoeda', '').strip().upper()

        if not currency_code:
            await bot.reply_to(msg, "Por favor, forneça o código da moeda após o comando. Exemplo: /setmoeda BRL")
            return

        user = get_user(chat_id)
        if user:
            save_user(
                chat_id=chat_id,
                name=user['name'],
                phone=user['phone'],
                city=user['default_city'],
                currency=currency_code,
                role=user['role']
            )
            user_chats.pop(chat_id, None)
            await bot.reply_to(msg, f"Sua moeda preferida foi atualizada para: **{currency_code}**", parse_mode="Markdown")

    @bot.message_handler(commands=['settelefone'])
    async def set_phone(msg):
        chat_id = msg.chat.id
        phone_number = msg.text.replace('/settelefone', '').strip()

        if not phone_number:
            await bot.reply_to(msg, "Por favor, forneça o número de telefone após o comando. Exemplo: /settelefone +5511999999999")
            return

        user = get_user(chat_id)
        if user:
            save_user(
                chat_id=chat_id,
                name=user['name'],
                phone=phone_number,
                city=user['default_city'],
                currency=user['preferred_currency'],
                role=user['role']
            )
            user_chats.pop(chat_id, None)
            await bot.reply_to(msg, f"Seu número de telefone foi atualizado para: **{phone_number}**", parse_mode="Markdown")

    @bot.message_handler(commands=['help'])
    async def help_cmd(msg):
        await bot.reply_to(msg, "Aqui estão os comandos disponíveis:\n\n"
                           "/start - Inicia o bot e mostra uma mensagem de boas-vindas.\n"
                           "/help - Exibe esta mensagem de ajuda.\n"
                           "/menu - Mostra o menu principal com as opções disponíveis.\n"
                           "/perfil - Exibe suas informações de perfil.\n"
                           "/task <descrição> - Adiciona uma nova tarefa.\n"
                           "/tasks - Exibe a lista de tarefas.")

    @bot.message_handler(commands=['teste_alerta'])
    async def test_alert(msg):
        await bot.reply_to(msg, "⚙️ Disparando alerta de teste...")
        await send_daily_briefing(bot)