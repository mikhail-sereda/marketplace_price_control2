from aiogram import Router, types, F
from aiogram.filters import CommandStart

from keyboards.kb_user import kb_main_user
from data import orm
from utils.parser1 import img_by_id, all_pars
from filters.my_filter import CheckTariff, CheckLink
from static.caption import creating_caption_product

router: Router = Router()


@router.message(CommandStart())
async def start_other(msg: types.Message):
    """при входе нового пользователя добавляет в БД"""
    orm.db_add_user(msg.from_user.id)
    await msg.answer(text=f'Привет {msg.from_user.first_name}', reply_markup=kb_main_user)


@router.message(F.text == 'Помощь')
async def help_all(msg: types.Message):
    """Обрабатывает кнопку помощь для всех пользователей"""
    await msg.answer(text=f'<b>Привет👋, {msg.from_user.first_name}</b>\n'
                          f'💜Этот бот предназначен '
                          f'для отслеживания цены товаров на '
                          f'онлайн-маркетплейсе Wildberries.\n\n'
                          f'💜Бот автоматически проверяет актуальную цену выбранного вами товара и '
                          f'в случае ее уменьшения, отправляет вам уведомление.\n\n'
                          f'💜Теперь вы можете быть в курсе последних изменений цен и не упустить выгодную сделку на Wildberries!\n\n'
                          f'<b>Инструкция</b>\n'
                          f'💜Чтобы отслеживать товар, скиньте ссылку на товар в чат с ботом.\n\n'
                          f'💜У каждого пользователя есть личный кабинет в котором можно:\n'
                          f'✅проверить текущее количество ваших товаров и сколько из них отслеживается\n'
                          f'✅увидеть информацию о вашем текущем тарифе и балансе\n'
                          f'✅подключить расширенный тариф\n'
                          f'✅пополнить свой баланс', reply_markup=kb_main_user)


@router.message(F.text == 'Полезное')
async def useful(msg: types.Message):
    """Обрабатывает кнопку полезное для всех пользователей"""
    await msg.answer(text=f'В скором времени сдесь появятся ссылки на полезные ресурсы', reply_markup=kb_main_user)


@router.message(CheckLink(), CheckTariff())
async def parsing_link(msg: types.Message):
    """Получает ссылку на wildber выбирает id передаёт парсеру и записывает в бд"""
    product_dict = {'user_id': msg.from_user.id, 'link': msg.text}
    url_list = msg.text.split('/')
    id_prod = list(
        filter(lambda x: x.isnumeric(), url_list))  # список строк состоящих из цифр из переданного сообщенния
    try:
        prod_info = all_pars(id_prod[0])
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
        else:
            await msg.answer(text='Ссылка уже отслеживается')
    except:
        await msg.answer(text='Не верная ссылка')


# @router.message()
# async def processing_other_messages(msg: types.Message):
#     """обрабатывает прочие сообщения"""
#     await msg.answer(text=f'Я вас не понимаю!!!', reply_markup=kb_main_user)
