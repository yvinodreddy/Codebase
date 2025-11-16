# LaTeX Integration Guide for Generated Images

## Overview

This guide explains how to integrate the 6 world-class Neo4j-style visualizations into your academic paper LaTeX files.

All images are:
- ✅ 300 DPI resolution (publication quality)
- ✅ Professional Neo4j graph database aesthetics
- ✅ Rounded corners, no text cutoff
- ✅ Complete legends and self-explanatory
- ✅ Ready for IEEE, ACM, Springer, Elsevier submissions

---

## Generated Images

### Image 1: System Architecture Overview
**File:** `image1_system_architecture.png` (566KB, 16x10 @ 300 DPI)

**Description:** Complete end-to-end system flow showing:
- Data ingestion from multiple sources (market data, news, social media, options)
- Preprocessing and graph construction
- Heat diffusion engine with Graph Laplacian
- Dynamic weight optimization (HMM + Kalman)
- Trading recommendation output
- All core components and performance metrics

**Suggested Placement:** Section 1 (Introduction) or Section 2 (System Overview)

**LaTeX Code:**
```latex
\begin{figure}[!t]
\centering
\includegraphics[width=0.95\textwidth]{image1_system_architecture.png}
\caption{Stock Heat Diffusion Model System Architecture. The framework processes multi-source data through graph construction, applies heat diffusion equations, optimizes factor weights dynamically using HMM regime detection and Kalman filtering, and generates explainable trading recommendations with 99\%+ confidence. Performance metrics show Sharpe ratio of 0.63, Information ratio of 0.43, and 58.3\% directional accuracy with sub-1.65 second latency.}
\label{fig:system_architecture}
\end{figure}
```

---

### Image 2: 10-Factor Category Graph
**File:** `image2_factor_graph.png` (820KB, 14x14 @ 300 DPI)

**Description:** Neo4j-style circular graph showing:
- Central stock node (red)
- 10 factor categories arranged in circle (purple nodes)
- Weight percentages for each category (baseline risk parity allocation)
- Normalization constraint: ∑wᵢ(t) = 1.0
- Heat equation at top
- Clear labels with weight ranges

**Suggested Placement:** Section 3 (Factor Taxonomy) or Section 4 (Model Architecture)

**LaTeX Code:**
```latex
\begin{figure}[!t]
\centering
\includegraphics[width=0.85\textwidth]{image2_factor_graph.png}
\caption{Ten-Factor Category Knowledge Graph with Baseline Weight Allocation. The central stock node (red) connects to ten factor categories (purple): Macroeconomic (12\%), Microeconomic (28\%), News Sentiment (10\%), Social Media (8\%), Order Flow (18\%), Options Flow (15\%), Technical Indicators (12\%), Sector Correlations (4\%), Supply Chain (2\%), and Other Quantitative (1\%). Weights represent risk parity baseline and sum to 1.0 at all times. Heat equation shown at top: heat\_stock(t) = ∑wᵢ(t)·factorᵢ(t) + diffusion\_term(t).}
\label{fig:factor_graph}
\end{figure}
```

---

### Image 3: Heat Diffusion Process Over Time
**File:** `image3_heat_diffusion.png` (682KB, 14x12 @ 300 DPI)

**Description:** Four-panel time-series visualization (t=0, t=1, t=2, t=3) showing:
- Initial heat source at event node
- Heat propagating through news and social media nodes
- Heat reaching stock node
- Final diffusion to options and technical factors
- Color-coded heat intensity (red=hot, orange=warm, yellow=mild, gray=cold)
- Temporal decay equation shown

**Suggested Placement:** Section 2 (Heat Diffusion on Financial Graphs) or Section 5 (Implementation)

**LaTeX Code:**
```latex
\begin{figure}[!t]
\centering
\includegraphics[width=0.9\textwidth]{image3_heat_diffusion.png}
\caption{Heat Diffusion Process Over Time (t=0 to t=3). An initial event creates heat (h=1.0) at source node which propagates through the knowledge graph according to the diffusion equation ∂h/∂t = -βL·h(t). Heat intensity shown by color: red (h > 0.6), orange (0.3 < h ≤ 0.6), yellow (0 < h ≤ 0.3), gray (h=0). Temporal decay follows exp(-γt) with γ=0.5 for high-frequency news events. By t=3, heat has diffused from the event through news/social media to the stock node (h=0.73) and onwards to options and technical factors.}
\label{fig:heat_diffusion}
\end{figure}
```

---

