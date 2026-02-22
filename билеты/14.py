from datetime import date
day, month, year = int(input('День ')), int(input('Месяц ')), int(input('Год '))
try:
    date(year, month, day)
    print('Правильные данные')
except Exception:
    print('Неправильные данные')