from fastapi import APIRouter , Depends, HTTPException, status
from .auth_router import security
from fastapi.security import HTTPBasicCredentials
from typing import Annotated

router = APIRouter(tags=["Start"])

@router.get("/")
def hi(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    if credentials.username:
        return f"Welcome {credentials.username}!"
    else:
        return f"Hello World!"

