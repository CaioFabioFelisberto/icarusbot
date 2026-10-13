import pytest
from unittest.mock import AsyncMock, patch
from src.services.triggers import send_daily_briefing

@pytest.mark.asyncio
async def test_send_daily_briefing_execution():
    """Verifica se o trigger percorre os usuários e chama o método de envio do bot."""
    mock_bot = AsyncMock()
    
    mock_users = [{
        'chat_id': 12345,
        'name': 'Caio',
        'phone': None,
        'default_city': 'Anápolis',
        'preferred_currency': 'BRL',
        'role': 'user'
    }]

    with patch("src.services.triggers.get_all_users", return_value=mock_users), \
         patch("src.services.triggers.get_weather", return_value="25°C, Ensolarado"), \
         patch("src.services.triggers.get_financial_summary", return_value="USD: 5.10"):

        await send_daily_briefing(mock_bot)
        assert mock_bot.send_message.called