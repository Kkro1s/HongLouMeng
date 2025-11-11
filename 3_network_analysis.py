#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶段三：网络分析（使用选中的20章）
- 构建网络图
- 计算中心性指标
- 生成可视化
"""

import os
import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 配置
OUTPUT_DIR = "data"
RESULTS_DIR = os.path.join(OUTPUT_DIR, "results_v2")
TARGET_CHARACTER = "薛寶釵"

os.makedirs(RESULTS_DIR, exist_ok=True)

def load_interactions():
    """加载互动数据"""
    df = pd.read_csv(os.path.join(OUTPUT_DIR, "interactions_v2.csv"))
    return df

def build_network(df_interactions):
    """构建网络图"""
    G = nx.DiGraph()  # 有向图
    
    # 添加边
    for _, row in df_interactions.iterrows():
        source = row['Source']
        target = row['Target']
        weight = row['Frequency']
        
        if G.has_edge(source, target):
            G[source][target]['weight'] += weight
        else:
            G.add_edge(source, target, weight=weight)
    
    return G

def calculate_centrality_metrics(G, target_char):
    """计算中心性指标"""
    metrics = {}
    
    # 1. 度中心性 (Degree Centrality)
    degree_centrality = nx.degree_centrality(G)
    metrics['degree_centrality'] = degree_centrality.get(target_char, 0)
    
    # 2. 入度和出度
    if target_char in G:
        in_degree = G.in_degree(target_char)
        out_degree = G.out_degree(target_char)
        total_degree = in_degree + out_degree
    else:
        in_degree = out_degree = total_degree = 0
    
    metrics['in_degree'] = in_degree
    metrics['out_degree'] = out_degree
    metrics['total_degree'] = total_degree
    
    # 3. 加权度中心性
    weighted_degree = sum([G[target_char][neighbor]['weight'] 
                          for neighbor in G.neighbors(target_char)])
    metrics['weighted_degree'] = weighted_degree
    
    # 4. 介数中心性 (Betweenness Centrality)
    try:
        betweenness = nx.betweenness_centrality(G, weight='weight')
        metrics['betweenness_centrality'] = betweenness.get(target_char, 0)
    except:
        metrics['betweenness_centrality'] = 0
    
    # 5. 接近中心性 (Closeness Centrality)
    try:
        closeness = nx.closeness_centrality(G, distance='weight')
        metrics['closeness_centrality'] = closeness.get(target_char, 0)
    except:
        metrics['closeness_centrality'] = 0
    
    # 6. 特征向量中心性 (Eigenvector Centrality)
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000, weight='weight')
        metrics['eigenvector_centrality'] = eigenvector.get(target_char, 0)
    except:
        metrics['eigenvector_centrality'] = 0
    
    # 7. PageRank
    try:
        pagerank = nx.pagerank(G, weight='weight')
        metrics['pagerank'] = pagerank.get(target_char, 0)
    except:
        metrics['pagerank'] = 0
    
    # 8. 聚类系数 (Clustering Coefficient)
    try:
        clustering = nx.clustering(nx.Graph(G))  # 转换为无向图
        metrics['clustering_coefficient'] = clustering.get(target_char, 0)
    except:
        metrics['clustering_coefficient'] = 0
    
    return metrics

def get_all_centrality_metrics(G):
    """计算所有节点的中心性指标"""
    all_metrics = {}
    
    for node in G.nodes():
        metrics = {}
        metrics['degree'] = G.degree(node)
        metrics['in_degree'] = G.in_degree(node)
        metrics['out_degree'] = G.out_degree(node)
        metrics['weighted_degree'] = sum([G[node][neighbor].get('weight', 1) 
                                         for neighbor in G.neighbors(node)])
        all_metrics[node] = metrics
    
    # 计算全局中心性
    try:
        degree_cent = nx.degree_centrality(G)
        betweenness = nx.betweenness_centrality(G, weight='weight')
        closeness = nx.closeness_centrality(G, distance='weight')
        
        for node in G.nodes():
            all_metrics[node]['degree_centrality'] = degree_cent.get(node, 0)
            all_metrics[node]['betweenness_centrality'] = betweenness.get(node, 0)
            all_metrics[node]['closeness_centrality'] = closeness.get(node, 0)
    except:
        pass
    
    return all_metrics

def visualize_network(G, target_char, df_interactions):
    """可视化网络"""
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    
    # 图1: 基本网络图
    ax1 = axes[0]
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # 节点颜色：目标人物为红色，其他为蓝色
    node_colors = ['red' if node == target_char else 'lightblue' for node in G.nodes()]
    
    # 节点大小：基于度中心性
    node_sizes = [G.degree(node) * 300 + 300 for node in G.nodes()]
    
    # 边宽度：基于权重
    edge_widths = [G[u][v].get('weight', 1) * 1.5 for u, v in G.edges()]
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=node_sizes, ax=ax1, alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=edge_widths, 
                          alpha=0.5, edge_color='gray', ax=ax1, arrows=True, arrowsize=15)
    nx.draw_networkx_labels(G, pos, font_size=9, ax=ax1, font_family='Arial Unicode MS')
    
    ax1.set_title(f'薛寶釵社交网络图 (选中20章)', fontsize=16, pad=20)
    ax1.axis('off')
    
    # 图2: 力导向布局（更美观）
    ax2 = axes[1]
    pos2 = nx.spring_layout(G, k=2.5, iterations=100, seed=42)
    
    # 只显示主要连接（权重>=5）
    G_filtered = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        if data.get('weight', 0) >= 5:
            G_filtered.add_edge(u, v, **data)
    
    if len(G_filtered.nodes()) > 0:
        pos2_filtered = {node: pos2[node] for node in G_filtered.nodes()}
        node_colors2 = ['red' if node == target_char else 'lightblue' 
                       for node in G_filtered.nodes()]
        node_sizes2 = [G.degree(node) * 300 + 300 for node in G_filtered.nodes()]
        edge_widths2 = [G_filtered[u][v].get('weight', 1) * 2 
                        for u, v in G_filtered.edges()]
        
        nx.draw_networkx_nodes(G_filtered, pos2_filtered, node_color=node_colors2,
                              node_size=node_sizes2, ax=ax2, alpha=0.8)
        nx.draw_networkx_edges(G_filtered, pos2_filtered, width=edge_widths2,
                              alpha=0.6, edge_color='darkgray', ax=ax2, 
                              arrows=True, arrowsize=20)
        nx.draw_networkx_labels(G_filtered, pos2_filtered, font_size=10, 
                               ax=ax2, font_family='Arial Unicode MS')
        
        # 添加边标签（权重）
        edge_labels = {(u, v): str(d['weight']) 
                       for u, v, d in G_filtered.edges(data=True)}
        nx.draw_networkx_edge_labels(G_filtered, pos2_filtered, edge_labels, 
                                   ax=ax2, font_size=7)
    
    ax2.set_title('主要互动关系网络 (频率≥5)', fontsize=16, pad=20)
    ax2.axis('off')
    
    plt.tight_layout()
    output_file = os.path.join(RESULTS_DIR, "network_visualization.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   已保存网络可视化: {output_file}")
    plt.close()

def create_centrality_chart(metrics_dict, target_char, df_interactions):
    """创建中心性指标对比图 - 使用互动频率"""
    # 从互动数据中提取频率信息
    interaction_freq = {}
    for _, row in df_interactions.iterrows():
        target = row['Target']
        freq = row['Frequency']
        interaction_freq[target] = freq
    
    # 排除目标人物本身，只显示与薛寶釵互动的人物
    nodes_to_show = [node for node in interaction_freq.keys() if node != target_char]
    frequencies = [interaction_freq[node] for node in nodes_to_show]
    
    # 创建条形图
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # 图1: 互动频率对比
    ax1 = axes[0]
    sorted_data = sorted(zip(nodes_to_show, frequencies), key=lambda x: x[1], reverse=True)
    sorted_nodes, sorted_freqs = zip(*sorted_data)
    
    colors = ['#FF6B6B' if freq >= 20 else '#4ECDC4' if freq >= 10 else '#95E1D3' 
              for freq in sorted_freqs]
    
    bars1 = ax1.barh(range(len(sorted_nodes)), sorted_freqs, color=colors, alpha=0.8)
    ax1.set_yticks(range(len(sorted_nodes)))
    ax1.set_yticklabels(sorted_nodes, fontsize=10)
    ax1.set_xlabel('互动频率 (Frequency)', fontsize=12, fontweight='bold')
    ax1.set_title('与薛寶釵的互动频率对比 (20章)', fontsize=14, pad=20, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    # 添加数值标签
    for i, (node, freq) in enumerate(zip(sorted_nodes, sorted_freqs)):
        ax1.text(freq + 1, i, str(int(freq)), va='center', fontsize=9, fontweight='bold')
    
    # 添加图例
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF6B6B', alpha=0.8, label='高频互动 (≥20次)'),
        Patch(facecolor='#4ECDC4', alpha=0.8, label='中频互动 (10-19次)'),
        Patch(facecolor='#95E1D3', alpha=0.8, label='低频互动 (<10次)')
    ]
    ax1.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    # 图2: 互动类型分布
    ax2 = axes[1]
    interaction_types = {}
    for _, row in df_interactions.iterrows():
        target = row['Target']
        types_str = row['Interaction_Types']
        type_count = {}
        for type_info in types_str.split('、'):
            if '(' in type_info:
                type_name = type_info.split('(')[0]
                count = int(type_info.split('(')[1].split(')')[0])
                type_count[type_name] = count
        interaction_types[target] = type_count
    
    # 统计各类型总数
    type_totals = {'对话': 0, '行为': 0, '共同出现': 0}
    for target, types in interaction_types.items():
        for ttype, count in types.items():
            if ttype in type_totals:
                type_totals[ttype] += count
    
    type_names = list(type_totals.keys())
    type_counts = list(type_totals.values())
    colors_pie = ['#FF6B6B', '#4ECDC4', '#95E1D3']
    ax2.pie(type_counts, labels=type_names, autopct='%1.1f%%', 
           colors=colors_pie, startangle=90, textprops={'fontsize': 11})
    ax2.set_title('互动类型分布', fontsize=14, pad=20, fontweight='bold')
    
    plt.tight_layout()
    output_file = os.path.join(RESULTS_DIR, "centrality_comparison.png")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"   已保存中心性对比图: {output_file}")
    plt.close()

def main():
    print("=" * 60)
    print("阶段三：网络分析（使用选中的20章）")
    print("=" * 60)
    
    # 1. 加载数据
    print("\n1. 加载互动数据...")
    df_interactions = load_interactions()
    print(f"   互动关系数: {len(df_interactions)}")
    
    # 2. 构建网络
    print("\n2. 构建网络图...")
    G = build_network(df_interactions)
    print(f"   节点数: {G.number_of_nodes()}")
    print(f"   边数: {G.number_of_edges()}")
    print(f"   网络密度: {nx.density(G):.4f}")
    
    # 保存网络数据（GML格式，可用于Gephi）
    gml_file = os.path.join(RESULTS_DIR, "network.gml")
    nx.write_gml(G, gml_file)
    print(f"   已保存网络数据(GML): {gml_file}")
    
    # 3. 计算中心性指标
    print("\n3. 计算中心性指标...")
    target_metrics = calculate_centrality_metrics(G, TARGET_CHARACTER)
    
    print(f"\n   薛寶釵的中心性指标:")
    print(f"   度中心性: {target_metrics['degree_centrality']:.4f}")
    print(f"   总度数: {target_metrics['total_degree']}")
    print(f"   入度: {target_metrics['in_degree']}")
    print(f"   出度: {target_metrics['out_degree']}")
    print(f"   加权度: {target_metrics['weighted_degree']}")
    print(f"   介数中心性: {target_metrics['betweenness_centrality']:.4f}")
    print(f"   接近中心性: {target_metrics['closeness_centrality']:.4f}")
    print(f"   特征向量中心性: {target_metrics['eigenvector_centrality']:.4f}")
    print(f"   PageRank: {target_metrics['pagerank']:.4f}")
    print(f"   聚类系数: {target_metrics['clustering_coefficient']:.4f}")
    
    # 计算所有节点的指标
    all_metrics = get_all_centrality_metrics(G)
    
    # 保存指标数据
    metrics_list = []
    for node, metrics in all_metrics.items():
        metrics['character'] = node
        metrics_list.append(metrics)
    
    df_metrics = pd.DataFrame(metrics_list)
    metrics_file = os.path.join(RESULTS_DIR, "centrality_metrics.csv")
    df_metrics.to_csv(metrics_file, index=False, encoding='utf-8-sig')
    print(f"\n   已保存中心性指标表: {metrics_file}")
    
    # 保存目标人物的详细指标
    target_file = os.path.join(RESULTS_DIR, f"{TARGET_CHARACTER}_metrics.json")
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(target_metrics, f, ensure_ascii=False, indent=2)
    print(f"   已保存薛寶釵详细指标: {target_file}")
    
    # 4. 可视化
    print("\n4. 生成可视化...")
    visualize_network(G, TARGET_CHARACTER, df_interactions)
    create_centrality_chart(all_metrics, TARGET_CHARACTER, df_interactions)
    
    # 5. 网络统计
    print("\n5. 网络统计:")
    print(f"   平均度: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")
    if nx.is_strongly_connected(G):
        print(f"   平均路径长度: {nx.average_shortest_path_length(G):.4f}")
    else:
        print("   网络不连通，无法计算平均路径长度")
    
    # 找出与薛寶釵直接连接的人物
    neighbors = list(G.neighbors(TARGET_CHARACTER))
    print(f"\n   与薛寶釵直接互动的人物 ({len(neighbors)} 个):")
    for neighbor in neighbors:
        weight = G[TARGET_CHARACTER][neighbor]['weight']
        print(f"     - {neighbor}: {weight} 次")
    
    print("\n" + "=" * 60)
    print("阶段三完成！")
    print("=" * 60)
    
    return G, target_metrics, df_metrics

if __name__ == "__main__":
    G, target_metrics, df_metrics = main()

