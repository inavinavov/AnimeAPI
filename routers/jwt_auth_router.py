import jwt

from schemas.UserSchema import UserAuthClass
from auth import utils_jwt as auth_utils
from fastapi import APIRouter, Depends,FastAPI,status, HTTPException, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials,OAuth2PasswordBearer
from pydantic import BaseModel
from crud.UserCrud import get_all_login_pass
from auth.utils_jwt import encode_jwt, decode_jwt,validate_password
from jwt.exceptions import InvalidTokenError



router = APIRouter(prefix="/jwt", tags=["JWT"])

#http_bearer = HTTPBearer()
OAuth2Scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login"
)

class TokenInfo(BaseModel):
    access_token: str
    token_type: str




def validate_auth_user(
        username : str = Form(...),
        password: str = Form(...),
        auth_users = Depends(get_all_login_pass),
):
    unauth_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = auth_users.get(username.lower())
    if not user:
        raise unauth_ex

    if not validate_password(password=password, hashed_password=user.password):
        raise unauth_ex
    return user




@router.post("/login", response_model=TokenInfo)
def login_jwt(
    user: UserAuthClass = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": str(user.id),
        "mail": user.mail,
        "nick_name": user.nick_name,
    }

    token = encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
    )


def get_current_token_payload(
    token : str = Depends(OAuth2Scheme),
) -> dict:
    try:
        payload = decode_jwt(
            token
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token228",
        )

    return payload




def get_current_auth_user(
    payload : dict = Depends(get_current_token_payload),
    users_db = Depends(get_all_login_pass)
) -> UserAuthClass:
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="utoken invalid")

    user = next((u for u in users_db.values() if str(u.id) == str(user_id)), None)
    if not user:
        raise HTTPException(status_code=401, detail="utoken invalid")
    return user


def get_current_active_auth_user(
        user : UserAuthClass = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail="User is deleted")


@router.get("/me")
def auth_user_info(
        payload : dict = Depends(get_current_token_payload),
        user : UserAuthClass = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "id": user.id,
        "mail": user.mail,
        "nick_name": user.nick_name,
        "logged_in_at": iat,
    }


