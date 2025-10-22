from fastapi import HTTPException

from app.core.database import SessionLocal
from models.UserModel import User
from sqlalchemy import select, text
from schemas.UserSchema import UserCreateClass


def get_id():
    with SessionLocal() as session:
        # Находим максимальный ID
        result = session.execute(select(User.id).order_by(User.id.desc()))
        max_id = result.scalar()  # scalar() возвращает одно значение
        return 1 if max_id is None else max_id + 1


def create_user_db(user: UserCreateClass):
    with SessionLocal() as session:
        try:
            new_user = User(
                id=get_id(),
                mail=user.mail,
                password=user.password,
                nick_name=user.nick_name,
                age=user.age,
                anime_count=0,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            result = {
                "id": new_user.id,
                "mail": new_user.mail,
                "nick_name": new_user.nick_name,
                "age": new_user.age,
                "anime_count": new_user.anime_count,
            }
            return result
        except:
            session.rollback()
            return f"User {user.nick_name} wasn't created"

def get_all_login_pass():
    with SessionLocal() as session:
        try:
            stat = select(User.mail, User.password)
            data = session.execute(stat).all()
            return {nick.lower():password  for nick, password  in data}
        except:
            session.rollback()
            raise HTTPException(status_code=401, detail="Invalid username or password")





def drop_db_user():
    with SessionLocal() as session:
        try:
            session.execute(text('DROP TABLE IF EXISTS "Users"'))  # ✅ Добавить text()
            session.commit()
            print("✅ Таблица Anime успешно удалена!")
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка: {e}")
