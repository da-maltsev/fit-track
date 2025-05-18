<script lang="ts">
    import { api } from '$lib/api';
    import { auth } from '$lib/stores/auth';
    import { onMount } from 'svelte';
    import type { TrainingRead } from '$lib/types';

    let trainings: TrainingRead[] = [];
    let loading = true;
    let error = '';

    async function loadTrainings() {
        try {
            loading = true;
            error = '';
            trainings = await api.listTrainings();
        } catch (e) {
            error = 'Failed to load trainings';
        } finally {
            loading = false;
        }
    }

    onMount(loadTrainings);
</script>

<div class="space-y-6">
    <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold">My Trainings</h1>
        <a
            href="/trainings/new"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
            New Training
        </a>
    </div>

    {#if error}
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
        </div>
    {/if}

    {#if loading}
        <div class="text-center py-4">Loading...</div>
    {:else if trainings.length === 0}
        <div class="text-center py-4 text-gray-500">
            No trainings yet. Create your first training!
        </div>
    {:else}
        <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {#each trainings as training}
                <div class="bg-white rounded-lg shadow p-4">
                    <div class="flex justify-between items-start mb-4">
                        <h2 class="text-lg font-semibold">
                            {new Date(training.date).toLocaleDateString()}
                        </h2>
                        <div class="space-x-2">
                            <a
                                href="/trainings/{training.id}/edit"
                                class="text-blue-500 hover:text-blue-600"
                            >
                                Edit
                            </a>
                            <button
                                on:click={async () => {
                                    if (confirm('Are you sure you want to delete this training?')) {
                                        try {
                                            await api.deleteTraining(training.id);
                                            trainings = trainings.filter((t) => t.id !== training.id);
                                        } catch (e) {
                                            error = 'Failed to delete training';
                                        }
                                    }
                                }}
                                class="text-red-500 hover:text-red-600"
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                    <div class="space-y-2">
                        {#each training.exercises as exercise}
                            <div class="border-t pt-2">
                                <div class="font-medium">{exercise.exercise.name}</div>
                                <div class="text-sm text-gray-600">
                                    {exercise.sets} sets × {exercise.reps} reps @ {exercise.weight}kg
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>
