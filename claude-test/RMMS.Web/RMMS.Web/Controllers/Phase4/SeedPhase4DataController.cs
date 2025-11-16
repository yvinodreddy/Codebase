using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.API;
using RMMS.Models.Mobile;
using RMMS.Models.Monitoring;
using System.Security.Cryptography;
using System.Text;

namespace RMMS.Web.Controllers.Phase4
{
    [AllowAnonymous] // For easy access during development
    public class SeedPhase4DataController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<SeedPhase4DataController> _logger;

        public SeedPhase4DataController(ApplicationDbContext context, ILogger<SeedPhase4DataController> logger)
        {
            _context = context;
            _logger = logger;
        }

        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> SeedAll()
        {
            try
            {
                var report = new List<string>();

                // Clear existing Phase 4 data
                _context.Set<ApiKey>().RemoveRange(_context.Set<ApiKey>());
                _context.Set<Webhook>().RemoveRange(_context.Set<Webhook>());
                _context.PushNotifications.RemoveRange(_context.PushNotifications);
                _context.MobileDevices.RemoveRange(_context.MobileDevices);
                _context.Set<MobileAnalyticsEvent>().RemoveRange(_context.Set<MobileAnalyticsEvent>());
                _context.Set<RealtimeMetric>().RemoveRange(_context.Set<RealtimeMetric>());
                await _context.SaveChangesAsync();
                report.Add("✅ Cleared existing Phase 4 data");

                // Seed API Keys
                await SeedApiKeys();
                report.Add("✅ Seeded 4 API Keys (with 199%+ utilization)");

                // Seed Webhooks
                await SeedWebhooks();
                report.Add("✅ Seeded 5 Webhooks");

                // Seed Mobile Devices
                await SeedMobileDevices();
                report.Add("✅ Seeded 7 Mobile Devices (4 Android, 3 iOS)");

                // Seed Push Notifications
                await SeedPushNotifications();
                report.Add("✅ Seeded 9 Push Notifications");

                // Seed Analytics Events
                await SeedAnalyticsEvents();
                report.Add("✅ Seeded 50 Mobile Analytics Events");

                // Seed Realtime Metrics
                await SeedRealtimeMetrics();
                report.Add("✅ Seeded 30 Realtime Metrics");

                TempData["Success"] = string.Join("<br/>", report) + "<br/><br/>🎉 All Phase 4 data seeded successfully!";
                _logger.LogInformation("Phase 4 data seeded successfully");
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error seeding Phase 4 data");
                TempData["Error"] = $"Error seeding data: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        private async Task SeedApiKeys()
        {
            var apiKeys = new List<ApiKey>
            {
                new ApiKey
                {
                    Name = "Production API Key",
                    Description = "Main production API access",
                    KeyValue = HashApiKey("rmms_prod_key_12345"),
                    RateLimit = 10000,
                    RequestCount = 9500, // 95% utilization
                    IsActive = true,
                    Permissions = "read,write,delete",
                    CreatedDate = DateTime.Now.AddDays(-30),
                    CreatedBy = "admin",
                    LastUsed = DateTime.Now.AddHours(-2)
                },
                new ApiKey
                {
                    Name = "Mobile App Key",
                    Description = "Mobile application API access",
                    KeyValue = HashApiKey("rmms_mobile_key_67890"),
                    RateLimit = 5000,
                    RequestCount = 12715, // 254.3% over limit!
                    IsActive = true,
                    Permissions = "read,write",
                    CreatedDate = DateTime.Now.AddDays(-20),
                    CreatedBy = "admin",
                    LastUsed = DateTime.Now.AddMinutes(-15)
                },
                new ApiKey
                {
                    Name = "Analytics Key",
                    Description = "Data analytics and reporting",
                    KeyValue = HashApiKey("rmms_analytics_key_abc"),
                    RateLimit = 2000,
                    RequestCount = 4560, // 228% over limit!
                    IsActive = true,
                    Permissions = "read",
                    CreatedDate = DateTime.Now.AddDays(-15),
                    CreatedBy = "admin",
                    LastUsed = DateTime.Now.AddHours(-1)
                },
                new ApiKey
                {
                    Name = "Test Key",
                    Description = "Development and testing",
                    KeyValue = HashApiKey("rmms_test_key_xyz"),
                    RateLimit = 1000,
                    RequestCount = 0, // 0% utilization
                    IsActive = false,
                    Permissions = "read",
                    CreatedDate = DateTime.Now.AddDays(-5),
                    CreatedBy = "developer",
                    ExpiresAt = DateTime.Now.AddDays(30)
                }
            };

            await _context.Set<ApiKey>().AddRangeAsync(apiKeys);
            await _context.SaveChangesAsync();
        }

        private async Task SeedWebhooks()
        {
            var webhooks = new List<Webhook>
            {
                new Webhook
                {
                    Name = "Order Created Webhook",
                    Description = "Notification when new orders are created",
                    Url = "https://api.example.com/webhooks/order-created",
                    EventType = "order.created",
                    Method = "POST",
                    IsActive = true,
                    RetryCount = 3,
                    TimeoutSeconds = 30,
                    CreatedDate = DateTime.UtcNow.AddDays(-10),
                    CreatedBy = "admin",
                    LastTriggered = DateTime.UtcNow.AddHours(-3)
                },
                new Webhook
                {
                    Name = "Production Batch Completed",
                    Description = "Alert when production batches complete",
                    Url = "https://api.example.com/webhooks/batch-complete",
                    EventType = "production.batch.completed",
                    Method = "POST",
                    IsActive = true,
                    RetryCount = 5,
                    TimeoutSeconds = 60,
                    CreatedDate = DateTime.UtcNow.AddDays(-8),
                    CreatedBy = "admin",
                    LastTriggered = DateTime.UtcNow.AddHours(-1)
                },
                new Webhook
                {
                    Name = "Low Stock Alert",
                    Description = "Notification for low inventory levels",
                    Url = "https://api.example.com/webhooks/low-stock",
                    EventType = "inventory.low_stock",
                    Method = "POST",
                    IsActive = true,
                    RetryCount = 3,
                    TimeoutSeconds = 30,
                    CreatedDate = DateTime.UtcNow.AddDays(-5),
                    CreatedBy = "admin",
                    LastTriggered = DateTime.UtcNow.AddDays(-1)
                },
                new Webhook
                {
                    Name = "Payment Received",
                    Description = "Customer payment notifications",
                    Url = "https://api.example.com/webhooks/payment",
                    EventType = "payment.received",
                    Method = "POST",
                    IsActive = true,
                    RetryCount = 3,
                    TimeoutSeconds = 30,
                    CreatedDate = DateTime.UtcNow.AddDays(-3),
                    CreatedBy = "admin",
                    LastTriggered = DateTime.UtcNow.AddHours(-6)
                },
                new Webhook
                {
                    Name = "Inactive Webhook",
                    Description = "Currently paused webhook",
                    Url = "https://api.example.com/webhooks/inactive",
                    EventType = "customer.created",
                    Method = "POST",
                    IsActive = false,
                    RetryCount = 3,
                    TimeoutSeconds = 30,
                    CreatedDate = DateTime.UtcNow.AddDays(-1),
                    CreatedBy = "admin"
                }
            };

            await _context.Set<Webhook>().AddRangeAsync(webhooks);
            await _context.SaveChangesAsync();
        }

        private async Task SeedMobileDevices()
        {
            var devices = new List<MobileDevice>
            {
                // Android devices
                new MobileDevice
                {
                    UserId = "user1",
                    DeviceId = "android-device-001",
                    Platform = "Android",
                    DeviceModel = "Samsung Galaxy S23",
                    OSVersion = "14.0",
                    AppVersion = "1.2.0",
                    PushToken = "fcm-token-android-001",
                    Language = "en-US",
                    NotificationsEnabled = true,
                    BiometricEnabled = true,
                    LastActiveAt = DateTime.UtcNow.AddMinutes(-10),
                    RegisteredAt = DateTime.UtcNow.AddDays(-30),
                    IsActive = true
                },
                new MobileDevice
                {
                    UserId = "user2",
                    DeviceId = "android-device-002",
                    Platform = "Android",
                    DeviceModel = "Google Pixel 8",
                    OSVersion = "14.0",
                    AppVersion = "1.2.0",
                    PushToken = "fcm-token-android-002",
                    Language = "en-US",
                    NotificationsEnabled = true,
                    BiometricEnabled = false,
                    LastActiveAt = DateTime.UtcNow.AddHours(-2),
                    RegisteredAt = DateTime.UtcNow.AddDays(-25),
                    IsActive = true
                },
                new MobileDevice
                {
                    UserId = "user3",
                    DeviceId = "android-device-003",
                    Platform = "Android",
                    DeviceModel = "OnePlus 11",
                    OSVersion = "13.0",
                    AppVersion = "1.1.0",
                    PushToken = "fcm-token-android-003",
                    Language = "es-ES",
                    NotificationsEnabled = false,
                    BiometricEnabled = true,
                    LastActiveAt = DateTime.UtcNow.AddDays(-5),
                    RegisteredAt = DateTime.UtcNow.AddDays(-20),
                    IsActive = true
                },
                // iOS devices
                new MobileDevice
                {
                    UserId = "user4",
                    DeviceId = "ios-device-001",
                    Platform = "iOS",
                    DeviceModel = "iPhone 15 Pro",
                    OSVersion = "17.1",
                    AppVersion = "1.2.0",
                    PushToken = "apns-token-ios-001",
                    Language = "en-US",
                    NotificationsEnabled = true,
                    BiometricEnabled = true,
                    LastActiveAt = DateTime.UtcNow.AddMinutes(-30),
                    RegisteredAt = DateTime.UtcNow.AddDays(-28),
                    IsActive = true
                },
                new MobileDevice
                {
                    UserId = "user5",
                    DeviceId = "ios-device-002",
                    Platform = "iOS",
                    DeviceModel = "iPhone 14",
                    OSVersion = "17.0",
                    AppVersion = "1.2.0",
                    PushToken = "apns-token-ios-002",
                    Language = "en-GB",
                    NotificationsEnabled = true,
                    BiometricEnabled = true,
                    LastActiveAt = DateTime.UtcNow.AddHours(-1),
                    RegisteredAt = DateTime.UtcNow.AddDays(-15),
                    IsActive = true
                },
                new MobileDevice
                {
                    UserId = "user6",
                    DeviceId = "ios-device-003",
                    Platform = "iOS",
                    DeviceModel = "iPad Pro 12.9",
                    OSVersion = "17.1",
                    AppVersion = "1.2.0",
                    PushToken = "apns-token-ios-003",
                    Language = "fr-FR",
                    NotificationsEnabled = true,
                    BiometricEnabled = false,
                    LastActiveAt = DateTime.UtcNow.AddDays(-2),
                    RegisteredAt = DateTime.UtcNow.AddDays(-10),
                    IsActive = true
                },
                // Inactive device
                new MobileDevice
                {
                    UserId = "user7",
                    DeviceId = "android-device-old",
                    Platform = "Android",
                    DeviceModel = "Samsung Galaxy S20",
                    OSVersion = "12.0",
                    AppVersion = "1.0.0",
                    PushToken = "fcm-token-old",
                    Language = "en-US",
                    NotificationsEnabled = false,
                    BiometricEnabled = false,
                    LastActiveAt = DateTime.UtcNow.AddDays(-60),
                    RegisteredAt = DateTime.UtcNow.AddDays(-90),
                    IsActive = false
                }
            };

            await _context.MobileDevices.AddRangeAsync(devices);
            await _context.SaveChangesAsync();
        }

        private async Task SeedPushNotifications()
        {
            var devices = await _context.MobileDevices.ToListAsync();
            var notifications = new List<PushNotification>
            {
                new PushNotification
                {
                    Name = "Production Alert 1",
                    Title = "Production Complete",
                    Body = "Batch #12345 has completed processing",
                    UserId = "user1",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user1")?.Id,
                    Type = "production",
                    Priority = "high",
                    Status = "sent",
                    CreatedAt = DateTime.UtcNow.AddHours(-2),
                    SentAt = DateTime.UtcNow.AddHours(-2),
                    IsRead = true,
                    ReadAt = DateTime.UtcNow.AddHours(-1),
                    AttemptCount = 1
                },
                new PushNotification
                {
                    Name = "Sales Notification",
                    Title = "New Order Received",
                    Body = "Order #98765 has been placed",
                    UserId = "user2",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user2")?.Id,
                    Type = "sales",
                    Priority = "normal",
                    Status = "delivered",
                    CreatedAt = DateTime.UtcNow.AddHours(-5),
                    SentAt = DateTime.UtcNow.AddHours(-5),
                    IsRead = true,
                    ReadAt = DateTime.UtcNow.AddHours(-4),
                    AttemptCount = 1
                },
                new PushNotification
                {
                    Name = "Inventory Alert",
                    Title = "Low Stock Warning",
                    Body = "Rice variety XYZ is running low",
                    UserId = "user4",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user4")?.Id,
                    Type = "inventory",
                    Priority = "high",
                    Status = "sent",
                    CreatedAt = DateTime.UtcNow.AddHours(-8),
                    SentAt = DateTime.UtcNow.AddHours(-8),
                    IsRead = false,
                    AttemptCount = 1
                },
                new PushNotification
                {
                    Name = "Payment Alert",
                    Title = "Payment Received",
                    Body = "Payment of $5,000 received",
                    UserId = "user1",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user1")?.Id,
                    Type = "payment",
                    Priority = "normal",
                    Status = "sent",
                    CreatedAt = DateTime.UtcNow.AddHours(-1),
                    SentAt = DateTime.UtcNow.AddHours(-1),
                    IsRead = true,
                    ReadAt = DateTime.UtcNow.AddMinutes(-30),
                    AttemptCount = 1
                },
                new PushNotification
                {
                    Name = "Quality Check",
                    Title = "Quality Inspection Due",
                    Body = "Batch #12346 requires inspection",
                    UserId = "user2",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user2")?.Id,
                    Type = "quality",
                    Priority = "normal",
                    Status = "delivered",
                    CreatedAt = DateTime.UtcNow.AddHours(-3),
                    SentAt = DateTime.UtcNow.AddHours(-3),
                    IsRead = false,
                    AttemptCount = 1
                },
                new PushNotification
                {
                    Name = "Weekly Report",
                    Title = "Weekly Summary Ready",
                    Body = "Your weekly report is ready to view",
                    UserId = "user5",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user5")?.Id,
                    Type = "report",
                    Priority = "low",
                    Status = "sent",
                    CreatedAt = DateTime.UtcNow.AddDays(-2),
                    SentAt = DateTime.UtcNow.AddDays(-2),
                    IsRead = true,
                    ReadAt = DateTime.UtcNow.AddDays(-1),
                    AttemptCount = 1
                },
                new PushNotification
                {
                    Name = "System Update",
                    Title = "App Update Available",
                    Body = "New version 1.3.0 is available",
                    UserId = "user4",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user4")?.Id,
                    Type = "system",
                    Priority = "normal",
                    Status = "sent",
                    CreatedAt = DateTime.UtcNow.AddDays(-3),
                    SentAt = DateTime.UtcNow.AddDays(-3),
                    IsRead = false,
                    AttemptCount = 1
                },
                new PushNotification
                {
                    Name = "Scheduled Alert",
                    Title = "Scheduled Maintenance",
                    Body = "System maintenance tonight at 10 PM",
                    UserId = "user1",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user1")?.Id,
                    Type = "system",
                    Priority = "normal",
                    Status = "pending",
                    CreatedAt = DateTime.UtcNow,
                    IsRead = false,
                    AttemptCount = 0
                },
                new PushNotification
                {
                    Name = "Failed Delivery",
                    Title = "Test Notification",
                    Body = "This notification failed to deliver",
                    UserId = "user3",
                    DeviceId = devices.FirstOrDefault(d => d.UserId == "user3")?.Id,
                    Type = "test",
                    Priority = "low",
                    Status = "failed",
                    CreatedAt = DateTime.UtcNow.AddHours(-12),
                    ErrorMessage = "Device token invalid",
                    IsRead = false,
                    AttemptCount = 3
                }
            };

            await _context.PushNotifications.AddRangeAsync(notifications);
            await _context.SaveChangesAsync();
        }

        private async Task SeedAnalyticsEvents()
        {
            var events = new List<MobileAnalyticsEvent>();
            var random = new Random();
            var categories = new[] { "screen_view", "button_click", "performance", "error", "user_action" };
            var actions = new[] { "view", "click", "load_time", "exception", "submit" };
            var screens = new[] { "Dashboard", "Production", "Sales", "Inventory", "Reports", "Settings" };
            var platforms = new[] { "Android", "iOS" };

            for (int i = 0; i < 50; i++)
            {
                events.Add(new MobileAnalyticsEvent
                {
                    UserId = $"user{(i % 6) + 1}",
                    DeviceId = (i % 6) + 1,
                    Category = categories[i % categories.Length],
                    Action = actions[i % actions.Length],
                    Label = $"Event {i}",
                    Screen = screens[i % screens.Length],
                    Value = random.Next(100, 1000),
                    Platform = platforms[i % platforms.Length],
                    AppVersion = "1.2.0",
                    ServerTimestamp = DateTime.UtcNow.AddMinutes(-(i * 10)),
                    ClientTimestamp = DateTime.UtcNow.AddMinutes(-(i * 10))
                });
            }

            await _context.Set<MobileAnalyticsEvent>().AddRangeAsync(events);
            await _context.SaveChangesAsync();
        }

        private async Task SeedRealtimeMetrics()
        {
            var metrics = new List<RealtimeMetric>();
            var random = new Random();
            var metricTypes = new[] { "api_latency", "db_query_time", "memory_usage", "cpu_usage" };

            for (int i = 0; i < 30; i++)
            {
                metrics.Add(new RealtimeMetric
                {
                    MetricType = metricTypes[i % metricTypes.Length],
                    Value = random.Next(10, 100),
                    CreatedDate = DateTime.Now.AddMinutes(-i),
                    IsActive = true
                });
            }

            await _context.Set<RealtimeMetric>().AddRangeAsync(metrics);
            await _context.SaveChangesAsync();
        }

        private string HashApiKey(string apiKey)
        {
            using (var sha256 = SHA256.Create())
            {
                var hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(apiKey));
                return Convert.ToBase64String(hashBytes);
            }
        }
    }
}
