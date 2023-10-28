# -*- coding: utf-8 -*-
import threading

import requests
from fake_useragent import UserAgent
import asyncio

from create_bot import bot
from data import orm
from static.caption import creating_caption_product
url_get = 'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=29&nm='


def defines_product_id(urls_user: str):
    """Из url id товара"""
    try:
        url_list = urls_user.split('/')
        id_prod = filter(lambda x: x.isnumeric(), url_list)
        return list(id_prod)[0]
    except IndexError:
        return False


def img_by_id(id_ph):
    """формирует ссылу на фото товара"""
    headers = {'User-Agent': UserAgent().chrome}
    short_id = int(id_ph) // 100000
    basket = ''
    match short_id:
        case num if num in range(0, 144):
            basket = '01'
        case num if num in range(144, 288):
            basket = '02'
        case num if num in range(288, 432):
            basket = '03'
        case num if num in range(432, 720):
            basket = '04'
        case num if num in range(720, 1008):
            basket = '05'
        case num if num in range(1008, 1062):
            basket = '06'
        case num if num in range(1062, 1116):
            basket = '07'
        case num if num in range(1116, 1170):
            basket = '08'
        case num if num in range(1170, 1314):
            basket = '09'
        case num if num in range(1314, 1602):
            basket = '10'
        case num if num in range(1602, 1656):
            basket = '11'
        case num if num in range(1656, 1920):
            basket = '12'
        case _:
            basket = '13'  # Если _short_id не входит ни в один из предыдущих диапазонов, присвоить '13' basket-у
    s = f'https://basket-{basket}.wb.ru/vol{short_id}/part{int(id_ph) // 1000}/{id_ph}/images/c246x328/1.jpg'
    try:
        requests.get(s, headers)
        return s
    except:
        s = 'https://avatars.mds.yandex.net/i?id=a53e9cddb18926e986bddd7acb96cd3973307967-10088009-images-thumbs&n=13'
        return s


def generates_link_request(id_prod):
    """ get запрос по id, возращает словарь с полным описанием товара"""
    headers = {'User-Agent': UserAgent().chrome}
    url_get_user = url_get + id_prod
    req = requests.get(url_get_user, headers)
    return req.json()


def selects_values(js_dict):
    """Выбирает нужные характеристики"""
    dict_bd = dict()
    dict_bd['id_prod'] = js_dict['data']['products'][0]['id']
    dict_bd['name_prod'] = js_dict['data']['products'][0]['name']
    try:
        dict_bd['price'] = js_dict['data']['products'][0]['extended']['clientPriceU'] / 100
    except KeyError:
        dict_bd['price'] = js_dict['data']['products'][0]['priceU'] / 100
    return dict_bd


def all_pars(id_all):
    """При первом парсенге ссылки"""
    a = generates_link_request(id_all)
    all_bd = (selects_values(a))
    return all_bd


def parsing_all():
    """Парсит цены и сравнивает их с ценой и мин ценой в БД. Если изменено перезаписывает"""
    all_product = orm.db_get_all_product()  # только активные продукты
    headers = {'User-Agent': UserAgent().chrome}
    for i in all_product:
        url_get_prod = url_get + str(i.id_prod)
        req = requests.get(url_get_prod, headers)
        js_dict = req.json()
        if js_dict['data']['products']:
            try:
                price = js_dict['data']['products'][0]['extended']['clientPriceU'] / 100
            except KeyError:
                price = js_dict['data']['products'][0]['priceU'] / 100
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
        parsing = threading.Thread(target=parsing_all)
        parsing.start()
        await sends_price_change_message()
