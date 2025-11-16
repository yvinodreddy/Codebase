#!/usr/bin/env python3
"""
Create professional Neo4j-style network graphs for Stock Heat Diffusion Model paper
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx

# High-quality settings
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 9

# Professional color palette (Neo4j inspired - LIGHT TO DARK)
COLORS = {
    'stock': '#E8697D',        # Soft red/coral - center node
    'category': '#7C9FCC',     # Soft blue - factor categories
    'factor': '#A3D5A3',       # Soft green - individual factors
    'edge': '#CCCCCC',         # Light gray edges
    'text': '#2C3E50',         # Dark blue-gray text
    'bg': '#FAFBFC',           # Very light background
    'legend_bg': '#FFFFFF'     # White legend background
}


def draw_professional_node(ax, x, y, radius, color, label, weight_text='',
                           outline_color='#34495E', zorder=10):
    """
    Draw a professional node with light-to-dark gradient (Neo4j style)
    """
    # Create light-to-dark radial gradient
    resolution = 100
    Y, X = np.ogrid[-radius:radius:resolution*1j, -radius:radius:resolution*1j]
    R = np.sqrt(X**2 + Y**2)

    # Light in center, darker at edges (NOT black)
    light_center = np.array([int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)])
    dark_edge = (light_center * 0.6).astype(int)  # 40% darker, NOT black

    gradient = np.zeros((resolution, resolution, 4))
    mask = R <= radius

    for i in range(resolution):
        for j in range(resolution):
            if mask[i, j]:
                t = min(R[i, j] / radius, 1.0)
                # Interpolate from light to dark
                rgb = light_center * (1 - t) + dark_edge * t
                gradient[i, j, :3] = rgb / 255
                gradient[i, j, 3] = 1.0

    # Draw gradient
    ax.imshow(gradient, extent=[x-radius, x+radius, y-radius, y+radius],
              origin='lower', zorder=zorder, interpolation='bilinear')

    # Outline
    circle_outline = Circle((x, y), radius, fill=False, edgecolor=outline_color,
                           linewidth=1.5, zorder=zorder+1)
    ax.add_patch(circle_outline)

    # Label text
    if label:
        ax.text(x, y, label, ha='center', va='center', fontsize=9,
               fontweight='bold', color='white', zorder=zorder+2)

    # Weight badge (below node)
    if weight_text:
        badge = FancyBboxPatch((x-0.3, y-radius-0.35), 0.6, 0.25,
                              boxstyle="round,pad=0.05",
                              facecolor='white', edgecolor=outline_color,
                              linewidth=1, zorder=zorder+2)
        ax.add_patch(badge)
        ax.text(x, y-radius-0.225, weight_text, ha='center', va='center',
               fontsize=7, color=COLORS['text'], zorder=zorder+3, fontweight='bold')


def draw_edge(ax, x1, y1, x2, y2, color=COLORS['edge'], alpha=0.5, width=1.5, zorder=1):
    """Draw connection edge"""
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           connectionstyle="arc3,rad=0",
                           arrowstyle='-',
                           color=color, linewidth=width,
                           alpha=alpha, zorder=zorder)
    ax.add_patch(arrow)


def create_baseline_weights_graph():
    """
    Figure 1: Baseline Weight Allocation Network Graph
    """
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    # Title
    ax.text(0, 7.5, 'Baseline Weight Allocation',
           fontsize=16, fontweight='bold', ha='center', color=COLORS['text'])
    ax.text(0, 7, 'Risk Parity Approach - All Weights Sum to 1.0',
           fontsize=11, ha='center', color=COLORS['text'], style='italic')

    # Central stock node
    draw_professional_node(ax, 0, 0, 1.0, COLORS['stock'],
                          'Stock\nPrice', '', '#C0392B', zorder=20)

    # Factor categories with weights (from Table 1 in paper)
    factors = [
        ('Microeconomic', 0.28, 'Highest info content'),
        ('Order Flow', 0.18, 'Intraday predictive'),
        ('Options Flow', 0.15, 'Microstructure driver'),
        ('Technical', 0.12, 'Momentum/reversion'),
        ('News\nSentiment', 0.10, 'Event-driven'),
        ('Social Media', 0.08, 'Retail sentiment'),
        ('Sector\nCorrelation', 0.04, 'Market beta'),
        ('Macro', 0.03, 'Low frequency'),
        ('Supply Chain', 0.02, 'Slow-moving'),
    ]

    n_factors = len(factors)
    angles = np.linspace(0, 2*np.pi, n_factors, endpoint=False) - np.pi/2
    radius_dist = 5.0

    for i, ((name, weight, desc), angle) in enumerate(zip(factors, angles)):
        x = radius_dist * np.cos(angle)
        y = radius_dist * np.sin(angle)

        # Draw edge first (behind nodes)
        draw_edge(ax, 0, 0, x, y, color=COLORS['edge'], alpha=0.4, width=2, zorder=5)

        # Draw factor node
        node_radius = 0.4 + weight * 0.8  # Size proportional to weight
        draw_professional_node(ax, x, y, node_radius, COLORS['category'],
                              name, f'w={weight:.2f}', '#2C3E50', zorder=10)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['stock'], edgecolor='#C0392B',
                      label='Target Stock (Central Node)'),
        mpatches.Patch(facecolor=COLORS['category'], edgecolor='#2C3E50',
                      label='Factor Categories'),
        mpatches.Rectangle((0, 0), 1, 1, facecolor='none', edgecolor=COLORS['edge'],
                          linewidth=2, label='Influence Relationships')
    ]

    legend = ax.legend(handles=legend_elements, loc='upper left',
                      frameon=True, fancybox=True, shadow=True,
                      fontsize=9, bbox_to_anchor=(0.02, 0.98))
    legend.get_frame().set_facecolor(COLORS['legend_bg'])
    legend.get_frame().set_alpha(0.95)

    # Note about weight normalization
    note_box = FancyBboxPatch((-3.5, -7.5), 7, 0.8,
                             boxstyle="round,pad=0.1",
                             facecolor='#FFF9E6', edgecolor='#F39C12',
                             linewidth=2, zorder=30)
    ax.add_patch(note_box)
    ax.text(0, -7.1, r'Mathematical Constraint: $\sum_{i=1}^{10} w_i(t) = 1.0$ (Always Normalized)',
           fontsize=10, ha='center', va='center', color=COLORS['text'],
           fontweight='bold', zorder=31)

    plt.tight_layout()
    plt.savefig('GRAPH_baseline_weights.jpg', format='jpg', dpi=300,
                bbox_inches='tight', facecolor=COLORS['bg'])
    print("✓ Created GRAPH_baseline_weights.jpg")
    plt.close()


def create_regime_comparison_graph():
    """
    Figure 2: Regime-Dependent Weight Allocations
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 16))
    fig.patch.set_facecolor(COLORS['bg'])

    # Overall title
    fig.suptitle('Regime-Dependent Weight Configurations',
                fontsize=18, fontweight='bold', color=COLORS['text'], y=0.98)

    # Regime configurations (from Table 2 in paper)
    regimes = {
        'Bull Market': {
            'Micro': 0.32, 'Order': 0.08, 'Options': 0.15, 'Technical': 0.18,
            'News': 0.12, 'Social': 0.10, 'Sector': 0.03, 'Macro': 0.02, 'Supply': 0.00
        },
        'Bear Market': {
            'Micro': 0.20, 'Order': 0.22, 'Options': 0.25, 'Technical': 0.10,
            'News': 0.06, 'Social': 0.03, 'Sector': 0.02, 'Macro': 0.12, 'Supply': 0.00
        },
        'High Volatility': {
            'Micro': 0.15, 'Order': 0.25, 'Options': 0.30, 'Technical': 0.08,
            'News': 0.15, 'Social': 0.02, 'Sector': 0.00, 'Macro': 0.05, 'Supply': 0.00
        },
        'Sideways/Normal': {
            'Micro': 0.28, 'Order': 0.18, 'Options': 0.15, 'Technical': 0.12,
            'News': 0.10, 'Social': 0.08, 'Sector': 0.04, 'Macro': 0.03, 'Supply': 0.02
        }
    }

    regime_colors = {
        'Bull Market': '#27AE60',      # Green
        'Bear Market': '#E74C3C',      # Red
        'High Volatility': '#F39C12',  # Orange
        'Sideways/Normal': '#3498DB'   # Blue
    }

    axes_flat = axes.flatten()

    for idx, (regime_name, weights) in enumerate(regimes.items()):
        ax = axes_flat[idx]
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor(COLORS['bg'])

        # Regime title
        ax.text(0, 5.5, regime_name, fontsize=14, fontweight='bold',
               ha='center', color=regime_colors[regime_name])

        # Central stock node
        draw_professional_node(ax, 0, 0, 0.8, regime_colors[regime_name],
                              'Stock', '', '#2C3E50', zorder=20)

        # Factor nodes
        n_factors = len(weights)
        angles = np.linspace(0, 2*np.pi, n_factors, endpoint=False) - np.pi/2
        radius_dist = 4.0

        for i, ((name, weight), angle) in enumerate(zip(weights.items(), angles)):
            x = radius_dist * np.cos(angle)
            y = radius_dist * np.sin(angle)

            # Edge
            edge_width = 1 + weight * 4  # Width proportional to weight
            draw_edge(ax, 0, 0, x, y, color=COLORS['edge'],
                     alpha=0.3 + weight*0.5, width=edge_width, zorder=5)

            # Node size proportional to weight
            node_radius = 0.25 + weight * 0.6
            draw_professional_node(ax, x, y, node_radius, COLORS['category'],
                                  name, f'{weight:.2f}', '#2C3E50', zorder=10)

    # Overall legend
    legend_elements = [
        mpatches.Patch(facecolor=regime_colors['Bull Market'],
                      label='Bull: Emphasis on momentum & fundamentals'),
        mpatches.Patch(facecolor=regime_colors['Bear Market'],
                      label='Bear: Increase options & order flow'),
        mpatches.Patch(facecolor=regime_colors['High Volatility'],
                      label='High Vol: Heavy microstructure weights'),
        mpatches.Patch(facecolor=regime_colors['Sideways/Normal'],
                      label='Sideways: Balanced risk parity allocation')
    ]

    fig.legend(handles=legend_elements, loc='lower center', ncol=2,
              frameon=True, fancybox=True, shadow=True, fontsize=10,
              bbox_to_anchor=(0.5, -0.02))

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.savefig('GRAPH_regime_weights.jpg', format='jpg', dpi=300,
                bbox_inches='tight', facecolor=COLORS['bg'])
    print("✓ Created GRAPH_regime_weights.jpg")
    plt.close()


