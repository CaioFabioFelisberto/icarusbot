import asyncio
from datetime import datetime
from src.services.db import get_all_users
from src.services.weather import get_weather
from src.services.money import get_financial_summary
import logging

async def send_daily_briefing(bot):
    """
    Envia um resumo diário personalizado para todos os usuários cadastrados.
    """
    users = get_all_users()
    
    for user in users:
        chat_id = user['chat_id']
        name = user['name']
        city = user['default_city']
        
        message = f"☀️ **BOM DIA, {name.upper()}!**\n\n"
        
        if city:
            weather_data = get_weather(city)
            message += f"🌍 **Clima em {city}:**\n{weather_data}\n\n"
        else:
            message += "🌍 **Clima:** Use `/setcidade` para receber a previsão automática aqui!\n\n"
            
        financial_data = get_financial_summary()
        message += f"📈 **Mercado Financeiro:**\n{financial_data}\n"
        
        try:
            await bot.send_message(chat_id, message, parse_mode="Markdown")
            await asyncio.sleep(0.5)
        except Exception as e:
            logging.error(f"Erro ao enviar alerta para {chat_id}: {e}")

async def start_scheduler(bot):
    """
    Loop que monitora o horário em segundo plano para disparar às 08:00.
    """
    logging.info("Agendador de Triggers iniciado!")
    while True:
        now = datetime.now()
        if now.hour == 8 and now.minute == 0:
            logging.info("Executando disparos do resumo matinal...")
            await send_daily_briefing(bot)
            await asyncio.sleep(60)
            
        await asyncio.sleep(30)