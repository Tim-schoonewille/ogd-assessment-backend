import { fail } from '@sveltejs/kit';
import type { Actions } from '../$types';
import { page } from '$app/stores';

export const actions = {
	default: async ({ request }) => {
		const formdata = await request.formData();
		const username = formdata.get('username');
		const password = formdata.get('password');

		if (!username) {
			return fail(400, { success: false, missing: 'username' });
		}

		if (!password) {
			return fail(400, { success: false, missing: 'password', username });
		}
		console.log('hitting success return now...');
		return { success: true, username, password, content: 'rofl' };
	}
};
