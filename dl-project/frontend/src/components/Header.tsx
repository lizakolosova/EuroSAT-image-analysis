import React from 'react';
import { Satellite, Info } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="text-center mb-8">
      <div className="flex items-center justify-center mb-4">
        <Satellite className="w-12 h-12 text-indigo-600 mr-3" aria-hidden="true" />
        <h1 className="text-4xl sm:text-5xl font-bold text-gray-900">
          EuroSAT Classifier
        </h1>
      </div>
      <p className="text-lg text-gray-600 max-w-2xl mx-auto">
        Deep learning-powered satellite image classification using transfer learning with ResNet50
      </p>
      <div className="mt-4 flex items-center justify-center gap-2 text-sm text-gray-500">
        <Info className="w-4 h-4" aria-hidden="true" />
        <span>Trained on 27,000 labeled Sentinel-2 satellite images</span>
      </div>
    </header>
  );
};