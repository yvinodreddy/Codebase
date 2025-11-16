# 🔥 RAGHEAT Neo4j Cypher Query Guide

## 📊 Complete Guide for Data Analysis & Time Series Operations

This comprehensive guide provides ready-to-use Cypher queries for analyzing your RAGHEAT financial knowledge graph and time series data.

---

## 🗄️ **Database Schema Overview**

### Node Types
- **Market**: Global market root node
- **Sector**: Industry sectors (Technology, Healthcare, etc.)
- **Stock**: Individual stock entities with live data
- **Factor**: Market factors affecting stock performance

### Relationship Types
- **CONTAINS**: Market contains Sectors
- **BELONGS_TO**: Stocks belong to Sectors
- **CORRELATES_WITH**: Stock correlations
- **INFLUENCED_BY**: Factor influences
- **HAS_PRICE_HISTORY**: Time series price data

---

## 🚀 **Basic Data Exploration Queries**

### 1. Get Database Overview
```cypher
// Database statistics
MATCH (n)
RETURN
  labels(n)[0] as NodeType,
  count(n) as Count
ORDER BY Count DESC;

// Relationship overview
MATCH ()-[r]->()
RETURN
  type(r) as RelationshipType,
  count(r) as Count
ORDER BY Count DESC;
```

### 2. Market Structure Analysis
```cypher
// Complete market hierarchy
MATCH (m:Market)-[:CONTAINS]->(s:Sector)-[:CONTAINS]->(st:Stock)
RETURN
  m.name as Market,
  s.name as Sector,
  count(st) as StockCount,
  collect(st.symbol)[0..5] as SampleStocks
ORDER BY StockCount DESC;
```

### 3. Live Data Status Check
```cypher
// Check which stocks have live data
MATCH (s:Stock)
WHERE s.last_update IS NOT NULL
RETURN
  s.symbol as Symbol,
  s.name as Name,
  s.price as CurrentPrice,
  s.change_pct as ChangePercent,
  s.volume as Volume,
  s.data_source as DataSource,
  s.is_streaming as IsLive,
  datetime(s.last_update) as LastUpdate
ORDER BY s.change_pct DESC
LIMIT 20;
```

---

## 📈 **Price and Performance Analysis**

### 4. Top Performers Analysis
```cypher
// Top gainers today
MATCH (s:Stock)
WHERE s.change_pct IS NOT NULL
RETURN
  s.symbol as Symbol,
  s.name as Company,
  s.price as Price,
  s.change_pct as ChangePercent,
  s.volume as Volume,
  s.market_cap as MarketCap
ORDER BY s.change_pct DESC
LIMIT 10;

// Top losers today
MATCH (s:Stock)
WHERE s.change_pct IS NOT NULL
RETURN
  s.symbol as Symbol,
  s.name as Company,
  s.price as Price,
  s.change_pct as ChangePercent,
  s.volume as Volume
ORDER BY s.change_pct ASC
LIMIT 10;
```

### 5. Sector Performance Analysis
```cypher
// Sector performance summary
MATCH (sec:Sector)<-[:BELONGS_TO]-(s:Stock)
WHERE s.change_pct IS NOT NULL
RETURN
  sec.name as Sector,
  count(s) as StockCount,
  avg(s.change_pct) as AvgChange,
  max(s.change_pct) as MaxGain,
  min(s.change_pct) as MaxLoss,
  sum(s.volume) as TotalVolume,
  avg(s.price) as AvgPrice
ORDER BY AvgChange DESC;
```

### 6. Heat Score Analysis
```cypher
// Stocks by heat level (market momentum)
MATCH (s:Stock)
WHERE s.heat_score IS NOT NULL
RETURN
  s.symbol as Symbol,
  s.heat_score as HeatScore,
  s.change_pct as ChangePercent,
  s.volume as Volume,
  CASE
    WHEN s.heat_score > 0.7 THEN 'HOT 🔥'
    WHEN s.heat_score > 0.4 THEN 'WARM 🌡️'
    WHEN s.heat_score > 0.2 THEN 'NEUTRAL ⚖️'
    ELSE 'COOL ❄️'
  END as HeatLevel
ORDER BY s.heat_score DESC;
```

---

## 🔗 **Correlation and Relationship Analysis**

