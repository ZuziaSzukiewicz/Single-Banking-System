from exceptions import InvalidTransactionType, InvalidAmount
from datetime import datetime

class Transaction:
    def __init__(self, client_id, transaction_type, amount):
        if type(transaction_type) is not str or transaction_type not in ["withdraw", "deposit"]:
            raise InvalidTransactionType("You can perform either a withdraw or deposit operation.")
        if type(amount) is not int or amount <= 0:
            raise InvalidAmount("Provided amount must be an integer greater than zero")
        self.client_id = client_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = datetime.utcnow()

    def __str__(self):
        return f'Client identified with an id number: {self.client_id} performs a {self.transaction_type} with an amount {self.amount} at {self.date.strftime("%Y-%m-%d %H:%M:%S")}'
    
    def __repr__(self):
        return f"Transaction(client_id={self.client_id}, '  '={self.transaction_type}, amount={self.amount}, date={self.date})"