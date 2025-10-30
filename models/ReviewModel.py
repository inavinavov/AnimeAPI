from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from .BaseModel import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from typing import Optional


class ReviewStatus(str, Enum):
    watching = "watching"
    completed = "completed"
    planned = "planned"
    dropped = "dropped"
    paused = "paused"
    not_specified = "not_specified"


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    anime_id: Mapped[int] = mapped_column(ForeignKey("anime.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    status: Mapped[ReviewStatus] = mapped_column(SQLEnum(ReviewStatus), nullable=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    review_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="reviews")
    anime = relationship("Anime", back_populates="reviews")
