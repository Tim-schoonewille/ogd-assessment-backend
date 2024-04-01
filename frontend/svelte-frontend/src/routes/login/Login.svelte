<script lang="ts">
	import { enhance, applyAction } from '$app/forms';
	import { page } from '$app/stores';
	//export let form;

	console.log('page: ', $page);
	let loading = false;
</script>

<div class="w-full max-w-xs">
	content: {$page.form?.content ? $page.form.content : ''}
	<form
		class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4"
		method="POST"
		use:enhance={({ formElement, formData, action, cancel, submitter }) => {
			console.log('form data:', formData);
			console.log('actioN: ', action);
			loading = true;

			return async ({ result, update }) => {
				console.log('result: ', result);
				console.log('update: ', update);

				loading = false;
				await applyAction(result);

				await update({ invalidateAll: true });
			};
		}}
	>
		<div class="mb-4">
			<label class="block text-gray-700 text-sm font-bold mb-2" for="username"> Username </label>
			<input
				class="mb-3 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
				id="username"
				name="username"
				type="text"
				placeholder="Username"
			/>
			{#if $page.form?.success === false && $page.form?.missing === 'username'}
				<p class="text-red-500 text-xs italic">Please provide a username.</p>
			{/if}
		</div>
		<div class="mb-6">
			<label class="block text-gray-700 text-sm font-bold mb-2" for="password"> Password </label>
			<input
				class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
				id="password"
				name="password"
				type="password"
				placeholder="******************"
			/>
			{#if $page.form?.success === false && $page.form?.missing === 'password'}
				<p class="text-red-500 text-xs italic">Please provide a password.</p>
			{/if}
		</div>
		<div class="flex items-center justify-between">
			<button
				class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
				type="submit"
			>
				Sign In
			</button>
			<a
				class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
				href="#"
			>
				Forgot Password?
			</a>
		</div>
		{#if $page.form?.success}
			<p class="text-green-500 mt-4 text-center text-2xl">Login Success!!!.</p>
		{/if}
		{#if loading}
			<p class="text-2xl mt-4 text-center">LOADING.....</p>
		{/if}
	</form>
	<p class="text-center text-gray-500 text-xs">&copy;2020 Acme Corp. All rights reserved.</p>
</div>
