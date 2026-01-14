# Skin Lesion Classifier

AI-powered skin lesion detection and classification using deep learning (ResNet18).

## About

This application uses a ResNet18 model trained on the HAM10000 dataset to classify skin lesions into 7 categories:
- **AKIEC** - Actinic Keratoses (Precancerous)
- **BCC** - Basal Cell Carcinoma (Malignant)
- **BKL** - Benign Keratosis (Benign)
- **DF** - Dermatofibroma (Benign)
- **MEL** - Melanoma (Malignant - Critical)
- **NV** - Melanocytic Nevi (Benign)
- **VASC** - Vascular Lesions (Benign)

## Features

- Beautiful futuristic purple-themed UI
- Real-time skin lesion classification
- Confidence scores with interactive visualizations
- Educational information about each lesion type
- FastAPI backend + Streamlit frontend

## Tech Stack

- **Model**: ResNet18 (Transfer Learning)
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Framework**: PyTorch
- **Dataset**: HAM10000

## Disclaimer

**This is a research and educational tool.** It should NOT be used as a substitute for professional medical diagnosis. Always consult with a qualified healthcare provider for medical concerns.

## How to Use

1. Navigate to the "CLASSIFY IMAGE" tab
2. Upload a clear image of a skin lesion
3. Click "ANALYZE IMAGE"
4. Review the prediction results and confidence scores
5. Check the "CLASS INFORMATION" tab for detailed information about each lesion type


## Development Mode

To run the application with hot-reloading enabled for development:

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start Backend (FastAPI)**
    ```bash
    uvicorn api.app:app --reload --port 8000
    ```
    The API will be available at `http://localhost:8000`.

3.  **Start Frontend (Streamlit)**
    ```bash
    streamlit run streamlit_app/app.py
    ```
    The UI will open in your browser at `http://localhost:8501`.

## Model Performance

- Training Dataset: HAM10000 (10,015 images)
- Architecture: ResNet18 with transfer learning
- Image Size: 224x224
- Classes: 7
