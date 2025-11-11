#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级网络分析算法补充
实现更多样化的网络分析算法
"""

import os
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 配置
OUTPUT_DIR = "data"
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results_v2")  # 使用v2结果目录
TARGET_CHARACTER = "薛寶釵"

os.makedirs(RESULTS_DIR, exist_ok=True)

def load_data():
    """加载数据"""
    # 优先使用v2数据
    interactions_file = os.path.join(OUTPUT_DIR, "interactions_v2.csv")
    if not os.path.exists(interactions_file):
        interactions_file = os.path.join(OUTPUT_DIR, "interactions.csv")
    df_interactions = pd.read_csv(interactions_file)
    
    # 构建网络
    G = nx.DiGraph()
    for _, row in df_interactions.iterrows():
        if G.has_edge(row['Source'], row['Target']):
            G[row['Source']][row['Target']]['weight'] += row['Frequency']
        else:
            G.add_edge(row['Source'], row['Target'], weight=row['Frequency'])
    
    return G, df_interactions

def calculate_katz_centrality(G):
    """计算Katz中心性"""
    try:
        # 转换为无向图进行计算
        G_undirected = nx.Graph(G)
        katz = nx.katz_centrality(G_undirected, alpha=0.1, beta=1.0, max_iter=1000, tol=1e-06)
        return katz
    except Exception as e:
        print(f"   Katz中心性计算失败: {e}")
        return {}

def calculate_harmonic_centrality(G):
    """计算调和中心性"""
    try:
        harmonic = nx.harmonic_centrality(G)
        return harmonic
    except Exception as e:
        print(f"   调和中心性计算失败: {e}")
        return {}

def calculate_hits(G):
    """计算HITS算法（Hub和Authority）"""
    try:
        hubs, authorities = nx.hits(G, max_iter=100, tol=1e-08)
        return hubs, authorities
    except Exception as e:
        print(f"   HITS算法计算失败: {e}")
        return {}, {}

def calculate_subgraph_centrality(G):
    """计算子图中心性"""
    try:
        # 转换为无向图
        G_undirected = nx.Graph(G)
        subgraph = nx.subgraph_centrality(G_undirected)
        return subgraph
    except Exception as e:
        print(f"   子图中心性计算失败: {e}")
        return {}

def calculate_core_periphery(G):
    """计算核心-边缘结构"""
    try:
        # 转换为无向图
        G_undirected = nx.Graph(G)
        core_number = nx.core_number(G_undirected)
        return core_number
    except Exception as e:
        print(f"   核心-边缘分析失败: {e}")
        return {}

def calculate_structural_holes(G):
    """计算结构洞指标"""
    try:
        constraint = nx.constraint(G)
        return constraint
    except Exception as e:
        print(f"   结构洞分析失败: {e}")
        return {}

def detect_communities(G):
    """社区检测（使用Louvain算法）"""
    try:
        # 尝试导入community库
        try:
            import community.community_louvain as community_louvain
            # 转换为无向图
            G_undirected = nx.Graph(G)
            communities = community_louvain.best_partition(G_undirected)
            return communities
        except ImportError:
            print("   社区检测需要python-louvain库，使用替代方法")
            # 使用NetworkX内置的贪心模块度算法
            from networkx.algorithms import community
            G_undirected = nx.Graph(G)
            communities_generator = community.greedy_modularity_communities(G_undirected)
            communities = {}
            for i, comm in enumerate(communities_generator):
                for node in comm:
                    communities[node] = i
            return communities
    except Exception as e:
        print(f"   社区检测失败: {e}")
        return {}

def analyze_triads(G):
    """三元组分析"""
    try:
        from networkx.algorithms import triad
        G_undirected = nx.Graph(G)
        triad_census = triad.triads_by_type(G_undirected)
        return triad_census
    except Exception as e:
        print(f"   三元组分析失败: {e}")
        return {}

def calculate_network_properties(G):
    """计算网络属性"""
    properties = {}
    
    # 基本属性
    properties['num_nodes'] = G.number_of_nodes()
    properties['num_edges'] = G.number_of_edges()
    properties['density'] = nx.density(G)
    
    # 度分布
    degree_sequence = [d for n, d in G.degree()]
    properties['avg_degree'] = np.mean(degree_sequence)
    properties['max_degree'] = max(degree_sequence)
    properties['min_degree'] = min(degree_sequence)
    
    # 互惠性
    try:
        properties['reciprocity'] = nx.reciprocity(G)
    except:
        properties['reciprocity'] = 0
    
    # 传递性（转换为无向图）
    try:
        G_undirected = nx.Graph(G)
        properties['transitivity'] = nx.transitivity(G_undirected)
    except:
        properties['transitivity'] = 0
    
    # 连通性
    properties['is_strongly_connected'] = nx.is_strongly_connected(G)
    properties['is_weakly_connected'] = nx.is_weakly_connected(G)
    
    # 强连通分量
    if properties['is_strongly_connected']:
        properties['num_strongly_connected_components'] = 1
    else:
        properties['num_strongly_connected_components'] = nx.number_strongly_connected_components(G)
    
    return properties

def visualize_advanced_metrics(all_metrics, target_char):
    """可视化高级指标"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 提取数据
    characters = [m['character'] for m in all_metrics if m['character'] != target_char]
    
    # 图1: Katz中心性
    ax1 = axes[0, 0]
    katz_values = [m.get('katz_centrality', 0) for m in all_metrics if m['character'] != target_char]
    if katz_values and max(katz_values) > 0:
        sorted_data = sorted(zip(characters, katz_values), key=lambda x: x[1], reverse=True)
        sorted_chars, sorted_katz = zip(*sorted_data)
        colors = ['#FF6B6B' if k >= max(katz_values)*0.5 else '#4ECDC4' for k in sorted_katz]
        ax1.barh(range(len(sorted_chars)), sorted_katz, color=colors, alpha=0.8)
        ax1.set_yticks(range(len(sorted_chars)))
        ax1.set_yticklabels(sorted_chars, fontsize=10)
        ax1.set_xlabel('Katz中心性', fontsize=11)
        ax1.set_title('Katz中心性对比', fontsize=12, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)
    
    # 图2: HITS - Hub值
    ax2 = axes[0, 1]
    hub_values = [m.get('hub_score', 0) for m in all_metrics if m['character'] != target_char]
    if hub_values and max(hub_values) > 0:
        sorted_data = sorted(zip(characters, hub_values), key=lambda x: x[1], reverse=True)
        sorted_chars, sorted_hubs = zip(*sorted_data)
        colors = ['#FF6B6B' if h >= max(hub_values)*0.5 else '#4ECDC4' for h in sorted_hubs]
        ax2.barh(range(len(sorted_chars)), sorted_hubs, color=colors, alpha=0.8)
        ax2.set_yticks(range(len(sorted_chars)))
        ax2.set_yticklabels(sorted_chars, fontsize=10)
        ax2.set_xlabel('Hub分数', fontsize=11)
        ax2.set_title('HITS算法 - Hub值', fontsize=12, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
    
    # 图3: HITS - Authority值
    ax3 = axes[1, 0]
    auth_values = [m.get('authority_score', 0) for m in all_metrics if m['character'] != target_char]
    if auth_values and max(auth_values) > 0:
        sorted_data = sorted(zip(characters, auth_values), key=lambda x: x[1], reverse=True)
        sorted_chars, sorted_auths = zip(*sorted_data)
        colors = ['#FF6B6B' if a >= max(auth_values)*0.5 else '#4ECDC4' for a in sorted_auths]
        ax3.barh(range(len(sorted_chars)), sorted_auths, color=colors, alpha=0.8)
        ax3.set_yticks(range(len(sorted_chars)))
        ax3.set_yticklabels(sorted_chars, fontsize=10)
        ax3.set_xlabel('Authority分数', fontsize=11)
        ax3.set_title('HITS算法 - Authority值', fontsize=12, fontweight='bold')
        ax3.grid(axis='x', alpha=0.3)
    
    # 图4: 调和中心性
    ax4 = axes[1, 1]
    harmonic_values = [m.get('harmonic_centrality', 0) for m in all_metrics if m['character'] != target_char]
    if harmonic_values and max(harmonic_values) > 0:
        sorted_data = sorted(zip(characters, harmonic_values), key=lambda x: x[1], reverse=True)
        sorted_chars, sorted_harmonic = zip(*sorted_data)
        colors = ['#FF6B6B' if h >= max(harmonic_values)*0.5 else '#4ECDC4' for h in sorted_harmonic]
        ax4.barh(range(len(sorted_chars)), sorted_harmonic, color=colors, alpha=0.8)
        ax4.set_yticks(range(len(sorted_chars)))
        ax4.set_yticklabels(sorted_chars, fontsize=10)
        ax4.set_xlabel('调和中心性', fontsize=11)
        ax4.set_title('调和中心性对比', fontsize=12, fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    output_file = os.path.join(RESULTS_DIR, "advanced_metrics.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   已保存高级指标可视化: {output_file}")
    plt.close()

def main():
    print("=" * 60)
    print("高级网络分析算法补充")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n1. 加载数据...")
    G, df_interactions = load_data()
    print(f"   节点数: {G.number_of_nodes()}")
    print(f"   边数: {G.number_of_edges()}")
    
    # 2. 计算高级指标
    print("\n2. 计算高级网络分析指标...")
    
    all_metrics = []
    
    # Katz中心性
    print("   计算Katz中心性...")
    katz = calculate_katz_centrality(G)
    
    # 调和中心性
    print("   计算调和中心性...")
    harmonic = calculate_harmonic_centrality(G)
    
    # HITS算法
    print("   计算HITS算法...")
    hubs, authorities = calculate_hits(G)
    
    # 子图中心性
    print("   计算子图中心性...")
    subgraph = calculate_subgraph_centrality(G)
    
    # 核心-边缘分析
    print("   计算核心-边缘结构...")
    core_number = calculate_core_periphery(G)
    
    # 结构洞分析
    print("   计算结构洞指标...")
    constraint = calculate_structural_holes(G)
    
    # 社区检测
    print("   进行社区检测...")
    communities = detect_communities(G)
    
    # 三元组分析
    print("   进行三元组分析...")
    triad_census = analyze_triads(G)
    
    # 网络属性
    print("   计算网络属性...")
    network_props = calculate_network_properties(G)
    
    # 3. 整合所有指标
    print("\n3. 整合指标数据...")
    for node in G.nodes():
        metrics = {
            'character': node,
            'katz_centrality': katz.get(node, 0),
            'harmonic_centrality': harmonic.get(node, 0),
            'hub_score': hubs.get(node, 0),
            'authority_score': authorities.get(node, 0),
            'subgraph_centrality': subgraph.get(node, 0),
            'core_number': core_number.get(node, 0),
            'constraint': constraint.get(node, 0),
            'community': communities.get(node, -1)
        }
        all_metrics.append(metrics)
    
    # 保存高级指标
    df_advanced = pd.DataFrame(all_metrics)
    advanced_file = os.path.join(RESULTS_DIR, "advanced_metrics.csv")
    df_advanced.to_csv(advanced_file, index=False, encoding='utf-8-sig')
    print(f"   已保存高级指标表: {advanced_file}")
    
    # 保存网络属性
    props_file = os.path.join(RESULTS_DIR, "network_properties.json")
    with open(props_file, 'w', encoding='utf-8') as f:
        json.dump(network_props, f, ensure_ascii=False, indent=2)
    print(f"   已保存网络属性: {props_file}")
    
    # 保存三元组分析结果
    if triad_census:
        triad_file = os.path.join(RESULTS_DIR, "triad_census.json")
        with open(triad_file, 'w', encoding='utf-8') as f:
            json.dump(triad_census, f, ensure_ascii=False, indent=2)
        print(f"   已保存三元组分析: {triad_file}")
    
    # 4. 可视化
    print("\n4. 生成可视化...")
    visualize_advanced_metrics(all_metrics, TARGET_CHARACTER)
    
    # 5. 输出关键结果
    print("\n5. 关键结果:")
    target_metrics = [m for m in all_metrics if m['character'] == TARGET_CHARACTER]
    if target_metrics:
        tm = target_metrics[0]
        print(f"\n   薛寶釵的高级指标:")
        print(f"   Katz中心性: {tm['katz_centrality']:.6f}")
        print(f"   调和中心性: {tm['harmonic_centrality']:.6f}")
        print(f"   Hub分数: {tm['hub_score']:.6f}")
        print(f"   Authority分数: {tm['authority_score']:.6f}")
        print(f"   子图中心性: {tm['subgraph_centrality']:.6f}")
        print(f"   核心数: {tm['core_number']}")
        print(f"   约束度: {tm['constraint']:.6f}")
        print(f"   社区ID: {tm['community']}")
    
    print(f"\n   网络属性:")
    print(f"   密度: {network_props['density']:.4f}")
    print(f"   平均度: {network_props['avg_degree']:.2f}")
    print(f"   互惠性: {network_props['reciprocity']:.4f}")
    print(f"   传递性: {network_props['transitivity']:.4f}")
    print(f"   强连通: {network_props['is_strongly_connected']}")
    print(f"   弱连通: {network_props['is_weakly_connected']}")
    
    print("\n" + "=" * 60)
    print("高级网络分析完成！")
    print("=" * 60)
    
    return all_metrics, network_props

if __name__ == "__main__":
    all_metrics, network_props = main()

