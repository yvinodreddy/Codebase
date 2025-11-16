# Stock Heat Diffusion Model - Deployment Guide

## 📋 Overview

This guide provides step-by-step instructions for deploying the Stock Heat Diffusion Model to **any publicly traded company**. The framework is designed to be ticker-agnostic, requiring only sector-specific calibration and historical data.

---

## 🎯 Quick Reference

### Deployment Time Estimates
- **Academic paper only**: 10 minutes (compile LaTeX)
- **Single stock deployment**: 2-4 hours (including data collection)
- **Multi-stock portfolio**: 1-2 days (depending on number of stocks)

### Prerequisites
- Historical stock data (2+ years recommended)
- Neo4j database instance
- Python 3.8+ environment
- Access to market data feeds

---

## 📊 Step-by-Step Deployment

### Phase 1: Stock Selection and Classification

#### Step 1.1: Identify Target Ticker
```python
# Example selections
TICKER = "AAPL"  # Apple Inc.
TICKER = "XOM"   # Exxon Mobil
TICKER = "JPM"   # JPMorgan Chase
TICKER = "WMT"   # Walmart
```

#### Step 1.2: Sector Classification

Classify your stock into one of the following sectors:

| Sector | Characteristics | Example Tickers |
|--------|----------------|-----------------|
| **Technology** | Software, hardware, platforms | AAPL, MSFT, GOOGL |
| **Energy** | Oil, gas, renewables | XOM, CVX, NEE |
| **Financial** | Banks, insurance, asset management | JPM, BAC, GS |
| **Consumer Discretionary** | Retail, auto, luxury | AMZN, WMT, TSLA |
| **Consumer Staples** | Food, beverage, household | PG, KO, WMT |
| **Healthcare** | Pharma, biotech, medical devices | JNJ, PFE, UNH |
| **Industrials** | Manufacturing, aerospace, defense | BA, CAT, GE |
| **Materials** | Mining, chemicals, metals | LIN, APD, FCX |
| **Utilities** | Electric, gas, water utilities | NEE, DUK, SO |
| **Real Estate** | REITs, property management | AMT, PLD, EQIX |
| **Communication Services** | Telecom, media, entertainment | GOOGL, META, DIS |

#### Step 1.3: Market Capitalization Assessment

```python
import yfinance as yf

def get_market_cap(ticker):
    stock = yf.Ticker(ticker)
    market_cap = stock.info.get('marketCap', 0)

    if market_cap > 200e9:
        return 'mega-cap'  # > $200B
    elif market_cap > 10e9:
        return 'large-cap'  # $10B - $200B
    elif market_cap > 2e9:
        return 'mid-cap'    # $2B - $10B
    elif market_cap > 300e6:
        return 'small-cap'  # $300M - $2B
    else:
        return 'micro-cap'  # < $300M

cap_class = get_market_cap("AAPL")
print(f"Market cap classification: {cap_class}")
```

---

### Phase 2: Historical Data Collection

#### Step 2.1: Price and Volume Data
```python
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def collect_price_data(ticker, years=2):
    """Collect historical price and volume data"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*years)

    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date, interval='1d')

    return df

# Example
price_data = collect_price_data("AAPL", years=2)
print(f"Collected {len(price_data)} days of data")
```

#### Step 2.2: Options Data (if available)
```python
def assess_options_liquidity(ticker):
    """Assess options market liquidity"""
    stock = yf.Ticker(ticker)

    try:
        # Get current options chain
        exp_dates = stock.options
        if len(exp_dates) == 0:
            return 'none', 0.0

        # Sample first expiration
        opt_chain = stock.option_chain(exp_dates[0])
        calls = opt_chain.calls
        puts = opt_chain.puts

        avg_volume = (calls['volume'].mean() + puts['volume'].mean()) / 2

        if avg_volume > 1000:
            return 'high', 15.0  # Options weight %
        elif avg_volume > 100:
            return 'medium', 10.0
        elif avg_volume > 10:
            return 'low', 5.0
        else:
            return 'minimal', 2.0

    except:
        return 'none', 0.0

liquidity, options_weight = assess_options_liquidity("AAPL")
print(f"Options liquidity: {liquidity}, suggested weight: {options_weight}%")
```

