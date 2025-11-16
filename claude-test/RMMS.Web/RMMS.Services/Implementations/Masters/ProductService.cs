using RMMS.DataAccess.Repositories.Masters;
using RMMS.Models.Masters;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services.Implementations.Masters
{
    public class ProductService : IProductService
    {
        private readonly IProductRepository _repository;

        public ProductService(IProductRepository repository)
        {
            _repository = repository;
        }

        public List<Product> GetAllProducts(bool activeOnly = true)
        {
            return _repository.GetAll(activeOnly);
        }

        public Product? GetProductById(int id)
        {
            return _repository.GetById(id);
        }

        public Product? GetProductByCode(string code)
        {
            return _repository.GetByCode(code);
        }

        public int CreateProduct(Product product, string createdBy)
        {
            product.CreatedDate = DateTime.Now;
            product.CreatedBy = createdBy;
            product.IsActive = true;

            if (string.IsNullOrEmpty(product.ProductCode))
            {
                product.ProductCode = GenerateProductCode(product.ProductCategory);
            }

            return _repository.Create(product);
        }

        public bool UpdateProduct(Product product, string modifiedBy)
        {
            product.ModifiedDate = DateTime.Now;
            product.ModifiedBy = modifiedBy;
            return _repository.Update(product);
        }

        public bool DeleteProduct(int id, string deletedBy)
        {
            return _repository.Delete(id);
        }

        public List<Product> SearchProducts(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return GetAllProducts();

            return _repository.Search(searchTerm);
        }

        public List<Product> GetProductsByCategory(string category)
        {
            return _repository.GetByCategory(category);
        }

        public List<Product> GetRawMaterials()
        {
            return _repository.GetRawMaterials();
        }

        public List<Product> GetFinishedProducts()
        {
            return _repository.GetFinishedProducts();
        }

        public List<Product> GetByProducts()
        {
            return _repository.GetByProducts();
        }

        public string GenerateProductCode(string category)
        {
            var prefix = category?.ToUpper() switch
            {
                "RICE" => "RICE",
                "PADDY" => "PADY",
                "BY-PRODUCT" => "BYPD",
                _ => "PROD"
            };

            var products = _repository.GetAll(false);
            if (products.Any())
            {
                var maxCode = products
                    .Select(p => p.ProductCode)
                    .Where(code => code.StartsWith(prefix))
                    .Select(code => int.TryParse(code.Substring(4), out int num) ? num : 0)
                    .DefaultIfEmpty(0)
                    .Max();
                return $"{prefix}{(maxCode + 1):D4}";
            }
            return $"{prefix}0001";
        }
    }
}
