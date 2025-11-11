#!/bin/bash

# GitHub部署脚本
# 使用方法: ./deploy_to_github.sh

echo "🚀 准备部署到GitHub..."

# 检查是否已初始化git
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
fi

# 添加所有必要文件
echo "📝 添加文件到Git..."
git add 4_streamlit_app.py
git add requirements.txt
git add README.md
git add STREAMLIT_README.md
git add DEPLOYMENT_GUIDE.md
git add .gitignore
git add .streamlit/
git add data/
git add Dockerfile
git add Procfile
git add setup.sh

# 可选：添加其他文档文件
git add *.md 2>/dev/null || true

echo ""
echo "📋 准备提交的文件："
git status --short

echo ""
read -p "是否继续提交？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 1
fi

# 提交
echo "💾 提交更改..."
git commit -m "Initial commit: Xue Baochai social network analysis Streamlit app"

echo ""
echo "✅ 提交完成！"
echo ""
echo "📤 下一步："
echo "1. 在GitHub上创建仓库（如果还没有）"
echo "2. 运行以下命令添加远程仓库并推送："
echo ""
echo "   git remote add origin https://github.com/你的用户名/你的仓库名.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "或者如果远程仓库已存在，运行："
echo "   git remote set-url origin https://github.com/你的用户名/你的仓库名.git"
echo "   git push -u origin main"



