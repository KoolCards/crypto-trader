#!/bin/bash

# Setup script for GitHub Actions deployment

echo "🚀 Setting up GitHub Actions for fetch_live_price"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please run:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin YOUR_GITHUB_REPO_URL"
    echo "   git push -u origin main"
    exit 1
fi

# Check if GitHub remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No GitHub remote found. Please add your GitHub repository:"
    echo "   git remote add origin YOUR_GITHUB_REPO_URL"
    exit 1
fi

echo "✅ Git repository found"

# Check if workflow file exists
if [ ! -f ".github/workflows/fetch_price.yml" ]; then
    echo "❌ GitHub Actions workflow not found"
    echo "   Please ensure .github/workflows/fetch_price.yml exists"
    exit 1
fi

echo "✅ GitHub Actions workflow found"

# Show next steps
echo ""
echo "📋 Next Steps:"
echo "1. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Add GitHub Actions workflow'"
echo "   git push"
echo ""
echo "2. Go to your GitHub repository"
echo "3. Click on the 'Actions' tab"
echo "4. Enable GitHub Actions if prompted"
echo "5. The workflow will run automatically at 9 AM UTC daily"
echo ""
echo "6. To test manually:"
echo "   - Go to Actions tab"
echo "   - Click on 'Fetch Ethereum Price' workflow"
echo "   - Click 'Run workflow' button"
echo ""
echo "7. Monitor execution:"
echo "   - Check the Actions tab for logs"
echo "   - Data will be stored as artifacts"
echo "   - Data files will be committed back to your repo"
echo ""

# Check current git status
echo "📊 Current git status:"
git status --porcelain

echo ""
echo "🎉 Setup complete! Follow the steps above to deploy to GitHub Actions." 