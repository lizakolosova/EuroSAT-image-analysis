import React, { useRef } from 'react';
import { Upload, Image as ImageIcon, Satellite, Loader2, X } from 'lucide-react';
import { ErrorMessage } from './ErrorMessage';

interface ImageUploadProps {
  preview: string | null;
  error: string | null;
  loading: boolean;
  onUpload: (file: File) => void;
  onClassify?: () => void;
  onReset: () => void;
  showClassifyButton: boolean;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  preview,
  error,
  loading,
  onUpload,
  onClassify,
  onReset,
  showClassifyButton,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <section className="bg-white rounded-2xl shadow-xl p-6 sm:p-8">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
        <Upload className="w-6 h-6 mr-2 text-indigo-600" aria-hidden="true" />
        Upload Image
      </h2>

      {!preview ? (
        <div
          onClick={() => fileInputRef.current?.click()}
          onKeyDown={(e) => e.key === 'Enter' && fileInputRef.current?.click()}
          role="button"
          tabIndex={0}
          className="border-3 border-dashed border-indigo-300 rounded-xl p-12 text-center cursor-pointer hover:border-indigo-500 hover:bg-indigo-50 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          aria-label="Upload satellite image"
        >
          <ImageIcon className="w-16 h-16 text-indigo-400 mx-auto mb-4" aria-hidden="true" />
          <p className="text-gray-600 mb-2 font-medium">Click to upload satellite image</p>
          <p className="text-sm text-gray-400">PNG, JPG, TIFF up to 10MB</p>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="hidden"
            aria-label="File upload"
          />
        </div>
      ) : (
        <div className="relative">
          <img
            src={preview}
            alt="Uploaded satellite imagery preview"
            className="w-full rounded-xl shadow-lg"
          />
          <button
            onClick={onReset}
            className="absolute top-3 right-3 bg-red-500 hover:bg-red-600 text-white rounded-full p-2 shadow-lg transition-colors focus:outline-none focus:ring-2 focus:ring-red-500"
            aria-label="Remove image"
          >
            <X className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>
      )}

      {error && <ErrorMessage message={error} />}

      {showClassifyButton && onClassify && (
        <button
          onClick={onClassify}
          disabled={loading}
          className="w-full mt-6 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed text-white font-semibold py-4 rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          aria-label={loading ? 'Analyzing image' : 'Classify image'}
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" aria-hidden="true" />
              Analyzing...
            </>
          ) : (
            <>
              <Satellite className="w-5 h-5 mr-2" aria-hidden="true" />
              Classify Image
            </>
          )}
        </button>
      )}
    </section>
  );
};