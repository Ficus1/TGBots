import requests
import json
from bs4 import BeautifulSoup
from random import choice


stop_user = {}
try:
    stop_user = json.load(open('stop.json'))
except Exception:
    f = open('stop.json', 'w')
    json.dump(dict(), f)
api_token = '5201995653:AAH1cTZhkd8TB-MYR9B6S8eTnKurCNahLn4'
URL = "https://api.telegram.org/bot" + api_token
current_update_id = 0


def load_image(text=''):
    r = requests.get(f"https://yandex.ru/images/search?text=маникюр {text}")
    soup = BeautifulSoup(r.text, 'html.parser')
    link = choice(soup.findAll(attrs={'class': 'serp-item__thumb justifier__thumb'}))
    url = link['src']
    # with open(f'{chat_id}.png', 'wb') as f:
    #     f.write(requests.get('http:' + link['src']).content)
    return 'https:' + url


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
    global stop_user
    try:
        reply_markup = {"keyboard": [["Помощь", "Остановить бота" if not stop_user[str(chat_id)] else 'Запустить бота'], ["Матовые", "Френч"]], "one_time_keyboard": False}
        photo = requests.post(URL + '/sendPhoto', data={'chat_id': chat_id, 'photo': url, 'caption': caption, 'reply_markup':  json.dumps(reply_markup)})
    except Exception:
        pass


def send_message(chat_id, text="Hello"):
    global stop_user
    try:
        reply_markup = {"keyboard": [["Помощь", "Остановить бота" if not stop_user[str(chat_id)] else 'Запустить бота'], ["Матовые", "Френч"]], "one_time_keyboard": False}

        message = requests.post(URL + '/sendMessage', data={'chat_id': chat_id, 'text': text, 'reply_markup':  json.dumps(reply_markup)})
    except Exception:
        pass


def run_command(chat_id, command='start'):
    global stop_user
    if command == 'start':
        stop_user[str(chat_id)] = False
        with open('stop.json', 'w') as f:
            json.dump(stop_user, f)
        return send_message(chat_id, 'Я вывожу маникюр на каждый день')
    if command == 'stop':
        stop_user[str(chat_id)] = True
        with open('stop.json', 'w') as f:
            json.dump(stop_user, f)
        return send_message(chat_id, 'До встречи!')
    if command == 'help':
        return send_message(chat_id, f'''Список доступных команд
/help - Вывести список доступных команд бота
''')


def main():
    global stop_user
    chat_id, message = get_message()
    if message and message.startswith('/') and (not stop_user.get(str(chat_id)) or message[1:] == 'start'):
        run_command(chat_id, message[1:])
    else:
        if message and (not stop_user.get(str(chat_id)) or message == 'Запустить бота'):
            if message == 'Помощь':
                return run_command(chat_id, 'help')
            elif message == 'Остановить бота':
                return run_command(chat_id, 'stop')
            elif message == 'Запустить бота':
                return run_command(chat_id, 'start')
            elif message:
                send_photo(chat_id, load_image(message))


if __name__ == '__main__':
    while True:
        main()