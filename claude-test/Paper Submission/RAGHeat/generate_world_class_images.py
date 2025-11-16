#!/usr/bin/env python3
"""
World-Class Publication-Ready Image Generator for RAGHeat Paper
Generates Neo4j-style knowledge graphs and professional visualizations
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
import numpy as np
import networkx as nx
from matplotlib.patches import ConnectionPatch
import matplotlib.gridspec as gridspec
from matplotlib import cm
from scipy.interpolate import make_interp_spline

# Set publication-quality parameters
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['text.usetex'] = False

# Color palette for publication (IEEE style)
COLORS = {
    'primary': '#1f77b4',      # Blue
    'secondary': '#ff7f0e',    # Orange
    'success': '#2ca02c',      # Green
    'danger': '#d62728',       # Red
    'warning': '#9467bd',      # Purple
    'info': '#8c564b',         # Brown
    'light': '#e377c2',        # Pink
    'dark': '#7f7f7f',         # Gray
    'sector': '#17becf',       # Cyan
    'event': '#bcbd22',        # Yellow-green
    'stock': '#ff9896',        # Light red
    'indicator': '#c5b0d5',    # Light purple
}


def create_neo4j_knowledge_graph():
    """Generate a Neo4j-style knowledge graph visualization"""
    fig, ax = plt.subplots(figsize=(12, 10))

    # Create graph structure
    G = nx.Graph()

    # Define nodes with positions (circular layout with hierarchy)
    nodes = {
        # Central market node
        'USA_Market': {'pos': (0, 0), 'size': 3000, 'color': COLORS['primary'], 'type': 'Market'},

        # Sector nodes (inner circle)
        'Technology': {'pos': (3, 3), 'size': 2000, 'color': COLORS['sector'], 'type': 'Sector'},
        'Finance': {'pos': (4, 0), 'size': 2000, 'color': COLORS['sector'], 'type': 'Sector'},
        'Healthcare': {'pos': (3, -3), 'size': 2000, 'color': COLORS['sector'], 'type': 'Sector'},
        'Energy': {'pos': (-3, -3), 'size': 2000, 'color': COLORS['sector'], 'type': 'Sector'},
        'Consumer': {'pos': (-4, 0), 'size': 2000, 'color': COLORS['sector'], 'type': 'Sector'},
        'Industrial': {'pos': (-3, 3), 'size': 2000, 'color': COLORS['sector'], 'type': 'Sector'},

        # Stock nodes (outer circle)
        'AAPL': {'pos': (5, 5), 'size': 1200, 'color': COLORS['stock'], 'type': 'Stock', 'heat': 0.85},
        'NVDA': {'pos': (6, 2), 'size': 1200, 'color': COLORS['stock'], 'type': 'Stock', 'heat': 0.92},
        'GOOGL': {'pos': (5, 0), 'size': 1200, 'color': COLORS['stock'], 'type': 'Stock', 'heat': 0.65},
        'JPM': {'pos': (6, -2), 'size': 1200, 'color': COLORS['stock'], 'type': 'Stock', 'heat': 0.78},
        'JNJ': {'pos': (5, -5), 'size': 1200, 'color': COLORS['stock'], 'type': 'Stock', 'heat': 0.45},
        'XOM': {'pos': (-5, -5), 'size': 1200, 'color': COLORS['stock'], 'type': 'Stock', 'heat': 0.88},
        'WMT': {'pos': (-6, 0), 'size': 1200, 'color': COLORS['stock'], 'type': 'Stock', 'heat': 0.55},
        'CAT': {'pos': (-5, 5), 'size': 1200, 'color': COLORS['stock'], 'type': 'Stock', 'heat': 0.62},

        # Event/Indicator nodes
        'Fed_Rate': {'pos': (0, -6), 'size': 1500, 'color': COLORS['event'], 'type': 'Event'},
        'CPI': {'pos': (-4, -6), 'size': 1500, 'color': COLORS['indicator'], 'type': 'Indicator'},
        'GDP': {'pos': (4, -6), 'size': 1500, 'color': COLORS['indicator'], 'type': 'Indicator'},
        'Earnings': {'pos': (0, 6), 'size': 1500, 'color': COLORS['event'], 'type': 'Event'},
    }

    # Add nodes to graph
    for node, attrs in nodes.items():
        G.add_node(node, **attrs)

    # Add edges (relationships)
    edges = [
        # Market to sectors
        ('USA_Market', 'Technology', 1.0),
        ('USA_Market', 'Finance', 1.0),
        ('USA_Market', 'Healthcare', 1.0),
        ('USA_Market', 'Energy', 1.0),
        ('USA_Market', 'Consumer', 1.0),
        ('USA_Market', 'Industrial', 1.0),

        # Sectors to stocks
        ('Technology', 'AAPL', 0.9),
        ('Technology', 'NVDA', 0.95),
        ('Technology', 'GOOGL', 0.85),
        ('Finance', 'JPM', 0.9),
        ('Healthcare', 'JNJ', 0.9),
        ('Energy', 'XOM', 0.95),
        ('Consumer', 'WMT', 0.9),
        ('Industrial', 'CAT', 0.9),

        # Events/Indicators to market
        ('Fed_Rate', 'USA_Market', 0.85),
        ('CPI', 'USA_Market', 0.75),
        ('GDP', 'USA_Market', 0.7),
        ('Earnings', 'USA_Market', 0.8),

        # Cross-sector correlations
        ('Technology', 'Finance', 0.6),
        ('Energy', 'Industrial', 0.7),
        ('AAPL', 'NVDA', 0.75),
    ]

    for src, dst, weight in edges:
        G.add_edge(src, dst, weight=weight)

    # Draw edges with varying thickness and transparency
    for edge in G.edges(data=True):
        src, dst, data = edge
        weight = data.get('weight', 0.5)
        src_pos = nodes[src]['pos']
        dst_pos = nodes[dst]['pos']

        arrow = FancyArrowPatch(
            src_pos, dst_pos,
            arrowstyle='-',
            linewidth=weight * 2,
            color='#888888',
            alpha=0.3 + weight * 0.3,
            connectionstyle='arc3,rad=0.1',
            zorder=1
        )
        ax.add_patch(arrow)

    # Draw nodes with Neo4j-style circles
    for node, attrs in nodes.items():
        pos = attrs['pos']
        size = attrs['size']
        color = attrs['color']
        node_type = attrs['type']

        # Outer ring for emphasis
        circle_outer = Circle(pos, radius=np.sqrt(size/np.pi) * 0.035,
                             color=color, alpha=0.2, zorder=2)
        ax.add_patch(circle_outer)

        # Main node circle
        circle = Circle(pos, radius=np.sqrt(size/np.pi) * 0.025,
                       color=color, alpha=0.9, zorder=3,
                       edgecolor='white', linewidth=2)
        ax.add_patch(circle)

        # Add heat glow for stock nodes
        if node_type == 'Stock' and 'heat' in attrs:
            heat = attrs['heat']
            glow = Circle(pos, radius=np.sqrt(size/np.pi) * 0.045,
                         color='red', alpha=heat * 0.3, zorder=1)
            ax.add_patch(glow)

        # Add labels
        label_offset = 0.7 if node_type in ['Stock', 'Event', 'Indicator'] else 0.5
        ax.text(pos[0], pos[1] - label_offset, node,
               ha='center', va='top', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                        edgecolor=color, alpha=0.8), zorder=4)

        # Add property annotations for key nodes
        if node == 'AAPL':
            ax.text(pos[0] + 1.2, pos[1], 'Price: $175.43\nHeat: 0.85\nVolume: 45.2M',
                   fontsize=7, bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='lightyellow', alpha=0.9), zorder=4)
        elif node == 'USA_Market':
            ax.text(pos[0], pos[1] + 0.8, 'S&P 500: 4,567\nRegime: Bull',
                   ha='center', fontsize=7,
                   bbox=dict(boxstyle='round,pad=0.4',
                   facecolor='lightblue', alpha=0.9), zorder=4)

    # Add legend
    legend_elements = [
        mpatches.Patch(color=COLORS['primary'], label='Market', alpha=0.9),
        mpatches.Patch(color=COLORS['sector'], label='Sector', alpha=0.9),
        mpatches.Patch(color=COLORS['stock'], label='Stock', alpha=0.9),
        mpatches.Patch(color=COLORS['event'], label='Event', alpha=0.9),
        mpatches.Patch(color=COLORS['indicator'], label='Indicator', alpha=0.9),
    ]
    ax.legend(handles=legend_elements, loc='upper right', framealpha=0.95)

    # Styling
    ax.set_xlim(-8, 9)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('RAGHeat Financial Knowledge Graph\n(Neo4j-Style Visualization with Heat Scores)',
                fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('ragheat_knowledge_graph_neo4j.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: ragheat_knowledge_graph_neo4j.png")
    plt.close()


def create_system_architecture():
    """Generate comprehensive system architecture diagram"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'RAGHeat System Architecture', ha='center', va='top',
           fontsize=14, fontweight='bold')

    # Layer 1: Data Sources (top)
    sources = [
        ('Yahoo\nFinance', 1, 8.5, COLORS['primary']),
        ('SEC\nEDGAR', 2.8, 8.5, COLORS['secondary']),
        ('Social\nMedia', 4.6, 8.5, COLORS['success']),
        ('FRED\nAPI', 6.4, 8.5, COLORS['warning']),
        ('News\nFeeds', 8.2, 8.5, COLORS['info']),
        ('Options\nData', 10, 8.5, COLORS['light']),
        ('Market\nData', 11.8, 8.5, COLORS['danger']),
    ]

    for name, x, y, color in sources:
        box = FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.8, boxstyle='round,pad=0.1',
                            facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.7)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    # Apache Kafka (data ingestion)
    kafka_box = FancyBboxPatch((2, 7), 9, 0.6, boxstyle='round,pad=0.05',
                              facecolor='#231F20', edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(kafka_box)
    ax.text(6.5, 7.3, 'Apache Kafka - Real-time Data Ingestion',
           ha='center', va='center', fontsize=10, fontweight='bold', color='white')

    # Layer 2: Processing Pipeline
    processing = [
        ('NER +\nSentiment\n(FinBERT)', 2, 5.8, COLORS['primary'], 1.5),
        ('Triple\nExtraction\n(OpenIE)', 5, 5.8, COLORS['secondary'], 1.5),
        ('Text\nEmbedding\n(SBERT)', 8, 5.8, COLORS['success'], 1.5),
        ('Knowledge\nGraph\nConstruction', 11, 5.8, COLORS['warning'], 1.5),
    ]

    for name, x, y, color, width in processing:
        box = FancyBboxPatch((x-width/2, y-0.5), width, 1, boxstyle='round,pad=0.1',
                            facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.75)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    # Layer 3: Storage Layer
    storage = [
        ('Neo4j\nGraph DB', 2.5, 4, COLORS['primary'], 2),
        ('PostgreSQL\nTime Series', 6, 4, COLORS['secondary'], 2),
        ('FAISS\nVector Store', 9.5, 4, COLORS['success'], 2),
    ]

    for name, x, y, color, width in storage:
        box = FancyBboxPatch((x-width/2, y-0.4), width, 0.8, boxstyle='round,pad=0.1',
                            facecolor=color, edgecolor='black', linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold', color='white')

    # Layer 4: ML/Processing Layer
    ml_layer = [
        ('Heat Diffusion\nEngine\n(Graph Laplacian)', 2.5, 2.3, COLORS['danger'], 2.2),
        ('GAT Layer\n(Heat-Biased\nAttention)', 6, 2.3, COLORS['warning'], 2.2),
        ('Hybrid Retriever\n(Graph + Vector\n+ Heat)', 9.5, 2.3, COLORS['info'], 2.2),
    ]

    for name, x, y, color, width in ml_layer:
        box = FancyBboxPatch((x-width/2, y-0.6), width, 1.2, boxstyle='round,pad=0.1',
                            facecolor=color, edgecolor='black', linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    # Layer 5: LLM Reasoning
    llm_box = FancyBboxPatch((2.5, 0.6), 9, 0.8, boxstyle='round,pad=0.05',
                            facecolor=COLORS['light'], edgecolor='black', linewidth=2, alpha=0.85)
    ax.add_patch(llm_box)
    ax.text(7, 1, 'LLM Reasoning Layer (GPT-4 / FinGPT)\nChain-of-Thought Generation',
           ha='center', va='center', fontsize=9, fontweight='bold')

    # Layer 6: Output
    output = [
        ('REST API', 3.5, 0, COLORS['primary'], 1.8),
        ('Streamlit UI', 7, 0, COLORS['secondary'], 1.8),
        ('D3.js Viz', 10.5, 0, COLORS['success'], 1.8),
    ]

    for name, x, y, color, width in output:
        box = FancyBboxPatch((x-width/2, y-0.3), width, 0.6, boxstyle='round,pad=0.05',
                            facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

    # Add connecting arrows
    arrow_props = dict(arrowstyle='->', lw=2, color='#555555', alpha=0.6)

    # Sources to Kafka
    for name, x, y, color in sources:
        ax.annotate('', xy=(x, 7.6), xytext=(x, y-0.4), arrowprops=arrow_props)

    # Kafka to Processing
    for name, x, y, color, width in processing:
        ax.annotate('', xy=(x, y+0.5), xytext=(6.5, 7), arrowprops=arrow_props)

    # Processing to Storage
    ax.annotate('', xy=(2.5, 4.4), xytext=(2, 5.3), arrowprops=arrow_props)
    ax.annotate('', xy=(6, 4.4), xytext=(5, 5.3), arrowprops=arrow_props)
    ax.annotate('', xy=(9.5, 4.4), xytext=(8, 5.3), arrowprops=arrow_props)

    # Storage to ML Layer
    for name, x, y, color, width in storage:
        for ml_name, ml_x, ml_y, ml_color, ml_width in ml_layer:
            ax.annotate('', xy=(ml_x, ml_y+0.6), xytext=(x, y-0.4),
                       arrowprops=dict(arrowstyle='->', lw=1, color='#888888', alpha=0.3))

    # ML to LLM
    for name, x, y, color, width in ml_layer:
        ax.annotate('', xy=(7, 1.4), xytext=(x, y-0.6), arrowprops=arrow_props)

    # LLM to Output
    for name, x, y, color, width in output:
        ax.annotate('', xy=(x, y+0.3), xytext=(7, 0.6), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig('ragheat_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: ragheat_architecture.png")
    plt.close()


def create_heat_diffusion_flow():
    """Generate heat diffusion temporal flow visualization"""
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    # Time steps
    time_steps = ['t=0\n(Event)', 't=1\n(Immediate)', 't=3\n(Propagation)', 't=5\n(Equilibrium)']

    # Network structure
    G = nx.Graph()
    pos = {
        'Fed': (0, 2),
        'Market': (2, 2),
        'Tech': (1, 3.5),
        'Finance': (3, 3.5),
        'AAPL': (0.5, 5),
        'NVDA': (1.5, 5),
        'JPM': (2.5, 5),
        'MS': (3.5, 5),
    }

    edges = [
        ('Fed', 'Market'),
        ('Market', 'Tech'),
        ('Market', 'Finance'),
        ('Tech', 'AAPL'),
        ('Tech', 'NVDA'),
        ('Finance', 'JPM'),
        ('Finance', 'MS'),
        ('AAPL', 'NVDA'),
        ('JPM', 'MS'),
    ]

    G.add_edges_from(edges)

    # Heat values at different time steps
    heat_evolution = [
        # t=0: Event at Fed
        {'Fed': 1.0, 'Market': 0.0, 'Tech': 0.0, 'Finance': 0.0,
         'AAPL': 0.0, 'NVDA': 0.0, 'JPM': 0.0, 'MS': 0.0},
        # t=1: Immediate propagation
        {'Fed': 0.8, 'Market': 0.7, 'Tech': 0.2, 'Finance': 0.2,
         'AAPL': 0.0, 'NVDA': 0.0, 'JPM': 0.0, 'MS': 0.0},
        # t=3: Further propagation
        {'Fed': 0.5, 'Market': 0.6, 'Tech': 0.5, 'Finance': 0.5,
         'AAPL': 0.3, 'NVDA': 0.3, 'JPM': 0.35, 'MS': 0.35},
        # t=5: Equilibrium
        {'Fed': 0.3, 'Market': 0.4, 'Tech': 0.4, 'Finance': 0.4,
         'AAPL': 0.38, 'NVDA': 0.38, 'JPM': 0.42, 'MS': 0.42},
    ]

    for idx, (ax, t_step, heats) in enumerate(zip(axes, time_steps, heat_evolution)):
        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#888888',
                              width=2, alpha=0.4)

        # Draw nodes with heat-based coloring
        node_colors = [heats[node] for node in G.nodes()]
        nodes = nx.draw_networkx_nodes(G, pos, ax=ax,
                                       node_color=node_colors,
                                       cmap='hot', vmin=0, vmax=1,
                                       node_size=800,
                                       edgecolors='black', linewidths=2)

        # Draw labels
        labels = {node: f'{node}\n{heats[node]:.2f}' for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, ax=ax, font_size=8, font_weight='bold')

        ax.set_title(t_step, fontsize=11, fontweight='bold')
        ax.axis('off')
        ax.set_xlim(-0.5, 4)
        ax.set_ylim(1, 5.5)

    # Add colorbar
    cbar = plt.colorbar(nodes, ax=axes, orientation='horizontal',
                       pad=0.05, fraction=0.05, aspect=50)
    cbar.set_label('Heat Score (Influence Magnitude)', fontsize=10)

    fig.suptitle('Heat Diffusion Process: Federal Reserve Rate Hike Impact Propagation',
                fontsize=13, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig('heat_diffusion_flow.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: heat_diffusion_flow.png")
    plt.close()


def create_data_flow_pipeline():
    """Generate detailed data flow pipeline diagram"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7, 7.5, 'RAGHeat Query Processing Pipeline', ha='center', va='top',
           fontsize=14, fontweight='bold')

    # User Query Input
    input_box = FancyBboxPatch((0.5, 6.5), 2, 0.8, boxstyle='round,pad=0.1',
                              facecolor=COLORS['primary'], edgecolor='black',
                              linewidth=2, alpha=0.85)
    ax.add_patch(input_box)
    ax.text(1.5, 6.9, 'User Query', ha='center', va='center',
           fontsize=10, fontweight='bold', color='white')
    ax.text(1.5, 6.6, '"Tech stocks\nafter rate hike"', ha='center', va='center',
           fontsize=7, color='white', style='italic')

    # Query Parsing
    parse_box = FancyBboxPatch((3.5, 6.5), 1.8, 0.8, boxstyle='round,pad=0.1',
                              facecolor=COLORS['secondary'], edgecolor='black',
                              linewidth=2, alpha=0.85)
    ax.add_patch(parse_box)
    ax.text(4.4, 6.9, 'NER + Parse', ha='center', va='center',
           fontsize=9, fontweight='bold', color='white')

    # Parallel Retrieval Branches
    branch_y = 4.5
    branches = [
        ('Graph\nTraversal\n(Neo4j)', 1.5, branch_y, COLORS['success'], 1.5),
        ('Vector\nSearch\n(FAISS)', 4.4, branch_y, COLORS['warning'], 1.5),
        ('Heat\nScoring\n(Diffusion)', 7.3, branch_y, COLORS['danger'], 1.5),
    ]

    for name, x, y, color, width in branches:
        box = FancyBboxPatch((x-width/2, y-0.5), width, 1, boxstyle='round,pad=0.1',
                            facecolor=color, edgecolor='black', linewidth=2, alpha=0.85)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center',
               fontsize=9, fontweight='bold', color='white')

    # Results from branches
    results = [
        ('Graph Paths\n& Nodes', 1.5, 3, COLORS['success'], 1.5),
        ('Relevant\nDocuments', 4.4, 3, COLORS['warning'], 1.5),
        ('Heat-Ranked\nEntities', 7.3, 3, COLORS['danger'], 1.5),
    ]

    for name, x, y, color, width in results:
        box = FancyBboxPatch((x-width/2, y-0.4), width, 0.8, boxstyle='round,pad=0.05',
                            facecolor=color, edgecolor='black', linewidth=1.5, alpha=0.7)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center',
               fontsize=8, fontweight='bold', color='white')

    # Score Fusion
    fusion_box = FancyBboxPatch((2.5, 1.5), 4, 0.8, boxstyle='round,pad=0.1',
                               facecolor=COLORS['info'], edgecolor='black',
                               linewidth=2, alpha=0.85)
    ax.add_patch(fusion_box)
    ax.text(4.5, 1.9, 'Hybrid Score Fusion', ha='center', va='center',
           fontsize=10, fontweight='bold', color='white')
    ax.text(4.5, 1.6, r'S = 0.4·S_sem + 0.3·S_struct + 0.3·S_heat',
           ha='center', va='center', fontsize=7, color='white')

    # Context Assembly
    context_box = FancyBboxPatch((8.5, 5.5), 2.5, 2, boxstyle='round,pad=0.1',
                                facecolor=COLORS['light'], edgecolor='black',
                                linewidth=2, alpha=0.85)
    ax.add_patch(context_box)
    ax.text(9.75, 6.8, 'Context Assembly', ha='center', va='top',
           fontsize=9, fontweight='bold')
    ax.text(9.75, 6.4, '• Top-10 docs\n• Graph subgraph\n• Heat map\n• Event chains',
           ha='center', va='top', fontsize=7)

    # LLM Generation
    llm_box = FancyBboxPatch((8.5, 3.5), 2.5, 1.2, boxstyle='round,pad=0.1',
                            facecolor=COLORS['primary'], edgecolor='black',
                            linewidth=2, alpha=0.85)
    ax.add_patch(llm_box)
    ax.text(9.75, 4.3, 'LLM Generation', ha='center', va='center',
           fontsize=10, fontweight='bold', color='white')
    ax.text(9.75, 3.9, 'Chain-of-Thought\nReasoning', ha='center', va='center',
           fontsize=7, color='white')

    # Output
    output_box = FancyBboxPatch((11.5, 5), 2, 3, boxstyle='round,pad=0.1',
                               facecolor=COLORS['secondary'], edgecolor='black',
                               linewidth=2, alpha=0.85)
    ax.add_patch(output_box)
    ax.text(12.5, 7.5, 'Output', ha='center', va='top',
           fontsize=10, fontweight='bold', color='white')
    ax.text(12.5, 7, '✓ Ranked stocks\n✓ Explanations\n✓ Heat viz\n✓ Confidence\n✓ Citations',
           ha='center', va='top', fontsize=7, color='white')

    # Arrows
    arrow_props = dict(arrowstyle='->', lw=2.5, color='#333333')

    # Input to Parse
    ax.annotate('', xy=(3.5, 6.9), xytext=(2.5, 6.9), arrowprops=arrow_props)

    # Parse to branches
    for name, x, y, color, width in branches:
        ax.annotate('', xy=(x, y+0.5), xytext=(4.4, 6.5),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#555555'))

    # Branches to results
    for (bn, bx, by, bc, bw), (rn, rx, ry, rc, rw) in zip(branches, results):
        ax.annotate('', xy=(rx, ry+0.4), xytext=(bx, by-0.5),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#555555'))

    # Results to fusion
    for name, x, y, color, width in results:
        ax.annotate('', xy=(4.5, 2.3), xytext=(x, y-0.4),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='#555555'))

    # Fusion to context
    ax.annotate('', xy=(8.5, 6.5), xytext=(6.5, 1.9),
               arrowprops=arrow_props)

    # Context to LLM
    ax.annotate('', xy=(9.75, 4.7), xytext=(9.75, 5.5),
               arrowprops=arrow_props)

    # LLM to Output
    ax.annotate('', xy=(11.5, 6.5), xytext=(11, 4.1),
               arrowprops=arrow_props)

    # Add timing annotations
    ax.text(2, 7.3, '~45ms', ha='center', fontsize=7, color='red', fontweight='bold')
    ax.text(5.5, 5.5, '~120ms', ha='center', fontsize=7, color='red', fontweight='bold')
    ax.text(5.5, 2.5, '~85ms', ha='center', fontsize=7, color='red', fontweight='bold')
    ax.text(10.5, 5, '~1.2s', ha='center', fontsize=7, color='red', fontweight='bold')
    ax.text(13.8, 4, 'Total: ~1.6s', ha='center', fontsize=8,
           color='red', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

    plt.tight_layout()
    plt.savefig('data_flow_pipeline.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: data_flow_pipeline.png")
    plt.close()


def create_performance_comparison():
    """Generate performance comparison charts"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    models = ['Collab\nFilter', 'Vanilla\nRAG', 'GAT\nOnly', 'GNN+\nText', 'FinBERT\nRAG', 'RAGHeat\n(Ours)']

    # nDCG@5 comparison
    ndcg5 = [0.421, 0.556, 0.598, 0.631, 0.647, 0.801]
    bars = axes[0, 0].bar(models, ndcg5, color=[COLORS['dark']]*5 + [COLORS['primary']],
                          edgecolor='black', linewidth=1.5, alpha=0.85)
    bars[-1].set_edgecolor(COLORS['danger'])
    bars[-1].set_linewidth(3)
    axes[0, 0].set_ylabel('nDCG@5', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Ranking Performance (nDCG@5)', fontsize=12, fontweight='bold')
    axes[0, 0].grid(axis='y', alpha=0.3, linestyle='--')
    axes[0, 0].set_ylim(0, 0.9)

    # Add value labels on bars
    for bar, val in zip(bars, ndcg5):
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                       f'{val:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # MRR comparison
    mrr = [0.385, 0.521, 0.562, 0.598, 0.612, 0.769]
    bars = axes[0, 1].bar(models, mrr, color=[COLORS['dark']]*5 + [COLORS['secondary']],
                          edgecolor='black', linewidth=1.5, alpha=0.85)
    bars[-1].set_edgecolor(COLORS['danger'])
    bars[-1].set_linewidth(3)
    axes[0, 1].set_ylabel('Mean Reciprocal Rank', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Mean Reciprocal Rank (MRR)', fontsize=12, fontweight='bold')
    axes[0, 1].grid(axis='y', alpha=0.3, linestyle='--')
    axes[0, 1].set_ylim(0, 0.9)

    for bar, val in zip(bars, mrr):
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                       f'{val:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Explanation Quality (grouped bar)
    exp_models = ['Vanilla\nRAG', 'GNN+\nText', 'FinBERT\nRAG', 'RAGHeat']
    coherence = [3.2, 2.9, 3.5, 4.2]
    faithfulness = [2.8, 3.1, 3.3, 4.1]
    usefulness = [2.9, 2.7, 3.4, 4.3]

    x = np.arange(len(exp_models))
    width = 0.25

    bars1 = axes[1, 0].bar(x - width, coherence, width, label='Coherence',
                          color=COLORS['success'], edgecolor='black', linewidth=1, alpha=0.85)
    bars2 = axes[1, 0].bar(x, faithfulness, width, label='Faithfulness',
                          color=COLORS['warning'], edgecolor='black', linewidth=1, alpha=0.85)
    bars3 = axes[1, 0].bar(x + width, usefulness, width, label='Usefulness',
                          color=COLORS['info'], edgecolor='black', linewidth=1, alpha=0.85)

    axes[1, 0].set_ylabel('Score (1-5 scale)', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Explanation Quality (Human Evaluation)', fontsize=12, fontweight='bold')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(exp_models)
    axes[1, 0].legend(loc='upper left', framealpha=0.95)
    axes[1, 0].grid(axis='y', alpha=0.3, linestyle='--')
    axes[1, 0].set_ylim(0, 5)

    # Ablation study
    ablation_models = ['Full\nModel', '- Heat\nDiff', '- GAT\nLayer', '- Hybrid\nRetr', 'Sem.\nOnly', 'Graph\nOnly']
    ablation_ndcg = [0.801, 0.732, 0.709, 0.748, 0.651, 0.713]
    ablation_exp = [4.2, 3.8, 3.9, 3.7, 3.2, 3.5]

    x2 = np.arange(len(ablation_models))
    width2 = 0.35

    bars1 = axes[1, 1].bar(x2 - width2/2, ablation_ndcg, width2, label='nDCG@5',
                          color=COLORS['primary'], edgecolor='black', linewidth=1.5, alpha=0.85)
    bars1[0].set_edgecolor(COLORS['danger'])
    bars1[0].set_linewidth(3)

    ax2 = axes[1, 1].twinx()
    bars2 = ax2.bar(x2 + width2/2, ablation_exp, width2, label='Explanation',
                   color=COLORS['secondary'], edgecolor='black', linewidth=1.5, alpha=0.85)
    bars2[0].set_edgecolor(COLORS['danger'])
    bars2[0].set_linewidth(3)

    axes[1, 1].set_ylabel('nDCG@5', fontsize=11, fontweight='bold', color=COLORS['primary'])
    ax2.set_ylabel('Explanation Score', fontsize=11, fontweight='bold', color=COLORS['secondary'])
    axes[1, 1].set_title('Ablation Study Results', fontsize=12, fontweight='bold')
    axes[1, 1].set_xticks(x2)
    axes[1, 1].set_xticklabels(ablation_models, fontsize=8)
    axes[1, 1].tick_params(axis='y', labelcolor=COLORS['primary'])
    ax2.tick_params(axis='y', labelcolor=COLORS['secondary'])
    axes[1, 1].grid(axis='y', alpha=0.3, linestyle='--')
    axes[1, 1].set_ylim(0.6, 0.85)
    ax2.set_ylim(2.5, 4.5)

    # Combined legend
    lines1, labels1 = axes[1, 1].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    axes[1, 1].legend(lines1 + lines2, labels1 + labels2, loc='lower left', framealpha=0.95)

    plt.suptitle('RAGHeat Performance Analysis', fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: performance_comparison.png")
    plt.close()


def create_gat_attention_mechanism():
    """Generate GAT attention mechanism with heat bias visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Standard GAT
    ax1.text(0.5, 0.95, 'Standard GAT Attention', ha='center', va='top',
            transform=ax1.transAxes, fontsize=12, fontweight='bold')

    # Center node
    center = Circle((0.5, 0.5), 0.08, color=COLORS['primary'],
                   edgecolor='black', linewidth=2, zorder=10)
    ax1.add_patch(center)
    ax1.text(0.5, 0.5, 'i', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white', zorder=11)

    # Neighbor nodes (standard attention)
    neighbors_std = [
        (0.2, 0.8, 'j₁', 0.45, COLORS['secondary']),
        (0.8, 0.8, 'j₂', 0.25, COLORS['success']),
        (0.2, 0.2, 'j₃', 0.15, COLORS['warning']),
        (0.8, 0.2, 'j₄', 0.15, COLORS['info']),
    ]

    for x, y, label, attn, color in neighbors_std:
        node = Circle((x, y), 0.06, color=color, edgecolor='black',
                     linewidth=1.5, alpha=0.8, zorder=10)
        ax1.add_patch(node)
        ax1.text(x, y, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', zorder=11)

        # Attention arrow
        arrow = FancyArrowPatch((x, y), (0.5, 0.5),
                               arrowstyle='->', mutation_scale=20,
                               linewidth=attn * 8, color=color, alpha=0.6,
                               zorder=5)
        ax1.add_patch(arrow)

        # Attention weight label
        mid_x, mid_y = (x + 0.5) / 2, (y + 0.5) / 2
        ax1.text(mid_x, mid_y, f'α={attn:.2f}',
                fontsize=8, bbox=dict(boxstyle='round,pad=0.2',
                facecolor='white', alpha=0.9), zorder=12)

    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # Right: Heat-biased GAT
    ax2.text(0.5, 0.95, 'RAGHeat: Heat-Biased GAT', ha='center', va='top',
            transform=ax2.transAxes, fontsize=12, fontweight='bold')

    # Center node
    center2 = Circle((0.5, 0.5), 0.08, color=COLORS['primary'],
                    edgecolor='black', linewidth=2, zorder=10)
    ax2.add_patch(center2)
    ax2.text(0.5, 0.5, 'i', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white', zorder=11)

    # Neighbor nodes (heat-biased attention)
    neighbors_heat = [
        (0.2, 0.8, 'j₁', 0.50, 0.85, COLORS['secondary']),  # High heat
        (0.8, 0.8, 'j₂', 0.30, 0.45, COLORS['success']),    # Medium heat
        (0.2, 0.2, 'j₃', 0.15, 0.15, COLORS['warning']),    # Low heat
        (0.8, 0.2, 'j₄', 0.05, 0.10, COLORS['info']),       # Low heat
    ]

    for x, y, label, attn, heat, color in neighbors_heat:
        # Heat glow
        glow = Circle((x, y), 0.12, color='red', alpha=heat * 0.4, zorder=8)
        ax2.add_patch(glow)

        node = Circle((x, y), 0.06, color=color, edgecolor='black',
                     linewidth=1.5, alpha=0.8, zorder=10)
        ax2.add_patch(node)
        ax2.text(x, y, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white', zorder=11)

        # Attention arrow (thicker for high heat)
        arrow = FancyArrowPatch((x, y), (0.5, 0.5),
                               arrowstyle='->', mutation_scale=20,
                               linewidth=attn * 10, color=color, alpha=0.7,
                               zorder=5)
        ax2.add_patch(arrow)

        # Attention weight and heat labels
        mid_x, mid_y = (x + 0.5) / 2, (y + 0.5) / 2
        ax2.text(mid_x, mid_y, f'α={attn:.2f}\nh={heat:.2f}',
                fontsize=7, ha='center',
                bbox=dict(boxstyle='round,pad=0.2',
                facecolor='lightyellow', alpha=0.95), zorder=12)

    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.axis('off')

    # Add formula annotations
    formula1 = r'$\alpha_{ij} = \frac{\exp(LeakyReLU(\mathbf{a}^T[\mathbf{Wh}_i || \mathbf{Wh}_j]))}{\sum_{k} \exp(...)}$'
    ax1.text(0.5, 0.05, formula1, ha='center', va='bottom',
            transform=ax1.transAxes, fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

    formula2 = r'$\alpha_{ij} = \frac{\exp(LeakyReLU(...) + \lambda \cdot s_j)}{\sum_{k} \exp(...)}$'
    ax2.text(0.5, 0.05, formula2, ha='center', va='bottom',
            transform=ax2.transAxes, fontsize=9,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))

    plt.suptitle('Graph Attention Network: Standard vs Heat-Biased',
                fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('gat_attention_mechanism.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: gat_attention_mechanism.png")
    plt.close()


def create_temporal_heat_evolution():
    """Generate temporal heat evolution visualization"""
    fig, ax = plt.subplots(figsize=(12, 7))

    # Time series data
    time_hours = np.linspace(0, 24, 100)

    # Different decay rates for different event types
    events = {
        'Fed Rate Hike': {'start': 2, 'initial': 1.0, 'decay': 0.05, 'color': COLORS['primary']},
        'Earnings Miss': {'start': 6, 'initial': 0.85, 'decay': 0.15, 'color': COLORS['danger']},
        'News Article': {'start': 10, 'initial': 0.6, 'decay': 0.5, 'color': COLORS['secondary']},
        'Social Media': {'start': 14, 'initial': 0.4, 'decay': 0.8, 'color': COLORS['success']},
    }

    for event_name, params in events.items():
        start = params['start']
        initial = params['initial']
        decay = params['decay']
        color = params['color']

        # Calculate heat evolution
        heat = np.zeros_like(time_hours)
        for i, t in enumerate(time_hours):
            if t >= start:
                heat[i] = initial * np.exp(-decay * (t - start))

        # Plot with smooth curve
        ax.plot(time_hours, heat, linewidth=2.5, label=event_name,
               color=color, alpha=0.85)

        # Fill under curve
        ax.fill_between(time_hours, 0, heat, alpha=0.15, color=color)

        # Mark event occurrence
        ax.axvline(x=start, color=color, linestyle='--', alpha=0.4, linewidth=1.5)
        ax.scatter([start], [initial], color=color, s=150, zorder=10,
                  edgecolor='black', linewidth=2)
        ax.text(start, initial + 0.08, f'{event_name}\n(γ={decay})',
               ha='center', va='bottom', fontsize=8,
               bbox=dict(boxstyle='round,pad=0.3', facecolor=color,
                        alpha=0.3, edgecolor=color))

    # Styling
    ax.set_xlabel('Time (hours)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Heat Score (Normalized Influence)', fontsize=12, fontweight='bold')
    ax.set_title('Temporal Heat Decay: Impact of Different Event Types\n' +
                r'$h(t) = h_0 \cdot e^{-\gamma t}$',
                fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='upper right', framealpha=0.95, fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 1.1)

    # Add decay rate annotations
    ax.text(0.98, 0.25, 'Decay Rates (γ):\n' +
           '• Structural (Fed): γ=0.05\n' +
           '• Fundamental: γ=0.15\n' +
           '• News: γ=0.5\n' +
           '• Social: γ=0.8',
           transform=ax.transAxes, ha='right', va='bottom',
           fontsize=9, bbox=dict(boxstyle='round,pad=0.5',
           facecolor='lightgray', alpha=0.9))

    plt.tight_layout()
    plt.savefig('temporal_heat_evolution.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Generated: temporal_heat_evolution.png")
    plt.close()


def main():
    """Generate all publication-ready images"""
    print("\n" + "="*70)
    print("RAGHeat World-Class Publication Image Generator")
    print("="*70 + "\n")

    print("Generating Neo4j-style knowledge graph...")
    create_neo4j_knowledge_graph()

    print("Generating system architecture diagram...")
    create_system_architecture()

    print("Generating heat diffusion flow visualization...")
    create_heat_diffusion_flow()

    print("Generating data flow pipeline diagram...")
    create_data_flow_pipeline()

    print("Generating performance comparison charts...")
    create_performance_comparison()

    print("Generating GAT attention mechanism visualization...")
    create_gat_attention_mechanism()

    print("Generating temporal heat evolution chart...")
    create_temporal_heat_evolution()

    print("\n" + "="*70)
    print("✓ All images generated successfully!")
    print("="*70)
    print("\nGenerated files:")
    print("  1. ragheat_knowledge_graph_neo4j.png")
    print("  2. ragheat_architecture.png")
    print("  3. heat_diffusion_flow.png")
    print("  4. data_flow_pipeline.png")
    print("  5. performance_comparison.png")
    print("  6. gat_attention_mechanism.png")
    print("  7. temporal_heat_evolution.png")
    print("\nAll images are publication-ready at 300 DPI")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
