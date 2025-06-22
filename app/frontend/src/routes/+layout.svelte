<script lang="ts">
import { user, loadUser, setUser } from '$lib/stores';
import { goto } from '$app/navigation';
import { onMount } from 'svelte';

onMount(() => {
  loadUser();
});

function logout() {
  localStorage.removeItem('token');
  setUser(null);
  goto('/login');
}
</script>

<nav class="bg-gray-800 text-white p-4 flex items-center justify-between">
  <a href="/dashboard" class="font-bold text-xl">SavvyBudget</a>
  <div class="flex gap-4 items-center">
    {#if $user}
      <span class="text-sm">Hello, {$user}!</span>
      <button class="bg-red-500 px-3 py-1 rounded hover:bg-red-600" on:click={logout}>Logout</button>
    {:else}
      <a href="/login" class="hover:underline">Login</a>
      <a href="/register" class="hover:underline">Register</a>
    {/if}
  </div>
</nav>

<slot />
