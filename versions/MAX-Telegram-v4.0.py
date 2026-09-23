import requests
import time
import telebot
import os
from io import BytesIO

bot = telebot.TeleBot("")
url = ""
chat_id_tg = ""
target_sender = ""
DB_FILE = "processed_ids.txt"

payload = { "chatId": "", "count": 10 }
headers = { "Content-Type": "application/json" }


if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        processed_ids = set(line.strip() for line in f if line.strip())
else:
    processed_ids = set()

print(f"Загружено ID: {len(processed_ids)}")

def download_file(file_url):
    try:
        response = requests.get(file_url, timeout=30)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            print(f"Ошибка скачивания файла: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при скачивании: {e}")
        return None

while True:
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data and isinstance(data, list):
                for item in reversed(data):
                    current_id = item.get("idMessage")
                    sender_name = item.get("senderName")

                    if current_id and current_id not in processed_ids and sender_name == target_sender:
                        msg_type = item.get("typeMessage")
                        text = item.get("textMessage") or item.get("caption") or ""
                        file_url = item.get("downloadUrl")

                        try:
                            if msg_type == "imageMessage" and file_url:
                                bot.send_photo(chat_id_tg, file_url, caption=text)
                                print("Отправлено фото")

                            elif msg_type == "videoMessage" and file_url:
                                bot.send_video(chat_id_tg, file_url, caption=text)
                                print("Отправлено видео")

                            elif msg_type == "audioMessage" and file_url:
                                bot.send_audio(chat_id_tg, file_url, caption=text)
                                print("Отправлено аудио")

                            elif msg_type == "documentMessage" and file_url:
                                file_data = download_file(file_url)
                                if file_data:
                                    file_name = item.get("fileName") or "document"
                                    bot.send_document(
                                        chat_id_tg,
                                        file_data,
                                        caption=text,
                                        visible_file_name=file_name
                                    )
                                print("Отправлен документ")
                            elif text:
                                bot.send_message(chat_id_tg, text)
                                print(f"Отправлено сообщение: {text[:20]}...")

                            processed_ids.add(current_id)
                            with open(DB_FILE, "a") as f:
                                f.write(f"{current_id}\n")

                        except Exception as e:
                            print(f"Ошибка при пересылке контента: {e}")
        else:
            print(f"Ошибка API: {response.status_code}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    if len(processed_ids) > 200:
        processed_ids = set(list(processed_ids)[-100:])

    time.sleep(10)
