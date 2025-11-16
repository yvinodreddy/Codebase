#!/usr/bin/env python3
"""
Generate visualization images for RAGHEAT system based on documentation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

def create_system_architecture():
    """Generate RAGHEAT System Architecture Diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'RAGHeat System Architecture',
            fontsize=20, fontweight='bold', ha='center')

    # Data Layer
    data_layer = FancyBboxPatch((0.5, 7.5), 9, 1.2,
                                boxstyle="round,pad=0.1",
                                edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax.add_patch(data_layer)
    ax.text(5, 8.3, 'Data Layer', fontsize=14, fontweight='bold', ha='center')
    ax.text(2, 7.9, 'Market Hours\nDetection', fontsize=10, ha='center')
    ax.text(5, 7.9, 'Real-time API\n(Market Open)', fontsize=10, ha='center')
    ax.text(8, 7.9, 'Synthetic Data\n(Market Closed)', fontsize=10, ha='center')

    # Processing Layer
    proc1 = FancyBboxPatch((0.5, 5.5), 2.5, 1.5,
                           boxstyle="round,pad=0.1",
                           edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(proc1)
    ax.text(1.75, 6.5, 'Heat Equation\nEngine', fontsize=11, fontweight='bold', ha='center')
    ax.text(1.75, 6, '2D Heat Diffusion\nSector Analysis', fontsize=9, ha='center')

    proc2 = FancyBboxPatch((3.5, 5.5), 2.5, 1.5,
                           boxstyle="round,pad=0.1",
                           edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(proc2)
    ax.text(4.75, 6.5, 'GraphRAG\nEngine', fontsize=11, fontweight='bold', ha='center')
    ax.text(4.75, 6, 'Knowledge Graph\n25+ Entities', fontsize=9, ha='center')

    proc3 = FancyBboxPatch((6.5, 5.5), 2.5, 1.5,
                           boxstyle="round,pad=0.1",
                           edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(proc3)
    ax.text(7.75, 6.5, 'PathRAG\nReasoning', fontsize=11, fontweight='bold', ha='center')
    ax.text(7.75, 6, 'Multi-hop\nPath Discovery', fontsize=9, ha='center')

    # Analysis Layer
    analysis = FancyBboxPatch((2, 3.5), 6, 1.2,
                              boxstyle="round,pad=0.1",
                              edgecolor='purple', facecolor='plum', linewidth=2)
    ax.add_patch(analysis)
    ax.text(5, 4.3, 'LLM Analysis Service', fontsize=14, fontweight='bold', ha='center')
    ax.text(5, 3.9, 'Multi-Modal Reasoning | Risk Assessment | Trading Signals', fontsize=10, ha='center')

    # Streaming Layer
    stream = FancyBboxPatch((1.5, 2), 7, 1,
                            boxstyle="round,pad=0.1",
                            edgecolor='orange', facecolor='moccasin', linewidth=2)
    ax.add_patch(stream)
    ax.text(5, 2.7, 'Kafka Streaming Pipeline', fontsize=12, fontweight='bold', ha='center')
    ax.text(5, 2.3, 'Real-time Data | Heat Maps | Graph Updates | Analysis Results', fontsize=9, ha='center')

    # Output Layer
    out1 = FancyBboxPatch((0.5, 0.3), 2.8, 1.2,
                          boxstyle="round,pad=0.1",
                          edgecolor='red', facecolor='lightcoral', linewidth=2)
    ax.add_patch(out1)
    ax.text(1.9, 1.1, 'Trading Dashboard', fontsize=11, fontweight='bold', ha='center')
    ax.text(1.9, 0.7, 'React UI\nReal-time Charts', fontsize=9, ha='center')

    out2 = FancyBboxPatch((3.8, 0.3), 2.8, 1.2,
                          boxstyle="round,pad=0.1",
                          edgecolor='red', facecolor='lightcoral', linewidth=2)
    ax.add_patch(out2)
    ax.text(5.2, 1.1, 'API Endpoints', fontsize=11, fontweight='bold', ha='center')
    ax.text(5.2, 0.7, 'FastAPI\nRESTful Services', fontsize=9, ha='center')

    out3 = FancyBboxPatch((7.1, 0.3), 2.4, 1.2,
                          boxstyle="round,pad=0.1",
                          edgecolor='red', facecolor='lightcoral', linewidth=2)
    ax.add_patch(out3)
    ax.text(8.3, 1.1, 'Alerts & Reports', fontsize=11, fontweight='bold', ha='center')
    ax.text(8.3, 0.7, 'Email/SMS\nPDF Reports', fontsize=9, ha='center')

    # Arrows
    arrow_props = dict(arrowstyle='->', lw=2, color='black')

    # Data to Processing
    ax.annotate('', xy=(1.75, 7), xytext=(1.75, 7.5), arrowprops=arrow_props)
    ax.annotate('', xy=(4.75, 7), xytext=(4.75, 7.5), arrowprops=arrow_props)
    ax.annotate('', xy=(7.75, 7), xytext=(7.75, 7.5), arrowprops=arrow_props)

    # Processing to Analysis
    ax.annotate('', xy=(3, 4.5), xytext=(1.75, 5.5), arrowprops=arrow_props)
    ax.annotate('', xy=(5, 4.5), xytext=(4.75, 5.5), arrowprops=arrow_props)
    ax.annotate('', xy=(7, 4.5), xytext=(7.75, 5.5), arrowprops=arrow_props)

    # Analysis to Streaming
    ax.annotate('', xy=(5, 3), xytext=(5, 3.5), arrowprops=arrow_props)

    # Streaming to Outputs
    ax.annotate('', xy=(1.9, 1.5), xytext=(3, 2), arrowprops=arrow_props)
    ax.annotate('', xy=(5.2, 1.5), xytext=(5, 2), arrowprops=arrow_props)
    ax.annotate('', xy=(8.3, 1.5), xytext=(7, 2), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/RAGHEAT/ragheat_architecture.png', dpi=300, bbox_inches='tight')
    print("✅ Created: ragheat_architecture.png")
    plt.close()


def create_heat_diffusion_diagram():
    """Generate Heat Diffusion Visualization"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Create heat map data
    x = np.linspace(0, 10, 100)
    y = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x, y)

    # Initial heat distribution (t=0)
    Z1 = np.exp(-((X-5)**2 + (Y-5)**2)/2)

    # Heat diffusion after time t (simulated)
    Z2 = np.exp(-((X-5)**2 + (Y-5)**2)/4)

    # Plot initial state
    im1 = ax1.contourf(X, Y, Z1, levels=20, cmap='hot')
    ax1.set_title('Initial Heat Distribution (t=0)\nMarket Event Impact', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Market Space X')
    ax1.set_ylabel('Market Space Y')
    plt.colorbar(im1, ax=ax1, label='Heat Intensity')

    # Plot diffused state
    im2 = ax2.contourf(X, Y, Z2, levels=20, cmap='hot')
    ax2.set_title('Heat Diffusion (t=Δt)\nSector Contagion Spread', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Market Space X')
    ax2.set_ylabel('Market Space Y')
    plt.colorbar(im2, ax=ax2, label='Heat Intensity')

    # Add equation
    fig.text(0.5, 0.02, r'Heat Equation: $\frac{\partial H}{\partial t} = \alpha \nabla^2 H + S(x,t)$',
             ha='center', fontsize=14, style='italic')

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/RAGHEAT/heat_diffusion_visualization.png', dpi=300, bbox_inches='tight')
    print("✅ Created: heat_diffusion_visualization.png")
    plt.close()


def create_graphrag_structure():
    """Generate GraphRAG Knowledge Graph Structure"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'GraphRAG Knowledge Graph Structure',
            fontsize=18, fontweight='bold', ha='center')

    # Central node - Market
    market = plt.Circle((5, 5), 0.5, color='red', alpha=0.7)
    ax.add_patch(market)
    ax.text(5, 5, 'Market', fontsize=12, fontweight='bold', ha='center', va='center', color='white')

    # Sector nodes
    sectors = [
        ('Tech', 2, 7, 'blue'),
        ('Finance', 8, 7, 'green'),
        ('Healthcare', 2, 3, 'purple'),
        ('Energy', 8, 3, 'orange'),
        ('Consumer', 5, 8.5, 'brown')
    ]

    for name, x, y, color in sectors:
        circle = plt.Circle((x, y), 0.4, color=color, alpha=0.7)
        ax.add_patch(circle)
        ax.text(x, y, name, fontsize=10, fontweight='bold', ha='center', va='center', color='white')

        # Draw connection to market
        ax.plot([x, 5], [y, 5], 'k--', alpha=0.5, linewidth=1.5)

    # Stock nodes (smaller)
    stocks = [
        ('AAPL', 1.5, 8, 'lightblue'),
        ('GOOGL', 2.5, 6.5, 'lightblue'),
        ('JPM', 7.5, 8, 'lightgreen'),
        ('BAC', 8.5, 6.5, 'lightgreen'),
        ('JNJ', 1.5, 2, 'plum'),
        ('PFE', 2.5, 3.5, 'plum'),
        ('XOM', 7.5, 2, 'moccasin'),
        ('CVX', 8.5, 3.5, 'moccasin')
    ]

    for name, x, y, color in stocks:
        circle = plt.Circle((x, y), 0.25, color=color, alpha=0.9, edgecolor='black', linewidth=1)
        ax.add_patch(circle)
        ax.text(x, y, name, fontsize=8, ha='center', va='center')

    # Legend
    legend_elements = [
        mpatches.Patch(color='red', label='Market (Root)'),
        mpatches.Patch(color='blue', label='Sectors'),
        mpatches.Patch(color='lightblue', label='Stocks'),
        mpatches.Patch(color='gray', label='Relationships')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

    # Add relationship types
    ax.text(0.5, 0.8, 'Relationships:\n• CONTAINS\n• CORRELATED_WITH\n• INFLUENCED_BY\n• HAS_SECTOR',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/RAGHEAT/graphrag_knowledge_graph.png', dpi=300, bbox_inches='tight')
    print("✅ Created: graphrag_knowledge_graph.png")
    plt.close()


def create_data_pipeline():
    """Generate Data Processing Pipeline"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'RAGHeat Data Processing Pipeline',
            fontsize=18, fontweight='bold', ha='center')

    # Stage 1: Input
    stage1 = FancyBboxPatch((0.3, 7), 1.8, 1.5,
                            boxstyle="round,pad=0.1",
                            edgecolor='blue', facecolor='lightblue', linewidth=2)
    ax.add_patch(stage1)
    ax.text(1.2, 8, 'Data\nIngestion', fontsize=11, fontweight='bold', ha='center')
    ax.text(1.2, 7.4, 'Market Hours\nDetection', fontsize=8, ha='center')

    # Stage 2: Routing
    stage2 = FancyBboxPatch((2.6, 7), 1.8, 1.5,
                            boxstyle="round,pad=0.1",
                            edgecolor='green', facecolor='lightgreen', linewidth=2)
    ax.add_patch(stage2)
    ax.text(3.5, 8, 'Smart\nRouting', fontsize=11, fontweight='bold', ha='center')
    ax.text(3.5, 7.4, 'Real-time or\nSynthetic', fontsize=8, ha='center')

    # Stage 3: Processing
    stage3a = FancyBboxPatch((4.9, 8.2), 1.5, 0.8,
                             boxstyle="round,pad=0.05",
                             edgecolor='purple', facecolor='plum', linewidth=1.5)
    ax.add_patch(stage3a)
    ax.text(5.65, 8.6, 'Heat\nEngine', fontsize=9, fontweight='bold', ha='center')

    stage3b = FancyBboxPatch((4.9, 7.2), 1.5, 0.8,
                             boxstyle="round,pad=0.05",
                             edgecolor='purple', facecolor='plum', linewidth=1.5)
    ax.add_patch(stage3b)
    ax.text(5.65, 7.6, 'GraphRAG', fontsize=9, fontweight='bold', ha='center')

    stage3c = FancyBboxPatch((4.9, 6.2), 1.5, 0.8,
                             boxstyle="round,pad=0.05",
                             edgecolor='purple', facecolor='plum', linewidth=1.5)
    ax.add_patch(stage3c)
    ax.text(5.65, 6.6, 'PathRAG', fontsize=9, fontweight='bold', ha='center')

    # Stage 4: Analysis
    stage4 = FancyBboxPatch((6.9, 7), 1.8, 1.5,
                            boxstyle="round,pad=0.1",
                            edgecolor='orange', facecolor='moccasin', linewidth=2)
    ax.add_patch(stage4)
    ax.text(7.8, 8, 'LLM\nAnalysis', fontsize=11, fontweight='bold', ha='center')
    ax.text(7.8, 7.4, 'Signal\nGeneration', fontsize=8, ha='center')

    # Stage 5: Output
    stage5 = FancyBboxPatch((9.2, 7), 0.7, 1.5,
                            boxstyle="round,pad=0.05",
                            edgecolor='red', facecolor='lightcoral', linewidth=2)
    ax.add_patch(stage5)
    ax.text(9.55, 7.75, 'Output', fontsize=10, fontweight='bold', ha='center', rotation=90, va='center')

    # Kafka Stream underneath
    kafka = FancyBboxPatch((0.3, 5), 9.4, 0.8,
                           boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='yellow', linewidth=2, alpha=0.3)
    ax.add_patch(kafka)
    ax.text(5, 5.4, 'Kafka Streaming Layer (Real-time Data Flow)',
            fontsize=12, fontweight='bold', ha='center', style='italic')

    # Neo4j Storage
    neo4j = FancyBboxPatch((0.3, 3.5), 4.5, 1,
                           boxstyle="round,pad=0.1",
                           edgecolor='darkgreen', facecolor='lightgreen', linewidth=2, alpha=0.5)
    ax.add_patch(neo4j)
    ax.text(2.55, 4, 'Neo4j Graph Database', fontsize=11, fontweight='bold', ha='center')
    ax.text(2.55, 3.7, 'Knowledge Graph Storage & Queries', fontsize=9, ha='center')

    # Metrics Storage
    metrics = FancyBboxPatch((5.2, 3.5), 4.5, 1,
                             boxstyle="round,pad=0.1",
                             edgecolor='darkblue', facecolor='lightblue', linewidth=2, alpha=0.5)
    ax.add_patch(metrics)
    ax.text(7.45, 4, 'Time-Series Database', fontsize=11, fontweight='bold', ha='center')
    ax.text(7.45, 3.7, 'Market Data & Heat Metrics', fontsize=9, ha='center')

    # Arrows
    arrow_props = dict(arrowstyle='->', lw=2.5, color='black')

    ax.annotate('', xy=(2.6, 7.75), xytext=(2.1, 7.75), arrowprops=arrow_props)
    ax.annotate('', xy=(4.9, 7.75), xytext=(4.4, 7.75), arrowprops=arrow_props)
    ax.annotate('', xy=(6.9, 7.75), xytext=(6.4, 7.75), arrowprops=arrow_props)
    ax.annotate('', xy=(9.2, 7.75), xytext=(8.7, 7.75), arrowprops=arrow_props)

    # Processing connections
    ax.plot([4.4, 4.9], [7.75, 8.6], 'k-', linewidth=2)
    ax.plot([4.4, 4.9], [7.75, 7.6], 'k-', linewidth=2)
    ax.plot([4.4, 4.9], [7.75, 6.6], 'k-', linewidth=2)

    ax.plot([6.4, 6.9], [8.6, 7.75], 'k-', linewidth=2)
    ax.plot([6.4, 6.9], [7.6, 7.75], 'k-', linewidth=2)
    ax.plot([6.4, 6.9], [6.6, 7.75], 'k-', linewidth=2)

    # Storage connections
    ax.annotate('', xy=(2.55, 5), xytext=(2.55, 5.8), arrowprops=dict(arrowstyle='<->', lw=1.5, color='green'))
    ax.annotate('', xy=(7.45, 5), xytext=(7.45, 5.8), arrowprops=dict(arrowstyle='<->', lw=1.5, color='blue'))

    # Timeline
    ax.text(5, 2.5, 'Processing Timeline: 5-10 seconds per cycle',
            fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Metrics
    ax.text(1, 1.5, '📊 Throughput:\n• 1000+ events/sec\n• 5-sec latency\n• 99.9% uptime',
            fontsize=9, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

    ax.text(5, 1.5, '🔥 Heat Processing:\n• 2D PDE Solver\n• Convergence: <100ms\n• Accuracy: 99%+',
            fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

    ax.text(9, 1.5, '🧠 AI Analysis:\n• Multi-hop reasoning\n• Confidence scoring\n• Explainable AI',
            fontsize=9, ha='right',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    plt.tight_layout()
    plt.savefig('/home/user01/claude-test/RAGHEAT/data_processing_pipeline.png', dpi=300, bbox_inches='tight')
    print("✅ Created: data_processing_pipeline.png")
    plt.close()


if __name__ == '__main__':
    print("🎨 Generating RAGHeat System Images...")
    print("=" * 60)

    create_system_architecture()
    create_heat_diffusion_diagram()
    create_graphrag_structure()
    create_data_pipeline()

    print("=" * 60)
    print("✅ All images generated successfully!")
    print("\nGenerated files:")
    print("  1. ragheat_architecture.png - System architecture overview")
    print("  2. heat_diffusion_visualization.png - Heat equation visualization")
    print("  3. graphrag_knowledge_graph.png - Knowledge graph structure")
    print("  4. data_processing_pipeline.png - Complete data pipeline")
    print("\n📍 Location: /home/user01/claude-test/RAGHEAT/")
