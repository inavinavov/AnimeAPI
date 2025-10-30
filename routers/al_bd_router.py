from fastapi import APIRouter
from crud.AnimeCrud import create_db, drop_all_tables


router = APIRouter(prefix="/main", tags=["Terminal endpoints"])





@router.get("/create/db")
def create_db_endpoint(go: str):
    if go.lower() == "y":
        messages = create_db()  # вызываем CRUD функцию
        return {"status": "success", "messages": messages}
    return {"status": "cancelled"}

@router.get("/drop/db")
def delete_db(go: str):
    if go.lower() == "y":
        return drop_all_tables()



