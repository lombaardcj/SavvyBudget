from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    date: Optional[datetime] = None
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    envelope_id: int
    class Config:
        orm_mode = True

class EnvelopeBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: str

class EnvelopeCreate(EnvelopeBase):
    pass

class Envelope(EnvelopeBase):
    id: int
    user_id: int
    transactions: List[Transaction] = []
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    envelopes: List[Envelope] = []
    class Config:
        orm_mode = True
