from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.kb_admin import kb_main_admin
from keyboards.ikb_admin import gen_markup_category_tariff, gen_markup_cancel_fsm
from filters.my_filter import AdmFilter
from parser1 import img_by_id, all_pars
from data import orm
from data.FSMbot.FSMadmin import FiltersFSM

router: Router = Router()
router.message.filter(AdmFilter())  # применяем ко всем хендлерам фильтр на админа


# https://mastergroosha.github.io/aiogram-3-guide/fsm/
@router.message(CommandStart())
async def start_admin(msg: types.Message):
    await msg.answer(text='Привет', reply_markup=kb_main_admin)


@router.message(F.text == 'Тарифы')
async def useful(msg: types.Message):
    """Обрабатывает кнопку тарифы"""
    await msg.answer(text=f'Тарифы', reply_markup=await gen_markup_category_tariff())


@router.callback_query(lambda x: x.data.startswith('tariff_active'))
async def returns_all_tariff_to_the_admin(callback: types.CallbackQuery):
    """Показывает активные или не активные тарифы"""
    inl_col = callback.data.split(':')
    if int(inl_col[1]):
        tariffs = orm.db_get_tariffs(1)
        if tariffs:
            for tariff in tariffs:
                await callback.message.answer(text=f'{tariff.name_tariff}')
        else:
            await callback.message.answer(text=f'Нет активных тарифов')
    else:
        tariffs = orm.db_get_tariffs(0)
        if tariffs:
            for tariff in tariffs:
                await callback.message.answer(text=f'{tariff.name_tariff}')
        else:
            await callback.answer(text=f'Нет неактивных тарифов')


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
async def add_tariff_3(msg: types.Message, state: FSMContext):
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


@router.callback_query(lambda x: x.data.startswith('cancelFSM'))
async def fsm_cancel(callback: types.CallbackQuery, state: FSMContext):
    """Отмена FSM по нажатию кнопки отмена"""
    await state.clear()
    await callback.answer('Отмена')
    await callback.message.delete()
