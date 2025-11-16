# Diagram Generator Usage Guide

## 📊 Overview

The **Stock Heat Diffusion Model** now includes TWO diagram generators:
1. **`generate_diagrams.py`** - Tesla-specific (original, 6 diagrams)
2. **`generate_diagrams_generic.py`** - **Universal** (works for ANY company, **10 diagrams**) ✅

## 🆕 **NEW: Graph Network Visualizations!**

Version 2.0 adds **4 Neo4j-style graph visualizations** inspired by the knowledge graph format:

1. **Knowledge Graph Network** - Full entity-relationship structure showing stock → factors → entities
2. **Factor Influence Graph** - Weighted network showing factor-to-factor correlations
3. **Heat Propagation Graph** - Multi-layer temporal diffusion across market entities
4. **Market Event Impact Graph** - Information flow from events through participants and media

**Total Output:** 10 professional diagrams per ticker (6 original + 4 graph networks)

---

## 🆕 Generic Diagram Generator

### Features
- ✅ **Ticker-agnostic**: Works for any stock (AAPL, MSFT, GOOGL, JPM, XOM, etc.)
- ✅ **Command-line arguments**: Easy to customize
- ✅ **Flexible naming**: Auto-generates filenames based on ticker
- ✅ **Weight constraint verified**: All diagrams maintain Σwᵢ = 1.0
- ✅ **Professional quality**: 300 DPI, publication-ready

---

## 🚀 Quick Start Examples

### Example 1: Apple Inc. (AAPL)
```bash
cd "/home/user01/claude-test/Paper Submission/RAGHeat"

# Generate all diagrams for Apple
python3 generate_diagrams_generic.py --ticker AAPL --company "Apple Inc."

# Or using short flags
python3 generate_diagrams_generic.py -t AAPL -c "Apple Inc."
```

**Output files (10 diagrams):**
```
📊 Original Diagrams:
aapl_architecture_diagram.png
aapl_weight_distribution.png
aapl_heat_diffusion_flow.png
aapl_factor_taxonomy.png
aapl_dynamic_weight_adjustment.png
aapl_weight_time_evolution.png

🔗 Graph Network Visualizations (Neo4j-style):
aapl_knowledge_graph_network.png
aapl_factor_influence_graph.png
aapl_heat_propagation_graph.png
aapl_market_event_impact_graph.png
```

---

### Example 2: Microsoft (MSFT)
```bash
python3 generate_diagrams_generic.py --ticker MSFT --company "Microsoft Corporation"
```

**Output files (10 diagrams):**
```
📊 Original: msft_architecture_diagram.png, msft_weight_distribution.png, etc.
🔗 Graphs: msft_knowledge_graph_network.png, msft_factor_influence_graph.png, etc.
(Total: 10 PNG files)
```

---

### Example 3: JPMorgan Chase (JPM)
```bash
python3 generate_diagrams_generic.py --ticker JPM --company "JPMorgan Chase & Co."
```

**Output files (10 diagrams):**
```
📊 Original: jpm_architecture_diagram.png, jpm_weight_distribution.png, etc.
🔗 Graphs: jpm_knowledge_graph_network.png, jpm_factor_influence_graph.png, etc.
(Total: 10 PNG files)
```

---

### Example 4: Exxon Mobil (XOM) - Energy Sector
```bash
python3 generate_diagrams_generic.py --ticker XOM --company "Exxon Mobil Corp."
```

**Output files (10 diagrams):**
```
📊 Original: xom_architecture_diagram.png, xom_weight_distribution.png, etc.
🔗 Graphs: xom_knowledge_graph_network.png, xom_factor_influence_graph.png, etc.
(Total: 10 PNG files)
```

---

### Example 5: Custom Prefix
```bash
# Use a custom filename prefix
python3 generate_diagrams_generic.py \
  --ticker GOOGL \
  --company "Alphabet Inc." \
  --prefix alphabet_stock

# Output files will be:
# alphabet_stock_architecture_diagram.png
# alphabet_stock_weight_distribution.png
# etc.
```

