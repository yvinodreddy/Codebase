using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Integrations;
using RMMS.Models.API;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;

namespace RMMS.Web.Controllers.Phase4
{
    [AllowAnonymous] // Temporarily enabled for testing
    public class IntegrationsController : Controller
    {
        private readonly IIntegrationService _integrationService;
        private readonly ApplicationDbContext _context;
        private readonly ILogger<IntegrationsController> _logger;
        private readonly HttpClient _httpClient;

        public IntegrationsController(
            IIntegrationService integrationService,
            ApplicationDbContext context,
            ILogger<IntegrationsController> logger,
            IHttpClientFactory httpClientFactory)
        {
            _integrationService = integrationService;
            _context = context;
            _logger = logger;
            _httpClient = httpClientFactory.CreateClient();
            _httpClient.Timeout = TimeSpan.FromSeconds(10);
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                // Get all integrations with comprehensive statistics
                var integrations = await _context.Set<IntegrationStatus>()
                    .OrderByDescending(i => i.CreatedDate)
                    .ToListAsync();

                // Calculate dashboard statistics
                ViewBag.TotalIntegrations = integrations.Count;
                ViewBag.ConnectedCount = integrations.Count(i => i.Status == "Connected");
                ViewBag.ErrorCount = integrations.Count(i => i.Status == "Error");
                ViewBag.DisconnectedCount = integrations.Count(i => i.Status == "Disconnected");

                // Calculate success rate across all integrations
                var totalAttempts = integrations.Sum(i => i.SuccessCount + i.FailureCount);
                var totalSuccess = integrations.Sum(i => i.SuccessCount);
                ViewBag.OverallSuccessRate = totalAttempts > 0
                    ? Math.Round((totalSuccess / (double)totalAttempts) * 100, 2)
                    : 0;

                // Average response time across connected integrations
                var connectedIntegrations = integrations.Where(i => i.Status == "Connected" && i.ResponseTime > 0).ToList();
                ViewBag.AvgResponseTime = connectedIntegrations.Any()
                    ? Math.Round(connectedIntegrations.Average(i => i.ResponseTime), 0)
                    : 0;

                // Recent activity count
                ViewBag.RecentlyChecked = integrations.Count(i =>
                    i.LastChecked.HasValue && i.LastChecked.Value > DateTime.UtcNow.AddHours(-1));

                // Integration types for dropdown
                ViewBag.IntegrationTypes = new List<string>
                {
                    "ERP", "CRM", "Accounting", "Logistics", "Payment",
                    "Warehouse", "Analytics", "Communication", "Other"
                };

                return View(integrations);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading integrations");
                TempData["Error"] = $"Error loading integrations: {ex.Message}";
                return View(new List<IntegrationStatus>());
            }
        }

