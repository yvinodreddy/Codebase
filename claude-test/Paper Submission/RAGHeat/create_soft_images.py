#!/usr/bin/env python3
"""
Soft, Beautiful JPG Images - Like Photoshop
Smooth gradients, gentle shadows, silky appearance
"""

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Soft, smooth settings
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['lines.antialiased'] = True
plt.rcParams['patch.antialiased'] = True

# Soft pastel colors
SOFT = {
    'stock': '#FF9E80',  # Soft coral
    'factor': '#90CAF9', # Soft blue
    'entity': '#A5D6A7', # Soft green
    'regime': '#FFCC80', # Soft orange
    'edge': '#BDBDBD',   # Soft gray
}

def soft_node(ax, x, y, r, color, label, size=11, badge='', zorder=10):
    """Create soft gradient node"""
    # Soft shadows (multiple layers)
    for i in range(4):
        offset = 0.02 * (i+1)
        alpha = 0.06 / (i+1)
        Circle((x+offset, y-offset), r, fc='black', ec='none',
              alpha=alpha, zorder=zorder-5).set_transform(ax.add_patch(
                  Circle((x+offset, y-offset), r, fc='black', ec='none',
                        alpha=alpha, zorder=zorder-5)).get_transform())

    # Main circle with soft gradient
    grad_n = 200
    Y, X = np.ogrid[-r:r:grad_n*1j, -r:r:grad_n*1j]
    R = np.sqrt(X**2 + Y**2)
    R_norm = np.clip(R / r, 0, 1)
    mask = R_norm <= 1.0

    # Light center to edge
    cmap = LinearSegmentedColormap.from_list('soft', ['#FFFFFF', color, color], N=256)
    extent = [x-r, x+r, y-r, y+r]
    ax.imshow(R_norm, extent=extent, cmap=cmap, origin='lower',
             interpolation='bilinear', alpha=mask*0.9, zorder=zorder)

    # Soft highlight
    Circle((x-r*0.3, y+r*0.3), r*0.35, fc='white', ec='none',
          alpha=0.3, zorder=zorder+1).set_transform(ax.add_patch(
              Circle((x-r*0.3, y+r*0.3), r*0.35, fc='white', ec='none',
                    alpha=0.3, zorder=zorder+1)).get_transform())

    # Soft border
    ax.add_patch(Circle((x, y), r, fc='none', ec='white', linewidth=2, alpha=0.7, zorder=zorder+2))

    # Text with soft shadow
    txt = ax.text(x, y, label, ha='center', va='center',
                 fontsize=size, fontweight='600', color='white',
                 zorder=zorder+3, alpha=0.95)
    txt.set_path_effects([
        path_effects.Stroke(linewidth=4, foreground='black', alpha=0.2),
        path_effects.Normal()
    ])

    # Badge
    if badge:
        by = y - r - 0.35
        bw = len(badge) * 0.09 + 0.15
        bg = FancyBboxPatch((x-bw/2, by-0.1), bw, 0.2,
                           boxstyle="round,pad=0.03",
                           fc=color, ec='white', linewidth=1.5, alpha=0.85,
                           zorder=zorder+4)
        ax.add_patch(bg)
        btxt = ax.text(x, by, badge, ha='center', va='center',
                      fontsize=9, fontweight='600', color='white',
                      zorder=zorder+5, alpha=0.95)
        btxt.set_path_effects([
            path_effects.Stroke(linewidth=2, foreground='black', alpha=0.2),
            path_effects.Normal()
        ])

def soft_edge(ax, x1, y1, x2, y2, color='#BDBDBD', w=2.5, zorder=5):
    """Create soft curved edge"""
    # Bezier
    mx, my = (x1+x2)/2, (y1+y2)/2
    dx, dy = x2-x1, y2-y1
    px, py = -dy, dx
    length = np.sqrt(px**2 + py**2)
    if length > 0:
        px, py = px/length, py/length
    cx = mx + px * 0.25
    cy = my + py * 0.25

    path = Path([(x1,y1), (cx,cy), (x2,y2)],
               [Path.MOVETO, Path.CURVE3, Path.CURVE3])

    # Soft glows
    for width, alpha in [(w*3, 0.04), (w*2, 0.07), (w*1.5, 0.1)]:
        ax.add_patch(mpatches.PathPatch(path, fc='none', ec=color,
                                       linewidth=width, alpha=alpha, capstyle='round',
                                       zorder=zorder))

    # Main line
    ax.add_patch(mpatches.PathPatch(path, fc='none', ec=color,
                                   linewidth=w, alpha=0.6, capstyle='round',
                                   zorder=zorder+1))

