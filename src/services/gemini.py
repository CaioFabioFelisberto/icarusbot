import time
import asyncio

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