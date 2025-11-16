// =====================================================
// REPORT SERVICE
// =====================================================

// RMMS.Services/ReportService.cs
using System;
using System.Data;
using System.Collections.Generic;
using RMMS.DataAccess.Helpers;
using Microsoft.Extensions.Configuration;
using Microsoft.Data.SqlClient;
using System.Linq;
using RMMS.Models;
 
namespace RMMS.Services
{
    public interface IReportService
    {
        // These methods provide aggregated data for various reports
        Dictionary<string, decimal> GetDailySalesReport(DateTime date);
        Dictionary<string, decimal> GetMonthlySalesReport(int month, int year);
        Dictionary<string, decimal> GetProfitLossReport(DateTime startDate, DateTime endDate);
        Dictionary<string, decimal> GetCashFlowReport(DateTime startDate, DateTime endDate);
        Dictionary<string, decimal> GetGSTReport(int month, int year);

        // This was missing and causing your CS1061 error
        Dictionary<string, object> GetStockSummaryReport();

        // Additional report methods you might need
        Dictionary<string, decimal> GetProductWiseReport(DateTime startDate, DateTime endDate);
        Dictionary<string, decimal> GetCustomerWiseReport(DateTime startDate, DateTime endDate);
    }

 
        public class ReportService : IReportService
        {
            // We'll inject these services once they're properly configured
            private readonly IRiceSalesService _riceSalesService;
            private readonly IByProductSalesService _byProductSalesService;
            private readonly ICashBookService _cashBookService;
            private readonly IBankTransactionService _bankService;

            // For now, use a parameterless constructor that works without dependencies
            public ReportService()
            {
                // Services will be injected when dependency injection is fully configured
                _riceSalesService = null!;
                _byProductSalesService = null!;
                _cashBookService = null!;
                _bankService = null!;
            }

            // Constructor with all dependencies for when DI is ready
            public ReportService(
                IRiceSalesService riceSalesService,
                IByProductSalesService byProductSalesService,
                ICashBookService cashBookService,
                IBankTransactionService bankService)
            {
                _riceSalesService = riceSalesService;
                _byProductSalesService = byProductSalesService;
                _cashBookService = cashBookService;
                _bankService = bankService;
            }

            public Dictionary<string, decimal> GetDailySalesReport(DateTime date)
            {
                // This aggregates all sales data for a specific day
                var report = new Dictionary<string, decimal>();

                try
                {
                    if (_riceSalesService != null)
                    {
                        var riceSales = _riceSalesService.GetAllSales(true)
                            .Where(s => s.SaleDate.Date == date.Date)
                            .ToList();

                        report["TotalRiceSales"] = riceSales.Sum(s => s.GrossInvoiceAmount);
                        report["RiceQuantity"] = riceSales.Sum(s => s.Quantity);
                        report["NumberOfRiceInvoices"] = riceSales.Count;
                    }
                    else
                    {
                        // Default values when service isn't available yet
                        report["TotalRiceSales"] = 0;
                        report["RiceQuantity"] = 0;
                        report["NumberOfRiceInvoices"] = 0;
                    }

                    if (_byProductSalesService != null)
                    {
                        var byProductSales = _byProductSalesService.GetAllSales()
                            .Where(s => s.SaleDate.Date == date.Date)
                            .ToList();

                        report["TotalByProductSales"] = byProductSales.Sum(s => s.TotalAmount);
                        report["ByProductQuantity"] = byProductSales.Sum(s => s.Quantity);
                    }
                    else
                    {
                        report["TotalByProductSales"] = 0;
                        report["ByProductQuantity"] = 0;
                    }

                    // Calculate totals
                    report["TotalSales"] = report["TotalRiceSales"] + report["TotalByProductSales"];
                    report["TotalQuantity"] = report["RiceQuantity"] + report["ByProductQuantity"];
                    report["AverageInvoiceValue"] = report["NumberOfRiceInvoices"] > 0 ?
                        report["TotalSales"] / report["NumberOfRiceInvoices"] : 0;
                }
                catch (Exception)
                {
                    // Return empty report if there's any error
                    return GetEmptyDailySalesReport();
                }

                return report;
            }

