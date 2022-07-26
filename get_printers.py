import requests
from bs4 import BeautifulSoup as bs
import re
import random


offices = dict()
addr = ['Маяковского, 8', 'Игнатенко, 13', 'Одоевского, 48',
        'Короткевича, 5', 'Семашко, 1', 'Кулешова, 6',
        'Якубова, 10', 'Солтыса, 177', 'Независимости, 95']
for i in range(1, len(addr)+1):
    offices[f'Офис_{i}'] = addr[i-1]

def get_last(url_first):
    r = requests.get(url_first)
    soup = bs(r.text, 'lxml')
    url_last = 'https://tm.by'+soup.find('li',  class_="pager-last").find('a').attrs['href']
    r = requests.get(url_last)
    soup = bs(r.text, 'lxml')
    last_page = soup.find('li',  class_="active").find('span').text

    return int(last_page)


def get_printers():
    url = 'https://tm.by/printery-i-mfu?f[]=categories:26901&f[]=categories:26900&f[]=categories:26857&items_per_page=25'
    r = requests.get(url)
    last_page = get_last(url)
    printers = [[], [], [], []]
    printer_id = 1
    for i in range(0, last_page):
        if i == 0:
            url = url
        else:
            url = f'{url}&page={i}'
        r = requests.get(url)
        soup = bs(r.text, 'lxml')
        names = soup.find_all('div', class_=re.compile(r'h4'), limit =25)
        specs = soup.find_all('div', class_="field field-name-field-parameters clearfix")
        prices = soup.find_all('div', class_=re.compile('.*display-price'))
        amount = min(len(names), len(specs), len(prices))
        for k in range(0, random.randint(amount, amount*2)):
            print(k)
            g = random.randint(0, amount-1)
            number = prices[g].text.translate(prices[g].text.maketrans('', '', ' '))[:-1]
            try:
                number = float(number)
            except ValueError:
                if names[g].text in printers[1]:
                    printers[3].append(printers[3][printers[1].index(names[g].text)])
                else:
                    printers[3].append(round((random.uniform(500, 2000)), 2))
            else:
                printers[3].append(number)
            printers[1].append(names[g].text)
            printers[0].append(printer_id)
            printer_id += 1
            items = specs[g].find_all('div',  class_="field-items")
            word = 'Бренд:'+ items[0].text+', Артикул производителя:'+items[0].text
            printers[2].append(word)
            word = ''


    with open('Printers.txt', 'w', encoding='utf-8') as file:
        techs = {}
        for i in range(0, len(printers[0])):
            office_key = random.choice(list(offices))
            techs[printers[0][i]] = [printers[1][i], printers[2][i],office_key,offices[office_key], printers[3][i]]
            file.write('{}|{}|{}|{}|{}|{}\n'.format(printers[0][i], printers[1][i], printers[2][i],office_key,offices[office_key], printers[3][i]))

    return techs, offices
