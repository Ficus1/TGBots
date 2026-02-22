import pyttsx3
import requests
import json
from translate import translate_text, languages_list


language_user = json.load(open('languages.json'))
api_token = open('token.txt').read()
URL = "https://api.telegram.org/bot" + api_token
current_update_id = 0
try:
    stop_user = json.load(open('stop.json'))
except Exception:
    f = open('stop.json', 'w')
    json.dump(dict(), f)
    stop_user = {}


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
    if not language_user.get(str(chat_id)):
        language_user[str(chat_id)] = 'ru'
    if not stop_user.get(str(chat_id)):
        stop_user[str(chat_id)] = False
    with open('last_update_id.txt', 'w') as f:
        f.write(str(current_update_id))
    return chat_id, message


def send_message(chat_id, text="Hello"):
    try:
        reply_markup = {"keyboard": [["/help", '/en'],["/start"], ["/stop"], ["/ru"]], "one_time_keyboard": False}
        message = requests.post(URL + '/sendMessage', data={'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)})
    except Exception:
        pass


def send_voice(chat_id, text):
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, 'audio.ovv')
        engine.runAndWait()
        audio = open('audio.ovv', 'rb')
        reply_markup = {"keyboard": [["/help", '/en'], ["/start"], ["/stop"], ["/ru"]], "one_time_keyboard": False}
        voice = requests.post(URL + '/sendVoice', files={'voice': audio},
                                data={'chat_id': chat_id, 'reply_markup': json.dumps(reply_markup)})
    except Exception:
        pass


def run_command(chat_id, command='help'):
    global stop_user
    if command in languages_list:
        language_user[str(chat_id)] = command
        with open("languages.json", "w") as f:
            json.dump(language_user, f)
        return send_message(chat_id, "Вы успешно поставили язык перевода на " + languages_list[command])
    if command == 'help':
        text = '''Список доступных команд
/help - Вывести список доступных команд бота
'''

        for i in languages_list:
            text += '/' + i + ' - перевод на ' + languages_list[i] + '\n'
        return send_message(chat_id, text)
    if command == 'start':
        stop_user[str(chat_id)] = False
        with open("stop.json", "w") as f:
            json.dump(language_user, f)
        return send_message(chat_id, 'Привет , я hikkgkjTranslator, по умолчанию перевод стоит на ru. Напишите сообщение и я переведу его вам!')
    if command == 'stop':
        stop_user[str(chat_id)] = True
        with open("stop.json", "w") as f:
            json.dump(language_user, f)
        return send_message(chat_id, 'До встречи!')


def main():
    global stop_user
    chat_id, message = get_message()
    if message and message.startswith('/') and (not stop_user.get(str(chat_id)) or message[1:] == 'start'):
        run_command(chat_id, message[1:])

    else:
        if chat_id and not stop_user.get(str(chat_id)):
            send_voice(chat_id, translate_text(message, language_user[str(chat_id)]))


if __name__ == '__main__':
    while True:
        main()