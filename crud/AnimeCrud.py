from app.core.database import engine, SessionLocal
from sqlalchemy import select, text
from models.AnimeModel import Anime
from schemas.AnimeSchema import AnimeCreateClass
from app.core.Anime_list import A_L
from fastapi import HTTPException
from models.BaseModel import Base


def get_id():
    with SessionLocal() as session:
        # Находим максимальный ID
        result = session.execute(select(Anime.id).order_by(Anime.id.desc()))
        max_id = result.scalar()  # scalar() возвращает одно значение
        return 1 if max_id is None else max_id + 1


def create_anime_list(anime_list):
    for anime in anime_list:
        db_add_anime(anime)
        print(f"Добавлено: {anime.name}")


def db_add_anime(title: AnimeCreateClass):
    with SessionLocal() as session:
        try:
            new_anime = Anime(
                name=title.name,
                create_data=title.create_data,
                final_data=title.final_data,
                count_of_series=title.count_of_series,
                genre=title.genre,
            )

            session.add(new_anime)
            session.commit()
            session.refresh(new_anime)
            return {
                "id": new_anime.id,
                "name": new_anime.name,
                "genre": new_anime.genre,
                "create_data": new_anime.create_data,
                "final_data": new_anime.final_data,
                "count_of_series": new_anime.count_of_series,
            }

        except Exception as e:
            session.rollback()
            create_db()
            print(f"❌ Не удалось добавить {title.name}: {str(e)}")
            return None  # Явно возвращаем None при ошибке


def create_db():
    Base.metadata.create_all(engine)
    create_anime_list(A_L)


def show_anime_db():
    result = []
    with SessionLocal() as session:
        stat = select(Anime).order_by(Anime.id)
        data = session.scalars(stat).all()
        for anime in data:
            result.append(
                {
                    "id": anime.id,
                    "name": anime.name,
                    "create_data": anime.create_data,
                    "final_data": anime.final_data,
                    "count_of_series": anime.count_of_series,
                    "genre": anime.genre,
                }
            )
        return result


def update_anime_db(id: int, title: AnimeCreateClass):
    with SessionLocal() as session:
        try:
            stat = select(Anime).where(Anime.id == id)
            updated_anime = session.scalars(stat).one()
            updated_anime.name = title.name
            updated_anime.create_data = title.create_data
            updated_anime.final_data = title.final_data
            updated_anime.count_of_series = title.count_of_series
            updated_anime.genre = title.genre
            session.commit()
            session.refresh(updated_anime)
            return {
                "id": updated_anime.id,
                "name": updated_anime.name,
                "create_data": updated_anime.create_data,
                "final_data": updated_anime.final_data,
                "count_of_series": updated_anime.count_of_series,
                "genre": updated_anime.genre,
            }
        except Exception as e:
            session.rollback()
            print(f"Ошибка: {e}")


def delete_anime_db(id: int):
    with SessionLocal() as session:
        try:
            anime_deleted = session.get(Anime, id)
            if anime_deleted is None:
                raise HTTPException(status_code=404, detail="User not found")
            result = {
                "id": anime_deleted.id,
                "name": anime_deleted.name,
                "genre": anime_deleted.genre,
                "create_data": anime_deleted.create_data,
                "final_data": anime_deleted.final_data,
                "count_of_series": anime_deleted.count_of_series,
            }
            session.delete(anime_deleted)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            return None


def show_anime_by_id(id: int):
    with SessionLocal() as session:
        stat = select(Anime).where(Anime.id == id)
        data = session.scalars(stat).first()
        if data:
            return data


def drop_db_anime():
    with SessionLocal() as session:
        try:
            session.execute(text('DROP TABLE IF EXISTS "Anime"'))  # ✅ Добавить text()
            session.commit()
            print("✅ Таблица Anime успешно удалена!")
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка: {e}")
