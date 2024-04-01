<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { loading, movie } from '../store';
	import Spinner from './Spinner.svelte';

	let title = '';
	let error = '';
</script>

<form
	method="POST"
	class="flex flex-col gap-2 mb-6"
	use:enhance={() => {
		error = '';
		loading.set(true);
		movie.set(title);

		return async ({ result, update }) => {
			if (result.type === 'failure') {
				error = result.data?.error;
			}
			console.log('result form use enhance:', result);
			await update();
			loading.set(false);
		};
	}}
>
	<input
		name="title"
		class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
		placeholder="Search for movie trailers..."
		bind:value={title}
	/>

	<!-- {#if !$page.form?.success && $page.form?.missing === 'title'}
		<p class="text-red-500 text-center">Please insert title</p>
	{/if} -->
	<button
		disabled={false}
		type="submit"
		class="bg-teal-500 hover:bg-teal-400 text-white font-bold py-2 px-4 border-b-4 border-teal-700 hover:border-teal-500 rounded"
	>
		Search
	</button>
	{#if $movie && $loading}
		<p class="italic text-sm mb-3 text-center tracking-tight">Searching for: {$movie}</p>
	{/if}

	{#if $loading}
		<Spinner />
	{/if}
	{#if error}
		<p>{error}</p>
	{/if}
</form>
