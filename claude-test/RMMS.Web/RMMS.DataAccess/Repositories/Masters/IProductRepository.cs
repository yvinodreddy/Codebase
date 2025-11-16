using RMMS.Models.Masters;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Masters
{
    public interface IProductRepository
    {
        List<Product> GetAll(bool activeOnly = true);
        Product? GetById(int id);
        Product? GetByCode(string code);
        int Create(Product product);
        bool Update(Product product);
        bool Delete(int id);
        List<Product> Search(string searchTerm);
        List<Product> GetByCategory(string category);
        List<Product> GetRawMaterials();
        List<Product> GetFinishedProducts();
        List<Product> GetByProducts();
    }
}
