from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

@router.get("/")
async def read_root():
    return {"message": "Hello World"}
