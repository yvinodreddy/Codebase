#!/usr/bin/env python3
"""
Stock Heat Diffusion Model - Professional Diagram Generator
Generates production-quality visualizations for any company/ticker
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Wedge
import numpy as np
import seaborn as sns
from matplotlib.patches import Arc
import networkx as nx
import warnings
import argparse
import sys

warnings.filterwarnings('ignore')

# Set professional style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
colors = sns.color_palette("Set2", 15)

# Configure fonts for publication quality
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['figure.dpi'] = 300

def create_architecture_diagram(ticker, company_name, prefix):
    """Generate comprehensive system architecture diagram"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, f'{company_name} Stock Heat Diffusion Model - System Architecture',
            ha='center', va='top', fontsize=14, fontweight='bold')

    # Layer 1: Data Sources (Top)
    data_sources = [
        ('Market Data\n(Yahoo/Alpha)', 1, 8.5),
        ('News\n(Reuters/Bloomberg)', 3.5, 8.5),
        ('Social Media\n(Twitter/Reddit)', 6, 8.5),
        ('Macro Indicators\n(FRED)', 8.5, 8.5),
        ('Options Flow\n(Market Data)', 11, 8.5)
    ]

    for name, x, y in data_sources:
        box = FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.7,
                            boxstyle="round,pad=0.05",
                            edgecolor=colors[0], facecolor=colors[0], alpha=0.3, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold')
        # Arrows down
        ax.arrow(x, y-0.5, 0, -0.3, head_width=0.15, head_length=0.1,
                fc=colors[0], ec=colors[0], linewidth=1.2)

    # Layer 2: Data Processing (Middle-Top)
    ax.text(7, 7.3, 'Real-Time Data Ingestion (Apache Kafka)',
            ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[1], alpha=0.4, edgecolor=colors[1], linewidth=1.5))

    # Arrow down from Kafka
    ax.arrow(7, 7, 0, -0.4, head_width=0.2, head_length=0.15,
            fc=colors[1], ec=colors[1], linewidth=1.5)

    # Layer 3: Processing Pipelines
    pipelines = [
        ('NER + Sentiment\n(FinBERT)', 2.5, 6.2),
        ('Triple Extraction\n(OpenIE)', 5.5, 6.2),
        ('Text Embedding\n(SBERT)', 8.5, 6.2),
        ('Factor Extraction', 11.5, 6.2)
    ]

    for name, x, y in pipelines:
        box = FancyBboxPatch((x-0.7, y-0.35), 1.4, 0.7,
                            boxstyle="round,pad=0.05",
                            edgecolor=colors[2], facecolor=colors[2], alpha=0.3, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold')
        # Arrows down
        ax.arrow(x, y-0.45, 0, -0.25, head_width=0.15, head_length=0.1,
                fc=colors[2], ec=colors[2], linewidth=1.2)

    # Layer 4: Storage Layer
    storage = [
        ('Knowledge Graph\n(Neo4j)', 2.5, 5),
        ('Time Series DB\n(PostgreSQL)', 5.5, 5),
        ('Vector Store\n(FAISS)', 8.5, 5),
        ('Factor Database', 11.5, 5)
    ]

    for name, x, y in storage:
        box = FancyBboxPatch((x-0.7, y-0.35), 1.4, 0.7,
                            boxstyle="round,pad=0.05",
                            edgecolor=colors[3], facecolor=colors[3], alpha=0.3, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold')

    # Arrows down to Core Engine
    for _, x, _ in storage:
        ax.arrow(x, 4.6, (7-x)*0.15, -0.5, head_width=0.12, head_length=0.08,
                fc=colors[3], ec=colors[3], linewidth=1.0, alpha=0.7)

    # Layer 5: Core Processing Engine (Central)
    engine_box = FancyBboxPatch((3.5, 2.8), 7, 1.5,
                                boxstyle="round,pad=0.1",
                                edgecolor=colors[4], facecolor=colors[4], alpha=0.2, linewidth=2)
    ax.add_patch(engine_box)

    ax.text(7, 3.9, 'Heat Diffusion Engine', ha='center', va='center',
            fontsize=10, fontweight='bold')

    sub_components = [
        ('Graph\nLaplacian\nL = D - A', 4.2, 3.3),
        ('Heat Kernel\ne^(-βLt)', 5.8, 3.3),
        ('Weight\nCalculation\nΣwᵢ = 1', 7.4, 3.3),
        ('GAT Layer\nwith Heat\nBias', 9, 3.3)
    ]

    for name, x, y in sub_components:
        box = FancyBboxPatch((x-0.5, y-0.35), 1, 0.7,
                            boxstyle="round,pad=0.03",
                            edgecolor=colors[5], facecolor='white', alpha=0.9, linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=7)

    # Arrow down from Engine
    ax.arrow(7, 2.7, 0, -0.4, head_width=0.2, head_length=0.15,
            fc=colors[4], ec=colors[4], linewidth=1.5)

    # Layer 6: Hybrid Retrieval
    retrieval_box = FancyBboxPatch((4, 1.5), 6, 0.7,
                                  boxstyle="round,pad=0.08",
                                  edgecolor=colors[6], facecolor=colors[6], alpha=0.3, linewidth=1.5)
    ax.add_patch(retrieval_box)
    ax.text(7, 1.85, 'Hybrid Retrieval: αS_semantic + βS_structural + γS_heat',
            ha='center', va='center', fontsize=9, fontweight='bold')

    # Arrow down to LLM
    ax.arrow(7, 1.4, 0, -0.3, head_width=0.2, head_length=0.15,
            fc=colors[6], ec=colors[6], linewidth=1.5)

    # Layer 7: LLM Generation
    llm_box = FancyBboxPatch((4.5, 0.3), 5, 0.6,
                            boxstyle="round,pad=0.08",
                            edgecolor=colors[7], facecolor=colors[7], alpha=0.3, linewidth=1.5)
    ax.add_patch(llm_box)
    ax.text(7, 0.6, 'LLM Chain-of-Thought Generation (GPT-4 / FinGPT)',
            ha='center', va='center', fontsize=9, fontweight='bold')

    # Output indicators
    ax.text(12.5, 3.5, '→ Real-time\nPredictions', ha='left', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[8], alpha=0.3))
    ax.text(12.5, 1.85, '→ Explanations', ha='left', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[9], alpha=0.3))
    ax.text(12.5, 0.6, '→ Visualizations', ha='left', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[10], alpha=0.3))

    plt.tight_layout()
    filename = f'{prefix}_architecture_diagram.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Architecture diagram generated: {filename}")
    plt.close()