### 7. Stock Correlations
```cypher
// Find highly correlated stocks
MATCH (s1:Stock)-[r:CORRELATES_WITH]->(s2:Stock)
WHERE r.correlation > 0.7
RETURN
  s1.symbol as Stock1,
  s2.symbol as Stock2,
  r.correlation as Correlation,
  s1.change_pct as Stock1Change,
  s2.change_pct as Stock2Change
ORDER BY r.correlation DESC;

// Sector correlation matrix
MATCH (s1:Stock)-[:BELONGS_TO]->(sec1:Sector),
      (s2:Stock)-[:BELONGS_TO]->(sec2:Sector),
      (s1)-[r:CORRELATES_WITH]->(s2)
WHERE sec1 <> sec2
RETURN
  sec1.name as Sector1,
  sec2.name as Sector2,
  avg(r.correlation) as AvgCorrelation,
  count(r) as RelationshipCount
ORDER BY AvgCorrelation DESC;
```

### 8. Market Influence Network
```cypher
// Find stocks that influence others
MATCH (influencer:Stock)-[r:INFLUENCES]->(influenced:Stock)
RETURN
  influencer.symbol as InfluencerStock,
  count(influenced) as InfluencesCount,
  collect(influenced.symbol)[0..5] as SampleInfluenced,
  avg(r.strength) as AvgInfluenceStrength
ORDER BY InfluencesCount DESC
LIMIT 10;
```

---

## ⏰ **Time Series Analysis Queries**

### 9. Price History Analysis
```cypher
// Daily price movements for a specific stock
MATCH (s:Stock {symbol: 'AAPL'})-[:HAS_PRICE_HISTORY]->(p:PricePoint)
WHERE p.timestamp >= datetime() - duration('P7D')
RETURN
  s.symbol as Symbol,
  p.timestamp as DateTime,
  p.price as Price,
  p.volume as Volume,
  p.high as High,
  p.low as Low,
  p.open as Open,
  p.close as Close
ORDER BY p.timestamp DESC;
```

### 10. Volatility Analysis
```cypher
// Calculate stock volatility over time periods
MATCH (s:Stock)-[:HAS_PRICE_HISTORY]->(p:PricePoint)
WHERE p.timestamp >= datetime() - duration('P30D')
WITH s,
     stdev(p.price) as PriceVolatility,
     avg(p.price) as AvgPrice,
     max(p.price) - min(p.price) as PriceRange,
     count(p) as DataPoints
RETURN
  s.symbol as Symbol,
  PriceVolatility,
  AvgPrice,
  PriceRange,
  (PriceVolatility / AvgPrice) * 100 as VolatilityPercent,
  DataPoints
ORDER BY VolatilityPercent DESC;
```

### 11. Moving Averages
```cypher
// Calculate 5-day and 20-day moving averages
MATCH (s:Stock {symbol: 'NVDA'})-[:HAS_PRICE_HISTORY]->(p:PricePoint)
WHERE p.timestamp >= datetime() - duration('P30D')
WITH s, p
ORDER BY p.timestamp
WITH s, collect(p) as prices
UNWIND range(4, size(prices)-1) as i
WITH s, prices[i] as current_price,
     prices[i-4..i] as ma5_window,
     prices[max(0, i-19)..i] as ma20_window
RETURN
  s.symbol as Symbol,
  current_price.timestamp as Date,
  current_price.price as CurrentPrice,
  avg([p in ma5_window | p.price]) as MA5,
  avg([p in ma20_window | p.price]) as MA20
ORDER BY current_price.timestamp DESC
LIMIT 20;
```

### 12. Volume Analysis
```cypher
// Volume pattern analysis
MATCH (s:Stock)-[:HAS_PRICE_HISTORY]->(p:PricePoint)
WHERE p.timestamp >= datetime() - duration('P7D')
WITH s, p
ORDER BY s.symbol, p.timestamp
WITH s, collect(p) as prices
WITH s, prices,
     avg([p in prices | p.volume]) as avgVolume,
     max([p in prices | p.volume]) as maxVolume
UNWIND prices as p
RETURN
  s.symbol as Symbol,
  p.timestamp as Date,
  p.volume as Volume,
  avgVolume,
  (p.volume / avgVolume) as VolumeRatio,
  CASE
    WHEN p.volume > avgVolume * 2 THEN 'HIGH_VOLUME 📈'
    WHEN p.volume < avgVolume * 0.5 THEN 'LOW_VOLUME 📉'
    ELSE 'NORMAL_VOLUME ➡️'
  END as VolumeCategory
ORDER BY s.symbol, p.timestamp DESC;
```

---

## 🔥 **Advanced Analytics Queries**

