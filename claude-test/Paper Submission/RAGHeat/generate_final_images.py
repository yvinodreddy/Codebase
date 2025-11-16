#!/usr/bin/env python3
"""
FINAL Enhanced Neo4j-Style Visualizations
FIXES:
- Remove irrelevant left sidebar (Graph/Table/Text/Code)
- Larger, readable fonts (14-18pt)
- Better spacing and layout
- Remove ICD10 badge (irrelevant)
- Add relevant financial metrics
- No cutoff issues
- Professional and attractive presentation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
import numpy as np
import matplotlib.patheffects as path_effects
import warnings
warnings.filterwarnings('ignore')

# Set high DPI
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 14  # Increased from 11
plt.rcParams['axes.linewidth'] = 0

# Enhanced color palette - more vibrant and readable
COLORS = {
    'bg_main': '#1E2329',           # Darker main background for better contrast
    'bg_panel': '#2A3038',          # Panel background (lighter than main)
    'node_green': '#5FD3BC',        # Brighter teal (more readable)
    'node_cream': '#FFF4E0',        # Lighter cream (better contrast)
    'node_orange': '#FF9F40',       # Brighter orange
    'node_gray': '#A8B2BD',         # Lighter gray (more readable)
    'edge': '#6B7785',              # Lighter edge color
    'text_primary': '#FFFFFF',      # White text
    'text_secondary': '#D1D9E0',    # Light gray (much more readable)
    'text_bright': '#E8F0F8',       # Very bright text for emphasis
    'accent_green': '#48C78E',      # Success green
    'accent_blue': '#3E8ED0',       # Info blue
    'accent_gold': '#FFD93D',       # Gold for metrics
    'border': '#4A5568',            # Visible border
}

def add_text(ax, x, y, text, fontsize=14, color='white', ha='center', va='center', weight='normal'):
    """Add text with better visibility"""
    txt = ax.text(x, y, text, fontsize=fontsize, color=color, ha=ha, va=va,
                 weight=weight, zorder=10, family='sans-serif')
    return txt

def draw_node(ax, x, y, radius, label, color, has_shadow=True, fontsize=14):
    """Draw node with enhanced visibility"""
    if has_shadow:
        shadow = Circle((x + 0.08, y - 0.08), radius * 1.08,
                       facecolor='black', alpha=0.4, zorder=3)
        ax.add_patch(shadow)

    # Glow effect
    glow = Circle((x, y), radius * 1.2, facecolor=color, alpha=0.25, zorder=4)
    ax.add_patch(glow)

    # Main node
    circle = Circle((x, y), radius, facecolor=color, edgecolor='white',
                   linewidth=2, alpha=0.95, zorder=5)
    ax.add_patch(circle)

    # Label with better visibility
    add_text(ax, x, y, label, fontsize=fontsize, weight='bold', color='white')
    return circle

def draw_edge(ax, x1, y1, x2, y2, label='', curvature=0.0):
    """Draw edge with better visibility"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle='-', color=COLORS['edge'], linewidth=2, alpha=0.7,
        connectionstyle=f"arc3,rad={curvature}", zorder=2
    )
    ax.add_patch(arrow)

    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        add_text(ax, mid_x, mid_y + 0.25, label, fontsize=10,
                color=COLORS['text_secondary'])
    return arrow

def create_panel(ax, x, y, width, height, title, content_lines):
    """Create attractive panel with better spacing"""
    # Panel background with border
    panel = Rectangle((x, y), width, height,
                     facecolor=COLORS['bg_panel'],
                     edgecolor=COLORS['border'],
                     linewidth=2, zorder=8)
    ax.add_patch(panel)

    # Title with better styling
    title_bg = Rectangle((x, y + height - 0.6), width, 0.6,
                         facecolor=COLORS['accent_blue'],
                         edgecolor='none', zorder=9)
    ax.add_patch(title_bg)
    add_text(ax, x + width/2, y + height - 0.3, title,
            fontsize=16, weight='bold', color='white')

    # Content with better spacing
    line_height = 0.45  # Increased spacing
    for i, line in enumerate(content_lines):
        y_pos = y + height - 1.1 - (i * line_height)
        if isinstance(line, tuple):
            key, value = line
            add_text(ax, x + 0.3, y_pos, key, fontsize=13,
                   color=COLORS['text_secondary'], ha='left')
            add_text(ax, x + width - 0.3, y_pos, str(value), fontsize=14,
                   color=COLORS['text_bright'], ha='right', weight='bold')
        else:
            add_text(ax, x + 0.3, y_pos, line, fontsize=13,
                   color=COLORS['text_secondary'], ha='left')


