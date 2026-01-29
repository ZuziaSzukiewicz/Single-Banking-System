
class InvalidData(ValueError):
    pass

class InsufficientBalance(ValueError):
    pass

class InvalidAmount(ValueError):
    pass

class InvalidTransactionType(ValueError):
    pass

class ClientNotFound(LookupError):
    pass