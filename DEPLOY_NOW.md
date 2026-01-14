# Deploy to Hugging Face - Your Action Items

## Step-by-Step Instructions

### **Step 1: Hugging Face Account & Space** 

1. **Create account** (if you don't have one):
   - Go to: https://huggingface.co/join
   - Sign up

2. **Create a new Space**:
   - Go to: https://huggingface.co/new-space
   - **Space name**: `skin-lesion-classifier`
   - **License**: MIT
   - **SDK**: Select **"Docker"**
   - **Visibility**: Public
   - Click **"Create Space"**

3. **You'll get a URL** like:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier
   ```

---

### **Step 2: Install Git LFS** 

Git LFS is needed to upload your 43MB model file.

```bash
# Install Git LFS
sudo apt-get update
sudo apt-get install git-lfs -y

# Initialize it
git lfs install
```

---

### **Step 3: Upload Your Code** 

You have **two options** - choose what works best:

#### **Option A: Using Git** (Recommended)

```bash
cd skin-lesion-classifier

# Track large model files with LFS
git lfs track "models/*.pt"
git add .gitattributes

# Add Hugging Face remote (replace YOUR_USERNAME)
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier

# Stage all files
git add .

# Commit
git commit -m "Deploy to Hugging Face Spaces"

# Push to Hugging Face
git push hf main
```

**When prompted for credentials:**
- **Username**: Your Hugging Face username
- **Password**: Create a token at https://huggingface.co/settings/tokens
  - Click "New token"
  - Name it "deploy"
  - Role: "write"
  - Copy the token and paste when asked for password

---

#### **Option B: Web Upload** (Easier, but slower)

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`

2. Click **"Files"** → **"Add file"** → **"Upload files"**

3. **Upload these files/folders**:
   ```
   Essential files:
   Dockerfile
   README.md
   requirements.txt
   config.yaml
   .streamlit/config.toml
   
   Code folders:
   api/ (folder with app.py and utils.py)
   streamlit_app/ (folder with app.py)
   src/ (folder with all Python files)
   model/ (folder with model.py)
   
   Model file (IMPORTANT):
   models/resnet18_best.pt (43MB)
   ```

4. Click **"Commit changes to main"**

---

### **Step 4: Wait for Build** (3-5 minutes)

After uploading:
1. Hugging Face will automatically start building
2. Go to your Space page
3. You'll see **"Building..."** status
4. Click **"Logs"** tab to watch progress
5. Build takes ~3-5 minutes

---

### **Step 5: Congratulations, Your App is Live!** 

Once building completes:
- Your app is live at: `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`
- **Share this link** with anyone!
- Test it by uploading an image


## Troubleshooting

**Build fails?**
- Check that `models/resnet18_best.pt` was uploaded
- Verify you selected "Docker" SDK
- Check Logs tab for errors

**Model not found?**
- Ensure the model file is in `models/` folder
- File should be 43MB

**App is slow?**
- Free tier uses CPU (3-5s per prediction)
- Upgrade to GPU for faster inference (paid)

---

## What Happens Next

After deployment:
1. Your app has a public URL
2. Anyone can access it
3. You can see visitor analytics
4. Push updates with `git push hf main`

---

## Timeline

- Setup Git LFS: 1 min
- Upload files: 3-5 min
- Build time: 3-5 min
- **Total: ~10 minutes to live!**

---

## Tips

- **First deployment** takes longest (uploading model)
- **Updates are faster** (just code changes)
- **Monitor usage** in Space → Insights
- **Pause Space** when not in use (Settings)

---

**Ready?** Follow Step 1 above to get started! 

Your public URL will be: `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`
