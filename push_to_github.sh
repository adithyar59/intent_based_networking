#!/usr/bin/env bash
# Script to prepare and push project to GitHub

set -e

echo "🚀 Preparing Intent-Based Networking project for GitHub..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please run:"
    echo "   sudo apt install git"
    exit 1
fi

# Initialize git repo if not already initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "ℹ️  Git repository already initialized"
fi

# Configure git user if not configured
if ! git config user.name &> /dev/null; then
    echo "⚠️  Git user.name not set. You'll need to configure:"
    echo "   git config --global user.name 'Your Name'"
    echo "   git config --global user.email 'your.email@example.com'"
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Show status
echo ""
echo "📊 Files staged for commit:"
git status --short

# Commit
echo ""
echo "💾 Creating commit..."
git commit -m "Initial commit: Intent-Based Networking for Campus LAN

- Complete IBN automation pipeline (YANG, NETCONF, Prometheus)
- Intent parser (JSON → YANG XML)
- NETCONF push with auto-fallback simulation
- Prometheus verification script
- Mock NETCONF server and connectivity test tools
- Automated setup script
- Comprehensive documentation"

echo ""
echo "✅ Project committed to local repository!"
echo ""
echo "📤 Next steps to push to GitHub:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Name it: intent_based_networking"
echo "   - DON'T initialize with README, .gitignore, or license"
echo ""
echo "2. Add GitHub remote and push:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/intent_based_networking.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "   OR if using SSH:"
echo "   git remote add origin git@github.com:YOUR_USERNAME/intent_based_networking.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