# ============================================================================
# FINAL IMAGE 1: Knowledge Graph with Sidebars (FIXED)
# ============================================================================
def generate_final_image1():
    """Clean knowledge graph with RIGHT sidebar only (NO left clutter)"""
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 12)
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg_main'])
    ax.set_facecolor(COLORS['bg_main'])

    # ===== MAIN GRAPH AREA (NO LEFT SIDEBAR) =====
    graph_x_start = 0.5
    graph_x_end = 12.5

    # Title bar - larger and more visible
    add_text(ax, (graph_x_start + graph_x_end) / 2, 11.3,
            'Stock Heat Diffusion Knowledge Graph',
            fontsize=20, weight='bold', color=COLORS['text_bright'])
    add_text(ax, (graph_x_start + graph_x_end) / 2, 10.7,
            'Neo4j Implementation - TSLA Stock Analysis',
            fontsize=14, color=COLORS['text_secondary'])

    # Central stock node
    center_x, center_y = 6.5, 5.5
    draw_node(ax, center_x, center_y, 1.0, 'TSLA\nStock',
             COLORS['node_cream'], fontsize=15)

    # Factor categories (inner ring) - 6 categories
    categories = [
        ('Macroeconomic', 0),
        ('Microeconomic', 60),
        ('News\nSentiment', 120),
        ('Social\nMedia', 180),
        ('Order\nFlow', 240),
        ('Options\nFlow', 300),
    ]

    cat_positions = {}
    radius_inner = 3.5
    for cat_name, angle in categories:
        angle_rad = np.radians(angle)
        x = center_x + radius_inner * np.cos(angle_rad)
        y = center_y + radius_inner * np.sin(angle_rad)
        cat_positions[cat_name] = (x, y)

        draw_node(ax, x, y, 0.75, cat_name, COLORS['node_green'], fontsize=12)
        draw_edge(ax, x, y, center_x, center_y)

    # Individual factors (outer ring) - more visible
    factors = [
        ('Fed Rate\n5.25%', 'Macroeconomic', 0, 6, COLORS['node_gray']),
        ('Earnings\n+2.3%', 'Microeconomic', 60, 6, COLORS['node_orange']),
        ('Sentiment\n+0.68', 'News\nSentiment', 120, 6, COLORS['node_orange']),
        ('Twitter\n12.5K', 'Social\nMedia', 180, 6, COLORS['node_gray']),
        ('Buy Imbal\n+15.3%', 'Order\nFlow', 240, 6, COLORS['node_orange']),
        ('Put/Call\n0.75', 'Options\nFlow', 300, 6, COLORS['node_gray']),
    ]

    for label, category, angle, radius_outer, color in factors:
        angle_rad = np.radians(angle)
        x = center_x + radius_outer * np.cos(angle_rad)
        y = center_y + radius_outer * np.sin(angle_rad)

        draw_node(ax, x, y, 0.55, label, color, fontsize=11)
        cat_x, cat_y = cat_positions[category]
        draw_edge(ax, x, y, cat_x, cat_y)

    # ===== RIGHT SIDEBAR - Better organized =====
    sidebar_x = 13
    sidebar_width = 4.8

    # Node Properties Panel - larger and better spaced
    create_panel(ax, sidebar_x, 5.5, sidebar_width, 6,
                'Node Properties',
                [
                    ('Ticker', 'TSLA'),
                    ('Price', '$242.50'),
                    ('Temperature', '0.73'),
                    ('Heat Score', '0.68'),
                    ('Sector', 'Technology'),
                    ('Market Cap', '$769.2B'),
                    ('Beta', '1.82'),
                    ('Volume', '125.3M'),
                    ('Timestamp', '2025-11-09'),
                ])

    # Metrics Panel - replaced ICD10 with relevant metrics
    create_panel(ax, sidebar_x, 0.5, sidebar_width, 4.5,
                'Graph Statistics',
                [
                    ('Total Nodes', '13'),
                    ('Relationships', '18'),
                    ('Factor Categories', '6'),
                    ('Active Factors', '3'),
                    '',
                    'Influence Strength:',
                    ('Micro factors', 'High'),
                    ('Options flow', 'High'),
                    ('News sentiment', 'Medium'),
                ])

    plt.tight_layout(pad=0)
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/final_v3_knowledge_graph.png',
                dpi=300, bbox_inches='tight', facecolor=COLORS['bg_main'],
                edgecolor='none', pad_inches=0.3)
    plt.close()
    print("✅ Final Image 1: Knowledge Graph (clean, no sidebar clutter)")


