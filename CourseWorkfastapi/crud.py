from sqlalchemy.orm import Session
from sqlalchemy import select

import models
import schemas


# Эта функция проверяет соответствие пароля для пользователя с заданным user_id
def check_password(db: Session, password: str, user_id: str):
    row = db.execute(select(models.User.stream).where(models.User.id == user_id).where(models.User.hashed_password == password)).first()
    return row


# Эта функция создает нового пользователя в базе данных.
def create_user(db: Session, id:str, hashed_password:str, stream:str):
    db_user = models.User(id=id, hashed_password=hashed_password, stream=stream)
    print(id, hashed_password, stream)
    db.add(db_user)
    db.commit()
    print(db_user)
    return db_user