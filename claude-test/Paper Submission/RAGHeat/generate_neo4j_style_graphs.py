#!/usr/bin/env python3
"""
Neo4j-Style Graph Visualizations for Stock Heat Diffusion Model

Generates production-ready visualizations matching Neo4j Browser aesthetic:
- Large circular nodes with centered labels
- Curved, labeled relationships
- Professional Neo4j color palette
- Node properties displayed
- High-quality 300 DPI output

Based on actual research paper data (Tables 1, 2, 3, 5)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch, Arc, Wedge
from matplotlib.path import Path
from matplotlib.bezier import BezierSegment
import matplotlib.patheffects as path_effects
import numpy as np
import networkx as nx
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')

# Neo4j-style configuration
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 16,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 18,
    'text.usetex': False,
    'axes.unicode_minus': False
})


class Neo4jColorPalette:
    """
    Professional Neo4j-style color palette
    Based on Neo4j Browser default theme
    """

    # Node colors (Neo4j standard palette)
    NODE_STOCK = '#DA5C54'          # Red (primary entity)
    NODE_FACTOR = '#6C4C9D'         # Purple (categories)
    NODE_ENTITY = '#4E9CD6'         # Blue (entities)
    NODE_EVENT = '#F16667'          # Light red (events)
    NODE_DERIVATIVE = '#A879D9'     # Light purple (derivatives)
    NODE_PARTICIPANT = '#F79767'    # Orange (participants)
    NODE_MEDIA = '#5BBCAA'          # Teal (media)
    NODE_REGIME = '#FBC845'         # Yellow (regimes)

    # Relationship colors
    REL_INFLUENCES = '#9B9B9B'      # Gray (standard)
    REL_HEAT = '#F16667'            # Red (heat flow)
    REL_CORRELATES = '#4E9CD6'      # Blue (correlation)

    # Background and text
    BG_COLOR = '#FFFFFF'            # White background
    BG_GRAPH = '#F9F9F9'            # Light gray graph area
    TEXT_PRIMARY = '#2C3E50'        # Dark gray text
    TEXT_SECONDARY = '#7F8C8D'      # Medium gray text
    TEXT_ON_NODE = '#FFFFFF'        # White text on nodes

    # Neo4j-style shadows and effects
    SHADOW_COLOR = '#000000'
    SHADOW_ALPHA = 0.15


class Neo4jNode:
    """Represents a Neo4j-style circular node with label and properties"""

    def __init__(self, id: str, label: str, node_type: str, properties: Dict = None):
        self.id = id
        self.label = label
        self.node_type = node_type
        self.properties = properties or {}

    def get_color(self) -> str:
        """Get color based on node type"""
        color_map = {
            'stock': Neo4jColorPalette.NODE_STOCK,
            'factor': Neo4jColorPalette.NODE_FACTOR,
            'entity': Neo4jColorPalette.NODE_ENTITY,
            'event': Neo4jColorPalette.NODE_EVENT,
            'derivative': Neo4jColorPalette.NODE_DERIVATIVE,
            'participant': Neo4jColorPalette.NODE_PARTICIPANT,
            'media': Neo4jColorPalette.NODE_MEDIA,
            'regime': Neo4jColorPalette.NODE_REGIME
        }
        return color_map.get(self.node_type, Neo4jColorPalette.NODE_ENTITY)


def draw_neo4j_node(ax, x: float, y: float, node: Neo4jNode, radius: float = 0.4,
                     show_properties: bool = False, zorder: int = 10):
    """
    Draw a Neo4j-style circular node with label

    Features:
    - Large circular node
    - Centered white text
    - Drop shadow
    - Optional property badge
    """

    color = node.get_color()

    # Draw shadow
    shadow = Circle((x + 0.015, y - 0.015), radius,
                   facecolor=Neo4jColorPalette.SHADOW_COLOR,
                   edgecolor='none',
                   alpha=Neo4jColorPalette.SHADOW_ALPHA,
                   zorder=zorder-1)
    ax.add_patch(shadow)

    # Draw main node circle
    circle = Circle((x, y), radius,
                   facecolor=color,
                   edgecolor='white',
                   linewidth=3,
                   zorder=zorder)
    ax.add_patch(circle)

    # Draw label (centered, white text)
    label_text = node.label.replace('\\n', '\n')
    text = ax.text(x, y, label_text,
                  ha='center', va='center',
                  fontsize=11, weight='bold',
                  color=Neo4jColorPalette.TEXT_ON_NODE,
                  zorder=zorder+1)

    # Optional: Draw property badge
    if show_properties and node.properties:
        badge_y = y - radius - 0.15
        prop_text = '\n'.join([f'{k}: {v}' for k, v in list(node.properties.items())[:2]])
        ax.text(x, badge_y, prop_text,
               ha='center', va='top',
               fontsize=8,
               bbox=dict(boxstyle='round,pad=0.3',
                        facecolor='white',
                        edgecolor=color,
                        linewidth=1.5,
                        alpha=0.95),
               zorder=zorder+2)

    return circle


def draw_neo4j_relationship(ax, x1: float, y1: float, x2: float, y2: float,
                            label: str = '', color: str = None,
                            linewidth: float = 2.5, curvature: float = 0.15,
                            zorder: int = 1):
    """
    Draw a Neo4j-style curved relationship with arrow and label

    Features:
    - Curved Bezier path
    - Directional arrow
    - Relationship label
    - Professional styling
    """

    if color is None:
        color = Neo4jColorPalette.REL_INFLUENCES

    # Calculate control point for curve
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1

    # Perpendicular offset for curve
    ctrl_x = mid_x - dy * curvature
    ctrl_y = mid_y + dx * curvature

    # Create curved path
    verts = [(x1, y1), (ctrl_x, ctrl_y), (x2, y2)]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
    path = Path(verts, codes)

    # Draw relationship path
    patch = mpatches.PathPatch(path,
                              facecolor='none',
                              edgecolor=color,
                              linewidth=linewidth,
                              alpha=0.7,
                              zorder=zorder)
    ax.add_patch(patch)

    # Draw arrow at end
    # Calculate direction at end point
    t = 0.9  # Position along curve for arrow
    arrow_x = (1-t)**2 * x1 + 2*(1-t)*t * ctrl_x + t**2 * x2
    arrow_y = (1-t)**2 * y1 + 2*(1-t)*t * ctrl_y + t**2 * y2

    # Arrow direction (derivative of Bezier curve)
    arrow_dx = 2*(1-t)*(ctrl_x - x1) + 2*t*(x2 - ctrl_x)
    arrow_dy = 2*(1-t)*(ctrl_y - y1) + 2*t*(y2 - ctrl_y)
    arrow_len = np.sqrt(arrow_dx**2 + arrow_dy**2)
    arrow_dx /= arrow_len
    arrow_dy /= arrow_len

    # Draw arrowhead
    arrow_size = 0.12
    arrow = mpatches.FancyArrow(
        arrow_x - arrow_dx * arrow_size,
        arrow_y - arrow_dy * arrow_size,
        arrow_dx * arrow_size * 2,
        arrow_dy * arrow_size * 2,
        width=arrow_size * 0.8,
        head_width=arrow_size * 1.5,
        head_length=arrow_size * 1.2,
        facecolor=color,
        edgecolor='none',
        alpha=0.7,
        zorder=zorder+1
    )
    ax.add_patch(arrow)

    # Draw relationship label
    if label:
        # Position label at curve midpoint
        t_label = 0.5
        label_x = (1-t_label)**2 * x1 + 2*(1-t_label)*t_label * ctrl_x + t_label**2 * x2
        label_y = (1-t_label)**2 * y1 + 2*(1-t_label)*t_label * ctrl_y + t_label**2 * y2

        ax.text(label_x, label_y, label,
               ha='center', va='center',
               fontsize=9, style='italic',
               color=Neo4jColorPalette.TEXT_SECONDARY,
               bbox=dict(boxstyle='round,pad=0.3',
                        facecolor='white',
                        edgecolor='none',
                        alpha=0.9),
               zorder=zorder+2)


def create_neo4j_baseline_weights_graph(output_prefix: str):
    """
    Neo4j-style graph showing baseline weight allocation

    Visualization:
    - Central stock node
    - 10 factor category nodes in circle
    - Weighted relationships (INFLUENCES)
    - Neo4j aesthetic
    """

    # Data from Table 1
    factors = [
        ('MICRO', 'Microeconomic\nFactors', 0.28),
        ('ORDER', 'Order Flow\nMicrostructure', 0.18),
        ('OPTIONS', 'Options Flow\nDerivatives', 0.15),
        ('TECH', 'Technical\nIndicators', 0.12),
        ('NEWS', 'News\nSentiment', 0.10),
        ('SOCIAL', 'Social Media\nSignals', 0.08),
        ('SECTOR', 'Sector\nCorrelation', 0.04),
        ('MACRO', 'Macroeconomic\nFactors', 0.03),
        ('SUPPLY', 'Supply Chain\nSignals', 0.02),
    ]

    # Create figure
    fig, ax = plt.subplots(figsize=(18, 18))
    fig.patch.set_facecolor(Neo4jColorPalette.BG_COLOR)
    ax.set_facecolor(Neo4jColorPalette.BG_GRAPH)
    ax.axis('off')

    # Create nodes
    stock_node = Neo4jNode('STOCK', 'Stock\nPrice', 'stock', {'heat': 1.0})
    stock_pos = (0, 0)

    # Draw factor nodes in circle
    n_factors = len(factors)
    radius_circle = 3.0

    for i, (factor_id, label, weight) in enumerate(factors):
        angle = 2 * np.pi * i / n_factors - np.pi / 2  # Start from top
        x = radius_circle * np.cos(angle)
        y = radius_circle * np.sin(angle)

        # Create node
        node = Neo4jNode(factor_id, label, 'factor', {'weight': f'{weight:.2f}'})

        # Draw node
        draw_neo4j_node(ax, x, y, node, radius=0.45, show_properties=True)

        # Draw relationship to stock
        draw_neo4j_relationship(
            ax, x, y, stock_pos[0], stock_pos[1],
            label=f'INFLUENCES\nw={weight:.2f}',
            color=Neo4jColorPalette.REL_INFLUENCES,
            linewidth=weight * 15,  # Thickness proportional to weight
            curvature=0.0  # Straight lines for clarity
        )

    # Draw central stock node (last, on top)
    draw_neo4j_node(ax, stock_pos[0], stock_pos[1], stock_node,
                   radius=0.6, show_properties=False)

    # Title
    ax.text(0, 4.2, 'Stock Heat Diffusion Model\nBaseline Weight Allocation (Neo4j Graph)',
           fontsize=20, weight='bold', ha='center', va='top',
           color=Neo4jColorPalette.TEXT_PRIMARY)

    # Constraint annotation
    constraint_text = r'Constraint: $\sum_{i=1}^{10} w_i = 1.00$'
    ax.text(0, -4.2, constraint_text,
           fontsize=14, ha='center', va='bottom', style='italic', weight='bold',
           color=Neo4jColorPalette.NODE_STOCK,
           bbox=dict(boxstyle='round,pad=0.6',
                    facecolor='white',
                    edgecolor=Neo4jColorPalette.NODE_STOCK,
                    linewidth=2))

    # Legend
    legend_elements = [
        mpatches.Patch(color=Neo4jColorPalette.NODE_STOCK, label='Stock (Central Node)'),
        mpatches.Patch(color=Neo4jColorPalette.NODE_FACTOR, label='Factor Categories'),
        mpatches.Rectangle((0, 0), 1, 0.1, facecolor=Neo4jColorPalette.REL_INFLUENCES,
                          alpha=0.7, label='INFLUENCES Relationship')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
             frameon=True, fancybox=True, shadow=True)

    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4.5, 4.5)
    ax.set_aspect('equal')

    filename = f'{output_prefix}_neo4j_baseline_weights.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=Neo4jColorPalette.BG_COLOR)
    print(f"✅ Generated: {filename}")
    plt.close()


def create_neo4j_regime_graph(output_prefix: str):
    """
    Neo4j-style graph showing regime-dependent weight changes

    Visualization:
    - Central stock node
    - 4 regime nodes (Bull, Bear, High Vol, Sideways)
    - Top 3 factors for each regime
    - Weighted relationships showing regime-specific allocations
    """

    # Regime data from Table 5
    regimes = {
        'BULL': {
            'label': 'Bull\nMarket',
            'color': '#27AE60',
            'factors': [('Micro', 0.32), ('Technical', 0.18), ('Options', 0.15)]
        },
        'BEAR': {
            'label': 'Bear\nMarket',
            'color': '#E74C3C',
            'factors': [('Options', 0.25), ('Order Flow', 0.22), ('Macro', 0.12)]
        },
        'HIGH_VOL': {
            'label': 'High\nVolatility',
            'color': '#F39C12',
            'factors': [('Options', 0.30), ('Order Flow', 0.25), ('News', 0.15)]
        },
        'SIDEWAYS': {
            'label': 'Sideways\nNormal',
            'color': '#3498DB',
            'factors': [('Micro', 0.28), ('Order Flow', 0.18), ('Options', 0.15)]
        }
    }

    # Create figure
    fig, ax = plt.subplots(figsize=(20, 16))
    fig.patch.set_facecolor(Neo4jColorPalette.BG_COLOR)
    ax.set_facecolor(Neo4jColorPalette.BG_GRAPH)
    ax.axis('off')

    # Central stock node
    stock_node = Neo4jNode('STOCK', 'Stock\nPrice', 'stock')
    stock_pos = (0, 0)

    # Position regimes in circle
    regime_radius = 4.0
    regime_positions = {}

    for i, (regime_id, regime_data) in enumerate(regimes.items()):
        angle = 2 * np.pi * i / len(regimes) - np.pi / 2
        x = regime_radius * np.cos(angle)
        y = regime_radius * np.sin(angle)
        regime_positions[regime_id] = (x, y)

        # Create regime node
        regime_node = Neo4jNode(regime_id, regime_data['label'], 'regime')

        # Draw regime node
        circle = Circle((x, y), 0.5,
                       facecolor=regime_data['color'],
                       edgecolor='white',
                       linewidth=3,
                       zorder=10)
        ax.add_patch(circle)

        ax.text(x, y, regime_data['label'],
               ha='center', va='center',
               fontsize=12, weight='bold',
               color='white',
               zorder=11)

        # Draw relationship to stock
        draw_neo4j_relationship(
            ax, x, y, stock_pos[0], stock_pos[1],
            label='AFFECTS',
            color=regime_data['color'],
            linewidth=3.0,
            curvature=0.1
        )

        # Draw top 3 factors for this regime
        for j, (factor_name, weight) in enumerate(regime_data['factors']):
            factor_angle = angle + (j - 1) * 0.3
            factor_radius = regime_radius + 1.8
            fx = factor_radius * np.cos(factor_angle)
            fy = factor_radius * np.sin(factor_angle)

            # Factor node (small)
            factor_circle = Circle((fx, fy), 0.35,
                                  facecolor=Neo4jColorPalette.NODE_FACTOR,
                                  edgecolor='white',
                                  linewidth=2,
                                  zorder=8)
            ax.add_patch(factor_circle)

            ax.text(fx, fy, factor_name,
                   ha='center', va='center',
                   fontsize=9, weight='bold',
                   color='white',
                   zorder=9)

            # Relationship to regime
            draw_neo4j_relationship(
                ax, fx, fy, x, y,
                label=f'w={weight:.2f}',
                color=regime_data['color'],
                linewidth=weight * 10,
                curvature=0.05
            )

    # Draw central stock node
    draw_neo4j_node(ax, stock_pos[0], stock_pos[1], stock_node, radius=0.7)

    # Title
    ax.text(0, 6.5, 'Regime-Dependent Weight Allocations\n(Neo4j Knowledge Graph)',
           fontsize=22, weight='bold', ha='center', va='top',
           color=Neo4jColorPalette.TEXT_PRIMARY)

    # Regime legend
    legend_y = -6.5
    ax.text(0, legend_y, 'Market Regimes:',
           fontsize=12, weight='bold', ha='center', va='top',
           color=Neo4jColorPalette.TEXT_PRIMARY)

    regime_texts = [
        'Bull: ↑ Micro (0.32), ↑ Technical (0.18)',
        'Bear: ↑ Options (0.25), ↑ Order Flow (0.22), ↑ Macro (0.12)',
        'High Vol: ↑↑ Options (0.30), ↑ Order Flow (0.25)',
        'Sideways: Balanced allocation (baseline)'
    ]

    for i, text in enumerate(regime_texts):
        ax.text(0, legend_y - 0.4 - i * 0.35, text,
               fontsize=10, ha='center', va='top', style='italic',
               color=Neo4jColorPalette.TEXT_SECONDARY)

    ax.set_xlim(-7, 7)
    ax.set_ylim(-7.5, 7)
    ax.set_aspect('equal')

    filename = f'{output_prefix}_neo4j_regime_graph.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=Neo4jColorPalette.BG_COLOR)
    print(f"✅ Generated: {filename}")
    plt.close()


def create_neo4j_heat_propagation_graph(output_prefix: str):
    """
    Neo4j-style heat propagation graph across temporal layers

    Visualization:
    - 4 temporal layers (t=0 to t=3)
    - Nodes color-coded by heat intensity
    - Heat decay relationships
    - Neo4j aesthetic
    """

    # Create figure
    fig, ax = plt.subplots(figsize=(22, 14))
    fig.patch.set_facecolor(Neo4jColorPalette.BG_COLOR)
    ax.set_facecolor(Neo4jColorPalette.BG_GRAPH)
    ax.axis('off')

    # Layer data
    layers = {
        0: [('EVENT', 'Market\nEvent', 1.00)],
        1: [
            ('STOCK', 'Target\nStock', 0.85),
            ('SECTOR_ETF', 'Sector\nETF', 0.78),
            ('INDEX', 'Sector\nIndex', 0.72)
        ],
        2: [
            ('PEER1', 'Peer\nStock 1', 0.55),
            ('PEER2', 'Peer\nStock 2', 0.50),
            ('SUPPLIER', 'Key\nSupplier', 0.48),
            ('CUSTOMER', 'Major\nCustomer', 0.52),
        ],
        3: [
            ('CALLS', 'Call\nOptions', 0.32),
            ('PUTS', 'Put\nOptions', 0.28),
            ('FUTURES', 'Index\nFutures', 0.30),
            ('INTL1', 'Intl\nPeer 1', 0.25),
            ('INTL2', 'Intl\nPeer 2', 0.27),
        ]
    }

    # Position nodes
    node_positions = {}
    layer_x_positions = [-6, -2, 2, 6]

    for layer_idx, nodes in layers.items():
        x = layer_x_positions[layer_idx]
        n_nodes = len(nodes)
        y_spacing = 1.8
        y_start = -(n_nodes - 1) * y_spacing / 2

        for i, (node_id, label, heat) in enumerate(nodes):
            y = y_start + i * y_spacing
            node_positions[node_id] = (x, y, heat, label)

    # Draw relationships (edges)
    # Layer 0 → Layer 1
    for target_id in ['STOCK', 'SECTOR_ETF', 'INDEX']:
        x1, y1, h1, _ = node_positions['EVENT']
        x2, y2, h2, _ = node_positions[target_id]

        draw_neo4j_relationship(
            ax, x1, y1, x2, y2,
            label=f'PROPAGATES\nh={h2:.2f}',
            color=Neo4jColorPalette.REL_HEAT,
            linewidth=h2 * 5,
            curvature=0.1
        )

    # Layer 1 → Layer 2
    for source_id in ['STOCK', 'SECTOR_ETF']:
        for target_id in ['PEER1', 'PEER2', 'SUPPLIER', 'CUSTOMER']:
            x1, y1, h1, _ = node_positions[source_id]
            x2, y2, h2, _ = node_positions[target_id]

            draw_neo4j_relationship(
                ax, x1, y1, x2, y2,
                label='',
                color=Neo4jColorPalette.REL_HEAT,
                linewidth=h2 * 4,
                curvature=0.15,
                zorder=0
            )

    # Layer 2 → Layer 3
    for source_id in ['PEER1', 'PEER2', 'SUPPLIER']:
        for target_id in ['CALLS', 'PUTS', 'FUTURES', 'INTL1', 'INTL2']:
            x1, y1, h1, _ = node_positions[source_id]
            x2, y2, h2, _ = node_positions[target_id]

            # Only draw some relationships to avoid clutter
            if np.random.random() < 0.4:
                draw_neo4j_relationship(
                    ax, x1, y1, x2, y2,
                    label='',
                    color=Neo4jColorPalette.REL_HEAT,
                    linewidth=h2 * 3,
                    curvature=0.2,
                    zorder=0
                )

    # Draw nodes
    for node_id, (x, y, heat, label) in node_positions.items():
        # Color based on heat intensity
        if heat >= 0.7:
            color = '#E74C3C'  # Red (high heat)
        elif heat >= 0.5:
            color = '#F39C12'  # Orange (medium heat)
        elif heat >= 0.3:
            color = '#F1C40F'  # Yellow (low heat)
        else:
            color = '#95A5A6'  # Gray (very low heat)

        # Node size based on heat
        radius = 0.25 + heat * 0.25

        # Draw shadow
        shadow = Circle((x + 0.015, y - 0.015), radius,
                       facecolor=Neo4jColorPalette.SHADOW_COLOR,
                       alpha=0.15,
                       zorder=9)
        ax.add_patch(shadow)

        # Draw node
        circle = Circle((x, y), radius,
                       facecolor=color,
                       edgecolor='white',
                       linewidth=2.5,
                       zorder=10)
        ax.add_patch(circle)

        # Label
        ax.text(x, y, label,
               ha='center', va='center',
               fontsize=9, weight='bold',
               color='white',
               zorder=11)

        # Heat value below node
        ax.text(x, y - radius - 0.22, f'h={heat:.2f}',
               ha='center', va='top',
               fontsize=9,
               bbox=dict(boxstyle='round,pad=0.25',
                        facecolor='white',
                        alpha=0.9),
               zorder=11)

    # Layer labels
    layer_labels = ['t=0\nEvent\nSource', 't=1\nDirect\nImpact',
                   't=2\nSecondary\nImpact', 't=3\nTertiary\nImpact']

    for i, (x_pos, label_text) in enumerate(zip(layer_x_positions, layer_labels)):
        ax.text(x_pos, 5.5, label_text,
               ha='center', va='center',
               fontsize=13, weight='bold',
               color='white',
               bbox=dict(boxstyle='round,pad=0.5',
                        facecolor=Neo4jColorPalette.NODE_FACTOR,
                        edgecolor='white',
                        linewidth=2))

    # Title
    ax.text(0, 6.8, 'Multi-Hop Heat Propagation Across Temporal Layers\n(Neo4j Knowledge Graph)',
           fontsize=22, weight='bold', ha='center', va='top',
           color=Neo4jColorPalette.TEXT_PRIMARY)

    # Heat equation
    equation_text = r'$h(t) = e^{-\beta L t} \cdot h_0$'
    ax.text(0, -6.0, equation_text,
           fontsize=16, ha='center', va='bottom',
           bbox=dict(boxstyle='round,pad=0.6',
                    facecolor='#FFF9C4',
                    edgecolor=Neo4jColorPalette.NODE_REGIME,
                    linewidth=2))

    # Heat decay pattern
    decay_text = 'Heat Decay: t=0 (h=1.00) → t=1 (h≈0.78) → t=2 (h≈0.50) → t=3 (h≈0.28)'
    ax.text(0, -6.6, decay_text,
           fontsize=11, ha='center', va='bottom', style='italic',
           color=Neo4jColorPalette.TEXT_SECONDARY)

    # Heat intensity legend
    legend_elements = [
        mpatches.Patch(color='#E74C3C', label='High Heat (h ≥ 0.7)'),
        mpatches.Patch(color='#F39C12', label='Medium Heat (0.5 ≤ h < 0.7)'),
        mpatches.Patch(color='#F1C40F', label='Low Heat (0.3 ≤ h < 0.5)'),
        mpatches.Patch(color='#95A5A6', label='Very Low Heat (h < 0.3)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=11,
             frameon=True, fancybox=True, shadow=True)

    ax.set_xlim(-8, 8)
    ax.set_ylim(-7, 7.5)
    ax.set_aspect('equal')

    filename = f'{output_prefix}_neo4j_heat_propagation.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=Neo4jColorPalette.BG_COLOR)
    print(f"✅ Generated: {filename}")
    plt.close()


def create_neo4j_complete_knowledge_graph(output_prefix: str, ticker: str = 'STOCK'):
    """
    Neo4j-style complete knowledge graph with all entity types

    Comprehensive visualization showing:
    - Stock (central)
    - Factor categories
    - Individual entities
    - Events
    - Derivatives
    - Participants
    - Media sources
    """

    # Create figure
    fig, ax = plt.subplots(figsize=(24, 20))
    fig.patch.set_facecolor(Neo4jColorPalette.BG_COLOR)
    ax.set_facecolor(Neo4jColorPalette.BG_GRAPH)
    ax.axis('off')

    # Central stock node
    stock_node = Neo4jNode(ticker, f'{ticker}\nStock', 'stock',
                          {'price': '$XXX.XX', 'heat': '1.0'})
    stock_pos = (0, 0)

    # Factor categories (inner circle)
    factors = [
        ('MICRO', 'Microeconomic', 0.28),
        ('ORDER', 'Order Flow', 0.18),
        ('OPTIONS', 'Options Flow', 0.15),
        ('TECH', 'Technical', 0.12),
        ('NEWS', 'News', 0.10),
        ('SOCIAL', 'Social Media', 0.08),
    ]

    factor_radius = 3.5
    factor_positions = {}

    for i, (fid, label, weight) in enumerate(factors):
        angle = 2 * np.pi * i / len(factors) - np.pi / 2
        x = factor_radius * np.cos(angle)
        y = factor_radius * np.sin(angle)
        factor_positions[fid] = (x, y, weight)

        # Draw factor node
        node = Neo4jNode(fid, label, 'factor', {'weight': f'{weight:.2f}'})
        draw_neo4j_node(ax, x, y, node, radius=0.5, show_properties=True)

        # Relationship to stock
        draw_neo4j_relationship(
            ax, x, y, stock_pos[0], stock_pos[1],
            label=f'w={weight:.2f}',
            color=Neo4jColorPalette.REL_INFLUENCES,
            linewidth=weight * 12,
            curvature=0.0
        )

    # Entity nodes (outer circle) - specific examples for each factor
    entities = [
        # Microeconomic entities
        ('EARNINGS', 'Earnings\nReport', 'entity', 'MICRO'),
        ('REVENUE', 'Revenue\nGrowth', 'entity', 'MICRO'),

        # Order flow entities
        ('VWAP', 'VWAP', 'entity', 'ORDER'),
        ('SPREAD', 'Bid-Ask\nSpread', 'entity', 'ORDER'),

        # Options entities
        ('IV', 'Implied\nVolatility', 'derivative', 'OPTIONS'),
        ('GAMMA', 'Gamma\nExposure', 'derivative', 'OPTIONS'),

        # Technical entities
        ('RSI', 'RSI', 'entity', 'TECH'),
        ('MACD', 'MACD', 'entity', 'TECH'),

        # News entities
        ('BLOOMBERG', 'Bloomberg', 'media', 'NEWS'),
        ('CNBC', 'CNBC', 'media', 'NEWS'),

        # Social entities
        ('TWITTER', 'Twitter/X', 'media', 'SOCIAL'),
        ('REDDIT', 'Reddit\nWSB', 'media', 'SOCIAL'),
    ]

    entity_radius = 6.5

    for i, (eid, label, etype, parent_factor) in enumerate(entities):
        # Distribute around circle
        angle = 2 * np.pi * i / len(entities) - np.pi / 2
        x = entity_radius * np.cos(angle)
        y = entity_radius * np.sin(angle)

        # Draw entity node
        node = Neo4jNode(eid, label, etype)
        draw_neo4j_node(ax, x, y, node, radius=0.38, show_properties=False, zorder=8)

        # Relationship to parent factor
        if parent_factor in factor_positions:
            fx, fy, _ = factor_positions[parent_factor]
            draw_neo4j_relationship(
                ax, x, y, fx, fy,
                label='',
                color=Neo4jColorPalette.REL_CORRELATES,
                linewidth=1.5,
                curvature=0.1,
                zorder=1
            )

    # Draw central stock node (on top)
    draw_neo4j_node(ax, stock_pos[0], stock_pos[1], stock_node,
                   radius=0.7, show_properties=False, zorder=15)

    # Title
    ax.text(0, 8.5, f'{ticker} Stock Heat Diffusion Model\nComplete Knowledge Graph (Neo4j Style)',
           fontsize=24, weight='bold', ha='center', va='top',
           color=Neo4jColorPalette.TEXT_PRIMARY)

    # Statistics box
    stats_text = (
        f'Nodes: {1 + len(factors) + len(entities)}\n'
        f'Relationships: {len(factors) + len(entities)}\n'
        f'Node Types: 5 (Stock, Factor, Entity, Derivative, Media)'
    )
    ax.text(-7.5, -7.5, stats_text,
           fontsize=11,
           bbox=dict(boxstyle='round,pad=0.6',
                    facecolor='white',
                    edgecolor=Neo4jColorPalette.NODE_FACTOR,
                    linewidth=2),
           verticalalignment='bottom')

    # Legend
    legend_elements = [
        mpatches.Patch(color=Neo4jColorPalette.NODE_STOCK, label='Stock'),
        mpatches.Patch(color=Neo4jColorPalette.NODE_FACTOR, label='Factor Category'),
        mpatches.Patch(color=Neo4jColorPalette.NODE_ENTITY, label='Entity'),
        mpatches.Patch(color=Neo4jColorPalette.NODE_DERIVATIVE, label='Derivative'),
        mpatches.Patch(color=Neo4jColorPalette.NODE_MEDIA, label='Media Source'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=12,
             frameon=True, fancybox=True, shadow=True, ncol=2)

    # Constraint
    constraint_text = r'$\sum_{i=1}^{10} w_i(t) = 1.0$'
    ax.text(7.5, -7.5, constraint_text,
           fontsize=13, ha='right', va='bottom', weight='bold',
           color=Neo4jColorPalette.NODE_STOCK,
           bbox=dict(boxstyle='round,pad=0.5',
                    facecolor='white',
                    edgecolor=Neo4jColorPalette.NODE_STOCK,
                    linewidth=2))

    ax.set_xlim(-9, 9)
    ax.set_ylim(-9, 9)
    ax.set_aspect('equal')

    filename = f'{output_prefix}_neo4j_complete_graph.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor=Neo4jColorPalette.BG_COLOR)
    print(f"✅ Generated: {filename}")
    plt.close()


def main():
    """Generate all Neo4j-style visualizations"""

    print("=" * 80)
    print("GENERATING NEO4J-STYLE GRAPH VISUALIZATIONS")
    print("Stock Heat Diffusion Model - Production-Ready Neo4j Aesthetic")
    print("=" * 80)
    print()

    ticker = "STOCK"
    output_prefix = "paper"

    print(f"📊 Generating Neo4j-style graphs for: {ticker}")
    print(f"📁 Output prefix: {output_prefix}_neo4j_*.png")
    print()
    print("🎨 Creating visualizations...")
    print()

    # Generate all Neo4j-style visualizations
    create_neo4j_baseline_weights_graph(output_prefix)
    create_neo4j_regime_graph(output_prefix)
    create_neo4j_heat_propagation_graph(output_prefix)
    create_neo4j_complete_knowledge_graph(output_prefix, ticker)

    print()
    print("=" * 80)
    print("✅ ALL NEO4J-STYLE VISUALIZATIONS GENERATED SUCCESSFULLY")
    print("=" * 80)
    print()
    print("📋 Generated Files:")
    print("   1. paper_neo4j_baseline_weights.png    - Baseline weight allocation graph")
    print("   2. paper_neo4j_regime_graph.png        - Regime-dependent weight graph")
    print("   3. paper_neo4j_heat_propagation.png    - Temporal heat propagation graph")
    print("   4. paper_neo4j_complete_graph.png      - Complete knowledge graph")
    print()
    print("🎨 Style: Neo4j Browser Aesthetic")
    print("   - Large circular nodes with centered labels")
    print("   - Curved relationships with arrows")
    print("   - Professional Neo4j color palette")
    print("   - Drop shadows for depth")
    print("   - Clean white background")
    print()
    print("📐 Resolution: 300 DPI (publication quality)")
    print("🎨 Color: Neo4j standard palette")
    print("📊 Data: From paper Tables 1, 2, 3, 5")
    print()
    print("🏆 PRODUCTION-READY FOR SUBMISSION")
    print("=" * 80)


if __name__ == "__main__":
    main()