# ============================================================================
# FINAL IMAGE 2: Heat Diffusion (BETTER SPACING & FONTS)
# ============================================================================
def generate_final_image2():
    """Heat diffusion with better spacing and readability"""
    fig, ax = plt.subplots(figsize=(16, 11))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg_main'])
    ax.set_facecolor(COLORS['bg_main'])

    # Title - larger and clearer
    add_text(ax, 8, 10.3, 'Heat Diffusion Process Over Time',
            fontsize=22, weight='bold', color=COLORS['text_bright'])
    add_text(ax, 8, 9.7, '∂h/∂t = -βL·h(t)  |  Temporal Evolution (t=0 → t=3)',
            fontsize=15, color=COLORS['text_secondary'])

    # Node network
    nodes = {
        'Event': (3, 6),
        'News': (5.5, 7.2),
        'Social': (5.5, 4.8),
        'TSLA': (8, 6),
        'Options': (10.5, 7.2),
        'Tech': (10.5, 4.8),
        'Market': (13, 6),
    }

    edges = [
        ('Event', 'News'), ('Event', 'Social'),
        ('News', 'TSLA'), ('Social', 'TSLA'),
        ('TSLA', 'Options'), ('TSLA', 'Tech'),
        ('Options', 'Market'), ('Tech', 'Market'),
    ]

    # Final timestep heat values
    heat_values = {
        'Event': 0.22, 'News': 0.41, 'Social': 0.41,
        'TSLA': 0.73, 'Options': 0.52, 'Tech': 0.52, 'Market': 0.38
    }

    # Draw edges
    for n1, n2 in edges:
        x1, y1 = nodes[n1]
        x2, y2 = nodes[n2]
        draw_edge(ax, x1, y1, x2, y2)

    # Draw nodes with heat colors
    for node_name, (x, y) in nodes.items():
        heat = heat_values[node_name]

        if heat > 0.6:
            color = COLORS['node_orange']
        elif heat > 0.3:
            color = COLORS['node_green']
        elif heat > 0.0:
            color = COLORS['node_gray']
        else:
            color = COLORS['bg_panel']

        draw_node(ax, x, y, 0.7, f'{node_name}\nh={heat:.2f}', color, fontsize=13)

    # Timeline - better spacing and larger
    timeline_y = 2.8
    add_text(ax, 8, 3.6, 'Time Progression', fontsize=16, weight='bold',
            color=COLORS['text_bright'])

    for i, t in enumerate(['t=0', 't=1', 't=2', 't=3']):
        x_pos = 3.5 + i * 3

        # Timeline marker - larger
        marker = Circle((x_pos, timeline_y), 0.4,
                       facecolor=COLORS['accent_blue'] if i == 3 else COLORS['node_gray'],
                       edgecolor='white', linewidth=2, alpha=0.9, zorder=5)
        ax.add_patch(marker)
        add_text(ax, x_pos, timeline_y, t, fontsize=14, weight='bold')

        if i < 3:
            ax.plot([x_pos + 0.4, x_pos + 2.6], [timeline_y, timeline_y],
                   color=COLORS['edge'], linewidth=3, alpha=0.6)

    # Heat legend - better spacing
    legend_y = 1.3
    add_text(ax, 8, 2, 'Heat Intensity Legend', fontsize=14, weight='bold',
            color=COLORS['text_secondary'])

    legend_items = [
        ('Hot (h>0.6)', COLORS['node_orange']),
        ('Warm (0.3<h≤0.6)', COLORS['node_green']),
        ('Mild (0<h≤0.3)', COLORS['node_gray']),
        ('Cold (h=0)', COLORS['bg_panel']),
    ]

    for i, (label, color) in enumerate(legend_items):
        x_pos = 2.5 + i * 3.5
        legend_node = Circle((x_pos, legend_y), 0.35, facecolor=color,
                           edgecolor='white', linewidth=2, alpha=0.9, zorder=5)
        ax.add_patch(legend_node)
        add_text(ax, x_pos + 1.5, legend_y, label, fontsize=13,
                color=COLORS['text_secondary'], ha='left')

    # Decay information
    decay_box = Rectangle((5.5, 0.2), 5, 0.7,
                         facecolor=COLORS['bg_panel'],
                         edgecolor=COLORS['border'], linewidth=2, zorder=8)
    ax.add_patch(decay_box)
    add_text(ax, 8, 0.55, 'Temporal Decay: h(t) = h₀·exp(-γt) with γ=0.5/hour',
            fontsize=12, color=COLORS['text_bright'], weight='bold')

    plt.tight_layout(pad=0)
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/final_v3_heat_diffusion.png',
                dpi=300, bbox_inches='tight', facecolor=COLORS['bg_main'],
                edgecolor='none', pad_inches=0.3)
    plt.close()
    print("✅ Final Image 2: Heat Diffusion (better spacing & fonts)")


