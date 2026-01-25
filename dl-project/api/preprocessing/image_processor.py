import torch
from torchvision import transforms
from PIL import Image
import io
from typing import Tuple


class ImagePreprocessor:

    def __init__(self, image_size: int = 224):
        self.image_size = image_size
        self.transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def preprocess(self, image_bytes: bytes) -> Tuple[torch.Tensor, Image.Image]:
        try:
            image = Image.open(io.BytesIO(image_bytes))

            if image.mode != 'RGB':
                image = image.convert('RGB')

            image_tensor = self.transform(image).unsqueeze(0)

            return image_tensor, image

        except Exception as e:
            raise ValueError(f"Invalid image format: {str(e)}")

    def preprocess_from_path(self, image_path: str) -> Tuple[torch.Tensor, Image.Image]:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        return self.preprocess(image_bytes)