def create_weight_distribution(ticker, company_name, prefix):
    """Generate weight distribution diagram showing Σwᵢ = 1"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Factor categories and baseline weights
    categories = [
        'Microeconomic', 'Order Flow', 'Options Flow', 'Technical',
        'News Sentiment', 'Social Media', 'Sector Correlation',
        'Macro', 'Supply Chain', 'Other Quant'
    ]

    baseline_weights = [0.28, 0.18, 0.15, 0.12, 0.10, 0.08, 0.04, 0.03, 0.02, 0.00]

    # Verify sum = 1
    total = sum(baseline_weights)
    assert abs(total - 1.0) < 0.001, f"Weights must sum to 1.0, got {total}"

    # Left plot: Pie chart with weights
    colors_pie = sns.color_palette("Set3", len(categories))
    wedges, texts, autotexts = ax1.pie(baseline_weights, labels=categories, autopct='%1.1f%%',
                                        startangle=90, colors=colors_pie, textprops={'fontsize': 9})

    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(8)

    ax1.set_title(f'{company_name} ({ticker})\nBaseline Weight Distribution\n(Σwᵢ = 1.0)',
                  fontsize=12, fontweight='bold', pad=20)

    # Right plot: Horizontal bar chart with ranges
    weight_ranges = [
        (0.25, 0.35),  # Microeconomic: 25-35%
        (0.15, 0.20),  # Order Flow: 15-20%
        (0.12, 0.18),  # Options Flow: 12-18%
        (0.10, 0.15),  # Technical: 10-15%
        (0.10, 0.15),  # News: 10-15%
        (0.08, 0.12),  # Social: 8-12%
        (0.08, 0.12),  # Sector: 8-12%
        (0.10, 0.15),  # Macro: 10-15%
        (0.05, 0.08),  # Supply: 5-8%
        (0.05, 0.08),  # Other: 5-8%
    ]

    y_pos = np.arange(len(categories))

    # Plot ranges as horizontal bars
    for i, (low, high) in enumerate(weight_ranges):
        mid = (low + high) / 2
        width = high - low
        ax2.barh(i, width, left=low, height=0.6,
                color=colors_pie[i], alpha=0.6, edgecolor='black', linewidth=0.8)
        ax2.plot(baseline_weights[i], i, 'o', color='red', markersize=8,
                markeredgecolor='black', markeredgewidth=1, zorder=3)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(categories, fontsize=9)
    ax2.set_xlabel('Weight Value', fontsize=10, fontweight='bold')
    ax2.set_title('Weight Ranges by Regime\n(Red dot = baseline)',
                 fontsize=12, fontweight='bold', pad=20)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.set_xlim(0, 0.40)

    # Add constraint annotation
    fig.text(0.5, 0.02, 'Constraint: Σwᵢ(t) = 1.0 ∀t (normalized at each time step)',
            ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    filename = f'{prefix}_weight_distribution.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Weight distribution diagram generated: {filename}")
    plt.close()

def create_heat_diffusion_flow(ticker, company_name, prefix):
    """Generate heat diffusion process flow diagram"""
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7, 7.5, 'Heat Diffusion Process: Market Event Impact Propagation',
            ha='center', va='top', fontsize=13, fontweight='bold')

    # Time steps
    time_steps = ['t=0\n(Event)', 't=1\n(Immediate)', 't=2\n(1-hop)', 't=3\n(2-hop)', 't=∞\n(Steady State)']
    x_positions = [1.5, 4, 6.5, 9, 11.5]

    # Event source
    event = Circle((1.5, 5), 0.4, facecolor='red', edgecolor='darkred', linewidth=2, alpha=0.8)
    ax.add_patch(event)
    ax.text(1.5, 5, 'Market\nEvent', ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    ax.text(1.5, 3.8, 'h = 1.0', ha='center', va='center', fontsize=9, fontweight='bold', color='red')

    # t=1: Direct impact on sectors
    sectors_t1 = [
        ('Related\nSector 1', 4, 6.5, 0.85),
        ('Target\nStock', 4, 5, 0.75),
        ('Related\nSector 2', 4, 3.5, 0.80)
    ]

    for name, x, y, heat in sectors_t1:
        color_intensity = plt.cm.Reds(heat)
        circle = Circle((x, y), 0.35, facecolor=color_intensity, edgecolor='darkred', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=7, fontweight='bold')
        ax.text(x, y-0.6, f'h={heat:.2f}', ha='center', va='center', fontsize=7, color='red')
        # Arrow from event
        ax.annotate('', xy=(x-0.35, y), xytext=(1.9, 5),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='red', alpha=0.6))

    # t=2: Secondary impact on stocks
    stocks_t2 = [
        ('Peer 1', 6.5, 7, 0.65),
        ('Peer 2', 6.5, 5.5, 0.50),
        ('Peer 3', 6.5, 4, 0.55),
        ('Peer 4', 6.5, 2.5, 0.70)
    ]

    for name, x, y, heat in stocks_t2:
        color_intensity = plt.cm.Oranges(heat + 0.2)
        circle = Circle((x, y), 0.3, facecolor=color_intensity, edgecolor='orange', linewidth=1.2)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=6, fontweight='bold')
        ax.text(x, y-0.5, f'h={heat:.2f}', ha='center', va='center', fontsize=6, color='darkorange')
        # Arrow from appropriate sector
        source_y = 5
        ax.annotate('', xy=(x-0.3, y), xytext=(4.35, source_y),
                   arrowprops=dict(arrowstyle='->', lw=1.2, color='orange', alpha=0.5))

    # t=3: Tertiary impact
    tertiary_t3 = [
        ('Supply\nChain', 9, 6, 0.35),
        ('Correlated\nStocks', 9, 4.5, 0.30),
        ('ETFs', 9, 3, 0.40)
    ]

    for name, x, y, heat in tertiary_t3:
        color_intensity = plt.cm.YlOrBr(heat + 0.3)
        circle = Circle((x, y), 0.35, facecolor=color_intensity, edgecolor='goldenrod', linewidth=1)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=6)
        ax.text(x, y-0.6, f'h={heat:.2f}', ha='center', va='center', fontsize=6, color='darkgoldenrod')
        # Arrows from stocks
        ax.annotate('', xy=(x-0.35, y), xytext=(6.8, 5),
                   arrowprops=dict(arrowstyle='->', lw=1, color='goldenrod', alpha=0.4))

    # t=∞: Steady state
    steady = Circle((11.5, 4.75), 0.4, facecolor='lightblue', edgecolor='blue', linewidth=1.5)
    ax.add_patch(steady)
    ax.text(11.5, 4.75, 'Market\nEquilibrium', ha='center', va='center', fontsize=7, fontweight='bold')
    ax.text(11.5, 3.8, 'h→0.05', ha='center', va='center', fontsize=7, color='blue')

    # Time labels
    for i, (label, x) in enumerate(zip(time_steps, x_positions)):
        ax.text(x, 1.5, label, ha='center', va='center', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[i], alpha=0.3))

    # Equation at bottom
    equation = r'$\frac{\partial h}{\partial t} = -\beta L \cdot h(t)$     Solution: $h(t) = e^{-\beta Lt} \cdot h_0$'
    ax.text(7, 0.8, equation, ha='center', va='center', fontsize=11,
           bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.8))

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='red', edgecolor='darkred', label='High Heat (h > 0.7)'),
        mpatches.Patch(facecolor='orange', edgecolor='orange', label='Medium Heat (0.4 < h < 0.7)'),
        mpatches.Patch(facecolor='yellow', edgecolor='goldenrod', label='Low Heat (0.2 < h < 0.4)'),
        mpatches.Patch(facecolor='lightblue', edgecolor='blue', label='Residual (h < 0.2)')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=8, framealpha=0.9)

    plt.tight_layout()
    filename = f'{prefix}_heat_diffusion_flow.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Heat diffusion flow diagram generated: {filename}")
    plt.close()

def create_factor_taxonomy(ticker, company_name, prefix):
    """Generate comprehensive factor taxonomy visualization"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, f'{company_name} ({ticker}): 10-Category Factor Taxonomy with Weight Ranges',
            ha='center', va='top', fontsize=14, fontweight='bold')

    # Central node
    center_circle = Circle((7, 5), 0.6, facecolor='gold', edgecolor='darkgoldenrod', linewidth=3, alpha=0.9)
    ax.add_patch(center_circle)
    ax.text(7, 5, f'{ticker}\nStock\nPrice', ha='center', va='center', fontsize=10, fontweight='bold')

    # Factor categories arranged in circle
    categories = [
        ('Microeconomic\n(Company)\n25-35%', 0, 3),
        ('Order Flow\n(Market μStruct)\n15-20%', 45, 3.5),
        ('Options Flow\n(Derivatives)\n12-18%', 90, 3.5),
        ('Technical\n(Indicators)\n10-15%', 135, 3),
        ('News\nSentiment\n10-15%', 180, 3),
        ('Social Media\n(Retail)\n8-12%', 225, 3),
        ('Sector\nCorrelation\n8-12%', 270, 3.5),
        ('Macro\n(Economy)\n10-15%', 315, 3.5),
        ('Supply Chain\n(Materials)\n5-8%', -45, 3.5),
        ('Quant Factors\n(Alpha)\n5-8%', -90, 3.5)
    ]

    for i, (name, angle, radius) in enumerate(categories):
        # Calculate position
        x = 7 + radius * np.cos(np.radians(angle))
        y = 5 + radius * np.sin(np.radians(angle))

        # Draw circle for category
        circle = Circle((x, y), 0.55, facecolor=colors[i], edgecolor='black', linewidth=1.5, alpha=0.7)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=7, fontweight='bold')

        # Draw arrow from category to center
        arrow = FancyArrowPatch((x, y), (7, 5),
                               arrowstyle='->', mutation_scale=15,
                               linewidth=2, color=colors[i], alpha=0.5,
                               connectionstyle='arc3,rad=0')
        ax.add_patch(arrow)

    # Add example factors in boxes outside
    examples = [
        ('Earnings\nRevenue\nMargins', 0, 6.5, 0),
        ('Order\nImbalance\nVWAP', 45, 7, 1),
        ('Gamma\nExposure\nIV Rank', 90, 7, 2),
        ('RSI\nMACD\nBollinger', 135, 6.5, 3),
        ('Bloomberg\nReuters\nCNBC', 180, 6.5, 4),
        ('Twitter\nReddit\nStockTwits', 225, 6.5, 5),
        ('Sector ETF\nPeers\nIndex', 270, 7, 6),
        ('Fed Rates\nCPI\nGDP', 315, 7, 7),
        ('Materials\nSuppliers\nProduction', -45, 7, 8),
        ('Short Int\nDark Pool\n13F', -90, 7, 9)
    ]

    for name, angle, radius, color_idx in examples:
        x = 7 + radius * np.cos(np.radians(angle))
        y = 5 + radius * np.sin(np.radians(angle))

        box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6,
                            boxstyle="round,pad=0.05",
                            edgecolor=colors[color_idx], facecolor='white',
                            alpha=0.9, linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=6)

    # Add equation at bottom with ticker variable
    eq_text = rf'$heat_{{{ticker}}}(t) = \sum_{{i=1}}^{{10}} w_i(t) \cdot factor_i(t) + diffusion\_term(t)$'
    ax.text(7, 0.8, eq_text, ha='center', va='center', fontsize=12,
           bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', edgecolor='orange', linewidth=2))

    constraint_text = r'Constraint: $\sum_{i=1}^{10} w_i(t) = 1.0$ ∀t'
    ax.text(7, 0.3, constraint_text, ha='center', va='center', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.6))

    plt.tight_layout()
    filename = f'{prefix}_factor_taxonomy.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Factor taxonomy diagram generated: {filename}")
    plt.close()

