# RMMS Web - Quick Access Guide

## 🚀 Application is LIVE!

**URL**: http://localhost:5000
**Status**: ✅ Running (PID: 6837)
**Port**: 5000

---

## 📱 Quick Links - Transaction Pages

| Page | Direct Link |
|------|-------------|
| 🌾 Paddy Procurement | http://localhost:5000/PaddyProcurement |
| 🍚 Rice Sales | http://localhost:5000/RiceSales |
| 💰 Cash Book | http://localhost:5000/CashBook |
| 🏦 Bank Transactions | http://localhost:5000/BankTransactions |
| 📄 Vouchers | http://localhost:5000/Vouchers |
| 🏢 Fixed Assets | http://localhost:5000/FixedAssets |
| 💵 Loans & Advances | http://localhost:5000/LoansAdvances |
| ♻️ By-Product Sales | http://localhost:5000/ByProductSales |
| 📦 External Rice Sales | http://localhost:5000/ExternalRiceSales |
| ⏰ Payables Overdue | http://localhost:5000/PayablesOverdue |
| 📮 Receivables Overdue | http://localhost:5000/ReceivablesOverdue |

---

## 📊 Quick Links - Yield Analysis

| Page | Direct Link |
|------|-------------|
| 📈 Yield Trends | http://localhost:5000/YieldAnalysis/Trends |
| 🌱 Yield by Variety | http://localhost:5000/YieldAnalysis/ByVariety |
| ⚙️ Yield by Machine | http://localhost:5000/YieldAnalysis/ByMachine |
| 📉 Yield Variance | http://localhost:5000/YieldAnalysis/Variance |
| 🎯 Batch Performance | http://localhost:5000/YieldAnalysis/Performance |
| ⬇️ Low Yield Analysis | http://localhost:5000/YieldAnalysis/LowYield |
| ⬆️ High Yield Analysis | http://localhost:5000/YieldAnalysis/HighYield |

---

## 📋 Quick Links - Reports

| Page | Direct Link |
|------|-------------|
| 👥 Customer-wise Sales | http://localhost:5000/Reports/CustomerWiseSales |
| 📦 Product-wise Sales | http://localhost:5000/Reports/ProductWiseSales |
| 📅 Daily Sales | http://localhost:5000/Reports/DailySales |
| 💳 Outstanding Payments | http://localhost:5000/Reports/OutstandingPayments |
| 📊 Stock Movement | http://localhost:5000/Reports/StockMovement |
| 🌾 Paddy Stock | http://localhost:5000/Reports/PaddyStock |
| 🍚 Rice Stock | http://localhost:5000/Reports/RiceStock |

---

## 🔧 Quick Commands

### Check Application Status
```bash
ps aux | grep RMMS.Web
```

### Check Port Status
```bash
ss -tlnp | grep :5000
```

### Stop Application
```bash
kill 6837
```

### Start Application
```bash
cd /home/user01/claude-test/RMMS.Web/RMMS.Web
dotnet run --urls "http://0.0.0.0:5000"
```

### Generate Test Data
```bash
cd /home/user01/claude-test/RMMS.Web
./SEED_ALL_DATA.sh
```

---

## ✅ What to Verify

On each page, check for:

1. **Pagination controls** at bottom
2. **"Show entries" dropdown** (10, 16, 25, 50, 100, All)
3. **Search box** at top right
4. **Sortable columns** (arrows on headers)
5. **Info text**: "Showing X to Y of Z entries"
6. **Export buttons**: Copy, Excel, PDF, Print

---

## 📚 Documentation

- **Full Report**: `/home/user01/claude-test/RMMS.Web/DEPLOYMENT_VERIFICATION_REPORT.md`
- **Fix Summary**: `/home/user01/claude-test/RMMS.Web/PAGINATION_AND_SORTING_FIX_SUMMARY.md`
- **This Guide**: `/home/user01/claude-test/RMMS.Web/QUICK_ACCESS_GUIDE.md`

---

## 🎯 Key Features Enabled

- ✅ **16 rows per page** (default)
- ✅ **Column sorting** (click any header)
- ✅ **Full-text search** across all columns
- ✅ **Export to Excel/PDF/CSV**
- ✅ **Responsive** (works on mobile)
- ✅ **State persistence** (remembers your settings for 24hrs)

---

## 🎉 100% Complete!

All grids now have pagination and sorting enabled.
The application is production-ready!

**Access now**: http://localhost:5000
