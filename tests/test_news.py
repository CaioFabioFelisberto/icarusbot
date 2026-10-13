import pytest
from unittest.mock import patch
from src.services.news import get_latest_news

@pytest.mark.asyncio
async def test_get_latest_news_format():
    """Valida se a função assíncrona de notícias devolve o feed formatado."""
    with patch("src.services.news.get_latest_news", return_value="📰 **Principais Notícias:**\n- Notícia 1"):
        news = await get_latest_news()
        assert news is not None
        assert isinstance(news, str)
        assert "📰" in news