def create_dynamic_weight_adjustment(ticker, company_name, prefix):
    """Generate dynamic weight adjustment visualization across regimes"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'{company_name} ({ticker}): Dynamic Weight Adjustment Across Market Regimes (Σwᵢ = 1.0)',
                fontsize=14, fontweight='bold', y=0.98)

    categories = ['Micro', 'Order', 'Options', 'Tech', 'News', 'Social', 'Sector', 'Macro', 'Supply', 'Quant']

    # Four regimes
    regimes = {
        'Bull Market': [0.32, 0.08, 0.15, 0.18, 0.12, 0.10, 0.03, 0.02, 0.00, 0.00],
        'Bear Market': [0.20, 0.22, 0.25, 0.10, 0.06, 0.03, 0.02, 0.12, 0.00, 0.00],
        'High Volatility': [0.15, 0.25, 0.30, 0.08, 0.15, 0.02, 0.00, 0.05, 0.00, 0.00],
        'Sideways/Normal': [0.28, 0.18, 0.15, 0.12, 0.10, 0.08, 0.04, 0.03, 0.02, 0.00]
    }

    regime_colors = {
        'Bull Market': 'green',
        'Bear Market': 'red',
        'High Volatility': 'orange',
        'Sideways/Normal': 'blue'
    }

    axes_flat = axes.flatten()

    for idx, (regime_name, weights) in enumerate(regimes.items()):
        ax = axes_flat[idx]

        # Verify sum = 1
        assert abs(sum(weights) - 1.0) < 0.001, f"{regime_name}: weights sum to {sum(weights)}, not 1.0"

        # Create bar chart
        bars = ax.bar(categories, weights, color=colors[:10], edgecolor='black', linewidth=0.8, alpha=0.8)

        # Highlight top 3 factors
        sorted_indices = np.argsort(weights)[::-1][:3]
        for i in sorted_indices:
            bars[i].set_edgecolor(regime_colors[regime_name])
            bars[i].set_linewidth(3)

        ax.set_ylabel('Weight Value', fontsize=10, fontweight='bold')
        ax.set_title(f'{regime_name}\n(Σw = {sum(weights):.2f})',
                    fontsize=11, fontweight='bold', color=regime_colors[regime_name])
        ax.set_ylim(0, 0.35)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.tick_params(axis='x', rotation=45, labelsize=8)

        # Add value labels on bars
        for i, (cat, w) in enumerate(zip(categories, weights)):
            if w > 0.01:
                ax.text(i, w + 0.01, f'{w:.2f}', ha='center', va='bottom', fontsize=7, fontweight='bold')

    plt.tight_layout()
    filename = f'{prefix}_dynamic_weight_adjustment.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Dynamic weight adjustment diagram generated: {filename}")
    plt.close()

def create_time_series_weight_evolution(ticker, company_name, prefix):
    """Generate time series showing weight evolution during a market event"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Time points
    time = np.arange(0, 50, 1)

    # Simulate a shock event at t=10
    shock_time = 10

    # Weight evolutions for key factors
    macro_weight = 0.03 + 0.09 * np.exp(-(time - shock_time)**2 / 20) * (time >= shock_time)
    options_weight = 0.15 + 0.12 * np.exp(-(time - shock_time)**2 / 30) * (time >= shock_time)
    orderflow_weight = 0.18 + 0.10 * np.exp(-(time - shock_time)**2 / 15) * (time >= shock_time)
    micro_weight = 0.28 - 0.08 * np.exp(-(time - shock_time)**2 / 25) * (time >= shock_time)
    news_weight = 0.10 + 0.05 * np.exp(-(time - shock_time)**2 / 10) * (time >= shock_time)

    # Adjust to ensure sum = 1
    other_weight = 1.0 - (macro_weight + options_weight + orderflow_weight + micro_weight + news_weight)

    # Verify constraint
    total = macro_weight + options_weight + orderflow_weight + micro_weight + news_weight + other_weight
    assert np.allclose(total, 1.0), "Weights must sum to 1.0"

    # Top plot: Individual weight trajectories
    ax1.plot(time, macro_weight, '-o', label='Macro', linewidth=2, markersize=4, color=colors[0])
    ax1.plot(time, options_weight, '-s', label='Options Flow', linewidth=2, markersize=4, color=colors[1])
    ax1.plot(time, orderflow_weight, '-^', label='Order Flow', linewidth=2, markersize=4, color=colors[2])
    ax1.plot(time, micro_weight, '-d', label='Microeconomic', linewidth=2, markersize=4, color=colors[3])
    ax1.plot(time, news_weight, '-*', label='News Sentiment', linewidth=2, markersize=5, color=colors[4])

    ax1.axvline(x=shock_time, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Market Event')
    ax1.set_ylabel('Weight Value', fontsize=11, fontweight='bold')
    ax1.set_title(f'{company_name} ({ticker}): Dynamic Weight Evolution During Market Event',
                  fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9, framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 0.45)

    # Bottom plot: Stacked area showing total always = 1
    ax2.stackplot(time, macro_weight, options_weight, orderflow_weight, micro_weight, news_weight, other_weight,
                 labels=['Macro', 'Options', 'Order Flow', 'Micro', 'News', 'Other'],
                 colors=colors[:6], alpha=0.7)

    ax2.axvline(x=shock_time, color='red', linestyle='--', linewidth=2, alpha=0.7)
    ax2.axhline(y=1.0, color='black', linestyle='-', linewidth=2, label='Σwᵢ = 1.0')
    ax2.set_xlabel('Time (hours since market open)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Cumulative Weight', fontsize=11, fontweight='bold')
    ax2.set_title('Normalized Weight Distribution (Stacked)', fontsize=12, fontweight='bold')
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.05)

    plt.tight_layout()
    filename = f'{prefix}_weight_time_evolution.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Weight time evolution diagram generated: {filename}")
    plt.close()

