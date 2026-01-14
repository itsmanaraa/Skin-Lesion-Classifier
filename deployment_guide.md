# Deployment Guide for Skin Lesion Classifier

This guide provides detailed instructions for deploying the skin lesion classifier application.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Testing the Deployment](#testing-the-deployment)
5. [Troubleshooting](#troubleshooting)
6. [Cloud Deployment](#cloud-deployment)

---

## Prerequisites

### Required
- **Python 3.9+** installed
- **Trained model** at `models/resnet18_best.pt`
- **Git** (for cloning the repository)

### Optional
- **Docker** and **Docker Compose** (for containerized deployment)
- **CUDA-compatible GPU** (for faster inference, optional)

---

## Local Deployment

### Step 1: Environment Setup

1. **Clone the repository**:
   ```bash
   cd /home/mehrab/skin-lesion-classifier
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Step 2: Verify Model

Ensure the trained model exists:
```bash
ls -lh models/resnet18_best.pt
```

If the file doesn't exist, you need to train the model first:
```bash
python -m src.train
```

### Step 3: Start Services

**Terminal 1 - FastAPI Backend**:
```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
Loading model from models/resnet18_best.pt on cpu...
✅ Model loaded successfully on cpu
INFO:     Application startup complete.
```

**Terminal 2 - Streamlit UI**:
```bash
streamlit run streamlit_app/app.py
```

Expected output:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Step 4: Access the Application

- **Streamlit UI**: http://localhost:8501
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## Docker Deployment

Docker deployment packages everything (app, dependencies, environment) into a container, making it easy to deploy anywhere.

### Step 1: Install Docker

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

**Verify installation**:
```bash
docker --version
docker-compose --version
```

### Step 2: Build and Run

**Option A: Using Docker Compose (Recommended)**

Single command to build and run everything:
```bash
docker-compose up --build
```

Run in background (detached mode):
```bash
docker-compose up -d --build
```

**Option B: Using Dockerfile Directly**

Build the image:
```bash
docker build -t skin-lesion-classifier .
```

Run the container:
```bash
docker run -p 8000:8000 -p 8501:8501 skin-lesion-classifier
```

### Step 3: Access the Application

Same as local deployment:
- **Streamlit UI**: http://localhost:8501
- **FastAPI**: http://localhost:8000

### Step 4: Managing Docker Services

**Stop services**:
```bash
docker-compose down
```

**View logs**:
```bash
docker-compose logs -f
```

**Restart services**:
```bash
docker-compose restart
```

**Remove containers and images**:
```bash
docker-compose down --rmi all
```

---

## Testing the Deployment

### 1. Test FastAPI Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model": "resnet18",
  "device": "cpu",
  "num_classes": 7
}
```

### 2. Test Class Endpoint

```bash
curl http://localhost:8000/classes
```

### 3. Test Prediction

```bash
# Replace with actual image path
curl -X POST -F "file=@test_images/sample.jpg" http://localhost:8000/predict
```

Expected response:
```json
{
  "prediction": {
    "class": "nv",
    "description": "Melanocytic nevi - Common moles",
    "confidence": 0.92,
    "percentage": "92.00%"
  },
  "all_probabilities": [...]
}
```

### 4. Test Streamlit UI

1. Open browser to http://localhost:8501
2. Click on "Classify Image" tab
3. Upload a test image
4. Click "🔬 Analyze Image"
5. Verify prediction appears with confidence scores

---

## Troubleshooting

### Issue: "Model file not found"

**Error**: `FileNotFoundError: Model file not found at models/resnet18_best.pt`

**Solution**:
- Ensure model file exists: `ls models/resnet18_best.pt`
- Train model if missing: `python -m src.train`

### Issue: "Cannot connect to API"

**Error**: Streamlit shows "Cannot connect to API"

**Solution**:
1. Check if FastAPI is running: `curl http://localhost:8000/health`
2. If using Docker, ensure both containers are running: `docker-compose ps`
3. Check firewall settings

### Issue: Port already in use

**Error**: `Address already in use: 8000` or `8501`

**Solution**:
```bash
# Find process using the port
lsof -i :8000
# or
lsof -i :8501

# Kill the process
kill -9 <PID>
```

### Issue: Out of memory

**Error**: `CUDA out of memory` or system freezes

**Solution**:
- Model loads on CPU by default
- Reduce batch size if processing multiple images
- Close other applications

### Issue: Slow predictions

**Cause**: Running on CPU

**Solution**:
- Use GPU if available (automatic detection)
- For Docker: add GPU support with nvidia-docker

---

## Cloud Deployment

### AWS Deployment (EC2)

1. **Launch EC2 instance** (t2.medium or larger)
2. **Install Docker**:
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   ```
3. **Clone repository** and follow Docker deployment steps
4. **Configure security group**: Open ports 8000 and 8501
5. **Access via public IP**: `http://<EC2-PUBLIC-IP>:8501`

### Google Cloud Platform (Cloud Run)

1. **Build container**:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/skin-lesion-classifier
   ```
2. **Deploy**:
   ```bash
   gcloud run deploy --image gcr.io/PROJECT-ID/skin-lesion-classifier --platform managed
   ```

### Heroku Deployment

1. **Create Procfile**:
   ```
   web: uvicorn api.app:app --host 0.0.0.0 --port $PORT
   ```
2. **Deploy**:
   ```bash
   heroku create skin-lesion-app
   git push heroku main
   ```

---

## Performance Optimization

### For Production

1. **Use production ASGI server**:
   ```bash
   gunicorn api.app:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Enable model caching**: Already implemented in API

3. **Add Redis for caching predictions**

4. **Use CDN for static assets**

5. **Implement rate limiting**

### For Accuracy

1. **Use GPU for inference**: Automatically detected
2. **Batch predictions**: Process multiple images together
3. **Model quantization**: Reduce model size for faster loading

---

## Next Steps

- ✅ Deployment complete!
- 🔧 Monitor logs for errors
- 📊 Collect user feedback
- 🎯 Improve model accuracy
- 🚀 Add more features

For model improvement strategies, see the implementation plan.

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review logs: `docker-compose logs` or terminal output
3. Ensure all prerequisites are met
4. Verify model file exists and is valid
