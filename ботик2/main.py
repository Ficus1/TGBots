import requests
import json
from bs4 import BeautifulSoup
from random import choice


api_token = 'Свой токен мур мур мур рррррр'
URL = "https://api.telegram.org/bot" + api_token
current_update_id = 0


def load_image(text, chat_id='1'):
    r = requests.get(f"https://fonwall.ru/search?q={text}")
    soup = BeautifulSoup(r.text, 'html.parser')
    link = choice(soup.findAll(attrs={'class': 'photo-item__img'}))
    url = link['src']
    # with open(f'{chat_id}.png', 'wb') as f:
    #     f.write(requests.get('http:' + link['src']).content)
    return url


def get_updates():
    update = requests.get(URL + '/getupdates').json()
    return update


def get_message():
    global current_update_id, cities
    data = get_updates()
    if len(data['result']) == 0:
        return None, None
    current_update_id = data['result'][-1]['update_id']
    try:
        open('last_update_id.txt').read()
    except Exception:
        with open('last_update_id.txt', 'w') as f:
            f.write('0')
    last_update_id = open('last_update_id.txt').read()
    with open("data.json", "w") as f:
        json.dump(data, f)
    if current_update_id == int(last_update_id):
        return None, None
    chat_id = data['result'][-1]['message']['chat']['id']
    message = data['result'][-1]['message']['text']
    with open('last_update_id.txt', 'w') as f:
        f.write(str(current_update_id))
    return chat_id, message


def send_photo(chat_id, url, caption=''):
    try:
        reply_markup = {"keyboard": [["/help", '/in_trend'], ["/top_10_month", "/top_10_day"]], "one_time_keyboard": False}
        photo = requests.post(URL + '/sendPhoto', data={'chat_id': chat_id, 'photo': url, 'caption': caption, 'reply_markup': reply_markup})
    except Exception:
        pass


def send_message(chat_id, text="Hello"):
    try:
        message = requests.post(URL + '/sendMessage', data={'chat_id': chat_id, 'text': text})
    except Exception:
        pass


def top_10_month(chat_id):
    r = requests.get(f"https://fonwall.ru/popular-photos/month/")
    soup = BeautifulSoup(r.text, 'html.parser')
    i = 1
    for link in soup.findAll(attrs={'class': 'photo-item__img'})[:10]:
        url = link['src']
        send_photo(chat_id, url, f"Топ месяца. Фото номер: {i}")
        i += 1


def top_10_day(chat_id):
    r = requests.get(f"https://fonwall.ru/popular-photos/day/")
    soup = BeautifulSoup(r.text, 'html.parser')
    i = 1
    for link in soup.findAll(attrs={'class': 'photo-item__img'})[:10]:
        url = link['src']
        send_photo(chat_id, url, f"Топ дня. Фото номер: {i}")
        i += 1


def in_trend(chat_id):
    r = requests.get(f"https://fonwall.ru/popular-photos/")
    soup = BeautifulSoup(r.text, 'html.parser')
    i = 1
    for link in soup.findAll(attrs={'class': 'photo-item__img'})[:10]:
        url = link['src']
        send_photo(chat_id, url, f"В тренде. Фото номер: {i}")
        i += 1


def run_command(chat_id, command='start'):
    if command == 'start':
        return send_message(chat_id, 'Я вывожу картинку на слово, которое вы мне напишите')
    if command == 'help':
        return send_message(chat_id, f'''Список доступных команд
/help - Вывести список доступных команд бота
/top_10_month - Вывести текущий прогноз погоды для выбранного города
/top_10_day - Прогноз погоды на 24 часа
/in_trend - Вывести текущий назначенный город
''')
    if command == 'top_10_day':
        return top_10_day(chat_id)
    if command == 'top_10_month':
        return top_10_month(chat_id)
    if command == 'in_trend':
        return in_trend(chat_id)


def main():
    chat_id, message = get_message()
    if message and message.startswith('/'):
        run_command(chat_id, message[1:])
    else:
        if message:
            send_photo(chat_id, load_image(message))


if __name__ == '__main__':
    while True:
        main()