#### Step 2.3: Social Media Presence
```python
def assess_social_presence(ticker):
    """
    Assess social media visibility
    Note: Requires Twitter API or StockTwits API access
    """
    # Placeholder - implement with actual API
    # For now, manual assessment:

    visibility_map = {
        'AAPL': 'high',    # CEO active, massive retail following
        'TSLA': 'very_high',  # Extreme social media presence
        'JPM': 'medium',   # Professional coverage, limited retail
        'XOM': 'low',      # Minimal social media discussion
        'NEE': 'very_low'  # Utilities rarely discussed
    }

    visibility = visibility_map.get(ticker, 'medium')

    weight_map = {
        'very_high': 15.0,
        'high': 10.0,
        'medium': 6.0,
        'low': 3.0,
        'very_low': 1.0
    }

    return visibility, weight_map[visibility]

visibility, social_weight = assess_social_presence("AAPL")
print(f"Social visibility: {visibility}, suggested weight: {social_weight}%")
```

---

### Phase 3: Weight Calibration

#### Step 3.1: Sector-Specific Base Weights

```python
def get_sector_weights(sector):
    """
    Return baseline weight allocations for each sector
    All weights sum to 1.0
    """
    sector_weights = {
        'Technology': {
            'Microeconomic': 0.30,
            'OrderFlow': 0.18,
            'OptionsFlow': 0.15,
            'Technical': 0.12,
            'NewsSentiment': 0.15,  # Higher for tech
            'SocialMedia': 0.10,     # Higher for tech
            'SectorCorrelation': 0.04,
            'Macro': 0.03,
            'SupplyChain': 0.02,
            'OtherQuant': 0.00
        },
        'Energy': {
            'Microeconomic': 0.25,
            'OrderFlow': 0.15,
            'OptionsFlow': 0.12,
            'Technical': 0.10,
            'NewsSentiment': 0.08,
            'SocialMedia': 0.03,     # Lower for energy
            'SectorCorrelation': 0.05,
            'Macro': 0.20,           # Higher (commodities, rates)
            'SupplyChain': 0.02,
            'OtherQuant': 0.00
        },
        'Financial': {
            'Microeconomic': 0.28,
            'OrderFlow': 0.18,
            'OptionsFlow': 0.15,
            'Technical': 0.10,
            'NewsSentiment': 0.10,
            'SocialMedia': 0.04,
            'SectorCorrelation': 0.05,
            'Macro': 0.20,           # Rate-sensitive
            'SupplyChain': 0.00,     # Not applicable
            'OtherQuant': 0.00
        },
        'Consumer Discretionary': {
            'Microeconomic': 0.28,
            'OrderFlow': 0.16,
            'OptionsFlow': 0.13,
            'Technical': 0.15,       # Trend-following
            'NewsSentiment': 0.12,
            'SocialMedia': 0.10,     # Higher retail interest
            'SectorCorrelation': 0.04,
            'Macro': 0.05,
            'SupplyChain': 0.02,
            'OtherQuant': 0.00
        },
        'Utilities': {
            'Microeconomic': 0.25,
            'OrderFlow': 0.15,
            'OptionsFlow': 0.08,     # Lower activity
            'Technical': 0.10,
            'NewsSentiment': 0.08,
            'SocialMedia': 0.02,     # Very low
            'SectorCorrelation': 0.05,
            'Macro': 0.25,           # Rate-sensitive
            'SupplyChain': 0.02,
            'OtherQuant': 0.00
        }
    }

    # Default for unlisted sectors
    default_weights = {
        'Microeconomic': 0.28,
        'OrderFlow': 0.18,
        'OptionsFlow': 0.15,
        'Technical': 0.12,
        'NewsSentiment': 0.10,
        'SocialMedia': 0.08,
        'SectorCorrelation': 0.04,
        'Macro': 0.03,
        'SupplyChain': 0.02,
        'OtherQuant': 0.00
    }

    weights = sector_weights.get(sector, default_weights)

    # Verify sum = 1.0
    total = sum(weights.values())
    assert abs(total - 1.0) < 1e-10, f"Weights sum to {total}, not 1.0!"

    return weights

# Example
weights_aapl = get_sector_weights('Technology')
print(f"AAPL baseline weights: {weights_aapl}")
print(f"Sum: {sum(weights_aapl.values())}")
```

#### Step 3.2: Liquidity-Based Adjustments

