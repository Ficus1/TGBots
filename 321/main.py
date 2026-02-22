import requests
import json
from currency import currency

key = 'SMdcBBU5W3idki8OrXdsRingnbzFYBbB'
api_token = '5201995653:AAH1cTZhkd8TB-MYR9B6S8eTnKurCNahLn4'
URL = "https://api.telegram.org/bot" + api_token
current_update_id = 0
stop_user = {}
try:
    stop_user = json.load(open('stop.json'))
except Exception:
    f = open('stop.json', 'w')
    json.dump(dict(), f)


def get_currency(current):
    #r = requests.get(f"https://free.currconv.com/api/v7/convert?q=RUB_{current},{current}_RUB&compact=ultra&apiKey=" + key).json()
    r = requests.get(f"https://api.apilayer.com/fixer/convert?to=RUB&from={current}&amount=1&apikey=" + key).json()
    return current + ' в RUB ' + str(r['result']) + '\n' 'RUB в ' + current + ' ' + str(1 / r['result'])


def get_updates():
    update = requests.get(URL + '/getUpdates').json()

    return update


def get_message():
    global current_update_id
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
    print(message)
    with open('last_update_id.txt', 'w') as f:
        f.write(str(current_update_id))
    return chat_id, message


def send_message(chat_id, text="Hello"):
    try:
        reply_markup = {'keyboard': [['Привет', 'Помощь'], ['GBP', 'AED', 'TRY'], ['Пока']], 'one_time_keyboard': False}
        message = requests.post(URL + '/sendMessage',
                                data={'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)})
        if message.json()['error_code'] == 400:
            requests.post(URL + '/sendMessage',
                          data={'chat_id': chat_id, 'text': '\n'.join(text.split('\n')[:len(text.split('\n')) // 2])})
            requests.post(URL + '/sendMessage',
                          data={'chat_id': chat_id, 'text': '\n'.join(text.split('\n')[len(text.split('\n')) // 2:])})
    except Exception:
        pass


def send_photo(chat_id, caption=''):
    message = requests.post(URL + '/sendPhoto', files={'photo': open('error.jpg', 'rb')}, data={'chat_id': chat_id, 'caption': caption})


def run_command(chat_id, command='start'):
    if command in currency:
        return send_message(chat_id, get_currency(command))
    if command == 'start':
        stop_user[str(chat_id)] = False
        with open('stop.json', 'w') as f:
            json.dump(stop_user, f)
        return send_message(chat_id, 'Я конвертирую валюту в рубли')
    if command == 'help':
        text = '''Список доступных команд
/help - Вывести список доступных команд бота
'''
        for i in currency:
            text += '/' + i + ' - конвертация на ' + i + ' ' + currency[i] + '\n'
        return send_message(chat_id, text)
    if command == 'stop':
        stop_user[str(chat_id)] = True
        with open('stop.json', 'w') as f:
            json.dump(stop_user, f)
        return send_message(chat_id, "До новых встреч, мой друг. Помни что курс валют меняется очень часто. Возвращайся скорее.")


def main():
    chat_id, message = get_message()
    if message and message.startswith('/'):
        run_command(chat_id, message[1:])
    else:
        if message and (not stop_user.get(str(chat_id)) or message == 'Привет'):
            if message == "Привет":
                run_command(chat_id, 'start')
                return send_message(chat_id, "Привет, я бот конвертатор. Нажми /help для помощи.")
            if message == "Помощь":
                return send_message(chat_id, "/help")
            if message == "Пока":
                return run_command(chat_id, 'stop')
            if message in currency:
                return run_command(chat_id, message)
            elif message in [currency[i].strip() for i in currency]:
                return run_command(chat_id, [i for i in currency if currency[i].strip() == message][0])
            else:
                send_photo(chat_id)


if __name__ == '__main__':
    while True:
        main()