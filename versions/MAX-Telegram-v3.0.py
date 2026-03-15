import requests
import time
import telebot

  
bot = telebot.TeleBot('')

url = ""
chat_id_tg = 

payload = {
    "chatId": "", 
    "count": 1
}
headers = { "Content-Type": "application/json" }

last_msg_id = None
target_sender = ""

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
                    file_url = item.get('downloadUrl')

                    try:
                        if msg_type == 'imageMessage' and file_url:
                            bot.send_photo(chat_id_tg, file_url, caption=text)
                            print(f"Отправлено фото")
                          
                        elif msg_type == 'videoMessage' and file_url:
                            bot.send_video(chat_id_tg, file_url, caption=text)
                            print(f"Отправлено видео")
                          
                        elif msg_type == 'audioMessage' and file_url:
                            bot.send_audio(chat_id_tg, file_url)
                            print(f"Отправлено аудио")

                        elif text:
                            bot.send_message(chat_id_tg, text)
                            print(f"Отправлено сообщение: {text[:20]}...")
                            
                    except Exception as e:
                        print(f"Ошибка при пересылке контента: {e}")

                    last_msg_id = current_id
        else:
            print(f"Ошибка API: {response.status_code}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    time.sleep(10)
