from http.client import HTTPException

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from starlette.responses import JSONResponse

from app import models, schemas


def create_book(db: Session, book: schemas.BookCreate):
    try:
        db_book = models.Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        db_book_with_reviews = db.query(models.Book).options(joinedload(models.Book.reviews)).filter(models.Book.id == db_book.id).first()
        return db_book_with_reviews
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Unexpected error occurred: {str(e)}")


def get_books(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(models.Book).options(joinedload(models.Book.reviews)).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Unexpected error occurred: {str(e)}")


def get_book(db: Session, book_id: int):
    try:
        book = db.query(models.Book).options(joinedload(models.Book.reviews)).filter(models.Book.id == book_id).first()
        if not book:
            return JSONResponse(status_code=404, content="Book not found")
        return book
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Unexpected error occurred: {str(e)}")


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        for key, value in book.dict(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def create_review(db: Session, book_id: int, review: schemas.ReviewCreate):
    try:
        db_review = models.Review(book_id=book_id, review_text=review.review_text, rating=review.rating)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Unexpected error occurred: {str(e)}")


def get_reviews(db: Session, book_id: int):
    try:
        book = db.query(models.Review).filter(models.Review.book_id == book_id)
        if not book:
            return []
        return book
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Unexpected error occurred: {str(e)}")


def get_book_summary(db: Session, book_id: int):
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not book:
            return JSONResponse(status_code=404, content="Book not found")

        reviews = db.query(models.Review).filter(models.Review.book_id == book_id).all()
        total_rating = sum(review.rating for review in reviews) if reviews else 0
        avg_rating = total_rating / len(reviews) if reviews else 0

        summary = {
            "title": book.title,
            "author": book.author,
            "genre": book.genre,
            "year_published": book.year_published,
            "summary": book.summary,
            "average_rating": avg_rating,
            "reviews": [review.review_text for review in reviews]
        }
        return summary
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error occurred: {str(e)}")
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Unexpected error occurred: {str(e)}")
