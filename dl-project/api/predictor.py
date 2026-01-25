
import torch
import torch.nn as nn
from typing import Dict, List
import traceback

class PredictionEngine:

    def __init__(self, model: nn.Module, device: str, class_names: List[str], logger=None):
        self.model = model
        self.device = device
        self.class_names = class_names
        self.logger = logger

    def _log(self, message: str, level: str = 'info'):
        if self.logger:
            getattr(self.logger, level)(message)

    def predict(self, image_tensor: torch.Tensor, top_k: int = 5) -> Dict:
        try:
            image_tensor = image_tensor.to(self.device)

            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)

            confidence, predicted_class = torch.max(probabilities, 1)
            predicted_class = predicted_class.item()
            confidence = confidence.item()

            all_probs = probabilities[0].cpu().numpy().tolist()

            class_predictions = [
                {
                    'class_id': i,
                    'class_name': self.class_names[i],
                    'probability': prob
                }
                for i, prob in enumerate(all_probs)
            ]
            class_predictions.sort(key=lambda x: x['probability'], reverse=True)

            result = {
                'success': True,
                'prediction': {
                    'class_id': predicted_class,
                    'class_name': self.class_names[predicted_class],
                    'confidence': confidence,
                    'all_probabilities': all_probs,
                    'top_k': class_predictions[:top_k]
                }
            }

            if self.logger:
                self._log(
                    f"Prediction: {self.class_names[predicted_class]} "
                    f"({confidence:.4f})"
                )

            return result

        except Exception as e:
            if self.logger:
                self._log(f"Error during prediction: {str(e)}", 'error')
                self._log(traceback.format_exc(), 'error')
            raise

    def predict_batch(self, image_tensors: torch.Tensor, top_k: int = 5) -> List[Dict]:
        try:
            image_tensors = image_tensors.to(self.device)

            with torch.no_grad():
                outputs = self.model(image_tensors)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)

            results = []
            for i in range(probabilities.size(0)):
                probs = probabilities[i].cpu().numpy().tolist()
                predicted_class = torch.argmax(probabilities[i]).item()
                confidence = probabilities[i][predicted_class].item()

                class_predictions = [
                    {
                        'class_id': j,
                        'class_name': self.class_names[j],
                        'probability': probs[j]
                    }
                    for j in range(len(probs))
                ]
                class_predictions.sort(key=lambda x: x['probability'], reverse=True)

                results.append({
                    'success': True,
                    'prediction': {
                        'class_id': predicted_class,
                        'class_name': self.class_names[predicted_class],
                        'confidence': confidence,
                        'all_probabilities': probs,
                        'top_k': class_predictions[:top_k]
                    }
                })

            return results

        except Exception as e:
            if self.logger:
                self._log(f"Error during batch prediction: {str(e)}", 'error')
            raise
