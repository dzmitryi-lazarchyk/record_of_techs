import requests
from bs4 import BeautifulSoup as bs
import re
import random

def get_id():
    """Function searches file 'techs.txt' for id's. If it finds some, it returns
    next ordinal id. Otherwise, function returns 1."""
    techs = dict()
    try:
        with open('techs.txt', 'r', encoding='utf-8') as file:
    except FileNotFoundError:
        techs = get_techs()
    else:
        for line in file:
            if re.search(r'.+\|.+\|.+\|.+\|.+\|.+', line):
                list_techs = line.split('|')
                techs[list_techs[0]] = [list_techs[1:]]
            else:
                continue
    finally:
        all_id = set(techs.keys())
        if all_id:
            stencil = set([i for i in range(1, len(all_id) + 3)])
            return min(stencil - all_id)
        else:
            return 1


def get_offices():
    offices = dict()
    try:
        with open('offices.txt', 'r', encoding='utf-8') as file:
    except FileNotFoundError:
        addr = ['Маяковского, 8', 'Игнатенко, 13', 'Одоевского, 48',
                'Короткевича, 5', 'Семашко, 1', 'Кулешова, 6',
                'Якубова, 10', 'Солтыса, 177', 'Независимости, 95']
        for i in range(1, len(addr) + 1):
            offices[f'Офис_{i}'] = addr[i - 1]
    else:
        for line in file:
            if re.search(r'.+\|.+', line):
                list_offices = line.split('|')
                offices[list_offices[0]] = list_offices[1]
            else:
                continue
    return offices


def get_last(url_first):
    """Function takes in url of the first page and returns url of the last one."""
    r = requests.get(url_first)
    soup = bs(r.text, 'lxml')
    url_last = 'https://tm.by'+soup.find('li',  class_="pager-last").find('a').attrs['href']
    r = requests.get(url_last)
    soup = bs(r.text, 'lxml')
    last_page = soup.find('li',  class_="active").find('span').text

    return int(last_page)


def get_techs():
    techs = dict()
    try:
        with open('techs.txt', 'r', encoding='utf-8') as file:
    except FileNotFoundError:
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

        with open('techs.txt', 'w', encoding='utf-8') as file:
            offices = get_offices()
            for i in range(0, len(printers[0])):
                office_key = random.choice(list(offices))
                techs[printers[0][i]] = [printers[1][i], printers[2][i],office_key,offices[office_key], printers[3][i]]
                file.write('{}|{}|{}|{}|{}|{}\n'.format(printers[0][i], printers[1][i], printers[2][i],office_key,offices[office_key], printers[3][i]))
    else:
        for line in file:
            if re.search(r'.+\|.+\|.+\|.+\|.+\|.+', line):
                list_techs = line.split('|')
                techs[list_techs[0]] = [list_techs[1:]]
            else:
                continue
    return techs

get_techs()
