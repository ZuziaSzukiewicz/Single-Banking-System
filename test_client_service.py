import os
import pytest
from database import Base, Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from client_service import create_client, get_next_client_id

TEST_DB_URL = "sqlite:///test_database.db"


@pytest.fixture
def db():
    if os.path.exists("test_database.db"):
        os.remove("test_database.db")

    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session
    session.close()

def test_create_first_client(db):
    client = create_client(db, "Karol", "Nowak", 1000)
    assert client.client_id == 1

    clients_in_db = db.query(Client).all()
    assert len(clients_in_db) == 1
    assert clients_in_db[0].client_id == 1



