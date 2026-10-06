from src.handlers.command_handler import register_command_handlers
from src.handlers.menu_handler import register_menu_handlers
from src.handlers.todo_handler import register_todo_handlers
from src.handlers.ai_handler import register_ai_handlers

def register_all_handlers(bot, ai_client, user_chats, user_states):
    register_command_handlers(bot, user_chats)
    register_menu_handlers(bot, user_states)
    register_todo_handlers(bot)
    register_ai_handlers(bot, ai_client, user_chats, user_states)