from crud.AnimeCrud import show_db, db_add_anime, update_db, create_db, delete_db, show_anime_by_id, drop_db_anime
from fastapi import APIRouter , Depends, HTTPException, status
from schemas.AnimeSchema import AnimeCreateClass

router = APIRouter(prefix="/anime", tags=["Anime endpoints"])



@router.get("")
def get_anime():
    return show_db()

@router.get("/{anime_id}")
def get_anime_by_id(anime_id: int):
    return show_anime_by_id(anime_id)

@router.post("/create")
def create_anime(anime: AnimeCreateClass):
    return db_add_anime(anime)

@router.put("/update/{anime_id}")
def update_anime(anime_id: int, anime: AnimeCreateClass):
    return update_db(anime_id, anime)

@router.delete("/delete/{anime_id}")
def delete_anime(anime_id: int):
    return delete_db(anime_id)

@router.delete("/delete/alldata/{i}", description="""Enter 0 if you want to delete all data | Enter 1 if you want to create data""")
def delete_data(i: int):
    if i == 0:
        drop_db_anime()
        return "dropping data"
    elif i == 1:
        create_db()
        return show_db()
