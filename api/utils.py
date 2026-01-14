"""
Utility functions for the FastAPI application.
Handles image preprocessing and prediction formatting.
"""
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from typing import Dict, List


def get_transform():
    """
    Get the base image transformation pipeline for inference.
    """
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def preprocess_image(image: Image.Image, device: str = "cpu") -> torch.Tensor:
    """
    Preprocess a PIL Image for model inference with Test Time Augmentation (TTA).
    Generates 5 versions of the image:
    1. Original
    2. Horizontal Flip
    3. Vertical Flip
    4. Rotate 90 degrees
    5. Rotate -90 degrees
    
    Args:
        image: PIL Image object (RGB)
        device: Device to put tensor on ('cpu' or 'cuda')
    
    Returns:
        Batch of preprocessed images (5, 3, 224, 224)
    """
    transform = get_transform()
    
    # Generate augmentations
    images = [
        image,                                  # Original
        image.transpose(Image.FLIP_LEFT_RIGHT), # Horizontal Flip
        image.transpose(Image.FLIP_TOP_BOTTOM), # Vertical Flip
        image.rotate(90),                       # Rotate 90
        image.rotate(-90)                       # Rotate -90
    ]
    
    # Transform and stack
    tensors = [transform(img) for img in images]
    batch_tensor = torch.stack(tensors)
    
    return batch_tensor.to(device)


def format_prediction(
    probabilities: np.ndarray,
    class_names: List[str],
    class_descriptions: Dict[str, str]
) -> Dict:
    """
    Format model predictions into a structured response.
    
    Args:
        probabilities: NumPy array of class probabilities
        class_names: List of class names
        class_descriptions: Dictionary mapping class names to descriptions
    
    Returns:
        Dictionary with prediction details
    """
    # Get predicted class
    predicted_idx = int(np.argmax(probabilities))
    predicted_class = class_names[predicted_idx]
    confidence = float(probabilities[predicted_idx])
    
    # Create class probabilities list
    all_probabilities = [
        {
            "class": class_name,
            "description": class_descriptions.get(class_name, ""),
            "confidence": float(prob),
            "percentage": f"{float(prob) * 100:.2f}%"
        }
        for class_name, prob in zip(class_names, probabilities)
    ]
    
    # Sort by confidence (descending)
    all_probabilities.sort(key=lambda x: x["confidence"], reverse=True)
    
    return {
        "prediction": {
            "class": predicted_class,
            "description": class_descriptions.get(predicted_class, ""),
            "confidence": confidence,
            "percentage": f"{confidence * 100:.2f}%"
        },
        "all_probabilities": all_probabilities
    }
