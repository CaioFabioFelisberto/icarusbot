from src.services.todo import add_task, get_tasks, toggle_task, delete_task
from src.keyboards.menu import build_todo_keyboard

def register_todo_handlers(bot):
    @bot.message_handler(commands=['task', 'tarefa'])
    async def handle_add_task(msg):
        task_text = msg.text.replace('/task', '').replace('/tarefa', '').strip()

        if not task_text:
            await bot.reply_to(msg, "Por favor, forneça a descrição da tarefa após o comando. Exemplo: /task Comprar leite")
            return
        add_task(msg.chat.id, task_text)
        await bot.reply_to(msg, f"Tarefa adicionada: {task_text}")

    @bot.message_handler(commands=['tasks', 'tarefas'])
    async def handle_list_tasks(msg):
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
            
        tasks = get_tasks(chat_id)
        if tasks:
            markup = build_todo_keyboard(chat_id)
            await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=markup)
        else:
            await bot.edit_message_text("🎉 Todas as tarefas foram concluídas ou removidas!", chat_id, call.message.message_id)