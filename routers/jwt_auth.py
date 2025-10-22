from schemas.UserSchema import UserAuthClass
from auth import utils_jwt as auth_utils
from fastapi import APIRouter, Depends
from pydantic import BaseModel
router = APIRouter(prefix="/jwt", tags=["JWT"])

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

john = UserAuthClass(
    username="john",
    password=auth_utils.hash_password("123"),
    email="123@mail.ru",
)
john = UserAuthClass(
    username="john",
    password=auth_utils.hash_password("123"),
    email="123@mail.ru",
)
sam = UserAuthClass(
    username="sam",
    password=auth_utils.hash_password("1234"),
)

user_db : dict[str, UserAuthClass] = {
    john.username: john,
    sam.username: sam,
}

def validate_auth_user():
    pass


@router.post("/login", response_model=TokenInfo)
def login_jwt(
        user: UserAuthClass = Depends(),
):
    jwt_payload = {
        "username": user.username,
        "mail": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer")