import sqlite3

DB_PATH = "src/database/users.db"

def init_db():
    """Cria as tabelas caso não existam."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            default_city TEXT,
            preferred_currency TEXT DEFAULT 'USD',
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

def save_user(chat_id: int, name: str, phone: str = None, city: str = None, currency: str = "USD", role: str = "user"):
    """Cadastra ou atualiza o perfil do usuário."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (chat_id, name, phone, default_city, preferred_currency, role)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(chat_id) DO UPDATE SET
            name = excluded.name,
            phone = excluded.phone,
            default_city = excluded.default_city,
            preferred_currency = excluded.preferred_currency,
            role = excluded.role
    """, (chat_id, name, phone, city, currency, role))
    conn.commit()
    conn.close()

def get_user(chat_id: int):
    """Busca o perfil completo do usuário pelo chat_id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, name, phone, default_city, preferred_currency, role FROM users WHERE chat_id = ?", (chat_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "chat_id": user[0],
            "name": user[1],
            "phone": user[2],
            "default_city": user[3],
            "preferred_currency": user[4],
            "role": user[5]
        }
    return None

def get_all_users():
    """
    Retorna uma lista de todos os usuários cadastrados no banco de dados.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, name, phone, default_city, preferred_currency, role FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = []

    for row in rows:
        users.append({
            "chat_id": row[0],
            "name": row[1],
            "phone": row[2],
            "default_city": row[3],
            "preferred_currency": row[4],
            "role": row[5]
        })
    return users