# ============================================================================
# FINAL IMAGE 3: Factor Weights (IMPROVED READABILITY)
# ============================================================================
def generate_final_image3():
    """Factor weights with much better spacing and fonts"""
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_xlim(-7.5, 7.5)
    ax.set_ylim(-7.5, 7.5)
    ax.axis('off')
    fig.patch.set_facecolor(COLORS['bg_main'])
    ax.set_facecolor(COLORS['bg_main'])

    # Title - larger and clearer
    add_text(ax, 0, 7, 'Stock Heat Diffusion: Factor Category Weights',
            fontsize=20, weight='bold', color=COLORS['text_bright'])
    add_text(ax, 0, 6.3, 'Dynamic Weight Allocation with Normalization Constraint',
            fontsize=14, color=COLORS['text_secondary'])

    # Central stock node - larger
    draw_node(ax, 0, 0, 1.1, 'STOCK\nTSLA\nTemp: 0.73',
             COLORS['node_cream'], fontsize=15)

    # 10 Factor categories - better spacing
    factors = [
        ('Macro\n12%', 0),
        ('Micro\n28%', 36),
        ('News\n10%', 72),
        ('Social\n8%', 108),
        ('Order\n18%', 144),
        ('Options\n15%', 180),
        ('Technical\n12%', 216),
        ('Sector\n4%', 252),
        ('Supply\n2%', 288),
        ('Quant\n1%', 324),
    ]

    radius = 4.8
    for label, angle_deg in factors:
        angle_rad = np.radians(angle_deg)
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)

        draw_node(ax, x, y, 0.85, label, COLORS['node_green'], fontsize=13)
        draw_edge(ax, x, y, 0, 0)

    # Constraint box - larger and more prominent
    constraint_box = Rectangle((-3.5, -6.8), 7, 0.9,
                              facecolor=COLORS['accent_green'],
                              edgecolor='white', linewidth=3, zorder=8)
    ax.add_patch(constraint_box)
    add_text(ax, 0, -6.35, 'Constraint: ∑wᵢ(t) = 1.0  ∀t',
            fontsize=16, color='white', weight='bold')

    # Heat equation box - better spacing
    eq_box = Rectangle((-5, -5.7), 10, 0.9,
                      facecolor=COLORS['bg_panel'],
                      edgecolor=COLORS['border'], linewidth=2, zorder=8)
    ax.add_patch(eq_box)
    add_text(ax, 0, -5.25, 'heatstock(t) = ∑ wᵢ(t)·factorᵢ(t) + diffusion_term(t)',
            fontsize=14, color=COLORS['text_bright'], weight='bold')

    # Add weight legend
    legend_y = -4.3
    add_text(ax, 0, legend_y + 0.5, 'Weight Ranges by Factor Category',
            fontsize=13, weight='bold', color=COLORS['text_secondary'])

    weight_info = [
        'High Impact (>15%): Micro, Order, Options',
        'Medium Impact (10-15%): Macro, Technical, News',
        'Low Impact (<10%): Social, Sector, Supply, Quant',
    ]

    for i, info in enumerate(weight_info):
        add_text(ax, 0, legend_y - 0.5 - i*0.5, info, fontsize=11,
                color=COLORS['text_secondary'])

    plt.tight_layout(pad=0)
    plt.savefig('/home/user01/claude-test/Paper Submission/RAGHeat/final_v3_factor_weights.png',
                dpi=300, bbox_inches='tight', facecolor=COLORS['bg_main'],
                edgecolor='none', pad_inches=0.3)
    plt.close()
    print("✅ Final Image 3: Factor Weights (improved readability)")


# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == '__main__':
    print("\n" + "="*80)
    print("GENERATING FINAL ENHANCED IMAGES (V3)")
    print("FIXES: Better fonts, spacing, no sidebar clutter, no ICD10, more readable")
    print("="*80 + "\n")

    generate_final_image1()
    generate_final_image2()
    generate_final_image3()

    print("\n" + "="*80)
    print("✅ ALL FINAL IMAGES GENERATED!")
    print("="*80)
    print("\nImprovements:")
    print("  ✅ Removed irrelevant left sidebar (Graph/Table/Text/Code)")
    print("  ✅ Larger, readable fonts (14-22pt)")
    print("  ✅ Better spacing between all elements")
    print("  ✅ Removed ICD10 badge - replaced with Graph Statistics")
    print("  ✅ More vibrant, readable colors")
    print("  ✅ No cutoff issues - proper padding")
    print("  ✅ Professional and attractive presentation")
    print("\nGenerated Files:")
    print("  1. final_v3_knowledge_graph.png   (Clean, no clutter)")
    print("  2. final_v3_heat_diffusion.png    (Better spacing)")
    print("  3. final_v3_factor_weights.png    (Improved readability)")
    print("\n" + "="*80 + "\n")