---

## 📋 Command-Line Arguments

### Required: None (has defaults)

### Optional Arguments

| Argument | Short | Default | Description | Example |
|----------|-------|---------|-------------|---------|
| `--ticker` | `-t` | `STOCK` | Stock ticker symbol | `AAPL`, `MSFT`, `JPM` |
| `--company` | `-c` | Same as ticker | Company full name | `"Apple Inc."` |
| `--prefix` | `-p` | Lowercase ticker | Output filename prefix | `apple`, `custom_name` |

---

## 🎯 Usage Scenarios

### Scenario 1: Default (Generic Stock)
```bash
# No arguments - creates generic "STOCK" diagrams
python3 generate_diagrams_generic.py
```
**Output:** `stock_*.png` files

---

### Scenario 2: Ticker Only
```bash
# Provide only ticker - company name defaults to ticker
python3 generate_diagrams_generic.py --ticker NVDA
```
**Output:**
- Titles: "NVDA: ..."
- Files: `nvda_*.png`

---

### Scenario 3: Full Specification
```bash
# Provide all parameters for maximum customization
python3 generate_diagrams_generic.py \
  --ticker TSLA \
  --company "Tesla Inc." \
  --prefix tesla_heat_model
```
**Output:**
- Titles: "Tesla Inc. (TSLA): ..."
- Files: `tesla_heat_model_*.png`

---

## 📊 Generated Diagrams Details

### 📈 Original Diagrams (6 files)

### 1. Architecture Diagram (`*_architecture_diagram.png`)
- **Shows**: Complete system architecture
- **Includes**: Data sources → Processing → Storage → Heat Engine → LLM
- **Title**: Uses company name and ticker
- **Key Feature**: Shows Σwᵢ = 1 in heat engine

### 2. Weight Distribution (`*_weight_distribution.png`)
- **Shows**: Pie chart + bar chart with ranges
- **Includes**: All 10 factor categories
- **Title**: Company name with ticker
- **Verification**: Displays Σwᵢ = 1.0 constraint at bottom

### 3. Heat Diffusion Flow (`*_heat_diffusion_flow.png`)
- **Shows**: Multi-hop propagation through network
- **Includes**: Event → Immediate → 1-hop → 2-hop → Steady state
- **Title**: "Heat Diffusion Process: Market Event Impact Propagation"
- **Generic**: No company-specific elements

### 4. Factor Taxonomy (`*_factor_taxonomy.png`)
- **Shows**: Central ticker with 10 surrounding factor categories
- **Includes**: Ticker in center, factor examples
- **Title**: Company name with ticker
- **Equation**: Uses ticker variable (e.g., heat_AAPL(t))

### 5. Dynamic Weight Adjustment (`*_dynamic_weight_adjustment.png`)
- **Shows**: 4 market regimes (Bull/Bear/Volatility/Sideways)
- **Includes**: Weight bar charts for each regime
- **Title**: Company name with ticker
- **Verification**: Σw = 1.00 shown for each regime

### 6. Weight Time Evolution (`*_weight_time_evolution.png`)
- **Shows**: Time series of weight changes during market event
- **Includes**: Individual trajectories + stacked area
- **Title**: Company name with ticker
- **Verification**: Stacked area always sums to 1.0

---

### 🔗 Graph Network Visualizations (4 files - NEW!)

### 7. Knowledge Graph Network (`*_knowledge_graph_network.png`)
- **Style**: Neo4j-inspired graph visualization
- **Shows**: Complete knowledge graph structure
- **Nodes**:
  - 🔴 Red: Stock (central node)
  - 🟣 Purple: 10 factor categories
  - ⚪ Gray: Entity nodes (earnings, VWAP, gamma, RSI, etc.)
