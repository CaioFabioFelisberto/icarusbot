import json
import os

TASKS_FILE = "src/database/todo.json"

def _load_tasks():
    """Lê o arquivo JSON de tarefas. Cria um dicionário vazio se o arquivo não existir."""
    if not os.path.exists(TASKS_FILE):
        return {}
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_tasks(tasks_data):
    """Salva o dicionário de tarefas no arquivo JSON."""
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks_data, f, ensure_ascii=False, indent=4)

def add_task(chat_id: int, task_text: str):
    """Adiciona uma nova tarefa para o chat_id (padrão: concluída = False)."""
    data = _load_tasks()
    str_chat_id = str(chat_id)
    
    if str_chat_id not in data:
        data[str_chat_id] = []
        
    data[str_chat_id].append({
        "text": task_text,
        "done": False
    })
    
    _save_tasks(data)
    return True

def get_tasks(chat_id: int):
    """Retorna a lista de tarefas do chat_id."""
    data = _load_tasks()
    return data.get(str(chat_id), [])

def toggle_task(chat_id: int, index: int):
    """Alterna o status de concluída (True/False) de uma tarefa pelo índice."""
    data = _load_tasks()
    str_chat_id = str(chat_id)
    
    if str_chat_id in data and 0 <= index < len(data[str_chat_id]):
        current_status = data[str_chat_id][index]["done"]
        data[str_chat_id][index]["done"] = not current_status
        _save_tasks(data)
        return True
    return False

def delete_task(chat_id: int, index: int):
    """Remove uma tarefa pelo índice."""
    data = _load_tasks()
    str_chat_id = str(chat_id)
    
    if str_chat_id in data and 0 <= index < len(data[str_chat_id]):
        data[str_chat_id].pop(index)
        _save_tasks(data)
        return True
    return False