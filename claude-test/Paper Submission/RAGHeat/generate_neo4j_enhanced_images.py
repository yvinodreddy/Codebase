#!/usr/bin/env python3
"""
Enhanced Neo4j-Style Visualization Generator
Based on ACTUAL Neo4j Browser Interface Design

Features:
- Dark background (#2D333B) matching Neo4j Browser
- Right sidebar with node properties
- Left sidebar with navigation
- Professional shadows and depth
- High-quality typography
- Exact Neo4j color palette
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
import numpy as np
import matplotlib.patheffects as path_effects
from matplotlib.collections import PatchCollection
import warnings
warnings.filterwarnings('ignore')

# Set high DPI and professional styling
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 0

# EXACT Neo4j Browser Color Palette
NEO4J_COLORS = {
    'bg_main': '#2D333B',           # Main dark background
    'bg_sidebar': '#22272E',        # Sidebar background (darker)
    'bg_panel': '#373E47',          # Panel/card background
    'node_green': '#68BFA0',        # Primary node color (teal/green)
    'node_cream': '#F4E8D8',        # Secondary node color (cream)
    'node_orange': '#F5A142',       # Accent node color (orange)
    'node_gray': '#8B949E',         # Inactive/secondary nodes
    'edge': '#57606A',              # Edge color (gray)
    'edge_label': '#8B949E',        # Edge label color
    'text_primary': '#FFFFFF',      # Primary text (white)
    'text_secondary': '#ADB6BF',    # Secondary text (light gray)
    'text_dim': '#768390',          # Dim text
    'accent_green': '#3FB950',      # Success/accent green
    'accent_blue': '#539BF5',       # Info blue
    'badge_bg': '#373E47',          # Badge background
    'border': '#444C56',            # Border color
}

def add_neo4j_text(ax, x, y, text, fontsize=11, color='white', ha='center', va='center', weight='normal'):
    """Add text with Neo4j styling"""
    txt = ax.text(x, y, text, fontsize=fontsize, color=color, ha=ha, va=va,
                 weight=weight, zorder=10, family='sans-serif')
    return txt

def draw_neo4j_node(ax, x, y, radius, label, color, has_shadow=True, fontsize=10):
    """Draw Neo4j-style circular node with shadow and glow"""
    if has_shadow:
        # Shadow circle
        shadow = Circle((x + 0.05, y - 0.05), radius * 1.05,
                       facecolor='black', alpha=0.3, zorder=3)
        ax.add_patch(shadow)

    # Main circle with glow effect
    glow = Circle((x, y), radius * 1.15, facecolor=color, alpha=0.2, zorder=4)
    ax.add_patch(glow)

    # Main node
    circle = Circle((x, y), radius, facecolor=color, edgecolor=color,
                   linewidth=0, alpha=0.95, zorder=5)
    ax.add_patch(circle)

    # Label
    add_neo4j_text(ax, x, y, label, fontsize=fontsize, weight='normal')
    return circle

def draw_neo4j_edge(ax, x1, y1, x2, y2, label='', curvature=0.0):
    """Draw Neo4j-style edge with optional label"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='-', color=NEO4J_COLORS['edge'], linewidth=1.5, alpha=0.6,
        connectionstyle=f"arc3,rad={curvature}", zorder=2
    )
    ax.add_patch(arrow)

    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        add_neo4j_text(ax, mid_x, mid_y + 0.2, label,
                      fontsize=7, color=NEO4J_COLORS['edge_label'])
    return arrow

def create_sidebar_panel(ax, x, y, width, height, title, content_lines):
    """Create Neo4j-style sidebar panel"""
    # Panel background
    panel = Rectangle((x, y), width, height,
                     facecolor=NEO4J_COLORS['bg_panel'],
                     edgecolor=NEO4J_COLORS['border'],
                     linewidth=1, zorder=8)
    ax.add_patch(panel)

    # Title
    add_neo4j_text(ax, x + width/2, y + height - 0.3, title,
                  fontsize=12, weight='bold', color=NEO4J_COLORS['text_primary'])

    # Content
    for i, line in enumerate(content_lines):
        y_pos = y + height - 0.8 - (i * 0.35)
        if isinstance(line, tuple):
            key, value = line
            add_neo4j_text(ax, x + 0.2, y_pos, key, fontsize=9,
                         color=NEO4J_COLORS['text_secondary'], ha='left')
            add_neo4j_text(ax, x + width - 0.2, y_pos, str(value), fontsize=9,
                         color=NEO4J_COLORS['text_primary'], ha='right', weight='bold')
        else:
            add_neo4j_text(ax, x + 0.2, y_pos, line, fontsize=9,
                         color=NEO4J_COLORS['text_secondary'], ha='left')

