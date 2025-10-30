from crud.AnimeCrud import show_anime_db, db_add_anime, update_anime_db, create_db, delete_anime_db, show_anime_by_id, drop_db_anime
from fastapi import APIRouter , Depends, HTTPException, status
from schemas.AnimeSchema import AnimeCreateClass

router = APIRouter(prefix="/anime", tags=["Anime endpoints"])



@router.get("/show/all")
def get_anime():
    return show_anime_db()


@router.post("/create")
def create_anime(anime: AnimeCreateClass):
    return db_add_anime(anime)



@router.get("/show/{anime_id}/")
def get_anime_by_id(anime_id: int):
    return show_anime_by_id(anime_id)



@router.put("/update/{anime_id}")
def update_anime(anime_id: int, anime: AnimeCreateClass):
    return update_anime_db(anime_id, anime)



@router.delete("/delete/{anime_id}")
def delete_anime(anime_id: int):
    return delete_anime_db(anime_id)

