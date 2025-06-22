
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth, database
from typing import List, Optional
from .database import SessionLocal, init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user
def get_current_user(db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    return auth.get_current_user(token, db)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Envelope Endpoints
@app.get("/envelopes", response_model=List[schemas.Envelope])
def list_envelopes(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_envelopes(db, user_id=current_user.id)

@app.get("/envelopes/{envelope_id}", response_model=schemas.Envelope)
def get_envelope(envelope_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    envelope = crud.get_envelope(db, envelope_id, user_id=current_user.id)
    if not envelope:
        raise HTTPException(status_code=404, detail="Envelope not found")
    return envelope

@app.post("/envelopes", response_model=schemas.Envelope)
def create_envelope(envelope: schemas.EnvelopeCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_envelope(db, envelope, user_id=current_user.id)

@app.put("/envelopes/{envelope_id}", response_model=schemas.Envelope)
def update_envelope(envelope_id: int, envelope: schemas.EnvelopeCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated = crud.update_envelope(db, envelope_id, envelope, user_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Envelope not found")
    return updated

@app.delete("/envelopes/{envelope_id}")
def delete_envelope(envelope_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = crud.delete_envelope(db, envelope_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Envelope not found")
    return {"ok": True}

# Transaction Endpoints
@app.get("/envelopes/{envelope_id}/transactions", response_model=List[schemas.Transaction])
def list_transactions(envelope_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from datetime import datetime
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None
    return crud.get_transactions(db, envelope_id, user_id=current_user.id, start_date=start, end_date=end)

@app.post("/envelopes/{envelope_id}/transactions", response_model=schemas.Transaction)
def create_transaction(envelope_id: int, transaction: schemas.TransactionCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    created = crud.create_transaction(db, transaction, envelope_id, user_id=current_user.id)
    if not created:
        raise HTTPException(status_code=404, detail="Envelope not found")
    return created

@app.put("/envelopes/{envelope_id}/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(envelope_id: int, transaction_id: int, transaction: schemas.TransactionCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated = crud.update_transaction(db, transaction_id, transaction, envelope_id, user_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated

@app.delete("/envelopes/{envelope_id}/transactions/{transaction_id}")
def delete_transaction(envelope_id: int, transaction_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    deleted = crud.delete_transaction(db, transaction_id, envelope_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"ok": True}