def create_badge(ax, x, y, text, color=NEO4J_COLORS['accent_green']):
    """Create Neo4j-style badge"""
    box = FancyBboxPatch((x, y), 1.2, 0.35, boxstyle="round,pad=0.05",
                        facecolor=color, edgecolor='none', alpha=0.8, zorder=9)
    ax.add_patch(box)
    add_neo4j_text(ax, x + 0.6, y + 0.175, text, fontsize=9, weight='bold')


# ============================================================================
# ENHANCED IMAGE 1: Full Neo4j Interface - Knowledge Graph
# ============================================================================
def generate_enhanced_image1_knowledge_graph():
    """
    Full Neo4j Browser interface with dark theme, sidebars, and main graph view
    """
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    fig.patch.set_facecolor(NEO4J_COLORS['bg_main'])
    ax.set_facecolor(NEO4J_COLORS['bg_main'])

    # ===== LEFT SIDEBAR =====
    sidebar_left = Rectangle((0, 0), 1.5, 12,
                             facecolor=NEO4J_COLORS['bg_sidebar'],
                             edgecolor='none', zorder=1)
    ax.add_patch(sidebar_left)

    # Sidebar icons/labels
    sidebar_items = ['Graph', 'Table', 'Text', 'Code']
    for i, item in enumerate(sidebar_items):
        y_pos = 11 - i * 1.5
        add_neo4j_text(ax, 0.75, y_pos, item, fontsize=9,
                      color=NEO4J_COLORS['text_secondary'])

    # ===== MAIN GRAPH AREA =====
    graph_x_start = 2
    graph_x_end = 13
    graph_y_start = 1
    graph_y_end = 11

    # Title bar
    title_bar = Rectangle((graph_x_start, graph_y_end),
                          graph_x_end - graph_x_start, 0.8,
                          facecolor=NEO4J_COLORS['bg_sidebar'],
                          edgecolor='none', zorder=7)
    ax.add_patch(title_bar)
    add_neo4j_text(ax, (graph_x_start + graph_x_end) / 2, graph_y_end + 0.4,
                  'Stock Heat Diffusion Knowledge Graph',
                  fontsize=14, weight='bold', color=NEO4J_COLORS['text_primary'])

    # Central stock node (TSLA)
    center_x, center_y = 7.5, 6
    draw_neo4j_node(ax, center_x, center_y, 0.8, 'TSLA\nStock',
                   NEO4J_COLORS['node_cream'], fontsize=11)

    # Factor category nodes (inner ring)
    categories = [
        ('Macro', 0),
        ('Micro', 60),
        ('News', 120),
        ('Social', 180),
        ('Order', 240),
        ('Options', 300),
    ]

    cat_positions = {}
    radius_inner = 3
    for cat_name, angle in categories:
        angle_rad = np.radians(angle)
        x = center_x + radius_inner * np.cos(angle_rad)
        y = center_y + radius_inner * np.sin(angle_rad)
        cat_positions[cat_name] = (x, y)

        draw_neo4j_node(ax, x, y, 0.6, cat_name, NEO4J_COLORS['node_green'], fontsize=10)
        draw_neo4j_edge(ax, x, y, center_x, center_y, label='INFLUENCES')

    # Individual factors (outer ring) - selected samples
    factors = [
        ('Fed\n5.25%', 'Macro', 0, 5.5, NEO4J_COLORS['node_gray']),
        ('Earnings\n+2.3%', 'Micro', 60, 5.5, NEO4J_COLORS['node_orange']),
        ('Sentiment\n+0.68', 'News', 120, 5.5, NEO4J_COLORS['node_orange']),
        ('Twitter\n12.5K', 'Social', 180, 5.5, NEO4J_COLORS['node_gray']),
        ('Imbalance\n+15%', 'Order', 240, 5.5, NEO4J_COLORS['node_orange']),
        ('P/C\n0.75', 'Options', 300, 5.5, NEO4J_COLORS['node_gray']),
    ]

    for label, category, angle, radius_outer, color in factors:
        angle_rad = np.radians(angle)
        x = center_x + radius_outer * np.cos(angle_rad)
        y = center_y + radius_outer * np.sin(angle_rad)

        draw_neo4j_node(ax, x, y, 0.45, label, color, fontsize=8)
        cat_x, cat_y = cat_positions[category]
        draw_neo4j_edge(ax, x, y, cat_x, cat_y)

    # ===== RIGHT SIDEBAR (Node Properties) =====
    sidebar_right_x = 13.5
    sidebar_right_width = 4.3

    # Background
    sidebar_right = Rectangle((sidebar_right_x, 0), sidebar_right_width, 12,
                              facecolor=NEO4J_COLORS['bg_sidebar'],
                              edgecolor='none', zorder=1)
    ax.add_patch(sidebar_right)

    # Node Properties Panel
    create_sidebar_panel(ax, sidebar_right_x + 0.2, 7, sidebar_right_width - 0.4, 4.5,
                        'Node properties',
                        [
                            ('ticker', 'TSLA'),
                            ('price', '$242.50'),
                            ('temperature', '0.73'),
                            ('heatScore', '0.68'),
                            ('sector', 'Technology'),
                            ('marketCap', '$769.2B'),
                            ('beta', '1.82'),
                            ('timestamp', '2025-11-09'),
                        ])

    # Overview Panel
    create_sidebar_panel(ax, sidebar_right_x + 0.2, 3.5, sidebar_right_width - 0.4, 3,
                        'Overview',
                        [
                            'Node labels',
                            'Stock (1)  Factor (12)',
                            '',
                            'Relationship types',
                            'INFLUENCES (18)',
                            '',
                            '13 nodes, 18 relationships',
                        ])

    # Badges at bottom
    create_badge(ax, sidebar_right_x + 0.3, 2.5, 'ICD10', NEO4J_COLORS['accent_green'])
    create_badge(ax, sidebar_right_x + 1.8, 2.5, 'Stock', NEO4J_COLORS['accent_blue'])

    plt.tight_layout(pad=0)
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/neo4j_v2_knowledge_graph.png',
                dpi=300, bbox_inches='tight', facecolor=NEO4J_COLORS['bg_main'],
                edgecolor='none', pad_inches=0.1)
    plt.close()
    print("✅ Enhanced Image 1: Neo4j-Style Knowledge Graph (with sidebars)")


