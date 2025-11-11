#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶段二：互动关系识别（使用选中的20章）
- 自动提取薛寶釵与其他人物的互动关系
"""

import os
import re
import json
import pandas as pd
from collections import defaultdict

# 配置
OUTPUT_DIR = "data"
CLEANED_DIR = os.path.join(OUTPUT_DIR, "cleaned_texts_v2")
TARGET_CHARACTER = "薛寶釵"

def load_data():
    """加载数据"""
    # 加载人物词典
    with open(os.path.join(OUTPUT_DIR, "character_dictionary_v2.json"), 'r', encoding='utf-8') as f:
        character_dict = json.load(f)
    
    # 加载选中的章节列表
    with open(os.path.join(OUTPUT_DIR, "selected_chapters.json"), 'r', encoding='utf-8') as f:
        selection_data = json.load(f)
    selected_chapters = selection_data['selected_chapters']
    
    # 加载清理后的文本
    chapters = {}
    for chapter_num in selected_chapters:
        filename = f"ch{chapter_num:03d}_cleaned.txt"
        filepath = os.path.join(CLEANED_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                chapters[chapter_num] = f.read()
    
    return character_dict, chapters

def identify_interactions_advanced(text, target_variants, other_characters_dict, chapter_num):
    """高级互动识别：基于句子和段落"""
    interactions = []
    
    # 按句子分割
    sentences = re.split(r'[。！？\n]', text)
    
    for sentence_idx, sentence in enumerate(sentences):
        # 检查句子中是否包含薛寶釵
        has_target = any(variant in sentence for variant in target_variants)
        if not has_target:
            continue
        
        # 检查句子中是否有其他人物
        for char_name, char_variants in other_characters_dict.items():
            if char_name == TARGET_CHARACTER:
                continue
            
            has_other = any(variant in sentence for variant in char_variants)
            if has_other:
                # 确定互动类型
                interaction_type = "共同出现"
                if any(word in sentence for word in ['道', '說', '問', '答', '回', '笑', '叫', '勸', '罵']):
                    interaction_type = "对话"
                elif any(word in sentence for word in ['見', '遇', '訪', '來', '去', '送', '給', '拉', '推']):
                    interaction_type = "行为"
                
                # 获取前后句子作为上下文
                context_sentences = sentences[max(0, sentence_idx-1):min(len(sentences), sentence_idx+2)]
                context = '。'.join(context_sentences)
                
                interactions.append({
                    'source': TARGET_CHARACTER,
                    'target': char_name,
                    'chapter': chapter_num,
                    'type': interaction_type,
                    'context': context,
                    'sentence': sentence
                })
    
    return interactions

def main():
    print("=" * 60)
    print("阶段二：互动关系识别（使用选中的20章）")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n1. 加载数据...")
    character_dict, chapters = load_data()
    target_variants = character_dict[TARGET_CHARACTER]
    
    # 移除目标人物
    other_characters = {k: v for k, v in character_dict.items() if k != TARGET_CHARACTER}
    
    print(f"   目标人物: {TARGET_CHARACTER}")
    print(f"   目标人物变体: {len(target_variants)} 个")
    print(f"   其他人物数量: {len(other_characters)}")
    print(f"   章节数量: {len(chapters)}")
    
    # 2. 提取互动关系
    print("\n2. 提取互动关系...")
    all_interactions = []
    
    for chapter_num in sorted(chapters.keys()):
        text = chapters[chapter_num]
        print(f"   处理章节 {chapter_num}...", end=' ')
        
        # 使用高级方法
        interactions = identify_interactions_advanced(
            text, target_variants, character_dict, chapter_num
        )
        
        all_interactions.extend(interactions)
        print(f"找到 {len(interactions)} 个互动")
    
    print(f"\n   总共找到 {len(all_interactions)} 个互动关系")
    
    # 3. 去重和聚合
    print("\n3. 处理互动数据...")
    interaction_dict = defaultdict(lambda: {
        'count': 0,
        'types': defaultdict(int),
        'chapters': set(),
        'contexts': []
    })
    
    for interaction in all_interactions:
        key = (interaction['source'], interaction['target'])
        interaction_dict[key]['count'] += 1
        interaction_dict[key]['types'][interaction['type']] += 1
        interaction_dict[key]['chapters'].add(interaction['chapter'])
        if len(interaction_dict[key]['contexts']) < 3:  # 只保留前3个上下文
            interaction_dict[key]['contexts'].append(interaction.get('context', interaction.get('sentence', '')))
    
    # 转换为DataFrame
    interaction_list = []
    for (source, target), data in interaction_dict.items():
        interaction_list.append({
            'Source': source,
            'Target': target,
            'Frequency': data['count'],
            'Interaction_Types': '、'.join([f"{k}({v})" for k, v in data['types'].items()]),
            'Chapters': '、'.join([str(c) for c in sorted(data['chapters'])]),
            'Chapter_Count': len(data['chapters']),
            'Context_1': data['contexts'][0] if len(data['contexts']) > 0 else '',
            'Context_2': data['contexts'][1] if len(data['contexts']) > 1 else '',
            'Context_3': data['contexts'][2] if len(data['contexts']) > 2 else '',
        })
    
    df_interactions = pd.DataFrame(interaction_list)
    df_interactions = df_interactions.sort_values('Frequency', ascending=False)
    
    # 保存结果
    csv_file = os.path.join(OUTPUT_DIR, "interactions_v2.csv")
    df_interactions.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"   已保存互动关系表: {csv_file}")
    
    # 保存详细数据（JSON格式）
    json_file = os.path.join(OUTPUT_DIR, "interactions_detailed_v2.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_interactions, f, ensure_ascii=False, indent=2)
    print(f"   已保存详细互动数据: {json_file}")
    
    # 4. 统计信息
    print("\n4. 统计信息:")
    print(f"   总互动关系数: {len(interaction_list)}")
    print(f"   总互动次数: {sum(i['Frequency'] for i in interaction_list)}")
    print(f"\n   前10个最频繁的互动:")
    for idx, row in df_interactions.head(10).iterrows():
        print(f"     {row['Target']}: {row['Frequency']} 次 (章节: {row['Chapters']})")
    
    print("\n" + "=" * 60)
    print("阶段二完成！")
    print("=" * 60)
    
    return df_interactions

if __name__ == "__main__":
    df_interactions = main()

