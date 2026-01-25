import { useState, useCallback } from 'react';
import type {Prediction} from '../types';
import { apiService } from '../services/api';

export const useClassification = () => {
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const classify = useCallback(async (imageFile: File | null) => {
    if (!imageFile) return;

    setLoading(true);
    setError(null);

    try {
      const data = await apiService.classifyImage(imageFile);

      if (data.success) {
        setPrediction({
          class_id: data.prediction.class_id,
          confidence: data.prediction.confidence,
          all_probabilities: data.prediction.all_probabilities,
        });
      } else {
        setError(data.error || 'Classification failed');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to classify image';
      setError(errorMessage);
      console.error('Classification error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setPrediction(null);
    setError(null);
  }, []);

  return {
    prediction,
    loading,
    error,
    classify,
    reset,
  };
};