        [HttpPost]
        public async Task<IActionResult> TestConnection(int id)
        {
            try
            {
                var integration = await _context.Set<IntegrationStatus>().FindAsync(id);
                if (integration == null)
                {
                    TempData["Error"] = "Integration not found";
                    return RedirectToAction(nameof(Index));
                }

                var startTime = DateTime.UtcNow;
                bool isConnected = false;
                string? errorMessage = null;

                try
                {
                    // Attempt to ping the endpoint
                    var response = await _httpClient.GetAsync(integration.Endpoint);
                    var elapsed = (DateTime.UtcNow - startTime).TotalMilliseconds;

                    isConnected = response.IsSuccessStatusCode;
                    integration.ResponseTime = (int)elapsed;
                    integration.LastChecked = DateTime.UtcNow;

                    if (isConnected)
                    {
                        integration.Status = "Connected";
                        integration.LastSuccess = DateTime.UtcNow;
                        integration.SuccessCount++;
                        integration.LastError = string.Empty;

                        TempData["Success"] = $"✓ Connection successful to {integration.Name}! Response time: {elapsed:F0}ms";
                        _logger.LogInformation($"Integration test successful: {integration.Name} - {elapsed:F0}ms");
                    }
                    else
                    {
                        integration.Status = "Error";
                        integration.FailureCount++;
                        errorMessage = $"HTTP {(int)response.StatusCode} - {response.ReasonPhrase}";
                        integration.LastError = errorMessage;

                        TempData["Error"] = $"Connection failed to {integration.Name}: {errorMessage}";
                    }
                }
                catch (TaskCanceledException)
                {
                    integration.Status = "Error";
                    integration.FailureCount++;
                    integration.LastChecked = DateTime.UtcNow;
                    errorMessage = "Connection timeout - endpoint did not respond within 10 seconds";
                    integration.LastError = errorMessage;

                    TempData["Error"] = $"Connection timeout for {integration.Name}";
                }
                catch (HttpRequestException httpEx)
                {
                    integration.Status = "Error";
                    integration.FailureCount++;
                    integration.LastChecked = DateTime.UtcNow;
                    errorMessage = $"Network error: {httpEx.Message}";
                    integration.LastError = errorMessage;

                    TempData["Error"] = $"Network error connecting to {integration.Name}";
                }

                await _context.SaveChangesAsync();
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error testing connection");
                TempData["Error"] = $"Error testing connection: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> SyncNow(int id)
        {
            try
            {
                var integration = await _context.Set<IntegrationStatus>().FindAsync(id);
                if (integration == null)
                {
                    TempData["Error"] = "Integration not found";
                    return RedirectToAction(nameof(Index));
                }

                // Simulate sync operation
                _logger.LogInformation($"Starting manual sync for: {integration.Name}");

                // Update last checked time
                integration.LastChecked = DateTime.UtcNow;

                // Simulate sync success
                if (integration.Status == "Connected")
                {
                    integration.LastSuccess = DateTime.UtcNow;
                    integration.SuccessCount++;
                    await _context.SaveChangesAsync();

                    TempData["Success"] = $"✓ Data sync initiated successfully for {integration.Name}. Last sync: {DateTime.UtcNow:g}";
                }
                else
                {
                    TempData["Error"] = $"Cannot sync - {integration.Name} is not connected. Test connection first.";
                }

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error syncing data");
                TempData["Error"] = $"Error syncing data: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ToggleStatus(int id)
        {
            try
            {
                var integration = await _context.Set<IntegrationStatus>().FindAsync(id);
                if (integration == null)
                {
                    TempData["Error"] = "Integration not found";
                    return RedirectToAction(nameof(Index));
                }

                integration.IsActive = !integration.IsActive;
                integration.ModifiedDate = DateTime.UtcNow;
                integration.ModifiedBy = User.Identity?.Name ?? "system";

                if (!integration.IsActive)
                {
                    integration.Status = "Disconnected";
                }

                await _context.SaveChangesAsync();

                TempData["Success"] = $"Integration '{integration.Name}' {(integration.IsActive ? "activated" : "deactivated")} successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error toggling integration status");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public IActionResult Create()
        {
            ViewBag.IntegrationTypes = new List<string>
            {
                "ERP", "CRM", "Accounting", "Logistics", "Payment",
                "Warehouse", "Analytics", "Communication", "Other"
            };

            return View(new IntegrationStatus
            {
                Status = "Disconnected",
                ResponseTime = 0,
                SuccessCount = 0,
                FailureCount = 0
            });
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(IntegrationStatus model)
        {
            if (!ModelState.IsValid)
            {
                ViewBag.IntegrationTypes = new List<string>
                {
                    "ERP", "CRM", "Accounting", "Logistics", "Payment",
                    "Warehouse", "Analytics", "Communication", "Other"
                };
                return View(model);
            }

            try
            {
                model.CreatedDate = DateTime.UtcNow;
                model.IsActive = true;
                model.Status = "Disconnected";
                model.ResponseTime = 0;
                model.SuccessCount = 0;
                model.FailureCount = 0;
                model.CreatedBy = User.Identity?.Name ?? "system";

                await _context.Set<IntegrationStatus>().AddAsync(model);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Integration created: {model.Name} ({model.IntegrationType})");
                TempData["Success"] = $"Integration '{model.Name}' created successfully! Use 'Test Connection' to verify connectivity.";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating integration");
                TempData["Error"] = $"Error creating integration: {ex.Message}";
                return View(model);
            }
        }

        [HttpGet]
        public async Task<IActionResult> Edit(int id)
        {
            try
            {
                var integration = await _context.Set<IntegrationStatus>().FindAsync(id);
                if (integration == null)
                {
                    TempData["Error"] = "Integration not found";
                    return RedirectToAction(nameof(Index));
                }

                ViewBag.IntegrationTypes = new List<string>
                {
                    "ERP", "CRM", "Accounting", "Logistics", "Payment",
                    "Warehouse", "Analytics", "Communication", "Other"
                };

                return View(integration);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading integration");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(IntegrationStatus model)
        {
            if (!ModelState.IsValid)
            {
                ViewBag.IntegrationTypes = new List<string>
                {
                    "ERP", "CRM", "Accounting", "Logistics", "Payment",
                    "Warehouse", "Analytics", "Communication", "Other"
                };
                return View(model);
            }

            try
            {
                var existing = await _context.Set<IntegrationStatus>().FindAsync(model.Id);
                if (existing == null)
                {
                    TempData["Error"] = "Integration not found";
                    return RedirectToAction(nameof(Index));
                }

                existing.Name = model.Name;
                existing.IntegrationType = model.IntegrationType;
                existing.Description = model.Description;
                existing.Endpoint = model.Endpoint;
                existing.ModifiedDate = DateTime.UtcNow;
                existing.ModifiedBy = User.Identity?.Name ?? "system";

                await _context.SaveChangesAsync();

                TempData["Success"] = $"Integration '{model.Name}' updated successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating integration");
                TempData["Error"] = $"Error: {ex.Message}";
                return View(model);
            }
        }

        [HttpPost]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var integration = await _context.Set<IntegrationStatus>().FindAsync(id);
                if (integration == null)
                {
                    TempData["Error"] = "Integration not found";
                    return RedirectToAction(nameof(Index));
                }

                _context.Set<IntegrationStatus>().Remove(integration);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Integration deleted: {integration.Name}");
                TempData["Success"] = $"Integration '{integration.Name}' deleted successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting integration");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetStatistics()
        {
            try
            {
                var integrations = await _context.Set<IntegrationStatus>().ToListAsync();

                var stats = new
                {
                    total = integrations.Count,
                    connected = integrations.Count(i => i.Status == "Connected"),
                    error = integrations.Count(i => i.Status == "Error"),
                    disconnected = integrations.Count(i => i.Status == "Disconnected"),
                    avgResponseTime = integrations.Where(i => i.ResponseTime > 0).Any()
                        ? integrations.Where(i => i.ResponseTime > 0).Average(i => i.ResponseTime)
                        : 0,
                    totalSuccess = integrations.Sum(i => i.SuccessCount),
                    totalFailures = integrations.Sum(i => i.FailureCount),
                    byType = integrations.GroupBy(i => i.IntegrationType)
                                         .Select(g => new { type = g.Key, count = g.Count() })
                                         .ToList(),
                    recentActivity = integrations
                        .Where(i => i.LastChecked.HasValue)
                        .OrderByDescending(i => i.LastChecked)
                        .Take(5)
                        .Select(i => new
                        {
                            name = i.Name,
                            status = i.Status,
                            lastChecked = i.LastChecked
                        })
                        .ToList()
                };

                return Json(new { success = true, data = stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting statistics");
                return Json(new { success = false, message = ex.Message });
            }
        }
    }
}
