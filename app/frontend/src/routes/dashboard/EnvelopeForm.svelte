<script lang="ts">
export let envelope = { name: '', description: '', color: '#38bdf8' };
export let onSave: (data: typeof envelope) => void;
let local = { ...envelope };

function handleSubmit() {
  onSave(local);
}
</script>

<form class="space-y-2" on:submit|preventDefault={handleSubmit}>
  <input class="input w-full" type="text" placeholder="Name" bind:value={local.name} required />
  <input class="input w-full" type="text" placeholder="Description (optional)" bind:value={local.description} />
  <div class="flex items-center gap-2">
    <label>Color:</label>
    <input type="color" bind:value={local.color} />
  </div>
  <button class="btn bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700" type="submit">Save</button>
</form>

<style>
.input { @apply border p-2 rounded; }
</style>
