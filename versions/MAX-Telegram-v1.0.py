import requests
import time
import telebot

bot = telebot.TeleBot("") #токен бота
url = "https://3100.api.green-api.com"
chat_id_tg = 

payload = {
    "chatId": "", 
    "count": 1
}

headers = {'Content-Type': 'application/json'}
oldt = ""

while True:
    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            last_msg = data[0]
            t = last_msg.get('textMessage', '')

            if t and t != oldt:
                print(f"Новое: {t}")
                bot.send_message(chat_id_tg, t)
                oldt = t
    except Exception as e:
        print(f"Ошибка: {e}")
    
    time.sleep(10)
