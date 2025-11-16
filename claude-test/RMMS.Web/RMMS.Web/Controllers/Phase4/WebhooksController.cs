using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.Services.Services.Integrations;
using RMMS.Models.API;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;

namespace RMMS.Web.Controllers.Phase4
{
    [AllowAnonymous] // Temporarily enabled for testing
    public class WebhooksController : Controller
    {
        private readonly IWebhookService _webhookService;
        private readonly ApplicationDbContext _context;
        private readonly ILogger<WebhooksController> _logger;

        public WebhooksController(
            IWebhookService webhookService,
            ApplicationDbContext context,
            ILogger<WebhooksController> logger)
        {
            _webhookService = webhookService;
            _context = context;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                // Get all webhooks with statistics
                var webhooks = await _context.Set<Webhook>()
                    .OrderByDescending(w => w.CreatedDate)
                    .ToListAsync();

                // Calculate statistics
                ViewBag.TotalWebhooks = webhooks.Count;
                ViewBag.ActiveWebhooks = webhooks.Count(w => w.IsActive);
                ViewBag.InactiveWebhooks = webhooks.Count(w => !w.IsActive);
                ViewBag.RecentlyTriggered = webhooks.Count(w => w.LastTriggered.HasValue && w.LastTriggered.Value > DateTime.Now.AddHours(-24));

                // Available event types for webhook subscription
                ViewBag.EventTypes = new List<string>
                {
                    "order.created",
                    "order.updated",
                    "order.completed",
                    "production.batch.started",
                    "production.batch.completed",
                    "inventory.low_stock",
                    "customer.created",
                    "payment.received",
                    "shipment.dispatched",
                    "*" // All events
                };

                return View(webhooks);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading webhooks");
                TempData["Error"] = $"Error loading webhooks: {ex.Message}";
                return View(new List<Webhook>());
            }
        }

