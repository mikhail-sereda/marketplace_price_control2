
def creating_caption_product(link, link_text, start_price, min_price, price):
    caption = f'<a href="{link}"><b>{link_text}</b></a>\n\n' \
              f'<b>Начальная цена: </b>{start_price} руб.\n' \
              f'<b>Минимальная цена: </b>{min_price} руб.\n' \
              f'<b>Текущая цена: </b>{price} руб.'
    return caption


def creating_text_help():
    pass


def creating_text_useful():
    pass
