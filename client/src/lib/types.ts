export interface UserCreate {
    email: string;
    username: string;
    password: string;
}

export interface UserResponse {
    email: string;
    username: string;
    id: number;
}

export interface Token {
    access_token: string;
    token_type: string;
}

export interface ExerciseDetail {
    id: number;
    name: string;
    description: string;
    aliases: string[];
    muscle_group: MuscleGroupBase;
}

export interface ExerciseList {
    id: number;
    name: string;
    description: string;
    aliases: string[];
    muscle_group: MuscleGroupBase;
}

export interface MuscleGroupBase {
    id: number;
    name: string;
}

export interface TrainingExerciseCreate {
    exercise_id: number;
    sets: number;
    reps: number;
    weight: number;
}

export interface TrainingExerciseRead extends TrainingExerciseCreate {
    id: number;
    training_id: number;
    exercise: ExerciseInfo;
}

export interface ExerciseInfo {
    name: string;
    muscle_group: string;
}

export interface TrainingCreate {
    date: string;
    exercises: TrainingExerciseCreate[];
}

export interface TrainingRead {
    date: string;
    id: number;
    user_id: number;
    exercises: TrainingExerciseRead[];
}

export interface TrainingUpdate {
    date: string;
    exercises: TrainingExerciseCreate[];
} 