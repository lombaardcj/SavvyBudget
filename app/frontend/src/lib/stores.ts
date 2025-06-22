// src/lib/stores.ts
import { writable } from 'svelte/store';

export const user = writable<string | null>(null);

export function setUser(username: string | null) {
  user.set(username);
  if (username) {
    localStorage.setItem('username', username);
  } else {
    localStorage.removeItem('username');
  }
}

export function loadUser() {
  const username = localStorage.getItem('username');
  user.set(username);
}
