from pydantic import BaseModel
from datetime import datetime

class CreateClient(BaseModel):
    name: str
    surname: str
    balance: int

class ClientOut(BaseModel):
    client_id: int
    name: str
    surname: str
    balance: int

    class Config:
        from_attributes = True

class AmountIn(BaseModel):
    amount: int

class TransactionOut(BaseModel):
    id: int
    client_id: int
    transaction_type: str
    amount: int
    date: datetime

    class Config:
        from_attributes = True