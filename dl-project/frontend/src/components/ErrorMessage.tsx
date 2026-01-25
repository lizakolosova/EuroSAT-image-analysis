import React from 'react';
import { AlertCircle } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  return (
    <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start" role="alert">
      <AlertCircle className="w-5 h-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" aria-hidden="true" />
      <p className="text-red-700 text-sm">{message}</p>
    </div>
  );
};