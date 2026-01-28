from exceptions import InvalidData, InsufficientBalance, InvalidAmount

class Client:

    def __init__(self, id, name, surname, balance):
        if type(id) is not int or id <= 0:
            raise InvalidData("ID must be provided and be more than zero.")
        if type(name) is not str or name.strip() == "":
            raise InvalidData("Name must be provided and explicitly be a string.")
        if type(surname) is not str or surname.strip() == "":
            raise InvalidData("Surname must be provided and explicitly be a string.")
        if type(balance) is not int or balance < 0:
            raise InvalidData("Initial balance cannot be below zero.")
        self.id = id
        self.name = name
        self.surname = surname
        self._balance = balance

    def __str__(self):
        return f"Client {self.name} {self.surname} with an ID number: {self.id} has currently balance = {self.balance}"

    def __repr__(self):
        return f"Client(id={self.id}, name='{self.name}', surname='{self.surname}', balance={self._balance})"
    
    @property
    def balance(self):
        return self._balance

    def withdraw(self, amount):
        if type(amount) is not int or amount <= 0:
            raise InvalidAmount("Amount for withdrawal must be greater then zero.")
        if self.balance - amount < 0:
            raise InsufficientBalance("You cannot withdraw money, your balance is not high enough.")
        self._balance -= amount
        return self.balance
    
    def deposit(self, amount):
        if type(amount) is not int or amount <= 0:
            raise InvalidAmount("Amount for deposit must be grater then zero.")
        self._balance += amount
        return self.balance