def create_heat_propagation_graph():
    """
    Figure 3: Heat Diffusion Through Network
    """
    fig, ax = plt.subplots(figsize=(14, 12))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    # Title
    ax.text(0, 7.5, 'Heat Propagation Through Financial Network',
           fontsize=16, fontweight='bold', ha='center', color=COLORS['text'])
    ax.text(0, 7, 'Multi-Hop Influence Diffusion from Event to Stock Price',
           fontsize=11, ha='center', color=COLORS['text'], style='italic')

    # Heat levels (temperature visualization)
    heat_cmap = LinearSegmentedColormap.from_list('heat',
                                                   ['#FFFACD', '#FFD700', '#FF8C00', '#FF4500'])

    # Event node (heat source) - HOT
    event_x, event_y = -5, 4
    draw_professional_node(ax, event_x, event_y, 0.7, '#FF4500',
                          'Fed Rate\nChange', 'Heat=1.0', '#8B0000', zorder=25)

    # First hop: Macro factor
    macro_x, macro_y = -2, 3
    draw_edge(ax, event_x, event_y, macro_x, macro_y,
             color='#FF6347', alpha=0.7, width=3, zorder=10)
    draw_professional_node(ax, macro_x, macro_y, 0.6, '#FF8C00',
                          'Macro\nFactors', 'Heat=0.75', '#8B4513', zorder=20)

    # Second hop: Multiple categories
    categories = [
        ('News', -1, 0, 0.55, '#FFD700'),
        ('Order\nFlow', 1, 1.5, 0.50, '#FFA500'),
        ('Technical', 2, -1, 0.45, '#FFB84D'),
    ]

    for name, cx, cy, heat, color in categories:
        draw_edge(ax, macro_x, macro_y, cx, cy,
                 color='#FFA500', alpha=0.6, width=2.5, zorder=8)
        draw_professional_node(ax, cx, cy, 0.55, color,
                              name, f'Heat={heat:.2f}', '#8B4513', zorder=18)

    # Third hop: Stock (final destination)
    stock_x, stock_y = 0, -3.5
    for name, cx, cy, heat, color in categories:
        draw_edge(ax, cx, cy, stock_x, stock_y,
                 color='#FFB84D', alpha=0.5, width=2, zorder=6)

    draw_professional_node(ax, stock_x, stock_y, 1.0, '#FFFACD',
                          'Stock\nPrice', 'Heat=0.35', '#DAA520', zorder=22)

    # Heat equation display
    equation_box = FancyBboxPatch((3, 3), 4.5, 3,
                                 boxstyle="round,pad=0.15",
                                 facecolor='white', edgecolor='#2C3E50',
                                 linewidth=2, zorder=30)
    ax.add_patch(equation_box)

    ax.text(5.25, 5.3, 'Heat Diffusion Equation', fontsize=11,
           fontweight='bold', ha='center', color=COLORS['text'], zorder=31)
    ax.text(5.25, 4.7, r'$\frac{\partial h(t)}{\partial t} = -\beta L \cdot h(t)$',
           fontsize=13, ha='center', color=COLORS['text'], zorder=31)
    ax.text(5.25, 4.2, r'$h(t) = e^{-\beta L t} \cdot h_0$',
           fontsize=12, ha='center', color=COLORS['text'], zorder=31)
    ax.text(5.25, 3.6, 'where L = Graph Laplacian', fontsize=9,
           ha='center', color=COLORS['text'], style='italic', zorder=31)

    # Heat legend
    legend_elements = [
        mpatches.Patch(facecolor='#FF4500', label='High Heat (Source: 1.0)'),
        mpatches.Patch(facecolor='#FF8C00', label='Medium-High Heat (0.5-0.8)'),
        mpatches.Patch(facecolor='#FFD700', label='Medium Heat (0.3-0.5)'),
        mpatches.Patch(facecolor='#FFFACD', label='Low Heat (Destination)'),
    ]

    legend = ax.legend(handles=legend_elements, loc='lower left',
                      frameon=True, fancybox=True, shadow=True, fontsize=9,
                      title='Heat Level', title_fontsize=10)
    legend.get_frame().set_facecolor(COLORS['legend_bg'])

    # Time steps annotation
    ax.text(-5, -6.5, 't=0: Event occurs', fontsize=9, color='#FF4500', fontweight='bold')
    ax.text(-5, -7, 't=1: First diffusion', fontsize=9, color='#FFA500', fontweight='bold')
    ax.text(-5, -7.5, 't=2-3: Multi-hop propagation', fontsize=9, color='#FFD700', fontweight='bold')

    plt.tight_layout()
    plt.savefig('GRAPH_heat_propagation.jpg', format='jpg', dpi=300,
                bbox_inches='tight', facecolor=COLORS['bg'])
    print("✓ Created GRAPH_heat_propagation.jpg")
    plt.close()


