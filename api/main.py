from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from session import init_db, get_session
from client_service import create_client, list_clients, get_client, deposit, withdraw, get_statement, delete_client
from api.schemas import CreateClient, ClientOut, AmountIn, TransactionOut
from sqlalchemy.orm import Session
from exceptions import InvalidData, InvalidAmount, InsufficientBalance, ClientNotFound


app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

def get_db():
    db = get_session()
    try: 
        yield db
    finally:
        db.close()

@app.post("/clients", response_model = ClientOut)
def create_client_endpoint(payload: CreateClient, db: Session = Depends(get_db)):
    client = create_client(db, payload.name, payload.surname, payload.balance)
    return client   

@app.get("/clients", response_model=list[ClientOut])
def list_clients_endpoint(db: Session = Depends(get_db)):
    return list_clients(db)

@app.get("/clients/{client_id}", response_model=ClientOut)
def get_client_endpoint(client_id: int, db: Session = Depends(get_db)):
    return get_client(db, client_id)

@app.exception_handler(ClientNotFound)
def client_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(InvalidData)
@app.exception_handler(InvalidAmount)
@app.exception_handler(InsufficientBalance)
def bad_request_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.post("/clients/{client_id}/deposit")
def deposit_endpoint(client_id: int, payload: AmountIn, db: Session = Depends(get_db)):
    new_balance = deposit(db, client_id, payload.amount)
    return {"client_id": client_id, "balance": new_balance}

@app.post("/clients/{client_id}/withdraw")
def withdraw_endpoint(client_id: int, payload: AmountIn, db: Session = Depends(get_db)):
    new_balance = withdraw(db, client_id, payload.amount)
    return {"client_id": client_id, "balance": new_balance}

@app.get("/clients/{client_id}/statement", response_model=list[TransactionOut])
def statement_endpoint(client_id: int, db: Session = Depends(get_db)):
    return get_statement(db, client_id)

@app.delete("/clients/{client_id}")
def delete_client_endpoint(client_id: int, db: Session = Depends(get_db)):
    deleted_id = delete_client(db, client_id)
    return {"deleted_client_id": deleted_id}

