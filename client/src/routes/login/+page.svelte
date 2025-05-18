<script lang="ts">
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    let username = '';
    let password = '';
    let error = '';
    let loading = false;

    async function handleSubmit() {
        try {
            loading = true;
            error = '';
            await auth.login(username, password);
            goto('/');
        } catch (e) {
            error = 'Invalid username or password';
        } finally {
            loading = false;
        }
    }
</script>

<div class="min-h-[calc(100vh-4rem)] flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 class="text-2xl font-bold mb-6 text-center">Login</h1>

        {#if error}
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {error}
            </div>
        {/if}

        <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            <div>
                <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                <input
                    type="text"
                    id="username"
                    bind:value={username}
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
            </div>

            <div>
                <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                <input
                    type="password"
                    id="password"
                    bind:value={password}
                    required
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
            </div>

            <button
                type="submit"
                disabled={loading}
                class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 disabled:opacity-50"
            >
                {loading ? 'Logging in...' : 'Login'}
            </button>
        </form>

        <p class="mt-4 text-center text-sm text-gray-600">
            Don't have an account?
            <a href="/register" class="text-blue-500 hover:text-blue-600">Register here</a>
        </p>
    </div>
</div> 