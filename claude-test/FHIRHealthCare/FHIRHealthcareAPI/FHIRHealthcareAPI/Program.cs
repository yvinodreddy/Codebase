using System.Text.Json;
using FHIRHealthcareAPI.HealthChecks;
using FHIRHealthcareAPI.Infrastructure;
using FHIRHealthcareAPI.Middleware;
using FHIRHealthcareAPI.Services;
using FHIRHealthcareAPI.Services.Cache;
using FHIRHealthcareAPI.Services.Clinical; // Add this for new controllers
using FHIRHealthcareAPI.Services.Terminology;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using Polly;
using Polly.Extensions.Http;
using System;
using System.Net.Http;
using System.Text;
using FHIRHealthcareAPI.Modules.KnowledgeGraph.Services;
using FHIRHealthcareAPI.Modules.MachineLearning.Services;
using FHIRHealthcareAPI.Infrastructure.Hubs;
using FHIRHealthcareAPI.Infrastructure.GraphDatabase;
using System.Security.Claims;
using FHIRHealthcareAPI.Models;

namespace FHIRHealthcareAPI
{
    public class Program
    {
        public static void Main(string[] args)
        {
            // At the very beginning of Program.cs
            DotNetEnv.Env.Load(); // This loads .env file 

            var builder = WebApplication.CreateBuilder(args);

            // Now environment variables are available
            builder.Configuration
                .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true, reloadOnChange: true)
                .AddEnvironmentVariables()  // Regular environment variables
                .AddEnvironmentVariables(prefix: "HEALTHCARE_");  // Prefixed environment variables for Docker/production

            // This allows you to override settings with environment variables like:
            // HEALTHCARE_ConnectionStrings__RedisCache=your-redis-connection
            // HEALTHCARE_GraphDB__Password=your-secure-password
            builder.Services.AddControllers();

            // Cache configuration (your working setup)
            var redisConnection = builder.Configuration.GetConnectionString("RedisCache");
            if (!string.IsNullOrEmpty(redisConnection))
            {
                builder.Services.AddStackExchangeRedisCache(options =>
                {
                    options.Configuration = redisConnection;
                    options.InstanceName = "FhirApi";
                });
            }
            else
            {
                builder.Services.AddDistributedMemoryCache();
            }

            // Register cache and rate limiting services (your working setup)
            builder.Services.AddSingleton<ICacheService, CacheService>();
            builder.Services.AddMemoryCache();
            builder.Services.AddSingleton<ExternalApiRateLimiter>();

            // Register HTTP clients with retry policies (your working setup)
            builder.Services.AddHttpClient<SimplifiedRxNormService>()
                .AddPolicyHandler(GetRetryPolicy());

            // Register terminology services (your working setup)
            builder.Services.AddScoped<LoincService>();
            builder.Services.AddScoped<SnomedService>();

            // Register clinical services (your working setup)
            builder.Services.AddScoped<ObservationService>();
            builder.Services.AddScoped<ConditionService>();

            // JWT Configuration (your working setup)
            // JWT Configuration - FIXED
            var jwtSettings = builder.Configuration.GetSection("JwtSettings");
            var secretKeyString = jwtSettings["SecretKey"];  // Get the actual string value
            var secretKey = Encoding.UTF8.GetBytes(secretKeyString);

            // Debug the secret key
            Console.WriteLine($"Program.cs - Secret Key: {secretKeyString}");
            Console.WriteLine($"Program.cs - Secret Key Length: {secretKey.Length} bytes");
            Console.WriteLine($"Program.cs - Issuer: {jwtSettings["Issuer"]}, Audience: {jwtSettings["Audience"]}");

