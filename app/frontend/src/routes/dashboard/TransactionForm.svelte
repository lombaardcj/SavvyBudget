<script lang="ts">
export let transaction = { amount: 0, date: '', description: '' };
export let onSave: (data: typeof transaction) => void;
let local = { ...transaction };

function handleSubmit() {
  onSave(local);
}
</script>

<form class="space-y-2" on:submit|preventDefault={handleSubmit}>
  <input class="input w-full" type="number" step="0.01" placeholder="Amount" bind:value={local.amount} required />
  <input class="input w-full" type="date" bind:value={local.date} />
  <input class="input w-full" type="text" placeholder="Description (optional)" bind:value={local.description} />
  <button class="btn bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700" type="submit">Save</button>
</form>

<style>
.input { @apply border p-2 rounded; }
</style>
