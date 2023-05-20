from pydantic import BaseModel


# Она содержит общие поля, которые могут использоваться 
# для создания и обновления объектов пользователя.
class UserBase(BaseModel):
    id: str
    stream: str
    hashed_password: str
    is_active: bool


# Она используется для создания новых пользователей.
class UserCreate(UserBase):
    id: str
    hashed_password: str
    stream: str


# Эта модель представляет объект пользователя
class User(UserBase):
    id: str
    stream: str
    hashed_password: str

    class Config:
        orm_mode = True