import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app as flask_app
from db import db as _db
from sqlalchemy.orm import scoped_session, sessionmaker
from models import AccountHolder, Account, Transaction

@pytest.fixture(scope='session')
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.drop_all()

@pytest.fixture(scope='session')
def db(app):
    return _db

@pytest.fixture(scope='function', autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    scoped = scoped_session(session_factory)

    db.session = scoped
    yield scoped

    transaction.rollback()
    connection.close()
    scoped.remove()

@pytest.fixture
def client(app):
    return app.test_client()
