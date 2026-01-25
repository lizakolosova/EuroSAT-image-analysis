import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

class Config:
    MODEL_PATH = str(PROJECT_ROOT / "saved_models" / "hyperparameter_tuning" / "model_lr_0.00001.pt")

    DEVICE = "cpu"
    try:
        import torch as pytorch_lib
        if pytorch_lib.cuda.is_available():
            DEVICE = "cuda"
    except Exception:
        pass

    NUM_CLASSES = 10
    MAX_IMAGE_SIZE = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}

    CLASS_NAMES = [
        "Annual Crop",
        "Forest",
        "Herbaceous Vegetation",
        "Highway",
        "Industrial",
        "Pasture",
        "Permanent Crop",
        "Residential",
        "River",
        "Sea/Lake"
    ]

    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    CORS_ORIGINS = os.getenv(
        'CORS_ORIGINS',
        'http://localhost:5176,http://localhost:3000'
    ).split(',')