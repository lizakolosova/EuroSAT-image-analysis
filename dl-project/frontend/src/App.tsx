import React from 'react';
import { Header } from './components/Header';
import { ImageUpload } from './components/ImageUpload';
import { PredictionResults } from './components/PredictionResults';
import { ClassReference } from './components/ClassReference';
import { useImageUpload } from './hooks/useImageUpload';
import { useClassification } from './hooks/useClassification';

const App: React.FC = () => {
  const {
    imageFile,
    preview,
    error: uploadError,
    handleUpload,
    reset: resetUpload,
  } = useImageUpload();

  const {
    prediction,
    loading,
    error: classifyError,
    classify,
    reset: resetPrediction,
  } = useClassification();

  const handleClassify = () => {
    if (imageFile) {
      classify(imageFile);
    }
  };

  const handleReset = () => {
    resetUpload();
    resetPrediction();
  };

  const error = uploadError || classifyError;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4 sm:p-8">
      <div className="max-w-6xl mx-auto">
        <Header />

        <main className="grid md:grid-cols-2 gap-8">
          <ImageUpload
            preview={preview}
            error={error}
            loading={loading}
            onUpload={handleUpload}
            onClassify={!prediction ? handleClassify : undefined}
            onReset={handleReset}
            showClassifyButton={!!preview && !prediction}
          />

          <PredictionResults
            prediction={prediction}
            onReset={handleReset}
          />
        </main>

        <ClassReference />

        <footer className="mt-8 text-center text-gray-500 text-sm">
          <p>Built with PyTorch, ResNet50, and React | Deep Learning Project 2025</p>
        </footer>
      </div>
    </div>
  );
};

export default App;