#!/bin/bash
# 运行完整分析流程

echo "=========================================="
echo "红楼梦人物社交网络分析 - 完整流程"
echo "=========================================="

echo ""
echo "阶段一：数据准备..."
python3 1_data_preparation.py

echo ""
echo "阶段二：互动关系识别..."
python3 2_interaction_extraction.py

echo ""
echo "阶段三：网络分析..."
python3 3_network_analysis.py

echo ""
echo "=========================================="
echo "分析完成！"
echo "=========================================="
echo ""
echo "要启动Streamlit应用，请运行："
echo "  streamlit run 4_streamlit_app.py"
echo ""

