#!/bin/bash

# Quick Setup Script for Hugging Face Spaces Deployment
# Run this before pushing to Hugging Face

echo "🚀 Setting up Hugging Face Spaces deployment..."
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✅ Git is installed"

# Check if Git LFS is installed
if ! command -v git-lfs &> /dev/null; then
    echo "⚠️  Git LFS is not installed."
    echo "📥 Installing Git LFS..."
    
    # Try to install based on OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install git-lfs -y
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install git-lfs
    else
        echo "❌ Please install Git LFS manually: https://git-lfs.github.com/"
        exit 1
    fi
fi

echo "✅ Git LFS is installed"

# Initialize Git LFS
echo "🔧 Initializing Git LFS..."
git lfs install

# Track model files
echo "📦 Tracking model files with LFS..."
git lfs track "models/*.pt"
git lfs track "models/*.pth"

# Add .gitattributes
git add .gitattributes

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Create a Space at: https://huggingface.co/spaces"
echo "2. Choose 'Docker' as SDK"
echo "3. Run these commands:"
echo ""
echo "   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier"
echo "   git add ."
echo "   git commit -m 'Deploy to Hugging Face Spaces'"
echo "   git push hf main"
echo ""
echo "4. Your app will be live at:"
echo "   https://huggingface.co/spaces/YOUR_USERNAME/skin-lesion-classifier"
echo ""
echo "📖 Full instructions: See HUGGINGFACE_DEPLOY.md"
