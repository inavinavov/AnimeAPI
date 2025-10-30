from fastapi import APIRouter

router = APIRouter(tags=["Start"])


@router.get("/")
def auth_user_info(
):
        return {"message":"hell0!"}