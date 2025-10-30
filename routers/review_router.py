from fastapi import APIRouter,Depends

from models import Review
from schemas.ReviewSchema import ReviewCreateClass, ReviewInputClass
from crud.ReviewCrud import create_review_db, show_reviews_db, delete_review_db_by_user
from schemas.UserSchema import UserAuthClass
from .jwt_auth_router import get_current_active_auth_user

router = APIRouter(prefix="/review", tags=["Review endpoints"])


@router.post("/create")
def create_review(
        review: ReviewCreateClass,
        auth_user: UserAuthClass = Depends(get_current_active_auth_user),
):
    new_review = {
        "anime_id": review.anime_id,
        "user_id": auth_user.id,
        "status": review.status,
        "rating": review.rating,
        "review_text": review.review_text,
    }
    us = ReviewInputClass(**new_review)
    result = create_review_db(us)
    return result


@router.get("/show_all")
def show_all_review():
    return show_reviews_db()


@router.delete("/me/delete/{anime_id}")
def delete_user_s_review(
        anime_id : int ,
        auth_user: UserAuthClass = Depends(get_current_active_auth_user),
):
    user_id = int(auth_user.id)
    return delete_review_db_by_user(user_id, anime_id)




