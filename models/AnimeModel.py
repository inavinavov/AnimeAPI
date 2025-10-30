from .BaseModel import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import String, Integer
from typing import Optional


class Anime(Base):
    __tablename__ = "anime"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200))
    create_data: Mapped[str] = mapped_column(String(11))
    final_data: Mapped[str] = mapped_column(String(11))
    count_of_series: Mapped[int] = mapped_column(Integer)
    genre: Mapped[Optional[str]] = mapped_column(String(100))

    reviews = relationship("Review", back_populates="anime")

    def __repr__(self) -> str:
        return f"""
Anime {self.id} 
{self.name}
{self.create_data} - {self.final_data}
Series: {self.count_of_series}
Genre: {self.genre}
"""
