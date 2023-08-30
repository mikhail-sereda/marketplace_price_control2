from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import dotenv_values

from data.models import User, UserProduct, Base

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
        new_user = User(user_id=user_id)
        session.add(new_user)
        session.commit()


def db_my_filter_user(user_id: int):
    with Session() as session:
        user1 = session.query(User).filter(User.user_id == user_id).first()
        return bool(user1)


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


def db_get_count_product_user(id_user):
    """Отдаёт количество товаров пользователя па id user"""
    with Session() as session:
        count = session.query(UserProduct).filter(UserProduct.user_id == id_user).count()
        return count


def db_dell_product(id_rec):
    with Session() as session:
        record_to_delete = session.query(UserProduct).filter(UserProduct.id == id_rec).first()
        session.delete(record_to_delete)
        session.commit()


def db_get_profile(id_user):
    """Отдаёт данные профиля па id user"""
    with Session() as session:
        return session.query(User).filter(User.user_id == id_user).first()