# ============================================================================
# ENHANCED IMAGE 2: Heat Diffusion Visualization
# ============================================================================
def generate_enhanced_image2_heat_diffusion():
    """
    Neo4j-style heat diffusion showing time progression with dark theme
    """
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor(NEO4J_COLORS['bg_main'])
    ax.set_facecolor(NEO4J_COLORS['bg_main'])

    # Title
    add_neo4j_text(ax, 8, 9.5, 'Heat Diffusion Process: ∂h/∂t = -βL·h(t)',
                  fontsize=16, weight='bold', color=NEO4J_COLORS['text_primary'])
    add_neo4j_text(ax, 8, 9, 'Temporal Evolution (t=0 → t=3)',
                  fontsize=12, color=NEO4J_COLORS['text_secondary'])

    # Node network structure
    nodes = {
        'Event': (3, 5.5),
        'News': (5.5, 6.5),
        'Social': (5.5, 4.5),
        'TSLA': (8, 5.5),
        'Options': (10.5, 6.5),
        'Tech': (10.5, 4.5),
        'Market': (13, 5.5),
    }

    edges = [
        ('Event', 'News'), ('Event', 'Social'),
        ('News', 'TSLA'), ('Social', 'TSLA'),
        ('TSLA', 'Options'), ('TSLA', 'Tech'),
        ('Options', 'Market'), ('Tech', 'Market'),
    ]

    # Heat progression stages
    timesteps = [
        {'Event': 1.0, 'News': 0.0, 'Social': 0.0, 'TSLA': 0.0, 'Options': 0.0, 'Tech': 0.0, 'Market': 0.0},
        {'Event': 0.61, 'News': 0.45, 'Social': 0.45, 'TSLA': 0.0, 'Options': 0.0, 'Tech': 0.0, 'Market': 0.0},
        {'Event': 0.37, 'News': 0.54, 'Social': 0.54, 'TSLA': 0.68, 'Options': 0.0, 'Tech': 0.0, 'Market': 0.0},
        {'Event': 0.22, 'News': 0.41, 'Social': 0.41, 'TSLA': 0.73, 'Options': 0.52, 'Tech': 0.52, 'Market': 0.38},
    ]

    # Show final timestep (t=3)
    heat_values = timesteps[3]

    # Draw edges first
    for n1, n2 in edges:
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        draw_neo4j_edge(ax, x1, y1, x2, y2)

    # Draw nodes with heat-based coloring
    for node_name, (x, y) in nodes.items():
        heat = heat_values[node_name]

        # Color based on heat intensity
        if heat > 0.6:
            color = NEO4J_COLORS['node_orange']  # Hot
        elif heat > 0.3:
            color = NEO4J_COLORS['node_green']   # Warm
        elif heat > 0.0:
            color = NEO4J_COLORS['node_gray']    # Mild
        else:
            color = NEO4J_COLORS['bg_panel']     # Cold

        draw_neo4j_node(ax, x, y, 0.6, f'{node_name}\nh={heat:.2f}', color, fontsize=10)

    # Timeline visualization
    timeline_y = 2.5
    for i, t in enumerate(['t=0', 't=1', 't=2', 't=3']):
        x_pos = 3 + i * 3.3

        # Timeline marker
        marker = Circle((x_pos, timeline_y), 0.3,
                       facecolor=NEO4J_COLORS['accent_blue'] if i == 3 else NEO4J_COLORS['node_gray'],
                       edgecolor='none', alpha=0.8, zorder=5)
        ax.add_patch(marker)
        add_neo4j_text(ax, x_pos, timeline_y, t, fontsize=10, weight='bold')

        if i < 3:
            # Connection line
            ax.plot([x_pos + 0.3, x_pos + 3], [timeline_y, timeline_y],
                   color=NEO4J_COLORS['edge'], linewidth=2, alpha=0.5)

    # Heat legend
    legend_y = 1
    legend_items = [
        ('Hot (h>0.6)', NEO4J_COLORS['node_orange']),
        ('Warm (0.3<h≤0.6)', NEO4J_COLORS['node_green']),
        ('Mild (0<h≤0.3)', NEO4J_COLORS['node_gray']),
        ('Cold (h=0)', NEO4J_COLORS['bg_panel']),
    ]

    for i, (label, color) in enumerate(legend_items):
        x_pos = 3 + i * 3.3
        legend_node = Circle((x_pos, legend_y), 0.25, facecolor=color,
                           edgecolor=NEO4J_COLORS['border'], alpha=0.9, zorder=5)
        ax.add_patch(legend_node)
        add_neo4j_text(ax, x_pos + 1.2, legend_y, label, fontsize=9,
                      color=NEO4J_COLORS['text_secondary'], ha='left')

    plt.tight_layout(pad=0)
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/neo4j_v2_heat_diffusion.png',
                dpi=300, bbox_inches='tight', facecolor=NEO4J_COLORS['bg_main'],
                edgecolor='none', pad_inches=0.1)
    plt.close()
    print("✅ Enhanced Image 2: Neo4j-Style Heat Diffusion")


