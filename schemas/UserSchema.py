from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreateClass(BaseModel):
    mail : str
    password : str
    nick_name : str
    age : int

class UserAuthClass(BaseModel):
    model_config = ConfigDict(strict=True)

    username : str
    password : bytes
    mail : EmailStr | None = None
    active: bool = True

