import type {ValidationResult} from '../types';
import { MAX_FILE_SIZE} from '../constants/classes';

export const validateImageFile = (file: File | null): ValidationResult => {
  if (!file) {
    return { valid: false, error: 'No file provided' };
  }

  if (!file.type.startsWith('image/')) {
    return { valid: false, error: 'Please upload a valid image file' };
  }

  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,
      error: `Image size should be less than ${MAX_FILE_SIZE / (1024 * 1024)}MB`
    };
  }

  return { valid: true, error: null };
};