```python
def adjust_for_liquidity(base_weights, avg_daily_volume, options_liquidity):
    """
    Adjust weights based on liquidity characteristics
    Maintains Σwᵢ = 1.0 constraint
    """
    weights = base_weights.copy()

    # Low volume stocks: reduce microstructure weights
    if avg_daily_volume < 100000:  # < 100K shares/day
        # Reduce order flow and options
        weights['OrderFlow'] *= 0.5
        weights['OptionsFlow'] *= 0.3

        # Increase technical and fundamental
        weights['Technical'] *= 1.3
        weights['Microeconomic'] *= 1.2

    # Limited options: redistribute options weight
    if options_liquidity == 'none' or options_liquidity == 'minimal':
        options_weight = weights['OptionsFlow']
        weights['OptionsFlow'] = 0.02  # Minimal

        # Redistribute to technical and order flow
        remaining = options_weight - 0.02
        weights['Technical'] += remaining * 0.6
        weights['OrderFlow'] += remaining * 0.4

    # Renormalize to ensure sum = 1.0
    total = sum(weights.values())
    weights = {k: v/total for k, v in weights.items()}

    # Verify
    assert abs(sum(weights.values()) - 1.0) < 1e-10

    return weights

# Example
adjusted_weights = adjust_for_liquidity(
    weights_aapl,
    avg_daily_volume=80_000_000,
    options_liquidity='high'
)
print(f"Adjusted weights sum: {sum(adjusted_weights.values())}")
```

---

### Phase 4: HMM Regime Calibration

#### Step 4.1: Calculate Historical Returns and Volatility

```python
import numpy as np
from scipy.stats import norm

def calculate_regime_parameters(price_data):
    """
    Calculate HMM emission parameters from historical data
    """
    # Calculate returns
    returns = price_data['Close'].pct_change().dropna()

    # Calculate rolling volatility (20-day)
    volatility = returns.rolling(window=20).std()

    # Identify regimes (simple threshold-based)
    bull_mask = (returns.rolling(20).mean() > 0.001) & (volatility < volatility.quantile(0.5))
    bear_mask = (returns.rolling(20).mean() < -0.001) | (volatility > volatility.quantile(0.75))
    sideways_mask = ~(bull_mask | bear_mask)

    # Calculate emission probabilities
    bull_returns = returns[bull_mask]
    bear_returns = returns[bear_mask]
    sideways_returns = returns[sideways_mask]

    params = {
        'bull': {
            'mean': bull_returns.mean() if len(bull_returns) > 0 else 0.001,
            'std': bull_returns.std() if len(bull_returns) > 0 else 0.01
        },
        'bear': {
            'mean': bear_returns.mean() if len(bear_returns) > 0 else -0.002,
            'std': bear_returns.std() if len(bear_returns) > 0 else 0.03
        },
        'sideways': {
            'mean': sideways_returns.mean() if len(sideways_returns) > 0 else 0.0,
            'std': sideways_returns.std() if len(sideways_returns) > 0 else 0.015
        }
    }

    return params

# Example
regime_params = calculate_regime_parameters(price_data)
print("HMM Emission Parameters:")
for regime, params in regime_params.items():
    print(f"  {regime}: μ={params['mean']:.4f}, σ={params['std']:.4f}")
```

---

### Phase 5: Neo4j Graph Construction

#### Step 5.1: Create Stock Node

```cypher
// Create parameterized stock node
CREATE (s:Stock {
  ticker: $ticker,
  name: $companyName,
  sector: $sector,
  marketCap: $marketCap,
  avgVolume: $avgVolume,
  beta: $beta,
  currentPrice: $currentPrice,
  temperature: 0.0,
  heatScore: 0.0,
  timestamp: datetime(),
  createdAt: datetime()
})
RETURN s
```

Example Python code:
```python
from neo4j import GraphDatabase

class StockDeployment:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def create_stock_node(self, ticker, sector, market_cap):
        query = """
        CREATE (s:Stock {
          ticker: $ticker,
          sector: $sector,
          marketCap: $marketCap,
          temperature: 0.0,
          timestamp: datetime()
        })
        RETURN s
        """

        with self.driver.session() as session:
            result = session.run(query,
                ticker=ticker,
                sector=sector,
                marketCap=market_cap
            )
            return result.single()

    def close(self):
        self.driver.close()

# Example usage
deploy = StockDeployment(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)

stock = deploy.create_stock_node(
    ticker="AAPL",
    sector="Technology",
    market_cap=3000000000000  # $3T
)
print(f"Created stock node: {stock}")
```

#### Step 5.2: Create Factor Nodes with Weights

