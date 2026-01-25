import React from 'react';
import { CLASS_INFO } from '../constants/classes';

export const ClassReference: React.FC = () => {
  return (
    <section className="mt-8 bg-white rounded-2xl shadow-xl p-6 sm:p-8">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Land Use Classes</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
        {Object.entries(CLASS_INFO).map(([id, info]) => (
          <div
            key={id}
            className="flex items-center p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
          >
            <div
              className="w-4 h-4 rounded-full mr-3 flex-shrink-0"
              style={{ backgroundColor: info.color }}
              aria-hidden="true"
            />
            <span className="text-sm font-medium text-gray-700">{info.name}</span>
          </div>
        ))}
      </div>
    </section>
  );
};