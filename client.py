from exceptions import InvalidData, InsufficientBalance, InvalidAmount, NegativeBalance

class Client:

    def __init__(self, id, name, surname, balance):
        if not id:
            raise InvalidData("ID must be provided.")
        if not name or not surname:
            raise InvalidData("Name/Surname must be provided.")
        if balance < 0:
            raise NegativeBalance("Initial balance cannot be below zero.")
        self.id = id
        self.name = name
        self.surname = surname
        self._balance = balance

    def __str__(self):
        return f"Client {self.name} {self.surname} with ID number: {self.id} has currently {self.balance}"

    def __repr__(self):
        return f"Client(id={self.id}, name='{self.name}', surname='{self.surname}', balance={self._balance})"
    
    @property
    def balance(self):
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmount("Amount for withdrawal must be greater then zero.")
        if self.balance - amount < 0:
            raise InsufficientBalance("You cannot withdraw money, your balance is not high enough.")
        self._balance -= amount
        return self.balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmount("Amount for deposit must be grater then zero.")
        self._balance += amount
        return self.balance