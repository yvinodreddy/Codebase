using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using RMMS.Services.Interfaces.Production;
using RMMS.Models.Production;
using Swashbuckle.AspNetCore.Annotations;

namespace RMMS.Web.Controllers.API.v1
{
    [Route("api/v1/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    [SwaggerTag("Production management endpoints")]
    public class ProductionController : BaseApiController
    {
        private readonly IProductionOrderService _productionOrderService;
        private readonly ILogger<ProductionController> _logger;

        public ProductionController(IProductionOrderService productionOrderService, ILogger<ProductionController> logger)
        {
            _productionOrderService = productionOrderService;
            _logger = logger;
        }

        [HttpGet]
        public IActionResult GetAll([FromQuery] int page = 1, [FromQuery] int pageSize = 20)
        {
            try
            {
                var orders = _productionOrderService.GetAllProductionOrders();
                var paginatedData = orders.Skip((page - 1) * pageSize).Take(pageSize).ToList();
                return Success(paginatedData);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving production orders");
                return Error("Failed to retrieve production orders", new List<string> { ex.Message }, 500);
            }
        }

        [HttpGet("{id}")]
        public IActionResult GetById(int id)
        {
            try
            {
                var order = _productionOrderService.GetProductionOrderById(id);
                return order == null ? NotFoundError($"Production order {id} not found") : Success(order);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving production order {Id}", id);
                return Error("Failed to retrieve production order", new List<string> { ex.Message }, 500);
            }
        }

        [HttpPost]
        public IActionResult Create([FromBody] ProductionOrder order)
        {
            try
            {
                if (!ModelState.IsValid) return ValidationError();
                var success = _productionOrderService.CreateProductionOrder(order, "API User");
                return success ? Success(order, "Production order created") : Error("Failed to create order", errors: null, statusCode: 500);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating production order");
                return Error("Failed to create production order", new List<string> { ex.Message }, 500);
            }
        }

        [HttpPut("{id}")]
        public IActionResult Update(int id, [FromBody] ProductionOrder order)
        {
            try
            {
                if (!ModelState.IsValid) return ValidationError();
                order.Id = id;
                var success = _productionOrderService.UpdateProductionOrder(order, "API User");
                return success ? Success(order, "Production order updated") : Error("Update failed", null, 500);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating production order {Id}", id);
                return Error("Failed to update production order", new List<string> { ex.Message }, 500);
            }
        }

        [HttpDelete("{id}")]
        public IActionResult Delete(int id)
        {
            try
            {
                var success = _productionOrderService.DeleteProductionOrder(id);
                return success ? Success("Production order deleted") : NotFoundError($"Production order {id} not found");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting production order {Id}", id);
                return Error("Failed to delete production order", new List<string> { ex.Message }, 500);
            }
        }
    }
}
