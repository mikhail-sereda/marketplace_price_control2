from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bt_user_my_stock: KeyboardButton = KeyboardButton(text='🛍Мои товары')
bt_user_profile: KeyboardButton = KeyboardButton(text='Профиль')
bt_user_useful: KeyboardButton = KeyboardButton(text='Полезное')
bt_user_help: KeyboardButton = KeyboardButton(text='🆘Помощь')


kb_main_user = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[bt_user_my_stock],
                                                                    [bt_user_profile, bt_user_useful], [bt_user_help]])
