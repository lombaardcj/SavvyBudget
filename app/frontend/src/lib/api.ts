// src/lib/api.ts
// SvelteKit API service for FastAPI backend

const API_URL = 'http://localhost:8000';

export async function register(username: string, password: string) {
  const res = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

export async function login(username: string, password: string) {
  const res = await fetch(`${API_URL}/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username, password })
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

export function setToken(token: string) {
  localStorage.setItem('token', token);
}

export function getToken(): string | null {
  return localStorage.getItem('token');
}

function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function getEnvelopes() {
  const res = await fetch(`${API_URL}/envelopes`, {
    headers: { ...authHeaders() }
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

// Add more envelope/transaction API functions as needed