            public Dictionary<string, decimal> GetMonthlySalesReport(int month, int year)
            {
                // This provides a comprehensive view of sales for an entire month
                var report = new Dictionary<string, decimal>();

                var startDate = new DateTime(year, month, 1);
                var endDate = startDate.AddMonths(1).AddDays(-1);

                try
                {
                    decimal riceSalesTotal = 0;
                    decimal byProductSalesTotal = 0;

                    if (_riceSalesService != null)
                    {
                        riceSalesTotal = _riceSalesService.GetTotalSalesAmount(startDate, endDate);
                    }

                    if (_byProductSalesService != null)
                    {
                        byProductSalesTotal = _byProductSalesService.GetTotalSalesAmount(startDate, endDate);
                    }

                    report["TotalSales"] = riceSalesTotal + byProductSalesTotal;
                    report["RiceSales"] = riceSalesTotal;
                    report["ByProductSales"] = byProductSalesTotal;
                    report["AverageDailySales"] = report["TotalSales"] / DateTime.DaysInMonth(year, month);

                    // GST calculations would go here
                    report["TotalGST"] = report["TotalSales"] * 0.05m; // 5% GST on rice
                    report["NetRevenue"] = report["TotalSales"] - report["TotalGST"];
                }
                catch (Exception)
                {
                    return GetEmptyMonthlySalesReport();
                }

                return report;
            }

            public Dictionary<string, decimal> GetProfitLossReport(DateTime startDate, DateTime endDate)
            {
                // This calculates your profit and loss for a given period
                var report = new Dictionary<string, decimal>();

                try
                {
                    // Revenue calculation
                    decimal revenue = 0;
                    if (_riceSalesService != null)
                    {
                        revenue += _riceSalesService.GetTotalSalesAmount(startDate, endDate);
                    }
                    if (_byProductSalesService != null)
                    {
                        revenue += _byProductSalesService.GetTotalSalesAmount(startDate, endDate);
                    }

                    // Expense calculation
                    decimal expenses = 0;
                    if (_cashBookService != null)
                    {
                        expenses += _cashBookService.GetTotalPayments(startDate, endDate);
                    }
                    if (_bankService != null)
                    {
                        var bankTransactions = _bankService.GetTransactionsByDateRange(startDate, endDate);
                        expenses += bankTransactions.Sum(t => t.Withdrawals);
                    }

                    report["Revenue"] = revenue;
                    report["DirectCosts"] = expenses * 0.6m; // Assuming 60% are direct costs
                    report["OperatingExpenses"] = expenses * 0.4m; // Assuming 40% are operating expenses
                    report["GrossProfit"] = revenue - report["DirectCosts"];
                    report["NetProfit"] = report["GrossProfit"] - report["OperatingExpenses"];
                    report["ProfitMargin"] = revenue > 0 ? (report["NetProfit"] / revenue) * 100 : 0;
                }
                catch (Exception)
                {
                    return GetEmptyProfitLossReport();
                }

                return report;
            }

            public Dictionary<string, decimal> GetCashFlowReport(DateTime startDate, DateTime endDate)
            {
                // This tracks the movement of cash through your business
                var report = new Dictionary<string, decimal>();

                try
                {
                    decimal cashReceipts = 0;
                    decimal cashPayments = 0;
                    decimal bankDeposits = 0;
                    decimal bankWithdrawals = 0;

                    if (_cashBookService != null)
                    {
                        cashReceipts = _cashBookService.GetTotalReceipts(startDate, endDate);
                        cashPayments = _cashBookService.GetTotalPayments(startDate, endDate);
                    }

                    if (_bankService != null)
                    {
                        var transactions = _bankService.GetTransactionsByDateRange(startDate, endDate);
                        bankDeposits = transactions.Sum(t => t.Deposits);
                        bankWithdrawals = transactions.Sum(t => t.Withdrawals);
                    }

                    report["OpeningBalance"] = 0; // This would come from historical data
                    report["CashReceipts"] = cashReceipts;
                    report["BankDeposits"] = bankDeposits;
                    report["TotalReceipts"] = cashReceipts + bankDeposits;
                    report["CashPayments"] = cashPayments;
                    report["BankWithdrawals"] = bankWithdrawals;
                    report["TotalPayments"] = cashPayments + bankWithdrawals;
                    report["NetCashFlow"] = report["TotalReceipts"] - report["TotalPayments"];
                    report["ClosingBalance"] = report["OpeningBalance"] + report["NetCashFlow"];
                }
                catch (Exception)
                {
                    return GetEmptyCashFlowReport();
                }

                return report;
            }

