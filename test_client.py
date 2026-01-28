import pytest
from client import Client
from exceptions import *

@pytest.mark.parametrize("id", [0, -1, -1100000, "smith", None, [123], {"id": 123}])
def test__wrong_data_in_constuctor_id(id):
    with pytest.raises(InvalidData):
        Client(id, "Karl", "Smith", 154) 

@pytest.mark.parametrize("id", [1232, 12, 1])
def test__correct_data_in_constuctor_id(id):
        client = Client(id, "Karl", "Smith", 154)
        assert client.id == id

@pytest.mark.parametrize("name", [1232, ["Zuzia"], "", None, " ",  {"surname": "Zuzia"}])
def test__wrong_data_in_constuctor_name(name):
    with pytest.raises(InvalidData):
        Client(1234, name, "Smith", 154) 

@pytest.mark.parametrize("name", ["Zuza", "Karol", "Kamila"])
def test__correct_data_in_constuctor_name(name):
        client = Client(1234, name, "Smith", 154)
        assert client.name == name

@pytest.mark.parametrize("surname", [1232, ["Zuzia"], "", None, " ", {"surname": "Zuzia"}])
def test__wrong_data_in_constuctor_surname(surname):
    with pytest.raises(InvalidData):
        Client(1234, "Karol", surname, 154) 

@pytest.mark.parametrize("surname", ["Zuza", "Karol", "Kamila"])
def test__correct_data_in_constuctor_surname(surname):
        client = Client(1234, "Karol", surname, 154)
        assert client.surname == surname

@pytest.mark.parametrize("balance", [-1, -1100000, "smith", None, [123], {"id": 123}])
def test__wrong_data_in_constuctor_balance(balance):
    with pytest.raises(InvalidData):
        Client(1234, "Karl", "Smith", balance) 

@pytest.mark.parametrize("balance", [1232, 12, 1, 0])
def test__correct_data_in_constuctor_balance(balance):
        client = Client(1234, "Karl", "Smith", balance)
        assert client.balance == balance

def test_str():
     client = Client(12, "Karol", "Nowak", 0)
     assert str(client) == "Client Karol Nowak with an ID number: 12 has currently balance = 0"

def test_repr():
    client = Client(12, "Karol", "Nowak", 0)
    assert repr(client) == "Client(id=12, name='Karol', surname='Nowak', balance=0)"

@pytest.mark.parametrize("amount", [0, -12, "smith", None, [123], {"id": 123}])
def test_wrong_data_withdrawl(amount):
     with pytest.raises(InvalidAmount):
        client = Client(12, "Karol", "Nowak", 0)
        Client.withdraw(client, amount)

#po dodaniu tego liczba testów sie zmniejszyla a nie zwiększyła
@pytest.mark.parametrize("amount", [15, 130, 40, 50])
def test_wrong_data_withdrawl(amount):
     with pytest.raises(InsufficientBalance):
        client = Client(12, "Karol", "Nowak", 0)
        Client.withdraw(client, amount)

#te normalnie się dodała ilość
@pytest.mark.parametrize("amount", [1232, 12, 1])
def test__correct_data_withdrawl(amount):
        client = Client(1234, "Karl", "Smith", 50000)
        Client.withdraw(client, amount)

@pytest.mark.parametrize("amount", [0, -12, "smith", None, [123], {"id": 123}])
def test_wrong_data_deposit(amount):
     with pytest.raises(InvalidAmount):
        client = Client(12, "Karol", "Nowak", 0)
        Client.withdraw(client, amount)

@pytest.mark.parametrize("amount", [1232, 12, 1])
def test__correct_data_deposit(amount):
        client = Client(1234, "Karl", "Smith", 50000)
        Client.withdraw(client, amount)
