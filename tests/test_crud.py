
import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from starlette.responses import JSONResponse

from app import models, crud, schemas


@pytest.fixture
def mock_session():

    return MagicMock()


def test_create_book_success(mock_session):
    mock_book = models.Book(
        id=1,
        title="Test Book",
        author="Test Author",
        genre="Fiction",
        year_published=2021,
        summary="A test book."
    )

    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    mock_session.refresh = MagicMock()

    mock_query = MagicMock()
    mock_query.options.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_book
    mock_session.query = MagicMock(return_value=mock_query)

    book_data = schemas.BookCreate(
        title="Test Book",
        author="Test Author",
        genre="Fiction",
        year_published=2021,
        summary="A test book.",
        reviews=[]
    )

    result = crud.create_book(mock_session, book_data)

    assert result.title == book_data.title
    assert result.author == book_data.author
    assert result.genre == book_data.genre
    assert result.year_published == book_data.year_published
    assert result.summary == book_data.summary
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    mock_query.first.assert_called_once()


def test_create_book_database_error(mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock(side_effect=SQLAlchemyError("Database error"))
    mock_session.refresh = MagicMock()

    book_data = schemas.BookCreate(title="Test Book", author="Test Author", genre="Fiction", year_published=2021,
                                   summary="A tests book.")

    with pytest.raises(RuntimeError, match="Database error occurred"):
        crud.create_book(mock_session, book_data)


def test_create_book_unexpected_error(mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock(side_effect=Exception("Unexpected error"))
    mock_session.refresh = MagicMock()

    book_data = schemas.BookCreate(title="Test Book", author="Test Author", genre="Fiction", year_published=2021,
                                   summary="A tests book.")

    with pytest.raises(RuntimeError, match="Unexpected error occurred"):
        crud.create_book(mock_session, book_data)


def test_get_books_success(mock_session):
    mock_query = MagicMock()
    mock_query.options = MagicMock(return_value=mock_query)
    mock_query.offset = MagicMock(return_value=mock_query)
    mock_query.limit = MagicMock(return_value=mock_query)
    mock_query.all = MagicMock(return_value=[models.Book(id=1, title="Test Book")])
    mock_session.query = MagicMock(return_value=mock_query)

    books = crud.get_books(mock_session, skip=0, limit=10)

    print(len(books))


    assert len(books) == 1
    assert books[0].title == "Test Book"
    mock_session.query.assert_called_once_with(models.Book)
    mock_query.offset.assert_called_once_with(0)
    mock_query.limit.assert_called_once_with(10)
    mock_query.all.assert_called_once()


def test_get_books_database_error(mock_session):

    mock_session.query = MagicMock(side_effect=SQLAlchemyError("Database error"))


    with pytest.raises(RuntimeError, match="Database error occurred"):
        crud.get_books(mock_session, skip=0, limit=10)


def test_get_books_unexpected_error(mock_session):

    mock_session.query = MagicMock(side_effect=Exception("Unexpected error"))


    with pytest.raises(RuntimeError, match="Unexpected error occurred"):
        crud.get_books(mock_session, skip=0, limit=10)


def test_get_book_success(mock_session):

    mock_query = MagicMock()
    mock_query.options = MagicMock(return_value=mock_query)
    mock_query.filter = MagicMock(return_value=mock_query)
    mock_query.first = MagicMock(return_value=models.Book(id=1, title="Test Book"))
    mock_session.query = MagicMock(return_value=mock_query)


    book = crud.get_book(mock_session, book_id=1)


    assert book.title == "Test Book"
    mock_session.query.assert_called_once_with(models.Book)
    mock_query.first.assert_called_once()


def test_get_book_not_found(mock_session):

    mock_query = MagicMock()
    mock_query.options = MagicMock(return_value=mock_query)
    mock_query.filter = MagicMock(return_value=mock_query)
    mock_query.first = MagicMock(return_value=None)
    mock_session.query = MagicMock(return_value=mock_query)


    response = crud.get_book(mock_session, book_id=1)
    assert response.status_code == 404


def test_get_book_database_error(mock_session):

    mock_session.query = MagicMock(side_effect=SQLAlchemyError("Database error"))


    with pytest.raises(RuntimeError, match="Database error occurred"):
        crud.get_book(mock_session, book_id=1)


def test_get_book_unexpected_error(mock_session):

    mock_session.query = MagicMock(side_effect=Exception("Unexpected error"))


    with pytest.raises(RuntimeError, match="Unexpected error occurred"):
        crud.get_book(mock_session, book_id=1)


def test_get_book_summary_success(mock_session):

    mock_book = models.Book(id=1, title="Test Book", author="Test Author", genre="Fiction", year_published=2021,
                            summary="A test book")
    mock_reviews = [models.Review(review_text="Great book!", rating=5), models.Review(review_text="Not bad.", rating=3)]


    mock_query = MagicMock()
    mock_query.filter = MagicMock(side_effect=lambda *args, **kwargs: mock_query)
    mock_query.first = MagicMock(return_value=mock_book)
    mock_query.all = MagicMock(return_value=mock_reviews)
    mock_session.query = MagicMock(side_effect=lambda model: mock_query)


    summary = crud.get_book_summary(mock_session, book_id=1)


    assert summary["title"] == "Test Book"
    assert summary["author"] == "Test Author"
    assert summary["genre"] == "Fiction"
    assert summary["year_published"] == 2021
    assert summary["summary"] == "A test book"
    assert summary["average_rating"] == 4.0
    assert summary["reviews"] == ["Great book!", "Not bad."]
    mock_query.filter.assert_called()
    mock_query.first.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_book_summary_no_reviews(mock_session):

    mock_book = models.Book(id=1, title="Test Book", author="Test Author", genre="Fiction", year_published=2021,
                            summary="A test book")


    mock_query = MagicMock()
    mock_query.filter = MagicMock(side_effect=lambda *args, **kwargs: mock_query)
    mock_query.first = MagicMock(return_value=mock_book)
    mock_query.all = MagicMock(return_value=[])
    mock_session.query = MagicMock(side_effect=lambda model: mock_query)


    summary = crud.get_book_summary(mock_session, book_id=1)


    assert summary["title"] == "Test Book"
    assert summary["author"] == "Test Author"
    assert summary["genre"] == "Fiction"
    assert summary["year_published"] == 2021
    assert summary["summary"] == "A test book"
    assert summary["average_rating"] == 0
    assert summary["reviews"] == []
    mock_query.filter.assert_called()
    mock_query.first.assert_called_once()
    mock_query.all.assert_called_once()


def test_get_book_summary_not_found(mock_session):

    mock_query = MagicMock()
    mock_query.filter = MagicMock(return_value=mock_query)
    mock_query.first = MagicMock(return_value=None)
    mock_session.query = MagicMock(return_value=mock_query)


    response = crud.get_book_summary(mock_session, book_id=1)
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404


def test_get_book_summary_database_error(mock_session):

    mock_session.query = MagicMock(side_effect=SQLAlchemyError("Database error"))


    with pytest.raises(RuntimeError, match="Database error occurred"):
        crud.get_book_summary(mock_session, book_id=1)


def test_get_book_summary_unexpected_error(mock_session):

    mock_session.query = MagicMock(side_effect=Exception("Unexpected error"))


    with pytest.raises(RuntimeError, match="Unexpected error occurred"):
        crud.get_book_summary(mock_session, book_id=1)
