import sqlite3


conn = sqlite3.connect('routes.db')
date = '2022-06-01'
town_to = 'Казань'
town_from = 'Москва'


def get_data(town_from, town_to, date):
    cur = conn.cursor()
    cur.execute(f'''Select price from route where date = "{date}" and town_to in ('{town_from}', '{town_to}') and town_from in ('{town_from}', '{town_to}')''')
    results = cur.fetchall()
    if results:
        return int(results[0][0])
    return 'Такого рейса не существует'


print(get_data(town_from, town_to, date))