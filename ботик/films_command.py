import requests
import json

api_key = 'k_9t35w5i1'


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