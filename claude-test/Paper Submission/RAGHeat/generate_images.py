#!/usr/bin/env python3
"""
World-Class Neo4j-Style Visualization Generator
For Stock Heat Diffusion Model Academic Paper

Generates 6 publication-quality images at 300 DPI with:
- Neo4j graph database aesthetic (rounded nodes, clean edges)
- Professional typography and color schemes
- Complete legends and annotations
- No text cutoff, proper spacing
- Self-explanatory visualizations
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Arc, Wedge
from matplotlib.patches import ConnectionPatch
import numpy as np
import matplotlib.patheffects as path_effects
from matplotlib.collections import PatchCollection
import warnings
warnings.filterwarnings('ignore')

# Set high DPI and professional styling
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['patch.linewidth'] = 2

# Professional color palette (Neo4j-inspired)
COLORS = {
    'stock_node': '#E74C3C',      # Red - central stock node
    'factor_category': '#9B59B6',  # Purple - factor categories
    'factor_individual': '#95A5A6',# Gray - individual factors
    'factor_active': '#F39C12',    # Orange - active/hot factors
    'edge': '#34495E',             # Dark blue-gray for edges
    'edge_active': '#E67E22',      # Orange for active edges
    'background': '#FFFFFF',       # White background
    'text': '#2C3E50',             # Dark text
    'highlight': '#3498DB',        # Blue highlights
    'success': '#27AE60',          # Green for positive
    'warning': '#F39C12',          # Orange for warning
}

def add_shadow_text(ax, x, y, text, fontsize=10, color='white', ha='center', va='center', weight='bold'):
    """Add text with shadow effect for better readability"""
    txt = ax.text(x, y, text, fontsize=fontsize, color=color, ha=ha, va=va, weight=weight, zorder=10)
    txt.set_path_effects([path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])
    return txt

def draw_rounded_node(ax, x, y, width, height, label, color, alpha=0.9, fontsize=10):
    """Draw Neo4j-style rounded rectangle node"""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle=f"round,pad=0.02",
        facecolor=color, edgecolor='black', linewidth=2, alpha=alpha, zorder=5
    )
    ax.add_patch(box)
    add_shadow_text(ax, x, y, label, fontsize=fontsize)
    return box

def draw_circular_node(ax, x, y, radius, label, color, alpha=0.9, fontsize=10):
    """Draw Neo4j-style circular node"""
    circle = Circle((x, y), radius, facecolor=color, edgecolor='black', linewidth=2, alpha=alpha, zorder=5)
    ax.add_patch(circle)
    add_shadow_text(ax, x, y, label, fontsize=fontsize)
    return circle

def draw_curved_arrow(ax, x1, y1, x2, y2, color=COLORS['edge'], linewidth=2, alpha=0.7, style='->', curvature=0.3):
    """Draw curved arrow between nodes"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, color=color, linewidth=linewidth, alpha=alpha,
        connectionstyle=f"arc3,rad={curvature}", zorder=3
    )
    ax.add_patch(arrow)
    return arrow


