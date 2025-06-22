from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash
from typing import List, Optional
from datetime import datetime

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_envelopes(db: Session, user_id: int) -> List[models.Envelope]:
    return db.query(models.Envelope).filter(models.Envelope.user_id == user_id).all()

def get_envelope(db: Session, envelope_id: int, user_id: int) -> Optional[models.Envelope]:
    return db.query(models.Envelope).filter(models.Envelope.id == envelope_id, models.Envelope.user_id == user_id).first()

def create_envelope(db: Session, envelope: schemas.EnvelopeCreate, user_id: int) -> models.Envelope:
    db_envelope = models.Envelope(**envelope.model_dump(), user_id=user_id)
    db.add(db_envelope)
    db.commit()
    db.refresh(db_envelope)
    return db_envelope

def update_envelope(db: Session, envelope_id: int, envelope: schemas.EnvelopeCreate, user_id: int) -> Optional[models.Envelope]:
    db_envelope = get_envelope(db, envelope_id, user_id)
    if db_envelope:
        for key, value in envelope.model_dump().items():
            setattr(db_envelope, key, value)
        db.commit()
        db.refresh(db_envelope)
    return db_envelope

def delete_envelope(db: Session, envelope_id: int, user_id: int) -> bool:
    db_envelope = get_envelope(db, envelope_id, user_id)
    if db_envelope:
        db.delete(db_envelope)
        db.commit()
        return True
    return False

def get_transactions(db: Session, envelope_id: int, user_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[models.Transaction]:
    query = db.query(models.Transaction).join(models.Envelope).filter(models.Envelope.id == envelope_id, models.Envelope.user_id == user_id)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    return query.all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate, envelope_id: int, user_id: int) -> Optional[models.Transaction]:
    envelope = get_envelope(db, envelope_id, user_id)
    if not envelope:
        return None
    db_transaction = models.Transaction(**transaction.model_dump(), envelope_id=envelope_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: schemas.TransactionCreate, envelope_id: int, user_id: int) -> Optional[models.Transaction]:
    db_transaction = db.query(models.Transaction).join(models.Envelope).filter(models.Transaction.id == transaction_id, models.Envelope.id == envelope_id, models.Envelope.user_id == user_id).first()
    if db_transaction:
        for key, value in transaction.model_dump().items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, envelope_id: int, user_id: int) -> bool:
    db_transaction = db.query(models.Transaction).join(models.Envelope).filter(models.Transaction.id == transaction_id, models.Envelope.id == envelope_id, models.Envelope.user_id == user_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return True
    return False
