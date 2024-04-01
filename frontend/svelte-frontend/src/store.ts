import { writable } from 'svelte/store';
import movieData from '$lib/lotr.json';
import type { MovieDataWithTrailer } from '$lib/types';

export const movie = writable('');
export const loading = writable(false);