- **Edges**: INFLUENCES and CONTRIBUTES_TO relationships
- **Layout**: Spring layout algorithm (networkx)
- **Stats Box**: Node/edge counts displayed
- **Size**: ~1.3 MB (large, detailed visualization)
- **Company-Specific**: Yes - ticker appears in stock node

### 8. Factor Influence Graph (`*_factor_influence_graph.png`)
- **Style**: Weighted directed graph
- **Shows**: Factor-to-factor influence relationships
- **Node Size**: Proportional to baseline weight
- **Node Color**: Heat map (yellow → orange → red) by weight
- **Edge Thickness**: Proportional to influence strength
- **Features**:
  - Weight labels (w=0.28, etc.) below each factor
  - Colorbar showing weight scale
  - Directional arrows showing influence flow
- **Examples**: News → Social (0.75), OrderFlow → Technical (0.70)
- **Verification**: "Σwᵢ = 1.0" constraint displayed
- **Company-Specific**: Yes - company name in title

### 9. Heat Propagation Graph (`*_heat_propagation_graph.png`)
- **Style**: Multi-layer temporal network
- **Shows**: Heat diffusion across 4 time layers
- **Layers**:
  - **t=0**: Market event (h=1.0)
  - **t=1**: Immediate impact - ticker stock, sector index, ETF
  - **t=2**: Secondary impact - peer stocks, suppliers, customers
  - **t=3**: Tertiary impact - supply chain, correlated stocks, derivatives
- **Node Color**: Heat intensity (white → red gradient)
- **Heat Labels**: h=0.85, h=0.55, h=0.30, etc.
- **Edge Opacity**: Proportional to diffusion weight
- **Colorbar**: Heat intensity scale (0.0 → 1.0)
- **Equation**: "h(t) = exp(-βLt)·h₀" in title
- **Company-Specific**: Yes - ticker in layer 1 nodes

### 10. Market Event Impact Graph (`*_market_event_impact_graph.png`)
- **Style**: Entity-relationship network
- **Shows**: Information flow from market event
- **Node Types**:
  - 🔴 Red: Event (earnings beat, etc.)
  - 🔵 Blue: Stock
  - 🟣 Purple: Derivatives (calls, puts, futures)
  - 🟠 Orange: Market participants (retail, hedge funds, institutions)
  - 🟢 Teal: Media (Bloomberg, Twitter, Reddit)
  - ⚪ Gray: Related stocks (peers, suppliers, ETF)
- **Relationships**: Undirected edges showing connections
- **Stats Box**: Total entities, relationships, average degree
- **Legend**: Node type legend with color coding
- **Company-Specific**: Yes - ticker in stock and futures nodes

---

## 🔧 Comparison: Tesla vs. Generic

### Tesla-Specific (`generate_diagrams.py`)

```bash
# Only works for Tesla
python3 generate_diagrams.py

# Output files:
# tesla_architecture_diagram.png
# All hardcoded "Tesla" and "TSLA"
```

**Hardcoded elements:**
- "Tesla Stock Heat Diffusion Model"
- "TSLA Stock Price" in center
- "heat_TSLA(t)" in equations
- All filenames start with "tesla_"

---

### Generic Version (`generate_diagrams_generic.py`)

```bash
# Works for ANY company
python3 generate_diagrams_generic.py --ticker AAPL --company "Apple Inc."

# Output files:
# aapl_architecture_diagram.png
# All references use provided ticker/company name
```

**Parameterized elements:**
- "{company_name} Stock Heat Diffusion Model"
- "{ticker} Stock Price" in center
- "heat_{ticker}(t)" in equations
- All filenames use provided prefix

---

## 🎨 Customization Examples

