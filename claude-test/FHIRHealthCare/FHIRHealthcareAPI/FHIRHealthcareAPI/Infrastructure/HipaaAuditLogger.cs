using System;
using System.Collections.Generic;
using System.Security.Claims;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;
using System.Text.Json;

namespace FHIRHealthcareAPI.Infrastructure
{
    /// <summary>
    /// HIPAA-compliant audit logging system
    /// </summary>
    public class HipaaAuditLogger
    {
        private readonly ILogger<HipaaAuditLogger> _logger;
        private readonly IConfiguration _configuration;

        public HipaaAuditLogger(ILogger<HipaaAuditLogger> logger, IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
        }

        /// <summary>
        /// Logs patient data access for HIPAA compliance
        /// </summary>
        public async Task LogPatientAccess(string userId, string patientId, string action, string resourceType, HttpContext context)
        {
            var auditEvent = new HipaaAuditEvent
            {
                EventId = Guid.NewGuid().ToString(),
                Timestamp = DateTime.UtcNow,
                EventType = "Patient Data Access",
                Action = action, // CREATE, READ, UPDATE, DELETE
                ResourceType = resourceType, // Patient, Observation, Medication, etc.
                ResourceId = patientId,
                UserId = userId,
                UserRole = context.User?.FindFirst(ClaimTypes.Role)?.Value,
                IpAddress = context.Connection.RemoteIpAddress?.ToString(),
                UserAgent = context.Request.Headers["User-Agent"].FirstOrDefault(),
                Outcome = "Success", // Success, Failed, Unauthorized
                Details = new Dictionary<string, string>
                {
                    ["PatientId"] = patientId,
                    ["Endpoint"] = context.Request.Path,
                    ["Method"] = context.Request.Method
                }
            };

            await LogAuditEvent(auditEvent);
        }

        /// <summary>
        /// Logs medication prescribing events
        /// </summary>
        public async Task LogMedicationEvent(string userId, string patientId, string medicationCode, string action, string outcome = "Success")
        {
            var auditEvent = new HipaaAuditEvent
            {
                EventId = Guid.NewGuid().ToString(),
                Timestamp = DateTime.UtcNow,
                EventType = "Medication Management",
                Action = action,
                ResourceType = "MedicationRequest",
                UserId = userId,
                Outcome = outcome,
                Details = new Dictionary<string, string>
                {
                    ["PatientId"] = patientId,
                    ["MedicationCode"] = medicationCode,
                    ["Action"] = action
                }
            };

            await LogAuditEvent(auditEvent);
        }

        /// <summary>
        /// Logs failed authentication attempts
        /// </summary>
        public async Task LogAuthenticationFailure(string username, string reason, HttpContext context)
        {
            var auditEvent = new HipaaAuditEvent
            {
                EventId = Guid.NewGuid().ToString(),
                Timestamp = DateTime.UtcNow,
                EventType = "Authentication",
                Action = "LOGIN_FAILED",
                UserId = username,
                Outcome = "Failed",
                IpAddress = context.Connection.RemoteIpAddress?.ToString(),
                Details = new Dictionary<string, string>
                {
                    ["Reason"] = reason,
                    ["AttemptTime"] = DateTime.UtcNow.ToString("O")
                }
            };

            await LogAuditEvent(auditEvent);
        }

        private async Task LogAuditEvent(HipaaAuditEvent auditEvent)
        {
            // Log to structured logging system
            _logger.LogInformation("HIPAA_AUDIT: {AuditEvent}", JsonSerializer.Serialize(auditEvent));

            // In production, also send to:
            // 1. Dedicated audit database
            // 2. SIEM system
            // 3. Compliance monitoring service

            await Task.CompletedTask;
        }
    }

    /// <summary>
    /// Advanced security middleware for healthcare API
    /// </summary>
    public class HealthcareSecurityMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly HipaaAuditLogger _auditLogger;
        private readonly ILogger<HealthcareSecurityMiddleware> _logger;

