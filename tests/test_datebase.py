import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from app.db.base import get_db


@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)


def test_get_db_creates_and_closes_session(mock_session):

    with patch('app.db.base.SessionLocal', return_value=mock_session):
        db_generator = get_db()
        db = next(db_generator)

        assert db == mock_session

        db_generator.close()
        db.close.assert_called_once()