### Example 1: Multiple Companies in Batch
```bash
#!/bin/bash
# Generate diagrams for portfolio of stocks

companies=(
  "AAPL:Apple Inc."
  "MSFT:Microsoft Corporation"
  "GOOGL:Alphabet Inc."
  "AMZN:Amazon.com Inc."
  "META:Meta Platforms Inc."
)

for company in "${companies[@]}"; do
  ticker="${company%%:*}"
  name="${company##*:}"
  echo "Generating diagrams for $ticker ($name)..."
  python3 generate_diagrams_generic.py --ticker "$ticker" --company "$name"
  echo ""
done
```

---

### Example 2: Energy Sector Analysis
```bash
# Generate for multiple energy stocks
python3 generate_diagrams_generic.py -t XOM -c "Exxon Mobil"
python3 generate_diagrams_generic.py -t CVX -c "Chevron Corporation"
python3 generate_diagrams_generic.py -t COP -c "ConocoPhillips"
```

---

### Example 3: Financial Sector
```bash
# Generate for banks
python3 generate_diagrams_generic.py -t JPM -c "JPMorgan Chase"
python3 generate_diagrams_generic.py -t BAC -c "Bank of America"
python3 generate_diagrams_generic.py -t WFC -c "Wells Fargo"
python3 generate_diagrams_generic.py -t GS -c "Goldman Sachs"
```

---

## ⚠️ Troubleshooting

### Issue 1: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'matplotlib'
```

**Solution:**
```bash
# Install required packages
pip3 install matplotlib seaborn numpy

# Or in virtual environment
python3 -m venv venv
source venv/bin/activate
pip install matplotlib seaborn numpy
python3 generate_diagrams_generic.py --ticker AAPL
```

---

### Issue 2: Invalid escape sequence warning
```
SyntaxWarning: invalid escape sequence
```

**Solution:** This is a non-blocking warning. The diagrams still generate correctly. Already fixed in the generic version using raw strings where needed.

---

### Issue 3: Permission denied
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Make script executable
chmod +x generate_diagrams_generic.py

# Run with python3 explicitly
python3 generate_diagrams_generic.py --ticker AAPL
```

---

## 📈 Weight Constraint Verification

### Automatic Verification

The generic diagram generator includes automatic verification:

```python
# Baseline weights
assert abs(sum(baseline_weights) - 1.0) < 0.001

# Each regime
assert abs(sum(weights) - 1.0) < 0.001

# Time series
assert np.allclose(total, 1.0)
```

**If weights don't sum to 1.0, the script will fail with an assertion error.**

---

## 🎯 Best Practices

### 1. Use Full Company Names
```bash
# Good
python3 generate_diagrams_generic.py -t AAPL -c "Apple Inc."

# Works but less professional in diagrams
python3 generate_diagrams_generic.py -t AAPL -c "Apple"
```

### 2. Use Consistent Naming
```bash
# For a paper, use consistent prefix
python3 generate_diagrams_generic.py -t AAPL -c "Apple Inc." -p apple_stock
python3 generate_diagrams_generic.py -t MSFT -c "Microsoft Corp." -p microsoft_stock
```

### 3. Organize Output
```bash
# Create diagrams directory
mkdir -p diagrams/aapl
cd diagrams/aapl

# Generate with custom prefix
python3 ../../generate_diagrams_generic.py -t AAPL -c "Apple Inc." -p aapl
```

---

## 📊 Sample Output

### Running for Apple Inc.