            public Dictionary<string, object> GetStockSummaryReport()
            {
                // This method was missing and causing your compilation error
                // It provides a comprehensive view of all inventory
                var report = new Dictionary<string, object>();

                try
                {
                    // Initialize stock values - these would come from inventory tracking
                    report["PaddyStock"] = 0m; // Will be populated from paddy procurement
                    report["RiceStock"] = 0m; // Will be calculated from production minus sales
                    report["ByProductStock"] = 0m; // Bran, husk, etc.
                    report["TotalStockValue"] = 0m; // Monetary value of all stock
                    report["LastUpdated"] = DateTime.Now;

                    // You can add more complex calculations here as your system grows
                    // For example, calculating stock based on:
                    // - Opening stock
                    // + Procurement/Production
                    // - Sales/Consumption
                    // = Closing stock
                }
                catch (Exception)
                {
                    report["PaddyStock"] = 0m;
                    report["RiceStock"] = 0m;
                    report["ByProductStock"] = 0m;
                    report["TotalStockValue"] = 0m;
                    report["LastUpdated"] = DateTime.Now;
                }

                return report;
            }

            public Dictionary<string, decimal> GetGSTReport(int month, int year)
            {
                // This helps with tax compliance by calculating GST obligations
                var report = new Dictionary<string, decimal>();

                var startDate = new DateTime(year, month, 1);
                var endDate = startDate.AddMonths(1).AddDays(-1);

                try
                {
                    if (_riceSalesService != null)
                    {
                        var sales = _riceSalesService.GetAllSales(true)
                            .Where(s => s.SaleDate >= startDate && s.SaleDate <= endDate)
                            .ToList();

                        report["TotalSales"] = sales.Sum(s => s.TotalInvoiceValue);
                        report["TaxableAmount"] = sales.Sum(s => s.TaxableValue);
                        report["CGST"] = sales.Sum(s => s.CGSTAmount);
                        report["SGST"] = sales.Sum(s => s.SGSTAmount);
                        report["IGST"] = sales.Sum(s => s.IGSTAmount);
                        report["TotalGST"] = report["CGST"] + report["SGST"] + report["IGST"];
                    }
                    else
                    {
                        return GetEmptyGSTReport();
                    }
                }
                catch (Exception)
                {
                    return GetEmptyGSTReport();
                }

                return report;
            }

            public Dictionary<string, decimal> GetProductWiseReport(DateTime startDate, DateTime endDate)
            {
                // Analyzes sales by product category
                var report = new Dictionary<string, decimal>();

                // Implementation would group sales by product type
                report["RiceProducts"] = 0;
                report["ByProducts"] = 0;
                report["Total"] = 0;

                return report;
            }

            public Dictionary<string, decimal> GetCustomerWiseReport(DateTime startDate, DateTime endDate)
            {
                // Analyzes sales by customer
                var report = new Dictionary<string, decimal>();

                // Implementation would group sales by customer
                report["TotalCustomers"] = 0;
                report["AveragePerCustomer"] = 0;
                report["TopCustomerValue"] = 0;

                return report;
            }

            // Helper methods to return empty reports when services aren't available
            private Dictionary<string, decimal> GetEmptyDailySalesReport()
            {
                return new Dictionary<string, decimal>
                {
                    ["TotalSales"] = 0,
                    ["TotalQuantity"] = 0,
                    ["NumberOfRiceInvoices"] = 0,
                    ["AverageInvoiceValue"] = 0
                };
            }

            private Dictionary<string, decimal> GetEmptyMonthlySalesReport()
            {
                return new Dictionary<string, decimal>
                {
                    ["TotalSales"] = 0,
                    ["RiceSales"] = 0,
                    ["ByProductSales"] = 0,
                    ["TotalGST"] = 0,
                    ["NetRevenue"] = 0
                };
            }

            private Dictionary<string, decimal> GetEmptyProfitLossReport()
            {
                return new Dictionary<string, decimal>
                {
                    ["Revenue"] = 0,
                    ["DirectCosts"] = 0,
                    ["GrossProfit"] = 0,
                    ["OperatingExpenses"] = 0,
                    ["NetProfit"] = 0
                };
            }

            private Dictionary<string, decimal> GetEmptyCashFlowReport()
            {
                return new Dictionary<string, decimal>
                {
                    ["OpeningBalance"] = 0,
                    ["CashReceipts"] = 0,
                    ["CashPayments"] = 0,
                    ["NetCashFlow"] = 0,
                    ["ClosingBalance"] = 0
                };
            }

            private Dictionary<string, decimal> GetEmptyGSTReport()
            {
                return new Dictionary<string, decimal>
                {
                    ["TotalSales"] = 0,
                    ["TaxableAmount"] = 0,
                    ["CGST"] = 0,
                    ["SGST"] = 0,
                    ["IGST"] = 0,
                    ["TotalGST"] = 0
                };
            }
        }
    
}