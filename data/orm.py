from datetime import datetime, timedelta

from sqlalchemy import create_engine, insert, sql
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values

from data.models import User, UserProduct, Tariffs, Base, Advertisement

config = dotenv_values(".env", encoding="utf-8")
ADMIN_ID = config['ADMIN_ID']
dbname = config['db_name']
host = config['HOST']
user = config['USER']
password = config['PASSWORD']
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def db_add_user(user_id):
    with Session() as session:
        replay_user = session.query(User).filter(User.user_id == user_id).first()
        if not replay_user:
            new_user = User(user_id=user_id)
            session.add(new_user)
            session.commit()
        else:
            db_changes_user_activ(id_user=user_id, activ=1)
            session.commit()


def db_my_filter_user(user_id: int):
    with Session() as session:
        user1 = session.query(User).filter(User.user_id == user_id, User.activ == 1).first()
        return bool(user1)


def db_changes_user_tariff(name_tariff: str, id_user: int, tracked_items: int, balance: float):
    """Изменяет тариф у пользователя"""
    with Session() as session:
        one_user = session.query(User).filter(User.user_id == id_user).first()
        one_user.tariff_user = name_tariff
        one_user.tracked_items = tracked_items
        one_user.tariff_user_date = datetime.now()
        one_user.balance = balance
        session.commit()


def db_changes_user_activ(id_user: int, activ: int):
    """Изменяет активность у пользователя. 0 не активный, 1 активный"""
    print(id_user, activ)
    with Session() as session:
        one_user = session.query(User).filter(User.user_id == id_user).first()
        one_user.activ = activ
        session.commit()


def db_increase_user_balance(user_id: int, balance: float):
    """Изменяет баланс у пользователя"""
    with Session() as session:
        one_user = session.query(User).filter(User.user_id == user_id).first()
        one_user.balance = one_user.balance + balance
        one_user.all_many = one_user.all_many + balance
        session.commit()


def db_get_all_users():
    """Отдаёт количество всex пользователей, с разбивкой на активные и нет"""
    with Session() as session:
        users = session.query(User).all()
        activ_users = 0
        no_activ_users = 0
        for us in users:
            if us.activ == 0:
                no_activ_users += 1
            elif us.activ == 1:
                activ_users += 1
        return len(users), activ_users, no_activ_users


def db_get_all_users_stop_tariff():
    """Отдаёт всex пользователей"""
    with Session() as session:
        filter_after = datetime.now() - timedelta(days=180)
        users = session.query(User).filter(User.tariff_user_date < filter_after,
                                           User.tariff_user != 'Стандартный').all()
        return users


def db_get_activ_users():
    """Отдаёт активных пользователей"""
    with Session() as session:
        users = session.query(User.user_id).filter(User.activ == 1).all()
        print(users)
        return users


def db_get_tracked_items(user_id):
    """Отает количество ссылок для отслеживания пользователю"""
    with Session() as session:
        items = session.query(User.tracked_items).filter(User.user_id == user_id).first()
        return items[0]


def db_add_product(product: dict):
    """добавляет новый товар и возвращает True, если пользователь уже следит за товаром возвращает False"""
    with Session() as session:
        replay_product = session.query(UserProduct).filter(UserProduct.user_id == product['user_id'],
                                                           UserProduct.id_prod == product['id_prod']).first()
        if not replay_product:
            session.execute(UserProduct.__table__.insert(), product)
            session.commit()
            return True

        else:
            session.commit()
            return False


def db_get_user_product(id_user):
    """Отдаёт все товары пользователя па id user"""
    with Session() as session:
        all_prod = session.query(UserProduct).order_by(UserProduct.id).filter(
            UserProduct.user_id == id_user).all()
        return all_prod


def db_get_all_product():
    """Отдаёт все активные товары"""
    with Session() as session:
        all_prod = session.query(UserProduct).filter(
            UserProduct.valve == 1).all()
        return all_prod


def db_get_modified_products():
    """Отдаёт все активные товары с изменённой ценой"""
    with Session() as session:
        mod_products = session.query(UserProduct).filter(
            UserProduct.price != UserProduct.pars_price, UserProduct.valve == 1).all()
        return mod_products


def db_get_count_product_user(id_user):
    """Отдаёт количество товаров пользователя па id user"""
    with Session() as session:
        count = session.query(UserProduct).filter(UserProduct.user_id == id_user).count()
        return count


def db_get_profile(id_user):
    """Отдаёт данные профиля па id user"""
    with Session() as session:
        return session.query(User).filter(User.user_id == id_user).first()


def db_adjusts_price(id_prod, price, min_price=None):
    """корректирует текущую цену и минимальную после сообщения пользователю об изменении цены"""
    with Session() as session:
        one_prod = session.query(UserProduct).filter(UserProduct.id == id_prod).first()
        if min_price:
            one_prod.price = price
            one_prod.min_price = min_price
        else:
            one_prod.price = price
        session.commit()


def db_disables_product_tracking(id_user, tracked_items=3):
    """Выключает отслеживание товаров превышающее тариф"""
    with Session() as session:
        user_products = session.query(UserProduct).order_by(UserProduct.id).filter(
            UserProduct.user_id == id_user).all()
        for prod_activ in user_products[:tracked_items]:
            prod_activ.valve = 1
        for prod in user_products[tracked_items:]:
            prod.valve = 0
        session.commit()





def db_adjusts_pars_price(id_prod, price):
    """Обновляет текущую цену после парсинга"""
    with Session() as session:
        one_prod = session.query(UserProduct).filter(UserProduct.id == id_prod).first()
        one_prod.pars_price = price
        session.commit()


def db_dell_product(id_rec):
    with Session() as session:
        record_to_delete = session.query(UserProduct).filter(UserProduct.id == id_rec).first()
        session.delete(record_to_delete)
        session.commit()


"""Tariffs"""


def db_get_tariffs(index_activ):
    """Получает активные или не активные тарифы """
    with Session() as session:
        return session.query(Tariffs).order_by(Tariffs.price_tariff).filter(Tariffs.active_tariff == index_activ).all()


def db_get_one_tariff(id_tariff):
    """Получает тариф по id"""
    with Session() as session:
        return session.query(Tariffs).get(id_tariff)


def db_add_new_tariff(new_tariff):
    with Session() as session:
        replay_tariff = session.query(Tariffs).filter(Tariffs.name_tariff == new_tariff['name_tariff'],
                                                      Tariffs.price_tariff == float(new_tariff['price_tariff'])).first()
        if not replay_tariff:
            session.execute(insert(Tariffs).values(new_tariff))
            session.commit()
            return True

        else:
            session.commit()
            return False


def db_dell_tariff(id_tariff):
    """удаление тарифа"""
    with Session() as session:
        record_to_delete = session.query(Tariffs).filter(Tariffs.id == id_tariff).first()
        session.delete(record_to_delete)
        session.commit()


def db_actions_with_tariffs(id_tariff, active_tariff):
    """изменяет активацию тарифа (0 или 1) в колонке active_tariff"""
    with Session() as session:
        tariff = session.query(Tariffs).filter(Tariffs.id == id_tariff).first()
        tariff.active_tariff = active_tariff
        session.commit()


"""_________________Advertisement__________________"""


def db_add_ad(data):
    """Добавляет новую рекламу в базу данных"""
    with Session() as session:
        session.execute(Advertisement.__table__.insert(), data)
        session.commit()


def db_get_ad():
    with Session() as session:
        ad_id = session.query(sql.func.max(Advertisement.id)).first()
        return session.query(Advertisement).filter(Advertisement.id == ad_id[0]).first()