### Image 4: Regime Detection & Dynamic Weight Adjustment
**File:** `image4_regime_detection.png` (541KB, 14x10 @ 300 DPI)

**Description:** HMM state machine visualization showing:
- Three market regimes: Bull, Sideways, Bear (circular nodes with parameters)
- Transition probabilities between states (arrows with values)
- Self-loop probabilities for state persistence
- Weight adjustment table showing multipliers by regime
- Normalization constraint reminder at bottom

**Suggested Placement:** Section 4 (Dynamic Weight Adjustment Algorithms)

**LaTeX Code:**
```latex
\begin{figure}[!t]
\centering
\includegraphics[width=0.9\textwidth]{image4_regime_detection.png}
\caption{Hidden Markov Model for Regime Detection and Dynamic Weight Adjustment. Three-state HMM identifies Bull (μ=+0.046\%, σ=0.94\%), Sideways (μ=+0.04\%, σ=3.47\%), and Bear (μ=-0.066\%, σ=13.63\%) market regimes. Transition probabilities shown on edges (e.g., Bull→Bull: 0.85, Bull→Sideways: 0.10). Weight adjustment table displays factor-specific multipliers: Bull markets emphasize microeconomic (1.3×) and technical momentum (1.5×), while Bear markets increase options flow (1.7×) and order flow (1.4×). After adjustment, weights are normalized to ensure ∑wᵢ = 1.0.}
\label{fig:regime_detection}
\end{figure}
```

---

### Image 5: Detailed Knowledge Graph (Neo4j Implementation)
**File:** `image5_knowledge_graph.png` (845KB, 16x14 @ 300 DPI)

**Description:** Comprehensive Neo4j-style graph showing:
- Central stock node with properties (ticker, price, temperature)
- Inner ring: 6 factor categories (Macro, Micro, News, Social, Order, Options)
- Outer ring: 12 individual factors with current values
- Color coding: Active factors (orange), regular factors (gray)
- Neo4j properties panel (bottom left) showing node attributes
- Cypher query example (bottom right) for graph traversal
- Professional graph database aesthetic

**Suggested Placement:** Section 5 (Neo4j Implementation Architecture)

**LaTeX Code:**
```latex
\begin{figure*}[!t]
\centering
\includegraphics[width=0.95\textwidth]{image5_knowledge_graph.png}
\caption{Neo4j Knowledge Graph Implementation with Detailed Node Structure. Central stock node (red, ticker=TSLA, temp=0.73, price=\$242.50) connects to six factor category nodes (purple): Macro, Micro, News, Social, Order, Options. Each category links to individual factor nodes (outer ring) showing current values: Fed Rate (5.25\%), Earnings Beat (+2.3\%), News Sentiment (+0.68), Twitter Volume (12.5K), Buy Imbalance (+15.3\%), Put/Call ratio (0.75), etc. Active factors with high influence shown in orange. Bottom panels display Neo4j node properties (left) and example Cypher query (right) for retrieving factors with temperature > 0.5. This structure enables efficient graph traversal, heat diffusion computation, and multi-hop influence modeling.}
\label{fig:knowledge_graph}
\end{figure*}
```

**Note:** Use `figure*` environment for two-column IEEE format to span full page width.

---

### Image 6: Kalman Filter Workflow
**File:** `image6_kalman_filter.png` (400KB, 14x10 @ 300 DPI)

**Description:** State-space model flowchart showing:
- Prediction step (blue): β̂ₜ|ₜ₋₁ = β̂ₜ₋₁|ₜ₋₁, Pₜ|ₜ₋₁ = Pₜ₋₁|ₜ₋₁ + Q
- Update step (orange): β̂ₜ|ₜ = β̂ₜ|ₜ₋₁ + Kₜyₜ
- Kalman gain computation (yellow)
- Innovation calculation (purple)
- Normalization step (green) ensuring ∑βᵢ = 1
- Feedback loop for iterative refinement
- Calibration parameters table
- Performance improvement metrics

**Suggested Placement:** Section 4 (Dynamic Weight Adjustment Algorithms - Kalman Filtering subsection)

