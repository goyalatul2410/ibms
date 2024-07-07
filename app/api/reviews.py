
from fastapi import APIRouter, HTTPException
from typing import List
from app import crud, schemas
from app.db.database import SessionLocal

router = APIRouter()

@router.post("/", response_model=schemas.Review)
def create_review(book_id: int, review: schemas.ReviewCreate):
    db = SessionLocal()
    db_review = crud.create_review(db=db, book_id=book_id, review=review)
    db.close()
    return db_review

@router.get("/", response_model=List[schemas.Review])
def read_reviews(book_id: int):
    db = SessionLocal()
    reviews = crud.get_reviews(db, book_id=book_id)
    db.close()
    return reviews
