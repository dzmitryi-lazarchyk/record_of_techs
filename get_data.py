import requests
from bs4 import BeautifulSoup as bs
import re
import random

'''Url and parameters of query. They represent parameters for the  fetch() function.'''
first_page_url = "https://catalog.onliner.by/sdapi/catalog.api/search/printers"
first_page_params = {
    "headers": {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "if-none-match": "W/\"4cabedf3598f0a4f4a8f0f2fc3584ab3\"",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "cookie": "_ym_uid=1658842657347516120; _ym_d=1658842657; _gid=GA1.2.414116336.1658842657; tmr_lvidTS=1658842657046; tmr_lvid=602da7258815aa8661b8fe0c09472d08; _ym_isad=2; catalog_session=OUvIOt0RpZzWfyeUkCku4PWxmnSfAH9dq9mhKyQk; ouid=snyBEGLf7iyM7e7/MsloAg==; _gcl_au=1.1.263137017.1658842670; _gaexp=GAX1.2.srp5-mVGQcyzlricTjj8PQ.19211.0; _fbp=fb.1.1658842670769.1898710537; _tt_enable_cookie=1; _ttp=0032b1bd-1855-453b-9197-c509d79c238a; __gads=ID=7db29bf78bc20e6f:T=1658842742:S=ALNI_Mb6VRSbLas_w5YCea2iPbEq_ucL4A; __gpi=UID=0000092b8086402b:T=1658842742:RT=1658842742:S=ALNI_MYYptD_jxRZlVhITwtCl27k5bapDA; tmr_reqNum=10; _gat_UA-340679-1=1; _gat_UA-340679-16=1; _ga=GA1.1.1191673485.1658842657; _ga_4Y6NQKE48G=GS1.1.1658842670.1.1.1658844721.11; _ga_NG54S9EFTD=GS1.1.1658842657.1.1.1658844721.0",
        "Referer": "https://catalog.onliner.by/printers",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    },
    "body": None,
    "method": "GET"
}



def get_id():
    """Function searches file 'techs.txt' for id's. If it finds some, it returns
    next ordinal id. Otherwise, function returns 1."""
    techs = dict()
    try:
        with open('techs.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if re.search(r'.+\|.+\|.+\|.+\|.+\|.+', line):
                    list_techs = line.split('|')
                    techs[list_techs[0]] = [list_techs[1:]]
                else:
                    continue
    except FileNotFoundError:
        techs = get_techs()
    finally:
        all_id = set(techs.keys())
        if all_id:
            stencil = set([str(i) for i in range(1, len(all_id) + 3)])
            return min(stencil - all_id)
        else:
            return 1


def get_offices():
    """Function reads data from file 'offices.txt' and returns data as dictionary.
    In case if file doesn't exit, it will be created and filled with data."""
    offices = dict()
    try:
        with open('offices.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if re.search(r'.+\|.+', line):
                    list_offices = line.split('|')
                    offices[list_offices[0]] = list_offices[1][:-1]
                else:
                    continue
    except FileNotFoundError:
        addr = ['Маяковского, 8', 'Игнатенко, 13', 'Одоевского, 48',
                'Короткевича, 5', 'Семашко, 1', 'Кулешова, 6',
                'Якубова, 10', 'Солтыса, 177', 'Независимости, 95']

        with open('offices.txt', 'w', encoding='utf-8') as file:
            for i in range(1, len(addr) + 1):
                offices[f'Офис_{i}'] = addr[i - 1]
                file.write('{}|{}\n'.format(f'Офис_{i}', addr[i - 1]))

    return offices





def fetch(url, params):
    """Function takes in url and parameters for fetch request and returns
    responce of the site."""
    headers = params['headers']
    body = params['body']
    if params['method'] == 'GET':
        return requests.get(url, headers=headers)
    if params['method'] == 'POST':
        return requests.post(url, headers=headers, data=body)


def get_techs():
    """Function reads data from files 'techs.txt' and returns data as dictionary.
        In case if file doesn't exit, it will be created and filled with data using fetch()
        and get_offices() functions."""
    techs = dict()
    try:
        with open('techs.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if re.search(r'.+\|.+\|.+\|.+\|.+\|.+', line):
                    list_techs = line.split('|')
                    techs[list_techs[0]] = list_techs[1], list_techs[2], list_techs[3], list_techs[4], list_techs[5][:-1]
                else:
                    continue
    except FileNotFoundError:
        printers_info = [[], [], []]
        page = fetch(first_page_url, first_page_params)
        pages = page.json()['page']['last']
        for n in range(1, int(pages) + 1):
            if n == 1:
                page_number = ''
            else:
                page_number = '?page=' + str(n)
            page = fetch(first_page_url + page_number, first_page_params)
            items = page.json()['products']
            for item in items:
                printers_info[0].append(item['extended_name'])
                printers_info[1].append(item['micro_description'])
                if item['prices']:
                    printers_info[2].append(item['prices']['price_min']['amount'])
                else:
                    printers_info[2].append(
                        round(sum([float(price) for price in printers_info[2]]) / len(printers_info[2]), 2))

        with open('techs.txt', 'w', encoding='utf-8') as file:
            offices = get_offices()
            printer_id = 1
            for i in range(0, len(printers_info[0])):
                office_key = random.choice(list(offices))
                techs[printer_id] = [printers_info[0][i], printers_info[1][i], office_key, offices[office_key],
                                     printers_info[2][i]]
                file.write(
                    '{}|{}|{}|{}|{}|{}\n'.format(printer_id, printers_info[0][i], printers_info[1][i], office_key,
                                                 offices[office_key], printers_info[2][i]))
                printer_id += 1

    return techs

get_techs()