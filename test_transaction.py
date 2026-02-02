import pytest
from transaction import Transaction
from exceptions import InvalidTransactionType, InvalidAmount

@pytest.mark.parametrize("transaction_type", ["get", "pay", "outdraw", " ", "", None, [1,2,3], 1223])
def test_wrong_transaction_type(transaction_type):
    with pytest.raises(InvalidTransactionType):
        Transaction(1234, transaction_type, 304)

@pytest.mark.parametrize("transaction_type", ["withdraw", "deposit"])
def test_correct_transaction_type(transaction_type):
    transaction = Transaction(1234, transaction_type, 304)
    assert transaction.transaction_type == transaction_type

@pytest.mark.parametrize("amount", [0, -120, -10002, 120*(-1203), [1,2,3], {"amount": 123}, None])
@pytest.mark.parametrize("transaction_type", ["withdraw", "deposit"])
def test_wrong_amount(amount, transaction_type):
    with pytest.raises(InvalidAmount):
        Transaction(1234, transaction_type, amount)

@pytest.mark.parametrize("amount", [1, 120, 151900 ])
@pytest.mark.parametrize("transaction_type", ["withdraw", "deposit"])
def test_correct_amount(amount, transaction_type):
    transaction = Transaction(1234, transaction_type, amount)
    assert transaction.amount == amount

def test_transaction_str_contains_correct_data():
    transaction = Transaction(1234, "withdraw", 151900)
    s = str(transaction)

    assert "Client identified with an id number: 1234" in s
    assert "withdraw" in s
    assert "151900" in s