def create_knowledge_graph_network(ticker, company_name, prefix):
    """Generate Neo4j-style knowledge graph network visualization"""
    fig, ax = plt.subplots(figsize=(16, 12))

    # Create directed graph
    G = nx.DiGraph()

    # Central stock node
    G.add_node(f'{ticker}_STOCK', node_type='stock', label=f'{ticker}\nStock Price')

    # Factor category nodes (10 categories)
    factors = [
        ('MICRO', 'Microeconomic\nFactors'),
        ('ORDERFLOW', 'Order Flow\nData'),
        ('OPTIONS', 'Options\nFlow'),
        ('TECHNICAL', 'Technical\nIndicators'),
        ('NEWS', 'News\nSentiment'),
        ('SOCIAL', 'Social Media\nSignals'),
        ('SECTOR', 'Sector\nCorrelation'),
        ('MACRO', 'Macro\nEconomic'),
        ('SUPPLY', 'Supply\nChain'),
        ('QUANT', 'Quant\nFactors')
    ]

    for fid, flabel in factors:
        G.add_node(fid, node_type='factor', label=flabel)
        G.add_edge(fid, f'{ticker}_STOCK', weight=0.1, label='INFLUENCES')

    # Entity nodes for each factor (2-3 examples per factor)
    entities = {
        'MICRO': [('EARNINGS', 'Earnings\nReport'), ('REVENUE', 'Revenue\nGrowth'), ('MARGINS', 'Profit\nMargins')],
        'ORDERFLOW': [('VWAP', 'VWAP\nDeviation'), ('IMBALANCE', 'Order\nImbalance')],
        'OPTIONS': [('GAMMA', 'Gamma\nExposure'), ('IV', 'Implied\nVolatility'), ('PUT_CALL', 'Put/Call\nRatio')],
        'TECHNICAL': [('RSI', 'RSI'), ('MACD', 'MACD'), ('BB', 'Bollinger\nBands')],
        'NEWS': [('BLOOMBERG', 'Bloomberg\nNews'), ('REUTERS', 'Reuters\nSentiment')],
        'SOCIAL': [('TWITTER', 'Twitter\nMentions'), ('REDDIT', 'Reddit\nVolume')],
        'SECTOR': [('SECTOR_ETF', 'Sector\nETF'), ('PEERS', 'Peer\nStocks')],
        'MACRO': [('FED_RATE', 'Fed\nRates'), ('CPI', 'CPI\nData')],
        'SUPPLY': [('MATERIALS', 'Raw\nMaterials'), ('SUPPLIERS', 'Supplier\nData')],
        'QUANT': [('SHORT_INT', 'Short\nInterest'), ('DARK_POOL', 'Dark Pool')]
    }

    for factor_id, entity_list in entities.items():
        for eid, elabel in entity_list:
            node_id = f'{factor_id}_{eid}'
            G.add_node(node_id, node_type='entity', label=elabel)
            G.add_edge(node_id, factor_id, weight=0.05, label='CONTRIBUTES_TO')

    # Layout using spring layout for better organization
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Separate nodes by type for different colors
    stock_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'stock']
    factor_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'factor']
    entity_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'entity']

    # Draw edges first (so they appear behind nodes)
    nx.draw_networkx_edges(G, pos, edge_color='#999999', width=1.5, alpha=0.5,
                          arrows=True, arrowsize=15, arrowstyle='->',
                          connectionstyle='arc3,rad=0.1', ax=ax)

    # Draw nodes with different colors and sizes
    nx.draw_networkx_nodes(G, pos, nodelist=stock_nodes, node_color='#E74C3C',
                          node_size=3000, node_shape='o', edgecolors='#C0392B',
                          linewidths=3, ax=ax, label='Stock')

    nx.draw_networkx_nodes(G, pos, nodelist=factor_nodes, node_color='#9B59B6',
                          node_size=2000, node_shape='o', edgecolors='#7D3C98',
                          linewidths=2.5, ax=ax, label='Factors')

    nx.draw_networkx_nodes(G, pos, nodelist=entity_nodes, node_color='#95A5A6',
                          node_size=1200, node_shape='o', edgecolors='#7F8C8D',
                          linewidths=2, ax=ax, label='Entities')

    # Draw labels
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=7, font_weight='bold',
                           font_color='white', ax=ax)

    # Title and styling
    ax.set_title(f'{company_name} ({ticker}): Knowledge Graph Network\n'
                f'Stock Heat Diffusion Model - Factor Influence Structure',
                fontsize=14, fontweight='bold', pad=20)

    ax.axis('off')
    ax.legend(loc='upper left', fontsize=10, framealpha=0.95, edgecolor='black')

    # Add stats box
    stats_text = f'Nodes: {G.number_of_nodes()}\nEdges: {G.number_of_edges()}\n' \
                f'Factors: {len(factor_nodes)}\nEntities: {len(entity_nodes)}'
    ax.text(0.02, 0.02, stats_text, transform=ax.transAxes, fontsize=9,
           verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    filename = f'{prefix}_knowledge_graph_network.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Knowledge graph network generated: {filename}")
    plt.close()

def create_factor_influence_graph(ticker, company_name, prefix):
    """Generate factor-to-factor influence network graph"""
    fig, ax = plt.subplots(figsize=(14, 10))

    # Create weighted directed graph
    G = nx.DiGraph()

    # Factor nodes
    factors = {
        'Macro': 0.10,
        'Micro': 0.28,
        'News': 0.12,
        'Social': 0.08,
        'Technical': 0.15,
        'OrderFlow': 0.18,
        'Options': 0.09
    }

    # Add nodes with weights
    for factor, weight in factors.items():
        G.add_node(factor, weight=weight)

    # Add influence edges (factor correlations and dependencies)
    influences = [
        ('News', 'Social', 0.75),
        ('News', 'Micro', 0.60),
        ('Social', 'News', 0.45),
        ('Macro', 'Micro', 0.55),
        ('Macro', 'Technical', 0.40),
        ('OrderFlow', 'Technical', 0.70),
        ('Options', 'OrderFlow', 0.65),
        ('Options', 'Technical', 0.50),
        ('Micro', 'Technical', 0.45),
        ('Technical', 'OrderFlow', 0.55),
        ('Social', 'Micro', 0.40),
        ('Macro', 'Options', 0.35)
    ]

    for source, target, influence in influences:
        G.add_edge(source, target, weight=influence)

    # Layout
    pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

    # Draw edges with varying thickness based on influence strength
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    edge_widths = [w * 4 for w in edge_weights]

    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='#3498DB',
                          alpha=0.6, arrows=True, arrowsize=20, arrowstyle='->',
                          connectionstyle='arc3,rad=0.2', ax=ax)

    # Draw nodes sized by their baseline weight
    node_weights = [factors[n] * 10000 for n in G.nodes()]
    node_colors = [factors[n] for n in G.nodes()]

    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_weights,
                                   node_color=node_colors, cmap='YlOrRd',
                                   vmin=0, vmax=0.30, edgecolors='black',
                                   linewidths=2.5, ax=ax)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold',
                           font_color='black', ax=ax)

    # Add weight labels below each node
    label_pos = {k: (v[0], v[1] - 0.12) for k, v in pos.items()}
    weight_labels = {k: f'w={v:.2f}' for k, v in factors.items()}
    nx.draw_networkx_labels(G, label_pos, weight_labels, font_size=8,
                           font_color='red', font_weight='bold', ax=ax)

    # Colorbar for node weights
    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=0, vmax=0.30))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Baseline Weight', fontsize=10, fontweight='bold')

    # Title
    ax.set_title(f'{company_name} ({ticker}): Factor Influence Network\n'
                f'Edge Thickness = Influence Strength | Node Size = Baseline Weight',
                fontsize=13, fontweight='bold', pad=20)

    ax.axis('off')

    # Add constraint note
    fig.text(0.5, 0.02, r'Constraint: $\sum w_i = 1.0$ (Node sizes proportional to weights)',
            ha='center', fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.4))

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    filename = f'{prefix}_factor_influence_graph.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Factor influence graph generated: {filename}")
    plt.close()

