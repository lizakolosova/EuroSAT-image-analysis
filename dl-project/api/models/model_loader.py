
import torch
import torch.nn as nn
from torchvision import models
from pathlib import Path
import traceback

class ModelLoader:

    def __init__(self, model_path: str, device: str, num_classes: int, logger=None):
        self.model_path = Path(model_path)
        self.device = device
        self.num_classes = num_classes
        self.logger = logger
        self.model = None

    def _log(self, message: str, level: str = 'info'):
        if self.logger:
            getattr(self.logger, level)(message)
        else:
            print(f"[{level.upper()}] {message}")

    def load_resnet50(self) -> nn.Module:
        model = models.resnet50(weights=None)
        model.fc = nn.Linear(model.fc.in_features, self.num_classes)
        return model

    def load_efficientnet_b0(self) -> nn.Module:
        from torchvision.models import efficientnet_b0
        model = efficientnet_b0(weights=None)
        num_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(num_features, self.num_classes)
        return model

    def load_model(self, architecture: str = 'resnet50') -> nn.Module:
        try:
            self._log(f"Loading {architecture} from {self.model_path}")

            if architecture == 'resnet50':
                model = self.load_resnet50()
            elif architecture == 'efficientnet_b0':
                model = self.load_efficientnet_b0()
            else:
                raise ValueError(f"Unsupported architecture: {architecture}")

            if not self.model_path.exists():
                raise FileNotFoundError(f"Model not found at {self.model_path}")

            checkpoint = torch.load(self.model_path, map_location=self.device)

            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
                self._log(f"Loaded checkpoint from epoch {checkpoint.get('epoch', 'unknown')}")
                if 'val_acc' in checkpoint:
                    self._log(f"Validation accuracy: {checkpoint['val_acc']:.4f}")
            else:
                model.load_state_dict(checkpoint)
                self._log("Loaded model weights")

            model = model.to(self.device)
            model.eval()

            self._log(f"Model loaded successfully on {self.device}")
            self.model = model
            return model

        except Exception as e:
            self._log(f"Error loading model: {str(e)}", 'error')
            self._log(traceback.format_exc(), 'error')
            raise
