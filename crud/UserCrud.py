from fastapi import HTTPException
from app.core.database import SessionLocal
from models.UserModel import User
from sqlalchemy import select, text
from schemas.UserSchema import UserCreateClass, UserAuthClass,UserUpdateClass
from sqlalchemy.exc import SQLAlchemyError
from auth.utils_jwt import hash_password


def create_user_db(user: UserCreateClass):
    with SessionLocal() as session:
        try:
            new_user = User(
                mail=user.mail,
                password=hash_password(user.password),
                nick_name=user.nick_name,
                age=user.age,
                anime_count=0,
            )
            existing_user = session.scalar(
                select(User).where(
                    (User.nick_name == new_user.nick_name)
                    | (User.mail == new_user.mail)
                )
            )
            if existing_user:
                raise HTTPException(
                    status_code=403, detail=f"User {new_user.nick_name} already exists"
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
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"User {user.nick_name} wasn't created: {str(e)}",
            )


def get_all_login_pass():
    with SessionLocal() as session:
        try:
            stat = select(User.id, User.mail, User.password, User.nick_name, User.active)
            data = session.execute(stat).all()
            result = {
                mail.lower(): UserAuthClass(id=id, mail=mail.lower(), password=password, nick_name=str(nick_name), active=active)
                for id, mail, password, nick_name, active in data
            }
            return result
        except:
            session.rollback()
            raise HTTPException(status_code=401, detail="Invalid username or password")



def show_all_users():
    with SessionLocal() as session:
        try:
            stat = select(
                User.id, User.mail, User.nick_name, User.age, User.anime_count,User.active
            ).order_by(User.id)
            data = session.execute(stat).all()
            return [
                {
                    "id": user[0],
                    "mail": user[1],
                    "nick_name": user[2],
                    "age": user[3],
                    "anime_count": user[4],
                    "active": user[5],
                }
                for user in data
            ]
        except:
            session.rollback()


def delete_user_db(user_id: int):
    with SessionLocal() as session:
        try:
            user_deleted = session.get(User, user_id)
            if user_deleted is None:
                raise HTTPException(status_code=404, detail="User not found")
            user_deleted.active = False
            session.commit()
            result = {
                "id": user_deleted.id,
                "mail": user_deleted.mail,
                "nick_name": user_deleted.nick_name,
                "age": user_deleted.age,
                "anime_count": user_deleted.anime_count,
                "active": user_deleted.active,
            }
            return result
        except Exception as e:
            session.rollback()
            return None


def drop_db_user():
    with SessionLocal() as session:
        try:
            session.execute(text('DROP TABLE IF EXISTS "Users"'))  # ✅ Добавить text()
            session.commit()
            print("✅ Таблица Anime успешно удалена!")
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка: {e}")


def update_user_db(
        user_id: int,
        user: UserUpdateClass
):
    with SessionLocal() as session:
        try:
            updated_user = session.get(User, user_id)
            if updated_user is None:
                raise HTTPException(status_code=404, detail="User not found")

            updated_user.mail = user.mail
            updated_user.password = hash_password(user.password)
            updated_user.nick_name = user.nick_name
            updated_user.age = user.age
            updated_user.active = user.active
            session.commit()
            session.refresh(updated_user)
            if updated_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            result = {
                "id": updated_user.id,
                "mail": updated_user.mail,
                "nick_name": updated_user.nick_name,
                "age": updated_user.age,
                "active": updated_user.active,
            }
            return result
        except Exception as e:
            session.rollback()
            return f"Ошибка: {e}"