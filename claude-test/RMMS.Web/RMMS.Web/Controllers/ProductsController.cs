using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Common.Extensions;
using RMMS.Common.Pagination;
using RMMS.Models.Masters;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Linq;

namespace RMMS.Web.Controllers
{
    // [Authorize] -- TEMPORARILY DISABLED FOR TESTING
    public class ProductsController : Controller
    {
        private readonly IProductService _productService;
        private readonly ILogger<ProductsController> _logger;

        public ProductsController(IProductService productService, ILogger<ProductsController> logger)
        {
            _productService = productService;
            _logger = logger;
        }

        // GET: Products
        public IActionResult Index(string searchTerm, int page = 1, string sortBy = "ProductName", string sortOrder = "asc")
        {
            try
            {
                const int pageSize = 16;

                List<Product> products;

                if (!string.IsNullOrWhiteSpace(searchTerm))
                {
                    products = _productService.SearchProducts(searchTerm);
                }
                else
                {
                    products = _productService.GetAllProducts();
                }

                // Apply sorting
                var productsQuery = products.AsQueryable().OrderByDynamic(sortBy, sortOrder);

                // Apply paging
                var pagedResult = PagedResult<Product>.Create(productsQuery, page, pageSize, sortBy, sortOrder);

                ViewBag.SearchTerm = searchTerm;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading products");
                TempData["Error"] = "Error loading products: " + ex.Message;
                return View(new PagedResult<Product>());
            }
        }

        // GET: Products/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var product = _productService.GetProductById(id);
                if (product == null)
                    return NotFound();

                return View(product);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading product {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Products/Create
        public IActionResult Create()
        {
            var product = new Product
            {
                ProductCode = "AUTO",
                Status = "Active",
                UnitOfMeasure = "Kg"
            };
            return View(product);
        }

        // POST: Products/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(Product product)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var productId = _productService.CreateProduct(product, username);
                    TempData["Success"] = $"Product {product.ProductName} created successfully!";
                    return RedirectToAction(nameof(Index));
                }
                return View(product);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating product");
                ModelState.AddModelError("", "Error creating product: " + ex.Message);
                return View(product);
            }
        }

        // GET: Products/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var product = _productService.GetProductById(id);
                if (product == null)
                    return NotFound();

                return View(product);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading product {id} for edit");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Products/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, Product product)
        {
            if (id != product.Id)
                return BadRequest();

            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var result = _productService.UpdateProduct(product, username);
                    if (result)
                    {
                        TempData["Success"] = "Product updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    ModelState.AddModelError("", "Failed to update product");
                }
                return View(product);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating product {id}");
                ModelState.AddModelError("", "Error updating product: " + ex.Message);
                return View(product);
            }
        }

        // GET: Products/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var product = _productService.GetProductById(id);
                if (product == null)
                    return NotFound();

                return View(product);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading product {id} for delete");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Products/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var result = _productService.DeleteProduct(id, username);
                if (result)
                    TempData["Success"] = "Product deleted successfully!";
                else
                    TempData["Error"] = "Failed to delete product";

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting product {id}");
                TempData["Error"] = "Error deleting product: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }
    }
}
