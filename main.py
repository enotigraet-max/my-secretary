import google.generativeai as genai
from pyrogram import Client, filters
import asyncio
import os

API_ID = 39339366  
API_HASH = "b5f7a4af5991b6c3221d9da302a321a6"  
GEMINI_KEY = "AQ.Ab8RN6Kjh5YdPPkjKGLv1V2S1BPFby2mFtbz4OpNJzxEEuQbJg"  
MY_PHONE = "+375291071476"  

TELEGRAM_CODE = os.environ.get("TG_CODE", "")

AI_PROMPT = "Ты личный ИИ-секретарь. Отвечай кратко от имени владельца."
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=AI_PROMPT)

app = Client("session_secretary", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.private & ~filters.me)
async def handle_new_message(client, message):
    if message.text:
        try:
            response = model.generate_content(message.text)
            await message.reply_text(response.text)
        except Exception as e: print(e)

async def main():
    await app.connect()
    if not TELEGRAM_CODE:
        print("ОТПРАВЛЯЕМ ЗАПРОС В TELEGRAM...")
        try:
            sent_code = await app.send_code(MY_PHONE)
            print("--------------------------------------------------")
            print("КОД УСПЕШНО ОТПРАВЛЕН В ТВОЙ TELEGRAM!")
            print(f"phone_code_hash:{sent_code.phone_code_hash}")
            print("--------------------------------------------------")
            with open("code_hash.txt", "w") as f: f.write(sent_code.phone_code_hash)
        except Exception as e: print(e)
    else:
        print("ВХОДИМ С ТВОИМ КОДОМ...")
        try:
            with open("code_hash.txt", "r") as f: phone_code_hash = f.read()
            await app.sign_in(MY_PHONE, phone_code_hash, TELEGRAM_CODE)
            print("УРА! ВХОД ВЫПОЛНЕН! СЕКРЕТАРЬ РАБОТАЕТ!")
            from pyrogram.methods.utilities.idle import idle
            await idle()
        except Exception as e: print(e)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
