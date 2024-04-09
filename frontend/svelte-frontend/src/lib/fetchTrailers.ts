import type { CompactMovieData, MovieDataWithTrailer } from './types';

export async function fetchCompactMovieData(title: string): Promise<CompactMovieData[]> {
	try {
		const response = await fetch(
			`http://localhost:8000/api/v2/trailer/search?title=${title}&networK_lag=0`,
			{
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Cache-Control': 'public'
				}
			}
		);
		if (response.ok) {
			const responseData = await response.json();
			return responseData;
		} else {
			throw new Error('Movie not found.');
		}
	} catch (e) {
		throw e;
	}
}

export async function fetchTrailer(imdbID: string): Promise<MovieDataWithTrailer> {
	try {
		const response = await fetch(
			`http://localhost:8000/api/v2/trailer/search/${imdbID}?network_lag=0.01`,
			{
				method: 'GET',
				headers: {
					'Content-Type': 'application/json'
				}
			}
		);

		if (response.ok) {
			const resData = await response.json();
			return resData;
		} else {
			throw new Error('Couldnt find trailer.');
		}
	} catch (e) {
		throw e;
	}
}
