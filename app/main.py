from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import books, reviews
from app.db.database import engine, Base
from app.middleware.auth_middleware import AuthMiddleware
import os

app = FastAPI(
    title="Intelligent Book Management System",
    description="API for managing books, reviews, and summaries.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "url": "https://your-website.com",
        "email": "your-email@domain.com",
    },
)

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

Base.metadata.create_all(bind=engine)

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(reviews.router, prefix="/books/{book_id}/reviews", tags=["reviews"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Management API"}
