<script lang="ts">
	import type { MovieDataWithTrailer } from '$lib/types';
	import FadeIn from 'svelte-transition';
	let showTrailer = false;
	export let movie: MovieDataWithTrailer;
	function toggleTrailer(): void {
		showTrailer = !showTrailer;
	}
</script>

<FadeIn show={true} appear={true}>
	<div class="mb-4 mt-4 flex flex-col gap-5">
		<div>
			<h1 class="tracking-tighter">
				{movie.title}
				-
				<span class="text-xs">
					({movie.year})
				</span>
				<!-- <span
					class="bg-teal-100 text-gray-800 text-sm font-semibold px-1 py-0.5 rounded dark:bg-teal-200 dark:text-gray-800 ms-2"
				>
					{movie.rated}</span
				> -->
			</h1>
		</div>
		<div class="flex flex-row gap-4">
			<div class="w-1/4">
				<img src={movie.poster} alt={`Poster for ${movie.title}`} />
			</div>
			<div class="flex flex-col gap-1 text-xs w-3/4">
				<p><span class="font-bold">Genre:</span> {movie.genre}</p>
				<p><span class="font-bold">Director: </span>{movie.director}</p>
				<p><span class="font-bold">Runtime: </span>{movie.runtime}</p>
				<p><span class="font-bold">ReleasedA: </span>{movie.released}</p>
				<p><span class="font-bold">IMDb Rating: </span>{movie.imdbrating}</p>
				<button
					on:click={toggleTrailer}
					class="bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-1 rounded text-xs"
					>Show trailer.</button
				>
			</div>
		</div>
		{#if showTrailer}
			<div class="shrink-0">
				<iframe
					class="no-shrink"
					width="100%"
					height="100%"
					src={movie.trailerEmbedLink}
					title="YouTube video player"
					frameborder="0"
					allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
					referrerpolicy="strict-origin-when-cross-origin"
					allowfullscreen
				></iframe>
			</div>
		{/if}
	</div>
	<hr />
</FadeIn>
