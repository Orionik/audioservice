from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создает экземпляр движка SQLAlchemy для подключения к базе данных MySQL.
engine = create_engine("mysql+pymysql://root:orion2003@localhost:3307/users",encoding="utf-8")

#Создает класс фабрики сеансов (sessionmaker) для создания сеансов базы данных.
SessionLocal = sessionmaker(bind=engine)

# Создает базовый класс Base, 
# который будет использоваться для объявления моделей SQLAlchemy. 
Base = declarative_base()