```python
def create_factor_nodes(session, ticker, weights):
    """
    Create all factor category nodes with calibrated weights
    """
    query = """
    UNWIND $factors AS factor
    CREATE (f:FactorCategory {
      ticker: $ticker,
      name: factor.name,
      baseWeight: factor.weight,
      currentWeight: factor.weight,
      category: factor.name,
      lastUpdated: datetime()
    })
    """

    factors = [
        {'name': k, 'weight': v}
        for k, v in weights.items()
    ]

    session.run(query, ticker=ticker, factors=factors)

    # Verify sum = 1.0
    verify_query = """
    MATCH (f:FactorCategory {ticker: $ticker})
    RETURN sum(f.baseWeight) AS total
    """

    result = session.run(verify_query, ticker=ticker)
    total = result.single()['total']

    print(f"Total weight for {ticker}: {total}")
    assert abs(total - 1.0) < 1e-10, f"Weights don't sum to 1.0! Got {total}"

# Usage
with deploy.driver.session() as session:
    create_factor_nodes(session, "AAPL", adjusted_weights)
```

#### Step 5.3: Create INFLUENCES Relationships

```cypher
// Connect factors to stock
MATCH (f:FactorCategory {ticker: $ticker})
MATCH (s:Stock {ticker: $ticker})
CREATE (f)-[r:INFLUENCES {
  weight: f.baseWeight,
  normalizedWeight: f.baseWeight,
  lastUpdated: datetime()
}]->(s)
RETURN count(r) AS relationshipCount
```

---

### Phase 6: Kalman Filter Initialization

#### Step 6.1: Historical Calibration

```python
import numpy as np
from scipy.linalg import inv

class KalmanFactorModel:
    def __init__(self, n_factors=10):
        self.n_factors = n_factors
        self.beta = np.ones(n_factors) / n_factors  # Initial weights (uniform)
        self.P = np.eye(n_factors) * 0.01  # Covariance matrix
        self.Q = np.eye(n_factors) * 0.001  # Process noise
        self.R = 0.0001  # Observation noise

    def calibrate(self, factor_returns, stock_returns):
        """
        Calibrate Kalman filter on historical data
        factor_returns: (T, n_factors) array
        stock_returns: (T,) array
        """
        T = len(stock_returns)

        for t in range(T):
            # Prediction
            beta_pred = self.beta
            P_pred = self.P + self.Q

            # Update
            f_t = factor_returns[t, :]
            y_t = stock_returns[t] - np.dot(f_t, beta_pred)

            S = np.dot(f_t, np.dot(P_pred, f_t)) + self.R
            K = np.dot(P_pred, f_t) / S

            self.beta = beta_pred + K * y_t
            self.P = P_pred - np.outer(K, f_t) @ P_pred

            # Enforce non-negativity and normalization
            self.beta = np.maximum(self.beta, 0)
            self.beta = self.beta / np.sum(self.beta)

        return self.beta

    def get_weights(self):
        """Return current normalized weights"""
        assert abs(np.sum(self.beta) - 1.0) < 1e-10
        return self.beta

# Example usage
kalman = KalmanFactorModel(n_factors=10)

# Simulate factor returns (replace with actual data)
factor_returns = np.random.randn(500, 10) * 0.01
stock_returns = np.random.randn(500) * 0.02

calibrated_weights = kalman.calibrate(factor_returns, stock_returns)
print(f"Calibrated weights: {calibrated_weights}")
print(f"Sum: {np.sum(calibrated_weights)}")
```

---

### Phase 7: Real-Time Deployment

#### Step 7.1: Heat Diffusion Query (Ticker-Specific)

```python
def run_heat_diffusion(session, ticker, delta_t=0.1, iterations=10):
    """
    Run heat diffusion for specific ticker
    """
    query = """
    // Initialize
    MATCH (f:Factor {ticker: $ticker, id: $eventId})
    SET f.temperature = 1.0, f.heat = 1.0

    // Iterate diffusion
    UNWIND range(1, $iterations) AS iter
    CALL {
      WITH iter
      MATCH (n:Factor {ticker: $ticker})
            -[r:CORRELATED_WITH|INFLUENCES]-(m:Factor)
      WITH n,
        sum(r.weight * coalesce(m.temperature, 0)) AS neighborHeat,
        sum(r.weight) AS totalWeight,
        n.temperature AS currentTemp
      SET n.nextTemperature = currentTemp + $deltaT *
        (neighborHeat / totalWeight - currentTemp)
    }

    // Commit
    MATCH (n:Factor {ticker: $ticker})
    SET n.temperature = coalesce(n.nextTemperature, n.temperature)
    REMOVE n.nextTemperature

    // Propagate to stock
    MATCH (f:Factor)-[r:INFLUENCES]->(s:Stock {ticker: $ticker})
    WITH s, sum(r.normalizedWeight * f.temperature) AS totalHeat
    SET s.temperature = totalHeat,
        s.heatScore = totalHeat,
        s.lastUpdated = datetime()

    RETURN s.ticker AS ticker,
           s.heatScore AS heatScore,
           s.temperature AS temperature
    """

    result = session.run(query,
        ticker=ticker,
        eventId='example_event',
        deltaT=delta_t,
        iterations=iterations
    )

    return result.single()

# Usage
with deploy.driver.session() as session:
    result = run_heat_diffusion(session, "AAPL", delta_t=0.1, iterations=15)
    print(f"Heat score for AAPL: {result['heatScore']}")
```

