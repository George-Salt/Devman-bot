import os

import requests
import telegram
from dotenv import load_dotenv


def send_notification(check):
    title = check["lesson_title"]
    link = check["lesson_url"]
    if check["is_negative"]:
        text=f"Преподаватель проверил урок `{title}`.\n\nВ работе нашлись ошибки.\nСсылка на урок - {link}."
    else:
        text=f"""Преподаватель проверил урок `{title}`.\n\nПреподавателю все понравилось. Можно приступать к следующему уроку.\nСсылка на урок - {link}."""
    
    bot.send_message(
        chat_id=chat_id,
        text=text
    )
    return "Уведомление отправлено!"


if __name__ == "__main__":
    load_dotenv()

    bot_token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    devman_token = os.getenv("DEVMAN_TOKEN")

    bot = telegram.Bot(token=bot_token)

    url = "https://dvmn.org/api/long_polling/"
    authorization = {
        "Authorization": f"Token {devman_token}"
    }
    params = {}

    while True:
        try:
            response = requests.get(url, headers=authorization, timeout=95, params=params)
            response.raise_for_status()

        except requests.exceptions.ReadTimeout:
            params = {"timestamp": response.json()["timestamp_to_request"]}
            continue

        except requests.exceptions.ConnectionError:
            continue

        if not response.json()["status"]:
            continue
        if not response.json()["status"] == "found":
            continue
        for check in response.json()["new_attempts"]:
            print(send_notification(check))