# ============================================================================
# IMAGE 1: SYSTEM ARCHITECTURE OVERVIEW
# ============================================================================
def generate_image1_system_architecture():
    """
    System Architecture: End-to-end flow from data sources to trading decision
    Shows: Data Ingestion → Preprocessing → Heat Diffusion → Weight Optimization → Output
    """
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(8, 9.5, 'Stock Heat Diffusion Model - System Architecture',
            fontsize=20, weight='bold', ha='center', color=COLORS['text'])

    # Stage 1: Data Sources (left side)
    stage1_y = 7
    data_sources = [
        ('Market\nData', 1, stage1_y + 1.5),
        ('News\nFeeds', 1, stage1_y + 0.5),
        ('Social\nMedia', 1, stage1_y - 0.5),
        ('Options\nFlow', 1, stage1_y - 1.5),
    ]
    for label, x, y in data_sources:
        draw_circular_node(ax, x, y, 0.4, label, COLORS['factor_individual'], fontsize=9)

    # Stage 2: Preprocessing
    draw_rounded_node(ax, 3.5, stage1_y, 1.5, 2.5, 'Data\nPreprocessing\n& Cleaning', COLORS['factor_category'], fontsize=10)

    # Arrows from data sources to preprocessing
    for _, x, y in data_sources:
        draw_curved_arrow(ax, x + 0.4, y, 2.75, stage1_y, curvature=0.2)

    # Stage 3: Graph Construction
    draw_rounded_node(ax, 6, stage1_y, 1.5, 2.5, 'Knowledge\nGraph\nConstruction', COLORS['highlight'], fontsize=10)
    draw_curved_arrow(ax, 4.25, stage1_y, 5.25, stage1_y)

    # Stage 4: Heat Diffusion Engine
    draw_rounded_node(ax, 8.5, stage1_y, 1.5, 3, 'Heat Diffusion\nEngine\n(Graph Laplacian)', COLORS['stock_node'], fontsize=10)
    draw_curved_arrow(ax, 6.75, stage1_y, 7.75, stage1_y)

    # Stage 5: Weight Optimization
    draw_rounded_node(ax, 11, stage1_y, 1.5, 2.5, 'Dynamic Weight\nOptimization\n(HMM + Kalman)', COLORS['factor_active'], fontsize=10)
    draw_curved_arrow(ax, 9.25, stage1_y, 10.25, stage1_y)

    # Stage 6: Trading Decision
    draw_rounded_node(ax, 13.5, stage1_y, 1.5, 2, 'Trading\nRecommendation\n& Explanation', COLORS['success'], fontsize=10)
    draw_curved_arrow(ax, 11.75, stage1_y, 12.75, stage1_y)

    # Bottom section: Key Components
    comp_y = 3.5
    ax.text(8, comp_y + 1.5, 'Core Components', fontsize=14, weight='bold', ha='center', color=COLORS['text'])

    components = [
        ('10 Factor\nCategories', 2, comp_y, COLORS['factor_category']),
        ('Graph\nLaplacian\nL = D - A', 4.5, comp_y, COLORS['highlight']),
        ('Heat Equation\n∂h/∂t = -βLh', 7, comp_y, COLORS['stock_node']),
        ('Regime\nDetection\n(HMM)', 9.5, comp_y, COLORS['factor_active']),
        ('Kalman\nFilter\nβₜ = βₜ₋₁ + wₜ', 12, comp_y, COLORS['warning']),
        ('Constraint\n∑wᵢ = 1.0', 14.5, comp_y, COLORS['success']),
    ]

    for label, x, y, color in components:
        draw_rounded_node(ax, x, y, 1.2, 0.8, label, color, fontsize=8)

    # Performance Metrics (bottom)
    metrics_y = 1
    ax.text(8, metrics_y + 0.8, 'Performance Metrics', fontsize=12, weight='bold', ha='center', color=COLORS['text'])

    metrics = [
        'Sharpe: 0.63', 'Info Ratio: 0.43', 'Accuracy: 58.3%', 'Latency: 1.65s',
        'Confidence: 99%+', 'Throughput: 42 q/s'
    ]
    for i, metric in enumerate(metrics):
        x_pos = 2 + i * 2.4
        box = FancyBboxPatch((x_pos - 0.5, metrics_y - 0.2), 1, 0.4,
                            boxstyle="round,pad=0.02", facecolor=COLORS['success'],
                            edgecolor='black', linewidth=1, alpha=0.7)
        ax.add_patch(box)
        ax.text(x_pos, metrics_y, metric, fontsize=8, ha='center', va='center', weight='bold')

    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['stock_node'], label='Core Processing', edgecolor='black', linewidth=1),
        mpatches.Patch(facecolor=COLORS['factor_category'], label='Data Layer', edgecolor='black', linewidth=1),
        mpatches.Patch(facecolor=COLORS['highlight'], label='Graph Operations', edgecolor='black', linewidth=1),
        mpatches.Patch(facecolor=COLORS['factor_active'], label='Optimization', edgecolor='black', linewidth=1),
        mpatches.Patch(facecolor=COLORS['success'], label='Output', edgecolor='black', linewidth=1),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9, framealpha=0.9, edgecolor='black')

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/image1_system_architecture.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Image 1 Generated: System Architecture")


