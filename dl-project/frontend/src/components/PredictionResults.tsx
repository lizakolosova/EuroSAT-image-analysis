import React from 'react';
import { CheckCircle, Satellite } from 'lucide-react';
import type {Prediction} from '../types';
import { CLASS_INFO } from '../constants/classes';

interface PredictionResultsProps {
  prediction: Prediction | null;
  onReset: () => void;
}

export const PredictionResults: React.FC<PredictionResultsProps> = ({ prediction, onReset }) => {
  if (!prediction) {
    return (
      <section className="bg-white rounded-2xl shadow-xl p-6 sm:p-8">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
          <CheckCircle className="w-6 h-6 mr-2 text-green-600" aria-hidden="true" />
          Results
        </h2>
        <div className="flex flex-col items-center justify-center h-64 text-gray-400">
          <Satellite className="w-20 h-20 mb-4 opacity-20" aria-hidden="true" />
          <p className="text-center">Upload and classify an image to see results</p>
        </div>
      </section>
    );
  }

  const classData = CLASS_INFO[prediction.class_id];
  const sortedProbabilities = prediction.all_probabilities
    .map((p, i) => ({ p, i }))
    .sort((a, b) => b.p - a.p);

  return (
    <section className="bg-white rounded-2xl shadow-xl p-6 sm:p-8">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
        <CheckCircle className="w-6 h-6 mr-2 text-green-600" aria-hidden="true" />
        Results
      </h2>

      <div className="space-y-6">
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-6 border-2 border-indigo-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-600">Predicted Class</span>
            <span className="text-sm font-bold text-indigo-600" aria-label={`Confidence: ${(prediction.confidence * 100).toFixed(1)}%`}>
              {(prediction.confidence * 100).toFixed(1)}%
            </span>
          </div>
          <h3 className="text-3xl font-bold text-gray-900 mb-2">
            {classData.name}
          </h3>
          <p className="text-gray-600">
            {classData.description}
          </p>
        </div>

        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Confidence</span>
            <span className="text-sm font-semibold text-gray-900">
              {(prediction.confidence * 100).toFixed(2)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden" role="progressbar" aria-valuenow={prediction.confidence * 100} aria-valuemin={0} aria-valuemax={100}>
            <div
              className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${prediction.confidence * 100}%` }}
            />
          </div>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Top 3 Predictions</h4>
          <div className="space-y-3">
            {sortedProbabilities.slice(0, 3).map(({ p: prob, i: classId }, idx) => (
              <div key={idx} className="flex items-center">
                <div
                  className="w-3 h-3 rounded-full mr-3"
                  style={{ backgroundColor: CLASS_INFO[classId].color }}
                  aria-hidden="true"
                />
                <div className="flex-1">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-medium text-gray-700">
                      {CLASS_INFO[classId].name}
                    </span>
                    <span className="text-xs text-gray-500">
                      {(prob * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2" role="progressbar" aria-valuenow={prob * 100} aria-valuemin={0} aria-valuemax={100}>
                    <div
                      className="h-2 rounded-full transition-all duration-700"
                      style={{
                        width: `${prob * 100}%`,
                        backgroundColor: CLASS_INFO[classId].color
                      }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={onReset}
          className="w-full mt-4 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-3 rounded-xl transition-colors focus:outline-none focus:ring-2 focus:ring-gray-400"
        >
          Classify Another Image
        </button>
      </div>
    </section>
  );
};