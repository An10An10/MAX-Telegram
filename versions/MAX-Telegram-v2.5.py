import requests
import time
import telebot

# Укажите токен бота в кавычках
bot = telebot.TeleBot('')
chat_id_tg = # Chat id в Telegram

# Настройки Green API
url = "https://3100.api.green-api.com"

payload = {
    "chatId": "",
    "count": 1
}
headers = { "Content-Type": "application/json" }

last_msg_id = None
target_sender = ""

print("Бот запущен...")

while True:
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and isinstance(data, list):
                item = data[0]
                current_id = item.get('idMessage')
                sender_name = item.get('senderName')

                if current_id != last_msg_id and sender_name == target_sender:
                    msg_type = item.get('typeMessage')
                    text = item.get('textMessage') or item.get('caption') or ""

                    if msg_type == 'imageMessage' and 'downloadUrl' in item:
                        img_url = item.get('downloadUrl')
                        try:
                            bot.send_photo(chat_id_tg, img_url, caption=text)
                            print(f"Отправлено фото от {sender_name}")
                        except Exception as e:
                            print(f"Ошибка при отправке фото: {e}")

                    elif text:
                        try:
                            bot.send_message(chat_id_tg, text)
                            print(f"Отправлено сообщение: {text[:20]}...")
                        except Exception as e:
                            print(f"Ошибка при отправке текста: {e}")

                    last_msg_id = current_id
        else:
            print(f"Ошибка API: {response.status_code}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(10)
