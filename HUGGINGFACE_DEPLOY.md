# 🚀 Deploy to Hugging Face Spaces - Step by Step

Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`

---

## ✅ Prerequisites

1. **Hugging Face account** (free)
   - Create at: https://huggingface.co/join

2. **Git installed** on your computer
   - Check: `git --version`

3. **Git LFS installed** (for large model file)
   - Install: https://git-lfs.github.com/

---

## 📦 Step 1: Create a New Space

1. **Go to Hugging Face**: https://huggingface.co/spaces

2. **Click "Create new Space"**

3. **Fill in details**:
   - **Owner**: Your username
   - **Space name**: `skin-lesion-classifier`
   - **License**: MIT
   - **Select SDK**: **Docker** (⚠️ Important!)
   - **Space hardware**: CPU basic (free) or GPU (paid for faster inference)
   - **Visibility**: Public (or Private if you prefer)

4. **Click "Create Space"**

5. **You'll get a repository URL** like:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier
   ```

---

## 📤 Step 2: Upload Your Code

### Option A: Using Git (Recommended)

```bash
# 1. Navigate to your project
cd /home/mehrab/skin-lesion-classifier

# 2. Initialize Git LFS (for model file)
git lfs install

# 3. Track large model files with LFS
git lfs track "models/*.pt"
git add .gitattributes

# 4. Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier
# Replace YOUR_USERNAME with your actual Hugging Face username

# 5. Add all files
git add .

# 6. Commit
git commit -m "Initial deployment to Hugging Face Spaces"

# 7. Push to Hugging Face
git push hf main
# You'll be asked for credentials:
# Username: YOUR_USERNAME
# Password: YOUR_HF_TOKEN (create at https://huggingface.co/settings/tokens)
```

### Option B: Using Web Interface (Easier but slower)

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`

2. Click "Files" → "Add file" → "Upload files"

3. **Upload these files/folders**:
   - `api/` folder
   - `streamlit_app/` folder  
   - `src/` folder
   - `model/` folder
   - `models/resnet18_best.pt` (⚠️ Important!)
   - `Dockerfile`
   - `requirements.txt`
   - `config.yaml`
   - `.streamlit/config.toml`
   - `README.md`

4. Click "Commit changes to main"

---

## ⚙️ Step 3: Configure (if needed)

Your Space should automatically start building! You'll see:
- "Building..." status
- Build logs in the "Logs" tab

**Build time**: ~3-5 minutes

---

## 🎉 Step 4: Access Your App

Once building completes:

1. **Your app is live at**:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier
   ```

2. **Share this link** with anyone!

3. The app will show:
   - Your beautiful purple UI
   - Real-time predictions
   - Interactive visualizations

---

## 🔧 Troubleshooting

### Build fails?

**Check logs**:
- Go to your Space → "Logs" tab
- Look for error messages

**Common issues**:

1. **Missing model file**:
   - Ensure `models/resnet18_best.pt` is uploaded
   - Check it's tracked with Git LFS

2. **Port issues**:
   - Hugging Face Spaces uses port 7860 (already configured in our files)

3. **Memory issues**:
   - Free tier has limited RAM
   - Consider upgrading to paid GPU tier

### App is slow?

- **Free CPU tier** is slower (~3-5s per prediction)
- **Upgrade to GPU** for instant predictions:
  - Go to Space → Settings → Change Hardware
  - Select "T4 small" (~$0.60/hour, only when running)

### Model not loading?

Check that `models/resnet18_best.pt` exists and is 43MB:
```bash
ls -lh models/resnet18_best.pt
```

If using Git LFS, verify it's tracked:
```bash
git lfs ls-files
```

---

## 🔒 Authentication (Optional)

To require login before using your app:

1. Go to Space → Settings
2. Enable "Private Space" or "Space Access Control"

---

## 🎨 Customization

### Change Space appearance:

Edit the header in `README.md`:
```yaml
---
title: Your Custom Title
emoji: 🔬
colorFrom: purple
colorTo: pink
---
```

### Update after deployment:

```bash
# Make changes to your code
git add .
git commit -m "Update app"
git push hf main
```

The Space will automatically rebuild!

---

## 📊 Monitor Usage

- **View analytics**: Space → Insights
- **Check logs**: Space → Logs
- **See visitors**: Space → Analytics

---

## 💰 Costs

**Free tier**:
- ✅ Unlimited public Spaces
- ✅ CPU inference (slower)
- ✅ Community support

**Paid GPU** (optional, for faster predictions):
- T4 Small: ~$0.60/hour
- Only charged when Space is running
- Can pause/resume anytime

---

## ✨ Next Steps After Deployment

1. **Test your live app**
2. **Share the link** with friends/colleagues
3. **Monitor performance** in Space analytics
4. **Improve model** to increase accuracy
5. **Add more features** (Grad-CAM visualization, etc.)

---

## 🆘 Need Help?

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Community Forum**: https://discuss.huggingface.co/
- **Discord**: https://discord.gg/hugging-face

---

## 🎯 Quick Checklist

- [ ] Created Hugging Face account
- [ ] Created new Space (Docker SDK)
- [ ] Installed Git LFS
- [ ] Uploaded all files including model
- [ ] Space is building (check Logs)
- [ ] App is live and accessible
- [ ] Tested predictions
- [ ] Shared link with others!

---

**Your public URL**: `https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier`

Share it with the world! 🌍
