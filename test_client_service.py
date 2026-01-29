import os
import pytest
from database import Base, Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from client_service import create_client, get_next_client_id, delete_client
from exceptions import InvalidData, ClientNotFound

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
    assert clients_in_db[0].name == "Karol"
    assert clients_in_db[0].surname == "Nowak"
    assert clients_in_db[0].balance == 1000

def test_get_next_client_id_returns_4_after_three_clients(db):
    create_client(db, "A", "A", 0)
    create_client(db, "B", "B", 0)
    create_client(db, "C", "C", 0)

    assert get_next_client_id(db) == 4

def test_generate_next_id(db):
    client1 = create_client(db, "Karol", "Nowak", 1000)
    client2 = create_client(db, "Karol", "Nowak", 1000)
    client3 = create_client(db, "Karol", "Nowak", 1000)
    assert client1.client_id == 1
    assert client2.client_id == 2
    assert client3.client_id == 3

    clients_in_db = db.query(Client).all()
    assert len(clients_in_db) == 3

def test_client_id_generation(db):
    client1 = create_client(db, "Karol", "Nowak", 1000)
    client2 = create_client(db, "Karol", "Nowak", 1000)
    client3 = create_client(db, "Karol", "Nowak", 1000)   

    deleated_id = delete_client(db, client1.client_id) 
    assert deleated_id == 1

    remaining_ids = [c.client_id for c in db.query(Client).order_by(Client.client_id).all()]
    assert remaining_ids == [2, 3]

    client4 = create_client(db, "Karol", "Nowak", 1000)
    assert client4.client_id == 1

@pytest.mark.parametrize("name", ["", " ", None, 123, [], {}])
def test_create_client_invalid_name(db, name):
    with pytest.raises(InvalidData):
        create_client(db, name, "Nowak", 1000)

@pytest.mark.parametrize("surname", ["", " ", None, 123, [], {}])
def test_create_client_invalid_surname(db, surname):
    with pytest.raises(InvalidData):
        create_client(db, "Karol", surname, 1000)

@pytest.mark.parametrize("balance", [-1, -100, None, "100", 12.5, [], {}])
def test_create_client_invalid_balance_raises(db, balance):
    with pytest.raises(InvalidData):
        create_client(db, "Karol", "Nowak", balance)

@pytest.mark.parametrize("id", [0, -1, None, "1", 1.5, [], {}])
def test_delete_client_invalid_id_raises(db, id):
    with pytest.raises(InvalidData):
        delete_client(db, id)

def test_delete_client_not_found_raises(db):
    with pytest.raises(ClientNotFound):
        delete_client(db, 999)