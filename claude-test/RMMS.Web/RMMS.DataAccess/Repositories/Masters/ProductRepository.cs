using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Masters;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Masters
{
    public class ProductRepository : IProductRepository
    {
        private readonly ApplicationDbContext _context;

        public ProductRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<Product> GetAll(bool activeOnly = true)
        {
            var query = _context.Products.AsQueryable();

            if (activeOnly)
                query = query.Where(p => p.IsActive);

            return query.OrderByDescending(p => p.CreatedDate).ToList();
        }

        public Product? GetById(int id)
        {
            return _context.Products.FirstOrDefault(p => p.Id == id);
        }

        public Product? GetByCode(string code)
        {
            return _context.Products.FirstOrDefault(p => p.ProductCode == code);
        }

        public int Create(Product product)
        {
            _context.Products.Add(product);
            _context.SaveChanges();
            return product.Id;
        }

        public bool Update(Product product)
        {
            _context.Products.Update(product);
            return _context.SaveChanges() > 0;
        }

        public bool Delete(int id)
        {
            var product = _context.Products.Find(id);
            if (product != null)
            {
                product.IsActive = false;
                product.ModifiedDate = DateTime.Now;
                return _context.SaveChanges() > 0;
            }
            return false;
        }

        public List<Product> Search(string searchTerm)
        {
            return _context.Products
                .Where(p => p.IsActive &&
                    (p.ProductName.Contains(searchTerm) ||
                     p.ProductCode.Contains(searchTerm) ||
                     (p.ProductType != null && p.ProductType.Contains(searchTerm)) ||
                     (p.HSNCode != null && p.HSNCode.Contains(searchTerm))))
                .OrderBy(p => p.ProductName)
                .ToList();
        }

        public List<Product> GetByCategory(string category)
        {
            return _context.Products
                .Where(p => p.IsActive && p.ProductCategory == category)
                .OrderBy(p => p.ProductName)
                .ToList();
        }

        public List<Product> GetRawMaterials()
        {
            return _context.Products
                .Where(p => p.IsActive && p.IsRawMaterial)
                .OrderBy(p => p.ProductName)
                .ToList();
        }

        public List<Product> GetFinishedProducts()
        {
            return _context.Products
                .Where(p => p.IsActive && p.IsFinishedProduct)
                .OrderBy(p => p.ProductName)
                .ToList();
        }

        public List<Product> GetByProducts()
        {
            return _context.Products
                .Where(p => p.IsActive && p.IsByProduct)
                .OrderBy(p => p.ProductName)
                .ToList();
        }
    }
}
