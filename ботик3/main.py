import requests
import json
from questions import capital


api_token = '5201995653:AAH1cTZhkd8TB-MYR9B6S8eTnKurCNahLn4'
URL = "https://api.telegram.org/bot" + api_token
current_update_id = 0
users_data = {}
try:
    users_data = json.load(open('users_data.json'))
except Exception:
    f = open('users_data.json', 'w')
    json.dump(dict(), f)
try:
    open('last_update_id.txt').read()
except Exception:
    with open('last_update_id.txt', 'w') as f:
        f.write('0')


def get_updates():
    update = requests.get(URL + '/getupdates').json()
    return update


def get_message():
    global current_update_id, users_data
    data = get_updates()
    if len(data['result']) == 0:
        return None, None
    current_update_id = data['result'][-1]['update_id']
    last_update_id = open('last_update_id.txt').read()
    with open("data.json", "w") as f:
        json.dump(data, f)
    if current_update_id == int(last_update_id):
        return None, None
    chat_id = data['result'][-1]['message']['chat']['id']
    message = data['result'][-1]['message']['text']
    if not users_data.get(str(chat_id)):
        users_data[str(chat_id)] = {'question_number': 0, 'is_start': False, 'victorina_name': ''}
    with open('last_update_id.txt', 'w') as f:
        f.write(str(current_update_id))
    return chat_id, message


def send_message(chat_id, text="Hello", markup=''):
    global users_data
    try:
        if not users_data[str(chat_id)]['is_start']:
            reply_markup = {"keyboard": [["Помощь"], ["Столицы"]], "one_time_keyboard": True}
        else:
            reply_markup = {"keyboard": [["Остановить", 'Рестарт']], "one_time_keyboard": True}
            if markup:
                reply_markup['keyboard'].append(markup)
        message = requests.post(URL + '/sendMessage',
                                data={'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)})
    except Exception:
        pass


def run_command(chat_id, command='start'):
    global users_data
    if command == 'start':
        return send_message(chat_id, 'Привет я бот интересных задач')
    if command == 'help':
        return send_message(chat_id, f'''Список доступных команд
/help - Вывести список доступных команд бота
''')
    if command == 'stop':
        users_data[str(chat_id)]['is_start'] = False
        users_data[str(chat_id)]['question_number'] = 0
        users_data[str(chat_id)]['victorina_name'] = ''
        with open('users_data.json', 'w') as f:
            json.dump(users_data, f)
        return send_message(chat_id, 'Вы оставновили викторину')
    if command == 'restart':
        users_data[str(chat_id)]['is_start'] = False
        users_data[str(chat_id)]['question_number'] = 0
        with open('users_data.json', 'w') as f:
            json.dump(users_data, f)
        return run_command(chat_id, users_data[str(chat_id)]['victorina_name'])
    if command == 'capital' and not users_data[str(chat_id)]['is_start']:
        users_data[str(chat_id)]['is_start'] = True
        users_data[str(chat_id)]['victorina_name'] = 'capital'
        with open('users_data.json', 'w') as f:
            json.dump(users_data, f)
        return send_message(chat_id, capital[users_data[str(chat_id)]['question_number']]['question'], capital[users_data[str(chat_id)]['question_number']]['options'])


def main():
    global users_data
    chat_id, message = get_message()
    if message and message.startswith('/'):
        run_command(chat_id, message[1:])
    else:
        if message:
            if message == 'Помощь':
                run_command(chat_id, 'help')
            if message == 'Остановить':
                run_command(chat_id, 'stop')
            if message == 'Рестарт':
                run_command(chat_id, 'restart')
            if message == 'Столицы':
                send_message(chat_id, f'Вы выбрали столицы мира')
                run_command(chat_id, 'capital')
            elif users_data[str(chat_id)]['is_start']:
                if message == capital[users_data[str(chat_id)]['question_number']]['answer']:
                    send_message(chat_id, 'Вы ответили правильно')
                else:
                    send_message(chat_id, f"Вы ответили неправильно. Правильный ответ: {capital[users_data[str(chat_id)]['question_number']]['answer']}")
                users_data[str(chat_id)]['question_number'] += 1
                with open('users_data.json', 'w') as f:
                    json.dump(users_data, f)
                if users_data[str(chat_id)]['question_number'] == len(capital):
                    users_data[str(chat_id)]['is_start'] = False
                    users_data[str(chat_id)]['question_number'] = 0
                    users_data[str(chat_id)]['victorina_name'] = ''
                    with open('users_data.json', 'w') as f:
                        json.dump(users_data, f)
                    send_message(chat_id, 'Вы ответили на все вопросы')
                else:
                    send_message(chat_id, capital[users_data[str(chat_id)]['question_number']]['question'], capital[users_data[str(chat_id)]['question_number']]['options'])


if __name__ == '__main__':
    while True:
        main()