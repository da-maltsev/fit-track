import type {
    UserCreate,
    UserResponse,
    Token,
    ExerciseDetail,
    ExerciseList,
    TrainingCreate,
    TrainingRead,
    TrainingUpdate
} from './types';
import { config } from './config';

class ApiClient {
    private token: string | null = null;

    setToken(token: string) {
        this.token = token;
    }

    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const headers: HeadersInit = {
            'Content-Type': 'application/json',
            ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
            ...options.headers
        };

        const response = await fetch(`${config.apiUrl}/api/v1${endpoint}`, {
            ...options,
            headers
        });

        if (!response.ok) {
            throw new Error(`API request failed: ${response.statusText}`);
        }

        return response.json();
    }

    // User endpoints
    async createUser(user: UserCreate): Promise<UserResponse> {
        return this.request<UserResponse>('/users/', {
            method: 'POST',
            body: JSON.stringify(user)
        });
    }

    async login(username: string, password: string): Promise<Token> {
        const response = await this.request<Token>('/users/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        this.setToken(response.access_token);
        return response;
    }

    async getCurrentUser(): Promise<UserResponse> {
        return this.request<UserResponse>('/users/me');
    }

    async getUser(userId: number): Promise<UserResponse> {
        return this.request<UserResponse>(`/users/${userId}`);
    }

    // Exercise endpoints
    async getExercise(exerciseId: number): Promise<ExerciseDetail> {
        return this.request<ExerciseDetail>(`/exercises/${exerciseId}`);
    }

    async listExercises(params?: {
        search?: string;
        muscle_group?: string;
    }): Promise<ExerciseList[]> {
        const searchParams = new URLSearchParams();
        if (params?.search) searchParams.append('search', params.search);
        if (params?.muscle_group) searchParams.append('muscle_group', params.muscle_group);

        return this.request<ExerciseList[]>(`/exercises/?${searchParams.toString()}`);
    }

    // Training endpoints
    async createTraining(training: TrainingCreate): Promise<TrainingRead> {
        return this.request<TrainingRead>('/trainings/', {
            method: 'POST',
            body: JSON.stringify(training)
        });
    }

    async getTraining(trainingId: number): Promise<TrainingRead> {
        return this.request<TrainingRead>(`/trainings/${trainingId}`);
    }

    async updateTraining(trainingId: number, training: TrainingUpdate): Promise<TrainingRead> {
        return this.request<TrainingRead>(`/trainings/${trainingId}`, {
            method: 'PUT',
            body: JSON.stringify(training)
        });
    }

    async deleteTraining(trainingId: number): Promise<void> {
        await this.request(`/trainings/${trainingId}`, {
            method: 'DELETE'
        });
    }

    async listTrainings(): Promise<TrainingRead[]> {
        return this.request<TrainingRead[]>('/trainings/');
    }
}

export const api = new ApiClient(); 