```bash
$ python3 generate_diagrams_generic.py --ticker AAPL --company "Apple Inc."

======================================================================
Stock Heat Diffusion Model - Diagram Generator
======================================================================

Ticker Symbol:  AAPL
Company Name:   Apple Inc.
Output Prefix:  aapl

Generating professional diagrams for academic paper...

✓ Architecture diagram generated: aapl_architecture_diagram.png
✓ Weight distribution diagram generated: aapl_weight_distribution.png
✓ Heat diffusion flow diagram generated: aapl_heat_diffusion_flow.png
✓ Factor taxonomy diagram generated: aapl_factor_taxonomy.png
✓ Dynamic weight adjustment diagram generated: aapl_dynamic_weight_adjustment.png
✓ Weight time evolution diagram generated: aapl_weight_time_evolution.png
✓ Knowledge graph network generated: aapl_knowledge_graph_network.png
✓ Factor influence graph generated: aapl_factor_influence_graph.png
✓ Heat propagation graph generated: aapl_heat_propagation_graph.png
✓ Market event impact graph generated: aapl_market_event_impact_graph.png

======================================================================
✓ All diagrams generated successfully!
======================================================================

Generated files:

📊 Original Diagrams:
  1. aapl_architecture_diagram.png
  2. aapl_weight_distribution.png
  3. aapl_heat_diffusion_flow.png
  4. aapl_factor_taxonomy.png
  5. aapl_dynamic_weight_adjustment.png
  6. aapl_weight_time_evolution.png

🔗 Graph Network Visualizations:
  7. aapl_knowledge_graph_network.png
  8. aapl_factor_influence_graph.png
  9. aapl_heat_propagation_graph.png
 10. aapl_market_event_impact_graph.png

All weight constraints verified: Σwᵢ = 1.0 ✓
```

---

## 🔍 Help Command

```bash
$ python3 generate_diagrams_generic.py --help

usage: generate_diagrams_generic.py [-h] [--ticker TICKER] [--company COMPANY] [--prefix PREFIX]

Stock Heat Diffusion Model - Professional Diagram Generator

optional arguments:
  -h, --help            show this help message and exit
  --ticker TICKER, -t TICKER
                        Stock ticker symbol (e.g., AAPL, MSFT, GOOGL) (default: STOCK)
  --company COMPANY, -c COMPANY
                        Company name (e.g., "Apple Inc.", "Microsoft Corp.") (default: None)
  --prefix PREFIX, -p PREFIX
                        Output filename prefix (default: lowercase ticker) (default: None)
```

---

## ✅ Migration from Tesla Version

### Before (Tesla-specific):
```bash
python3 generate_diagrams.py
# Output: tesla_*.png files only
```

### After (Generic):
```bash
# For Tesla
python3 generate_diagrams_generic.py -t TSLA -c "Tesla Inc."
# Output: tsla_*.png files

# For any other company
python3 generate_diagrams_generic.py -t AAPL -c "Apple Inc."
# Output: aapl_*.png files
```

---

## 🏆 Summary

| Feature | Tesla Version | Generic Version |
|---------|--------------|-----------------|
| **Applicability** | Tesla only | **Any stock** ✅ |
| **Command-line args** | None | **Ticker, company, prefix** ✅ |
| **Output filenames** | `tesla_*` | **`{prefix}_*`** ✅ |
| **Diagram count** | 6 diagrams | **10 diagrams** ✅ |
| **Graph visualizations** | None | **4 Neo4j-style graphs** ✅ |
| **Titles in diagrams** | Hardcoded "Tesla" | **Parameterized** ✅ |
| **Equation ticker** | Hardcoded "TSLA" | **Variable ticker** ✅ |
| **Weight constraint** | ✅ Verified | ✅ **Verified** |
| **Quality** | 300 DPI | **300 DPI** ✅ |
| **NetworkX support** | ❌ No | **✅ Yes (knowledge graphs)** |

---

## 📞 Support

For issues or questions:
1. Check this guide for common scenarios
2. Verify matplotlib/seaborn/numpy are installed
3. Ensure Python 3.8+ is being used
4. Check file permissions for output directory

---

**Document Version:** 2.0
**Last Updated:** November 8, 2025
**Status:** ✅ Production Ready for ANY Stock
**New Features:** 🔗 4 Graph Network Visualizations (Neo4j-style)

---

**Recommendation:** Use `generate_diagrams_generic.py` for all new diagrams. Keep `generate_diagrams.py` only for legacy Tesla-specific work.
