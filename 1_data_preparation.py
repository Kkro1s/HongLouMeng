#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶段一：数据准备（使用选中的20章）
- 文本清理与标准化
- 构建人物名称词典
"""

import os
import re
import json
import pandas as pd
from pathlib import Path

# 配置
CHAPTER_DIR = "Chapter 10- 20"
OUTPUT_DIR = "data"
CLEANED_DIR = os.path.join(OUTPUT_DIR, "cleaned_texts_v2")

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CLEANED_DIR, exist_ok=True)

def load_selected_chapters():
    """加载选中的章节列表"""
    selection_file = os.path.join(OUTPUT_DIR, "selected_chapters.json")
    with open(selection_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['selected_chapters']

def clean_text(text):
    """清理文本：移除标题、统一格式"""
    # 移除章节标题（如《金寡婦貪利權受辱　張太醫論病細窮源》）
    text = re.sub(r'《[^》]+》', '', text)
    # 移除多余的空白行
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
    # 移除行首行尾空白
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    return text.strip()

def load_chapters(selected_chapters):
    """加载选中的章节文本"""
    chapters = {}
    
    for chapter_num in selected_chapters:
        filename = f"ch{chapter_num:03d}.txt"
        filepath = os.path.join(CHAPTER_DIR, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            chapters[chapter_num] = {
                'filename': filename,
                'raw': content,
                'cleaned': clean_text(content)
            }
        else:
            print(f"警告: 未找到文件 {filepath}")
    
    return chapters

def build_character_dictionary():
    """构建人物名称词典"""
    character_dict = {
        # 薛寶釵及其变体
        '薛寶釵': ['薛寶釵', '寶釵', '寶姐姐', '薛大姑娘', '薛姑娘', '薛姨媽的女兒', '寶丫頭'],
        
        # 主要人物
        '賈寶玉': ['賈寶玉', '寶玉', '寶二爺', '寶兄弟', '寶哥哥', '怡紅公子', '二爺'],
        '林黛玉': ['林黛玉', '黛玉', '林妹妹', '林姑娘', '顰兒', '瀟湘妃子'],
        
        # 次要人物 - 丫鬟
        '襲人': ['襲人', '花襲人', '襲人姐姐'],
        '鴛鴦': ['鴛鴦', '鴛鴦姐姐'],
        '晴雯': ['晴雯', '晴雯姐姐'],
        '鶯兒': ['鶯兒', '黃金鶯'],
        '紫鵑': ['紫鵑', '紫鵑姐姐'],
        '香菱': ['香菱', '英蓮', '秋菱'],
        
        # 次要人物 - 长辈
        '賈母': ['賈母', '老太太', '老祖宗', '史太君'],
        '賈政': ['賈政', '老爺', '政老爺'],
        '王夫人': ['王夫人', '太太', '二太太'],
        '薛姨媽': ['薛姨媽', '薛姨媽', '姨媽'],
        '邢夫人': ['邢夫人', '大太太'],
        
        # 次要人物 - 同辈
        '賈環': ['賈環', '環哥兒', '環兄弟'],
        '賈蓉': ['賈蓉', '蓉哥兒'],
        '賈薔': ['賈薔', '薔哥兒'],
        '史湘雲': ['史湘雲', '湘雲', '雲妹妹', '史大姑娘'],
        '迎春': ['迎春', '二姑娘'],
        '探春': ['探春', '三姑娘'],
        '惜春': ['惜春', '四姑娘'],
        
        # 次要人物 - 其他
        '鳳姐': ['鳳姐', '鳳姐兒', '鳳丫頭', '璉二奶奶', '王熙鳳'],
        '尤氏': ['尤氏', '珍大奶奶'],
        '李紈': ['李紈', '大奶奶', '珠大奶奶'],
        '元春': ['元春', '元妃', '貴妃', '娘娘'],
        '秦鐘': ['秦鐘', '秦鐘兒'],
        '賈瑞': ['賈瑞', '瑞大爺'],
        '張太醫': ['張太醫', '張先生', '張友士'],
    }
    
    return character_dict

def create_character_mapping(character_dict):
    """创建人物名称到标准名称的映射"""
    mapping = {}
    for standard_name, variants in character_dict.items():
        for variant in variants:
            mapping[variant] = standard_name
    return mapping

def save_cleaned_texts(chapters):
    """保存清理后的文本"""
    for chapter_num, data in chapters.items():
        output_file = os.path.join(CLEANED_DIR, f"ch{chapter_num:03d}_cleaned.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(data['cleaned'])
        print(f"已保存清理后的章节 {chapter_num}: {output_file}")

def main():
    print("=" * 60)
    print("阶段一：数据准备（使用选中的20章）")
    print("=" * 60)
    
    # 1. 加载选中的章节
    print("\n1. 加载选中的章节...")
    selected_chapters = load_selected_chapters()
    print(f"   选中章节: {selected_chapters}")
    print(f"   章节数量: {len(selected_chapters)}")
    
    # 2. 加载章节文本
    print("\n2. 加载章节文本...")
    chapters = load_chapters(selected_chapters)
    print(f"   成功加载 {len(chapters)} 个章节")
    
    # 3. 保存清理后的文本
    print("\n3. 保存清理后的文本...")
    save_cleaned_texts(chapters)
    
    # 4. 构建人物词典
    print("\n4. 构建人物名称词典...")
    character_dict = build_character_dictionary()
    character_mapping = create_character_mapping(character_dict)
    
    # 保存人物词典
    dict_file = os.path.join(OUTPUT_DIR, "character_dictionary_v2.json")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(character_dict, f, ensure_ascii=False, indent=2)
    print(f"   已保存人物词典: {dict_file}")
    
    # 保存映射表
    mapping_file = os.path.join(OUTPUT_DIR, "character_mapping_v2.json")
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(character_mapping, f, ensure_ascii=False, indent=2)
    print(f"   已保存人物映射表: {mapping_file}")
    
    # 保存为CSV格式（便于查看）
    character_list = []
    for standard_name, variants in character_dict.items():
        character_list.append({
            '标准名称': standard_name,
            '变体名称': '、'.join(variants),
            '变体数量': len(variants)
        })
    
    df_characters = pd.DataFrame(character_list)
    csv_file = os.path.join(OUTPUT_DIR, "character_dictionary_v2.csv")
    df_characters.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"   已保存人物词典CSV: {csv_file}")
    
    # 5. 统计信息
    print("\n5. 数据统计:")
    total_chars = sum(len(ch['cleaned']) for ch in chapters.values())
    print(f"   总字符数: {total_chars:,}")
    print(f"   人物数量: {len(character_dict)}")
    print(f"   人物名称变体总数: {sum(len(v) for v in character_dict.values())}")
    
    print("\n" + "=" * 60)
    print("阶段一完成！")
    print("=" * 60)
    
    return chapters, character_dict, character_mapping

if __name__ == "__main__":
    chapters, character_dict, character_mapping = main()

