import requests
import json


api_key = 'k_9t35w5i1'
token = '5202817277:AAHtZ4ESk58YNurubjuCFYSxQBfc0uQklR4'
URL = "https://api.telegram.org/bot" + token
current_update_id = 0


def top_25_movies():
    data = requests.get('https://imdb-api.com/ru/API/Top250Movies/' + api_key).json()
    with open("film.json", "w") as f:
        json.dump(data, f)
    text = "Топ 25:"
    for i in data['items']:
        if data['items'].index(i) > 24:
            break
        text += f"{i['rank']}. {i['fullTitle']}. Cъемочная группа: {i['crew']}. Рейтинг: {i['imDbRating']}. Количество оценок: {i['imDbRatingCount']}" + '\n'
    return text


def top_25_tvs():
    data = requests.get('https://imdb-api.com/ru/API/Top250TVs/' + api_key).json()
    with open("film.json", "w") as f:
        json.dump(data, f)
    text = "Топ 25:"
    for i in data['items']:
        if data['items'].index(i) > 24:
            break
        text += f"{i['rank']}. {i['fullTitle']}. Cъемочная группа: {i['crew']}. Рейтинг: {i['imDbRating']}. Количество оценок: {i['imDbRatingCount']}" + '\n'
    return text


def most_popular_movies():
    data = requests.get('https://imdb-api.com/ru/API/MostPopularMovies/' + api_key).json()
    with open("film.json", "w") as f:
        json.dump(data, f)
    text = "Самое популярное:"
    for i in data['items']:
        if data['items'].index(i) > 24:
            break
        text += f"{i['rank']}({i['rankUpDown']}). {i['fullTitle']}. Cъемочная группа: {i['crew']}. Рейтинг: {i['imDbRating']}. Количество оценок: {i['imDbRatingCount']}" + '\n'
    return text


def most_popular_tvs():
    data = requests.get('https://imdb-api.com/ru/API/MostPopularTVs/' + api_key).json()
    with open("film.json", "w") as f:
        json.dump(data, f)
    text = "Самое популярное:"
    for i in data['items']:
        if data['items'].index(i) > 24:
            break
        text += f"{i['rank']}({i['rankUpDown']}). {i['fullTitle']}. Cъемочная группа: {i['crew']}. Рейтинг: {i['imDbRating']}. Количество оценок: {i['imDbRatingCount']}" + '\n'
    return text


def in_theaters():
    data = requests.get('https://imdb-api.com/ru/API/InTheaters/' + api_key).json()
    with open("film.json", "w") as f:
        json.dump(data, f)
    text = "Скоро в кинотеатрах:"
    for i in data['items']:
        if data['items'].index(i) > 24:
            break
        text += f"{int(data['items'].index(i)) + 1}. {i['fullTitle']}:\n" \
                f"Дата выхода в кинотеатрах: {i['releaseState']}. Жанр: {i['genres']}. Возрастное ограничение: {i['contentRating'] if i['contentRating'] else '18+'}.\n" \
                f"Сюжет: {i['plot']}.\n" \
                f"Длительность: {i['runtimeStr']}\n" \
                f"Режиссер: {i['directors']}." \
                f"Актеры: {i['stars']}." + '\n'
    return text


def coming_soon():
    data = requests.get('https://imdb-api.com/ru/API/ComingSoon/' + api_key).json()
    with open("film.json", "w") as f:
        json.dump(data, f)
    text = "Новинки:"
    for i in data['items']:
        if data['items'].index(i) > 24:
            break
        text += f"{int(data['items'].index(i)) + 1}. {i['fullTitle']}:\n" \
                f"Дата выхода: {i['releaseState']}. Жанр: {i['genres']}. Возрастное ограничение: {i['contentRating'] if i['contentRating'] else '18+'}.\n" \
                f"Сюжет: {i['plot']}.\n" \
                f"Режиссер: {i['directors']}.\n" \
                f"Актеры: {i['stars']}." + '\n'
    return text


def box_office_weekend():
    data = requests.get('https://imdb-api.com/ru/API/BoxOffice/' + api_key).json()
    with open("film.json", "w") as f:
        json.dump(data, f)
    text = "Кассовые сборы:"
    for i in data['items']:
        if data['items'].index(i) > 24:
            break
        text += f"{i['rank']}. {i['title']}:\n" \
                f"На этой неделе: {i['weekend']}\n" \
                f"Всего: {i['gross']}" + '\n'

    return text


def box_office_all():
    data = requests.get('https://imdb-api.com/ru/API/BoxOfficeAllTime/' + api_key).json()
    with open("film.json", "w") as f:
        json.dump(data, f)
    text = "Кассовые сборы:"
    for i in data['items']:
        if data['items'].index(i) > 24:
            break
        text += f"{i['rank']}. {i['title']} ({i['year']}):\n" \
                f"Всего: {i['worldwideLifetimeGross']}" + '\n'
    return text


def get_updates():
    update = requests.get(URL + '/getupdates').json()
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
    with open('last_update_id.txt', 'w') as f:
        f.write(str(current_update_id))
    return chat_id, message


def send_message(chat_id, text="Hello"):
    try:
        reply_markup = {"keyboard": [["/help", '/top25movies', '/top25tvs'], ["/mostpopularmovies", "/mostpopulartvs", '/intheater'],
                                     ['/comingsoon', '/boxoffiice', '/boxofficeall']], "one_time_keyboard": False}
        message = requests.post(URL + '/sendMessage',
                                data={'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)})
    except Exception:
        pass


def run_command(chat_id, command='help'):
    if command == 'help':
        return send_message(chat_id, f'''Список доступных команд
/help - Вывести список доступных команд
/top25movies - Вывести топ 25 фильмов
/top25tvs - Вывести топ 25 сериалов
/mostpopularmovies - Вывести 25 самых] популярных фильмов
/mostpopulartvs - Вывести 25 самых популярных сериалов
/intheater - Вывести фильмы, которые выходят в прокат
/comingsoon - Предстоящие новинки
/boxoffiice - Наибольшие недельные сборы
/boxofficeall - 25 самых кассовые фильмы за все время
''')
    if command == 'top25movies':
        return send_message(chat_id, top_25_movies())
    if command == 'top25tvs':
        return send_message(chat_id, top_25_tvs())
    if command == 'mostpopularmovies':
        return send_message(chat_id, most_popular_movies())
    if command == 'mostpopulartvs':
        return send_message(chat_id, most_popular_tvs())
    if command == 'intheater':
        return send_message(chat_id, in_theaters())
    if command == 'boxoffiice':
        return send_message(chat_id, box_office_weekend())
    if command == 'boxofficeall':
        return send_message(chat_id, box_office_all())
    if command == 'comingsoon':
        return send_message(chat_id, coming_soon())
    if command == 'start':
        return send_message(chat_id, 'Я могу показать информацию о фильмах и сериалах\n'
                                     'Для ознакомления с командами введите /help')
    return send_message(chat_id, "Я не знаю такую команду \nВоспользуйтесь командой /help")


def main():
    chat_id, message = get_message()
    if message and message.startswith('/'):
        run_command(chat_id, message[1:])
    else:
        if chat_id:
            send_message(chat_id, 'Введите команду /help для ознакомления с командами')


if __name__ == '__main__':
    while True:
        main()