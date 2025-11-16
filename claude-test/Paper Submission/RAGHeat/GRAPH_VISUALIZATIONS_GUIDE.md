# Graph Network Visualizations Guide

## 🔗 Neo4j-Style Graph Diagrams for Stock Heat Diffusion Model

**Version:** 2.0
**Last Updated:** November 8, 2025
**Library:** NetworkX + Matplotlib

---

## 📌 Overview

The Stock Heat Diffusion Model now generates **4 professional graph network visualizations** inspired by Neo4j knowledge graph visualizations. These diagrams provide an alternative representation of the heat diffusion model, showing entity relationships, influence networks, and temporal propagation.

### Why Graph Visualizations?

1. **Intuitive Representation**: Graph structures naturally represent relationships between financial entities
2. **Neo4j Compatibility**: Visual style matches Neo4j Browser output for consistency
3. **Publication Quality**: 300 DPI, professional styling, suitable for academic papers
4. **Interactive Insights**: Shows network topology, clustering, and information flow

---

## 🎨 Visualization Types

### 1. Knowledge Graph Network (`*_knowledge_graph_network.png`)

**Purpose**: Complete entity-relationship structure of the heat diffusion model

**Graph Structure**:
- **Graph Type**: Directed graph (DiGraph)
- **Layout**: Spring layout (Fruchterman-Reingold algorithm)
- **Nodes**: 36 total (1 stock + 10 factors + 25 entities)
- **Edges**: Directed relationships with labels

**Node Types**:

