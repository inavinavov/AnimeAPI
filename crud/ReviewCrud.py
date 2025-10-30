from app.core.database import engine, SessionLocal
from sqlalchemy import select, text
from models.ReviewModel import Review
from models.UserModel import User
from schemas.ReviewSchema import ReviewCreateClass, ReviewStatus, ReviewInputClass
from app.core.Anime_list import A_L
from fastapi import HTTPException
from models.BaseModel import Base


def show_reviews_db():
    with SessionLocal() as session:
        try:
            reviews = session.query(Review).order_by(Review.id.desc()).all()
            return [
                {
                    "id": review.id,
                    "Аниме": review.anime.name if review.anime else "❓Не указано",
                    "Юзер": review.user.nick_name if review.user else "❓Неизвестен",
                    "Статус": review.status.value if review.status else "❌Не указано",
                    "Оценка": review.rating if review.rating is not None else "—",
                    "Комментарий": review.review_text if review.review_text else "—",
                    "Создано в": review.created_at.strftime("%H:%M %d-%m-%Y"),
                    "Редактировалось в": (
                        review.updated_at.strftime("%H:%M %d-%m-%Y")
                        if review.updated_at
                        else "—"
                    ),
                }
                for review in reviews
            ]
        except:
            session.rollback()


def create_review_db(review: ReviewInputClass):
    with SessionLocal() as session:
        try:
            new_review = Review(
                anime_id=review.anime_id,
                user_id=review.user_id,
                status=review.status,
                rating=review.rating,
                review_text=review.review_text,
            )

            session.add(new_review)
            session.flush()
            session.refresh(new_review.user)

            new_review.user.anime_count = new_review.user.watched_anime_count

            session.commit()
            session.refresh(new_review)

            return {
                "Аниме": new_review.anime.name,
                "Юзер": new_review.user.nick_name,
                "Статус": new_review.status.value,
                "Оценка": new_review.rating,
                "Отзыв": new_review.review_text,
                "Создано в": new_review.created_at.strftime("%H:%M %d-%m-%Y"),
            }
        except Exception as e:
            session.rollback()
            return f"❌ Не удалось добавить ваше ревью: {str(e)}"


def delete_review_db_by_user(user_id, anime_id):
    with SessionLocal() as session:
        try:
            delete_review = (
                session.query(Review)
                .filter(Review.anime_id == anime_id, Review.user_id == user_id)
                .first()
            )
            if delete_review:
                session.delete(delete_review)
                result = {
                    "name": delete_review.anime.name,
                    "user": delete_review.user.nick_name,
                    "status": "Deleted",
                    "rating": delete_review.rating,
                    "review_text": delete_review.review_text,
                }
                session.commit()
                return result
        except Exception as e:
            session.rollback()
            return f"Ошибка {e}"

