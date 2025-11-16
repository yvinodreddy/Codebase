using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using RMMS.Services.Interfaces.Sales;
using RMMS.Models.Sales;
using Swashbuckle.AspNetCore.Annotations;

namespace RMMS.Web.Controllers.API.v1
{
    [Route("api/v1/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    [SwaggerTag("Sales order management endpoints")]
    public class SalesOrdersController : BaseApiController
    {
        private readonly ISalesOrderService _salesOrderService;
        private readonly ILogger<SalesOrdersController> _logger;

        public SalesOrdersController(ISalesOrderService salesOrderService, ILogger<SalesOrdersController> logger)
        {
            _salesOrderService = salesOrderService;
            _logger = logger;
        }

        [HttpGet]
        public async Task<IActionResult> GetAll([FromQuery] int page = 1, [FromQuery] int pageSize = 20)
        {
            try
            {
                var orders = await _salesOrderService.GetAllSalesOrdersAsync();
                var paginatedData = orders.Skip((page - 1) * pageSize).Take(pageSize).ToList();
                return Success(paginatedData);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving sales orders");
                return Error("Failed to retrieve sales orders", new List<string> { ex.Message }, 500);
            }
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetById(int id)
        {
            try
            {
                var order = await _salesOrderService.GetSalesOrderByIdAsync(id);
                return order == null ? NotFoundError($"Sales order {id} not found") : Success(order);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving sales order {Id}", id);
                return Error("Failed to retrieve sales order", new List<string> { ex.Message }, 500);
            }
        }

        [HttpPost]
        public async Task<IActionResult> Create([FromBody] SalesOrder order)
        {
            try
            {
                if (!ModelState.IsValid) return ValidationError();
                var created = await _salesOrderService.CreateSalesOrderAsync(order);
                return Success(created, "Sales order created");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating sales order");
                return Error("Failed to create sales order", new List<string> { ex.Message }, 500);
            }
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> Update(int id, [FromBody] SalesOrder order)
        {
            try
            {
                if (!ModelState.IsValid) return ValidationError();
                order.Id = id;
                await _salesOrderService.UpdateSalesOrderAsync(order);
                return Success(order, "Sales order updated");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating sales order {Id}", id);
                return Error("Failed to update sales order", new List<string> { ex.Message }, 500);
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                await _salesOrderService.DeleteSalesOrderAsync(id);
                return Success("Sales order deleted");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting sales order {Id}", id);
                return Error("Failed to delete sales order", new List<string> { ex.Message }, 500);
            }
        }
    }
}
