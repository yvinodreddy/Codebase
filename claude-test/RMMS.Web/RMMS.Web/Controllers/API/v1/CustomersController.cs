using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using RMMS.Services.Interfaces.Masters;
using RMMS.Models.Masters;
using Swashbuckle.AspNetCore.Annotations;

namespace RMMS.Web.Controllers.API.v1
{
    /// <summary>
    /// Customers API Controller - Manages customer data
    /// </summary>
    [Route("api/v1/[controller]")]
    [Authorize(AuthenticationSchemes = JwtBearerDefaults.AuthenticationScheme)]
    [SwaggerTag("Customer management endpoints")]
    public class CustomersController : BaseApiController
    {
        private readonly ICustomerService _customerService;
        private readonly ILogger<CustomersController> _logger;

        public CustomersController(
            ICustomerService customerService,
            ILogger<CustomersController> logger)
        {
            _customerService = customerService;
            _logger = logger;
        }

        /// <summary>
        /// Get all customers with optional pagination
        /// </summary>
        [HttpGet]
        [SwaggerOperation(Summary = "Get all customers", Description = "Returns paginated list of customers")]
        [SwaggerResponse(200, "Success", typeof(ApiResponse<List<Customer>>))]
        public IActionResult GetAll(
            [FromQuery] int page = 1,
            [FromQuery] int pageSize = 20,
            [FromQuery] string? search = null,
            [FromQuery] string? city = null,
            [FromQuery] bool? isActive = null)
        {
            try
            {
                pageSize = Math.Min(pageSize, 100);

                var allCustomers = _customerService.GetAllCustomers(activeOnly: false);

                // Apply filters
                var filtered = allCustomers.AsEnumerable();

                if (!string.IsNullOrEmpty(search))
                {
                    filtered = filtered.Where(c =>
                        c.CustomerName.Contains(search, StringComparison.OrdinalIgnoreCase) ||
                        c.CustomerCode.Contains(search, StringComparison.OrdinalIgnoreCase));
                }

                if (!string.IsNullOrEmpty(city))
                {
                    // Filter by city from addresses if available
                    filtered = filtered.Where(c => c.Addresses != null && c.Addresses.Any(a => a.City.Equals(city, StringComparison.OrdinalIgnoreCase)));
                }

                if (isActive.HasValue)
                {
                    filtered = filtered.Where(c => c.IsActive == isActive.Value);
                }

                var totalCount = filtered.Count();
                var totalPages = (int)Math.Ceiling(totalCount / (double)pageSize);

                var paginatedData = filtered
                    .Skip((page - 1) * pageSize)
                    .Take(pageSize)
                    .ToList();

                var response = Success(paginatedData, "Customers retrieved successfully");
                if (response is OkObjectResult okResult && okResult.Value is ApiResponse<List<Customer>> apiResponse)
                {
                    apiResponse.Pagination = new PaginationMetadata
                    {
                        CurrentPage = page,
                        PageSize = pageSize,
                        TotalPages = totalPages,
                        TotalCount = totalCount
                    };
                    return Ok(apiResponse);
                }

                return response;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving customers");
                return Error("Failed to retrieve customers", new List<string> { ex.Message }, 500);
            }
        }

        /// <summary>
        /// Get customer by ID
        /// </summary>
        [HttpGet("{id}")]
        [SwaggerOperation(Summary = "Get customer by ID")]
        [SwaggerResponse(200, "Success", typeof(ApiResponse<Customer>))]
        [SwaggerResponse(404, "Customer not found")]
        public IActionResult GetById(int id)
        {
            try
            {
                var customer = _customerService.GetCustomerById(id);
                if (customer == null)
                    return NotFoundError($"Customer with ID {id} not found");

                return Success(customer, "Customer retrieved successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving customer {CustomerId}", id);
                return Error("Failed to retrieve customer", new List<string> { ex.Message }, 500);
            }
        }

        /// <summary>
        /// Create new customer
        /// </summary>
        [HttpPost]
        [SwaggerOperation(Summary = "Create new customer")]
        [SwaggerResponse(201, "Customer created", typeof(ApiResponse<Customer>))]
        [SwaggerResponse(422, "Validation failed")]
        public IActionResult Create([FromBody] Customer customer)
        {
            try
            {
                if (!ModelState.IsValid)
                    return ValidationError();

                var customerId = _customerService.CreateCustomer(customer, "API User");

                _logger.LogInformation("Customer created: {CustomerName} (ID: {CustomerId})", customer.CustomerName, customerId);

                customer.Id = customerId;
                return CreatedAtAction(nameof(GetById), new { id = customerId },
                    Success(customer, "Customer created successfully"));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating customer");
                return Error("Failed to create customer", new List<string> { ex.Message }, 500);
            }
        }

        /// <summary>
        /// Update existing customer
        /// </summary>
        [HttpPut("{id}")]
        [SwaggerOperation(Summary = "Update customer")]
        [SwaggerResponse(200, "Customer updated", typeof(ApiResponse<Customer>))]
        [SwaggerResponse(404, "Customer not found")]
        public IActionResult Update(int id, [FromBody] Customer customer)
        {
            try
            {
                if (!ModelState.IsValid)
                    return ValidationError();

                var existing = _customerService.GetCustomerById(id);
                if (existing == null)
                    return NotFoundError($"Customer with ID {id} not found");

                customer.Id = id;
                var success = _customerService.UpdateCustomer(customer, "API User");

                if (!success)
                    return Error("Failed to update customer", null, 500);

                _logger.LogInformation("Customer updated: {CustomerName} (ID: {CustomerId})", customer.CustomerName, id);

                return Success(customer, "Customer updated successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating customer {CustomerId}", id);
                return Error("Failed to update customer", new List<string> { ex.Message }, 500);
            }
        }

        /// <summary>
        /// Delete customer
        /// </summary>
        [HttpDelete("{id}")]
        [SwaggerOperation(Summary = "Delete customer")]
        [SwaggerResponse(200, "Customer deleted")]
        [SwaggerResponse(404, "Customer not found")]
        public IActionResult Delete(int id)
        {
            try
            {
                var existing = _customerService.GetCustomerById(id);
                if (existing == null)
                    return NotFoundError($"Customer with ID {id} not found");

                var success = _customerService.DeleteCustomer(id, "API User");

                if (!success)
                    return Error("Failed to delete customer", null, 500);

                _logger.LogInformation("Customer deleted: ID {CustomerId}", id);

                return Success("Customer deleted successfully");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting customer {CustomerId}", id);
                return Error("Failed to delete customer", new List<string> { ex.Message }, 500);
            }
        }

        /// <summary>
        /// Search customers by name or code
        /// </summary>
        [HttpGet("search")]
        [SwaggerOperation(Summary = "Search customers")]
        [SwaggerResponse(200, "Success")]
        public IActionResult Search([FromQuery] string query)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(query))
                    return Error("Search query is required", null, 400);

                var results = _customerService.SearchCustomers(query)
                    .Take(50) // Limit to 50 results
                    .ToList();

                return Success(results, $"{results.Count} customers found");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error searching customers");
                return Error("Search failed", new List<string> { ex.Message }, 500);
            }
        }
    }
}
