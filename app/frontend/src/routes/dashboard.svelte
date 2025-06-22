<script lang="ts">
import { onMount } from 'svelte';
import { getEnvelopes, createEnvelope, updateEnvelope, deleteEnvelope, getTransactions, createTransaction, deleteTransaction } from '$lib/envelopeApi';
import EnvelopeForm from './dashboard/EnvelopeForm.svelte';
import TransactionForm from './dashboard/TransactionForm.svelte';
import { getToken } from '$lib/api';
import { goto } from '$app/navigation';

let envelopes = [];
let selectedEnvelope = null;
let transactions = [];
let showEnvelopeForm = false;
let editingEnvelope = null;
let showTransactionForm = false;
let editingTransaction = null;
let error = '';

async function loadEnvelopes() {
  try {
    envelopes = await getEnvelopes();
  } catch (e) {
    error = e instanceof Error ? e.message : 'Failed to load envelopes';
  }
}

async function selectEnvelope(env) {
  selectedEnvelope = env;
  await loadTransactions(env.id);
}

async function loadTransactions(envelopeId) {
  try {
    transactions = await getTransactions(envelopeId);
  } catch (e) {
    error = e instanceof Error ? e.message : 'Failed to load transactions';
  }
}

async function handleEnvelopeSave(data) {
  try {
    if (editingEnvelope) {
      await updateEnvelope(editingEnvelope.id, data);
    } else {
      await createEnvelope(data);
    }
    showEnvelopeForm = false;
    editingEnvelope = null;
    await loadEnvelopes();
  } catch (e) {
    error = e instanceof Error ? e.message : 'Failed to save envelope';
  }
}

async function handleEnvelopeDelete(env) {
  if (confirm('Delete this envelope?')) {
    await deleteEnvelope(env.id);
    if (selectedEnvelope && selectedEnvelope.id === env.id) {
      selectedEnvelope = null;
      transactions = [];
    }
    await loadEnvelopes();
  }
}

async function handleTransactionSave(data) {
  try {
    if (editingTransaction) {
      // Update transaction logic (not implemented in backend yet)
    } else {
      await createTransaction(selectedEnvelope.id, data);
    }
    showTransactionForm = false;
    editingTransaction = null;
    await loadTransactions(selectedEnvelope.id);
  } catch (e) {
    error = e instanceof Error ? e.message : 'Failed to save transaction';
  }
}

async function handleTransactionDelete(tx) {
  if (confirm('Delete this transaction?')) {
    await deleteTransaction(selectedEnvelope.id, tx.id);
    await loadTransactions(selectedEnvelope.id);
  }
}

onMount(async () => {
  if (!getToken()) {
    goto('/login');
    return;
  }
  await loadEnvelopes();
});
</script>

<div class="p-4 max-w-4xl mx-auto">
  <h1 class="text-2xl font-bold mb-4">Your Envelopes</h1>
  {#if error}
    <div class="text-red-500 mb-2">{error}</div>
  {/if}
  <div class="flex gap-8">
    <div class="w-1/2">
      <button class="mb-2 bg-blue-600 text-white px-4 py-2 rounded" on:click={() => { showEnvelopeForm = true; editingEnvelope = null; }}>+ Add Envelope</button>
      <div class="grid grid-cols-1 gap-2">
        {#each envelopes as env}
          <div class="rounded shadow p-4 flex justify-between items-center cursor-pointer" style="background-color: {env.color}" on:click={() => selectEnvelope(env)}>
            <div>
              <div class="font-bold text-lg">{env.name}</div>
              <div class="text-sm">{env.description}</div>
            </div>
            <div class="flex gap-2 items-center">
              <button class="text-xs bg-yellow-400 px-2 py-1 rounded" on:click|stopPropagation={() => { showEnvelopeForm = true; editingEnvelope = env; }}>Edit</button>
              <button class="text-xs bg-red-500 text-white px-2 py-1 rounded" on:click|stopPropagation={() => handleEnvelopeDelete(env)}>Delete</button>
            </div>
          </div>
        {/each}
      </div>
      {#if showEnvelopeForm}
        <div class="mt-4 bg-white p-4 rounded shadow">
          <EnvelopeForm envelope={editingEnvelope ?? { name: '', description: '', color: '#38bdf8' }} onSave={handleEnvelopeSave} />
          <button class="mt-2 text-sm text-gray-500 hover:underline" on:click={() => { showEnvelopeForm = false; editingEnvelope = null; }}>Cancel</button>
        </div>
      {/if}
    </div>
    <div class="w-1/2">
      {#if selectedEnvelope}
        <div class="mb-2">
          <div class="font-bold text-lg">{selectedEnvelope.name}</div>
          <div class="text-sm">{selectedEnvelope.description}</div>
          <div class="font-mono">Balance: <span class="font-bold">{selectedEnvelope.balance ?? 0}</span></div>
        </div>
        <button class="mb-2 bg-green-600 text-white px-4 py-2 rounded" on:click={() => { showTransactionForm = true; editingTransaction = null; }}>+ Add Transaction</button>
        <div class="bg-white rounded shadow p-2 mb-2">
          <div class="font-bold mb-2">Transactions</div>
          <div class="space-y-2">
            {#each transactions as tx}
              <div class="flex justify-between items-center border-b pb-1">
                <div>
                  <span class="font-mono">{tx.amount > 0 ? '+' : ''}{tx.amount}</span>
                  <span class="ml-2 text-xs text-gray-500">{tx.date?.slice(0, 10)}</span>
                  <span class="ml-2 text-xs">{tx.description}</span>
                </div>
                <button class="text-xs bg-red-500 text-white px-2 py-1 rounded" on:click={() => handleTransactionDelete(tx)}>Delete</button>
              </div>
            {/each}
          </div>
        </div>
        {#if showTransactionForm}
          <div class="mt-2 bg-white p-4 rounded shadow">
            <TransactionForm transaction={editingTransaction ?? { amount: 0, date: '', description: '' }} onSave={handleTransactionSave} />
            <button class="mt-2 text-sm text-gray-500 hover:underline" on:click={() => { showTransactionForm = false; editingTransaction = null; }}>Cancel</button>
          </div>
        {/if}
      {/if}
    </div>
  </div>
</div>
