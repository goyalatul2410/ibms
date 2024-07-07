

from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.base import get_db
from app.models import Book
from app.db.database import SessionLocal

router = APIRouter()


@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate):
    db = SessionLocal()
    db_book = crud.create_book(db=db, book=book)
    db.close()
    return db_book


@router.get("/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    books = crud.get_books(db, skip=skip, limit=limit)
    db.close()
    return books


@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int):
    db = SessionLocal()
    book = crud.get_book(db, book_id=book_id)
    db.close()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate):
    db = SessionLocal()
    db_book = crud.update_book(db, book_id=book_id, book=book)
    db.close()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int):
    db = SessionLocal()
    db_book = crud.delete_book(db, book_id=book_id)
    db.close()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.get("/{book_id}/summary", response_model=schemas.BookSummary)
def read_book_summary(book_id: int):
    db = SessionLocal()
    summary = crud.get_book_summary(db=db, book_id=book_id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return summary
