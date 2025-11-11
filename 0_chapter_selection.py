#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节选择：根据薛寶釵的出现频率选择前20章
"""

import os
import re
import json
import pandas as pd
from collections import defaultdict

# 配置
CHAPTER_DIR = "Chapter 10- 20"
TARGET_CHARACTER = "薛寶釵"
OUTPUT_DIR = "data"

# 薛寶釵的名称变体
BAOCHAI_VARIANTS = ['薛寶釵', '寶釵', '寶姐姐', '薛大姑娘', '薛姑娘', '薛姨媽的女兒', '寶丫頭']

def count_baochai_mentions(text):
    """统计薛寶釵在文本中的出现次数"""
    count = 0
    for variant in BAOCHAI_VARIANTS:
        # 使用正则表达式查找，考虑标点符号
        pattern = re.escape(variant)
        matches = re.findall(pattern, text)
        count += len(matches)
    return count

def analyze_all_chapters():
    """分析所有章节，统计薛寶釵的出现频率"""
    chapter_stats = []
    
    # 获取所有章节文件
    chapter_files = sorted([f for f in os.listdir(CHAPTER_DIR) 
                           if f.startswith('ch') and f.endswith('.txt')])
    
    print(f"找到 {len(chapter_files)} 个章节文件")
    print("\n正在分析各章节中薛寶釵的出现频率...")
    
    for filename in chapter_files:
        # 提取章节号
        match = re.search(r'ch(\d+)', filename)
        if not match:
            continue
        
        chapter_num = int(match.group(1))
        filepath = os.path.join(CHAPTER_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计出现次数
            mention_count = count_baochai_mentions(content)
            
            # 统计文本长度
            text_length = len(content)
            
            # 计算密度（每1000字出现的次数）
            density = (mention_count / text_length * 1000) if text_length > 0 else 0
            
            chapter_stats.append({
                'chapter': chapter_num,
                'filename': filename,
                'mention_count': mention_count,
                'text_length': text_length,
                'density': density
            })
            
            print(f"   章节 {chapter_num:2d}: {mention_count:3d} 次 (密度: {density:.2f}/千字)")
            
        except Exception as e:
            print(f"   错误处理章节 {chapter_num}: {e}")
            continue
    
    return chapter_stats

def select_top_chapters(chapter_stats, top_n=20):
    """选择出现频率最高的N章"""
    # 按出现次数排序
    sorted_chapters = sorted(chapter_stats, key=lambda x: x['mention_count'], reverse=True)
    
    # 选择前N章
    top_chapters = sorted_chapters[:top_n]
    
    # 按章节号排序
    top_chapters_sorted = sorted(top_chapters, key=lambda x: x['chapter'])
    
    return top_chapters_sorted, sorted_chapters

def main():
    print("=" * 60)
    print("章节选择：根据薛寶釵出现频率选择前20章")
    print("=" * 60)
    
    # 1. 分析所有章节
    chapter_stats = analyze_all_chapters()
    
    if not chapter_stats:
        print("未找到任何章节文件！")
        return
    
    # 2. 选择前20章
    print("\n" + "=" * 60)
    print("选择出现频率最高的20章...")
    print("=" * 60)
    
    top_20, all_sorted = select_top_chapters(chapter_stats, top_n=20)
    
    print(f"\n选中的20章（按章节号排序）:")
    print("-" * 60)
    print(f"{'章节':<8} {'出现次数':<10} {'文本长度':<12} {'密度(/千字)':<15}")
    print("-" * 60)
    
    total_mentions = 0
    for ch in top_20:
        print(f"第{ch['chapter']:2d}章    {ch['mention_count']:3d}次      {ch['text_length']:6d}字      {ch['density']:8.2f}")
        total_mentions += ch['mention_count']
    
    print("-" * 60)
    print(f"总计: {total_mentions} 次出现")
    
    # 3. 保存结果
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 保存选中的章节列表
    selected_chapters = [ch['chapter'] for ch in top_20]
    selection_file = os.path.join(OUTPUT_DIR, "selected_chapters.json")
    with open(selection_file, 'w', encoding='utf-8') as f:
        json.dump({
            'selected_chapters': selected_chapters,
            'total_chapters': len(selected_chapters),
            'total_mentions': total_mentions,
            'chapter_details': top_20
        }, f, ensure_ascii=False, indent=2)
    print(f"\n已保存选中章节列表: {selection_file}")
    
    # 保存所有章节的统计
    df_all = pd.DataFrame(all_sorted)
    all_stats_file = os.path.join(OUTPUT_DIR, "all_chapters_stats.csv")
    df_all.to_csv(all_stats_file, index=False, encoding='utf-8-sig')
    print(f"已保存所有章节统计: {all_stats_file}")
    
    # 保存选中章节的统计
    df_selected = pd.DataFrame(top_20)
    selected_stats_file = os.path.join(OUTPUT_DIR, "selected_chapters_stats.csv")
    df_selected.to_csv(selected_stats_file, index=False, encoding='utf-8-sig')
    print(f"已保存选中章节统计: {selected_stats_file}")
    
    # 4. 统计信息
    print("\n" + "=" * 60)
    print("统计信息:")
    print("=" * 60)
    print(f"总章节数: {len(chapter_stats)}")
    print(f"选中章节数: {len(top_20)}")
    print(f"平均出现次数（选中章节）: {total_mentions / len(top_20):.1f}")
    print(f"最高出现次数: {all_sorted[0]['mention_count']}次 (第{all_sorted[0]['chapter']}章)")
    print(f"最低出现次数（选中）: {top_20[-1]['mention_count']}次 (第{top_20[-1]['chapter']}章)")
    
    print("\n" + "=" * 60)
    print("章节选择完成！")
    print("=" * 60)
    
    return top_20, selected_chapters

if __name__ == "__main__":
    top_20, selected_chapters = main()

