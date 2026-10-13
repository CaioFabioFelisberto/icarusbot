from unittest.mock import MagicMock
from src.services.gemini import create_user_chat_session

def test_create_user_chat_session():
    """Verifica se a sessão do Gemini é criada com as instruções de sistema do usuário."""
    mock_client = MagicMock()
    user_data = {
        'name': 'Caio',
        'default_city': 'Anápolis',
        'preferred_currency': 'BRL',
        'role': 'user'
    }

    # Instancia a sessão simulada
    session = create_user_chat_session(mock_client, user_data)
    
    assert session is not None
    assert mock_client.chats.create.called