export interface ClassInfo {
  name: string;
  color: string;
  description: string;
}

export interface Prediction {
  class_id: number;
  confidence: number;
  all_probabilities: number[];
}

export interface ApiPredictionResponse {
  success: boolean;
  prediction: {
    class_id: number;
    class_name: string;
    confidence: number;
    all_probabilities: number[];
    top_k: Array<{
      class_id: number;
      class_name: string;
      probability: number;
    }>;
  };
  image_info?: {
    filename: string;
    size: number;
    dimensions: string;
  };
  error?: string;
}

export interface ValidationResult {
  valid: boolean;
  error: string | null;
}
