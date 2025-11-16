using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using System.Collections.Concurrent;
using System.Threading;

namespace FHIRHealthcareAPI.Middleware
{
    public class MedicalApiRateLimitingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly IMemoryCache _cache;
        private readonly ILogger<MedicalApiRateLimitingMiddleware> _logger;

        // Rate limits optimized for medical API usage
        private static readonly RateLimitConfig DefaultLimits = new RateLimitConfig
        {
            TerminologyValidation = new RateLimit { RequestsPerMinute = 100, RequestsPerHour = 1000 },
            PatientDataAccess = new RateLimit { RequestsPerMinute = 50, RequestsPerHour = 500 },
            MedicationPrescription = new RateLimit { RequestsPerMinute = 20, RequestsPerHour = 200 },
            ConditionManagement = new RateLimit { RequestsPerMinute = 30, RequestsPerHour = 300 },
            LabResults = new RateLimit { RequestsPerMinute = 40, RequestsPerHour = 400 }
        };

        public MedicalApiRateLimitingMiddleware(
            RequestDelegate next,
            IMemoryCache cache,
            ILogger<MedicalApiRateLimitingMiddleware> logger)
        {
            _next = next;
            _cache = cache;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            var endpoint = GetEndpointCategory(context.Request.Path);
            var clientId = GetClientIdentifier(context);
            var rateLimit = GetRateLimitForEndpoint(endpoint);

            if (await IsRateLimitExceeded(clientId, endpoint, rateLimit))
            {
                await HandleRateLimitExceeded(context, rateLimit);
                return;
            }

            await RecordRequest(clientId, endpoint);
            await _next(context);
        }

        private string GetEndpointCategory(PathString path)
        {
            return path.Value.ToLower() switch
            {
                var p when p.Contains("/rxnorm-") || p.Contains("/loinc-") || p.Contains("/snomed-")
                          || p.Contains("/icd10-") => "terminology",
                var p when p.Contains("/patient") => "patient",
                var p when p.Contains("/medication") => "medication",
                var p when p.Contains("/condition") => "condition",
                var p when p.Contains("/observation") || p.Contains("/lab") => "lab",
                var p when p.Contains("/careplan") => "careplan",
                var p when p.Contains("/encounter") => "encounter",
                _ => "general"
            };
        }

        private string GetClientIdentifier(HttpContext context)
        {
            // Priority order for client identification
            var userId = context.User?.Identity?.Name;
            if (!string.IsNullOrEmpty(userId))
                return $"user:{userId}";

            var apiKey = context.Request.Headers["X-API-Key"].FirstOrDefault();
            if (!string.IsNullOrEmpty(apiKey))
                return $"apikey:{apiKey}";

            var clientIp = context.Connection.RemoteIpAddress?.ToString();
            return $"ip:{clientIp ?? "unknown"}";
        }

        private RateLimit GetRateLimitForEndpoint(string endpoint)
        {
            return endpoint switch
            {
                "terminology" => DefaultLimits.TerminologyValidation,
                "patient" => DefaultLimits.PatientDataAccess,
                "medication" => DefaultLimits.MedicationPrescription,
                "condition" => DefaultLimits.ConditionManagement,
                "lab" => DefaultLimits.LabResults,
                _ => new RateLimit { RequestsPerMinute = 60, RequestsPerHour = 1000 }
            };
        }

        private async Task<bool> IsRateLimitExceeded(string clientId, string endpoint, RateLimit limit)
        {
            var now = DateTime.UtcNow;
            var minuteKey = $"rate:{clientId}:{endpoint}:minute:{now:yyyyMMddHHmm}";
            var hourKey = $"rate:{clientId}:{endpoint}:hour:{now:yyyyMMddHH}";

            var minuteCount = await GetRequestCount(minuteKey);
            var hourCount = await GetRequestCount(hourKey);

            return minuteCount >= limit.RequestsPerMinute || hourCount >= limit.RequestsPerHour;
        }

        private async Task<int> GetRequestCount(string key)
        {
            return await Task.FromResult(_cache.TryGetValue(key, out var count) ? (int)count : 0);
        }

        private async Task RecordRequest(string clientId, string endpoint)
        {
            var now = DateTime.UtcNow;
            var minuteKey = $"rate:{clientId}:{endpoint}:minute:{now:yyyyMMddHHmm}";
            var hourKey = $"rate:{clientId}:{endpoint}:hour:{now:yyyyMMddHH}";

            await IncrementCounter(minuteKey, TimeSpan.FromMinutes(1));
            await IncrementCounter(hourKey, TimeSpan.FromHours(1));
        }

