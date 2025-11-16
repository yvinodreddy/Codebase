#!/usr/bin/env python3
"""
SIMPLE: Generate stunning, ultra-high-resolution PNG images
Like Photoshop-quality output - clean, beautiful, professional
"""

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import colorsys
from matplotlib.colors import to_rgb, to_hex

# Ultra-high resolution settings
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['lines.antialiased'] = True
plt.rcParams['patch.antialiased'] = True
plt.rcParams['text.antialiased'] = True

# Professional color palette
COLORS = {
    'stock': '#FF6B35',      # Vibrant orange
    'factor': '#004E89',     # Deep blue
    'entity': '#00A8CC',     # Bright cyan
    'regime': '#F95738',     # Coral red
    'edge': '#8B8B8B',       # Gray
}

def create_gradient_node(ax, x, y, radius, color, label, label_size=10, zorder=10,
                        show_badge=False, badge_text=''):
    """Create beautiful node with gradient and glow"""

    # Calculate gradient colors
    rgb = to_rgb(color)
    hsv = colorsys.rgb_to_hsv(*rgb)
    light_hsv = (hsv[0], hsv[1] * 0.4, min(hsv[2] * 1.4, 1.0))
    light_color = to_hex(colorsys.hsv_to_rgb(*light_hsv))

    # Multiple shadow layers for depth
    for offset, alpha in [(0.05, 0.15), (0.03, 0.10), (0.015, 0.05)]:
        shadow = Circle((x + offset, y - offset), radius,
                       facecolor='black', edgecolor='none',
                       alpha=alpha, zorder=zorder-3)
        ax.add_patch(shadow)

    # Gradient fill
    gradient_size = 200
    Y, X = np.ogrid[-radius:radius:gradient_size*1j, -radius:radius:gradient_size*1j]
    R = np.sqrt(X**2 + Y**2)
    R_norm = np.clip(R / radius, 0, 1)
    mask = R_norm <= 1.0

    cmap = LinearSegmentedColormap.from_list('grad', [light_color, color, color], N=256)
    extent = [x - radius, x + radius, y - radius, y + radius]
    ax.imshow(R_norm, extent=extent, cmap=cmap, origin='lower',
             interpolation='bilinear', alpha=mask.astype(float), zorder=zorder)

    # Glossy highlight
    highlight = Circle((x - radius*0.3, y + radius*0.3), radius*0.3,
                      facecolor='white', edgecolor='none',
                      alpha=0.5, zorder=zorder+1)
    ax.add_patch(highlight)

    # Border
    border = Circle((x, y), radius, facecolor='none', edgecolor='white',
                   linewidth=2.5, zorder=zorder+2)
    ax.add_patch(border)

    # Label with glow
    text = ax.text(x, y, label, ha='center', va='center',
                  fontsize=label_size, fontweight='bold',
                  color='white', zorder=zorder+3)
    text.set_path_effects([
        path_effects.Stroke(linewidth=3, foreground='black', alpha=0.7),
        path_effects.Normal()
    ])

    # Badge
    if show_badge and badge_text:
        badge_y = y - radius - 0.3
        badge = FancyBboxPatch((x - 0.25, badge_y - 0.08), 0.5, 0.16,
                              boxstyle="round,pad=0.02",
                              facecolor=color, edgecolor='white',
                              linewidth=1.5, zorder=zorder+4)
        ax.add_patch(badge)

        badge_label = ax.text(x, badge_y, badge_text,
                             ha='center', va='center',
                             fontsize=8, fontweight='bold',
                             color='white', zorder=zorder+5)
        badge_label.set_path_effects([
            path_effects.Stroke(linewidth=2, foreground='black', alpha=0.5),
            path_effects.Normal()
        ])

