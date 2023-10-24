from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.kb_admin import kb_main_admin
from keyboards.ikb_admin import gen_markup_category_tariff, gen_markup_cancel_fsm, gen_markup_menu_tariff
from filters.my_filter import AdmFilter
from data import orm
from data.FSMbot.FSMadmin import FiltersFSM, AddMoneyFSM, AddAdvertisementFSM
from create_bot import bot

router: Router = Router()
router.message.filter(AdmFilter())  # применяем ко всем хендлерам фильтр на админа


# https://mastergroosha.github.io/aiogram-3-guide/fsm/
@router.message(CommandStart())
async def start_admin(msg: types.Message):
    await msg.answer(text='Привет', reply_markup=kb_main_admin)


@router.message(F.text == 'Пользователи')
async def users_statist(msg: types.Message):
    """Обрабатывает кнопку Пользователи"""
    users = orm.db_get_all_users()
    await msg.answer(text=f'Всего в базе {users[0]} чел.\n'
                          f'Активные пользователи {users[1]} чел.\n'
                          f'Не активные пользователи {users[2]} чел.\n')


@router.message(F.text == 'Тарифы')
async def useful(msg: types.Message):
    """Обрабатывает кнопку тарифы"""
    await msg.answer(text=f'Тарифы', reply_markup=await gen_markup_category_tariff())


@router.callback_query(lambda x: x.data.startswith('tariff_active'))
async def returns_all_tariff_to_the_admin(callback: types.CallbackQuery):
    """Показывает активные или не активные тарифы"""
    inl_col = callback.data.split(':')
    if int(inl_col[1]) == 1:
        tariffs = orm.db_get_tariffs(1)
        if tariffs:
            for tariff in tariffs:
                await callback.message.answer(text=f'{tariff.name_tariff}',
                                              reply_markup=await gen_markup_menu_tariff(tariff.id))
        else:
            await callback.answer(text=f'Нет активных тарифов')
    elif int(inl_col[1]) == 0:
        tariffs = orm.db_get_tariffs(0)
        if tariffs:
            for tariff in tariffs:
                await callback.message.answer(text=f'{tariff.name_tariff}',
                                              reply_markup=await gen_markup_menu_tariff(tariff.id, 0))
        else:
            await callback.answer(text=f'Нет неактивных тарифов')


@router.callback_query(lambda x: x.data.startswith('tar_action'))
async def tariff_action(callback: types.CallbackQuery):
    """действия с существующими тарифами (включение, выключение, удаление)"""
    inl_col = callback.data.split(':')
    match int(inl_col[2]):
        case 1:
            orm.db_actions_with_tariffs(int(inl_col[1]), 1)
            await callback.answer(text=f'Тариф активирова')
            await callback.message.delete()
        case 0:
            orm.db_actions_with_tariffs(int(inl_col[1]), 0)
            await callback.answer(text=f'Тариф выключен')
            await callback.message.delete()
        case 2:
            orm.db_dell_tariff(int(inl_col[1]))
            await callback.answer(text=f'Тариф удалён')
            await callback.message.delete()


@router.callback_query(lambda x: x.data.startswith('add_tariff'))
async def add_tariff_1(callback: types.CallbackQuery, state: FSMContext):
    """Добавление нового тарифа старт FSM"""
    await callback.message.answer(text='Укажи название нового тарифа', reply_markup=await gen_markup_cancel_fsm())
    await state.set_state(FiltersFSM.name_tariff)


@router.message(FiltersFSM.name_tariff)
async def add_tariff_2(msg: types.Message, state: FSMContext):
    """Ловит название тарифа и переходит в ожидание количества ссылок FSM"""
    if len(msg.text) > 20 or len(msg.text) < 2:
        await msg.answer(text='Название должно содержать от 2 до 20 символов, придумай подходящее название')
    else:
        await state.update_data(name_tariff=msg.text)
        await msg.answer(text='Укажи количество разрешенных ссылок', reply_markup=await gen_markup_cancel_fsm())
        await state.set_state(FiltersFSM.tracked_items)