        public HealthcareSecurityMiddleware(
            RequestDelegate next,
            HipaaAuditLogger auditLogger,
            ILogger<HealthcareSecurityMiddleware> logger)
        {
            _next = next;
            _auditLogger = auditLogger;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            // Security headers
            AddSecurityHeaders(context);

            // Request validation
            if (!await ValidateRequest(context))
                return;

            // Monitor sensitive endpoints
            if (IsSensitiveEndpoint(context.Request.Path))
            {
                await LogSensitiveAccess(context);
            }

            await _next(context);
        }

        private void AddSecurityHeaders(HttpContext context)
        {
            var response = context.Response;

            // Security headers for healthcare APIs
            response.Headers.Add("X-Content-Type-Options", "nosniff");
            response.Headers.Add("X-Frame-Options", "DENY");
            response.Headers.Add("X-XSS-Protection", "1; mode=block");
            response.Headers.Add("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
            response.Headers.Add("Content-Security-Policy", "default-src 'self'");
            response.Headers.Add("Referrer-Policy", "strict-origin-when-cross-origin");

            // HIPAA-specific headers
            response.Headers.Add("Cache-Control", "no-store, no-cache, must-revalidate");
            response.Headers.Add("Pragma", "no-cache");
        }

        private async Task<bool> ValidateRequest(HttpContext context)
        {
            // Validate content type for POST/PUT requests
            if ((context.Request.Method == "POST" || context.Request.Method == "PUT") &&
                !context.Request.ContentType?.StartsWith("application/json") == true)
            {
                context.Response.StatusCode = 415;
                await context.Response.WriteAsync("Unsupported Media Type");
                return false;
            }

            // Check for suspicious patterns
            if (ContainsSuspiciousContent(context.Request.QueryString.Value) ||
                ContainsSuspiciousContent(context.Request.Path))
            {
                _logger.LogWarning("Suspicious request detected from {IP}: {Path}",
                    context.Connection.RemoteIpAddress, context.Request.Path);

                context.Response.StatusCode = 400;
                await context.Response.WriteAsync("Bad Request");
                return false;
            }

            return true;
        }

        private bool IsSensitiveEndpoint(PathString path)
        {
            var sensitivePaths = new[]
            {
                "/patient", "/observation", "/condition",
                "/medication", "/encounter", "/careplan"
            };

            return sensitivePaths.Any(p => path.Value?.Contains(p, StringComparison.OrdinalIgnoreCase) == true);
        }

        private async Task LogSensitiveAccess(HttpContext context)
        {
            var userId = context.User?.Identity?.Name ?? "Anonymous";
            var patientId = ExtractPatientId(context.Request.Path);

            if (!string.IsNullOrEmpty(patientId))
            {
                await _auditLogger.LogPatientAccess(
                    userId,
                    patientId,
                    context.Request.Method,
                    GetResourceType(context.Request.Path),
                    context);
            }
        }

        private string ExtractPatientId(PathString path)
        {
            // Extract patient ID from various endpoint patterns
            // /api/fhir/patient/{id} or /api/fhir/observation/patient/{id}
            var segments = path.Value?.Split('/') ?? Array.Empty<string>();

            for (int i = 0; i < segments.Length - 1; i++)
            {
                if (segments[i].Equals("patient", StringComparison.OrdinalIgnoreCase))
                {
                    return segments[i + 1];
                }
            }

            return null;
        }

        private string GetResourceType(PathString path)
        {
            return path.Value?.Split('/').LastOrDefault(s =>
                !string.IsNullOrEmpty(s) && !Guid.TryParse(s, out _)) ?? "Unknown";
        }

        private bool ContainsSuspiciousContent(string input)
        {
            if (string.IsNullOrEmpty(input))
                return false;

            var suspiciousPatterns = new[]
            {
                "<script", "javascript:", "sql", "union", "select",
                "drop", "delete", "insert", "update", "--", ";--"
            };

            return suspiciousPatterns.Any(pattern =>
                input.Contains(pattern, StringComparison.OrdinalIgnoreCase));
        }
    }

    /// <summary>
    /// Performance monitoring and health check system
    /// </summary>
    public class HealthcarePerformanceMonitor
    {
        private readonly ILogger<HealthcarePerformanceMonitor> _logger;

