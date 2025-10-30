from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateClass(BaseModel):
    mail: EmailStr
    password: str
    nick_name: str
    age: int

class UserUpdateClass(UserCreateClass):
    active: bool


#ломающий приложение баг

class UserAuthClass(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    mail: EmailStr
    password: bytes
    nick_name: str
    active: bool

#ломающий приложение глич
