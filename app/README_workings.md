# SavvyBudget Backend: How It Works

This document explains the structure and usage of the FastAPI backend for SavvyBudget, including authentication and available API endpoints for managing users, envelopes, and transactions.

## Authentication
- **JWT-based authentication** is used. Users must register and log in to receive a token.
- The token must be included in the `Authorization` header as `Bearer <token>` for all protected endpoints.

### Register a User
- **Endpoint:** `POST /register`
- **Body:** `{ "username": "yourname", "password": "yourpassword" }`
- **Response:** User object (without password)

### Login (Obtain Token)
- **Endpoint:** `POST /token`
- **Body:** Form data: `username`, `password`
- **Response:** `{ "access_token": "...", "token_type": "bearer" }`
- **Usage:** Use `access_token` in the `Authorization` header for all further requests:
  - `Authorization: Bearer <access_token>`

## Health Check
- **Endpoint:** `GET /health`
- **Response:** `{ "status": "ok" }`
- **Purpose:** Check if the backend is running.

## Envelope Endpoints (CRUD)
- **All endpoints below require authentication.**

- **List Envelopes:**
  - `GET /envelopes`
  - Returns all envelopes for the current user.

- **Create Envelope:**
  - `POST /envelopes`
  - Body: `{ "name": "Groceries", "description": "", "color": "#38bdf8" }`
  - Returns the created envelope.

- **Update Envelope:**
  - `PUT /envelopes/{envelope_id}`
  - Body: `{ "name": "...", "description": "...", "color": "..." }`
  - Returns the updated envelope.

- **Delete Envelope:**
  - `DELETE /envelopes/{envelope_id}`
  - Returns success status.

## Transaction Endpoints (CRUD)
- **All endpoints below require authentication.**

- **List Transactions:**
  - `GET /envelopes/{envelope_id}/transactions`
  - Returns all transactions for the specified envelope.

- **Create Transaction:**
  - `POST /envelopes/{envelope_id}/transactions`
  - Body: `{ "amount": 50, "date": "2025-06-22T00:00:00", "description": "Grocery shopping" }`
  - Returns the created transaction.

- **Delete Transaction:**
  - `DELETE /envelopes/{envelope_id}/transactions/{transaction_id}`
  - Returns success status.

## Summary of Models
- **User:** username, hashed_password
- **Envelope:** name, description, color, user_id
- **Transaction:** amount, date, description, envelope_id

## Making API Calls
1. Register or log in to get a JWT token.
2. For all envelope/transaction endpoints, include the token in the `Authorization` header.
3. Use the endpoints above to create, read, update, or delete envelopes and transactions.

---

**Note:**
- All endpoints return JSON.
- If you receive a 401 error, check your token and ensure it is included in the header.
- The backend uses SQLite for persistence and is designed to be Replit-compatible.
