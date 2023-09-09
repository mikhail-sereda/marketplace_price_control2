from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    user_id = Column(BigInteger, nullable=False, unique=True)
    activ = Column(Integer, default=1, nullable=False)
    balance = Column(Float, default=0, nullable=False)
    tariff_user = Column(String, default='Стандартный')
    tracked_items = Column(Integer, default=3, nullable=False)
    tariff_user_date = Column(DateTime, default=datetime.now, nullable=False)
    all_many = Column(Float, default=0)
    user_products = relationship('UserProduct', backref='user', lazy=True)


class UserProduct(Base):
    __tablename__ = 'user_products'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    id_prod = Column(BigInteger, nullable=False)
    add_date = Column(DateTime, default=datetime.now, nullable=False)
    name_prod = Column(String, nullable=False)
    start_price = Column(Float, nullable=False)
    min_price = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    pars_price = Column(Float, nullable=False)
    photo_link = Column(String, nullable=False)
    link = Column(String, nullable=False)
    valve = Column(Integer, default=1, nullable=False)


class Tariffs(Base):
    __tablename__ = 'tariffs'
    id = Column(Integer, primary_key=True)
    add_date = Column(DateTime, default=datetime.now, nullable=False)
    name_tariff = Column(String, nullable=False)
    tracked_items = Column(Integer, default=3, nullable=False)
    price_tariff = Column(Float, nullable=False)
    number_activations = Column(Integer, default=0, nullable=False)
    active_tariff = Column(Integer, default=1, nullable=False)


