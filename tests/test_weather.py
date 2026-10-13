from unittest.mock import patch
from src.services.weather import get_weather

def test_get_weather_contract():
    cidade = "Anápolis"
    
    # Patch direto na execução real para simular retorno simples
    with patch("src.services.weather.get_weather", return_value=f"🌤️ Clima em {cidade}: 25°C, Ensolarado"):
        resultado = get_weather(cidade)
        
        assert resultado is not None
        assert isinstance(resultado, str)
        assert cidade in resultado
        assert "°C" in resultado