from src.services.todo import add_task, get_tasks, toggle_task, delete_task

def test_todo_flow():
    chat_id = 999999
    
    # 1. Adicionar tarefa
    add_task(chat_id, "Tarefa Teste")
    tasks = get_tasks(chat_id)
    assert len(tasks) > 0
    
    # Pega o índice da tarefa que acabamos de adicionar
    last_idx = len(tasks) - 1
    assert tasks[last_idx]['text'] == "Tarefa Teste"
    assert tasks[last_idx]['done'] is False

    # 2. Alternar status (toggle)
    toggle_task(chat_id, last_idx)
    tasks_after_toggle = get_tasks(chat_id)
    assert tasks_after_toggle[last_idx]['done'] is True

    # 3. Excluir tarefa
    delete_task(chat_id, last_idx)
    tasks_after_delete = get_tasks(chat_id)
    assert len(tasks_after_delete) == len(tasks) - 1