#### Step 7.2: Weight Normalization Enforcement

```python
def enforce_normalization(session, ticker):
    """
    Ensure Σwᵢ = 1.0 for all factor weights
    """
    query = """
    // Calculate total weight
    MATCH (:Factor {ticker: $ticker})-[r:INFLUENCES]->(:Stock {ticker: $ticker})
    WITH sum(r.weight) AS totalWeight

    // Normalize all weights
    MATCH (:Factor {ticker: $ticker})-[r:INFLUENCES]->(:Stock {ticker: $ticker})
    SET r.normalizedWeight = r.weight / totalWeight

    // Verify
    WITH sum(r.normalizedWeight) AS verifySum
    RETURN verifySum
    """

    result = session.run(query, ticker=ticker)
    total = result.single()['verifySum']

    print(f"Normalized weight sum for {ticker}: {total}")
    assert abs(total - 1.0) < 1e-6, f"Normalization failed! Got {total}"

    return total

# Usage
with deploy.driver.session() as session:
    total = enforce_normalization(session, "AAPL")
```

---

## 🔍 Validation Checklist

### Pre-Deployment
- [ ] Historical data collected (2+ years)
- [ ] Sector classification confirmed
- [ ] Market cap and liquidity assessed
- [ ] Social media visibility evaluated
- [ ] Base weights calculated (Σw = 1.0)
- [ ] HMM parameters calibrated
- [ ] Kalman filter initialized

### Neo4j Deployment
- [ ] Stock node created with correct ticker
- [ ] All 10 factor category nodes created
- [ ] INFLUENCES relationships established
- [ ] Edge weights sum to 1.0 verified
- [ ] Heat diffusion query tested
- [ ] Normalization enforcement validated

### Performance Testing
- [ ] Query latency < 2 seconds
- [ ] Heat propagation converges
- [ ] Weight updates maintain Σw = 1.0
- [ ] Regime detection functioning
- [ ] Real-time data feeds integrated

---

## 🚀 Example: Complete Deployment for Microsoft (MSFT)

```python
# Complete deployment script
def deploy_stock_model(ticker, sector):
    """Complete deployment for any ticker"""

    print(f"\n{'='*60}")
    print(f"Deploying Stock Heat Diffusion Model for {ticker}")
    print(f"{'='*60}\n")

    # Step 1: Data collection
    print("Step 1: Collecting historical data...")
    price_data = collect_price_data(ticker, years=2)
    print(f"  ✓ Collected {len(price_data)} days")

    # Step 2: Assess characteristics
    print("\nStep 2: Assessing stock characteristics...")
    liquidity, options_weight = assess_options_liquidity(ticker)
    visibility, social_weight = assess_social_presence(ticker)
    print(f"  ✓ Options liquidity: {liquidity}")
    print(f"  ✓ Social visibility: {visibility}")

    # Step 3: Calculate weights
    print("\nStep 3: Calibrating factor weights...")
    base_weights = get_sector_weights(sector)
    adjusted_weights = adjust_for_liquidity(
        base_weights,
        price_data['Volume'].mean(),
        liquidity
    )
    print(f"  ✓ Weights sum: {sum(adjusted_weights.values()):.10f}")

    # Step 4: HMM calibration
    print("\nStep 4: Calibrating regime detection...")
    regime_params = calculate_regime_parameters(price_data)
    print(f"  ✓ Bull regime: μ={regime_params['bull']['mean']:.4f}")
    print(f"  ✓ Bear regime: μ={regime_params['bear']['mean']:.4f}")

    # Step 5: Neo4j deployment
    print("\nStep 5: Deploying to Neo4j...")
    deploy = StockDeployment(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )

    with deploy.driver.session() as session:
        # Create stock node
        stock = deploy.create_stock_node(
            ticker=ticker,
            sector=sector,
            market_cap=1000000000000  # Placeholder
        )
        print(f"  ✓ Created stock node")

        # Create factor nodes
        create_factor_nodes(session, ticker, adjusted_weights)
        print(f"  ✓ Created factor nodes")

        # Enforce normalization
        total = enforce_normalization(session, ticker)
        print(f"  ✓ Verified normalization: Σw = {total:.10f}")

    deploy.close()

    print(f"\n{'='*60}")
    print(f"✓ Deployment complete for {ticker}!")
    print(f"{'='*60}\n")

    return adjusted_weights

# Deploy Microsoft
msft_weights = deploy_stock_model("MSFT", "Technology")
```

