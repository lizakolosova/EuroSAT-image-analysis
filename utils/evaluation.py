import torch
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns


def get_predictions(model, dataloader, device):
    """
    Get all predictions and true labels

    Returns:
        all_preds: Predicted labels
        all_labels: True labels
        all_probs: Prediction probabilities
    """
    model.eval()
    all_preds = []
    all_labels = []
    all_probs = []

    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            outputs = model(images)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
            all_probs.extend(probs.cpu().numpy())

    return np.array(all_preds), np.array(all_labels), np.array(all_probs)


def plot_confusion_matrix(y_true, y_pred, class_names, title='Confusion Matrix'):
    """
    Plot confusion matrix
    """
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    return plt.gcf()


def print_classification_report(y_true, y_pred, class_names):
    """
    Print detailed classification report
    """
    print("\nClassification Report:")
    print("=" * 60)
    print(classification_report(y_true, y_pred, target_names=class_names))


def get_misclassified_samples(model, dataloader, device, num_samples=10):
    """
    Get misclassified samples for error analysis

    Returns:
        misclassified: List of (image, true_label, pred_label, probs)
    """
    model.eval()
    misclassified = []

    with torch.no_grad():
        for images, labels in dataloader:
            images_gpu = images.to(device)
            outputs = model(images_gpu)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)

            # Find misclassified
            mask = preds.cpu() != labels
            if mask.any():
                for i in range(len(mask)):
                    if mask[i] and len(misclassified) < num_samples:
                        misclassified.append({
                            'image': images[i].cpu(),
                            'true_label': labels[i].item(),
                            'pred_label': preds[i].cpu().item(),
                            'probs': probs[i].cpu().numpy()
                        })

            if len(misclassified) >= num_samples:
                break

    return misclassified