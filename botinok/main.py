import requests
import json
from travel_command import *
from db_connect import *


# 5201995653:AAH1cTZhkd8TB-MYR9B6S8eTnKurCNahLn4
# 5356581871:AAG-2zFzSdcduF4fk00V3UMhCULa7IJl1Bo
try:
    open('mods.json')
except Exception as e:
    with open("mods.json", "w") as read_file:
        json.dump(dict(), read_file)
with open("mods.json", "r") as read_file:
    mods = json.load(read_file)
try:
    open('last_update_id.txt').read()
except Exception:
    with open('last_update_id.txt', 'w') as f:
        f.write('0')
stop_user = {}
try:
    stop_user = json.load(open('stop.json'))
except Exception:
    f = open('stop.json', 'w')
    json.dump(dict(), f)
api_token = open('token.txt').read()
URL = "https://api.telegram.org/bot" + api_token
current_update_id = 0


def get_updates():
    update = requests.get(URL + '/getUpdates').json()
    return update


def get_message():
    global current_update_id, mods
    data = get_updates()
    if not data.get('result') or len(data['result']) == 0:
        return None, None
    current_update_id = data['result'][-1]['update_id']
    last_update_id = open('last_update_id.txt').read()
    with open("data.json", "w") as f:
        json.dump(data, f)
    if current_update_id == int(last_update_id):
        return None, None
    chat_id = data['result'][-1]['message']['chat']['id']
    message = data['result'][-1]['message']['text']
    if not stop_user.get(str(chat_id)):
        stop_user[str(chat_id)] = False
    if not mods.get(str(chat_id)):
        mods[str(chat_id)] = {'is_start': False, 'date': '', 'city_to': '', 'city_from': ''}
        with open("mods.json", "w") as read_file:
            json.dump(mods, read_file)
    with open('last_update_id.txt', 'w') as f:
        f.write(str(current_update_id))
    return chat_id, message