        private async Task IncrementCounter(string key, TimeSpan expiration)
        {
            var count = _cache.TryGetValue(key, out var existingCount) ? (int)existingCount + 1 : 1;
            _cache.Set(key, count, expiration);
            await Task.CompletedTask;
        }

        private async Task HandleRateLimitExceeded(HttpContext context, RateLimit limit)
        {
            context.Response.StatusCode = 429; // Too Many Requests
            context.Response.Headers.Add("X-RateLimit-Limit-Minute", limit.RequestsPerMinute.ToString());
            context.Response.Headers.Add("X-RateLimit-Limit-Hour", limit.RequestsPerHour.ToString());
            context.Response.Headers.Add("Retry-After", "60");

            var response = new
            {
                error = "Rate limit exceeded",
                message = $"Maximum {limit.RequestsPerMinute} requests per minute or {limit.RequestsPerHour} per hour allowed",
                retryAfter = 60
            };

            await context.Response.WriteAsync(System.Text.Json.JsonSerializer.Serialize(response));

            _logger.LogWarning($"Rate limit exceeded for {GetClientIdentifier(context)}");
        }
    }

    // External API rate limiting for terminology services
    public class ExternalApiRateLimiter
    {
        private readonly ConcurrentDictionary<string, SemaphoreSlim> _semaphores;
        private readonly ConcurrentDictionary<string, DateTime> _lastRequests;
        private readonly ILogger<ExternalApiRateLimiter> _logger;

        // External API limits (conservative to avoid hitting their limits)
        private static readonly Dictionary<string, ApiLimits> ExternalLimits = new()
        {
            ["rxnorm"] = new ApiLimits { RequestsPerSecond = 5, MaxConcurrent = 10 },
            ["loinc"] = new ApiLimits { RequestsPerSecond = 3, MaxConcurrent = 5 },
            ["snomed"] = new ApiLimits { RequestsPerSecond = 2, MaxConcurrent = 3 },
            ["icd10"] = new ApiLimits { RequestsPerSecond = 1, MaxConcurrent = 2 }
        };

        public ExternalApiRateLimiter(ILogger<ExternalApiRateLimiter> logger)
        {
            _logger = logger;
            _semaphores = new ConcurrentDictionary<string, SemaphoreSlim>();
            _lastRequests = new ConcurrentDictionary<string, DateTime>();

            // Initialize semaphores for each API
            foreach (var limit in ExternalLimits)
            {
                _semaphores[limit.Key] = new SemaphoreSlim(limit.Value.MaxConcurrent, limit.Value.MaxConcurrent);
            }
        }

        public async Task<T> ExecuteWithRateLimit<T>(string apiName, Func<Task<T>> apiCall)
        {
            var limits = ExternalLimits.TryGetValue(apiName.ToLower(), out var limit)
                ? limit
                : new ApiLimits { RequestsPerSecond = 1, MaxConcurrent = 1 };

            var semaphore = _semaphores.GetOrAdd(apiName, _ => new SemaphoreSlim(limits.MaxConcurrent, limits.MaxConcurrent));

            await semaphore.WaitAsync();
            try
            {
                await EnforceRateLimit(apiName, limits.RequestsPerSecond);
                return await apiCall();
            }
            finally
            {
                semaphore.Release();
            }
        }

        private async Task EnforceRateLimit(string apiName, double requestsPerSecond)
        {
            var minInterval = TimeSpan.FromMilliseconds(1000.0 / requestsPerSecond);
            var lastRequest = _lastRequests.TryGetValue(apiName, out var last) ? last : DateTime.MinValue;
            var elapsed = DateTime.UtcNow - lastRequest;

            if (elapsed < minInterval)
            {
                var delay = minInterval - elapsed;
                _logger.LogDebug($"Rate limiting {apiName}: waiting {delay.TotalMilliseconds}ms");
                await Task.Delay(delay);
            }

            _lastRequests[apiName] = DateTime.UtcNow;
        }
    }

    public class RateLimitConfig
    {
        public RateLimit TerminologyValidation { get; set; }
        public RateLimit PatientDataAccess { get; set; }
        public RateLimit MedicationPrescription { get; set; }
        public RateLimit ConditionManagement { get; set; }
        public RateLimit LabResults { get; set; }
    }

    public class RateLimit
    {
        public int RequestsPerMinute { get; set; }
        public int RequestsPerHour { get; set; }
    }

    public class ApiLimits
    {
        public double RequestsPerSecond { get; set; }
        public int MaxConcurrent { get; set; }
    }
}
 