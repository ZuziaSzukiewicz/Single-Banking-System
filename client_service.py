from database import Client
from exceptions import InvalidData, ClientNotFound

def get_next_client_id(db):
    ids = db.query(Client.client_id).order_by(Client.client_id).all()
    expected = 1
    for (client_id,) in ids:
        if client_id == expected:
            expected += 1
        else:
            break
    return expected

def create_client(db, name, surname, balance):
    if type(name) is not str or name.strip() == "":
        raise InvalidData("Name must be provided and explicitly be a string.")
    if type(surname) is not str or surname.strip() == "":
        raise InvalidData("Surname must be provided and explicitly be a string.")
    if type(balance) is not int or balance < 0:
        raise InvalidData("Initial balance cannot be below zero.")
    unique_id = get_next_client_id(db)
    client = Client(client_id=unique_id, name=name, surname=surname, balance=balance)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def delete_client(db, client_id):
    if type(client_id) is not int or client_id <= 0:
        raise InvalidData("ID must be provided and be more than zero.")
    client = db.query(Client).filter_by(client_id=client_id).one_or_none()
    if client is None:
        raise ClientNotFound("Client was not found in the database")
    db.delete(client)
    db.commit()
    return client_id