# Public Deployment Guide - Skin Lesion Classifier

Get your app online so anyone can access it with a public URL!

---

## 🚀 Recommended Options (Easiest → Most Control)

### Option 1: Hugging Face Spaces (RECOMMENDED - FREE & EASY)

**Best for**: Quick deployment, ML apps, free hosting

**Pros**:
- ✅ **100% Free** 
- ✅ Beautiful public URL: `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`
- ✅ Optimized for ML/AI apps
- ✅ Can run both FastAPI + Streamlit in one Space
- ✅ No credit card required
- ✅ Automatic HTTPS

**Steps**:

1. **Create Hugging Face account**: https://huggingface.co/join

2. **Create new Space**:
   - Go to: https://huggingface.co/new-space
   - Name: `skin-lesion-classifier`
   - License: MIT
   - SDK: **Docker** (important!)
   - Click "Create Space"

3. **Prepare files** - Create these in your project:

```bash
# Create .streamlit directory for config
mkdir -p .streamlit
```

4. **Upload your code**:
   - Either use git: `git push` to the Space repository
   - Or use web interface to upload files

5. **Your app will be live at**:
   `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`

---

### Option 2: Render.com (FREE TIER)

**Best for**: Professional deployment, separate services

**Pros**:
- ✅ Free tier available
- ✅ Custom domain support
- ✅ Automatic HTTPS
- ✅ Can deploy FastAPI and Streamlit separately

**Steps**:

1. **Create account**: https://render.com/

2. **Deploy FastAPI Backend**:
   - New → Web Service
   - Connect your GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.app:app --host 0.0.0.0 --port $PORT`
   - Free tier
   - Get URL like: `https://skin-lesion-api.onrender.com`

3. **Deploy Streamlit Frontend**:
   - New → Web Service
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run streamlit_app/app.py --server.port $PORT`
   - Environment variable: `API_URL=https://skin-lesion-api.onrender.com`
   - Get URL like: `https://skin-lesion-ui.onrender.com`

**Note**: Free tier sleeps after inactivity (30s startup delay)

---

### Option 3: Streamlit Community Cloud (FREE - STREAMLIT ONLY)

**Best for**: If you want to deploy just the Streamlit UI

**Limitations**: Would need to deploy FastAPI separately or embed model in Streamlit

**Pros**:
- ✅ **100% Free forever**
- ✅ Beautiful URLs: `https://YOUR_APP.streamlit.app`
- ✅ Direct GitHub integration
- ✅ No credit card required

**Steps**:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push
   ```

2. **Deploy**:
   - Go to: https://share.streamlit.io/
   - Click "New app"
   - Select your GitHub repo
   - Main file: `streamlit_app/app.py`
   - Click "Deploy"

3. **Get URL**: `https://YOUR_USERNAME-skin-lesion-classifier.streamlit.app`

**Modification needed**: Move model inference into Streamlit (no separate FastAPI)

---

### Option 4: Railway.app (FREE $5 CREDIT/MONTH)

**Best for**: Easy deployment with good performance

**Pros**:
- ✅ $5 free credit monthly
- ✅ Fast deployment
- ✅ Good for both services

**Steps**:

1. **Create account**: https://railway.app/

2. **Deploy**:
   - New Project → Deploy from GitHub
   - Add both services (API + UI)
   - Railway auto-detects and deploys

---

## 📋 I'll Help You Deploy to Hugging Face (Recommended)

This is the **easiest and completely free** option. I'll create all the necessary files for you.

**What you'll get**:
- Public URL: `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`
- Automatic SSL (HTTPS)
- No credit card needed
- Optimized for ML apps

**Next steps**:
1. Create a Hugging Face account
2. I'll prepare all deployment files
3. You upload to Hugging Face Spaces
4. App goes live in ~2 minutes!

Would you like me to prepare the Hugging Face deployment files now?

---

## 🔒 Important Notes

**Model File**: Your `resnet18_best.pt` (43MB) needs to be uploaded:
- For Hugging Face: Use Git LFS for large files
- For other platforms: May need to upload separately or use cloud storage

**Free Tier Limitations**:
- Most free tiers have usage limits
- Apps may sleep after inactivity
- For production with high traffic, consider paid tiers

**Performance**:
- GPU inference available on Hugging Face (paid)
- Free tiers use CPU (slower predictions)
- Consider model optimization for faster CPU inference
