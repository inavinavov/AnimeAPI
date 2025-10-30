from fastapi import APIRouter, Depends, HTTPException
from schemas.UserSchema import UserCreateClass, UserUpdateClass, UserAuthClass
from crud.UserCrud import create_user_db, delete_user_db, show_all_users,update_user_db
from .jwt_auth_router import get_current_active_auth_user


router = APIRouter(prefix="/user", tags=["User endpoints"])


@router.get("/show_all")
def show_user():
    return show_all_users()


@router.post("/create")
def create_user(user : UserCreateClass):
    result = create_user_db(user)
    return result



@router.put("/update")
def update_user(
        us: UserUpdateClass,
        auth_user : UserAuthClass = Depends(get_current_active_auth_user)
):
    user_id = auth_user.id
    return update_user_db(user_id, us)


@router.delete("/me/account/delete/")
def delete_user(auth_user : UserAuthClass = Depends(get_current_active_auth_user)):
    user_id = auth_user.id
    return delete_user_db(user_id)