**LaTeX Code:**
```latex
\begin{figure}[!t]
\centering
\includegraphics[width=0.9\textwidth]{image6_kalman_filter.png}
\caption{Kalman Filter State-Space Model for Continuous Weight Updates. The filter operates in two phases: (1) Prediction step (blue) propagates previous state estimate β̂ₜ₋₁|ₜ₋₁ forward with process noise Q, (2) Update step (orange) incorporates new observations via Kalman gain Kₜ and innovation yₜ = rₜ - fₜᵀβ̂ₜ|ₜ₋₁. After update, weights are normalized (green) to satisfy non-negativity (βᵢ ≥ 0) and sum-to-one constraint (∑βᵢ = 1). Process noise calibrated as q=0.001 (daily) and q=0.01 (hourly). The iterative refinement improves Sharpe ratio from 0.52 to 0.63 (+21\%) with convergence in 10-20 periods.}
\label{fig:kalman_filter}
\end{figure}
```

---

## Integration Checklist

### 1. Copy Images to LaTeX Project Directory
```bash
cp image*.png /path/to/your/latex/project/
```

### 2. Verify Images in LaTeX Preamble
Ensure you have the `graphicx` package:
```latex
\usepackage{graphicx}
```

### 3. Optional: Convert to EPS for Some Publishers
If your publisher requires EPS format:
```bash
for file in image*.png; do
    convert "$file" "${file%.png}.eps"
done
```

### 4. Reference Figures in Text
Use `\ref{fig:label}` to reference figures:
```latex
As shown in Figure~\ref{fig:system_architecture}, the heat diffusion model...
The factor weights (Figure~\ref{fig:factor_graph}) are dynamically adjusted...
```

### 5. Check Image Quality in PDF
After compiling:
```bash
pdflatex your_paper.tex
# Open PDF and zoom to 200-300% to verify crisp rendering
```

---

## Recommended Figure Placement

### For `tesla_heat_diffusion_model.tex`:
- Figure 1 (System Architecture) → After Section 1 (Introduction), line 57
- Figure 2 (Factor Graph) → Section 3 (Factor Taxonomy), line 129
- Figure 3 (Heat Diffusion) → Section 2.3 (Temporal Decay), line 126
- Figure 4 (Regime Detection) → Section 4.1 (Regime Detection via HMM), line 456
- Figure 5 (Knowledge Graph) → Section 5.1 (Graph Structure), line 552
- Figure 6 (Kalman Filter) → Section 4.2 (Kalman Filtering), line 477

### For `stock_heat_diffusion_model.tex`:
Same placement strategy applies (generic version has same section structure).

---

## Advanced: Creating Additional Variants

If you need variations (e.g., different color schemes, smaller sizes):

### Adjust DPI for Different Use Cases
```python
# In generate_images.py, modify:
plt.rcParams['figure.dpi'] = 150  # For presentations
plt.rcParams['figure.dpi'] = 300  # For journal submission (current)
plt.rcParams['figure.dpi'] = 600  # For high-end print
```

### Change Color Scheme
```python
# Modify COLORS dictionary for grayscale:
COLORS = {
    'stock_node': '#2C3E50',
    'factor_category': '#7F8C8D',
    'factor_individual': '#BDC3C7',
    # ... etc
}
```

---

## Troubleshooting

### Issue: Images appear blurry in PDF
**Solution:** Images are 300 DPI. If blurry:
1. Check LaTeX scaling: Use `width=0.9\textwidth` instead of absolute sizes
2. Verify PDF viewer zoom is 100%+
3. Regenerate at 600 DPI if needed for ultra-high-end journals

### Issue: File size too large for submission
**Solution:** Compress without quality loss:
```bash
pngquant --quality=85-95 image*.png
```

### Issue: Text too small in figure
**Solution:** In `generate_images.py`, increase `fontsize` parameters:
```python
plt.rcParams['font.size'] = 12  # Instead of 10
```

---

## Color Palette Reference

For consistency when creating additional figures:

| Element | Color | Hex Code |
|---------|-------|----------|
| Stock Node (Central) | Red | #E74C3C |
| Factor Category | Purple | #9B59B6 |
| Individual Factor | Gray | #95A5A6 |
| Active/Hot Factor | Orange | #F39C12 |
| Edges | Dark Blue-Gray | #34495E |
| Active Edges | Orange | #E67E22 |
| Highlights | Blue | #3498DB |
| Success/Positive | Green | #27AE60 |
| Warning | Orange | #F39C12 |
| Text | Dark Gray | #2C3E50 |

---

## Contact & Support

If you need to regenerate images or create additional visualizations:

```bash
cd "/home/user01/claude-test/Paper Submission/RAGHeat"
python3 generate_images.py
```

All images are self-contained and production-ready. No additional post-processing required!

**Created:** 2025-11-09
**Generator:** Python matplotlib with Neo4j-style professional aesthetics
**Quality:** 300 DPI, publication-ready for all major academic publishers