@router.message(FiltersFSM.tracked_items)
async def add_tariff_3(msg: types.Message, state: FSMContext):
    """Ловит кол-во ссылок и переходит в ожидание стоимости тарифа FSM"""
    if msg.text.isdigit():
        await state.update_data(tracked_items=msg.text)
        await msg.answer(text='Укажи стоимость тарифа в рублях', reply_markup=await gen_markup_cancel_fsm())
        await state.set_state(FiltersFSM.price_tariff)
    else:
        await msg.answer(text='Сообщение должно содержать только цифры.')


@router.message(FiltersFSM.price_tariff)
async def add_tariff_4(msg: types.Message, state: FSMContext):
    """Ловит тарифа и завершает FSM"""
    if msg.text.isdigit():
        await state.update_data(price_tariff=msg.text)
        new_tariff = await state.get_data()
        await msg.answer(text=f'{new_tariff}')
        if orm.db_add_new_tariff(new_tariff):
            await msg.answer(text=f'Тариф {new_tariff["name_tariff"]} добавлен')
        else:
            await msg.answer(text='Похожий тариф уже существует.')
        await state.clear()
    else:
        await msg.answer(text='Сообщение должно содержать только цифры.')


"""__________________________________________"""


@router.message(F.text == 'Выгрузка')
async def add_advertisement_1(msg: types.Message, state: FSMContext):
    """Добавление новой рекламы старт FSM"""
    await msg.answer(text='Картинка рекламы', reply_markup=await gen_markup_cancel_fsm())
    await state.set_state(AddAdvertisementFSM.img)


@router.message(AddAdvertisementFSM.img)
async def add_advertisement_2(msg: types.Message, state: FSMContext):
    """Ловит фото и переходит в ожидание текста FSM"""
    await state.update_data(img=msg.photo[-1].file_id)
    await msg.answer(text='Текст рекламы', reply_markup=await gen_markup_cancel_fsm())
    await state.set_state(AddAdvertisementFSM.text)


@router.message(AddAdvertisementFSM.text)
async def add_advertisement_3(msg: types.Message, state: FSMContext):
    """Ловит текст рекламы текста FSM"""
    await state.update_data(text=msg.text)
    await msg.answer(text='Ссылка', reply_markup=await gen_markup_cancel_fsm())
    await state.set_state(AddAdvertisementFSM.button_link)


@router.message(AddAdvertisementFSM.button_link)
async def add_advertisement_4(msg: types.Message, state: FSMContext):
    """Ловит ссылку и завершает FSM"""

    await state.update_data(button=msg.text)
    x = await state.get_data()
    print(x)
    await msg.answer_photo(photo=x['img'], caption=f'{x["text"]} {x["button"]}', reply_markup=await gen_markup_cancel_fsm())
    await state.clear()


"""________________________________________________________________________"""


@router.callback_query(lambda x: x.data.startswith('ok_pay'))
async def start_fsm_add_money(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает кнопку пополнить бланс старт FSM ожидает сумму"""
    inl_col = callback.data.split(':')
    await callback.message.edit_reply_markup(inline_message_id=callback.id,
                                             reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                                 [InlineKeyboardButton(text=f'Отмена оплаты',
                                                                       callback_data=f'no_pay:{int(inl_col[1])}')]]))
    await callback.message.answer(text='Укажи сумму пополнения баланса', reply_markup=await gen_markup_cancel_fsm())
    await state.set_state(AddMoneyFSM.amount_money)
    await state.update_data(user_id=int(inl_col[1]))


@router.message(AddMoneyFSM.amount_money)
async def increase_user_balance(msg: types.Message, state: FSMContext):
    """Принимает сумму и пополняет баланс пользователю"""
    id_user = await state.get_data()
    print(id_user)
    orm.db_increase_user_balance(user_id=id_user['user_id'],
                                 balance=float(msg.text))
    # await msg.forward(chat_id=ADMIN_ID)
    await bot.send_message(chat_id=id_user['user_id'], text=f'Пополнение баланса.\n'
                                                 f'Ваш баланс пополнен на {msg.text} руб.\n')
    await state.clear()


@router.callback_query(lambda x: x.data.startswith('cancelFSM'))
async def fsm_cancel(callback: types.CallbackQuery, state: FSMContext):
    """Отмена FSM по нажатию кнопки отмена"""
    await state.clear()
    await callback.answer('Отмена')
    await callback.message.delete()
