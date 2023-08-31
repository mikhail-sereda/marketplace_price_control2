from aiogram import Router, types, F
from aiogram.filters import CommandStart

from keyboards.kb_admin import kb_main_admin
from keyboards.ikb_admin import gen_markup_category_tariff
from filters.my_filter import AdmFilter
from parser1 import img_by_id, all_pars
from data import orm

router: Router = Router()
router.message.filter(AdmFilter())  # применяем ко всем хендлерам фильтр на админа


@router.message(CommandStart())
async def start_admin(msg: types.Message):
    await msg.answer(text='Привет', reply_markup=kb_main_admin)


@router.message(F.text == 'Тарифы')
async def useful(msg: types.Message):
    """Обрабатывает кнопку тарифы"""
    await msg.answer(text=f'Тарифы', reply_markup=await gen_markup_category_tariff())


@router.callback_query(lambda x: x.data.startswith('tariff_active'))
async def returns_all_tariff_to_the_admin(callback: types.CallbackQuery):
    inl_col = callback.data.split(':')
    if int(inl_col[1]):
        tariffs = orm.db_get_tariffs(1)
        if tariffs:
            await callback.answer(text='Активные тарифы')
        else:
            await callback.answer(text=f'Нет активных тарифов')
    else:
        tariffs = orm.db_get_tariffs(0)
    if tariffs:
        pass
    else:
        await callback.answer(text=f'Нет неактивных тарифов')

# @router.message()
# async def eho_admin(msg: types.Message):
#     await msg.answer(text='ответcvbcv', reply_markup=kb_main_admin)

# @router.callback_query()
