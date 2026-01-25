import { useState, useCallback } from 'react';
import { validateImageFile } from '../utils/validation';

export const useImageUpload = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = useCallback((file: File | null) => {
    if (!file) return;

    const validation = validateImageFile(file);
    if (!validation.valid) {
      setError(validation.error);
      return;
    }

    setError(null);
    setImageFile(file);

    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  }, []);

  const reset = useCallback(() => {
    setImageFile(null);
    setPreview(null);
    setError(null);
  }, []);

  return {
    imageFile,
    preview,
    error,
    handleUpload,
    reset,
  };
};

