from app.core.database import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String,Integer
from typing import Optional

class User(Base):
    __tablename__ = "User"
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    mail: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(30))
    nick_name : Mapped[str] = mapped_column(String(200))
    age : Mapped[str] = mapped_column(String(11))
    anime_count : Mapped[int] = mapped_column(Integer)


    def __repr__(self) -> str:
        return f"""
{self.id} 
{self.nick_name}
"""







