import requests
import json
from weather_command import current_weather, forecast


with open("cities.json", "r") as read_file:
    cities = json.load(read_file)
api_token = open('token.txt').read()
URL = "https://api.telegram.org/bot" + api_token
current_update_id = 0


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
    if not cities.get(str(chat_id)):
        cities[str(chat_id)] = 'Москва'
    with open('last_update_id.txt', 'w') as f:
        f.write(str(current_update_id))
    return chat_id, message


def send_message(chat_id, text="Hello"):
    try:
        reply_markup = {"keyboard": [["/help", '/city'], ["/current", "/forecast"]], "one_time_keyboard": False}
        message = requests.post(URL + '/sendMessage', data={'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)})
        #message = requests.post(URL + '/sendMessage', data={'chat_id': chat_id, 'text': text})
    except Exception:
        pass


def run_command(chat_id, command='help'):
    global cities
    if command == 'help':
        return send_message(chat_id, f'''Список доступных команд
/help - Вывести список доступных команд бота
/current - Вывести текущий прогноз погоды для выбранного города
/forecast - Прогноз погоды на 24 часа
/city - Вывести текущий назначенный город
''')
    if command == 'city':
        return send_message(chat_id, f"Текущий город - {cities[str(chat_id)]}")
    if command == 'current':
        return send_message(chat_id, current_weather(cities[str(chat_id)]))
    if command == 'forecast':
        return send_message(chat_id, forecast(cities[str(chat_id)]))
    if command == 'start':
        return send_message(chat_id, 'Для начала работы введите город на любом языке, с которым я должен буду работа через команду\n'
                                     'Для ознакомления с командами введите /help')
    return send_message(chat_id, "Я не знаю такую команду \nВоспользуйтесь командой /help")


def main():
    chat_id, message = get_message()
    if message and message.startswith('/'):
        run_command(chat_id, message[1:])
    else:
        if message:
            cities[str(chat_id)] = message
            with open("cities.json", "w") as f:
                json.dump(cities, f)
            return send_message(chat_id, "Вы успешно указали город " + cities[str(chat_id)])


if __name__ == '__main__':
    while True:
        main()