using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using RMMS.Services.Interfaces.Masters;
using RMMS.Models.Masters;
using Swashbuckle.AspNetCore.Annotations;

namespace RMMS.Web.Controllers.API.v1
{
    [Route("api/v1/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    [SwaggerTag("Product management endpoints")]
    public class ProductsController : BaseApiController
    {
        private readonly IProductService _productService;
        private readonly ILogger<ProductsController> _logger;

        public ProductsController(IProductService productService, ILogger<ProductsController> logger)
        {
            _productService = productService;
            _logger = logger;
        }

        [HttpGet]
        public IActionResult GetAll([FromQuery] int page = 1, [FromQuery] int pageSize = 20, [FromQuery] string? category = null)
        {
            try
            {
                var products = string.IsNullOrEmpty(category)
                    ? _productService.GetAllProducts()
                    : _productService.GetProductsByCategory(category);

                var paginatedData = products.Skip((page - 1) * pageSize).Take(pageSize).ToList();
                return Success(paginatedData);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving products");
                return Error("Failed to retrieve products", new List<string> { ex.Message }, 500);
            }
        }

        [HttpGet("{id}")]
        public IActionResult GetById(int id)
        {
            try
            {
                var product = _productService.GetProductById(id);
                return product == null ? NotFoundError($"Product {id} not found") : Success(product);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving product {Id}", id);
                return Error("Failed to retrieve product", new List<string> { ex.Message }, 500);
            }
        }

        [HttpPost]
        public IActionResult Create([FromBody] Product product)
        {
            try
            {
                if (!ModelState.IsValid) return ValidationError();
                var id = _productService.CreateProduct(product, "API User");
                product.Id = id;
                return CreatedAtAction(nameof(GetById), new { id }, Success(product, "Product created"));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating product");
                return Error("Failed to create product", new List<string> { ex.Message }, 500);
            }
        }

        [HttpPut("{id}")]
        public IActionResult Update(int id, [FromBody] Product product)
        {
            try
            {
                if (!ModelState.IsValid) return ValidationError();
                product.Id = id;
                var success = _productService.UpdateProduct(product, "API User");
                return success ? Success(product, "Product updated") : Error("Update failed", errors: null, statusCode: 500);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating product {Id}", id);
                return Error("Failed to update product", new List<string> { ex.Message }, 500);
            }
        }

        [HttpDelete("{id}")]
        public IActionResult Delete(int id)
        {
            try
            {
                var success = _productService.DeleteProduct(id, "API User");
                return success ? Success("Product deleted") : NotFoundError($"Product {id} not found");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting product {Id}", id);
                return Error("Failed to delete product", new List<string> { ex.Message }, 500);
            }
        }
    }
}
