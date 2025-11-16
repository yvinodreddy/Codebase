using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;
using RMMS.Models.API;
using System.Security.Cryptography;
using System.Text;

namespace RMMS.Web.Controllers.Phase4
{
    [AllowAnonymous] // Temporarily enabled for testing
    public class ApiKeysController : Controller
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<ApiKeysController> _logger;

        public ApiKeysController(
            ApplicationDbContext context,
            ILogger<ApiKeysController> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<IActionResult> Index()
        {
            try
            {
                // Query API keys from database
                var apiKeys = await _context.Set<ApiKey>()
                    .OrderByDescending(k => k.CreatedDate)
                    .ToListAsync();

                // Calculate comprehensive statistics
                var now = DateTime.Now;
                var today = DateTime.Today;
                var thisHour = now.AddHours(-1);

                ViewBag.TotalKeys = apiKeys.Count;
                ViewBag.ActiveKeys = apiKeys.Count(k => k.IsActive);
                ViewBag.InactiveKeys = apiKeys.Count(k => !k.IsActive);
                ViewBag.ExpiredKeys = apiKeys.Count(k => k.ExpiresAt.HasValue && k.ExpiresAt.Value < now);
                ViewBag.ExpiringThisWeek = apiKeys.Count(k => k.ExpiresAt.HasValue &&
                    k.ExpiresAt.Value >= now && k.ExpiresAt.Value <= now.AddDays(7));

                // Usage statistics
                ViewBag.TotalRequests = apiKeys.Sum(k => k.RequestCount);
                ViewBag.RequestsToday = apiKeys.Where(k => k.LastUsed.HasValue && k.LastUsed.Value.Date == today)
                    .Sum(k => k.RequestCount);
                ViewBag.UsedToday = apiKeys.Count(k => k.LastUsed.HasValue && k.LastUsed.Value.Date == today);

                // Rate limit analysis
                var keysNearLimit = apiKeys.Where(k => k.IsActive && k.RateLimit > 0)
                    .Select(k => new {
                        Key = k,
                        Utilization = Math.Min(100, (k.RequestCount / (double)k.RateLimit) * 100)
                    })
                    .Where(x => x.Utilization >= 80)
                    .ToList();

                ViewBag.KeysNearLimit = keysNearLimit.Count;
                ViewBag.AverageUtilization = apiKeys.Any(k => k.RateLimit > 0)
                    ? Math.Min(100, Math.Round(apiKeys.Where(k => k.RateLimit > 0)
                        .Average(k => Math.Min(100, (k.RequestCount / (double)k.RateLimit) * 100)), 1))
                    : 0;

                // Most used keys
                ViewBag.MostUsedKey = apiKeys.OrderByDescending(k => k.RequestCount).FirstOrDefault()?.Name ?? "N/A";
                ViewBag.MostUsedKeyRequests = apiKeys.Any() ? apiKeys.Max(k => k.RequestCount) : 0;

                return View(apiKeys);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading API keys");
                TempData["Error"] = "Error loading API keys: " + ex.Message;
                return View(new List<ApiKey>());
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> GenerateApiKey(string name, string description, int rateLimit, DateTime? expiresAt, string permissions)
        {
            try
            {
                // Input validation
                if (string.IsNullOrWhiteSpace(name))
                {
                    TempData["Error"] = "API Key name is required";
                    return RedirectToAction(nameof(Index));
                }

                if (name.Length > 100)
                {
                    TempData["Error"] = "API Key name must be 100 characters or less";
                    return RedirectToAction(nameof(Index));
                }

                if (rateLimit < 0)
                {
                    TempData["Error"] = "Rate limit cannot be negative";
                    return RedirectToAction(nameof(Index));
                }

                if (expiresAt.HasValue && expiresAt.Value < DateTime.Now)
                {
                    TempData["Error"] = "Expiration date cannot be in the past";
                    return RedirectToAction(nameof(Index));
                }

                // Check for duplicate names
                var existingKey = await _context.Set<ApiKey>()
                    .FirstOrDefaultAsync(k => k.Name == name);
                if (existingKey != null)
                {
                    TempData["Error"] = $"API Key with name '{name}' already exists";
                    return RedirectToAction(nameof(Index));
                }

                // Generate secure API key
                var apiKey = GenerateSecureApiKey();

                var newKey = new ApiKey
                {
                    Name = name.Trim(),
                    Description = description?.Trim() ?? string.Empty,
                    KeyValue = HashApiKey(apiKey), // Store hashed version
                    RateLimit = rateLimit > 0 ? rateLimit : 1000,
                    ExpiresAt = expiresAt,
                    Permissions = permissions?.Trim() ?? string.Empty,
                    IsActive = true,
                    CreatedDate = DateTime.Now,
                    CreatedBy = User.Identity?.Name ?? "system",
                    RequestCount = 0
                };

                await _context.Set<ApiKey>().AddAsync(newKey);
                await _context.SaveChangesAsync();

                // Show key ONCE on creation (will never be shown again)
                TempData["Success"] = "API Key created successfully! Copy it now - it won't be shown again.";
                TempData["ApiKey"] = apiKey;
                TempData["ApiKeyName"] = name;

                _logger.LogInformation($"API Key '{name}' created by {User.Identity?.Name}");

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating API key");
                TempData["Error"] = "Error creating API key: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> RevokeApiKey(int id)
        {
            try
            {
                var apiKey = await _context.Set<ApiKey>().FindAsync(id);
                if (apiKey != null)
                {
                    apiKey.IsActive = false;
                    apiKey.ModifiedDate = DateTime.Now;
                    apiKey.ModifiedBy = User.Identity?.Name ?? "system";
                    await _context.SaveChangesAsync();

                    _logger.LogWarning($"API Key '{apiKey.Name}' revoked by {User.Identity?.Name}");
                    TempData["Success"] = $"API key '{apiKey.Name}' revoked successfully";
                }
                else
                {
                    TempData["Error"] = "API key not found";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error revoking API key");
                TempData["Error"] = "Error revoking API key: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ToggleStatus(int id)
        {
            try
            {
                var apiKey = await _context.Set<ApiKey>().FindAsync(id);
                if (apiKey != null)
                {
                    apiKey.IsActive = !apiKey.IsActive;
                    apiKey.ModifiedDate = DateTime.Now;
                    apiKey.ModifiedBy = User.Identity?.Name ?? "system";
                    await _context.SaveChangesAsync();

                    var status = apiKey.IsActive ? "activated" : "deactivated";
                    TempData["Success"] = $"API key '{apiKey.Name}' {status} successfully";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error toggling API key status");
                TempData["Error"] = ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var apiKey = await _context.Set<ApiKey>().FindAsync(id);
                if (apiKey != null)
                {
                    _context.Set<ApiKey>().Remove(apiKey);
                    await _context.SaveChangesAsync();

                    _logger.LogWarning($"API Key '{apiKey.Name}' deleted by {User.Identity?.Name}");
                    TempData["Success"] = $"API key '{apiKey.Name}' deleted successfully";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting API key");
                TempData["Error"] = ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public async Task<IActionResult> ResetRateLimit(int id)
        {
            try
            {
                var apiKey = await _context.Set<ApiKey>().FindAsync(id);
                if (apiKey != null)
                {
                    apiKey.RequestCount = 0;
                    apiKey.ModifiedDate = DateTime.Now;
                    apiKey.ModifiedBy = User.Identity?.Name ?? "system";
                    await _context.SaveChangesAsync();

                    TempData["Success"] = $"Rate limit reset for '{apiKey.Name}'";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error resetting rate limit");
                TempData["Error"] = ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetUsageStats(int id)
        {
            try
            {
                var apiKey = await _context.Set<ApiKey>().FindAsync(id);
                if (apiKey == null)
                {
                    return Json(new { success = false, message = "API key not found" });
                }

                var now = DateTime.Now;
                var today = DateTime.Today;
                var thisWeek = today.AddDays(-7);
                var thisMonth = today.AddMonths(-1);

                var stats = new
                {
                    name = apiKey.Name,
                    totalRequests = apiKey.RequestCount,
                    lastUsed = apiKey.LastUsed?.ToString("yyyy-MM-dd HH:mm:ss") ?? "Never",
                    rateLimit = apiKey.RateLimit,
                    utilizationPercent = apiKey.RateLimit > 0
                        ? Math.Min(100, Math.Round((apiKey.RequestCount / (double)apiKey.RateLimit) * 100, 2))
                        : 0,
                    remainingRequests = Math.Max(0, apiKey.RateLimit - apiKey.RequestCount),
                    isActive = apiKey.IsActive,
                    expiresAt = apiKey.ExpiresAt?.ToString("yyyy-MM-dd") ?? "Never",
                    daysUntilExpiry = apiKey.ExpiresAt.HasValue
                        ? (apiKey.ExpiresAt.Value - now).Days
                        : (int?)null,
                    permissions = apiKey.Permissions.Split(',', StringSplitOptions.RemoveEmptyEntries),
                    status = apiKey.ExpiresAt.HasValue && apiKey.ExpiresAt.Value < now
                        ? "Expired"
                        : apiKey.IsActive
                            ? "Active"
                            : "Inactive",
                    isOverLimit = apiKey.RequestCount > apiKey.RateLimit
                };

                return Json(new { success = true, data = stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting usage stats");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetStatistics()
        {
            try
            {
                var apiKeys = await _context.Set<ApiKey>().ToListAsync();
                var now = DateTime.Now;
                var today = DateTime.Today;

                var stats = new
                {
                    totalKeys = apiKeys.Count,
                    activeKeys = apiKeys.Count(k => k.IsActive),
                    expiredKeys = apiKeys.Count(k => k.ExpiresAt.HasValue && k.ExpiresAt.Value < now),
                    totalRequests = apiKeys.Sum(k => k.RequestCount),
                    averageUtilization = apiKeys.Any(k => k.RateLimit > 0)
                        ? Math.Min(100, Math.Round(apiKeys.Where(k => k.RateLimit > 0)
                            .Average(k => Math.Min(100, (k.RequestCount / (double)k.RateLimit) * 100)), 2))
                        : 0,
                    keysNearLimit = apiKeys.Count(k => k.IsActive && k.RateLimit > 0 &&
                        (k.RequestCount / (double)k.RateLimit) >= 0.8),
                    keysOverLimit = apiKeys.Count(k => k.RateLimit > 0 && k.RequestCount > k.RateLimit),
                    byStatus = new[]
                    {
                        new { status = "Active", count = apiKeys.Count(k => k.IsActive && (!k.ExpiresAt.HasValue || k.ExpiresAt.Value >= now)) },
                        new { status = "Inactive", count = apiKeys.Count(k => !k.IsActive) },
                        new { status = "Expired", count = apiKeys.Count(k => k.ExpiresAt.HasValue && k.ExpiresAt.Value < now) }
                    },
                    topKeys = apiKeys.OrderByDescending(k => k.RequestCount)
                        .Take(5)
                        .Select(k => new {
                            name = k.Name,
                            requests = k.RequestCount,
                            rateLimit = k.RateLimit,
                            utilization = k.RateLimit > 0
                                ? Math.Min(100, Math.Round((k.RequestCount / (double)k.RateLimit) * 100, 1))
                                : 0,
                            isOverLimit = k.RequestCount > k.RateLimit
                        })
                };

                return Json(new { success = true, data = stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting statistics");
                return Json(new { success = false, message = ex.Message });
            }
        }

        // Helper methods
        private string GenerateSecureApiKey()
        {
            const string prefix = "rmms_";
            var randomBytes = new byte[32];
            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(randomBytes);
            }
            return prefix + Convert.ToBase64String(randomBytes).Replace("+", "").Replace("/", "").Replace("=", "")[..40];
        }

        private string HashApiKey(string apiKey)
        {
            using (var sha256 = SHA256.Create())
            {
                var hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(apiKey));
                return Convert.ToBase64String(hashBytes);
            }
        }
    
        [HttpGet]
        public IActionResult Create()
        {
            try
            {
                return View(new ApiKey());
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading create page");
                TempData["Error"] = $"Error loading create page: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(ApiKey model)
        {
            if (!ModelState.IsValid)
            {
                return View(model);
            }

            try
            {
                model.CreatedDate = DateTime.Now;
                model.IsActive = true;
                model.CreatedBy = User.Identity?.Name ?? "system";

                await _context.Set<ApiKey>().AddAsync(model);
                await _context.SaveChangesAsync();

                TempData["Success"] = "ApiKey created successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating ApiKey");
                TempData["Error"] = $"Error creating record: {ex.Message}";
                return View(model);
            }
        }

    }
}
