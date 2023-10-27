from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.kb_user import kb_main_user
from keyboards.ikb_user import gen_markup_pagination, gen_markup_profile, gen_markup_users_tariff, \
    gen_markup_replenishes, gen_markup_consent
from keyboards.ikb_admin import gen_markup_cancel_fsm, gen_markup_ok_pay
from filters.my_filter import UserFilt, AdmFilter
from data import orm
from data.FSMbot.FSMusers import ChequeFSM
from data.orm import ADMIN_ID
from create_bot import bot
from static.caption import creating_caption_product, creating_text_help

router: Router = Router()


@router.message(UserFilt(), CommandStart())
async def start_user(msg: types.Message):
    """При входе зарегистрированого пользователя проверяет данные в БД"""
    orm.db_add_user(msg.from_user.id)
    await msg.answer(text=creating_text_help(msg.from_user.first_name), reply_markup=kb_main_user)


@router.message(F.text == 'Мои товары', AdmFilter())
async def user_products(msg: types.Message):
    """Кнопка Мои товары"""
    tracked_items = orm.db_get_tracked_items(msg.from_user.id)
    all_product = orm.db_get_user_product(msg.from_user.id)[0:tracked_items]
    if all_product:
        page_number = 0
        await msg.answer_photo(photo=all_product[page_number].photo_link,
                               caption=creating_caption_product(link=all_product[page_number].link,
                                                                link_text=all_product[page_number].name_prod,
                                                                start_price=all_product[page_number].start_price,
                                                                min_price=all_product[page_number].min_price,
                                                                price=all_product[page_number].price),
                               reply_markup=await gen_markup_pagination(str(all_product[page_number].id),
                                                                        len(all_product),
                                                                        page_number=page_number))
    else:
        await msg.answer(text=f'У вас нет сохранённых товаров')


@router.callback_query(lambda x: x.data.startswith('track'))
async def product_pagination(callback: types.CallbackQuery):
    """Обработка кнопокки пагинации моих товаров"""
    inl_col = callback.data.split(':')
    tracked_items = orm.db_get_tracked_items(callback.from_user.id)
    all_product = orm.db_get_user_product(callback.from_user.id)[0:tracked_items]
    page_number = int(inl_col[1])
    photo = types.InputMediaPhoto(media=all_product[page_number].photo_link,
                                  caption=creating_caption_product(link=all_product[page_number].link,
                                                                   link_text=all_product[page_number].name_prod,
                                                                   start_price=all_product[page_number].start_price,
                                                                   min_price=all_product[page_number].min_price,
                                                                   price=all_product[page_number].price))

    await callback.message.edit_media(media=photo,
                                      reply_markup=await gen_markup_pagination(
                                          str(all_product[page_number].id),
                                          len(all_product),
                                          page_number=page_number))
    await callback.answer()


@router.callback_query(lambda x: x.data.startswith('delall'))
async def del_all_product(callback: types.CallbackQuery):
    """обрабатывает кнопку Удаление товара при удалении последнего товара"""
    inl_col = callback.data.split(':')
    orm.db_dell_product(int(inl_col[1]))
    await callback.message.delete()
    await callback.answer(text='нет товаров')  # удаляем сообщеие с пагинацией и удаляем последний товар
    await callback.answer()


@router.callback_query(lambda x: x.data.startswith('delpr'))
async def del_product(callback: types.CallbackQuery):
    """Обрабатывает кнопку Удаление товара если в списке больше однго товара"""
    inl_col = callback.data.split(':')
    orm.db_dell_product(int(inl_col[1]))  # удаляет товар из бд
    tracked_items = orm.db_get_tracked_items(callback.from_user.id)
    orm.db_disables_product_tracking(id_user=callback.from_user.id, tracked_items=tracked_items)
    all_product = orm.db_get_user_product(callback.from_user.id)[0:tracked_items]
    page_number = int(inl_col[2])
    await callback.answer(text=f'Кнопка', reply_markup=kb_main_user)
    photo = types.InputMediaPhoto(media=all_product[page_number].photo_link,
                                  caption=creating_caption_product(link=all_product[page_number].link,
                                                                   link_text=all_product[page_number].name_prod,
                                                                   start_price=all_product[page_number].start_price,
                                                                   min_price=all_product[page_number].min_price,
                                                                   price=all_product[page_number].price))
    await callback.message.edit_media(media=photo,
                                      reply_markup=await gen_markup_pagination(str(all_product[page_number].id),
                                                                               len(all_product),
                                                                               page_number=page_number))
    await callback.answer()


@router.message(F.text == 'Профиль')
async def get_user_profile(msg: types.Message):
    """Кнопка Профиль"""
    id_user = msg.from_user.id
    profile_user = orm.db_get_profile(id_user)
    count = orm.db_get_count_product_user(id_user)
    await msg.answer(text=f'<b>___Профиль___</b>\n\n'
                          f'<b>Имя: </b>{msg.from_user.first_name}\n\n'
                          f'<b>ID: </b>{id_user}\n\n'
                          f'<b>Количество ваших товаров: </b>{count}\n\n'
                          f'<b>Товаров отслеживается: </b>'
                          f'{profile_user.tracked_items if count >= profile_user.tracked_items else count}\n\n'
                          f'<b>Тариф: </b>{profile_user.tariff_user} (до {profile_user.tracked_items} ссылок.)\n\n'
                          f'<b>Баланс: </b>{profile_user.balance} руб.\n\n',
                     reply_markup=await gen_markup_profile())


