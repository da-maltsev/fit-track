<script lang="ts">
    import { api } from '$lib/api';
    import { goto } from '$app/navigation';
    import type { ExerciseList, TrainingExerciseCreate } from '$lib/types';
    import { onMount } from 'svelte';

    let exercises: ExerciseList[] = [];
    let loading = true;
    let error = '';
    let date = new Date().toISOString().split('T')[0];
    let selectedExercises: TrainingExerciseCreate[] = [];
    let searchQuery = '';
    let muscleGroup = '';

    async function loadExercises() {
        try {
            loading = true;
            error = '';
            exercises = await api.listExercises({
                search: searchQuery || undefined,
                muscle_group: muscleGroup || undefined
            });
        } catch (e) {
            error = 'Failed to load exercises';
        } finally {
            loading = false;
        }
    }

    function addExercise(exercise: ExerciseList) {
        selectedExercises = [
            ...selectedExercises,
            {
                exercise_id: exercise.id,
                sets: 3,
                reps: 10,
                weight: 0
            }
        ];
    }

    function removeExercise(index: number) {
        selectedExercises = selectedExercises.filter((_, i) => i !== index);
    }

    async function handleSubmit() {
        if (selectedExercises.length === 0) {
            error = 'Please add at least one exercise';
            return;
        }

        try {
            loading = true;
            error = '';
            await api.createTraining({
                date: new Date(date).toISOString(),
                exercises: selectedExercises
            });
            goto('/');
        } catch (e) {
            error = 'Failed to create training';
        } finally {
            loading = false;
        }
    }

    onMount(loadExercises);
</script>

<div class="max-w-4xl mx-auto space-y-6">
    <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold">New Training</h1>
        <a href="/" class="text-blue-500 hover:text-blue-600">Back to Trainings</a>
    </div>

    {#if error}
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
        </div>
    {/if}

    <form on:submit|preventDefault={handleSubmit} class="space-y-6">
        <div>
            <label for="date" class="block text-sm font-medium text-gray-700">Date</label>
            <input
                type="date"
                id="date"
                bind:value={date}
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
        </div>

        <div class="space-y-4">
            <h2 class="text-lg font-semibold">Add Exercises</h2>

            <div class="flex gap-4">
                <div class="flex-1">
                    <label for="search" class="block text-sm font-medium text-gray-700">Search</label>
                    <input
                        type="text"
                        id="search"
                        bind:value={searchQuery}
                        on:input={() => loadExercises()}
                        placeholder="Search exercises..."
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                </div>
                <div class="flex-1">
                    <label for="muscleGroup" class="block text-sm font-medium text-gray-700"
                        >Muscle Group</label
                    >
                    <input
                        type="text"
                        id="muscleGroup"
                        bind:value={muscleGroup}
                        on:input={() => loadExercises()}
                        placeholder="Filter by muscle group..."
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                </div>
            </div>

            {#if loading}
                <div class="text-center py-4">Loading exercises...</div>
            {:else if exercises.length === 0}
                <div class="text-center py-4 text-gray-500">No exercises found</div>
            {:else}
                <div class="grid gap-4 md:grid-cols-2">
                    {#each exercises as exercise}
                        <div
                            class="bg-white rounded-lg shadow p-4 cursor-pointer hover:bg-gray-50"
                            on:click={() => addExercise(exercise)}
                        >
                            <h3 class="font-medium">{exercise.name}</h3>
                            <p class="text-sm text-gray-600">{exercise.description}</p>
                            <div class="mt-2 text-sm text-gray-500">
                                Muscle Group: {exercise.muscle_group.name}
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>

        {#if selectedExercises.length > 0}
            <div class="space-y-4">
                <h2 class="text-lg font-semibold">Selected Exercises</h2>
                {#each selectedExercises as exercise, index}
                    <div class="bg-white rounded-lg shadow p-4">
                        <div class="flex justify-between items-start mb-4">
                            <h3 class="font-medium">
                                {exercises.find((e) => e.id === exercise.exercise_id)?.name}
                            </h3>
                            <button
                                type="button"
                                on:click={() => removeExercise(index)}
                                class="text-red-500 hover:text-red-600"
                            >
                                Remove
                            </button>
                        </div>
                        <div class="grid grid-cols-3 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Sets</label>
                                <input
                                    type="number"
                                    min="1"
                                    bind:value={exercise.sets}
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Reps</label>
                                <input
                                    type="number"
                                    min="1"
                                    bind:value={exercise.reps}
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                />
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Weight (kg)</label>
                                <input
                                    type="number"
                                    min="0"
                                    step="0.5"
                                    bind:value={exercise.weight}
                                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                />
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}

        <div class="flex justify-end">
            <button
                type="submit"
                disabled={loading || selectedExercises.length === 0}
                class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 disabled:opacity-50"
            >
                {loading ? 'Creating...' : 'Create Training'}
            </button>
        </div>
    </form>
</div> 