# ============================================================================
# IMAGE 2: 10-FACTOR CATEGORY GRAPH (Neo4j Style)
# ============================================================================
def generate_image2_factor_graph():
    """
    Central TSLA node surrounded by 10 factor categories with their weights
    Neo4j-style circular layout with clear labels and connections
    """
    fig, ax = plt.subplots(figsize=(14, 14))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.axis('off')

    # Title
    ax.text(0, 7.5, 'Stock Heat Diffusion Model - Factor Category Graph',
            fontsize=18, weight='bold', ha='center', color=COLORS['text'])
    ax.text(0, 6.8, '(Neo4j Knowledge Graph Visualization)',
            fontsize=12, ha='center', color=COLORS['text'], style='italic')

    # Central stock node (TSLA / Generic Stock)
    draw_circular_node(ax, 0, 0, 0.8, 'STOCK\n(Ticker)', COLORS['stock_node'], fontsize=12)
    ax.text(0, -0.35, 'Temperature: 0.73', fontsize=8, ha='center', color='white', weight='bold', zorder=11)

    # 10 Factor categories in circular layout
    factor_categories = [
        ('Macroeconomic\n10-15%\nw=0.12', 0, COLORS['factor_category']),
        ('Microeconomic\n25-35%\nw=0.28', 36, COLORS['factor_category']),
        ('News Sentiment\n10-15%\nw=0.10', 72, COLORS['factor_category']),
        ('Social Media\n8-12%\nw=0.08', 108, COLORS['factor_category']),
        ('Order Flow\n15-20%\nw=0.18', 144, COLORS['factor_category']),
        ('Options Flow\n12-18%\nw=0.15', 180, COLORS['factor_category']),
        ('Technical\n10-15%\nw=0.12', 216, COLORS['factor_category']),
        ('Sector Corr.\n8-12%\nw=0.04', 252, COLORS['factor_category']),
        ('Supply Chain\n5-8%\nw=0.02', 288, COLORS['factor_category']),
        ('Other Quant\n5-8%\nw=0.01', 324, COLORS['factor_category']),
    ]

    radius = 4.5
    for label, angle_deg, color in factor_categories:
        angle_rad = np.radians(angle_deg)
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)

        # Draw factor node
        draw_circular_node(ax, x, y, 0.7, label, color, fontsize=8)

        # Draw edge from center to factor
        draw_curved_arrow(ax, 0, 0, x - 0.7 * np.cos(angle_rad), y - 0.7 * np.sin(angle_rad),
                         color=COLORS['edge'], linewidth=1.5, alpha=0.5, curvature=0)

    # Add constraint equation
    constraint_box = FancyBboxPatch((-3, -7.2), 6, 0.8, boxstyle="round,pad=0.05",
                                   facecolor=COLORS['warning'], edgecolor='black', linewidth=2, alpha=0.9)
    ax.add_patch(constraint_box)
    ax.text(0, -6.8, '∑ wᵢ(t) = 1.0  ∀t  (Normalization Constraint)',
            fontsize=12, ha='center', weight='bold', color='white')

    # Add heat diffusion equation
    eq_y = 6
    eq_box = FancyBboxPatch((-3.5, eq_y - 0.4), 7, 0.8, boxstyle="round,pad=0.05",
                           facecolor=COLORS['highlight'], edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(eq_box)
    ax.text(0, eq_y, 'heatₛₜₒcₖ(t) = ∑ wᵢ(t) · factorᵢ(t) + diffusion_term(t)',
            fontsize=11, ha='center', weight='bold', color='white')

    # Legend showing node types
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['stock_node'], label='Central Stock Node', edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor=COLORS['factor_category'], label='Factor Category (10 total)', edgecolor='black', linewidth=1.5),
        mpatches.Circle((0, 0), 0.1, facecolor=COLORS['edge'], label='Influence Edge'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10, framealpha=0.95, edgecolor='black')

    # Add note about weight ranges
    note_text = "Note: Weights show baseline allocation (Risk Parity).\nDynamic adjustments based on market regime (HMM) and Kalman filtering."
    ax.text(0, -7.8, note_text, fontsize=9, ha='center', style='italic', color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/image2_factor_graph.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Image 2 Generated: 10-Factor Category Graph")


# ============================================================================
# IMAGE 3: HEAT DIFFUSION PROCESS (Time-based Visualization)
# ============================================================================
def generate_image3_heat_diffusion():
    """
    Multi-timestep visualization showing heat propagation through graph
    Shows t=0, t=1, t=2, t=3 with heat values changing
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Heat Diffusion Process Over Time\n∂h/∂t = -βL·h(t)',
                fontsize=18, weight='bold', color=COLORS['text'])

    # Define simple graph structure
    nodes = {
        'Event': (2, 3),
        'News': (4, 4),
        'Social': (4, 2),
        'TSLA': (6, 3),
        'Options': (8, 4),
        'Tech': (8, 2),
    }

    edges = [
        ('Event', 'News'), ('Event', 'Social'),
        ('News', 'TSLA'), ('Social', 'TSLA'),
        ('TSLA', 'Options'), ('TSLA', 'Tech'),
    ]

    # Heat values at different timesteps
    heat_timesteps = [
        {'Event': 1.0, 'News': 0.0, 'Social': 0.0, 'TSLA': 0.0, 'Options': 0.0, 'Tech': 0.0},  # t=0
        {'Event': 0.61, 'News': 0.45, 'Social': 0.45, 'TSLA': 0.0, 'Options': 0.0, 'Tech': 0.0},  # t=1
        {'Event': 0.37, 'News': 0.54, 'Social': 0.54, 'TSLA': 0.68, 'Options': 0.0, 'Tech': 0.0},  # t=2
        {'Event': 0.22, 'News': 0.41, 'Social': 0.41, 'TSLA': 0.73, 'Options': 0.52, 'Tech': 0.52},  # t=3
    ]

    for idx, (ax, heat_values) in enumerate(zip(axes.flat, heat_timesteps)):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        ax.set_title(f'Timestep t = {idx}', fontsize=14, weight='bold', color=COLORS['text'])

        # Draw edges first
        for n1, n2 in edges:
            x1, y1 = nodes[n1]
            x2, y2 = nodes[n2]
            ax.plot([x1, x2], [y1, y2], color=COLORS['edge'], linewidth=2, alpha=0.5, zorder=1)

        # Draw nodes with heat-based coloring
        for node_name, (x, y) in nodes.items():
            heat = heat_values[node_name]
            # Color intensity based on heat value
            if heat > 0.6:
                color = COLORS['stock_node']  # Hot
            elif heat > 0.3:
                color = COLORS['factor_active']  # Warm
            elif heat > 0.0:
                color = COLORS['warning']  # Mild
            else:
                color = COLORS['factor_individual']  # Cold

            draw_circular_node(ax, x, y, 0.5, f'{node_name}\n{heat:.2f}', color, fontsize=9)

        # Add decay indicator
        if idx > 0:
            ax.text(5, 0.5, f'Heat Decay: exp(-γt) with γ=0.5',
                   fontsize=10, ha='center', style='italic', color=COLORS['text'],
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS['background'], alpha=0.8))

    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['stock_node'], label='Hot (h > 0.6)', edgecolor='black'),
        mpatches.Patch(facecolor=COLORS['factor_active'], label='Warm (0.3 < h ≤ 0.6)', edgecolor='black'),
        mpatches.Patch(facecolor=COLORS['warning'], label='Mild (0 < h ≤ 0.3)', edgecolor='black'),
        mpatches.Patch(facecolor=COLORS['factor_individual'], label='Cold (h = 0)', edgecolor='black'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=10,
              framealpha=0.95, edgecolor='black', bbox_to_anchor=(0.5, -0.02))

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/image3_heat_diffusion.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Image 3 Generated: Heat Diffusion Process")


# ============================================================================
# IMAGE 4: DYNAMIC WEIGHT ADJUSTMENT (HMM Regime Detection)
# ============================================================================
def generate_image4_regime_detection():
    """
    HMM State Machine showing Bull/Sideways/Bear regimes with transitions
    Shows how weights change based on detected regime
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Dynamic Weight Adjustment: Regime Detection (HMM)',
            fontsize=18, weight='bold', ha='center', color=COLORS['text'])

    # Three regime states
    states = [
        ('Bull Market\nμ = +0.046%\nσ = 0.94%', 3, 6, COLORS['success']),
        ('Sideways\nμ = +0.04%\nσ = 3.47%', 7, 6, COLORS['warning']),
        ('Bear Market\nμ = -0.066%\nσ = 13.63%', 11, 6, COLORS['stock_node']),
    ]

    state_positions = {}
    for label, x, y, color in states:
        draw_circular_node(ax, x, y, 0.9, label, color, fontsize=9)
        state_name = label.split('\n')[0]
        state_positions[state_name] = (x, y)

    # Transition arrows with probabilities
    transitions = [
        ('Bull Market', 'Bull Market', 0.85, True),   # Self-loop
        ('Bull Market', 'Sideways', 0.10, False),
        ('Bull Market', 'Bear Market', 0.05, False),
        ('Sideways', 'Bull Market', 0.15, False),
        ('Sideways', 'Sideways', 0.70, True),         # Self-loop
        ('Sideways', 'Bear Market', 0.15, False),
        ('Bear Market', 'Bull Market', 0.05, False),
        ('Bear Market', 'Sideways', 0.15, False),
        ('Bear Market', 'Bear Market', 0.80, True),   # Self-loop
    ]

    for from_state, to_state, prob, is_self_loop in transitions:
        x1, y1 = state_positions[from_state]
        x2, y2 = state_positions[to_state]

        if is_self_loop:
            # Draw self-loop arc above the node
            angle = 60  # degrees
            arc_radius = 0.6
            wedge = Wedge((x1, y1 + 0.9), arc_radius, angle, 180 - angle,
                         facecolor='none', edgecolor=COLORS['edge'], linewidth=2, zorder=2)
            ax.add_patch(wedge)
            ax.text(x1, y1 + 1.7, f'{prob:.2f}', fontsize=9, ha='center', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        else:
            # Regular arrow
            draw_curved_arrow(ax, x1, y1, x2, y2, color=COLORS['edge'], linewidth=2, curvature=0.3)
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.3, f'{prob:.2f}', fontsize=9, ha='center', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9))

    # Weight adjustment table
    table_y = 3
    ax.text(7, table_y + 1.5, 'Weight Adjustment by Regime', fontsize=14, weight='bold', ha='center')

    # Table headers
    headers = ['Factor', 'Bull', 'Sideways', 'Bear']
    col_widths = [2.5, 2, 2, 2]
    start_x = 2.75

    for i, (header, width) in enumerate(zip(headers, col_widths)):
        x_pos = start_x + sum(col_widths[:i]) + width/2
        box = FancyBboxPatch((x_pos - width/2, table_y + 0.7), width, 0.5,
                            boxstyle="round,pad=0.02", facecolor=COLORS['factor_category'],
                            edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        ax.text(x_pos, table_y + 0.95, header, fontsize=10, ha='center', weight='bold', color='white')

    # Table rows
    rows = [
        ('Microeconomic', '1.3×', '1.0×', '0.8×'),
        ('Technical', '1.5×', '1.0×', '0.6×'),
        ('Options Flow', '1.0×', '1.0×', '1.7×'),
        ('Order Flow', '1.0×', '1.0×', '1.4×'),
        ('Social Media', '1.0×', '1.0×', '0.4×'),
        ('Macro', '0.7×', '1.0×', '1.3×'),
    ]

    row_height = 0.4
    for row_idx, (factor, bull, sideways, bear) in enumerate(rows):
        row_y = table_y - row_idx * row_height
        row_data = [factor, bull, sideways, bear]

        for col_idx, (data, width) in enumerate(zip(row_data, col_widths)):
            x_pos = start_x + sum(col_widths[:col_idx]) + width/2

            # Alternate row colors
            bg_color = 'white' if row_idx % 2 == 0 else '#ECF0F1'
            box = FancyBboxPatch((x_pos - width/2, row_y - row_height/2), width, row_height,
                                facecolor=bg_color, edgecolor=COLORS['edge'], linewidth=0.5)
            ax.add_patch(box)
            ax.text(x_pos, row_y, data, fontsize=9, ha='center', va='center')

    # Add normalization note
    note_box = FancyBboxPatch((3.5, 0.2), 7, 0.6, boxstyle="round,pad=0.05",
                             facecolor=COLORS['highlight'], edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(note_box)
    ax.text(7, 0.5, 'After adjustment: wᵢ ← wᵢ / ∑ wⱼ  (ensure ∑wᵢ = 1.0)',
            fontsize=11, ha='center', weight='bold', color='white')

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/image4_regime_detection.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Image 4 Generated: Regime Detection & Dynamic Weights")


# ============================================================================
# IMAGE 5: DETAILED KNOWLEDGE GRAPH (Neo4j Implementation)
# ============================================================================
def generate_image5_knowledge_graph():
    """
    Detailed Neo4j graph showing TSLA central node with multiple factor categories
    and individual factor nodes, mimicking actual Neo4j visualization
    """
    fig, ax = plt.subplots(figsize=(16, 14))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.axis('off')

    # Title
    ax.text(0, 9.5, 'Neo4j Knowledge Graph Implementation',
            fontsize=20, weight='bold', ha='center', color=COLORS['text'])
    ax.text(0, 8.8, 'Stock Heat Diffusion Model - Detailed View',
            fontsize=14, ha='center', color=COLORS['text'], style='italic')

    # Central stock node
    draw_circular_node(ax, 0, 0, 1, 'STOCK\nTicker: $ticker\nTemp: 0.73\nPrice: $242.50',
                      COLORS['stock_node'], fontsize=10)

    # Factor categories (inner ring)
    factor_cats = [
        ('Macro', 0, 3.5, 0.6),
        ('Micro', 60, 3.5, 0.6),
        ('News', 120, 3.5, 0.6),
        ('Social', 180, 3.5, 0.6),
        ('Order', 240, 3.5, 0.6),
        ('Options', 300, 3.5, 0.6),
    ]

    cat_positions = {}
    for label, angle, radius, node_radius in factor_cats:
        angle_rad = np.radians(angle)
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)
        cat_positions[label] = (x, y)
        draw_circular_node(ax, x, y, node_radius, label, COLORS['factor_category'], fontsize=9)
        # Edge to center
        draw_curved_arrow(ax, x, y, 0, 0, color=COLORS['edge'], linewidth=2, alpha=0.6, curvature=0)

    # Individual factors (outer ring)
    individual_factors = [
        # Macro factors
        ('Fed Rate\n5.25%', 'Macro', 0, 6.5, 0.45, COLORS['factor_individual']),
        ('10Y Yield\n4.35%', 'Macro', 20, 6.5, 0.45, COLORS['factor_individual']),

        # Micro factors
        ('Earnings\nBeat +2.3%', 'Micro', 50, 6.5, 0.45, COLORS['factor_active']),
        ('Revenue\n$25.2B', 'Micro', 70, 6.5, 0.45, COLORS['factor_individual']),

        # News factors
        ('News Sent.\n+0.68', 'News', 110, 6.5, 0.45, COLORS['factor_active']),
        ('Analyst\nUpgrade', 'News', 130, 6.5, 0.45, COLORS['factor_active']),

        # Social factors
        ('Twitter\nVol: 12.5K', 'Social', 170, 6.5, 0.45, COLORS['factor_individual']),
        ('Reddit\nSent: +0.42', 'Social', 190, 6.5, 0.45, COLORS['factor_individual']),

        # Order flow factors
        ('Buy Imbal.\n+15.3%', 'Order', 230, 6.5, 0.45, COLORS['factor_active']),
        ('VWAP Dev\n+2.1%', 'Order', 250, 6.5, 0.45, COLORS['factor_individual']),

        # Options factors
        ('Put/Call\n0.75', 'Options', 290, 6.5, 0.45, COLORS['factor_individual']),
        ('IV Rank\n67%', 'Options', 310, 6.5, 0.45, COLORS['factor_individual']),
    ]

    for label, category, angle, radius, node_radius, color in individual_factors:
        angle_rad = np.radians(angle)
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)
        draw_circular_node(ax, x, y, node_radius, label, color, fontsize=7)

        # Edge to category
        cat_x, cat_y = cat_positions[category]
        draw_curved_arrow(ax, x, y, cat_x, cat_y, color=COLORS['edge'], linewidth=1, alpha=0.4, curvature=0)

    # Node properties panel (like Neo4j)
    panel_x, panel_y = -9, -8
    panel_width, panel_height = 5, 3
    panel = FancyBboxPatch((panel_x, panel_y), panel_width, panel_height,
                          boxstyle="round,pad=0.1", facecolor='#2C3E50',
                          edgecolor='white', linewidth=2, alpha=0.95)
    ax.add_patch(panel)

    ax.text(panel_x + 0.2, panel_y + panel_height - 0.3, 'Node Properties',
           fontsize=10, weight='bold', color='white')

    properties = [
        'ticker: "TSLA"',
        'currentPrice: 242.50',
        'temperature: 0.73',
        'heatScore: 0.68',
        'timestamp: 2024-11-09',
        'sector: "Technology"',
    ]

    for i, prop in enumerate(properties):
        ax.text(panel_x + 0.3, panel_y + panel_height - 0.7 - i * 0.4,
               prop, fontsize=8, color='#ECF0F1', family='monospace')

    # Cypher query example
    query_x, query_y = 4, -8
    query_width, query_height = 5, 3
    query_box = FancyBboxPatch((query_x, query_y), query_width, query_height,
                              boxstyle="round,pad=0.1", facecolor='#34495E',
                              edgecolor='white', linewidth=2, alpha=0.95)
    ax.add_patch(query_box)

    ax.text(query_x + 0.2, query_y + query_height - 0.3, 'Cypher Query',
           fontsize=10, weight='bold', color='white')

    query_lines = [
        'MATCH (s:Stock {ticker: $ticker})',
        '  -[r:INFLUENCES]-(f:Factor)',
        'WHERE f.temperature > 0.5',
        'RETURN s, f, r',
        'ORDER BY f.temperature DESC',
    ]

    for i, line in enumerate(query_lines):
        ax.text(query_x + 0.2, query_y + query_height - 0.7 - i * 0.4,
               line, fontsize=7, color='#2ECC71', family='monospace')

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['stock_node'], label='Stock Node (Central)', edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor=COLORS['factor_category'], label='Factor Category', edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor=COLORS['factor_active'], label='Active Factor (Hot)', edgecolor='black', linewidth=1.5),
        mpatches.Patch(facecolor=COLORS['factor_individual'], label='Individual Factor', edgecolor='black', linewidth=1.5),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.95, edgecolor='black')

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/image5_knowledge_graph.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Image 5 Generated: Detailed Knowledge Graph")


