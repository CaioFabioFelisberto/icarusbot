import sqlite3
import pytest
from src.services.db import DB_PATH, save_user, get_user, get_all_users

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    """Cria uma base de dados SQLite temporária para não afetar a base de dados real."""
    test_db = tmp_path / "test_users.db"
    monkeypatch.setattr("src.services.db.DB_PATH", str(test_db))
    
    # Inicializa a tabela
    conn = sqlite3.connect(str(test_db))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            default_city TEXT,
            preferred_currency TEXT DEFAULT 'USD',
            role TEXT DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

def test_save_and_get_user():
    save_user(
        chat_id=123456,
        name="Caio",
        phone="+5562999999999",
        city="Anápolis",
        currency="BRL",
        role="admin"
    )

    user = get_user(123456)
    assert user is not None
    assert user['name'] == "Caio"
    assert user['default_city'] == "Anápolis"
    assert user['preferred_currency'] == "BRL"

def test_get_all_users():
    save_user(chat_id=1, name="User1", phone=None, city="Cidade1", currency="USD", role="user")
    save_user(chat_id=2, name="User2", phone=None, city="Cidade2", currency="EUR", role="user")

    users = get_all_users()
    assert len(users) == 2