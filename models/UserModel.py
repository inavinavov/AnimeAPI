from .BaseModel import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, Integer, LargeBinary
from typing import Optional
from .ReviewModel import ReviewStatus


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mail: Mapped[str] = mapped_column(String(200))
    password: Mapped[bytes] = mapped_column(LargeBinary)
    nick_name: Mapped[str] = mapped_column(String(200))
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    anime_count: Mapped[int] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(default=True)

    reviews = relationship("Review", back_populates="user")

    def __repr__(self) -> str:
        return f"""
{self.id} 
{self.nick_name}
"""

    @property
    def watched_anime_count(self) -> int:
        return sum(1 for r in self.reviews if r.status == ReviewStatus.completed)
