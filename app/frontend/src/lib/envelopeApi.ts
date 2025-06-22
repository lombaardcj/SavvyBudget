// src/lib/envelopeApi.ts
import { getToken } from './api';

const API_URL = 'http://localhost:8000';

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

export async function createEnvelope(data: { name: string; description?: string; color: string }) {
  const res = await fetch(`${API_URL}/envelopes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

export async function updateEnvelope(id: number, data: { name: string; description?: string; color: string }) {
  const res = await fetch(`${API_URL}/envelopes/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

export async function deleteEnvelope(id: number) {
  const res = await fetch(`${API_URL}/envelopes/${id}`, {
    method: 'DELETE',
    headers: { ...authHeaders() }
  });
  if (!res.ok) throw new Error(await res.text());
  return true;
}

export async function getTransactions(envelopeId: number) {
  const res = await fetch(`${API_URL}/envelopes/${envelopeId}/transactions`, {
    headers: { ...authHeaders() }
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

export async function createTransaction(envelopeId: number, data: { amount: number; date?: string; description?: string }) {
  const res = await fetch(`${API_URL}/envelopes/${envelopeId}/transactions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

export async function deleteTransaction(envelopeId: number, transactionId: number) {
  const res = await fetch(`${API_URL}/envelopes/${envelopeId}/transactions/${transactionId}`, {
    method: 'DELETE',
    headers: { ...authHeaders() }
  });
  if (!res.ok) throw new Error(await res.text());
  return true;
}