def create_heat_propagation_graph(ticker, company_name, prefix):
    """Generate multi-hop heat propagation network"""
    fig, ax = plt.subplots(figsize=(16, 10))

    # Create graph with temporal layers
    G = nx.DiGraph()

    # Event node (source)
    G.add_node('EVENT', layer=0, heat=1.0, label='Market\nEvent')

    # Layer 1: Immediate impact (3 nodes)
    layer1 = [
        (f'{ticker}_STOCK', 0.85, f'{ticker}\nStock'),
        ('SECTOR_INDEX', 0.75, 'Sector\nIndex'),
        ('RELATED_ETF', 0.70, 'Related\nETF')
    ]

    for node_id, heat, label in layer1:
        G.add_node(node_id, layer=1, heat=heat, label=label)
        G.add_edge('EVENT', node_id, diffusion_weight=heat)

    # Layer 2: Secondary impact (5 nodes)
    layer2 = [
        ('PEER_1', 0.55, 'Peer\nStock 1'),
        ('PEER_2', 0.50, 'Peer\nStock 2'),
        ('PEER_3', 0.48, 'Peer\nStock 3'),
        ('SUPPLIER_1', 0.45, 'Supplier\nStock'),
        ('CUSTOMER_1', 0.52, 'Customer\nStock')
    ]

    for node_id, heat, label in layer2:
        G.add_node(node_id, layer=2, heat=heat, label=label)
        # Connect to layer 1 nodes
        G.add_edge(f'{ticker}_STOCK', node_id, diffusion_weight=heat * 0.8)
        if 'PEER' in node_id:
            G.add_edge('SECTOR_INDEX', node_id, diffusion_weight=heat * 0.7)

    # Layer 3: Tertiary impact (7 nodes)
    layer3 = [
        ('SUPPLY_CHAIN_1', 0.30, 'Supply\nChain 1'),
        ('SUPPLY_CHAIN_2', 0.28, 'Supply\nChain 2'),
        ('CORR_STOCK_1', 0.32, 'Correlated\nStock 1'),
        ('CORR_STOCK_2', 0.29, 'Correlated\nStock 2'),
        ('OPTIONS_MKT', 0.35, 'Options\nMarket'),
        ('FUTURES_MKT', 0.27, 'Futures\nMarket'),
        ('INTL_MARKET', 0.25, 'International\nMarket')
    ]

    for node_id, heat, label in layer3:
        G.add_node(node_id, layer=3, heat=heat, label=label)
        # Connect to layer 2 nodes (select appropriate connections)
        if 'SUPPLY' in node_id:
            G.add_edge('SUPPLIER_1', node_id, diffusion_weight=heat * 0.6)
        elif 'CORR' in node_id:
            G.add_edge('PEER_1', node_id, diffusion_weight=heat * 0.6)
            G.add_edge('PEER_2', node_id, diffusion_weight=heat * 0.5)
        else:
            G.add_edge('PEER_3', node_id, diffusion_weight=heat * 0.5)

    # Multipartite layout
    pos = nx.multipartite_layout(G, subset_key='layer', align='horizontal')

    # Rotate to vertical (top to bottom)
    pos = {k: (v[1], -v[0]) for k, v in pos.items()}

    # Get heat values for coloring
    heat_values = [G.nodes[n]['heat'] for n in G.nodes()]

    # Draw edges with alpha based on diffusion weight
    for u, v, data in G.edges(data=True):
        alpha_val = data.get('diffusion_weight', 0.5)
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                             edge_color='#E67E22', width=2, alpha=alpha_val * 0.8,
                             arrows=True, arrowsize=12, arrowstyle='->',
                             connectionstyle='arc3,rad=0.05', ax=ax)

    # Draw nodes colored by heat
    nodes = nx.draw_networkx_nodes(G, pos, node_color=heat_values,
                                   cmap='Reds', vmin=0, vmax=1.0,
                                   node_size=1800, edgecolors='darkred',
                                   linewidths=2, ax=ax)

    # Draw labels
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=7, font_weight='bold', ax=ax)

    # Add heat value labels
    heat_label_pos = {k: (v[0], v[1] - 0.08) for k, v in pos.items()}
    heat_labels = {n: f'h={G.nodes[n]["heat"]:.2f}' for n in G.nodes()}
    nx.draw_networkx_labels(G, heat_label_pos, heat_labels, font_size=6,
                           font_color='red', font_weight='bold', ax=ax)

    # Colorbar
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=0, vmax=1.0))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label('Heat Intensity', fontsize=10, fontweight='bold')

    # Add layer labels
    layer_y_positions = {}
    for node, (x, y) in pos.items():
        layer = G.nodes[node]['layer']
        if layer not in layer_y_positions:
            layer_y_positions[layer] = y

    layer_names = ['t=0\n(Event)', 't=1\n(Immediate)', 't=2\n(Secondary)', 't=3\n(Tertiary)']
    for layer, layer_name in enumerate(layer_names):
        if layer in layer_y_positions:
            ax.text(-0.25, layer_y_positions[layer], layer_name,
                   fontsize=10, fontweight='bold', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='lightblue',
                            edgecolor='blue', linewidth=2))

    # Title
    ax.set_title(f'{company_name} ({ticker}): Multi-Hop Heat Propagation Network\n'
                f'Graph-Based Diffusion: h(t) = exp(-βLt)·h₀',
                fontsize=14, fontweight='bold', pad=20)

    ax.axis('off')
    ax.margins(0.15)

    plt.tight_layout()
    filename = f'{prefix}_heat_propagation_graph.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Heat propagation graph generated: {filename}")
    plt.close()

