import re


def creating_caption_product(link, link_text, start_price, min_price, price):
    url_pattern = r'https://[\S]+'
    urls = re.findall(url_pattern, link)
    print(urls)
    caption = f'<a href="{urls[0]}"><b>{link_text}</b></a>\n\n' \
              f'<b>Начальная цена: </b>{start_price} руб.\n' \
              f'<b>Минимальная цена: </b>{min_price} руб.\n' \
              f'<b>Текущая цена: </b>{price} руб.'
    return caption


def creating_text_help(name_user):
    caption = f'<b>Привет👋, {name_user}</b>\n' \
              f'💜Этот бот предназначен ' \
              f'для отслеживания цены товаров на ' \
              f'онлайн-маркетплейсе Wildberries.\n\n' \
              f'💜Бот автоматически проверяет актуальную цену выбранного вами товара и ' \
              f'в случае ее уменьшения, отправляет вам уведомление.\n\n' \
              f'💜Теперь вы можете быть в курсе последних изменений цен и не упустить выгодную сделку на Wildberries!\n\n' \
              f'<b>Инструкция</b>\n' \
              f'💜Чтобы отслеживать товар, скиньте ссылку на товар в чат с ботом.\n\n' \
              f'💜У каждого пользователя есть личный кабинет в котором можно:\n' \
              f'✅увидеть информацию о вашем текущем тарифе и балансе\n' \
              f'✅подключить расширенный тариф\n' \
              f'✅пополнить свой баланс'
    return caption


def creating_text_useful():
    pass
