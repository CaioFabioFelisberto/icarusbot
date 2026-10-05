from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.services.todo import get_tasks

def get_main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton("🌤️ Clima", callback_data="opt_1")
    btn2 = InlineKeyboardButton("💵 Cotação de Moedas", callback_data="opt_2")
    btn3 = InlineKeyboardButton("📰 Notícias", callback_data="opt_3")
    markup.add(btn1, btn2, btn3)
    return markup

def get_back_markup():
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("⬅️️ Voltar ao Menu", callback_data="btn_back")
    markup.add(btn_back)
    return markup

def build_todo_keyboard(chat_id: int):
    """Gera os botões inline para marcar como concluída ou excluir."""
    tasks = get_tasks(chat_id)
    markup = InlineKeyboardMarkup()
    
    if not tasks:
        return None

    for idx, task in enumerate(tasks):
        status_icon = "✅" if task["done"] else "📌"
        text_button = f"{status_icon} {task['text']}"
        
        # Botão para alternar concluída/pendente
        btn_toggle = InlineKeyboardButton(text_button, callback_data=f"todo_toggle_{idx}")
        # Botão para excluir
        btn_del = InlineKeyboardButton("❌", callback_data=f"todo_del_{idx}")
        
        markup.add(btn_toggle, btn_del)
        
    return markup