        [HttpGet]
        public IActionResult Create()
        {
            ViewBag.EventTypes = new List<string>
            {
                "order.created",
                "order.updated",
                "order.completed",
                "production.batch.started",
                "production.batch.completed",
                "inventory.low_stock",
                "customer.created",
                "payment.received",
                "shipment.dispatched",
                "*"
            };

            ViewBag.Methods = new List<string> { "POST", "PUT" };

            return View(new Webhook());
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(Webhook model, string eventTypes)
        {
            if (!ModelState.IsValid)
            {
                ViewBag.EventTypes = new List<string>
                {
                    "order.created", "order.updated", "order.completed",
                    "production.batch.started", "production.batch.completed",
                    "inventory.low_stock", "customer.created", "payment.received",
                    "shipment.dispatched", "*"
                };
                return View(model);
            }

            try
            {
                // Input validation
                if (string.IsNullOrWhiteSpace(model.Name))
                {
                    TempData["Error"] = "Webhook name is required";
                    return View(model);
                }

                if (string.IsNullOrWhiteSpace(model.Url))
                {
                    TempData["Error"] = "Webhook URL is required";
                    return View(model);
                }

                // Validate URL format
                if (!Uri.TryCreate(model.Url, UriKind.Absolute, out var uriResult) ||
                    (uriResult.Scheme != Uri.UriSchemeHttp && uriResult.Scheme != Uri.UriSchemeHttps))
                {
                    TempData["Error"] = "Invalid webhook URL. Must be a valid HTTP or HTTPS URL";
                    return View(model);
                }

                // Check for duplicate names
                var existingWebhook = await _context.Set<Webhook>()
                    .FirstOrDefaultAsync(w => w.Name == model.Name);
                if (existingWebhook != null)
                {
                    TempData["Error"] = $"Webhook with name '{model.Name}' already exists";
                    return View(model);
                }

                // Validate retry count and timeout
                if (model.RetryCount < 0 || model.RetryCount > 10)
                {
                    model.RetryCount = 3; // Default
                }

                if (model.TimeoutSeconds < 1 || model.TimeoutSeconds > 300)
                {
                    model.TimeoutSeconds = 30; // Default
                }

                model.CreatedDate = DateTime.UtcNow;
                model.IsActive = true;
                model.CreatedBy = User.Identity?.Name ?? "system";
                model.Method = string.IsNullOrEmpty(model.Method) ? "POST" : model.Method.ToUpper();
                model.EventType = eventTypes ?? "*";

                await _context.Set<Webhook>().AddAsync(model);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Webhook created: {model.Name} for events: {model.EventType}");
                TempData["Success"] = $"Webhook '{model.Name}' created successfully! Subscribed to: {model.EventType}";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating Webhook");
                TempData["Error"] = $"Error creating webhook: {ex.Message}";
                ViewBag.EventTypes = new List<string>
                {
                    "order.created", "order.updated", "order.completed",
                    "production.batch.started", "production.batch.completed",
                    "inventory.low_stock", "customer.created", "payment.received",
                    "shipment.dispatched", "*"
                };
                return View(model);
            }
        }

        [HttpPost]
        public async Task<IActionResult> TestWebhook(int id)
        {
            try
            {
                var webhook = await _context.Set<Webhook>().FindAsync(id);
                if (webhook == null)
                {
                    TempData["Error"] = "Webhook not found";
                    return RedirectToAction(nameof(Index));
                }

                // Create test payload
                var testPayload = new
                {
                    eventType = webhook.EventType,
                    timestamp = DateTime.UtcNow,
                    data = new
                    {
                        id = 12345,
                        message = "This is a test webhook delivery",
                        status = "test",
                        generatedBy = "RMMS Webhook System"
                    }
                };

                var success = await _webhookService.DeliverWebhookAsync(webhook.EventType, testPayload);

                if (success)
                {
                    webhook.LastTriggered = DateTime.UtcNow;
                    await _context.SaveChangesAsync();

                    TempData["Success"] = $"Test webhook delivered successfully to {webhook.Url}";
                    _logger.LogInformation($"Test webhook delivered to: {webhook.Name}");
                }
                else
                {
                    TempData["Error"] = "Failed to deliver test webhook. Check URL and network connectivity.";
                }

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error testing webhook");
                TempData["Error"] = $"Error testing webhook: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ToggleStatus(int id)
        {
            try
            {
                var webhook = await _context.Set<Webhook>().FindAsync(id);
                if (webhook == null)
                {
                    TempData["Error"] = "Webhook not found";
                    return RedirectToAction(nameof(Index));
                }

                webhook.IsActive = !webhook.IsActive;
                webhook.ModifiedDate = DateTime.UtcNow;
                webhook.ModifiedBy = User.Identity?.Name ?? "system";

                await _context.SaveChangesAsync();

                TempData["Success"] = $"Webhook '{webhook.Name}' {(webhook.IsActive ? "activated" : "deactivated")} successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error toggling webhook status");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> Edit(int id)
        {
            try
            {
                var webhook = await _context.Set<Webhook>().FindAsync(id);
                if (webhook == null)
                {
                    TempData["Error"] = "Webhook not found";
                    return RedirectToAction(nameof(Index));
                }

                ViewBag.EventTypes = new List<string>
                {
                    "order.created", "order.updated", "order.completed",
                    "production.batch.started", "production.batch.completed",
                    "inventory.low_stock", "customer.created", "payment.received",
                    "shipment.dispatched", "*"
                };
                ViewBag.Methods = new List<string> { "POST", "PUT" };

                return View(webhook);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading webhook");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(Webhook model)
        {
            if (!ModelState.IsValid)
            {
                ViewBag.EventTypes = new List<string>
                {
                    "order.created", "order.updated", "order.completed",
                    "production.batch.started", "production.batch.completed",
                    "inventory.low_stock", "customer.created", "payment.received",
                    "shipment.dispatched", "*"
                };
                return View(model);
            }

            try
            {
                var existing = await _context.Set<Webhook>().FindAsync(model.Id);
                if (existing == null)
                {
                    TempData["Error"] = "Webhook not found";
                    return RedirectToAction(nameof(Index));
                }

                existing.Name = model.Name;
                existing.Url = model.Url;
                existing.Description = model.Description;
                existing.EventType = model.EventType;
                existing.Method = model.Method;
                existing.Headers = model.Headers;
                existing.PayloadTemplate = model.PayloadTemplate;
                existing.RetryCount = model.RetryCount;
                existing.TimeoutSeconds = model.TimeoutSeconds;
                existing.ModifiedDate = DateTime.UtcNow;
                existing.ModifiedBy = User.Identity?.Name ?? "system";

                await _context.SaveChangesAsync();

                TempData["Success"] = $"Webhook '{model.Name}' updated successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating webhook");
                TempData["Error"] = $"Error: {ex.Message}";
                return View(model);
            }
        }

        [HttpPost]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var webhook = await _context.Set<Webhook>().FindAsync(id);
                if (webhook == null)
                {
                    TempData["Error"] = "Webhook not found";
                    return RedirectToAction(nameof(Index));
                }

                _context.Set<Webhook>().Remove(webhook);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Webhook deleted: {webhook.Name}");
                TempData["Success"] = $"Webhook '{webhook.Name}' deleted successfully";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting webhook");
                TempData["Error"] = $"Error: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetStatistics()
        {
            try
            {
                var webhooks = await _context.Set<Webhook>().ToListAsync();

                var stats = new
                {
                    total = webhooks.Count,
                    active = webhooks.Count(w => w.IsActive),
                    inactive = webhooks.Count(w => !w.IsActive),
                    triggeredToday = webhooks.Count(w => w.LastTriggered.HasValue &&
                                                         w.LastTriggered.Value.Date == DateTime.Today),
                    triggeredThisWeek = webhooks.Count(w => w.LastTriggered.HasValue &&
                                                            w.LastTriggered.Value > DateTime.Now.AddDays(-7)),
                    byEventType = webhooks.GroupBy(w => w.EventType)
                                          .Select(g => new { eventType = g.Key, count = g.Count() })
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
