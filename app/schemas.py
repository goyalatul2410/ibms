from pydantic import BaseModel
from typing import List, Optional


class ReviewBase(BaseModel):
    book_id: int
    user_id: int
    review_text: str
    rating: int


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
    reviews: List[Review] = []

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class BookSummary(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str
    average_rating: Optional[float]
    reviews: List[Review] = []

    class Config:
        orm_mode = True