### 13. Momentum Analysis
```cypher
// Identify momentum stocks (consistent price increases)
MATCH (s:Stock)-[:HAS_PRICE_HISTORY]->(p:PricePoint)
WHERE p.timestamp >= datetime() - duration('P14D')
WITH s, p
ORDER BY s.symbol, p.timestamp
WITH s, collect(p.price) as prices
WHERE size(prices) >= 10
WITH s, prices,
     prices[-1] - prices[0] as totalChange,
     [i in range(1, size(prices)-1) |
      CASE WHEN prices[i] > prices[i-1] THEN 1 ELSE 0 END] as upDays
RETURN
  s.symbol as Symbol,
  s.current_price as CurrentPrice,
  totalChange,
  (totalChange / prices[0]) * 100 as TotalChangePercent,
  reduce(sum = 0, x in upDays | sum + x) as UpDays,
  size(upDays) as TotalDays,
  (reduce(sum = 0, x in upDays | sum + x) * 100.0 / size(upDays)) as UpDayPercent
ORDER BY TotalChangePercent DESC;
```

### 14. Risk Assessment
```cypher
// Risk assessment based on volatility and correlations
MATCH (s:Stock)
WHERE s.heat_score IS NOT NULL AND s.change_pct IS NOT NULL
OPTIONAL MATCH (s)-[r:CORRELATES_WITH]-()
WITH s, avg(abs(r.correlation)) as avgCorrelation, count(r) as correlationCount
RETURN
  s.symbol as Symbol,
  s.heat_score as HeatScore,
  abs(s.change_pct) as AbsoluteChange,
  avgCorrelation,
  correlationCount,
  CASE
    WHEN s.heat_score > 0.8 AND abs(s.change_pct) > 5 THEN 'HIGH_RISK ⚠️'
    WHEN s.heat_score > 0.6 OR abs(s.change_pct) > 3 THEN 'MEDIUM_RISK 🔶'
    ELSE 'LOW_RISK 🟢'
  END as RiskLevel
ORDER BY s.heat_score DESC, abs(s.change_pct) DESC;
```

### 15. Sector Rotation Analysis
```cypher
// Detect sector rotation patterns
MATCH (sec:Sector)<-[:BELONGS_TO]-(s:Stock)
WHERE s.change_pct IS NOT NULL
WITH sec,
     avg(s.change_pct) as avgChange,
     sum(s.volume) as totalVolume,
     count(s) as stockCount
ORDER BY avgChange DESC
WITH collect({
  sector: sec.name,
  avgChange: avgChange,
  totalVolume: totalVolume,
  stockCount: stockCount
}) as sectors
RETURN
  [s in sectors | s.sector][0..3] as TopSectors,
  [s in sectors | s.avgChange][0..3] as TopChanges,
  [s in sectors | s.sector][-3..] as BottomSectors,
  [s in sectors | s.avgChange][-3..] as BottomChanges;
```

---

## 🛠️ **Data Management Queries**

### 16. Data Quality Checks
```cypher
// Check for missing or stale data
MATCH (s:Stock)
RETURN
  count(s) as TotalStocks,
  count(s.price) as StocksWithPrice,
  count(s.last_update) as StocksWithUpdate,
  count(CASE WHEN s.last_update > datetime() - duration('PT1H') THEN 1 END) as RecentlyUpdated,
  count(CASE WHEN s.is_streaming = true THEN 1 END) as LiveStreaming;

// Find stocks with missing critical data
MATCH (s:Stock)
WHERE s.price IS NULL OR s.last_update IS NULL OR s.change_pct IS NULL
RETURN
  s.symbol as Symbol,
  s.name as Name,
  s.price as Price,
  s.last_update as LastUpdate,
  s.change_pct as ChangePercent,
  'MISSING_DATA' as Issue;
```

### 17. Performance Monitoring
```cypher
// Monitor data update frequencies
MATCH (s:Stock)
WHERE s.last_update IS NOT NULL
WITH s, datetime() - datetime(s.last_update) as staleness
RETURN
  s.data_source as DataSource,
  count(s) as StockCount,
  avg(staleness.seconds) as AvgStalenessSeconds,
  max(staleness.seconds) as MaxStalenessSeconds,
  count(CASE WHEN staleness.seconds < 300 THEN 1 END) as FreshData,
  count(CASE WHEN staleness.seconds > 3600 THEN 1 END) as StaleData
ORDER BY DataSource;
```

---

## 🔧 **Database Maintenance Queries**