def send_message(chat_id, text="Hello"):
    global mods, stop_user
    try:
        reply_markup = {"keyboard": [["Заполнить данные"]], "one_time_keyboard": True}
        if not stop_user.get(str(chat_id)) and not mods[str(chat_id)]['is_start']:
            reply_markup['keyboard'][0].append("Остановить бота")
            reply_markup['keyboard'][0].append("Помощь")
        else:
            if not mods[str(chat_id)]['is_start']:
                reply_markup['keyboard'][0].append("Запустить бота")
                reply_markup['keyboard'][0].append("Помощь")
        if mods[str(chat_id)]['is_start']:
            reply_markup['keyboard'][0].append('Стоп')
            reply_markup['keyboard'][0].append('Назад')
        else:
            reply_markup['keyboard'].append(["ЖД билет", "Сравнение цен", "Авиабилет"])
        message = requests.post(URL + '/sendMessage', data={'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)})
    except Exception:
        pass


#def send_location(chat_id, city):
#    try:
#        lat, lon = get_location(city)
#        location = requests.post(URL + '/sendLocation', data={'chat_id': chat_id, 'latitude': lat, 'longitude': lon, 'horizontal_accuracy': 1500})
#        return True
#    except Exception:
#        return


def run_command(chat_id, command='help'):
    global mods, stop_user
    with open("mods.json", "r") as read_file:
        mods = json.load(read_file)
    if command == 'help':
        return send_message(chat_id, f'''Для начала работы введите дату рейса, город отправки и город прибытия. 
Для этого введите "Заполнить данные"
''')
    if command == 'get_avia':
        if not mods[str(chat_id)]['city_to']:
            send_message(chat_id, 'Для начала вам надо заполнить данные о рейсе')
            if not mods[str(chat_id)]['date']:
                return
            return run_command(chat_id, 'get_data')
        price = get_avia_price(mods[str(chat_id)]['city_from'], mods[str(chat_id)]['city_to'], mods[str(chat_id)]['date'])
        if type(price) != int:
            return send_message(chat_id, price)
        return send_message(chat_id, f'Самая низкая цена на авиабилет: {price}руб.')
    if command == 'get_train':
        if not mods[str(chat_id)]['city_to']:
            send_message(chat_id, 'Для начала вам надо заполнить данные о рейсе\n')
            return run_command(chat_id, 'get_data')
        price = get_data(mods[str(chat_id)]['city_from'], mods[str(chat_id)]['city_to'], mods[str(chat_id)]['date'])
        if type(price) != int:
            return send_message(chat_id, price)
        return send_message(chat_id, f'Цена на жд билет: {price}руб.')
        #for i in get_train_price(mods[str(chat_id)]['city_from'], mods[str(chat_id)]['city_to']):
        #    if type(i) == str:
        #        return send_message(chat_id, get_train_price(mods[str(chat_id)]['city_from'], mods[str(chat_id)]['city_to']))
        #    send_message(chat_id, f"Цена на тариф: {i[0]} = {i[1]}руб.")
        #return
    if command == 'compare':
        if not mods[str(chat_id)]['city_to']:
            send_message(chat_id, 'Для начала вам надо заполнить данные о рейсе')
            return run_command(chat_id, 'get_data')
        price_avia = get_avia_price(mods[str(chat_id)]['city_from'], mods[str(chat_id)]['city_to'], mods[str(chat_id)]['date'])
        if type(price_avia) != int:
            return send_message(chat_id, price_avia)
        price = get_data(mods[str(chat_id)]['city_from'], mods[str(chat_id)]['city_to'], mods[str(chat_id)]['date'])
        if type(price) != int:
            return send_message(chat_id, price)
        send_message(chat_id, f'Цена на жд билет: {price}руб.')
        if price > price_avia:
            return send_message(chat_id, 'Выгоднее поехать на поезде')
        return send_message(chat_id, 'Выгоднее полететь на самолете')

        #send_message(chat_id, f'Цена на авиабилет: {price_avia}руб.')
        #for i in get_train_price(mods[str(chat_id)]['city_from'], mods[str(chat_id)]['city_to']):
        #    if type(i) == str:
        #        return send_message(chat_id, get_train_price(mods[str(chat_id)]['city_from'], mods[str(chat_id)]['city_to']))
        #    send_message(chat_id, f"Цена на ЖД билет. Тариф: {i[0]} = {i[1]}руб.")
        #return
    if command == 'get_data':
        if mods[str(chat_id)]['date']:
            mods[str(chat_id)] = {'is_start': False, 'date': '', 'city_to': '', 'city_from': ''}
            with open("mods.json", "w") as read_file:
                json.dump(mods, read_file)
        mods[str(chat_id)]['is_start'] = True
        with open("mods.json", "w") as read_file:
            json.dump(mods, read_file)
        return send_message(chat_id, 'Вы начали заполнение данных\n'
                                     'Для того, чтобы начать заполнение заново введите: "Заполнить данные"\n'
                                     'Введите дату рейса(в формате "год"-"месяц"-"день" Например: 2022-05-21)')
    if command == 'stop':
        mods[str(chat_id)] = {'is_start': False, 'date': '', 'city_to': '', 'city_from': ''}
        with open("mods.json", "w") as read_file:
            json.dump(mods, read_file)
        return send_message(chat_id, 'Вы остановили заполнение')
    if command == 'start':
        stop_user[str(chat_id)] = False
        with open('stop.json', 'w') as f:
            json.dump(stop_user, f)
        return send_message(chat_id, f'Привет, я Shorikoff, бот для сравнения цен на авиа и ЖД билеты\n'
                                     f'Для ознакомления с командами введите /help')
    if command == 'bot_stop':
        stop_user[str(chat_id)] = True
        with open('stop.json', 'w') as f:
            json.dump(stop_user, f)
        return send_message(chat_id, 'До встречи!')
    if command == 'backward':
        if not mods[str(chat_id)]['date']:
            mods[str(chat_id)]['is_start'] = False
            with open("mods.json", "w") as read_file:
                json.dump(mods, read_file)
            return send_message(chat_id, 'Вы отменили заполнение данных')
        elif not mods[str(chat_id)]['city_from']:
            mods[str(chat_id)]['date'] = ''
            with open("mods.json", "w") as read_file:
                json.dump(mods, read_file)
            return send_message(chat_id, 'Введите дату рейса(в формате "год"-"месяц"-"день" Например: 2022-05-21)')
        elif not mods[str(chat_id)]['city_to']:
            mods[str(chat_id)]['city_from'] = ''
            with open("mods.json", "w") as read_file:
                json.dump(mods, read_file)
            return send_message(chat_id, 'Введите город прибытия:')
    return send_message(chat_id, "Я не знаю такую команду \nВоспользуйтесь командой /help")


def main():
    global stop_user
    chat_id, message = get_message()
    if message and message.startswith('/') and (not stop_user.get(str(chat_id)) or message[1:] == 'start'):
        run_command(chat_id, message[1:])
    else:
        if message and (not stop_user.get(str(chat_id)) or message == 'Запустить бота'):
            if message == 'Запустить бота':
                return run_command(chat_id, 'start')
            if message == 'Назад':
                return run_command(chat_id, 'backward')
            if message == 'Остановить бота':
                return run_command(chat_id, 'bot_stop')
            if message == 'Заполнить данные':
                return run_command(chat_id, 'get_data')
            if message == 'Сравнение цен':
                return run_command(chat_id, 'compare')
            if message == 'ЖД билет':
                return run_command(chat_id, 'get_train')
            if message == 'Авиабилет':
                return run_command(chat_id, 'get_avia')
            if message == 'Помощь':
                return run_command(chat_id, 'help')
            if message == 'Стоп':
                return run_command(chat_id, 'stop')
            if mods[str(chat_id)]['is_start']:
                if not mods[str(chat_id)]['date']:
                    mods[str(chat_id)]['date'] = message
                    with open("mods.json", "w") as read_file:
                        json.dump(mods, read_file)
                    return send_message(chat_id, 'Вы успешно указали дату: ' + message + '\nВведите город отправки:')
                elif not mods[str(chat_id)]['city_from']:
                    mods[str(chat_id)]['city_from'] = message
                    with open("mods.json", "w") as read_file:
                        json.dump(mods, read_file)
                    return send_message(chat_id, 'Вы успешно указали город отправки: ' + message + '\nВведите город прибытия:')
                elif not mods[str(chat_id)]['city_to']:
                    mods[str(chat_id)]['city_to'] = message
                    mods[str(chat_id)]['is_start'] = False
                    with open("mods.json", "w") as read_file:
                        json.dump(mods, read_file)
                    return send_message(chat_id, 'Вы успешно указали город прибытия: ' + message + '\nВы упешно ввели все данные')
            else:
                return send_message(chat_id, 'Я не понимаю что вы от меня хотите')


if __name__ == '__main__':
    while True:
        main()