# FIGURE 1
def make_baseline():
    print("Creating soft baseline weights...")
    factors = [
        ('Microeconomic', 0.28), ('Order Flow', 0.18), ('Options', 0.15),
        ('Technical', 0.12), ('News', 0.10), ('Social', 0.08),
        ('Sector', 0.04), ('Macro', 0.03), ('Supply', 0.02)
    ]

    fig, ax = plt.subplots(figsize=(14, 14))
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    # Factors
    n = len(factors)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False) - np.pi/2
    for (name, w), angle in zip(factors, angles):
        x = 5.0 * np.cos(angle)
        y = 5.0 * np.sin(angle)
        soft_node(ax, x, y, 0.5+w*0.6, SOFT['factor'], name, 11, f'w={w:.2f}')
        soft_edge(ax, x, y, 0, 0, SOFT['edge'], 2.5)

    # Center
    soft_node(ax, 0, 0, 1.0, SOFT['stock'], 'Stock\nPrice', 14)

    # Title
    ax.text(0, 6.3, 'Baseline Factor Weights',
           ha='center', fontsize=22, fontweight='300', color='#424242')
    ax.text(0, 5.9, 'Stock Heat Diffusion Model',
           ha='center', fontsize=12, color='#757575')

    plt.savefig('SOFT_baseline_weights.jpg', dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("   ✅ SOFT_baseline_weights.jpg")

# FIGURE 2
def make_regime():
    print("Creating soft regime graph...")
    regimes = {
        'Low\nVolatility': {'f': [('Micro',0.35), ('Order',0.25), ('Options',0.20)], 'a': 0},
        'High\nVolatility': {'f': [('Options',0.40), ('Tech',0.30), ('Order',0.20)], 'a': 2*np.pi/3},
        'Trending': {'f': [('Tech',0.35), ('Micro',0.30), ('News',0.25)], 'a': 4*np.pi/3}
    }

    fig, ax = plt.subplots(figsize=(14, 12))
    ax.set_xlim(-7.5, 7.5)
    ax.set_ylim(-6.5, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    # Center
    soft_node(ax, 0, 0, 1.0, SOFT['stock'], 'Stock', 14)

    # Regimes
    for name, data in regimes.items():
        angle = data['a']
        rx = 4.2 * np.cos(angle - np.pi/2)
        ry = 4.2 * np.sin(angle - np.pi/2)
        soft_node(ax, rx, ry, 0.75, SOFT['regime'], name, 12)
        soft_edge(ax, rx, ry, 0, 0, SOFT['regime'], 3.0)

        # Factors
        n_f = len(data['f'])
        for i, (fname, w) in enumerate(data['f']):
            fangle = angle - 0.5 + i * 1.0 / (n_f-1) if n_f > 1 else angle
            fx = 6.2 * np.cos(fangle - np.pi/2)
            fy = 6.2 * np.sin(fangle - np.pi/2)
            soft_node(ax, fx, fy, 0.45+w*0.35, SOFT['factor'], fname, 10, f'{w:.2f}')
            soft_edge(ax, fx, fy, rx, ry, SOFT['edge'], 2.2)

    # Title
    ax.text(0, 6.0, 'Regime-Dependent Weights',
           ha='center', fontsize=22, fontweight='300', color='#424242')
    ax.text(0, 5.6, 'Dynamic Factor Allocation',
           ha='center', fontsize=12, color='#757575')

    plt.savefig('SOFT_regime_graph.jpg', dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("   ✅ SOFT_regime_graph.jpg")

# FIGURE 3
def make_heat():
    print("Creating soft heat propagation...")
    layers = {
        't=0': ([('Stock',1.00)], -8),
        't=1': ([('Order',0.85), ('Options',0.75), ('Micro',0.70)], -3),
        't=2': ([('Tech',0.60), ('News',0.55), ('Social',0.50)], 3),
        't=3': ([('Sector',0.35), ('Macro',0.30)], 8)
    }

    heat_cmap = LinearSegmentedColormap.from_list('heat',
        ['#FFF9E6', '#FFE8CC', '#FFD9B3', '#FFBD80', '#FFA34D'], N=256)

    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_xlim(-9.5, 9.5)
    ax.set_ylim(-5.5, 5.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    pos = {}
    for lname, (nodes, lx) in layers.items():
        n = len(nodes)
        y_start = -(n-1) * 1.9 / 2

        ax.text(lx, 4.8, lname, ha='center', fontsize=14,
               color='#424242', bbox=dict(boxstyle='round,pad=0.5',
               fc='white', alpha=0.8, ec='#E0E0E0', linewidth=1.5))

        for i, (name, heat) in enumerate(nodes):
            y = y_start + i * 1.9
            soft_node(ax, lx, y, 0.5+heat*0.55, heat_cmap(heat), name, 11, f'h={heat:.2f}')
            pos[name] = (lx, y)

    # Edges
    for i, lname in enumerate(['t=0', 't=1', 't=2']):
        src = layers[lname][0]
        tgt = layers[['t=1', 't=2', 't=3'][i]][0]
        for sn, _ in src:
            for tn, h in tgt:
                soft_edge(ax, *pos[sn], *pos[tn], SOFT['regime'], 1.8+h*2.0)

    # Title
    ax.text(0, 5.0, 'Heat Propagation Network',
           ha='center', fontsize=22, fontweight='300', color='#424242')
    ax.text(0, 4.6, 'Temporal Diffusion',
           ha='center', fontsize=12, color='#757575')

    plt.savefig('SOFT_heat_propagation.jpg', dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("   ✅ SOFT_heat_propagation.jpg")

# FIGURE 4
def make_complete():
    print("Creating soft complete graph...")

    fig, ax = plt.subplots(figsize=(16, 14))
    ax.set_xlim(-8.5, 8.5)
    ax.set_ylim(-7.5, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('#FAFAFA')

    # Center
    soft_node(ax, 0, 0, 1.1, SOFT['stock'], 'STOCK', 16)

    # Inner
    factors = ['Microeconomic', 'Order Flow', 'Options', 'Technical', 'News', 'Social']
    for i, name in enumerate(factors):
        angle = i * 2*np.pi/len(factors) - np.pi/2
        x, y = 4.0*np.cos(angle), 4.0*np.sin(angle)
        soft_node(ax, x, y, 0.7, SOFT['factor'], name, 10)
        soft_edge(ax, x, y, 0, 0, SOFT['edge'], 2.5)

    # Outer
    entities = ['Markets', 'Earnings', 'Fed', 'Sector', 'Supply', 'Options', 'Social', 'News']
    for i, name in enumerate(entities):
        angle = i * 2*np.pi/len(entities) - np.pi/2
        x, y = 7.2*np.cos(angle), 7.2*np.sin(angle)
        soft_node(ax, x, y, 0.55, SOFT['entity'], name, 9)

    # Title
    ax.text(0, 7.2, 'Complete Knowledge Graph',
           ha='center', fontsize=22, fontweight='300', color='#424242')
    ax.text(0, 6.8, 'Multi-Layer Network',
           ha='center', fontsize=12, color='#757575')

    # Legend
    for i, (color, label) in enumerate([(SOFT['stock'], 'Stock'),
                                        (SOFT['factor'], 'Factors'),
                                        (SOFT['entity'], 'Entities')]):
        lx = -4 + i*4
        ax.add_patch(Circle((lx-0.5, -6.8), 0.25, fc=color, ec='white', linewidth=2, alpha=0.85))
        ax.text(lx+0.2, -6.8, label, ha='left', va='center', fontsize=11, color='#424242')

    plt.savefig('SOFT_complete_graph.jpg', dpi=300, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    print("   ✅ SOFT_complete_graph.jpg")

# RUN
print("\n" + "="*80)
print("🎨 GENERATING SOFT PHOTOSHOP-QUALITY JPG IMAGES")
print("="*80)
make_baseline()
make_regime()
make_heat()
make_complete()
print("\n✅ ALL SOFT JPG IMAGES READY!")
print("="*80 + "\n")