@router.callback_query(lambda x: x.data.startswith('u_tariff'))
async def get_tariff_for_users(callback: types.CallbackQuery):
    """Показывает активные тарифы и кнопки подключения юзеру"""
    active_tariff = orm.db_get_tariffs(1)
    text_tariffs = f'Срок действия тарифов 180 дней.\n{"➖" * 10}\n'
    name_tariffs = []
    for text in active_tariff:
        text_tariffs += f'<b><u>{text.name_tariff}</u></b>\n\n' \
                        f'До {text.tracked_items} ссылок\n' \
                        f'Стоимость {text.price_tariff} руб.\n' \
                        f'{"➖" * 10}\n'
        name_tariffs.append([text.name_tariff, text.id])
    await callback.message.answer(text=text_tariffs, reply_markup=await gen_markup_users_tariff(name_tariffs))
    await callback.answer()


@router.callback_query(lambda x: x.data.startswith('plugtariff'))
async def connects_tariff(callback: types.CallbackQuery):
    """Обработка кнопок изменения тарифа с проверкой и изменением баланса."""
    inl_col = callback.data.split(':')
    tariff = orm.db_get_one_tariff(int(inl_col[1]))
    profile_user = orm.db_get_profile(callback.from_user.id)
    if profile_user.tariff_user == tariff.name_tariff:
        await callback.message.answer(f'У вас уже подключен тариф {tariff.name_tariff}')
        await callback.answer()
    elif profile_user.balance < tariff.price_tariff:
        await callback.message.answer(f'У вас недостаточно средств на счету.', reply_markup=await gen_markup_profile())
        await callback.answer()
    else:
        await callback.message.answer(text=f'Ваш текущий тариф {profile_user.tariff_user}\n'
                                           f'Можно отслеживать до {profile_user.tracked_items} ссылок.\n\n'
                                           f'Подключить тариф {tariff.name_tariff}?\n'
                                           f'Вы сможете отслеживать до {tariff.tracked_items} ссылок',
                                      reply_markup=await gen_markup_consent(tariff.id))


@router.callback_query(lambda x: x.data.startswith('t_change'))
async def confirms_tariff(callback: types.CallbackQuery):
    """Обработка кнопок подтверждения изменения тарифа."""
    inl_col = callback.data.split(':')
    if int(inl_col[1]):
        tariff = orm.db_get_one_tariff(int(inl_col[2]))
        profile_user = orm.db_get_profile(callback.from_user.id)
        orm.db_disables_product_tracking(id_user=callback.from_user.id, tracked_items=tariff.tracked_items)
        orm.db_changes_user_tariff(name_tariff=tariff.name_tariff,
                                   id_user=callback.from_user.id,
                                   tracked_items=tariff.tracked_items,
                                   balance=profile_user.balance - tariff.price_tariff)
        await callback.answer(text=f'👍Тариф {tariff.name_tariff} успешно подключен.👍\n'
                                           f'❤️Вы можете отслеживать до {tariff.tracked_items} ссылок', show_alert=True)
        await callback.message.delete()
    else:
        await callback.message.delete()


@router.callback_query(lambda x: x.data.startswith('money'))
async def replenishes_account(callback: types.CallbackQuery):
    """Обрабатывает кнопку пополнить баланс"""
    await callback.message.answer(
        f'<u>💰Для пополнения баланса:💰</u>\n\n'
        f'✅ Оплатите необходимую сумму.\n(перевод на карту <b>4279017009175522</b>)\n'
        f'✅ Cохраните чек.\n'
        f'✅ Нажмите на кнопку оплачено 👇 и отправьте чек об оплате.\n'
        f'✅ После проверки платежа ваш баланс будет пополнен.\n\n'
        f'❤️ За пополнение баланса комиссия не взъимается\n'
        f'❤️ О пополнении баланса мы вам пришлём уведомление.\n'
        f'❤️ Проверка платежа поизводится в ручную и занимает от 10 мин до 8 часов.\n'
        f'Спасибо за использование бота!',
        reply_markup=await gen_markup_replenishes(callback.from_user.id))
    await callback.answer()


@router.callback_query(lambda x: x.data.startswith('pay'))
async def replenishes_account(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает кнопку оплачено старт FSM ожидает подтверждения платежа"""
    await callback.message.answer(text='Пришлите подтверждение платежа', reply_markup=await gen_markup_cancel_fsm())
    await state.set_state(ChequeFSM.screen_cheque)


@router.message(ChequeFSM.screen_cheque)
async def sends_payment_receipt(msg: types.Message, state: FSMContext):
    """Принимает у пользователя подтверждение оплаты и отправляет админу
     копию сообщения и сообщение с кнопками подтверждения оплаты"""
    await msg.forward(chat_id=ADMIN_ID)
    await bot.send_message(chat_id=ADMIN_ID, text=f'Пополнение баланса.\n'
                                                  f'Пользователь {msg.from_user.first_name}\n'
                                                  f'ID{msg.from_user.id}',
                           reply_markup=await gen_markup_ok_pay(msg.from_user.id))
    await state.clear()
