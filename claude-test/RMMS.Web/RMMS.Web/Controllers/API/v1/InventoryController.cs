using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using RMMS.Services.Interfaces.Inventory;
using RMMS.Models.Inventory;
using Swashbuckle.AspNetCore.Annotations;

namespace RMMS.Web.Controllers.API.v1
{
    [Route("api/v1/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    [SwaggerTag("Inventory management endpoints")]
    public class InventoryController : BaseApiController
    {
        private readonly IInventoryLedgerService _inventoryService;
        private readonly ILogger<InventoryController> _logger;

        public InventoryController(IInventoryLedgerService inventoryService, ILogger<InventoryController> logger)
        {
            _inventoryService = inventoryService;
            _logger = logger;
        }

        [HttpGet]
        public IActionResult GetAll([FromQuery] int page = 1, [FromQuery] int pageSize = 20)
        {
            try
            {
                var inventory = _inventoryService.GetAllInventory();
                var paginatedData = inventory.Skip((page - 1) * pageSize).Take(pageSize).ToList();
                return Success(paginatedData);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving inventory");
                return Error("Failed to retrieve inventory", new List<string> { ex.Message }, 500);
            }
        }

        [HttpGet("{id}")]
        public IActionResult GetById(int id)
        {
            try
            {
                var item = _inventoryService.GetInventoryById(id);
                return item == null ? NotFoundError($"Inventory item {id} not found") : Success(item);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving inventory {Id}", id);
                return Error("Failed to retrieve inventory", new List<string> { ex.Message }, 500);
            }
        }

        [HttpGet("product/{productId}")]
        public IActionResult GetByProduct(int productId)
        {
            try
            {
                var items = _inventoryService.GetInventoryByProduct(productId);
                return Success(items);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving inventory for product {ProductId}", productId);
                return Error("Failed to retrieve inventory", new List<string> { ex.Message }, 500);
            }
        }

        [HttpGet("lowstock")]
        public IActionResult GetLowStock()
        {
            try
            {
                var items = _inventoryService.GetLowStockItems();
                return Success(items);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving low stock items");
                return Error("Failed to retrieve low stock items", new List<string> { ex.Message }, 500);
            }
        }
    }
}