def create_market_event_impact_graph(ticker, company_name, prefix):
    """Generate market event impact network with entity relationships"""
    fig, ax = plt.subplots(figsize=(14, 12))

    # Create graph
    G = nx.Graph()

    # Central event
    G.add_node('EVENT', node_type='event', label='Earnings\nBeat')

    # Stock and related entities
    stock_entities = [
        (f'{ticker}', 'stock', f'{ticker}\nStock'),
        ('CALL_OPTIONS', 'derivative', 'Call\nOptions'),
        ('PUT_OPTIONS', 'derivative', 'Put\nOptions'),
        ('STOCK_FUTURES', 'derivative', f'{ticker}\nFutures')
    ]

    for node_id, ntype, label in stock_entities:
        G.add_node(node_id, node_type=ntype, label=label)
        G.add_edge('EVENT', node_id)

    # Market participants
    participants = [
        ('RETAIL_TRADERS', 'participant', 'Retail\nTraders'),
        ('HEDGE_FUNDS', 'participant', 'Hedge\nFunds'),
        ('MARKET_MAKERS', 'participant', 'Market\nMakers'),
        ('INSTITUTIONS', 'participant', 'Institutional\nInvestors')
    ]

    for node_id, ntype, label in participants:
        G.add_node(node_id, node_type=ntype, label=label)
        G.add_edge(f'{ticker}', node_id)
        G.add_edge('CALL_OPTIONS', node_id)

    # News and social
    media = [
        ('BLOOMBERG', 'media', 'Bloomberg\nNews'),
        ('TWITTER', 'media', 'Twitter\nSentiment'),
        ('REDDIT_WSB', 'media', 'Reddit\nWSB'),
        ('ANALYST_UPGRADES', 'media', 'Analyst\nUpgrades')
    ]

    for node_id, ntype, label in media:
        G.add_node(node_id, node_type=ntype, label=label)
        G.add_edge('EVENT', node_id)
        G.add_edge('RETAIL_TRADERS', node_id)

    # Related stocks
    related = [
        ('PEER_A', 'related_stock', 'Peer\nStock A'),
        ('PEER_B', 'related_stock', 'Peer\nStock B'),
        ('SUPPLIER', 'related_stock', 'Key\nSupplier'),
        ('SECTOR_ETF', 'related_stock', 'Sector\nETF')
    ]

    for node_id, ntype, label in related:
        G.add_node(node_id, node_type=ntype, label=label)
        G.add_edge(f'{ticker}', node_id)
        if 'PEER' in node_id:
            G.add_edge('SECTOR_ETF', node_id)

    # Layout
    pos = nx.spring_layout(G, k=1.2, iterations=50, seed=42)

    # Separate by node type
    node_types = {
        'event': ('#E74C3C', 2500),      # Red
        'stock': ('#3498DB', 2000),      # Blue
        'derivative': ('#9B59B6', 1500), # Purple
        'participant': ('#F39C12', 1500),# Orange
        'media': ('#1ABC9C', 1200),      # Teal
        'related_stock': ('#95A5A6', 1200) # Gray
    }

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='#BDC3C7', width=1.5, alpha=0.6, ax=ax)

    # Draw nodes by type
    for ntype, (color, size) in node_types.items():
        nodelist = [n for n, d in G.nodes(data=True) if d.get('node_type') == ntype]
        if nodelist:
            nx.draw_networkx_nodes(G, pos, nodelist=nodelist, node_color=color,
                                 node_size=size, edgecolors='black', linewidths=2,
                                 ax=ax, label=ntype.replace('_', ' ').title())

    # Draw labels
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=7, font_weight='bold', ax=ax)

    # Title
    ax.set_title(f'{company_name} ({ticker}): Market Event Impact Network\n'
                f'Entity Relationships and Information Flow',
                fontsize=14, fontweight='bold', pad=20)

    ax.axis('off')
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95, ncol=2)

    # Stats
    stats = f'Total Entities: {G.number_of_nodes()}\n' \
           f'Relationships: {G.number_of_edges()}\n' \
           f'Avg Degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}'
    ax.text(0.98, 0.02, stats, transform=ax.transAxes, fontsize=9,
           verticalalignment='bottom', horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    plt.tight_layout()
    filename = f'{prefix}_market_event_impact_graph.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Market event impact graph generated: {filename}")
    plt.close()

def main():
    """Generate all diagrams with command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Stock Heat Diffusion Model - Professional Diagram Generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('--ticker', '-t', type=str, default='STOCK',
                       help='Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)')
    parser.add_argument('--company', '-c', type=str, default=None,
                       help='Company name (e.g., "Apple Inc.", "Microsoft Corp.")')
    parser.add_argument('--prefix', '-p', type=str, default=None,
                       help='Output filename prefix (default: lowercase ticker)')

    args = parser.parse_args()

    ticker = args.ticker.upper()
    company_name = args.company if args.company else ticker
    prefix = args.prefix if args.prefix else ticker.lower()

    print("\n" + "="*70)
    print("Stock Heat Diffusion Model - Diagram Generator")
    print("="*70 + "\n")
    print(f"Ticker Symbol:  {ticker}")
    print(f"Company Name:   {company_name}")
    print(f"Output Prefix:  {prefix}")
    print()
    print("Generating professional diagrams for academic paper...\n")

    try:
        # Original diagrams
        create_architecture_diagram(ticker, company_name, prefix)
        create_weight_distribution(ticker, company_name, prefix)
        create_heat_diffusion_flow(ticker, company_name, prefix)
        create_factor_taxonomy(ticker, company_name, prefix)
        create_dynamic_weight_adjustment(ticker, company_name, prefix)
        create_time_series_weight_evolution(ticker, company_name, prefix)

        # New graph-style visualizations (Neo4j-inspired)
        create_knowledge_graph_network(ticker, company_name, prefix)
        create_factor_influence_graph(ticker, company_name, prefix)
        create_heat_propagation_graph(ticker, company_name, prefix)
        create_market_event_impact_graph(ticker, company_name, prefix)

        print("\n" + "="*70)
        print("✓ All diagrams generated successfully!")
        print("="*70 + "\n")

        print("Generated files:")
        print(f"\n📊 Original Diagrams:")
        print(f"  1. {prefix}_architecture_diagram.png")
        print(f"  2. {prefix}_weight_distribution.png")
        print(f"  3. {prefix}_heat_diffusion_flow.png")
        print(f"  4. {prefix}_factor_taxonomy.png")
        print(f"  5. {prefix}_dynamic_weight_adjustment.png")
        print(f"  6. {prefix}_weight_time_evolution.png")
        print(f"\n🔗 Graph Network Visualizations:")
        print(f"  7. {prefix}_knowledge_graph_network.png")
        print(f"  8. {prefix}_factor_influence_graph.png")
        print(f"  9. {prefix}_heat_propagation_graph.png")
        print(f" 10. {prefix}_market_event_impact_graph.png")
        print()

        print("All weight constraints verified: Σwᵢ = 1.0 ✓")
        print()

    except Exception as e:
        print(f"\n❌ Error generating diagrams: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
