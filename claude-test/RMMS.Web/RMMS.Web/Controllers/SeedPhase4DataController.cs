using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.API;
using RMMS.Models.Mobile;
using System.Text;

namespace RMMS.Web.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SeedPhase4DataController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<SeedPhase4DataController> _logger;

        public SeedPhase4DataController(ApplicationDbContext context, ILogger<SeedPhase4DataController> logger)
        {
            _context = context;
            _logger = logger;
        }

        [HttpPost("seed-all")]
        public async Task<IActionResult> SeedAllPhase4Data()
        {
            try
            {
                var results = new StringBuilder();
                results.AppendLine("=== PHASE 4 DATA SEEDING STARTED ===\n");

                // 1. Seed Webhooks
                await SeedWebhooks(results);

                // 2. Seed Integration Status
                await SeedIntegrationStatus(results);

                // 3. Seed API Keys
                await SeedApiKeys(results);

                // 4. Seed Mobile Devices
                await SeedMobileDevices(results);

                // 5. Seed API Request Logs
                await SeedApiRequestLogs(results);

                // 6. Seed Mobile Analytics Events
                await SeedMobileAnalyticsEvents(results);

                results.AppendLine("\n=== PHASE 4 DATA SEEDING COMPLETED SUCCESSFULLY ===");

                _logger.LogInformation("Phase 4 data seeding completed");

                return Ok(new { success = true, message = results.ToString() });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error seeding Phase 4 data");
                return StatusCode(500, new { success = false, message = ex.Message });
            }
        }

        private async Task SeedWebhooks(StringBuilder results)
        {
            if (!await _context.Set<Webhook>().AnyAsync())
            {
                var webhooks = new List<Webhook>
                {
                    new Webhook
                    {
                        Name = "Production Alerts Webhook",
                        Url = "https://hooks.example.com/production",
                        Description = "Receives production batch completion notifications",
                        EventType = "production.batch.completed",
                        Method = "POST",
                        IsActive = true,
                        RetryCount = 3,
                        TimeoutSeconds = 30,
                        LastTriggered = DateTime.UtcNow.AddHours(-2),
                        CreatedDate = DateTime.UtcNow.AddDays(-10),
                        CreatedBy = "admin"
                    },
                    new Webhook
                    {
                        Name = "Order Notifications",
                        Url = "https://hooks.example.com/orders",
                        Description = "Notifies external system of new orders",
                        EventType = "order.created",
                        Method = "POST",
                        IsActive = true,
                        RetryCount = 5,
                        TimeoutSeconds = 60,
                        LastTriggered = DateTime.UtcNow.AddMinutes(-30),
                        CreatedDate = DateTime.UtcNow.AddDays(-15),
                        CreatedBy = "admin"
                    },
                    new Webhook
                    {
                        Name = "Inventory Low Stock Alert",
                        Url = "https://hooks.example.com/inventory",
                        Description = "Alerts when inventory falls below threshold",
                        EventType = "inventory.low_stock",
                        Method = "POST",
                        IsActive = true,
                        RetryCount = 3,
                        TimeoutSeconds = 30,
                        LastTriggered = DateTime.UtcNow.AddHours(-5),
                        CreatedDate = DateTime.UtcNow.AddDays(-20),
                        CreatedBy = "system"
                    },
                    new Webhook
                    {
                        Name = "Payment Received Webhook",
                        Url = "https://hooks.example.com/payments",
                        Description = "Notifies accounting system of payments",
                        EventType = "payment.received",
                        Method = "POST",
                        IsActive = false,
                        RetryCount = 5,
                        TimeoutSeconds = 45,
                        CreatedDate = DateTime.UtcNow.AddDays(-5),
                        CreatedBy = "admin"
                    },
                    new Webhook
                    {
                        Name = "All Events Monitor",
                        Url = "https://monitor.example.com/rmms",
                        Description = "Monitors all system events",
                        EventType = "*",
                        Method = "POST",
                        IsActive = true,
                        RetryCount = 1,
                        TimeoutSeconds = 120,
                        LastTriggered = DateTime.UtcNow.AddMinutes(-5),
                        CreatedDate = DateTime.UtcNow.AddDays(-30),
                        CreatedBy = "admin"
                    }
                };

                await _context.Set<Webhook>().AddRangeAsync(webhooks);
                await _context.SaveChangesAsync();
                results.AppendLine($"✓ Seeded {webhooks.Count} webhooks");
            }
            else
            {
                results.AppendLine("✓ Webhooks already exist - skipping");
            }
        }

        private async Task SeedIntegrationStatus(StringBuilder results)
        {
            if (!await _context.Set<IntegrationStatus>().AnyAsync())
            {
                var integrations = new List<IntegrationStatus>
                {
                    new IntegrationStatus
                    {
                        Name = "SAP ERP Integration",
                        IntegrationType = "ERP",
                        Description = "Enterprise Resource Planning integration",
                        Endpoint = "https://sap.example.com/api",
                        Status = "Connected",
                        IsActive = true,
                        LastChecked = DateTime.UtcNow.AddMinutes(-10),
                        LastSuccess = DateTime.UtcNow.AddMinutes(-10),
                        SuccessCount = 1250,
                        FailureCount = 3,
                        ResponseTime = 245,
                        CreatedDate = DateTime.UtcNow.AddDays(-90),
                        CreatedBy = "admin"
                    },
                    new IntegrationStatus
                    {
                        Name = "Salesforce CRM",
                        IntegrationType = "CRM",
                        Description = "Customer Relationship Management integration",
                        Endpoint = "https://api.salesforce.com",
                        Status = "Connected",
                        IsActive = true,
                        LastChecked = DateTime.UtcNow.AddMinutes(-5),
                        LastSuccess = DateTime.UtcNow.AddMinutes(-5),
                        SuccessCount = 892,
                        FailureCount = 1,
                        ResponseTime = 180,
                        CreatedDate = DateTime.UtcNow.AddDays(-60),
                        CreatedBy = "admin"
                    },
                    new IntegrationStatus
                    {
                        Name = "QuickBooks Accounting",
                        IntegrationType = "Accounting",
                        Description = "Financial system integration",
                        Endpoint = "https://api.quickbooks.com",
                        Status = "Error",
                        IsActive = true,
                        LastChecked = DateTime.UtcNow.AddHours(-1),
                        LastSuccess = DateTime.UtcNow.AddDays(-2),
                        LastError = "Authentication failed - Token expired",
                        SuccessCount = 445,
                        FailureCount = 12,
                        ResponseTime = 520,
                        CreatedDate = DateTime.UtcNow.AddDays(-45),
                        CreatedBy = "admin"
                    },
                    new IntegrationStatus
                    {
                        Name = "Shipping Provider API",
                        IntegrationType = "Logistics",
                        Description = "Shipping and logistics integration",
                        Endpoint = "https://api.fedex.com",
                        Status = "Connected",
                        IsActive = true,
                        LastChecked = DateTime.UtcNow.AddMinutes(-15),
                        LastSuccess = DateTime.UtcNow.AddMinutes(-15),
                        SuccessCount = 2103,
                        FailureCount = 5,
                        ResponseTime = 312,
                        CreatedDate = DateTime.UtcNow.AddDays(-120),
                        CreatedBy = "system"
                    },
                    new IntegrationStatus
                    {
                        Name = "Payment Gateway",
                        IntegrationType = "Payment",
                        Description = "Payment processing integration",
                        Endpoint = "https://api.stripe.com",
                        Status = "Disconnected",
                        IsActive = false,
                        LastChecked = DateTime.UtcNow.AddDays(-7),
                        LastSuccess = DateTime.UtcNow.AddDays(-7),
                        LastError = "Manually disabled for maintenance",
                        SuccessCount = 678,
                        FailureCount = 0,
                        ResponseTime = 0,
                        CreatedDate = DateTime.UtcNow.AddDays(-180),
                        CreatedBy = "admin"
                    }
                };

                await _context.Set<IntegrationStatus>().AddRangeAsync(integrations);
                await _context.SaveChangesAsync();
                results.AppendLine($"✓ Seeded {integrations.Count} integration statuses");
            }
            else
            {
                results.AppendLine("✓ Integration statuses already exist - skipping");
            }
        }

        private async Task SeedApiKeys(StringBuilder results)
        {
            if (!await _context.Set<ApiKey>().AnyAsync())
            {
                var apiKeys = new List<ApiKey>
                {
                    new ApiKey
                    {
                        Name = "Mobile App - Production",
                        KeyValue = GenerateApiKey(),
                        Description = "API key for production mobile application",
                        Permissions = "read:production,write:orders,read:inventory",
                        UserId = "mobile_app",
                        IsActive = true,
                        ExpiresAt = DateTime.UtcNow.AddMonths(6),
                        LastUsed = DateTime.UtcNow.AddMinutes(-5),
                        RequestCount = 45678,
                        RateLimit = 10000,
                        CreatedDate = DateTime.UtcNow.AddDays(-60),
                        CreatedBy = "admin"
                    },
                    new ApiKey
                    {
                        Name = "Web Dashboard",
                        KeyValue = GenerateApiKey(),
                        Description = "API key for web dashboard application",
                        Permissions = "read:*,write:*",
                        UserId = "web_dashboard",
                        IsActive = true,
                        ExpiresAt = DateTime.UtcNow.AddYears(1),
                        LastUsed = DateTime.UtcNow.AddMinutes(-2),
                        RequestCount = 123456,
                        RateLimit = 50000,
                        CreatedDate = DateTime.UtcNow.AddDays(-90),
                        CreatedBy = "admin"
                    },
                    new ApiKey
                    {
                        Name = "Third-Party Integration",
                        KeyValue = GenerateApiKey(),
                        Description = "API key for third-party system integration",
                        Permissions = "read:orders,read:customers",
                        UserId = "3rdparty",
                        IsActive = true,
                        ExpiresAt = DateTime.UtcNow.AddMonths(3),
                        LastUsed = DateTime.UtcNow.AddHours(-1),
                        RequestCount = 8912,
                        RateLimit = 1000,
                        CreatedDate = DateTime.UtcNow.AddDays(-30),
                        CreatedBy = "system"
                    },
                    new ApiKey
                    {
                        Name = "Development Testing",
                        KeyValue = GenerateApiKey(),
                        Description = "Temporary key for development testing",
                        Permissions = "read:*",
                        UserId = "developer",
                        IsActive = false,
                        ExpiresAt = DateTime.UtcNow.AddDays(-5),
                        LastUsed = DateTime.UtcNow.AddDays(-6),
                        RequestCount = 234,
                        RateLimit = 100,
                        CreatedDate = DateTime.UtcNow.AddDays(-45),
                        CreatedBy = "developer"
                    }
                };

                await _context.Set<ApiKey>().AddRangeAsync(apiKeys);
                await _context.SaveChangesAsync();
                results.AppendLine($"✓ Seeded {apiKeys.Count} API keys");
            }
            else
            {
                results.AppendLine("✓ API keys already exist - skipping");
            }
        }

        private async Task SeedMobileDevices(StringBuilder results)
        {
            if (!await _context.MobileDevices.AnyAsync())
            {
                var devices = new List<MobileDevice>
                {
                    new MobileDevice
                    {
                        UserId = "user1",
                        DeviceId = Guid.NewGuid().ToString(),
                        Platform = "Android",
                        PushToken = $"fcm_token_{Guid.NewGuid()}",
                        IsActive = true,
                        NotificationsEnabled = true,
                        RegisteredAt = DateTime.UtcNow.AddDays(-30),
                        LastActiveAt = DateTime.UtcNow.AddMinutes(-10)
                    },
                    new MobileDevice
                    {
                        UserId = "user2",
                        DeviceId = Guid.NewGuid().ToString(),
                        Platform = "iOS",
                        PushToken = $"apns_token_{Guid.NewGuid()}",
                        IsActive = true,
                        NotificationsEnabled = true,
                        RegisteredAt = DateTime.UtcNow.AddDays(-45),
                        LastActiveAt = DateTime.UtcNow.AddHours(-2)
                    },
                    new MobileDevice
                    {
                        UserId = "user3",
                        DeviceId = Guid.NewGuid().ToString(),
                        Platform = "Android",
                        PushToken = $"fcm_token_{Guid.NewGuid()}",
                        IsActive = true,
                        NotificationsEnabled = false,
                        RegisteredAt = DateTime.UtcNow.AddDays(-60),
                        LastActiveAt = DateTime.UtcNow.AddDays(-5)
                    },
                    new MobileDevice
                    {
                        UserId = "user4",
                        DeviceId = Guid.NewGuid().ToString(),
                        Platform = "iOS",
                        PushToken = $"apns_token_{Guid.NewGuid()}",
                        IsActive = false,
                        NotificationsEnabled = true,
                        RegisteredAt = DateTime.UtcNow.AddDays(-90),
                        LastActiveAt = DateTime.UtcNow.AddDays(-15)
                    }
                };

                await _context.MobileDevices.AddRangeAsync(devices);
                await _context.SaveChangesAsync();
                results.AppendLine($"✓ Seeded {devices.Count} mobile devices");
            }
            else
            {
                results.AppendLine("✓ Mobile devices already exist - skipping");
            }
        }

        private async Task SeedApiRequestLogs(StringBuilder results)
        {
            // Skipping API request logs - will be generated from actual API usage
            results.AppendLine("✓ API request logs will be generated from actual usage");
            await Task.CompletedTask;
        }

        private async Task SeedMobileAnalyticsEvents(StringBuilder results)
        {
            if (!await _context.Set<MobileAnalyticsEvent>().AnyAsync())
            {
                var random = new Random();
                var categories = new[] { "navigation", "action", "error", "performance" };
                var actions = new[] { "screen_view", "button_click", "form_submit", "api_call", "error_occurred" };
                var screens = new[] { "Home", "Production", "Orders", "Inventory", "Settings", "Reports" };

                var analyticsEvents = new List<MobileAnalyticsEvent>();

                // Generate 100 sample mobile analytics events
                for (int i = 0; i < 100; i++)
                {
                    var category = categories[random.Next(categories.Length)];
                    var action = actions[random.Next(actions.Length)];
                    var screen = screens[random.Next(screens.Length)];

                    analyticsEvents.Add(new MobileAnalyticsEvent
                    {
                        UserId = $"user{random.Next(1, 10)}",
                        Category = category,
                        Action = action,
                        Label = $"{screen} - {action}",
                        Value = random.Next(0, 100),
                        Screen = screen,
                        SessionId = Guid.NewGuid().ToString(),
                        Properties = $"{{ \"screen\": \"{screen}\", \"action\": \"{action}\" }}",
                        ClientTimestamp = DateTime.UtcNow.AddHours(-random.Next(1, 720)),
                        ServerTimestamp = DateTime.UtcNow.AddHours(-random.Next(1, 720)),
                        Platform = random.Next(2) == 0 ? "Android" : "iOS",
                        AppVersion = "2.5.1"
                    });
                }

                await _context.Set<MobileAnalyticsEvent>().AddRangeAsync(analyticsEvents);
                await _context.SaveChangesAsync();
                results.AppendLine($"✓ Seeded {analyticsEvents.Count} mobile analytics events");
            }
            else
            {
                results.AppendLine("✓ Mobile analytics events already exist - skipping");
            }
        }

        private string GenerateApiKey()
        {
            // Generate a secure random API key
            var bytes = new byte[32];
            using var rng = System.Security.Cryptography.RandomNumberGenerator.Create();
            rng.GetBytes(bytes);
            return Convert.ToBase64String(bytes).Replace("+", "").Replace("/", "").Replace("=", "").Substring(0, 40);
        }
    }
}
