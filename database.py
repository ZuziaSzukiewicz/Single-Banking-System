from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, autoincrement=False, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)

    transactions = relationship("Transaction", back_populates="client", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    transaction_type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, server_default=func.now())

    client = relationship("Client", back_populates="transactions")
    

