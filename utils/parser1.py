# -*- coding: utf-8 -*-
import pprint
import threading

import requests
from fake_useragent import UserAgent
import asyncio

from create_bot import bot
from data import orm
from static.caption import creating_caption_product

url_get0 = 'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=29&nm='
url_get = "https://u-card.wb.ru/cards/v4/detail?appType=1&curr=rub&dest=-1275608&spp=30&ab_testing=false&ab_testing=false&lang=ru&nm=492575882"


def defines_product_id(urls_user: str):
    """Из url id товара"""
    try:
        url_list = urls_user.split('/')
        id_prod = filter(lambda x: x.isnumeric(), url_list)
        return list(id_prod)[0]
    except IndexError:
        return False

def get_basket(short_id):
    basket = ''
    match short_id:
        case num if 0 <= short_id <= 143:
            basket = "01"
        case num if short_id <= 287:
            basket = "02"
        case num if short_id <= 431:
            basket = "03"
        case num if short_id <= 719:
            basket = "04"
        case num if short_id <= 1007:
            basket = "05"
        case num if short_id <= 1061:
            basket = "06"
        case num if short_id <= 1115:
            basket = "07"
        case num if short_id <= 1169:
            basket = "08"
        case num if short_id <= 1313:
            basket = "09"
        case num if short_id <= 1601:
            basket = "10"
        case num if short_id <= 1655:
            basket = "11"
        case num if short_id <= 1919:
            basket = "12"
        case num if short_id <= 2045:
            basket = "13"
        case num if short_id <= 2189:
            basket = "14"

        case num if short_id <= 2405:
            basket = "15"

        case num if short_id <= 2621:
            basket = "16"

        case num if short_id <= 2837:
            basket = "17"

        case num if short_id <= 3053:
            basket = "18"

        case num if short_id <= 3269:
            basket = "19"

        case num if short_id <= 3485:
            basket = "20"

        case num if short_id <= 3701:
            basket = "21"

        case num if short_id <= 3917:
            basket = "22"

        case num if short_id <= 4133:
            basket = "23"

        case num if short_id <= 4349:
            basket = "24"

        case num if short_id <= 4565:
            basket = "25"

        case num if short_id <= 4877:
            basket = "26"

        case num if short_id <= 5189:
            basket = "27"

        case num if short_id <= 5501:
            basket = "28"

        case num if short_id <= 5813:
            basket = "29"

        case num if short_id <= 6125:
            basket = "30"

        case num if short_id <= 6437:
            basket = "31"

        case _:
            basket = "32"
    return basket


def img_by_id(id_ph):
    """формирует ссылу на фото товара"""
    headers = {'User-Agent': UserAgent().chrome}
    short_id = int(id_ph) // 100000
    basket = get_basket(short_id)

    s = f'https://basket-{basket}.wbbasket.ru/vol{short_id}/part{int(id_ph) // 1000}/{id_ph}/images/c246x328/1.webp'
    try:
        requests.get(s, headers)
        return s
    except:
        s = 'https://sizprom.ru/image/cache/files/no-img_1488-1200x800.jpg'
        return s


def generates_link_request(id_prod):
    """ get запрос по id, возращает словарь с полным описанием товара"""
    headers = {'User-Agent': UserAgent().chrome}
    params = {"appType": "1",
             "curr": "rub",
             "dest": "-1275608",
             "spp": "30",
             "ab_testing": "false",
             "lang": "ru",
             "nm": id_prod}
    url_get_card_json = "https://u-card.wb.ru/cards/v4/detail"
    req = requests.get(url_get_card_json, params=params, headers=headers,)
    return req.json()


def selects_values(js_dict):
    """Выбирает нужные характеристики"""
    dict_bd = dict()
    dict_bd['id_prod'] = js_dict['products'][0]['id']
    dict_bd['name_prod'] = js_dict['products'][0]['name']
    try:
        if int(js_dict['products'][0]['sizes'][0]['price']['product']) > 0:
            dict_bd['price'] = int(js_dict['products'][0]['sizes'][0]['price']['product']) / 100
        else:
            dict_bd['price'] = int(js_dict['products'][0]['sizes'][0]['price']['basic']) / 100
    except KeyError:
        dict_bd['price'] = 9999999
    return dict_bd


def get_data_product(id_all):
    """При первом парсенге ссылки"""
    a = generates_link_request(id_all)
    all_bd = selects_values(a)
    return all_bd


def parsing_all_price():
    """Парсит цены и сравнивает их с ценой и мин ценой в БД. Если изменено перезаписывает"""
    all_product = orm.db_get_all_product()  # только активные продукты
    for i in all_product:
        js_dict = generates_link_request(i.id_prod)
        if js_dict['products']:
            try:
                if int(js_dict['products'][0]['sizes'][0]['price']['product']) > 0:
                    price = int(js_dict['products'][0]['sizes'][0]['price']['product']) / 100
                else:
                    price = int(js_dict['products'][0]['sizes'][0]['price']['basic']) / 100
            except KeyError:
                price = i.pars_price
            if i.pars_price != price:
                orm.db_adjusts_pars_price(id_prod=i.id, price=price)


async def sends_price_change_message():
    """Проверяет цену после парсинга с сохранёнными ценами, если цена снижена относительно стартовой сообщает пользователя
    если выше статовой, то перезаписывает текущую цену"""
    mod_products = orm.db_get_modified_products()
    for product in mod_products:
        caption = creating_caption_product(link=product.link,
                                           link_text=product.name_prod,
                                           start_price=product.start_price,
                                           min_price=product.min_price,
                                           price=product.pars_price)
        if product.pars_price >= product.start_price and product.pars_price != product.price:
            orm.db_adjusts_price(id_prod=product.id,
                                 price=product.pars_price)

        elif product.start_price > product.pars_price > product.price:
            orm.db_adjusts_price(id_prod=product.id,
                                 price=product.pars_price)
        elif product.pars_price < product.start_price \
                and product.pars_price < product.price \
                and product.pars_price < product.min_price:
            orm.db_adjusts_price(id_prod=product.id,
                                 price=product.pars_price,
                                 min_price=product.pars_price)
            try:
                await bot.send_photo(chat_id=product.user_id,
                                     photo=product.photo_link,
                                     caption=f'{caption}\n\n'
                                             f'Цена снижена на {100 - ((product.pars_price * 100) // product.start_price)}%\n'
                                             f'Цена минимальная с момента отслеживания')
            except:
                orm.db_changes_user_activ(id_user=product.user_id, activ=0)

        elif product.start_price > product.pars_price >= product.min_price \
                and product.pars_price < product.price:
            orm.db_adjusts_price(id_prod=product.id,
                                 price=product.pars_price)
            try:
                await bot.send_photo(chat_id=product.user_id,
                                     photo=product.photo_link,
                                     caption=f'{caption}\n\n'
                                             f'Цена снижена на {100 - ((product.pars_price * 100) // product.start_price)}%\n')
            except:
                orm.db_changes_user_activ(id_user=product.user_id, activ=0)


async def parsing_price_thread(wait_for):
    """Запускает новый поток для парсинга"""
    while True:
        await asyncio.sleep(wait_for)
        parsing = threading.Thread(target=parsing_all_price)
        parsing.start()
        await sends_price_change_message()