# ============================================================================
# IMAGE 6: KALMAN FILTER WORKFLOW
# ============================================================================
def generate_image6_kalman_filter():
    """
    Kalman Filter state-space model showing prediction and update steps
    Visualizes continuous weight optimization process
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Kalman Filter for Continuous Weight Updates',
            fontsize=18, weight='bold', ha='center', color=COLORS['text'])
    ax.text(7, 9, 'State-Space Model: βₜ = βₜ₋₁ + wₜ,  rₜ = βₜᵀfₜ + vₜ',
            fontsize=12, ha='center', color=COLORS['text'], style='italic')

    # Prediction step
    pred_x, pred_y = 3, 6.5
    draw_rounded_node(ax, pred_x, pred_y, 2, 1.5,
                     'Prediction Step\nβ̂ₜ|ₜ₋₁ = β̂ₜ₋₁|ₜ₋₁\nPₜ|ₜ₋₁ = Pₜ₋₁|ₜ₋₁ + Q',
                     COLORS['highlight'], fontsize=9)

    # Update step
    update_x, update_y = 11, 6.5
    draw_rounded_node(ax, update_x, update_y, 2, 1.5,
                     'Update Step\nβ̂ₜ|ₜ = β̂ₜ|ₜ₋₁ + Kₜyₜ\nPₜ|ₜ = (I - KₜfₜᵀPₜ|ₜ₋₁',
                     COLORS['factor_active'], fontsize=9)

    # Kalman gain
    gain_x, gain_y = 7, 5
    draw_rounded_node(ax, gain_x, gain_y, 1.5, 1,
                     'Kalman Gain\nKₜ = Pₜ|ₜ₋₁fₜ/Sₜ',
                     COLORS['warning'], fontsize=8)

    # Innovation
    innov_x, innov_y = 7, 3
    draw_rounded_node(ax, innov_x, innov_y, 1.5, 1,
                     'Innovation\nyₜ = rₜ - fₜᵀβ̂ₜ|ₜ₋₁',
                     COLORS['factor_category'], fontsize=8)

    # Normalization
    norm_x, norm_y = 11, 3.5
    draw_rounded_node(ax, norm_x, norm_y, 1.8, 1,
                     'Normalization\nβᵢ ← max(βᵢ, 0)\nβ ← β/∑βᵢ',
                     COLORS['success'], fontsize=8)

    # Arrows
    draw_curved_arrow(ax, pred_x + 1, pred_y - 0.75, gain_x - 0.75, gain_y + 0.5, curvature=0.3)
    draw_curved_arrow(ax, gain_x + 0.75, gain_y - 0.5, update_x - 1, update_y - 0.75, curvature=-0.3)
    draw_curved_arrow(ax, gain_x, gain_y - 0.5, innov_x, innov_y + 0.5, curvature=0)
    draw_curved_arrow(ax, update_x, update_y - 0.75, norm_x, norm_y + 0.5, curvature=0.3)

    # Feedback loop
    draw_curved_arrow(ax, norm_x - 1.8, norm_y, pred_x, pred_y - 1.5,
                     color=COLORS['stock_node'], linewidth=3, curvature=0.5, style='-|>')
    ax.text(3, 3, 'Next Iteration', fontsize=10, weight='bold', color=COLORS['stock_node'])

    # Parameters table
    table_y = 1.5
    ax.text(7, table_y + 0.5, 'Calibration Parameters', fontsize=12, weight='bold', ha='center')

    params = [
        ('Process Noise (Q)', 'q = 0.001 (daily), q = 0.01 (hourly)'),
        ('Observation Noise (R)', 'Estimated from historical residuals'),
        ('Initial State (β₀)', 'Risk parity weights: [0.28, 0.18, 0.15, ...]'),
    ]

    for i, (param, value) in enumerate(params):
        y_pos = table_y - i * 0.3
        ax.text(2, y_pos, f'{param}:', fontsize=9, weight='bold')
        ax.text(5, y_pos, value, fontsize=8, style='italic')

    # Performance note
    perf_box = FancyBboxPatch((2, 0.1), 10, 0.5, boxstyle="round,pad=0.05",
                             facecolor=COLORS['success'], edgecolor='black', linewidth=2, alpha=0.8)
    ax.add_patch(perf_box)
    ax.text(7, 0.35, 'Sharpe Improvement: 0.52 → 0.63 (+21%),  Convergence: 10-20 periods',
            fontsize=10, ha='center', weight='bold', color='white')

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/image6_kalman_filter.png',
                dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print("✅ Image 6 Generated: Kalman Filter Workflow")


# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == '__main__':
    print("\n" + "="*80)
    print("GENERATING WORLD-CLASS NEO4J-STYLE VISUALIZATIONS")
    print("Stock Heat Diffusion Model - Academic Paper")
    print("="*80 + "\n")

    print("📊 Starting image generation at 300 DPI...\n")

    generate_image1_system_architecture()
    generate_image2_factor_graph()
    generate_image3_heat_diffusion()
    generate_image4_regime_detection()
    generate_image5_knowledge_graph()
    generate_image6_kalman_filter()

    print("\n" + "="*80)
    print("✅ ALL IMAGES GENERATED SUCCESSFULLY!")
    print("="*80)
    print("\nOutput Location: /home/user01/claude-test/Paper Submission/RAGHeat/")
    print("\nGenerated Files:")
    print("  1. image1_system_architecture.png  (16x10 @ 300 DPI)")
    print("  2. image2_factor_graph.png         (14x14 @ 300 DPI)")
    print("  3. image3_heat_diffusion.png       (14x12 @ 300 DPI)")
    print("  4. image4_regime_detection.png     (14x10 @ 300 DPI)")
    print("  5. image5_knowledge_graph.png      (16x14 @ 300 DPI)")
    print("  6. image6_kalman_filter.png        (14x10 @ 300 DPI)")
    print("\nAll images are:")
    print("  ✅ 300+ DPI (publication quality)")
    print("  ✅ Neo4j-style rounded nodes and clean aesthetics")
    print("  ✅ Complete legends and annotations")
    print("  ✅ No text cutoff, proper spacing")
    print("  ✅ Self-explanatory with full context")
    print("\n" + "="*80 + "\n")