| Node Type | Color | Size | Count | Examples |
|-----------|-------|------|-------|----------|
| Stock | 🔴 Red (#E74C3C) | 3000 | 1 | AAPL_STOCK |
| Factors | 🟣 Purple (#9B59B6) | 2000 | 10 | MICRO, ORDERFLOW, OPTIONS, etc. |
| Entities | ⚪ Gray (#95A5A6) | 1200 | 25 | EARNINGS, VWAP, GAMMA, RSI, etc. |

**Relationships**:
- **INFLUENCES**: Factor → Stock (weight=0.1)
- **CONTRIBUTES_TO**: Entity → Factor (weight=0.05)

**Key Features**:
- Legend showing node types
- Stats box with node/edge counts
- White labels on colored nodes for readability
- Arrow directions showing influence flow

**File Size**: ~1.3 MB (detailed, high-resolution)

**Use Cases**:
- Understanding complete knowledge graph structure
- Visualizing entity hierarchies
- Identifying factor-entity relationships

---

### 2. Factor Influence Graph (`*_factor_influence_graph.png`)

**Purpose**: Factor-to-factor influence and correlation network

**Graph Structure**:
- **Graph Type**: Weighted directed graph
- **Layout**: Spring layout with k=1.5
- **Nodes**: 7 major factors
- **Edges**: 12 influence relationships

**Visual Encoding**:

| Element | Encoding | Meaning |
|---------|----------|---------|
| Node Size | Proportional to weight | Larger = higher baseline weight |
| Node Color | Yellow → Orange → Red | Heat map by weight value |
| Edge Thickness | 4 × influence strength | Thicker = stronger influence |
| Edge Direction | Arrow | Direction of influence |

**Factors Included**:
1. **Macro** (w=0.10) - Macroeconomic indicators
2. **Micro** (w=0.28) - Company fundamentals
3. **News** (w=0.12) - News sentiment
4. **Social** (w=0.08) - Social media signals
5. **Technical** (w=0.15) - Technical indicators
6. **OrderFlow** (w=0.18) - Order flow data
7. **Options** (w=0.09) - Options flow

**Key Influences** (strength > 0.6):
- News → Social (0.75) - Strong correlation
- OrderFlow → Technical (0.70) - Price action drives technicals
- Options → OrderFlow (0.65) - Derivatives impact order flow
- News → Micro (0.60) - Fundamental news affects company metrics

**Key Features**:
- Colorbar showing weight scale (0.0 → 0.30)
- Weight labels (w=X.XX) below each node
- Curved edges with arc3 style
- Σwᵢ = 1.0 constraint annotation

**Use Cases**:
- Analyzing factor correlations
- Understanding feedback loops
- Identifying key factor dependencies

---

### 3. Heat Propagation Graph (`*_heat_propagation_graph.png`)

**Purpose**: Multi-hop heat diffusion across temporal layers

**Graph Structure**:
- **Graph Type**: Directed acyclic graph (DAG)
- **Layout**: Multipartite layout (vertical layers)
- **Nodes**: 16 total across 4 time layers
- **Edges**: Propagation paths with varying opacity

**Temporal Layers**:

| Layer | Time | Nodes | Heat Range | Description |
|-------|------|-------|------------|-------------|
| 0 | t=0 | 1 | h=1.0 | Market event (source) |
| 1 | t=1 | 3 | h=0.70-0.85 | Immediate impact (stock, sector, ETF) |
| 2 | t=2 | 5 | h=0.45-0.55 | Secondary impact (peers, supply chain) |
| 3 | t=3 | 7 | h=0.25-0.35 | Tertiary impact (derivatives, intl markets) |

**Visual Encoding**:

| Element | Encoding | Meaning |
|---------|----------|---------|
| Node Color | White → Pink → Red | Heat intensity (cmap='Reds') |
| Edge Color | Orange (#E67E22) | Heat propagation path |
| Edge Opacity | 0.8 × diffusion_weight | Strength of connection |
| Heat Labels | h=X.XX below nodes | Exact heat values |

**Heat Decay Pattern**:
- Layer 0: h = 1.00 (100% intensity)
- Layer 1: h ≈ 0.75 (25% decay)
- Layer 2: h ≈ 0.50 (50% decay)
- Layer 3: h ≈ 0.30 (70% decay)

**Key Features**:
- Colorbar showing heat scale (0.0 → 1.0)
- Time labels for each layer
- Equation: h(t) = exp(-βLt)·h₀
- Company ticker in layer 1 stock node

**Use Cases**:
- Visualizing heat diffusion dynamics
- Understanding multi-hop propagation
- Analyzing temporal decay patterns
- Identifying critical nodes in diffusion path

---

### 4. Market Event Impact Graph (`*_market_event_impact_graph.png`)

**Purpose**: Entity relationships and information flow from market events

**Graph Structure**:
- **Graph Type**: Undirected graph
- **Layout**: Spring layout with k=1.2
- **Nodes**: 25 entities
- **Edges**: 40+ relationships

**Entity Categories**:

| Category | Color | Size | Count | Examples |
|----------|-------|------|-------|----------|
| Event | 🔴 Red (#E74C3C) | 2500 | 1 | Earnings beat |
| Stock | 🔵 Blue (#3498DB) | 2000 | 1 | AAPL stock |
| Derivatives | 🟣 Purple (#9B59B6) | 1500 | 3 | Calls, puts, futures |
| Participants | 🟠 Orange (#F39C12) | 1500 | 4 | Retail, hedge funds, institutions |
| Media | 🟢 Teal (#1ABC9C) | 1200 | 4 | Bloomberg, Twitter, Reddit |
| Related Stocks | ⚪ Gray (#95A5A6) | 1200 | 4 | Peers, suppliers, ETF |

**Information Flow Patterns**:
1. **Event → Direct Impact**: Event connects to stock, derivatives, and media
2. **Stock → Participants**: Stock connects to all trader types
3. **Derivatives → Participants**: Options/futures link to traders
4. **Media → Retail**: Social media influences retail traders
5. **Stock → Related**: Sector correlation through ETF and peers

**Network Metrics Displayed**:
- Total entities count
- Total relationships (edges)
- Average degree (connections per node)

**Key Features**:
- Multi-column legend with all 6 entity types
- Stats box in bottom-right corner
- Undirected edges (bidirectional information flow)
- Company ticker in stock and futures nodes

**Use Cases**:
- Understanding market event propagation
- Analyzing participant behavior
- Mapping information channels
- Identifying key intermediaries

---

## 🎯 Comparison: Graph vs. Original Diagrams

### Original Diagrams (6 files)

**Focus**: System architecture, weight distributions, mathematical flow

**Strengths**:
- Show complete pipeline (data → processing → LLM)
- Detailed weight breakdowns with verification
- Time series evolution
- Regime-specific adjustments

**Best For**:
- Understanding system design
- Mathematical verification (Σwᵢ = 1.0)
- Weight calibration
- Temporal dynamics

### Graph Network Visualizations (4 files)

**Focus**: Entity relationships, influence networks, propagation topology

**Strengths**:
- Intuitive network topology
- Neo4j-style professional appearance
- Entity-relationship structure
- Multi-hop propagation visualization

**Best For**:
- Knowledge graph representation
- Factor correlation analysis
- Heat diffusion visualization
- Event impact pathways

### Complementary Usage

**For Academic Papers**: Use both sets
- Original diagrams for methodology/architecture sections
- Graph visualizations for conceptual model and results sections

**For Presentations**: Prefer graph visualizations
- More visually intuitive
- Better for non-technical audiences
- Clear entity relationships

**For Technical Documentation**: Prefer original diagrams
- More detailed mathematical content
- Explicit weight constraints
- System architecture clarity

---

## 🔧 Technical Implementation

### NetworkX Graph Types Used

```python
# Knowledge Graph Network
G = nx.DiGraph()  # Directed graph for hierarchical relationships

# Factor Influence Graph
G = nx.DiGraph()  # Directed for one-way influences

# Heat Propagation Graph
G = nx.DiGraph()  # Directed acyclic graph (DAG) for temporal flow

# Market Event Impact Graph
G = nx.Graph()    # Undirected for bidirectional information flow
```

### Layout Algorithms

| Visualization | Algorithm | Parameters | Reasoning |
|--------------|-----------|------------|-----------|
| Knowledge Graph | Spring Layout | k=2, iterations=50 | Natural clustering of entity types |
| Factor Influence | Spring Layout | k=1.5, iterations=50 | Balanced node spacing |
| Heat Propagation | Multipartite | subset_key='layer' | Clear temporal layers |
| Market Event | Spring Layout | k=1.2, iterations=50 | Dense network with many connections |

### Color Schemes

**Node Colors** (carefully chosen for clarity):
- Stock: Red (#E74C3C) - High importance, central role
- Factors: Purple (#9B59B6) - Intermediate layer
- Entities: Gray (#95A5A6) - Leaf nodes
- Derivatives: Purple (#9B59B6) - Financial instruments
- Participants: Orange (#F39C12) - Human actors
- Media: Teal (#1ABC9C) - Information channels

**Edge Colors**:
- Gray (#999999, #BDC3C7) - General relationships
- Orange (#E67E22) - Heat propagation
- Blue (#3498DB) - Factor influences

**Colormaps**:
- `Reds`: Heat intensity (0.0 → 1.0)
- `YlOrRd`: Weight values (0.0 → 0.30)

---

## 📊 File Size and Performance

### Expected File Sizes

| Visualization | Typical Size | Resolution | Nodes | Edges |
|--------------|--------------|------------|-------|-------|
| Knowledge Graph Network | 1.0-1.5 MB | 16×12 in @ 300 DPI | 36 | 35 |
| Factor Influence Graph | 400-500 KB | 14×10 in @ 300 DPI | 7 | 12 |
| Heat Propagation Graph | 500-700 KB | 16×10 in @ 300 DPI | 16 | 21 |
| Market Event Impact | 600-800 KB | 14×12 in @ 300 DPI | 25 | 40+ |

### Generation Time

On typical hardware:
- **Each graph**: 1-2 seconds
- **All 4 graphs**: 5-8 seconds
- **Complete suite (10 diagrams)**: 15-25 seconds

---

## 🚀 Usage Examples

### Generate All Diagrams

```bash
# Apple Inc. - generates all 10 diagrams
python3 generate_diagrams_generic.py -t AAPL -c "Apple Inc."

# Output includes:
# - 6 original diagrams
# - 4 graph network visualizations
```

### Verify Graph Files

```bash
# Check generated graph files
ls -lh aapl_*graph*.png

# Expected output:
# aapl_knowledge_graph_network.png    (1.3M)
# aapl_factor_influence_graph.png     (480K)
# aapl_heat_propagation_graph.png     (607K)
# aapl_market_event_impact_graph.png  (694K)
```

### View Graph Statistics

Each graph includes a stats box showing:
- Node count
- Edge count
- Average degree (for undirected graphs)
- Factor/entity breakdown (for knowledge graph)

---

## 🎓 Academic Applications

### Conference Papers

**Recommended Diagrams**:
1. **Introduction**: Market Event Impact Graph (shows motivation)
2. **Methodology**: Architecture Diagram + Knowledge Graph Network
3. **Model Description**: Factor Taxonomy + Factor Influence Graph
4. **Results**: Heat Propagation Graph + Weight Time Evolution

### Journal Articles

**Full Suite**: Use all 10 diagrams across sections
- Abstract/Overview: Architecture Diagram
- Literature Review: Factor Taxonomy
- Methodology: Knowledge Graph Network + Factor Influence Graph
- Implementation: Dynamic Weight Adjustment
- Experiments: Heat Propagation Graph
- Results: Weight Time Evolution
- Discussion: Market Event Impact Graph

### Presentations

**Prioritize Graph Visualizations** (more intuitive):
1. Slide 1: Market Event Impact Graph (problem statement)
2. Slide 2: Knowledge Graph Network (solution overview)
3. Slide 3: Factor Influence Graph (key innovation)
4. Slide 4: Heat Propagation Graph (results)

---

## 🔍 Customization Guide

### Modifying Node Colors

Edit `node_types` dictionaries in each function:

```python
# In create_market_event_impact_graph()
node_types = {
    'event': ('#YOUR_COLOR', size),
    'stock': ('#YOUR_COLOR', size),
    # ...
}
```

### Changing Layout

Replace spring layout with alternatives:

```python
# Circular layout
pos = nx.circular_layout(G)

# Kamada-Kawai layout
pos = nx.kamada_kawai_layout(G)

# Shell layout (concentric circles)
pos = nx.shell_layout(G)

# Spectral layout
pos = nx.spectral_layout(G)
```

### Adding More Entities

In `create_knowledge_graph_network()`:

```python
entities = {
    'MICRO': [
        ('EARNINGS', 'Earnings\nReport'),
        ('YOUR_ENTITY', 'Your\nLabel'),  # Add here
    ],
    # ...
}
```

---

## 📞 Support and Troubleshooting

### Common Issues

**Issue 1**: "Module 'networkx' not found"
```bash
# Solution
pip3 install --break-system-packages networkx
```

**Issue 2**: Graph layout looks crowded
```python
# Solution: Increase k parameter in spring_layout
pos = nx.spring_layout(G, k=3, iterations=100)  # Increase from default k=2
```

**Issue 3**: Node labels overlap
```python
# Solution: Reduce font size or increase figure size
fig, ax = plt.subplots(figsize=(18, 14))  # Increase from (16, 12)
```

**Issue 4**: Large file sizes
```python
# Solution: Reduce DPI (trade-off with quality)
plt.savefig(filename, dpi=200)  # Reduce from 300
```

---

## ✅ Quality Checklist

Before using graph visualizations in publications:

- [ ] All node labels are readable
- [ ] Color contrast is sufficient (test with grayscale conversion)
- [ ] Stats boxes don't overlap with graph
- [ ] Legend is complete and clear
- [ ] Arrows point in correct direction (for directed graphs)
- [ ] File size is reasonable (<2 MB per graph)
- [ ] Company ticker appears in all relevant nodes
- [ ] Edge thickness reflects actual weights/influences
- [ ] No overlapping nodes or edges
- [ ] Title clearly describes the visualization

---

## 🏆 Summary

### Graph Visualizations Add Value By:

1. ✅ **Neo4j-style appearance** matches industry-standard knowledge graphs
2. ✅ **Entity relationships** clearly show network structure
3. ✅ **Multi-layer visualization** illustrates temporal propagation
4. ✅ **Professional quality** suitable for top-tier conferences
5. ✅ **Ticker-agnostic** works for ANY publicly traded company
6. ✅ **Mathematically accurate** node sizes/colors reflect actual weights
7. ✅ **Comprehensive coverage** 4 complementary graph perspectives
8. ✅ **High resolution** 300 DPI for publication quality

### Total Package

**10 Diagrams = Complete Visual Suite**
- 6 Original (system architecture, weights, time series)
- 4 Graph Networks (knowledge graph, influence, propagation, events)

**Universal Application**
- Any ticker symbol
- Any sector (Technology, Financial, Energy, etc.)
- Any market event type
- Any time scale

---

**Version:** 2.0
**Library Dependencies:** matplotlib, seaborn, numpy, networkx
**Python Version:** 3.8+
**License:** Compatible with academic and commercial use
**Status:** ✅ Production Ready

---

**Next Steps:**
1. Generate diagrams for your target ticker
2. Review all 10 visualizations
3. Select appropriate subset for your use case
4. Customize colors/layout if needed
5. Include in publication with proper citations
