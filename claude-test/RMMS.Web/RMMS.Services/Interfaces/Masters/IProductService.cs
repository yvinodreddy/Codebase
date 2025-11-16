using RMMS.Models.Masters;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Masters
{
    public interface IProductService
    {
        List<Product> GetAllProducts(bool activeOnly = true);
        Product? GetProductById(int id);
        Product? GetProductByCode(string code);
        int CreateProduct(Product product, string createdBy);
        bool UpdateProduct(Product product, string modifiedBy);
        bool DeleteProduct(int id, string deletedBy);
        List<Product> SearchProducts(string searchTerm);
        List<Product> GetProductsByCategory(string category);
        List<Product> GetRawMaterials();
        List<Product> GetFinishedProducts();
        List<Product> GetByProducts();
        string GenerateProductCode(string category);
    }
}