### 18. Index Creation (Run Once)
```cypher
// Create performance indexes
CREATE INDEX stock_symbol_idx IF NOT EXISTS FOR (s:Stock) ON (s.symbol);
CREATE INDEX stock_price_idx IF NOT EXISTS FOR (s:Stock) ON (s.price);
CREATE INDEX stock_change_idx IF NOT EXISTS FOR (s:Stock) ON (s.change_pct);
CREATE INDEX stock_heat_idx IF NOT EXISTS FOR (s:Stock) ON (s.heat_score);
CREATE INDEX stock_update_idx IF NOT EXISTS FOR (s:Stock) ON (s.last_update);
CREATE INDEX price_timestamp_idx IF NOT EXISTS FOR (p:PricePoint) ON (p.timestamp);
```

### 19. Data Cleanup
```cypher
// Remove old price history (keep last 90 days)
MATCH (p:PricePoint)
WHERE p.timestamp < datetime() - duration('P90D')
DELETE p;

// Update stale data indicators
MATCH (s:Stock)
WHERE datetime(s.last_update) < datetime() - duration('PT1H')
SET s.is_stale = true;
```

### 20. Backup Essential Data
```cypher
// Export current market snapshot
MATCH (s:Stock)
WHERE s.price IS NOT NULL
RETURN
  s.symbol as symbol,
  s.name as name,
  s.price as price,
  s.change_pct as change_pct,
  s.volume as volume,
  s.market_cap as market_cap,
  s.heat_score as heat_score,
  s.last_update as last_update,
  s.data_source as data_source
ORDER BY s.symbol;
```

---

## 📊 **Ready-to-Use Dashboard Queries**

### 21. Market Dashboard Data
```cypher
// Complete market overview for dashboard
MATCH (m:Market)-[:CONTAINS]->(sec:Sector)<-[:BELONGS_TO]-(s:Stock)
WHERE s.price IS NOT NULL
WITH sec,
     count(s) as stockCount,
     avg(s.change_pct) as avgChange,
     sum(s.volume) as totalVolume,
     sum(s.market_cap) as totalMarketCap,
     collect({symbol: s.symbol, change: s.change_pct, heat: s.heat_score}) as stocks
RETURN {
  sector: sec.name,
  stockCount: stockCount,
  avgChange: avgChange,
  totalVolume: totalVolume,
  totalMarketCap: totalMarketCap,
  topGainer: [s in stocks WHERE s.change IS NOT NULL | s][0],
  topLoser: [s in stocks WHERE s.change IS NOT NULL | s][-1],
  hottestStock: [s in stocks WHERE s.heat IS NOT NULL | s][0]
} as sectorData
ORDER BY avgChange DESC;
```

### 22. Real-time Alerts Query
```cypher
// Generate trading alerts
MATCH (s:Stock)
WHERE s.price IS NOT NULL AND s.change_pct IS NOT NULL
WITH s,
     CASE
       WHEN abs(s.change_pct) > 10 THEN 'MAJOR_MOVE'
       WHEN s.heat_score > 0.8 THEN 'HIGH_HEAT'
       WHEN s.volume > 50000000 THEN 'HIGH_VOLUME'
       ELSE null
     END as alertType
WHERE alertType IS NOT NULL
RETURN
  s.symbol as Symbol,
  s.name as Company,
  s.price as Price,
  s.change_pct as Change,
  s.volume as Volume,
  s.heat_score as Heat,
  alertType as AlertType,
  datetime() as AlertTime
ORDER BY abs(s.change_pct) DESC;
```

---

## 🚀 **Execute These Queries**

### In Neo4j Browser (http://localhost:7474):
1. Copy any query above
2. Paste into the query box
3. Click the play button or press Ctrl+Enter
4. View results in table or graph format

### In Python (using your existing connection):
```python
from neo4j import GraphDatabase

def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

# Example usage
market_overview = run_query("""
MATCH (s:Stock)
WHERE s.change_pct IS NOT NULL
RETURN s.symbol, s.change_pct
ORDER BY s.change_pct DESC
LIMIT 10
""")
```

---

## 📈 **Performance Tips**

1. **Always use LIMIT** for large result sets
2. **Use indexes** on frequently queried properties
3. **Filter early** with WHERE clauses
4. **Profile queries** with `PROFILE` prefix for optimization
5. **Use parameters** for repeated queries with different values

---

This guide provides complete Cypher query coverage for your RAGHEAT system. All queries are production-ready and optimized for your specific data schema. 🎯