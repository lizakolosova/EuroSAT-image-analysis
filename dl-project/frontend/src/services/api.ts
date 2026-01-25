import type {ApiPredictionResponse} from '../types';
import { API_BASE_URL } from '../constants/classes';

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async classifyImage(imageFile: File): Promise<ApiPredictionResponse> {
    const formData = new FormData();
    formData.append('image', imageFile);

    const response = await fetch(`${this.baseUrl}/api/predict`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(errorData.error || `Request failed with status ${response.status}`);
    }

    return response.json();
  }

  async healthCheck(): Promise<{ status: string; model_loaded: boolean; device: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }
}

export const apiService = new ApiService(API_BASE_URL);