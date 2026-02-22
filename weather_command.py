import requests
import json
import datetime

api_key = "a6211fcdfacef78e8cff51d27f12f29b"
URL = "http://api.openweathermap.org/data/2.5/"


def wind_direction(degrees):
    wind_directions = ("северный", "северо-восточный", "восточный", "юго-восточный", "южный", "юго-западный", "западный",
                      "северо-западный")
    direction = int((degrees + 22.5) // 45 % 8)
    return wind_directions[direction]


def forecast(city):
    try:
        weather = requests.get(URL + 'forecast',
                               params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': api_key, 'lang': 'ru'})
        with open("weather.json", "w") as f:
            json.dump(weather.json(), f)
        out = []
        for i in range(9):
            data = weather.json()['list'][i]
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            weather_description = data['weather'][-1]['description']
            wind_speed = data['wind']['speed']
            wind_direct = wind_direction(data['wind']['deg'])
            date = data['dt_txt']
            out.append(f'''Прогноз погоды на {date} для города {city}
Температура: {temp}℃
Ощущается как: {feels_like}℃
Минимальная температура: {temp_min}℃
Максимальная температура: {temp_max}℃
Давление: {pressure} мм.рт.ст
Влажность: {humidity}%
Погода: {weather_description}
Ветер: {wind_speed}м/с, {wind_direct}
                ''')
        return '\n'.join(out)
    except Exception as e:
        return "Мне не удалось выполнить команду. Возможно вы забыли указать город или неправильно его указали"


def current_weather(city):
    try:
        weather = requests.get(URL + 'find',
                     params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': api_key, 'lang': 'ru'})
        with open("weather.json", "w") as f:
            json.dump(weather.json(), f)
        data = weather.json()['list'][0]
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        weather_description = data['weather'][-1]['description']
        wind_speed = data['wind']['speed']
        wind_direct = wind_direction(data['wind']['deg'])
        date = datetime.datetime.fromtimestamp(int(data['dt'])).date()
        return f'''Прогноз погоды на {date} для города {city}
Температура: {temp}℃
Ощущается как: {feels_like}℃
Минимальная температура: {temp_min}℃
Максимальная температура: {temp_max}℃
Давление: {pressure} мм.рт.ст
Влажность: {humidity}%
Погода: {weather_description}
Ветер: {wind_speed}м/с, {wind_direct}
    '''
    except Exception:
        return "Мне не удалось выполнить команду. Возможно вы забыли указать город или неправильно его указали"

forecast('Москва')