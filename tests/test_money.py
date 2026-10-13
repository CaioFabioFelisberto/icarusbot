from unittest.mock import patch
from src.services.money import get_financial_summary

def test_get_financial_summary_format():
    """Valida se o resumo financeiro retorna uma string não vazia e formatada."""
    with patch("src.services.money.get_financial_summary", return_value="💵 **Cotações:**\nUSD: R$ 5.10"):
        summary = get_financial_summary()
        assert summary is not None
        assert isinstance(summary, str)
        assert "USD" in summary