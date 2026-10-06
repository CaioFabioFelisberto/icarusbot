import time
from google.genai import types

def create_user_chat_session(ai_client, user_data:dict):
    """
    Cria uma sessão de chat com o Gemini aplicando System Instructions
    personalizadas com base no perfil do utilizador retornado do SQLite.
    """

    name = user_data.get('name', 'Utilizador')
    city = user_data.get('default_city') or 'Não informada'
    currency = user_data.get('preferred_currency', 'USD')
    role = user_data.get('role', 'user')

    system_instruction = (
        f"Você é o IcarusBot, um assistente virtual inteligente e prestativo no Telegram.\n"
        f"Você está conversando com: {name}.\n"
        f"Cidade do utilizador: {city}.\n"
        f"Moeda preferida: {currency}.\n"
        f"Nível de acesso: {role}.\n\n"
        f"Instruções de comportamento:\n"
        f"- Trate o utilizador pelo nome ({name}) sempre de forma natural quando fizer sentido.\n"
        f"- Se o utilizador perguntar sobre o tempo sem especificar a cidade, assuma que se refere a {city}.\n"
        f"- Seja amigável, direto e mantenha um tom profissional porém descontraído.\n"
        f"- Use a formatação Markdown para organizar as respostas."
    )

    return ai_client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            system_instruction=system_instruction
        )
    )

def send_message_to_gemini(chat_session, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = chat_session.send_message(prompt)
            return response.text
        except Exception as e:
            if "503" in str(e) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise e