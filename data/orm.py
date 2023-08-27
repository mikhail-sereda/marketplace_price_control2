from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from dotenv import dotenv_values

from data.models import User, Base

config = dotenv_values("../.env", encoding="utf-8")

dbname = config['db_name']
host = config['HOST']
user = config['USER']
password = config['PASSWORD']
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}")
Base.metadata.create_all(engine)
