#!/bin/bash
# 清理不需要的文件

echo "=========================================="
echo "开始清理文件夹..."
echo "=========================================="

cd /Users/kkrois/Desktop/HongLouMeng

# 1. 删除旧的10-20章分析结果
echo ""
echo "1. 删除旧的10-20章分析结果..."
rm -rf data/results
echo "   ✓ 已删除 data/results/"

# 2. 删除旧的清理文本（10-20章）
echo ""
echo "2. 删除旧的清理文本（10-20章）..."
rm -rf data/cleaned_texts
echo "   ✓ 已删除 data/cleaned_texts/"

# 3. 删除旧的互动数据
echo ""
echo "3. 删除旧的互动数据..."
rm -f data/interactions.csv
rm -f data/interactions_detailed.json
echo "   ✓ 已删除 data/interactions.csv"
echo "   ✓ 已删除 data/interactions_detailed.json"

# 4. 删除旧的人物词典（非v2版本）
echo ""
echo "4. 删除旧的人物词典..."
rm -f data/character_dictionary.json
rm -f data/character_dictionary.csv
rm -f data/character_mapping.json
echo "   ✓ 已删除旧的人物词典文件"

# 5. 删除旧的Python脚本（v1版本）
echo ""
echo "5. 删除旧的Python脚本（v1版本）..."
rm -f 1_data_preparation.py
rm -f 2_interaction_extraction.py
rm -f 3_network_analysis.py
echo "   ✓ 已删除旧的Python脚本"

# 6. 重命名v2文件为标准名称（可选）
echo ""
echo "6. 重命名v2文件为标准名称..."
if [ -f "data/interactions_v2.csv" ]; then
    mv data/interactions_v2.csv data/interactions.csv
    echo "   ✓ 已重命名 interactions_v2.csv -> interactions.csv"
fi

if [ -f "data/interactions_detailed_v2.json" ]; then
    mv data/interactions_detailed_v2.json data/interactions_detailed.json
    echo "   ✓ 已重命名 interactions_detailed_v2.json -> interactions_detailed.json"
fi

if [ -f "data/character_dictionary_v2.json" ]; then
    mv data/character_dictionary_v2.json data/character_dictionary.json
    echo "   ✓ 已重命名 character_dictionary_v2.json -> character_dictionary.json"
fi

if [ -f "data/character_dictionary_v2.csv" ]; then
    mv data/character_dictionary_v2.csv data/character_dictionary.csv
    echo "   ✓ 已重命名 character_dictionary_v2.csv -> character_dictionary.csv"
fi

if [ -f "data/character_mapping_v2.json" ]; then
    mv data/character_mapping_v2.json data/character_mapping.json
    echo "   ✓ 已重命名 character_mapping_v2.json -> character_mapping.json"
fi

if [ -d "data/cleaned_texts_v2" ]; then
    mv data/cleaned_texts_v2 data/cleaned_texts
    echo "   ✓ 已重命名 cleaned_texts_v2/ -> cleaned_texts/"
fi

if [ -d "data/results_v2" ]; then
    mv data/results_v2 data/results
    echo "   ✓ 已重命名 results_v2/ -> results/"
fi

# 7. 重命名Python脚本（v2版本）
echo ""
echo "7. 重命名Python脚本..."
if [ -f "1_data_preparation_v2.py" ]; then
    mv 1_data_preparation_v2.py 1_data_preparation.py
    echo "   ✓ 已重命名 1_data_preparation_v2.py -> 1_data_preparation.py"
fi

if [ -f "2_interaction_extraction_v2.py" ]; then
    mv 2_interaction_extraction_v2.py 2_interaction_extraction.py
    echo "   ✓ 已重命名 2_interaction_extraction_v2.py -> 2_interaction_extraction.py"
fi

if [ -f "3_network_analysis_v2.py" ]; then
    mv 3_network_analysis_v2.py 3_network_analysis.py
    echo "   ✓ 已重命名 3_network_analysis_v2.py -> 3_network_analysis.py"
fi

echo ""
echo "=========================================="
echo "清理完成！"
echo "=========================================="
echo ""
echo "保留的文件："
echo "  - 源代码脚本（重命名后的标准版本）"
echo "  - 最终分析结果（data/results/）"
echo "  - 清理后的文本（data/cleaned_texts/）"
echo "  - 最新的数据文件"
echo "  - 文档文件"
echo "  - 原始章节文件（Chapter 10- 20/）"
echo ""

