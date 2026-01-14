"""
FastAPI application for skin lesion classification inference.
Serves the trained ResNet model and provides REST API endpoints.
"""
import os
import sys
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
from PIL import Image
import io

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from api.utils import preprocess_image, format_prediction
from model.model import load_checkpoint

# Configuration
MODEL_PATH = "models/resnet50_best.pt"
MODEL_NAME = "resnet50"
NUM_CLASSES = 7
CLASS_NAMES = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]
CLASS_DESCRIPTIONS = {
    "akiec": "Actinic keratoses - Precancerous skin lesion",
    "bcc": "Basal cell carcinoma - Most common skin cancer",
    "bkl": "Benign keratosis-like lesions - Non-cancerous growth",
    "df": "Dermatofibroma - Benign skin nodule",
    "mel": "Melanoma - Serious form of skin cancer",
    "nv": "Melanocytic nevi - Common moles",
    "vasc": "Vascular lesions - Blood vessel abnormalities"
}

# Initialize FastAPI app
app = FastAPI(
    title="Skin Lesion Classifier API",
    description="AI-powered skin lesion classification using ResNet",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variable
model = None
device = None


@app.on_event("startup")
async def load_model():
    """Load the trained model on application startup."""
    global model, device
    
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading model from {MODEL_PATH} on {device}...")
        
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
        model = load_checkpoint(
            path=MODEL_PATH,
            model_name=MODEL_NAME,
            num_classes=NUM_CLASSES,
            device=device
        )
        print(f"✅ Model loaded successfully on {device}")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Skin Lesion Classifier API",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Upload image for classification",
            "/health": "GET - Health check",
            "/classes": "GET - Get supported classes"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "device": device,
        "num_classes": NUM_CLASSES
    }


@app.get("/classes")
async def get_classes() -> Dict[str, List[Dict[str, str]]]:
    """Get list of supported skin lesion classes."""
    classes_info = [
        {
            "code": code,
            "description": CLASS_DESCRIPTIONS.get(code, "")
        }
        for code in CLASS_NAMES
    ]
    return {"classes": classes_info}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict skin lesion type from uploaded image.
    
    Args:
        file: Uploaded image file (JPEG, PNG, etc.)
    
    Returns:
        JSON with predicted class, confidence, and all class probabilities
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Please upload an image."
        )
    
    try:
        # Read and preprocess image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Preprocess for model
        input_tensor = preprocess_image(image, device)
        
        # Run inference with TTA (Test Time Augmentation)
        with torch.no_grad():
            # input_tensor is now (5, 3, 224, 224)
            logits = model(input_tensor)
            # Calculate probabilities for each augmentation
            probs_batch = torch.softmax(logits, dim=1)
            # Average probabilities across all augmentations
            avg_probs = torch.mean(probs_batch, dim=0)
            
        # Format response
        result = format_prediction(
            probabilities=avg_probs.cpu().numpy(),
            class_names=CLASS_NAMES,
            class_descriptions=CLASS_DESCRIPTIONS
        )
        
        # Check confidence threshold for OOD (Out of Distribution) detection
        confidence_threshold = 0.25
        max_conf = float(torch.max(avg_probs))
        
        if max_conf < confidence_threshold:
            result["prediction"] = {
                "class": "UNKNOWN",
                "description": "Uncertain / Potential Non-Skin Image",
                "confidence": max_conf,
                "percentage": f"{max_conf * 100:.2f}%"
            }
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
