<script lang="ts">
import { register, setToken } from '$lib/api';
import { goto } from '$app/navigation';
import { setUser } from '$lib/stores';
let username = '';
let password = '';
let error = '';

async function handleRegister() {
  error = '';
  try {
    const data = await register(username, password);
    setToken(data.access_token);
    setUser(username);
    goto('/dashboard');
  } catch (e) {
    error = e instanceof Error ? e.message : 'Registration failed';
  }
}
</script>

<div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
  <form class="bg-white p-8 rounded shadow w-full max-w-sm" on:submit|preventDefault={handleRegister}>
    <h2 class="text-2xl font-bold mb-4">Register</h2>
    {#if error}
      <div class="text-red-500 mb-2">{error}</div>
    {/if}
    <input class="input mb-2 w-full" type="text" placeholder="Username" bind:value={username} required />
    <input class="input mb-4 w-full" type="password" placeholder="Password" bind:value={password} required />
    <button class="btn w-full bg-green-600 text-white py-2 rounded hover:bg-green-700" type="submit">Register</button>
    <div class="mt-4 text-sm text-center">
      Already have an account? <a href="/login" class="text-blue-600 hover:underline">Login</a>
    </div>
  </form>
</div>

<style>
.input { @apply border p-2 rounded; }
</style>
