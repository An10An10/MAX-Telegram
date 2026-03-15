import requests
import time
import telebot

bot = telebot.TeleBot("")

url = "https://3100.api.green-api.com"
chat_id_tg = #из telegram

payload = {"chatId": "", "count": 1}    #из green api
headers = {"Content-Type": "application/json"}

last_msg_id = ""

while True:
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.text:
            data = response.json()
        else:
            time.sleep(10)
            continue

        if data and isinstance(data, list):
            item = data[0]
            
            current_id = item.get("idMessage")
            
            if current_id != last_msg_id:
                msg_type = item.get("typeMessage")
                text = item.get("textMessage") or item.get("caption") or ""
                
                if msg_type == "imageMessage" and "downloadUrl" in item:
                    img_url = item.get("downloadUrl")
                    try:
                        bot.send_photo(chat_id_tg, img_url, caption=text)
                        print(f"Отправлено фото: {img_url}")
                    except Exception as e:
                        print(f"Ошибка при отправке фото: {e}")
                
                elif text:
                    try:
                        bot.send_message(chat_id_tg, text)
                        print(f"Отправлено сообщение: {text[:20]}...")
                    except Exception as e:
                        print(f"Ошибка при отправке текста: {e}")

                last_msg_id = current_id
                
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    
    time.sleep(10)
