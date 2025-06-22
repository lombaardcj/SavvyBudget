# SavvyBudget

Take control of your finances with SavvyBudget! 📩 A smart envelope budgeting tool to organize monthly expenses, stash savings, and become a money-savvy pro. Budget wisely, win big! 💸 #SavvyBudget

## Project Structure
- `backend/`: FastAPI backend (Python, SQLite, JWT auth)
- `frontend/`: SvelteKit frontend (Svelte, Tailwind CSS)

## Setup (Replit)

### Backend
1. `cd backend`
2. `source ../backend-venv/bin/activate`
3. `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev -- --host`

## API Endpoints
- See FastAPI docs at `/docs` when backend is running.

## Features
- User registration/login (JWT)
- Envelope CRUD (name, description, color, balance)
- Transaction CRUD (amount, date, description)
- Real-time dashboard, filtering, and history

## Notes
- All data stored in SQLite for Replit compatibility.
- See code comments for further details.
