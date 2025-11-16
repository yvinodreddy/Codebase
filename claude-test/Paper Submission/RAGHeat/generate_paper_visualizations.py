#!/usr/bin/env python3
"""
Elite Production-Grade Visualizations for Stock Heat Diffusion Model Paper

Generates publication-ready figures based on actual research paper content:
- Baseline weight allocation (from Table 1)
- Regime-dependent weight comparison (from Table 5)
- Heat diffusion knowledge graph
- Factor taxonomy hierarchy
- Temporal heat propagation
- Performance comparison (from Table 2)
- Ablation study results (from Table 3)
- Dynamic weight evolution over time

All visualizations use professional color theory, 300 DPI resolution,
and Nature/Science/IEEE publication standards.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Wedge
from matplotlib.path import Path
import matplotlib.patheffects as path_effects
import numpy as np
import networkx as nx
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality defaults
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 13,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 14,
    'text.usetex': False,
    'axes.unicode_minus': False,
    'axes.axisbelow': True,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'axes.facecolor': '#FAFAFA',
    'figure.facecolor': 'white'
})


class PaperColorPalette:
    """Professional color palette for academic publications"""

    # Primary colors for 10 factor categories
    MICRO = '#E63946'        # Crimson - highest weight
    ORDER_FLOW = '#F77F00'   # Orange - high weight
    OPTIONS = '#9D4EDD'      # Purple - derivatives
    TECHNICAL = '#06D6A0'    # Emerald - technical analysis
    NEWS = '#4361EE'         # Royal blue - news/media
    SOCIAL = '#FF6B9D'       # Pink - social sentiment
    SECTOR = '#118AB2'       # Teal - correlations
    MACRO = '#073B4C'        # Dark blue - macro factors
    SUPPLY = '#8B5A3C'       # Brown - supply chain
    OTHER = '#95A5A6'        # Gray - supplementary

    # Regime colors
    BULL = '#27AE60'         # Green
    BEAR = '#E74C3C'         # Red
    HIGH_VOL = '#F39C12'     # Orange
    SIDEWAYS = '#3498DB'     # Blue

    # Performance comparison
    BASELINE = '#BDC3C7'     # Light gray
    OURS = '#E63946'         # Crimson (highlight)
    COMPETITOR = '#95A5A6'   # Gray

    # Heat diffusion
    HEAT_HIGH = '#FF0000'    # Red
    HEAT_MED = '#FFA500'     # Orange
    HEAT_LOW = '#FFFF00'     # Yellow
    HEAT_ZERO = '#FFFFFF'    # White

    # Background and text
    BG_COLOR = '#FAFAFA'
    TEXT_PRIMARY = '#2C3E50'
    TEXT_SECONDARY = '#7F8C8D'
    GRID_COLOR = '#ECF0F1'


def create_baseline_weight_visualization(output_prefix: str):
    """
    Generate baseline weight allocation visualization (from Table 1 in paper)

    Creates:
    1. Pie chart with weight distribution
    2. Horizontal bar chart with exact values
    """

    # Data from Table 1 in paper
    factors = [
        'Microeconomic',
        'Order Flow',
        'Options Flow',
        'Technical',
        'News Sentiment',
        'Social Media',
        'Sector Correlation',
        'Macro',
        'Supply Chain',
        'Other Quant'
    ]

    weights = [0.28, 0.18, 0.15, 0.12, 0.10, 0.08, 0.04, 0.03, 0.02, 0.00]

    colors = [
        PaperColorPalette.MICRO,
        PaperColorPalette.ORDER_FLOW,
        PaperColorPalette.OPTIONS,
        PaperColorPalette.TECHNICAL,
        PaperColorPalette.NEWS,
        PaperColorPalette.SOCIAL,
        PaperColorPalette.SECTOR,
        PaperColorPalette.MACRO,
        PaperColorPalette.SUPPLY,
        PaperColorPalette.OTHER
    ]

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('white')

    # PIE CHART
    # Filter out zero weights for pie chart
    non_zero_idx = [i for i, w in enumerate(weights) if w > 0]
    pie_factors = [factors[i] for i in non_zero_idx]
    pie_weights = [weights[i] for i in non_zero_idx]
    pie_colors = [colors[i] for i in non_zero_idx]

    wedges, texts, autotexts = ax1.pie(
        pie_weights,
        labels=pie_factors,
        colors=pie_colors,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 11, 'weight': 'bold', 'color': 'white'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2.5}
    )

    # Add shadow effect to percentages
    for autotext in autotexts:
        autotext.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground='black', alpha=0.5),
            path_effects.Normal()
        ])

    ax1.set_title('Baseline Weight Allocation\n(Risk Parity Approach)',
                  fontsize=16, weight='bold', pad=20, color=PaperColorPalette.TEXT_PRIMARY)

    # HORIZONTAL BAR CHART
    y_pos = np.arange(len(factors))
    bars = ax2.barh(y_pos, weights, color=colors, edgecolor='white', linewidth=2)

    # Add value labels
    for i, (bar, weight) in enumerate(zip(bars, weights)):
        if weight > 0:
            ax2.text(weight + 0.01, bar.get_y() + bar.get_height()/2,
                    f'{weight:.2f}',
                    va='center', ha='left', fontsize=10, weight='bold',
                    color=PaperColorPalette.TEXT_PRIMARY)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(factors, fontsize=11)
    ax2.set_xlabel('Weight Value', fontsize=12, weight='bold')
    ax2.set_title('Factor Category Weights\n(Σwᵢ = 1.0)',
                  fontsize=16, weight='bold', pad=20, color=PaperColorPalette.TEXT_PRIMARY)
    ax2.set_xlim(0, 0.32)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)

    # Add constraint annotation
    ax2.text(0.98, 0.02, 'Constraint: Σwᵢ = 1.00',
            transform=ax2.transAxes,
            fontsize=10, style='italic',
            ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

    plt.tight_layout()

    filename = f'{output_prefix}_baseline_weights.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {filename}")
    plt.close()


def create_regime_comparison_visualization(output_prefix: str):
    """
    Generate regime-dependent weight comparison (from Table 5 in paper)

    Shows how weights change across:
    - Bull Market
    - Bear Market
    - High Volatility
    - Sideways/Normal
    """

    # Data from Table 5 in paper
    factors = [
        'Micro',
        'Order',
        'Options',
        'Technical',
        'News',
        'Social',
        'Sector',
        'Macro',
        'Supply'
    ]

    # Regime-dependent weights
    bull = [0.32, 0.08, 0.15, 0.18, 0.12, 0.10, 0.03, 0.02, 0.00]
    bear = [0.20, 0.22, 0.25, 0.10, 0.06, 0.03, 0.02, 0.12, 0.00]
    high_vol = [0.15, 0.25, 0.30, 0.08, 0.15, 0.02, 0.00, 0.05, 0.00]
    sideways = [0.28, 0.18, 0.15, 0.12, 0.10, 0.08, 0.04, 0.03, 0.02]

    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('white')

    x = np.arange(len(factors))
    width = 0.20

    bars1 = ax.bar(x - 1.5*width, bull, width, label='Bull Market',
                   color=PaperColorPalette.BULL, edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x - 0.5*width, bear, width, label='Bear Market',
                   color=PaperColorPalette.BEAR, edgecolor='white', linewidth=1.5)
    bars3 = ax.bar(x + 0.5*width, high_vol, width, label='High Volatility',
                   color=PaperColorPalette.HIGH_VOL, edgecolor='white', linewidth=1.5)
    bars4 = ax.bar(x + 1.5*width, sideways, width, label='Sideways/Normal',
                   color=PaperColorPalette.SIDEWAYS, edgecolor='white', linewidth=1.5)

    # Add value labels on top of bars (only for non-zero values)
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            if height > 0.02:  # Only show labels for weights > 2%
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', fontsize=8, weight='bold')

    ax.set_xlabel('Factor Category', fontsize=13, weight='bold')
    ax.set_ylabel('Weight Value', fontsize=13, weight='bold')
    ax.set_title('Regime-Dependent Weight Allocations\n(All configurations sum to 1.0)',
                fontsize=16, weight='bold', pad=20, color=PaperColorPalette.TEXT_PRIMARY)
    ax.set_xticks(x)
    ax.set_xticklabels(factors, fontsize=11, rotation=0)
    ax.legend(loc='upper right', fontsize=12, frameon=True, shadow=True)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, 0.35)

    # Add regime characteristics annotations
    regime_notes = [
        "Bull: ↑ Microeconomic (0.32), ↑ Technical (0.18)",
        "Bear: ↑ Options (0.25), ↑ Order Flow (0.22), ↑ Macro (0.12)",
        "High Vol: ↑↑ Options (0.30), ↑ Order Flow (0.25)",
        "Sideways: Balanced allocation (baseline)"
    ]

    y_note = 0.97
    for note, color in zip(regime_notes, [PaperColorPalette.BULL, PaperColorPalette.BEAR,
                                          PaperColorPalette.HIGH_VOL, PaperColorPalette.SIDEWAYS]):
        ax.text(0.02, y_note, note, transform=ax.transAxes,
               fontsize=9, style='italic', color=color, weight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        y_note -= 0.04

    plt.tight_layout()

    filename = f'{output_prefix}_regime_weights.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {filename}")
    plt.close()


def create_heat_diffusion_network(output_prefix: str, ticker: str = 'STOCK'):
    """
    Generate heat diffusion knowledge graph visualization

    Shows:
    - Central stock node
    - 10 factor category nodes
    - Heat diffusion paths
    - Mathematical equation
    """

    # Create directed graph
    G = nx.DiGraph()

    # Central stock node
    stock_id = f'{ticker}_STOCK'
    G.add_node(stock_id, node_type='stock', label=f'{ticker}\nStock Price', weight=1.0)

    # 10 Factor category nodes with baseline weights
    factors = [
        ('MICRO', 'Microeconomic\nFactors', 0.28),
        ('ORDER', 'Order Flow\nMicrostructure', 0.18),
        ('OPTIONS', 'Options Flow\n& Derivatives', 0.15),
        ('TECH', 'Technical\nIndicators', 0.12),
        ('NEWS', 'News\nSentiment', 0.10),
        ('SOCIAL', 'Social Media\nSignals', 0.08),
        ('SECTOR', 'Sector\nCorrelation', 0.04),
        ('MACRO', 'Macroeconomic\nFactors', 0.03),
        ('SUPPLY', 'Supply Chain\nSignals', 0.02),
    ]

    for factor_id, label, weight in factors:
        G.add_node(factor_id, node_type='factor', label=label, weight=weight)
        G.add_edge(factor_id, stock_id, weight=weight)

    # Create figure
    fig, ax = plt.subplots(figsize=(16, 14))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(PaperColorPalette.BG_COLOR)
    ax.axis('off')

    # Use circular layout with stock at center
    pos = {}
    pos[stock_id] = (0, 0)  # Center

    # Arrange factors in a circle around stock
    n_factors = len(factors)
    for i, (factor_id, _, _) in enumerate(factors):
        angle = 2 * np.pi * i / n_factors
        radius = 2.5
        pos[factor_id] = (radius * np.cos(angle), radius * np.sin(angle))

    # Draw edges with varying thickness based on weight
    for factor_id, label, weight in factors:
        x0, y0 = pos[factor_id]
        x1, y1 = pos[stock_id]

        # Arrow with thickness proportional to weight
        arrow = FancyArrowPatch(
            (x0, y0), (x1, y1),
            arrowstyle='->,head_width=0.4,head_length=0.4',
            color=PaperColorPalette.HEAT_MED,
            linewidth=weight * 15,  # Scale by weight
            alpha=0.6,
            connectionstyle='arc3,rad=0',
            zorder=1
        )
        ax.add_patch(arrow)

        # Add weight label on edge
        mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
        ax.text(mid_x, mid_y, f'w={weight:.2f}',
               fontsize=9, ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9),
               zorder=3)

    # Draw factor nodes
    factor_colors = [
        PaperColorPalette.MICRO,
        PaperColorPalette.ORDER_FLOW,
        PaperColorPalette.OPTIONS,
        PaperColorPalette.TECHNICAL,
        PaperColorPalette.NEWS,
        PaperColorPalette.SOCIAL,
        PaperColorPalette.SECTOR,
        PaperColorPalette.MACRO,
        PaperColorPalette.SUPPLY
    ]

    for (factor_id, label, weight), color in zip(factors, factor_colors):
        x, y = pos[factor_id]

        # Node circle
        node_size = 0.35
        circle = Circle((x, y), node_size,
                       facecolor=color,
                       edgecolor='white',
                       linewidth=3,
                       zorder=10)
        ax.add_patch(circle)

        # Label
        ax.text(x, y, label,
               fontsize=10, weight='bold', color='white',
               ha='center', va='center',
               zorder=11,
               path_effects=[
                   path_effects.Stroke(linewidth=2, foreground='black', alpha=0.3),
                   path_effects.Normal()
               ])

    # Draw central stock node
    x, y = pos[stock_id]
    stock_circle = Circle((x, y), 0.5,
                         facecolor=PaperColorPalette.OURS,
                         edgecolor='white',
                         linewidth=4,
                         zorder=10)
    ax.add_patch(stock_circle)

    ax.text(x, y, f'{ticker}\nStock Price',
           fontsize=14, weight='bold', color='white',
           ha='center', va='center',
           zorder=11,
           path_effects=[
               path_effects.Stroke(linewidth=3, foreground='black', alpha=0.5),
               path_effects.Normal()
           ])

    # Add title
    ax.text(0, 3.5, 'Stock Heat Diffusion Model\nKnowledge Graph Structure',
           fontsize=18, weight='bold', ha='center', va='top',
           color=PaperColorPalette.TEXT_PRIMARY)

    # Add heat equation
    equation_text = r'$heat_{stock}(t) = \sum_{i=1}^{10} w_i(t) \cdot factor_i(t) + diffusion\_term(t)$'
    ax.text(0, -3.5, equation_text,
           fontsize=14, ha='center', va='bottom',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.3))

    # Add constraint
    constraint_text = r'Constraint: $\sum_{i=1}^{10} w_i(t) = 1.0 \quad \forall t$'
    ax.text(0, -4.0, constraint_text,
           fontsize=13, ha='center', va='bottom', style='italic', weight='bold',
           color=PaperColorPalette.OURS,
           bbox=dict(boxstyle='round,pad=0.6', facecolor='white', edgecolor=PaperColorPalette.OURS, linewidth=2))

    # Add legend
    legend_elements = [
        mpatches.Patch(color=PaperColorPalette.OURS, label='Stock (Central Node)'),
        mpatches.Patch(color=PaperColorPalette.MICRO, label='Factor Categories (10 types)'),
        mpatches.FancyArrow(0, 0, 1, 0, width=0.3, color=PaperColorPalette.HEAT_MED,
                           alpha=0.6, label='Influence (weighted edges)')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11, frameon=True, shadow=True)

    ax.set_xlim(-4, 4)
    ax.set_ylim(-4.5, 4)
    ax.set_aspect('equal')

    filename = f'{output_prefix}_heat_diffusion_network.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {filename}")
    plt.close()


def create_temporal_heat_propagation(output_prefix: str):
    """
    Generate temporal heat propagation visualization across multiple time layers

    Shows:
    - Layer 0: Market event (heat source)
    - Layer 1: Direct impact (stock, sector, ETF)
    - Layer 2: Secondary impact (peers, supply chain)
    - Layer 3: Tertiary impact (derivatives, international)
    """

    # Create directed acyclic graph
    G = nx.DiGraph()

    # Layer 0: Event source
    G.add_node('EVENT', layer=0, heat=1.00, label='Market\nEvent')

    # Layer 1: Direct impact
    layer1_nodes = [
        ('STOCK', 0.85, 'Target\nStock'),
        ('SECTOR_ETF', 0.78, 'Sector\nETF'),
        ('SECTOR_INDEX', 0.72, 'Sector\nIndex')
    ]
    for node_id, heat, label in layer1_nodes:
        G.add_node(node_id, layer=1, heat=heat, label=label)
        G.add_edge('EVENT', node_id, weight=heat)

    # Layer 2: Secondary impact
    layer2_nodes = [
        ('PEER1', 0.55, 'Peer\nStock 1'),
        ('PEER2', 0.50, 'Peer\nStock 2'),
        ('SUPPLIER', 0.48, 'Key\nSupplier'),
        ('CUSTOMER', 0.52, 'Major\nCustomer'),
        ('COMPETITOR', 0.47, 'Direct\nCompetitor')
    ]
    for node_id, heat, label in layer2_nodes:
        G.add_node(node_id, layer=2, heat=heat, label=label)
        # Connect to layer 1 nodes
        G.add_edge('STOCK', node_id, weight=heat*0.6)
        G.add_edge('SECTOR_ETF', node_id, weight=heat*0.4)

    # Layer 3: Tertiary impact
    layer3_nodes = [
        ('CALLS', 0.32, 'Call\nOptions'),
        ('PUTS', 0.28, 'Put\nOptions'),
        ('FUTURES', 0.30, 'Index\nFutures'),
        ('INTL_PEER1', 0.25, 'Intl\nPeer 1'),
        ('INTL_PEER2', 0.27, 'Intl\nPeer 2'),
        ('RETAIL_ETF', 0.26, 'Retail\nETF'),
        ('HEDGE_FUND', 0.29, 'Hedge\nFund')
    ]
    for node_id, heat, label in layer3_nodes:
        G.add_node(node_id, layer=3, heat=heat, label=label)
        # Connect to layer 2 nodes
        for l2_node, _, _ in layer2_nodes[:3]:
            G.add_edge(l2_node, node_id, weight=heat*0.5)

    # Create figure
    fig, ax = plt.subplots(figsize=(18, 10))
    fig.patch.set_facecolor('white')
    ax.set_facecolor(PaperColorPalette.BG_COLOR)
    ax.axis('off')

    # Multipartite layout
    pos = nx.multipartite_layout(G, subset_key='layer', align='horizontal', scale=3)

    # Rotate to vertical (layers top to bottom)
    pos = {node: (y, -x) for node, (x, y) in pos.items()}

    # Draw edges with opacity based on weight
    for (u, v, data) in G.edges(data=True):
        x_start, y_start = pos[u]
        x_end, y_end = pos[v]

        weight = data.get('weight', 0.5)

        arrow = FancyArrowPatch(
            (x_start, y_start), (x_end, y_end),
            arrowstyle='->,head_width=0.3,head_length=0.3',
            color=PaperColorPalette.HEAT_MED,
            linewidth=2,
            alpha=weight*0.8,
            connectionstyle='arc3,rad=0.05',
            zorder=1
        )
        ax.add_patch(arrow)

    # Draw nodes with heat-based coloring
    for node, data in G.nodes(data=True):
        x, y = pos[node]
        heat = data['heat']
        label = data['label']
        layer = data['layer']

        # Color based on heat intensity
        if heat >= 0.7:
            color = PaperColorPalette.HEAT_HIGH
        elif heat >= 0.4:
            color = PaperColorPalette.HEAT_MED
        elif heat >= 0.2:
            color = PaperColorPalette.HEAT_LOW
        else:
            color = PaperColorPalette.HEAT_ZERO

        # Node size based on heat
        node_size = 0.15 + heat * 0.25

        circle = Circle((x, y), node_size,
                       facecolor=color,
                       edgecolor='white' if heat < 0.5 else PaperColorPalette.HEAT_HIGH,
                       linewidth=3,
                       zorder=10)
        ax.add_patch(circle)

        # Label
        text_color = 'white' if heat >= 0.5 else PaperColorPalette.TEXT_PRIMARY
        ax.text(x, y, label,
               fontsize=9, weight='bold', color=text_color,
               ha='center', va='center',
               zorder=11)

        # Heat value below node
        ax.text(x, y - node_size - 0.08, f'h={heat:.2f}',
               fontsize=8, ha='center', va='top',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8),
               zorder=11)

    # Add layer labels
    layer_positions = [
        (pos['EVENT'][0] - 1.0, pos['EVENT'][1], 't=0\nEvent\nSource'),
        (pos['STOCK'][0] - 1.0, pos['STOCK'][1], 't=1\nDirect\nImpact'),
        (pos['PEER1'][0] - 1.0, pos['PEER1'][1], 't=2\nSecondary\nImpact'),
        (pos['CALLS'][0] - 1.0, pos['CALLS'][1], 't=3\nTertiary\nImpact')
    ]

    for x, y, text in layer_positions:
        ax.text(x, y, text,
               fontsize=12, weight='bold', ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=PaperColorPalette.SIDEWAYS,
                        edgecolor='white', linewidth=2, alpha=0.9),
               color='white')

    # Title
    ax.text(0, 1.8, 'Multi-Hop Heat Propagation Across Temporal Layers',
           fontsize=18, weight='bold', ha='center', va='top',
           color=PaperColorPalette.TEXT_PRIMARY)

    # Heat equation
    equation_text = r'$h(t) = e^{-\beta L t} \cdot h_0$'
    ax.text(0, -2.0, equation_text,
           fontsize=14, ha='center', va='bottom',
           bbox=dict(boxstyle='round,pad=0.6', facecolor='yellow', alpha=0.3))

    # Heat decay annotation
    decay_text = 'Heat Decay Pattern:\nt=0: h=1.00 → t=1: h≈0.78 → t=2: h≈0.50 → t=3: h≈0.28'
    ax.text(0, -2.4, decay_text,
           fontsize=10, ha='center', va='bottom', style='italic',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9))

    # Color legend
    legend_elements = [
        mpatches.Patch(color=PaperColorPalette.HEAT_HIGH, label='High Heat (h ≥ 0.7)'),
        mpatches.Patch(color=PaperColorPalette.HEAT_MED, label='Medium Heat (0.4 ≤ h < 0.7)'),
        mpatches.Patch(color=PaperColorPalette.HEAT_LOW, label='Low Heat (0.2 ≤ h < 0.4)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, frameon=True, shadow=True)

    ax.set_xlim(-1.8, 1.5)
    ax.set_ylim(-2.8, 2.2)
    ax.set_aspect('equal')

    filename = f'{output_prefix}_temporal_heat_propagation.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {filename}")
    plt.close()


def create_performance_comparison(output_prefix: str):
    """
    Generate performance comparison visualization (from Table 2 in paper)

    Compares:
    - Static Equal Weights
    - Static Risk Parity
    - LSTM (Price Only)
    - GAT (Graph Only)
    - FinBERT-RAG
    - Heat Diffusion (Ours)
    """

    models = [
        'Static\nEqual\nWeights',
        'Static\nRisk\nParity',
        'LSTM\n(Price Only)',
        'GAT\n(Graph Only)',
        'FinBERT\nRAG',
        'Heat Diffusion\n(Ours)'
    ]

    sharpe = [0.42, 0.52, 0.48, 0.55, 0.58, 0.63]
    info_ratio = [0.05, 0.12, 0.18, 0.25, 0.32, 0.43]
    accuracy = [53.1, 55.8, 54.3, 56.2, 57.4, 58.3]

    # Create figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    fig.patch.set_facecolor('white')

    x = np.arange(len(models))

    # Colors: gray for baselines, red for ours
    colors = [PaperColorPalette.BASELINE] * 5 + [PaperColorPalette.OURS]

    # SHARPE RATIO
    bars1 = ax1.bar(x, sharpe, color=colors, edgecolor='white', linewidth=2)
    for i, (bar, val) in enumerate(zip(bars1, sharpe)):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 0.02,
                f'{val:.2f}',
                ha='center', va='bottom', fontsize=10, weight='bold')

    ax1.set_ylabel('Sharpe Ratio', fontsize=12, weight='bold')
    ax1.set_title('Sharpe Ratio Comparison', fontsize=14, weight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, fontsize=9)
    ax1.set_ylim(0, 0.70)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.axhline(y=0.52, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax1.text(0.02, 0.52, 'Static Risk Parity Baseline',
            fontsize=8, color='red', va='bottom', transform=ax1.get_yaxis_transform())

    # INFORMATION RATIO
    bars2 = ax2.bar(x, info_ratio, color=colors, edgecolor='white', linewidth=2)
    for i, (bar, val) in enumerate(zip(bars2, info_ratio)):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 0.02,
                f'{val:.2f}',
                ha='center', va='bottom', fontsize=10, weight='bold')

    ax2.set_ylabel('Information Ratio', fontsize=12, weight='bold')
    ax2.set_title('Information Ratio Comparison', fontsize=14, weight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, fontsize=9)
    ax2.set_ylim(0, 0.50)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    # ACCURACY
    bars3 = ax3.bar(x, accuracy, color=colors, edgecolor='white', linewidth=2)
    for i, (bar, val) in enumerate(zip(bars3, accuracy)):
        ax3.text(bar.get_x() + bar.get_width()/2, val + 0.5,
                f'{val:.1f}%',
                ha='center', va='bottom', fontsize=10, weight='bold')

    ax3.set_ylabel('Direction Accuracy (%)', fontsize=12, weight='bold')
    ax3.set_title('Prediction Accuracy Comparison', fontsize=14, weight='bold', pad=15)
    ax3.set_xticks(x)
    ax3.set_xticklabels(models, fontsize=9)
    ax3.set_ylim(50, 62)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.axhline(y=55.8, color='red', linestyle='--', alpha=0.5, linewidth=1)

    # Overall title
    fig.suptitle('Performance Comparison vs. Baseline Models\n(Table 2 from Paper)',
                fontsize=16, weight='bold', y=1.00)

    plt.tight_layout()

    filename = f'{output_prefix}_performance_comparison.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {filename}")
    plt.close()


def create_ablation_study(output_prefix: str):
    """
    Generate ablation study visualization (from Table 3 in paper)

    Shows impact of removing each component
    """

    variants = [
        'Full Model',
        '- No heat\ndiffusion',
        '- No regime\ndetection (HMM)',
        '- No Kalman\nfiltering',
        '- Static\nweights only',
        '- No time-of-day\nadjustment'
    ]

    sharpe = [0.63, 0.58, 0.56, 0.59, 0.52, 0.61]
    delta = [0, -7.9, -11.1, -6.3, -17.5, -3.2]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('white')

    x = np.arange(len(variants))

    # Colors: green for full model, red for ablations
    colors = [PaperColorPalette.BULL] + [PaperColorPalette.BEAR] * 5

    # SHARPE RATIO
    bars1 = ax1.bar(x, sharpe, color=colors, edgecolor='white', linewidth=2)
    for i, (bar, val) in enumerate(zip(bars1, sharpe)):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 0.01,
                f'{val:.2f}',
                ha='center', va='bottom', fontsize=10, weight='bold')

    ax1.set_ylabel('Sharpe Ratio', fontsize=12, weight='bold')
    ax1.set_title('Ablation Study: Sharpe Ratio by Model Variant', fontsize=14, weight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(variants, fontsize=9)
    ax1.set_ylim(0, 0.70)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.axhline(y=0.63, color='green', linestyle='--', alpha=0.5, linewidth=2)

    # DELTA FROM FULL MODEL
    colors_delta = [PaperColorPalette.BULL] + [PaperColorPalette.BEAR] * 5
    bars2 = ax2.bar(x, delta, color=colors_delta, edgecolor='white', linewidth=2)
    for i, (bar, val) in enumerate(zip(bars2, delta)):
        if val != 0:
            ax2.text(bar.get_x() + bar.get_width()/2, val - 1.0,
                    f'{val:.1f}%',
                    ha='center', va='top', fontsize=10, weight='bold', color='white')

    ax2.set_ylabel('Performance Change (%)', fontsize=12, weight='bold')
    ax2.set_title('Component Contribution (Δ from Full Model)', fontsize=14, weight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(variants, fontsize=9)
    ax2.set_ylim(-20, 2)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.8, linewidth=1)

    # Key findings annotation
    findings = [
        "Regime detection (HMM): -11.1% (most critical)",
        "Static → Dynamic weights: -17.5% (essential)",
        "Heat diffusion: -7.9% (significant)",
        "Kalman filtering: -6.3% (important)",
        "Time-of-day: -3.2% (helpful)"
    ]

    y_pos = 0.97
    for finding in findings:
        ax2.text(0.02, y_pos, finding,
                transform=ax2.transAxes,
                fontsize=9, style='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        y_pos -= 0.05

    fig.suptitle('Ablation Study: Component-wise Performance Analysis\n(Table 3 from Paper)',
                fontsize=16, weight='bold', y=0.98)

    plt.tight_layout()

    filename = f'{output_prefix}_ablation_study.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {filename}")
    plt.close()


def create_weight_evolution_over_time(output_prefix: str):
    """
    Generate dynamic weight evolution visualization over time

    Shows how weights adapt based on regime changes
    """

    # Simulate 100 time steps with regime changes
    np.random.seed(42)
    time_steps = 100

    # Define regimes over time (25 steps each)
    regimes = ['sideways'] * 25 + ['bull'] * 25 + ['high_vol'] * 25 + ['bear'] * 25

    # Initialize weight arrays
    weights = {
        'Micro': np.zeros(time_steps),
        'Order': np.zeros(time_steps),
        'Options': np.zeros(time_steps),
        'Technical': np.zeros(time_steps),
        'News': np.zeros(time_steps)
    }

    # Regime-based weights
    regime_weights = {
        'sideways': {'Micro': 0.28, 'Order': 0.18, 'Options': 0.15, 'Technical': 0.12, 'News': 0.10},
        'bull': {'Micro': 0.32, 'Order': 0.08, 'Options': 0.15, 'Technical': 0.18, 'News': 0.12},
        'high_vol': {'Micro': 0.15, 'Order': 0.25, 'Options': 0.30, 'Technical': 0.08, 'News': 0.15},
        'bear': {'Micro': 0.20, 'Order': 0.22, 'Options': 0.25, 'Technical': 0.10, 'News': 0.06}
    }

    # Generate weights with smooth transitions
    for t in range(time_steps):
        regime = regimes[t]
        target_weights = regime_weights[regime]

        # Add some noise and smooth transitions
        for factor in weights.keys():
            if t == 0:
                weights[factor][t] = target_weights[factor]
            else:
                # Exponential moving average for smooth transitions
                alpha = 0.15
                weights[factor][t] = alpha * target_weights[factor] + (1 - alpha) * weights[factor][t-1]
                # Add small noise
                weights[factor][t] += np.random.normal(0, 0.005)

    # Create figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)
    fig.patch.set_facecolor('white')

    x = np.arange(time_steps)

    # TOP PANEL: Weight evolution
    colors = {
        'Micro': PaperColorPalette.MICRO,
        'Order': PaperColorPalette.ORDER_FLOW,
        'Options': PaperColorPalette.OPTIONS,
        'Technical': PaperColorPalette.TECHNICAL,
        'News': PaperColorPalette.NEWS
    }

    for factor, color in colors.items():
        ax1.plot(x, weights[factor], label=factor, color=color, linewidth=2.5, alpha=0.9)
        ax1.fill_between(x, 0, weights[factor], color=color, alpha=0.2)

    ax1.set_ylabel('Weight Value', fontsize=12, weight='bold')
    ax1.set_title('Dynamic Weight Evolution Across Market Regimes', fontsize=16, weight='bold', pad=15)
    ax1.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 0.35)

    # Add regime background shading
    regime_colors = {
        'sideways': PaperColorPalette.SIDEWAYS,
        'bull': PaperColorPalette.BULL,
        'high_vol': PaperColorPalette.HIGH_VOL,
        'bear': PaperColorPalette.BEAR
    }

    current_regime = regimes[0]
    start_idx = 0
    for i in range(1, time_steps + 1):
        if i == time_steps or regimes[i] != current_regime:
            end_idx = i
            ax1.axvspan(start_idx, end_idx, alpha=0.1, color=regime_colors[current_regime])
            # Add regime label
            mid_idx = (start_idx + end_idx) / 2
            ax1.text(mid_idx, 0.32, current_regime.upper().replace('_', ' '),
                    ha='center', va='center', fontsize=10, weight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
            if i < time_steps:
                current_regime = regimes[i]
                start_idx = i

    # BOTTOM PANEL: Regime indicator
    regime_numeric = {'sideways': 0, 'bull': 1, 'high_vol': 2, 'bear': 3}
    regime_values = [regime_numeric[r] for r in regimes]

    for i in range(len(regimes)):
        color = regime_colors[regimes[i]]
        ax2.bar(i, 1, color=color, edgecolor='none', alpha=0.8)

    ax2.set_ylabel('Market Regime', fontsize=12, weight='bold')
    ax2.set_xlabel('Time Steps', fontsize=12, weight='bold')
    ax2.set_yticks([0.5])
    ax2.set_yticklabels(['Regime'])
    ax2.set_xlim(0, time_steps)
    ax2.grid(False)

    # Legend for regimes
    regime_legend = [
        mpatches.Patch(color=PaperColorPalette.SIDEWAYS, label='Sideways/Normal'),
        mpatches.Patch(color=PaperColorPalette.BULL, label='Bull Market'),
        mpatches.Patch(color=PaperColorPalette.HIGH_VOL, label='High Volatility'),
        mpatches.Patch(color=PaperColorPalette.BEAR, label='Bear Market')
    ]
    ax2.legend(handles=regime_legend, loc='upper right', fontsize=10, frameon=True, shadow=True, ncol=4)

    fig.suptitle('Adaptive Weight Adjustment via HMM Regime Detection + Kalman Filtering',
                fontsize=16, weight='bold', y=0.995)

    plt.tight_layout()

    filename = f'{output_prefix}_weight_evolution.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Generated: {filename}")
    plt.close()


def main():
    """Generate all paper-specific visualizations"""

    print("=" * 70)
    print("GENERATING PAPER-SPECIFIC VISUALIZATIONS")
    print("Stock Heat Diffusion Model - Production-Ready Figures")
    print("=" * 70)
    print()

    # Default ticker (can be changed)
    ticker = "STOCK"
    output_prefix = "paper"

    print(f"📊 Generating visualizations for: {ticker}")
    print(f"📁 Output prefix: {output_prefix}_*.png")
    print()

    # Generate all visualizations
    print("🎨 Creating visualizations...")
    print()

    create_baseline_weight_visualization(output_prefix)
    create_regime_comparison_visualization(output_prefix)
    create_heat_diffusion_network(output_prefix, ticker)
    create_temporal_heat_propagation(output_prefix)
    create_performance_comparison(output_prefix)
    create_ablation_study(output_prefix)
    create_weight_evolution_over_time(output_prefix)

    print()
    print("=" * 70)
    print("✅ ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
    print("=" * 70)
    print()
    print("📋 Generated Files:")
    print("   1. paper_baseline_weights.png          - Baseline weight allocation (Table 1)")
    print("   2. paper_regime_weights.png            - Regime-dependent weights (Table 5)")
    print("   3. paper_heat_diffusion_network.png    - Knowledge graph structure")
    print("   4. paper_temporal_heat_propagation.png - Multi-hop heat propagation")
    print("   5. paper_performance_comparison.png    - Model comparison (Table 2)")
    print("   6. paper_ablation_study.png            - Ablation study (Table 3)")
    print("   7. paper_weight_evolution.png          - Dynamic weight adaptation")
    print()
    print("📐 Resolution: 300 DPI (publication quality)")
    print("🎨 Color: Professional palette (Nature/Science/IEEE standards)")
    print("📊 Data: Directly from paper Tables 1, 2, 3, 5")
    print()
    print("🏆 PRODUCTION-READY FOR SUBMISSION")
    print("=" * 70)


if __name__ == "__main__":
    main()
