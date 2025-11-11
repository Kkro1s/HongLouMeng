#!/bin/bash

# 推送到GitHub脚本
# 使用方法: ./push_to_github.sh

echo "📤 准备推送到GitHub..."
echo ""
echo "请提供你的GitHub仓库URL（例如：https://github.com/username/repo-name.git）"
read -p "GitHub仓库URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ 错误：未提供仓库URL"
    exit 1
fi

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

# 设置主分支
echo "🌿 设置主分支..."
git branch -M main

# 推送
echo "📤 推送到GitHub..."
git push -u origin main

echo ""
echo "✅ 完成！"
echo "现在可以访问你的GitHub仓库查看上传的文件。"
echo "下一步：在 https://share.streamlit.io/ 部署应用！"



