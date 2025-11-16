// Models/ViewModels/ProductWiseSalesViewModel.cs
using System.Collections.Generic;

namespace RMMS.Models.ViewModels
{
    public class ProductWiseSalesViewModel
    {
        public string? ProductFilter { get; set; }
        public int TotalProducts { get; set; }
        public decimal GrandTotalSales { get; set; }
        public decimal TotalQuantitySold { get; set; }
        public List<ProductSalesGroup> ProductGroups { get; set; } = new List<ProductSalesGroup>();

        public ProductWiseSalesViewModel()
        {
            ProductGroups = new List<ProductSalesGroup>();
        }
    }

    public class ProductSalesGroup
    {
        public string? ProductName { get; set; }
        public string? ProductCategory { get; set; }
        public decimal TotalQuantity { get; set; }
        public decimal TotalSales { get; set; }
        public int NumberOfSales { get; set; }
        public decimal AveragePrice { get; set; }
    }
}