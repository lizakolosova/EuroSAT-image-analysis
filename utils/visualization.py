import matplotlib.pyplot as plt
import numpy as np
import torch
from grad_cam import GradCAM
from grad_cam.utils import visualize_cam


def plot_training_curves(history_dict, title='Training History'):
    """
    Plot training and validation curves

    Args:
        history_dict: Dictionary with 'train_loss', 'train_acc', 'val_loss', 'val_acc'
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    epochs = range(1, len(history_dict['train_loss']) + 1)

    # Loss plot
    ax1.plot(epochs, history_dict['train_loss'], 'b-', label='Train Loss', linewidth=2)
    ax1.plot(epochs, history_dict['val_loss'], 'r-', label='Val Loss', linewidth=2)
    ax1.set_title('Loss Over Epochs', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Accuracy plot
    ax2.plot(epochs, history_dict['train_acc'], 'b-', label='Train Acc', linewidth=2)
    ax2.plot(epochs, history_dict['val_acc'], 'r-', label='Val Acc', linewidth=2)
    ax2.set_title('Accuracy Over Epochs', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.suptitle(title, fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig


def compare_models(histories, model_names, metric='val_acc'):
    """
    Compare multiple models

    Args:
        histories: List of history dictionaries
        model_names: List of model names
        metric: 'val_acc' or 'val_loss'
    """
    plt.figure(figsize=(12, 6))

    for history, name in zip(histories, model_names):
        epochs = range(1, len(history[metric]) + 1)
        plt.plot(epochs, history[metric], marker='o', label=name, linewidth=2)

    plt.title(f'Model Comparison: {metric.replace("_", " ").title()}',
              fontsize=14, fontweight='bold')
    plt.xlabel('Epoch')
    plt.ylabel(metric.replace('_', ' ').title())
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return plt.gcf()


def denormalize_image(tensor, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
    """
    Denormalize image tensor for visualization
    """
    tensor = tensor.clone()
    for t, m, s in zip(tensor, mean, std):
        t.mul_(s).add_(m)
    return torch.clamp(tensor, 0, 1)


def visualize_gradcam(model, image, true_label, pred_label, class_names,
                      target_layer, device):
    """
    Visualize Grad-CAM for a single image

    Args:
        model: PyTorch model
        image: Input image tensor (C, H, W)
        true_label: True class index
        pred_label: Predicted class index
        class_names: List of class names
        target_layer: Layer to visualize (e.g., model.layer4[-1])
        device: cuda or cpu

    Returns:
        fig: Matplotlib figure
    """
    model.eval()

    # Prepare image
    img_input = image.unsqueeze(0).to(device)

    # Generate Grad-CAM
    grad_cam = GradCAM(model, target_layer)
    mask, _ = grad_cam(img_input, class_idx=pred_label)

    # Convert image for visualization
    img_show = denormalize_image(image).permute(1, 2, 0).numpy()

    # Create heatmap
    heatmap, cam_result = visualize_cam(mask, img_show)

    # Plot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Original image
    axes[0].imshow(img_show)
    axes[0].set_title('Original Image', fontsize=12, fontweight='bold')
    axes[0].axis('off')

    # Heatmap
    axes[1].imshow(heatmap)
    axes[1].set_title('Grad-CAM Heatmap', fontsize=12, fontweight='bold')
    axes[1].axis('off')

    # Overlay
    axes[2].imshow(cam_result)
    axes[2].set_title('Grad-CAM Overlay', fontsize=12, fontweight='bold')
    axes[2].axis('off')

    # Add labels
    fig.suptitle(
        f'True: {class_names[true_label]} | Predicted: {class_names[pred_label]}',
        fontsize=14, fontweight='bold', color='green' if true_label == pred_label else 'red'
    )

    plt.tight_layout()
    return fig


def plot_sample_images(dataloader, class_names, num_samples=9):
    """
    Plot sample images from dataset
    """
    images, labels = next(iter(dataloader))

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    axes = axes.ravel()

    for i in range(min(num_samples, len(images))):
        img = denormalize_image(images[i]).permute(1, 2, 0).numpy()
        axes[i].imshow(img)
        axes[i].set_title(f'Class: {class_names[labels[i]]}', fontsize=10)
        axes[i].axis('off')

    plt.tight_layout()
    return fig