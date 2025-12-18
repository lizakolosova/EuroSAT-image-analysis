import torch
from models import SimpleCNN
from utils import train_one_epoch, plot_training_curves

# Test device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f" Device: {device}")

# Test model creation
model = SimpleCNN(num_classes=5)
print(f" Model created: {model.__class__.__name__}")

# Test dummy data
dummy_data = torch.randn(8, 3, 224, 224)
output = model(dummy_data)
print(f" Forward pass successful: {output.shape}")

# Test history plotting
history = {
    'train_loss': [0.5, 0.4, 0.3],
    'train_acc': [70, 80, 85],
    'val_loss': [0.6, 0.5, 0.4],
    'val_acc': [65, 75, 80]
}
fig = plot_training_curves(history)
print("✅ Visualization functions working")

print("\n🎉 All functions ready!")