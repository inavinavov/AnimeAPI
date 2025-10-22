from fastapi import APIRouter
from schemas.UserSchema import UserCreateClass
from crud.UserCrud import create_user_db
router = APIRouter(prefix="/user", tags=["User endpoints"])

@router.post("/create/user")
def create_user(us: UserCreateClass):
    result = create_user_db(us)
    return result