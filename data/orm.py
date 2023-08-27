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


def add_user(user_id):
    session = Session()
    new_user = User(user_id=user_id)
    session.add(new_user)
    session.commit()


def my_filter_user(user_id: int):
    session = Session()
    user1 = session.query(User).filter(User.user_id == user_id).first()
    return bool(user1)
