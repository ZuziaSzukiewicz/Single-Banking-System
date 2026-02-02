from pydantic import BaseModel, StrictStr, StrictInt
from datetime import datetime

class CreateClient(BaseModel):
    name: StrictStr
    surname: StrictStr
    balance: StrictInt

class ClientOut(BaseModel):
    client_id: StrictInt
    name: StrictStr
    surname: StrictStr
    balance: StrictInt

    class Config:
        from_attributes = True

class AmountIn(BaseModel):
    amount: StrictInt

class TransactionOut(BaseModel):
    id: StrictInt
    client_id: StrictInt
    transaction_type: StrictStr
    amount: StrictInt
    date: datetime

    class Config:
        from_attributes = True