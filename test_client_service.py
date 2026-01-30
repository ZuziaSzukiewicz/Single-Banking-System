import os
import pytest
from database import Base, Client, Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from client_service import create_client, get_next_client_id, delete_client, deposit, withdraw, get_statement, list_balances, list_clients
from exceptions import InvalidData, ClientNotFound, InvalidAmount, InsufficientBalance

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

    deleted_id = delete_client(db, client1.client_id) 
    assert deleted_id == 1

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
def test_create_client_invalid_balance(db, balance):
    with pytest.raises(InvalidData):
        create_client(db, "Karol", "Nowak", balance)

@pytest.mark.parametrize("id", [0, -1, None, "1", 1.5, [], {}])
def test_delete_client_invalid_id(db, id):
    with pytest.raises(InvalidData):
        delete_client(db, id)

def test_delete_client_not_found(db):
    with pytest.raises(ClientNotFound):
        delete_client(db, 999)

@pytest.mark.parametrize("id", [0, -1, None, "1", 1.5, [], {}])
def test_deposit_invalid_id(db, id):
    with pytest.raises(InvalidData):
        deposit(db, id, amount=50)

@pytest.mark.parametrize("amount", [0, -1, -100, None, "100", 12.5, [], {}])
def test_deposit_invalid_amount(db, amount):
    with pytest.raises(InvalidAmount):
        client1 = create_client(db, "Karol", "Nowak", 1000)
        deposit(db, client1.client_id, amount)

def test_deposit_client_not_found(db):
    with pytest.raises(ClientNotFound):
        deposit(db, 999, 1500)

@pytest.mark.parametrize("amount", [50, 60, 70, 2837, 6983])
def test_deposit_correct_balance(db, amount):
    client1 = create_client(db, "Karol", "Nowak", 10000) 
    deposited = deposit(db, client1.client_id, amount) 
    assert deposited == 10_000 + amount

def test_deposit_creates_transaction_and_updates_balance(db):
    client = create_client(db, "Karol", "Nowak", 1000)

    new_balance = deposit(db, client.client_id, 500)
    assert new_balance == 1500

    refreshed_client = db.query(Client).filter_by(client_id=client.client_id).one()
    assert refreshed_client.balance == 1500

    transactions = db.query(Transaction).filter_by(client_id=client.client_id).all()
    assert len(transactions) == 1

    tx = transactions[0]
    assert tx.client_id == client.client_id
    assert tx.transaction_type == "deposit"
    assert tx.amount == 500


@pytest.mark.parametrize("id", [0, -1, None, "1", 1.5, [], {}])
def test_withdraw_invalid_id(db, id):
    with pytest.raises(InvalidData):
        withdraw(db, id, amount=50)

@pytest.mark.parametrize("amount", [0, -1, -100, None, "100", 12.5, [], {}])
def test_withdraw_invalid_amount(db, amount):
    with pytest.raises(InvalidAmount):
        client1 = create_client(db, "Karol", "Nowak", 1000)
        withdraw(db, client1.client_id, amount)

def test_withdraw_client_not_found(db):
    with pytest.raises(ClientNotFound):
        withdraw(db, 999, 1500)

@pytest.mark.parametrize("amount", [50, 60, 150, 90])
def test_withdraw_insufficienet_balance(db, amount):
    with pytest.raises(InsufficientBalance):
        client1 = create_client(db, "Karol", "Nowak", 10)
        withdraw(db, client1.client_id, amount)

def test_withdraw_insufficient_balance_creates_no_transaction(db):
    client = create_client(db, "Karol", "Nowak", 100)

    with pytest.raises(InsufficientBalance):
        withdraw(db, client.client_id, 500)

    refreshed_client = db.query(Client).filter_by(client_id=client.client_id).one()
    assert refreshed_client.balance == 100

    transactions = db.query(Transaction).filter_by(client_id=client.client_id).all()
    assert transactions == []

       
@pytest.mark.parametrize("amount", [50, 60, 70, 2837, 6983])
def test_withdraw_correct_balance(db, amount):
    client1 = create_client(db, "Karol", "Nowak", 10000) 
    withdrawed = withdraw(db, client1.client_id, amount)
    assert withdrawed == 10_000 - amount

def test_withdraw_creates_transaction_and_updates_balance(db):
    client = create_client(db, "Karol", "Nowak", 1000)

    new_balance = withdraw(db, client.client_id, 400)
    assert new_balance == 600

    refreshed_client = db.query(Client).filter_by(client_id=client.client_id).one()
    assert refreshed_client.balance == 600


    transactions = db.query(Transaction).filter_by(client_id=client.client_id).all()
    assert len(transactions) == 1

    tx = transactions[0]
    assert tx.transaction_type == "withdraw"
    assert tx.amount == 400

def test_get_statement_client_not_found(db):
    with pytest.raises(ClientNotFound):
        get_statement(db, 999)

@pytest.mark.parametrize("client_id", [0, -1, None, "1", 1.5, [], {}])
def test_get_statement_invalid_client_id(db, client_id):
    with pytest.raises(InvalidData):
        get_statement(db, client_id)

def test_get_statement_returns_all_transactions_in_order(db):
    client = create_client(db, "Karol", "Nowak", 1000)

    deposit(db, client.client_id, 200)
    withdraw(db, client.client_id, 100)
    deposit(db, client.client_id, 50)

    statement = get_statement(db, client.client_id)

    assert len(statement) == 3

    assert statement[0].transaction_type == "deposit"
    assert statement[0].amount == 200

    assert statement[1].transaction_type == "withdraw"
    assert statement[1].amount == 100

    assert statement[2].transaction_type == "deposit"
    assert statement[2].amount == 50

def test_list_clients_empty_db(db):
    clients = list_clients(db)
    assert clients == []

def test_list_clients_returns_all_clients(db):
    c1 = create_client(db, "A", "A", 100)
    c2 = create_client(db, "B", "B", 200)
    c3 = create_client(db, "C", "C", 300)

    clients = list_clients(db)

    assert len(clients) == 3
    assert [c.client_id for c in clients] == [1, 2, 3]

def test_list_balances_returns_correct_balances(db):
    c1 = create_client(db, "Karol", "Nowak", 1000)
    c2 = create_client(db, "Anna", "Kowalska", 500)

    deposit(db, c1.client_id, 200)
    withdraw(db, c2.client_id, 100)

    balances = list_balances(db)

    balances_dict = {c.client_id: c.balance for c in balances}

    assert balances_dict[c1.client_id] == 1200
    assert balances_dict[c2.client_id] == 400