            builder.Services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
            })
            .AddJwtBearer(options =>
            {
                options.RequireHttpsMetadata = false;
                options.SaveToken = true;
                 
                options.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuerSigningKey = true,
                    IssuerSigningKey = new SymmetricSecurityKey(secretKey),
                    ValidateIssuer = true,
                    ValidIssuer = jwtSettings["Issuer"],
                    ValidateAudience = true,
                    ValidAudience = jwtSettings["Audience"],
                    ValidateLifetime = true,
                    ClockSkew = TimeSpan.FromMinutes(5) // Changed from Zero to 5 minutes
                };

                // Enhanced debugging events
                options.Events = new JwtBearerEvents
                {
                    OnMessageReceived = context =>
                    {
                        var authHeader = context.Request.Headers["Authorization"].FirstOrDefault();
                        Console.WriteLine($"🔍 Full Auth Header: '{authHeader}'");

                        if (string.IsNullOrEmpty(authHeader))
                        {
                            Console.WriteLine("❌ No Authorization header found!");
                        }
                        else if (!authHeader.StartsWith("Bearer ", StringComparison.OrdinalIgnoreCase))
                        {
                            Console.WriteLine($"❌ Auth header doesn't start with 'Bearer ': {authHeader.Substring(0, Math.Min(20, authHeader.Length))}");
                        }
                        else
                        {
                            var token = authHeader.Substring(7); // Remove "Bearer "
                            Console.WriteLine($"✅ Token extracted: {token.Substring(0, Math.Min(50, token.Length))}...");
                            context.Token = token; // Explicitly set the token
                        }

                        return Task.CompletedTask;
                    },
                    OnAuthenticationFailed = context =>
                    {
                        Console.WriteLine($"❌ JWT Authentication Failed!");
                        Console.WriteLine($"   Exception Type: {context.Exception.GetType().Name}");
                        Console.WriteLine($"   Exception Message: {context.Exception.Message}");
                        if (context.Exception.InnerException != null)
                        {
                            Console.WriteLine($"   Inner Exception: {context.Exception.InnerException.Message}");
                        }
                        return Task.CompletedTask;
                    },
                    OnTokenValidated = context =>
                    {
                        Console.WriteLine($"✅ JWT Token validated successfully!");
                        Console.WriteLine($"   User: {context.Principal?.Identity?.Name}");
                        Console.WriteLine($"   Claims: {string.Join(", ", context.Principal?.Claims.Select(c => c.Type) ?? new List<string>())}");
                        return Task.CompletedTask;
                    },
                    OnChallenge = context =>
                    {
                        Console.WriteLine($"🚫 JWT Challenge triggered!");
                        Console.WriteLine($"   Error: {context.Error}");
                        Console.WriteLine($"   Error Description: {context.ErrorDescription}");
                        Console.WriteLine($"   Auth Failure: {context.AuthenticateFailure?.Message}");
                        return Task.CompletedTask;
                    }
                };
            });

            builder.Services.AddAuthorization();

            // Existing services (your working setup)
            builder.Services.AddSingleton<UserService>();
            builder.Services.AddScoped<PatientService>();
            builder.Services.AddScoped<MedicationService>();
            builder.Services.AddScoped<AllergyService>();
            builder.Services.AddScoped<ClinicalDecisionSupportService>();

            // Production services (your working setup)
            builder.Services.AddSingleton<HipaaAuditLogger>();
            builder.Services.AddSingleton<HealthcarePerformanceMonitor>();

            // Data Seeding Service - Auto-seeds test data on startup
            builder.Services.AddHostedService<DataSeedingHostedService>();


            // Register FhirClient for dependency injection
            builder.Services.AddScoped<Hl7.Fhir.Rest.FhirClient>(provider =>
            {
                return new Hl7.Fhir.Rest.FhirClient("http://localhost:8080/fhir")
                {
                    Settings = new Hl7.Fhir.Rest.FhirClientSettings
                    {
                        PreferredFormat = Hl7.Fhir.Rest.ResourceFormat.Json,
                        Timeout = 30000
                    }
                };
            }); 

            // NEW: Add advanced clinical services (only if the files exist)
            // Uncomment these as you add the corresponding service files:
            builder.Services.AddScoped<CarePlanManagementService>();
            builder.Services.AddScoped<EncounterManagementService>();
            builder.Services.AddScoped<ClinicalDecisionSupportEngine>();

            // Register GraphDB and Knowledge services
            builder.Services.AddSingleton<GraphDBConnector>();
            builder.Services.AddScoped<KnowledgeGraphService>();
            builder.Services.AddScoped<SemanticQueryService>();

            // Register ML services
            builder.Services.AddSingleton<PredictiveHealthService>();

            // Add SignalR
            builder.Services.AddSignalR();

            // Add CORS for SignalR
            builder.Services.AddCors(options =>
            {
                options.AddPolicy("AllowAll", builder =>
                {
                    builder.AllowAnyOrigin()
                           .AllowAnyMethod()
                           .AllowAnyHeader();
                });
            }); 

            // Health checks (your working setup)
            builder.Services.AddHealthChecks()
                .AddTypeActivatedCheck<TerminologyHealthCheck>("terminology")
                .AddTypeActivatedCheck<FhirServerHealthCheck>("fhir-server");

            // Swagger (enhanced with your beautiful dark theme)
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen(options =>
            {
                options.SwaggerDoc("v1", new OpenApiInfo
                {
                    Title = "Advanced FHIR Healthcare API", // Updated title
                    Version = "v1",
                    Description = "Enterprise-grade FHIR healthcare API with clinical decision support, care plan management, and live medical terminology validation" // Enhanced description
                });

                options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
                {
                    Description = "JWT Authorization header using the Bearer scheme. Enter 'Bearer' [space] and then your token",
                    Name = "Authorization",
                    In = ParameterLocation.Header,
                    Type = SecuritySchemeType.ApiKey,
                    Scheme = "Bearer"
                });

                options.AddSecurityRequirement(new OpenApiSecurityRequirement
                {
                    {
                        new OpenApiSecurityScheme
                        {
                            Reference = new OpenApiReference
                            {
                                Type = ReferenceType.SecurityScheme,
                                Id = "Bearer"
                            }
                        },
                        Array.Empty<string>()
                    }
                });
            });

            var app = builder.Build();

            
            // 1. CORS first
            app.UseCors("AllowAll");

            // 2. Swagger (outside development check)
            app.UseSwagger();

            if (app.Environment.IsDevelopment())
            { 

                app.UseSwaggerUI(options =>
                {
                    options.SwaggerEndpoint("/swagger/v1/swagger.json", "Advanced FHIR Healthcare API v1");
                    options.DocumentTitle = "Healthcare API - Professional Dark Mode";

                    // Your excellent dark theme (keeping it exactly as is)
                    options.HeadContent = @"
            <style>
                .swagger-ui {
                    background-color: #1e1e1e !important;
                    color: #ffffff !important;
                }
                .swagger-ui .topbar {
                    background-color: #2d2d30 !important;
                }
                .swagger-ui .info {
                    background-color: #2d2d30 !important;
                    color: #ffffff !important;
                }
                .swagger-ui .info .title {
                    color: #4fc3f7 !important;
                }
                .swagger-ui .scheme-container {
                    background-color: #2d2d30 !important;
                }
                .swagger-ui .opblock {
                    background-color: #2d2d30 !important;
                    border: 1px solid #3e3e42 !important;
                    margin-bottom: 10px !important;
                }
                .swagger-ui .opblock-summary {
                    background-color: #3e3e42 !important;
                    border-bottom: 1px solid #3e3e42 !important;
                }
                .swagger-ui .opblock.opblock-get .opblock-summary {
                    background-color: #2e7d32 !important;
                }
                .swagger-ui .opblock.opblock-post .opblock-summary {
                    background-color: #1976d2 !important;
                }
                .swagger-ui .opblock.opblock-put .opblock-summary {
                    background-color: #f57c00 !important;
                }
                .swagger-ui .opblock.opblock-delete .opblock-summary {
                    background-color: #d32f2f !important;
                }
                .swagger-ui .parameters-container, 
                .swagger-ui .response-container {
                    background-color: #1e1e1e !important;
                }
                .swagger-ui input, 
                .swagger-ui textarea, 
                .swagger-ui select {
                    background-color: #3e3e42 !important;
                    color: #ffffff !important;
                    border: 1px solid #555 !important;
                }
                .swagger-ui .btn {
                    background-color: #1976d2 !important;
                    color: white !important;
                }
                .swagger-ui .highlight-code {
                    background-color: #2d2d30 !important;
                }
                .swagger-ui pre {
                    background-color: #2d2d30 !important;
                    color: #ffffff !important;
                }
                .swagger-ui .model-box {
                    background-color: #2d2d30 !important;
                }
                .swagger-ui .model {
                    color: #ffffff !important;
                }
            </style>";
                });
            }

            // 3. HTTPS redirection
            app.UseHttpsRedirection();

            // 4. Authentication BEFORE custom middleware (CRITICAL FIX)
            app.UseAuthentication();
            app.UseAuthorization();

            // 5. Custom middleware AFTER authentication
            // Add middleware (your working setup)
            //app.UseMiddleware<MedicalApiRateLimitingMiddleware>();
            //app.UseMiddleware<HealthcareSecurityMiddleware>();

            // 6. Health checks and controllers
            // Health check mapping with JSON response (your working setup)
            app.MapHealthChecks("/health", new HealthCheckOptions
            {
                ResponseWriter = async (context, report) =>
                {
                    var result = JsonSerializer.Serialize(new
                    {
                        status = report.Status.ToString(),
                        checks = report.Entries.Select(e => new
                        {
                            name = e.Key,
                            status = e.Value.Status.ToString(),
                            description = e.Value.Description,
                            duration = e.Value.Duration
                        })
                    });
                    await context.Response.WriteAsync(result);
                }
            });


            // 7. SignalR hub mapping
            app.MapHub<ClinicalIntelligenceHub>("/hubs/clinical-intelligence");

            app.MapControllers();
            app.Run();
        }

        private static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy()
        {
            return HttpPolicyExtensions
                .HandleTransientHttpError()
                .OrResult(msg => !msg.IsSuccessStatusCode)
                .WaitAndRetryAsync(
                    3,
                    retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
        }
    }
}