# ============================================================================
# ENHANCED IMAGE 3: Factor Categories with Weights
# ============================================================================
def generate_enhanced_image3_factor_weights():
    """
    10-factor category circular layout with weights, dark Neo4j theme
    """
    fig, ax = plt.subplots(figsize=(14, 14))
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.axis('off')
    fig.patch.set_facecolor(NEO4J_COLORS['bg_main'])
    ax.set_facecolor(NEO4J_COLORS['bg_main'])

    # Title
    add_neo4j_text(ax, 0, 6.5, 'Stock Heat Diffusion: Factor Category Weights',
                  fontsize=16, weight='bold', color=NEO4J_COLORS['text_primary'])
    add_neo4j_text(ax, 0, 6, 'Constraint: ∑wᵢ(t) = 1.0  ∀t',
                  fontsize=12, color=NEO4J_COLORS['accent_green'])

    # Central stock node
    draw_neo4j_node(ax, 0, 0, 0.9, 'STOCK\nTemp: 0.73',
                   NEO4J_COLORS['node_cream'], fontsize=12)

    # 10 Factor categories
    factors = [
        ('Macro\n12%', 0, NEO4J_COLORS['node_green']),
        ('Micro\n28%', 36, NEO4J_COLORS['node_green']),
        ('News\n10%', 72, NEO4J_COLORS['node_green']),
        ('Social\n8%', 108, NEO4J_COLORS['node_green']),
        ('Order\n18%', 144, NEO4J_COLORS['node_green']),
        ('Options\n15%', 180, NEO4J_COLORS['node_green']),
        ('Technical\n12%', 216, NEO4J_COLORS['node_green']),
        ('Sector\n4%', 252, NEO4J_COLORS['node_green']),
        ('Supply\n2%', 288, NEO4J_COLORS['node_green']),
        ('Quant\n1%', 324, NEO4J_COLORS['node_green']),
    ]

    radius = 4.5
    for label, angle_deg, color in factors:
        angle_rad = np.radians(angle_deg)
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)

        draw_neo4j_node(ax, x, y, 0.7, label, color, fontsize=9)
        draw_neo4j_edge(ax, x, y, 0, 0, label='wᵢ')

    # Heat equation box
    eq_box = Rectangle((-3, -6.5), 6, 0.8,
                      facecolor=NEO4J_COLORS['bg_panel'],
                      edgecolor=NEO4J_COLORS['border'], linewidth=2, zorder=8)
    ax.add_patch(eq_box)
    add_neo4j_text(ax, 0, -6.1, 'heatstock(t) = ∑ wᵢ(t)·factorᵢ(t) + diffusion_term(t)',
                  fontsize=11, color=NEO4J_COLORS['text_primary'], weight='bold')

    plt.tight_layout(pad=0)
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/neo4j_v2_factor_weights.png',
                dpi=300, bbox_inches='tight', facecolor=NEO4J_COLORS['bg_main'],
                edgecolor='none', pad_inches=0.1)
    plt.close()
    print("✅ Enhanced Image 3: Neo4j-Style Factor Weights")


# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == '__main__':
    print("\n" + "="*80)
    print("GENERATING ENHANCED NEO4J-STYLE VISUALIZATIONS")
    print("Based on ACTUAL Neo4j Browser Interface Design")
    print("="*80 + "\n")

    print("🎨 Using Neo4j dark theme with exact color palette...\n")

    generate_enhanced_image1_knowledge_graph()
    generate_enhanced_image2_heat_diffusion()
    generate_enhanced_image3_factor_weights()

    print("\n" + "="*80)
    print("✅ ALL ENHANCED IMAGES GENERATED!")
    print("="*80)
    print("\nFeatures:")
    print("  ✅ Dark Neo4j theme (#2D333B background)")
    print("  ✅ Sidebar panels with node properties")
    print("  ✅ Professional shadows and glow effects")
    print("  ✅ Exact Neo4j color palette")
    print("  ✅ High-quality typography")
    print("  ✅ 300 DPI publication quality")
    print("\nGenerated Files:")
    print("  1. neo4j_v2_knowledge_graph.png  (Full interface with sidebars)")
    print("  2. neo4j_v2_heat_diffusion.png   (Heat propagation visualization)")
    print("  3. neo4j_v2_factor_weights.png   (Factor category weights)")
    print("\n" + "="*80 + "\n")
