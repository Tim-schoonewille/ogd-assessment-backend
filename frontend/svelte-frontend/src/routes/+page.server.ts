import { fetchCompactMovieData, fetchTrailer } from '$lib/fetchTrailers.js';
// import data from '$lib/lotr.json';
import type { MovieDataWithTrailer } from '$lib/types';
import { fail } from '@sveltejs/kit';

// export async function load({ cookies, request }) {
// 	cookies.set('myname', 'Tim', { path: '/' });
// 	const url = new URL(request.url);
// 	const searchParams = url.searchParams;

// 	const title = searchParams.get('title');
// 	console.log(title);
// 	let outputData = [];
// 	if (title) {
// 		try {
// 			const compactMovieData = await fetchCompactMovieData(title);

// 			const trailerPromises = compactMovieData.map(async (data) => {
// 				return await fetchTrailer(data.imdbid);
// 			});
// 			const result = await Promise.all(trailerPromises);
// 			outputData = result;
// 			// return { data: result };
// 		} catch (e) {
// 			console.log(e);
// 			return;
// 		}
// 	}
// 	return { data: outputData };
// }

export const actions = {
	default: async ({ request }) => {
		const data = await request.formData();
		const movieTitle = data.get('title')?.toString();
		if (!movieTitle) return fail(400, { success: false, missing: 'title' });

		try {
			const compactMovieData = await fetchCompactMovieData(movieTitle);
			console.log('hitting this...');
			const trailerPromises = compactMovieData.map(async (data) => {
				return await fetchTrailer(data.imdbid);
			});
			const result = await Promise.all(trailerPromises);
			return {
				success: true,
				data: result
			};
		} catch (e: any) {
			console.error(e.message as string);
			return fail(400, {
				success: false,
				error: e.message as string
			});
		}
	}
};

// export const actions = {
// 	default: async ({ request }) => {
// 		const formdata = await request.formData();
// 		const title = formdata.get('title');
// 		console.log('rofl');
// 		return {
// 			success: true,
// 			foo: 'bar',
// 			title
// 		};
// 	}
// };