def create_complete_multilevel_graph():
    """
    Figure 4: Complete Multi-Level Knowledge Graph Structure
    """
    fig, ax = plt.subplots(figsize=(16, 14))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-9, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg'])
    ax.set_facecolor(COLORS['bg'])

    # Title
    ax.text(0, 8.5, 'Complete Knowledge Graph Architecture',
           fontsize=18, fontweight='bold', ha='center', color=COLORS['text'])
    ax.text(0, 7.8, 'Multi-Level Structure: Stock → Categories → Individual Factors',
           fontsize=12, ha='center', color=COLORS['text'], style='italic')

    # Level 1: Central stock
    draw_professional_node(ax, 0, 0, 1.2, COLORS['stock'],
                          'Target\nStock', '', '#C0392B', zorder=30)

    # Level 2: Category nodes (simplified - 6 main ones)
    categories = [
        ('Microeconomic\n(0.28)', 0),
        ('Order Flow\n(0.18)', 60),
        ('Options\n(0.15)', 120),
        ('Technical\n(0.12)', 180),
        ('News\n(0.10)', 240),
        ('Social\n(0.08)', 300),
    ]

    cat_radius = 5.0
    cat_nodes = {}

    for name, angle_deg in categories:
        angle = np.radians(angle_deg)
        x = cat_radius * np.cos(angle)
        y = cat_radius * np.sin(angle)

        # Edge to stock
        draw_edge(ax, 0, 0, x, y, color=COLORS['edge'],
                 alpha=0.4, width=2.5, zorder=10)

        # Category node
        draw_professional_node(ax, x, y, 0.8, COLORS['category'],
                              name, '', '#2C3E50', zorder=20)
        cat_nodes[name] = (x, y)

    # Level 3: Individual factor nodes (examples for first 3 categories)
    factor_examples = {
        'Microeconomic\n(0.28)': [
            ('Earnings', 0.10, 20),
            ('Revenue', 0.08, 340),
        ],
        'Order Flow\n(0.18)': [
            ('Bid-Ask', 0.06, 80),
            ('Imbalance', 0.07, 50),
        ],
        'Options\n(0.15)': [
            ('Put/Call', 0.05, 140),
            ('IV', 0.04, 110),
        ],
    }

    factor_radius = 8.0

    for cat_name, factors in factor_examples.items():
        cat_x, cat_y = cat_nodes[cat_name]

        for factor_name, weight, angle_deg in factors:
            angle = np.radians(angle_deg)
            fx = factor_radius * np.cos(angle)
            fy = factor_radius * np.sin(angle)

            # Edge from category to factor
            draw_edge(ax, cat_x, cat_y, fx, fy,
                     color='#B0B0B0', alpha=0.3, width=1.5, zorder=5)

            # Factor node (smaller, green)
            draw_professional_node(ax, fx, fy, 0.5, COLORS['factor'],
                                  factor_name, f'{weight:.2f}', '#27AE60', zorder=15)

    # Legend with all three levels
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['stock'], edgecolor='#C0392B',
                      label='Level 1: Target Stock (Central Node)'),
        mpatches.Patch(facecolor=COLORS['category'], edgecolor='#2C3E50',
                      label='Level 2: Factor Categories (10 total)'),
        mpatches.Patch(facecolor=COLORS['factor'], edgecolor='#27AE60',
                      label='Level 3: Individual Factors (100+ signals)'),
        mpatches.Rectangle((0, 0), 1, 1, facecolor='none', edgecolor=COLORS['edge'],
                          linewidth=2, label='Strong Relationships'),
        mpatches.Rectangle((0, 0), 1, 1, facecolor='none', edgecolor='#B0B0B0',
                          linewidth=1.5, label='Secondary Relationships'),
    ]

    legend = ax.legend(handles=legend_elements, loc='upper right',
                      frameon=True, fancybox=True, shadow=True, fontsize=10,
                      title='Graph Structure', title_fontsize=11)
    legend.get_frame().set_facecolor(COLORS['legend_bg'])
    legend.get_frame().set_alpha(0.95)

    # Architecture note
    note_box = FancyBboxPatch((-9.5, -8.5), 19, 1.3,
                             boxstyle="round,pad=0.15",
                             facecolor='#E8F8F5', edgecolor='#16A085',
                             linewidth=2, zorder=35)
    ax.add_patch(note_box)

    ax.text(0, -7.6, 'Graph Database Implementation: Neo4j Property Graph Model',
           fontsize=11, ha='center', fontweight='bold', color=COLORS['text'], zorder=36)
    ax.text(0, -8.15, 'Node Types: Stock, FactorCategory, Factor | Edge Types: INFLUENCES, CORRELATED_WITH | Properties: weight, heat, temperature',
           fontsize=9, ha='center', color=COLORS['text'], zorder=36, style='italic')

    # Node count annotations
    ax.text(-9, 7.5, 'Total Graph Size:', fontsize=10, fontweight='bold', color=COLORS['text'])
    ax.text(-9, 7, '• 1 Stock Node', fontsize=9, color=COLORS['text'])
    ax.text(-9, 6.5, '• 10 Category Nodes', fontsize=9, color=COLORS['text'])
    ax.text(-9, 6, '• 100+ Factor Nodes', fontsize=9, color=COLORS['text'])
    ax.text(-9, 5.5, '• 1000+ Edges', fontsize=9, color=COLORS['text'])

    plt.tight_layout()
    plt.savefig('GRAPH_complete_structure.jpg', format='jpg', dpi=300,
                bbox_inches='tight', facecolor=COLORS['bg'])
    print("✓ Created GRAPH_complete_structure.jpg")
    plt.close()


if __name__ == '__main__':
    print("Creating professional Neo4j-style network graphs...")
    print("=" * 60)

    create_baseline_weights_graph()
    create_regime_comparison_graph()
    create_heat_propagation_graph()
    create_complete_multilevel_graph()

    print("=" * 60)
    print("✓ All graphs created successfully!")
    print("\nGenerated files:")
    print("  • GRAPH_baseline_weights.jpg - Baseline weight allocation")
    print("  • GRAPH_regime_weights.jpg - Regime-dependent configurations")
    print("  • GRAPH_heat_propagation.jpg - Heat diffusion visualization")
    print("  • GRAPH_complete_structure.jpg - Complete multi-level architecture")
    print("\nThese graphs include:")
    print("  ✓ Light-to-dark gradients (NOT dark-to-black)")
    print("  ✓ All text labels and weight values")
    print("  ✓ Connection edges showing relationships")
    print("  ✓ Professional legends and annotations")
    print("  ✓ Multi-level network structure")
    print("  ✓ Neo4j-inspired styling")
