#!/usr/bin/env python3
"""
Tesla Stock Heat Diffusion Model - Professional Diagram Generator
Generates production-quality visualizations for academic paper
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Wedge
import numpy as np
import seaborn as sns
from matplotlib.patches import Arc
import warnings
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

def create_architecture_diagram():
    """Generate comprehensive system architecture diagram"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Tesla Stock Heat Diffusion Model - System Architecture',
            ha='center', va='top', fontsize=14, fontweight='bold')

    # Layer 1: Data Sources (Top)
    data_sources = [
        ('Market Data\n(Yahoo/Alpha)', 1, 8.5),
        ('News\n(Reuters/Bloomberg)', 3.5, 8.5),
        ('Social Media\n(Twitter/Reddit)', 6, 8.5),
        ('Macro Indicators\n(FRED)', 8.5, 8.5),
        ('Options Flow\n(SpotGamma)', 11, 8.5)
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
    plt.savefig('tesla_architecture_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Architecture diagram generated: tesla_architecture_diagram.png")
    plt.close()

def create_weight_distribution():
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

    ax1.set_title('Baseline Weight Distribution\n(Σwᵢ = 1.0)', fontsize=12, fontweight='bold', pad=20)

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
    plt.savefig('weight_distribution_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Weight distribution diagram generated: weight_distribution_diagram.png")
    plt.close()

def create_heat_diffusion_flow():
    """Generate heat diffusion process flow diagram"""
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, aspect='equal')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title
    ax.text(7, 7.5, 'Heat Diffusion Process: Federal Reserve Rate Hike Impact',
            ha='center', va='top', fontsize=13, fontweight='bold')

    # Time steps
    time_steps = ['t=0\n(Event)', 't=1\n(Immediate)', 't=2\n(1-hop)', 't=3\n(2-hop)', 't=∞\n(Steady State)']
    x_positions = [1.5, 4, 6.5, 9, 11.5]

    # Event source
    event = Circle((1.5, 5), 0.4, facecolor='red', edgecolor='darkred', linewidth=2, alpha=0.8)
    ax.add_patch(event)
    ax.text(1.5, 5, 'FED\nRate↑', ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    ax.text(1.5, 3.8, 'h = 1.0', ha='center', va='center', fontsize=9, fontweight='bold', color='red')

    # t=1: Direct impact on sectors
    sectors_t1 = [
        ('Finance', 4, 6.5, 0.85),
        ('Tech', 4, 5, 0.75),
        ('Real Estate', 4, 3.5, 0.80)
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
        ('JPM', 6.5, 7, 0.65),
        ('AAPL', 6.5, 5.5, 0.50),
        ('NVDA', 6.5, 4, 0.55),
        ('O (REIT)', 6.5, 2.5, 0.70)
    ]

    for name, x, y, heat in stocks_t2:
        color_intensity = plt.cm.Oranges(heat + 0.2)
        circle = Circle((x, y), 0.3, facecolor=color_intensity, edgecolor='orange', linewidth=1.2)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=6, fontweight='bold')
        ax.text(x, y-0.5, f'h={heat:.2f}', ha='center', va='center', fontsize=6, color='darkorange')
        # Arrow from appropriate sector
        if 'JPM' in name or 'O' in name:
            source_y = 6.5 if 'JPM' in name else 3.5
        else:
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
    plt.savefig('heat_diffusion_flow.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Heat diffusion flow diagram generated: heat_diffusion_flow.png")
    plt.close()

def create_factor_taxonomy():
    """Generate comprehensive factor taxonomy visualization"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(7, 9.5, 'Tesla Stock: 10-Category Factor Taxonomy with Weight Ranges',
            ha='center', va='top', fontsize=14, fontweight='bold')

    # Central node
    center_circle = Circle((7, 5), 0.6, facecolor='gold', edgecolor='darkgoldenrod', linewidth=3, alpha=0.9)
    ax.add_patch(center_circle)
    ax.text(7, 5, 'TSLA\nStock\nPrice', ha='center', va='center', fontsize=10, fontweight='bold')

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
        ('Earnings\nDeliveries\nMargins', 0, 6.5, 0),
        ('Order\nImbalance\nVWAP', 45, 7, 1),
        ('Gamma\nExposure\nIV Rank', 90, 7, 2),
        ('RSI\nMACD\nBollinger', 135, 6.5, 3),
        ('Bloomberg\nReuters\nCNBC', 180, 6.5, 4),
        ('Twitter\nReddit\nStockTwits', 225, 6.5, 5),
        ('EV Sector\nTech Sector\nQQQ', 270, 7, 6),
        ('Fed Rates\nCPI\nGDP', 315, 7, 7),
        ('Lithium\nNickel\nChips', -45, 7, 8),
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

    # Add equation at bottom
    eq_text = r'$heat_{TSLA}(t) = \sum_{i=1}^{10} w_i(t) \cdot factor_i(t) + diffusion\_term(t)$'
    ax.text(7, 0.8, eq_text, ha='center', va='center', fontsize=12,
           bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', edgecolor='orange', linewidth=2))

    constraint_text = 'Constraint: $\sum_{i=1}^{10} w_i(t) = 1.0$ ∀t'
    ax.text(7, 0.3, constraint_text, ha='center', va='center', fontsize=11, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.6))

    plt.tight_layout()
    plt.savefig('factor_taxonomy_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Factor taxonomy diagram generated: factor_taxonomy_diagram.png")
    plt.close()

def create_dynamic_weight_adjustment():
    """Generate dynamic weight adjustment visualization across regimes"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Dynamic Weight Adjustment Across Market Regimes (Σwᵢ = 1.0)',
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
    plt.savefig('dynamic_weight_adjustment.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Dynamic weight adjustment diagram generated: dynamic_weight_adjustment.png")
    plt.close()

def create_time_series_weight_evolution():
    """Generate time series showing weight evolution during a market event"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Time points
    time = np.arange(0, 50, 1)

    # Simulate a shock event at t=10 (Fed rate hike)
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

    ax1.axvline(x=shock_time, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Fed Rate Hike')
    ax1.set_ylabel('Weight Value', fontsize=11, fontweight='bold')
    ax1.set_title('Dynamic Weight Evolution During Market Event', fontsize=12, fontweight='bold')
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
    plt.savefig('weight_time_evolution.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Weight time evolution diagram generated: weight_time_evolution.png")
    plt.close()

def main():
    """Generate all diagrams"""
    print("\n" + "="*60)
    print("Tesla Stock Heat Diffusion Model - Diagram Generator")
    print("="*60 + "\n")

    print("Generating professional diagrams for academic paper...\n")

    create_architecture_diagram()
    create_weight_distribution()
    create_heat_diffusion_flow()
    create_factor_taxonomy()
    create_dynamic_weight_adjustment()
    create_time_series_weight_evolution()

    print("\n" + "="*60)
    print("✓ All diagrams generated successfully!")
    print("="*60 + "\n")

    print("Generated files:")
    print("  1. tesla_architecture_diagram.png")
    print("  2. weight_distribution_diagram.png")
    print("  3. heat_diffusion_flow.png")
    print("  4. factor_taxonomy_diagram.png")
    print("  5. dynamic_weight_adjustment.png")
    print("  6. weight_time_evolution.png")
    print()

if __name__ == "__main__":
    main()
