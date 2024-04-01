<script lang="ts">
	import type { MovieDataWithTrailer } from '$lib/types';
	import Header from './Header.svelte';
	import MovieCard from './MovieCard.svelte';
	import Searchbar from './Searchbar.svelte';
	import { fly, slide } from 'svelte/transition';

	import { page } from '$app/stores';
	import { loading } from '../store';

	// const queryTitle = $page.url.searchParams.get('title');
	// export let data;

	// console.log('movies from store:', $moviesWithTrailer);
	// console.log('data:', data);
</script>

<Header />
<Searchbar />

{#if $page.form?.data && !$loading}
	{#each $page.form?.data as singlemovie (singlemovie.imdbid)}
		<MovieCard movie={singlemovie} />
	{/each}
{/if}

<!-- {#each $moviesWithTrailer as singlemovie (singlemovie.imdbid)}
	<MovieCard movie={singlemovie} />
{/each} -->
