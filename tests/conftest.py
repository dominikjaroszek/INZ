import pytest
from app import create_app
from app.config import db

import pytest
from app import create_app
from app.config import db
from app.models.user import User

import pytest

@pytest.fixture()
def app():
    flask_app = create_app()  # Adjust this line if create_app needs to accept arguments
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with flask_app.app_context():
        yield flask_app