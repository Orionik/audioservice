from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

# User представляет собой таблицу users с тремя столбцами: id, stream и hashed_password.
class User(Base):
    __tablename__ = "users"

    id = Column(String(120), primary_key=True, index=True)
    stream = Column(String(120))
    hashed_password = Column(String(120))

