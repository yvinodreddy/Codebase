#!/bin/bash

# Fix QuotationsController
echo "Fixing QuotationsController..."
cp Controllers/QuotationsController.cs Controllers/QuotationsController.cs.backup

cat > /tmp/quotations_fix.txt << 'EOF'
        // GET: Quotations
        public async Task<IActionResult> Index(string searchTerm, string status, int page = 1)
        {
            try
            {
                const int pageSize = 16;
                IEnumerable<Quotation> quotations;

                if (!string.IsNullOrEmpty(searchTerm))
                {
                    quotations = await _quotationService.SearchQuotationsAsync(searchTerm);
                }
                else if (!string.IsNullOrEmpty(status))
                {
                    quotations = await _quotationService.GetQuotationsByStatusAsync(status);
                }
                else
                {
                    quotations = await _quotationService.GetAllQuotationsAsync();
                }

                var stats = await _quotationService.GetQuotationStatisticsAsync();
                ViewBag.Statistics = stats;
                ViewBag.SearchTerm = searchTerm;
                ViewBag.SelectedStatus = status;

                // Apply pagination
                var totalRecords = quotations.Count();
                var totalPages = (int)Math.Ceiling(totalRecords / (double)pageSize);
                var pagedQuotations = quotations.Skip((page - 1) * pageSize).Take(pageSize).ToList();

                ViewBag.CurrentPage = page;
                ViewBag.TotalPages = totalPages;
                ViewBag.TotalRecords = totalRecords;

                return View(pagedQuotations);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading quotations: {ex.Message}";
                return View(new List<Quotation>());
            }
        }
EOF

# Fix SalesOrdersController
echo "Fixing SalesOrdersController..."
cp Controllers/SalesOrdersController.cs Controllers/SalesOrdersController.cs.backup

cat > /tmp/salesorders_fix.txt << 'EOF'
        public async Task<IActionResult> Index(string searchTerm, string status, int page = 1)
        {
            try
            {
                const int pageSize = 16;
                IEnumerable<SalesOrder> salesOrders;

                if (!string.IsNullOrEmpty(searchTerm))
                {
                    salesOrders = await _salesOrderService.SearchSalesOrdersAsync(searchTerm);
                }
                else if (!string.IsNullOrEmpty(status))
                {
                    salesOrders = await _salesOrderService.GetSalesOrdersByStatusAsync(status);
                }
                else
                {
                    salesOrders = await _salesOrderService.GetAllSalesOrdersAsync();
                }

                var stats = await _salesOrderService.GetSalesOrderStatisticsAsync();
                ViewBag.Statistics = stats;
                ViewBag.SearchTerm = searchTerm;
                ViewBag.SelectedStatus = status;

                // Apply pagination
                var totalRecords = salesOrders.Count();
                var totalPages = (int)Math.Ceiling(totalRecords / (double)pageSize);
                var pagedSalesOrders = salesOrders.Skip((page - 1) * pageSize).Take(pageSize).ToList();

                ViewBag.CurrentPage = page;
                ViewBag.TotalPages = totalPages;
                ViewBag.TotalRecords = totalRecords;

                return View(pagedSalesOrders);
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error loading sales orders: {ex.Message}";
                return View(new List<SalesOrder>());
            }
        }
EOF

echo "✅ Pagination fixes prepared"
echo "Note: Manual edits still required to insert the code"
