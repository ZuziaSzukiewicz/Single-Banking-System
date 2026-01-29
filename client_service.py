from database import Client
from exceptions import InvalidData

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