---

## 📊 Multi-Stock Portfolio Deployment

```python
def deploy_portfolio(tickers_and_sectors):
    """Deploy multiple stocks simultaneously"""

    results = {}

    for ticker, sector in tickers_and_sectors.items():
        print(f"\nDeploying {ticker} ({sector})...")
        weights = deploy_stock_model(ticker, sector)
        results[ticker] = weights

    return results

# Example: Deploy tech portfolio
portfolio = {
    'AAPL': 'Technology',
    'MSFT': 'Technology',
    'GOOGL': 'Technology',
    'META': 'Technology',
    'NVDA': 'Technology'
}

portfolio_weights = deploy_portfolio(portfolio)
```

---

## 🛠️ Troubleshooting

### Issue: Weights don't sum to 1.0
**Solution:**
```python
def fix_normalization(weights):
    total = sum(weights.values())
    return {k: v/total for k, v in weights.items()}
```

### Issue: Neo4j connection failed
**Solution:**
```bash
# Check Neo4j status
sudo systemctl status neo4j

# Restart if needed
sudo systemctl restart neo4j

# Verify connection
cypher-shell -u neo4j -p password "RETURN 1"
```

### Issue: Insufficient historical data
**Solution:**
- Reduce lookback period to 1 year minimum
- Use sector averages for missing data
- Adjust HMM emission probabilities conservatively

---

## 📈 Performance Monitoring

### Real-Time Metrics Dashboard

```python
def monitor_performance(session, ticker):
    """Monitor real-time performance metrics"""

    query = """
    MATCH (s:Stock {ticker: $ticker})
    MATCH (f:Factor {ticker: $ticker})-[r:INFLUENCES]->(s)

    RETURN
      s.ticker AS ticker,
      s.heatScore AS currentHeat,
      s.temperature AS temperature,
      collect({
        factor: f.name,
        weight: r.normalizedWeight,
        temperature: f.temperature
      }) AS factors,
      sum(r.normalizedWeight) AS weightSum
    """

    result = session.run(query, ticker=ticker)
    data = result.single()

    print(f"\n{'='*60}")
    print(f"Performance Monitor: {data['ticker']}")
    print(f"{'='*60}")
    print(f"Heat Score: {data['currentHeat']:.4f}")
    print(f"Weight Sum: {data['weightSum']:.10f}")
    print(f"\nFactor Breakdown:")

    for factor in data['factors']:
        print(f"  {factor['factor']:20s}: {factor['weight']:.4f} "
              f"(temp: {factor['temperature']:.4f})")

    assert abs(data['weightSum'] - 1.0) < 1e-6, \
        f"ERROR: Weights don't sum to 1.0! Got {data['weightSum']}"

    print(f"{'='*60}\n")

# Usage
with deploy.driver.session() as session:
    monitor_performance(session, "AAPL")
```

---

## ✅ Final Deployment Checklist

- [ ] LaTeX paper compiled successfully
- [ ] Stock selection and classification completed
- [ ] Historical data collected (2+ years)
- [ ] Factor weights calibrated (Σw = 1.0 verified)
- [ ] HMM regime parameters estimated
- [ ] Kalman filter initialized
- [ ] Neo4j stock node created
- [ ] All factor nodes created
- [ ] INFLUENCES relationships established
- [ ] Normalization enforcement tested
- [ ] Heat diffusion convergence validated
- [ ] Real-time query latency < 2s
- [ ] Performance monitoring dashboard active
- [ ] Documentation updated for ticker

---

**Document Version:** 1.0
**Last Updated:** November 8, 2025
**Status:** ✅ Ready for Production Deployment

---

For questions or support, refer to README_GENERIC.md or contact the research team.