def create_glowing_edge(ax, x1, y1, x2, y2, color='#888888', width=2.5, zorder=5):
    """Create glowing curved edge with arrow"""

    # Bezier curve
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    perp_x, perp_y = -dy, dx
    length = np.sqrt(perp_x**2 + perp_y**2)
    if length > 0:
        perp_x, perp_y = perp_x / length, perp_y / length

    ctrl_x = mid_x + perp_x * 0.2
    ctrl_y = mid_y + perp_y * 0.2

    verts = [(x1, y1), (ctrl_x, ctrl_y), (x2, y2)]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
    path = Path(verts, codes)

    # Glow layers
    for w, a in [(width*2, 0.05), (width*1.5, 0.1), (width, 0.3)]:
        glow = mpatches.PathPatch(path, facecolor='none', edgecolor=color,
                                 linewidth=w, alpha=a, capstyle='round', zorder=zorder)
        ax.add_patch(glow)

    # Main edge
    edge = mpatches.PathPatch(path, facecolor='none', edgecolor=color,
                             linewidth=width, alpha=0.8, capstyle='round', zorder=zorder+1)
    ax.add_patch(edge)

    # Arrow
    t = 0.8
    arrow_x = (1-t)**2 * x1 + 2*(1-t)*t * ctrl_x + t**2 * x2
    arrow_y = (1-t)**2 * y1 + 2*(1-t)*t * ctrl_y + t**2 * y2
    t_prev = 0.75
    prev_x = (1-t_prev)**2 * x1 + 2*(1-t_prev)*t_prev * ctrl_x + t_prev**2 * x2
    prev_y = (1-t_prev)**2 * y1 + 2*(1-t_prev)*t_prev * ctrl_y + t_prev**2 * y2

    angle = np.arctan2(arrow_y - prev_y, arrow_x - prev_x)
    arrow_size = 0.15
    arrow = mpatches.FancyArrow(
        arrow_x - arrow_size * np.cos(angle),
        arrow_y - arrow_size * np.sin(angle),
        arrow_size * np.cos(angle),
        arrow_size * np.sin(angle),
        width=0.08, head_width=0.15, head_length=0.1,
        facecolor=color, edgecolor='white', linewidth=1.0,
        alpha=0.9, zorder=zorder+2
    )
    ax.add_patch(arrow)

