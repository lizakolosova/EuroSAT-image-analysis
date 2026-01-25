import type {ClassInfo} from '../types';

export const CLASS_INFO: Record<number, ClassInfo> = {
  0: { name: 'Annual Crop', color: '#f59e0b', description: 'Agricultural land with yearly harvests' },
  1: { name: 'Forest', color: '#10b981', description: 'Dense tree-covered areas' },
  2: { name: 'Herbaceous Vegetation', color: '#84cc16', description: 'Grasslands and meadows' },
  3: { name: 'Highway', color: '#6b7280', description: 'Major roads and highways' },
  4: { name: 'Industrial', color: '#8b5cf6', description: 'Factories and industrial zones' },
  5: { name: 'Pasture', color: '#a3e635', description: 'Grazing land for livestock' },
  6: { name: 'Permanent Crop', color: '#f97316', description: 'Orchards and vineyards' },
  7: { name: 'Residential', color: '#ef4444', description: 'Housing and urban areas' },
  8: { name: 'River', color: '#3b82f6', description: 'Rivers and waterways' },
  9: { name: 'Sea/Lake', color: '#0ea5e9', description: 'Large water bodies' }
} as const;

export const MAX_FILE_SIZE = 10 * 1024 * 1024;
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';