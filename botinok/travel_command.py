import requests, json, csv


token = 'f9342c623cab0ec77ea90e8d96d04bee'


def get_IATA(city_from, city_to):
    data = requests.get(f'https://www.travelpayouts.com/widgets_suggest_params?q='
                          f'{city_from.capitalize()} {city_to.capitalize()}').json()
    try:
        IATA_from, IATA_to = data['origin']['iata'], data['destination']['iata']
    except Exception:
        return 'Я не смог найти один из этих городов', None
    return IATA_from, IATA_to


def get_avia_price(city_from, city_to, date):
    IATA_from, IATA_to = get_IATA(city_from, city_to)
    if not IATA_to:
        return 'Вы непраильно указали данные'
    data = requests.get(f'https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={IATA_from}&destination={IATA_to}&currency=rub&departure_at={date}&sorting=price&direct=true&limit=10&token=f9342c623cab0ec77ea90e8d96d04bee').json()

    if len(data['data']) == 0:
        return 'Нет такого рейса'
    min_value = min([i['price'] for i in data['data']])
    return int(min_value)


def get_stations(city_from, city_to):
    with open('tutu_routes.csv', encoding='utf-8') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
     station_from_id, station_to_id = 0, 0
     for row in spamreader:
        if city_to.capitalize() == row[1] or city_to.capitalize() == row[3]:
            station_to_id = row[0]
        if city_from.capitalize() == row[1] or city_from.capitalize() == row[3]:
            station_from_id = row[0]
    if station_to_id == 0:
        return 'Вы неправильно ввели город прибытия или в этот город не ходят поезда', None
    if station_from_id == 0:
        return 'Вы неправильно ввели город отправки или в этот город не ходят поезда', None
    return station_from_id, station_to_id


def get_train_price(city_from, city_to):
    ID_from, ID_to = get_stations(city_from, city_to)
    values = []
    if not ID_from:
        return 'Такого рейса нет'
    if not ID_to:
        return ID_from
    data = requests.get(f'https://suggest.travelpayouts.com/search?service=tutu_trains&'
                        f'term={ID_from}&term2={ID_to}').json()
    categories = {'lux': 'Люкс', 'coupe': 'Купе', 'sedentary': 'Сидячий', 'plazcard': 'Плацкарт', 'soft': 'Мягкий'}
    if len(data) == 0:
        return 'Вы неправильно указали данные'
    for i in data['trips'][0]['categories']:
        values.append((categories.get(i['type']), i['price']))
    return values


print(get_train_price('Москва', 'Чебоксары'))