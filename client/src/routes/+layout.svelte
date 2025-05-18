<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { onMount } from 'svelte';
	import '../app.css';

	onMount(() => {
		auth.checkAuth();
	});
</script>

<div class="min-h-screen bg-gray-100">
	<nav class="bg-white shadow-lg">
		<div class="max-w-7xl mx-auto px-4">
			<div class="flex justify-between h-16">
				<div class="flex">
					<a href="/" class="flex items-center">
						<span class="text-xl font-bold">Fitness Tracker</span>
					</a>
				</div>
				<div class="flex items-center">
					{#if $auth}
						<span class="mr-4">Welcome, {$auth.username}</span>
						<button
							on:click={() => auth.logout()}
							class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
						>
							Logout
						</button>
					{:else}
						<a
							href="/login"
							class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded mr-2"
						>
							Login
						</a>
						<a
							href="/register"
							class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
						>
							Register
						</a>
					{/if}
				</div>
			</div>
		</div>
	</nav>

	<main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
		<slot />
	</main>
</div>