# FIGURE 1: Baseline Weights
def create_baseline_weights():
    print("\n🎨 Creating: Baseline Weights Graph...")

    factors = [
        ('Micro', 0.28), ('Order\nFlow', 0.18), ('Options', 0.15),
        ('Technical', 0.12), ('News', 0.10), ('Social', 0.08),
        ('Sector', 0.04), ('Macro', 0.03), ('Supply', 0.02),
    ]

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Factors in circle
    n = len(factors)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False) - np.pi/2
    radius_circle = 4.5

    for (name, weight), angle in zip(factors, angles):
        x = radius_circle * np.cos(angle)
        y = radius_circle * np.sin(angle)
        node_r = 0.5 + weight * 0.5

        create_gradient_node(ax, x, y, node_r, COLORS['factor'], name, 10,
                           show_badge=True, badge_text=f'w={weight:.2f}')
        create_glowing_edge(ax, x, y, 0, 0, COLORS['edge'], 2.5)

    # Center stock
    create_gradient_node(ax, 0, 0, 0.9, COLORS['stock'], 'Stock\nPrice', 14)

    # Title
    title = ax.text(0, 5.5, 'Baseline Factor Weights',
                   ha='center', va='bottom', fontsize=18, fontweight='bold',
                   color='#333333')
    title.set_path_effects([
        path_effects.Stroke(linewidth=2, foreground='white', alpha=0.8),
        path_effects.Normal()
    ])

    ax.text(0, 5.1, 'Stock Heat Diffusion Model',
           ha='center', va='top', fontsize=11, color='#666666')

    plt.savefig('final_baseline_weights.png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    plt.close()
    print("   ✅ final_baseline_weights.png")

# FIGURE 2: Regime Graph
def create_regime_graph():
    print("\n🎨 Creating: Regime Graph...")

    regimes = {
        'Low Vol': {'factors': [('Micro', 0.35), ('Order', 0.25), ('Options', 0.20)], 'angle': 0},
        'High Vol': {'factors': [('Options', 0.40), ('Tech', 0.30), ('Order', 0.20)], 'angle': 2*np.pi/3},
        'Trending': {'factors': [('Tech', 0.35), ('Micro', 0.30), ('News', 0.25)], 'angle': 4*np.pi/3},
    }

    fig, ax = plt.subplots(figsize=(13, 11))
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Center stock
    create_gradient_node(ax, 0, 0, 0.9, COLORS['stock'], 'Stock', 14)

    # Regimes
    regime_r = 4.0
    factor_offset = 2.0

    for name, data in regimes.items():
        angle = data['angle']
        rx = regime_r * np.cos(angle - np.pi/2)
        ry = regime_r * np.sin(angle - np.pi/2)

        create_gradient_node(ax, rx, ry, 0.7, COLORS['regime'], name, 11)
        create_glowing_edge(ax, rx, ry, 0, 0, COLORS['stock'], 3.0)

        n_f = len(data['factors'])
        f_angles = np.linspace(angle - 0.5, angle + 0.5, n_f)

        for (fname, weight), fangle in zip(data['factors'], f_angles):
            fx = (regime_r + factor_offset) * np.cos(fangle - np.pi/2)
            fy = (regime_r + factor_offset) * np.sin(fangle - np.pi/2)
            node_r = 0.4 + weight * 0.3

            create_gradient_node(ax, fx, fy, node_r, COLORS['factor'], fname, 9,
                               show_badge=True, badge_text=f'{weight:.2f}')
            create_glowing_edge(ax, fx, fy, rx, ry, COLORS['edge'], 2.0)

    # Title
    title = ax.text(0, 6.5, 'Regime-Dependent Weights',
                   ha='center', va='bottom', fontsize=18, fontweight='bold',
                   color='#333333')
    title.set_path_effects([
        path_effects.Stroke(linewidth=2, foreground='white', alpha=0.8),
        path_effects.Normal()
    ])

    ax.text(0, 6.1, 'Dynamic Factor Allocation Across Market Regimes',
           ha='center', va='top', fontsize=11, color='#666666')

    plt.savefig('final_regime_graph.png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    plt.close()
    print("   ✅ final_regime_graph.png")

# FIGURE 3: Heat Propagation
def create_heat_propagation():
    print("\n🎨 Creating: Heat Propagation Network...")

    layers = {
        't=0': {'nodes': [('Stock', 1.00)], 'x': -7},
        't=1': {'nodes': [('Order', 0.85), ('Options', 0.75), ('Micro', 0.70)], 'x': -2.5},
        't=2': {'nodes': [('Tech', 0.60), ('News', 0.55), ('Social', 0.50)], 'x': 2.5},
        't=3': {'nodes': [('Sector', 0.35), ('Macro', 0.30)], 'x': 7},
    }

    heat_colors = ['#FFFFFF', '#FFF4E6', '#FFE0B2', '#FFCC80', '#FFB74D', '#FF9800', '#F57C00', '#E65100']
    heat_cmap = LinearSegmentedColormap.from_list('heat', heat_colors, N=256)

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(-8.5, 8.5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')

    positions = {}

    for layer_name, layer_data in layers.items():
        x = layer_data['x']
        nodes = layer_data['nodes']
        n = len(nodes)
        y_start = -(n - 1) * 1.8 / 2

        # Layer label
        ax.text(x, 4.5, layer_name, ha='center', va='bottom',
               fontsize=13, fontweight='bold', color='#333333',
               bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                        edgecolor='#999999', linewidth=2))

        for i, (name, heat) in enumerate(nodes):
            y = y_start + i * 1.8
            node_r = 0.4 + heat * 0.5
            color = heat_cmap(heat)

            create_gradient_node(ax, x, y, node_r, color, name, 10,
                               show_badge=True, badge_text=f'h={heat:.2f}')
            positions[name] = (x, y)

    # Edges (simplified - connect layers)
    layer_list = ['t=0', 't=1', 't=2', 't=3']
    for i in range(len(layer_list) - 1):
        source_nodes = layers[layer_list[i]]['nodes']
        target_nodes = layers[layer_list[i+1]]['nodes']

        for sname, _ in source_nodes:
            sx, sy = positions[sname]
            for tname, heat in target_nodes:
                tx, ty = positions[tname]
                width = 1.5 + heat * 2.0
                create_glowing_edge(ax, sx, sy, tx, ty, COLORS['stock'], width)

    # Title
    title = ax.text(0, 4.8, 'Heat Propagation Network',
                   ha='center', va='bottom', fontsize=18, fontweight='bold',
                   color='#333333')
    title.set_path_effects([
        path_effects.Stroke(linewidth=2, foreground='white', alpha=0.8),
        path_effects.Normal()
    ])

    ax.text(0, 4.4, 'Temporal Diffusion of Market Signals',
           ha='center', va='top', fontsize=11, color='#666666')

    plt.savefig('final_heat_propagation.png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    plt.close()
    print("   ✅ final_heat_propagation.png")

# FIGURE 4: Complete Knowledge Graph
def create_complete_graph():
    print("\n🎨 Creating: Complete Knowledge Graph...")

    fig, ax = plt.subplots(figsize=(14, 12))
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')

    # Center stock
    create_gradient_node(ax, 0, 0, 1.0, COLORS['stock'], 'STOCK', 14)

    # Inner: Factors
    factors = ['Micro', 'Order', 'Options', 'Tech', 'News', 'Social']
    n_f = len(factors)
    f_angles = np.linspace(0, 2*np.pi, n_f, endpoint=False) - np.pi/2
    f_radius = 3.8

    for name, angle in zip(factors, f_angles):
        x = f_radius * np.cos(angle)
        y = f_radius * np.sin(angle)
        create_gradient_node(ax, x, y, 0.6, COLORS['factor'], name, 10)
        create_glowing_edge(ax, x, y, 0, 0, COLORS['edge'], 2.5)

    # Outer: Entities
    entities = ['Markets', 'Earnings', 'Fed', 'Sector', 'Supply', 'Options', 'Social', 'News']
    n_e = len(entities)
    e_angles = np.linspace(0, 2*np.pi, n_e, endpoint=False) - np.pi/2
    e_radius = 6.8

    for name, angle in zip(entities, e_angles):
        x = e_radius * np.cos(angle)
        y = e_radius * np.sin(angle)
        create_gradient_node(ax, x, y, 0.5, COLORS['entity'], name, 8)

    # Title
    title = ax.text(0, 7.5, 'Complete Knowledge Graph',
                   ha='center', va='bottom', fontsize=18, fontweight='bold',
                   color='#333333')
    title.set_path_effects([
        path_effects.Stroke(linewidth=2, foreground='white', alpha=0.8),
        path_effects.Normal()
    ])

    ax.text(0, 7.1, 'Multi-Layer Factor and Entity Network',
           ha='center', va='top', fontsize=11, color='#666666')

    # Legend
    legend_items = [
        (COLORS['stock'], 'Stock'), (COLORS['factor'], 'Factors'), (COLORS['entity'], 'Entities')
    ]
    for i, (color, label) in enumerate(legend_items):
        lx = -3 + i * 3
        small = Circle((lx - 0.4, -7.2), 0.2, facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(small)
        ax.text(lx, -7.2, label, ha='left', va='center', fontsize=10, fontweight='bold')

    plt.savefig('final_complete_graph.png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    plt.close()
    print("   ✅ final_complete_graph.png")

# MAIN
print("\n" + "="*80)
print("🎨 GENERATING STUNNING VISUALIZATIONS")
print("="*80)
print("Format: Ultra-high-resolution PNG (300 DPI)")
print("Quality: Photoshop-level professional")
print("="*80)

create_baseline_weights()
create_regime_graph()
create_heat_propagation()
create_complete_graph()

print("\n" + "="*80)
print("✅ ALL IMAGES GENERATED SUCCESSFULLY")
print("="*80)
print("\n📄 Generated Files:")
print("   • final_baseline_weights.png")
print("   • final_regime_graph.png")
print("   • final_heat_propagation.png")
print("   • final_complete_graph.png")
print("\n✨ Beautiful, professional, ready to use!")
print("="*80 + "\n")
