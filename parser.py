# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent


url_get = 'https://card.wb.ru/cards/detail?spp=0&regions=80,4,38,70,69,86,30,40,48,1,' \
          '112&pricemarginCoeff=1&reg=0&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=' \
          '2,12,7,6,9,21,11&dest=-1221185,-147166,-1749247,123585533&nm='


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
    basket =''
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
    s = f'https://basket-{basket}.wb.ru/vol{short_id}/part{int(id_ph)// 1000}/{id_ph}/images/c246x328/1.jpg'
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
    a = ['id', 'name']
    dict_bd = {}
    for i in js_dict['data']['products'][0].items():
        if i[0] in a:
            dict_bd.setdefault(i[0], i[1])
    try:
        dict_bd.setdefault('basicPriceU', js_dict['data']['products'][0]['extended']['basicPriceU'])
    except KeyError:
        dict_bd.setdefault('basicPriceU', js_dict['data']['products'][0]['priceU'])
    return dict_bd


def all_pars(url):
    """При первом парсенге ссылки"""
    id_all = defines_product_id(url)
    lin = img_by_id(str(id_all))
    a = generates_link_request(id_all)
    all_bd = (selects_values(a))
    all_bd.setdefault('link_photo', lin)
    all_bd.setdefault('link', url.split('\n')[-1])
    return all_bd


def parsing_evry_day(url):
    """проверка изменения цены"""
    id_all = defines_product_id(url)
    a = generates_link_request(id_all)
    all_bd = (selects_values(a))
    return all_bd

