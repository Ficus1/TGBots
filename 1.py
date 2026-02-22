import requests
from bs4 import BeautifulSoup
from random import choice


text = 'Кот'
api_token = '5201995653:AAH1cTZhkd8TB-MYR9B6S8eTnKurCNahLn4'
URL = "https://api.telegram.org/bot" + api_token
r = requests.get(f"https://yandex.ru/images/search?from=tabbar&text={text}")
soup = BeautifulSoup(r.text, 'html.parser')
link = choice(soup.findAll(attrs={'class': 'serp-item__thumb justifier__thumb'}))
with open(f'1.png', 'wb') as f:
    f.write(requests.get('http:' + link['src']).content)


def load_audio(text, chat_id='1'):
    r = requests.get(f"https://ru.hitmotop.com/search?q={text.replace(' ', '+')}")
    soup = BeautifulSoup(r.text, 'html.parser')
    link = choice(soup.findAll(attrs={'class': 'track__download-btn'})[::2])
    url = link['href']
    return url


def send_audio(chat_id, url):
    try:
        audio = requests.post(URL + '/sendAudio', data={'chat_id': chat_id, 'audio': requests.get(url).content})
        print(audio.json())
    except Exception:
        pass