import { writable } from 'svelte/store';
import type { UserResponse } from '../types';
import { api } from '../api';

function createAuthStore() {
    const { subscribe, set, update } = writable<UserResponse | null>(null);

    return {
        subscribe,
        login: async (username: string, password: string) => {
            await api.login(username, password);
            const user = await api.getCurrentUser();
            set(user);
            return user;
        },
        logout: () => {
            api.setToken('');
            set(null);
        },
        checkAuth: async () => {
            try {
                const user = await api.getCurrentUser();
                set(user);
                return user;
            } catch {
                set(null);
                return null;
            }
        }
    };
}

export const auth = createAuthStore(); 