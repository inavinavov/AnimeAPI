import secrets

from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter , Depends, HTTPException, status
from crud.UserCrud import get_all_login_pass


router = APIRouter(prefix="/auth", tags=["Basic auth"])


security = HTTPBasic()


def check_auth(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    users = get_all_login_pass()
    correct_password = users.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    if not secrets.compare_digest(
            credentials.password.encode('utf-8'),
            correct_password.encode('utf-8')
    ):
        raise unauthed_exc

    return credentials.username


print(get_all_login_pass())



@router.get("/basic-auth")
def basic_auth_username(
        auth_username: str = Depends(check_auth),
):
    return {"message": f"Welcome back, {auth_username}!",
            "username": auth_username}