        public HealthcarePerformanceMonitor(ILogger<HealthcarePerformanceMonitor> logger)
        {
            _logger = logger;
        }

        /// <summary>
        /// Monitors API performance metrics
        /// </summary>
        public async Task<PerformanceMetrics> GetPerformanceMetrics()
        {
            var metrics = new PerformanceMetrics
            {
                Timestamp = DateTime.UtcNow,
                ApiEndpoints = await GetEndpointMetrics(),
                DatabaseMetrics = await GetDatabaseMetrics(),
                ExternalApiMetrics = await GetExternalApiMetrics(),
                SystemMetrics = GetSystemMetrics()
            };

            return metrics;
        }

        private async Task<List<EndpointMetric>> GetEndpointMetrics()
        {
            // In production, this would query your metrics store
            return new List<EndpointMetric>
            {
                new EndpointMetric
                {
                    Endpoint = "/api/fhir/patient",
                    AverageResponseTime = TimeSpan.FromMilliseconds(150),
                    RequestCount = 1250,
                    ErrorRate = 0.02
                },
                new EndpointMetric
                {
                    Endpoint = "/api/rxnorm-live/drug",
                    AverageResponseTime = TimeSpan.FromMilliseconds(800),
                    RequestCount = 890,
                    ErrorRate = 0.05
                }
            };
        }

        private async Task<DatabaseMetrics> GetDatabaseMetrics()
        {
            return new DatabaseMetrics
            {
                AverageQueryTime = TimeSpan.FromMilliseconds(45),
                ActiveConnections = 15,
                ConnectionPoolUtilization = 0.3,
                SlowQueries = 2
            };
        }

        private async Task<ExternalApiMetrics> GetExternalApiMetrics()
        {
            return new ExternalApiMetrics
            {
                RxNormAvailability = 0.99,
                LoincAvailability = 0.98,
                SnomedAvailability = 0.97,
                AverageExternalResponseTime = TimeSpan.FromMilliseconds(650)
            };
        }

        private SystemMetrics GetSystemMetrics()
        {
            return new SystemMetrics
            {
                CpuUtilization = 0.35,
                MemoryUtilization = 0.42,
                DiskUtilization = 0.18,
                NetworkThroughput = 150.5 // MB/s
            };
        }
    }

    // Data models for audit and monitoring
    public class HipaaAuditEvent
    {
        public string EventId { get; set; }
        public DateTime Timestamp { get; set; }
        public string EventType { get; set; }
        public string Action { get; set; }
        public string ResourceType { get; set; }
        public string ResourceId { get; set; }
        public string UserId { get; set; }
        public string UserRole { get; set; }
        public string IpAddress { get; set; }
        public string UserAgent { get; set; }
        public string Outcome { get; set; }
        public Dictionary<string, string> Details { get; set; } = new();
    }

    public class PerformanceMetrics
    {
        public DateTime Timestamp { get; set; }
        public List<EndpointMetric> ApiEndpoints { get; set; }
        public DatabaseMetrics DatabaseMetrics { get; set; }
        public ExternalApiMetrics ExternalApiMetrics { get; set; }
        public SystemMetrics SystemMetrics { get; set; }
    }

    public class EndpointMetric
    {
        public string Endpoint { get; set; }
        public TimeSpan AverageResponseTime { get; set; }
        public int RequestCount { get; set; }
        public double ErrorRate { get; set; }
    }

    public class DatabaseMetrics
    {
        public TimeSpan AverageQueryTime { get; set; }
        public int ActiveConnections { get; set; }
        public double ConnectionPoolUtilization { get; set; }
        public int SlowQueries { get; set; }
    }

    public class ExternalApiMetrics
    {
        public double RxNormAvailability { get; set; }
        public double LoincAvailability { get; set; }
        public double SnomedAvailability { get; set; }
        public TimeSpan AverageExternalResponseTime { get; set; }
    }

    public class SystemMetrics
    {
        public double CpuUtilization { get; set; }
        public double MemoryUtilization { get; set; }
        public double DiskUtilization { get; set; }
        public double NetworkThroughput { get; set; }
    }
}
 