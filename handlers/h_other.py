from aiogram import Router, types, F
from aiogram.filters import CommandStart

from create_bot import bot
from keyboards.kb_user import kb_main_user
from data import orm
from utils.parser1 import img_by_id, get_data_product
from filters.my_filter import CheckTariff, CheckLink
from static.caption import creating_caption_product, creating_text_help

router: Router = Router()


@router.message(CommandStart())
async def start_other(msg: types.Message):
    """при входе нового пользователя добавляет в БД"""
    orm.db_add_user(msg.from_user.id)
    await msg.answer(text=creating_text_help(msg.from_user.first_name), reply_markup=kb_main_user)


@router.message(F.text == '🆘Помощь')
async def help_all(msg: types.Message):
    """Обрабатывает кнопку 🆘Помощь для всех пользователей"""
    await msg.answer(text=creating_text_help(msg.from_user.first_name), reply_markup=kb_main_user)


@router.message(F.text == 'Полезное')
async def useful(msg: types.Message):
    """Обрабатывает кнопку полезное для всех пользователей"""
    await msg.answer(text=f'В скором времени сдесь появятся ссылки на полезные ресурсы', reply_markup=kb_main_user)


@router.message(CheckLink(), CheckTariff())
async def parsing_link(msg: types.Message):
    """Получает ссылку на wildber выбирает id передаёт парсеру и записывает в бд"""
    product_dict = {'user_id': msg.from_user.id, 'link': msg.text}
    url_list = msg.text.split('/')
    #TODO Придумать как эффективней вытащить ID из ссылки
    id_prod = list(
        filter(lambda x: x.isnumeric(), url_list))  # список строк состоящих из цифр из переданного сообщенния
    try:
        prod_info = get_data_product(id_prod[0])
        product_dict.update(prod_info)
        product_dict['min_price'] = prod_info['price']
        product_dict['start_price'] = prod_info['price']
        product_dict['pars_price'] = prod_info['price']
        img_link = img_by_id(id_prod[0])
        product_dict['photo_link'] = img_link
        if orm.db_add_product(product_dict):
            await msg.answer_photo(photo=img_link,
                                   caption=creating_caption_product(link=product_dict['link'],
                                                                    link_text=product_dict['name_prod'],
                                                                    start_price=product_dict['min_price'],
                                                                    min_price=product_dict['start_price'],
                                                                    price=product_dict['pars_price']))
            if prod_info['price'] == 9999999:
                await bot.send_message(chat_id=msg.chat.id, text='<b>⚠️Не удалось получить цену товара.</b>\n'
                                                                 'Возможно товар закончился🤷\n'
                                                                 'Когда товар появится в продаже бот пришлёт сообщение о изменении цены.')

        else:
            # TODO делать проверку отслеживается ли товар до парсинга (либо предлагать изменить стартовую цену)
            await msg.answer(text='Ссылка уже отслеживается')
    except:
        await msg.answer(text='Не верная ссылка')


@router.message()
async def processing_other_messages(msg: types.Message):
    """обрабатывает прочие сообщения"""
    await msg.answer(text=f'Я вас не понимаю!!!', reply_markup=kb_main_user)
