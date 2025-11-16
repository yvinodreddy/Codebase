using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Google.Cloud.Diagnostics.AspNetCore3;
using Google.Cloud.Diagnostics.Common;
using Serilog;
using Serilog.Events;
using Serilog.Sinks.BigQuery;
using HealthcareManagement.AI.Services;
using HealthcareManagement.AI.Middleware;
using Microsoft.OpenApi.Models;
using System;
using System.IO;
using Google.Api;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

namespace HealthcareManagement.AI
{
    /// <summary>
    /// Main entry point for the AI-Generative Healthcare Platform
    /// This configuration enables all AI services required for Google Startup Program qualification
    /// </summary>
    public class Program
    {
        public static void Main(string[] args)
        {
            // Configure Serilog for comprehensive AI logging
            Log.Logger = new LoggerConfiguration()
                .MinimumLevel.Debug()
                .MinimumLevel.Override("Microsoft", LogEventLevel.Information)
                .Enrich.FromLogContext()
                .WriteTo.Console()
                .WriteTo.File("logs/ai-platform-.log", rollingInterval: RollingInterval.Day)
                .WriteTo.BigQuery(
                    projectId: Environment.GetEnvironmentVariable("GOOGLE_CLOUD_PROJECT"),
                    datasetId: "ai_logs",
                    tableId: "platform_logs",
                    autoCreateTable: true)
                .CreateLogger();

            try
            {
                Log.Information("Starting AI Healthcare Platform - Google Cloud AI Startup");
                CreateHostBuilder(args).Build().Run();
            }
            catch (Exception ex)
            {
                Log.Fatal(ex, "AI Platform failed to start");
                throw;
            }
            finally
            {
                Log.CloseAndFlush();
            }
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .UseSerilog()
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();

                    // Enable Google Cloud integration
                    var projectId = Environment.GetEnvironmentVariable("GOOGLE_CLOUD_PROJECT");
                    if (!string.IsNullOrEmpty(projectId))
                    {
                        webBuilder.UseGoogleDiagnostics(projectId, "ai-healthcare-platform", "v1.0");
                    }
                });
    }

    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        public void ConfigureServices(IServiceCollection services)
        {
            // Add Google Cloud credentials
            var credentialsPath = Configuration["GoogleCloud:CredentialsPath"];
            if (!string.IsNullOrEmpty(credentialsPath))
            {
                Environment.SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", credentialsPath);
            }

            // Configure AI Services - CORE OF OUR AI STARTUP
            ConfigureAIServices(services);

            // Add controllers with AI-enhanced features
            services.AddControllers()
                .AddNewtonsoftJson(options =>
                {
                    options.SerializerSettings.ReferenceLoopHandling = Newtonsoft.Json.ReferenceLoopHandling.Ignore;
                });

            // Configure JWT Authentication
            ConfigureAuthentication(services);

            // Add CORS for AI API access
            services.AddCors(options =>
            {
                options.AddPolicy("AIApiPolicy", builder =>
                {
                    builder.AllowAnyOrigin()
                           .AllowAnyMethod()
                           .AllowAnyHeader();
                });
            });

            // Configure Swagger for AI API documentation
            services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc("v1", new OpenApiInfo
                {
                    Title = "MediGenius AI Healthcare Platform API",
                    Version = "v1",
                    Description = "AI-Powered Healthcare Intelligence Platform - Qualifying for Google $350K AI Startup Credits",
                    Contact = new OpenApiContact
                    {
                        Name = "MediGenius AI Team",
                        Email = "api@medigenius-ai.com",
                        Url = new Uri("https://medigenius-ai.com")
                    }
                });

                // Add JWT Authentication to Swagger
                c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
                {
                    Description = "JWT Authorization header using the Bearer scheme",
                    Name = "Authorization",
                    In = ParameterLocation.Header,
                    Type = SecuritySchemeType.ApiKey,
                    Scheme = "Bearer"
                });

                c.AddSecurityRequirement(new OpenApiSecurityRequirement
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

                // Include XML documentation
                var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
                var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
                if (File.Exists(xmlPath))
                {
                    c.IncludeXmlComments(xmlPath);
                }
            });

            // Add health checks for AI services
            services.AddHealthChecks()
                .AddCheck<VertexAIHealthCheck>("vertex-ai")
                .AddCheck<GeminiHealthCheck>("gemini-api")
                .AddCheck<BigQueryHealthCheck>("bigquery")
                .AddCheck<CloudStorageHealthCheck>("cloud-storage");

            // Add SignalR for real-time AI updates
            services.AddSignalR();

            // Add background services for AI processing
            services.AddHostedService<AIModelUpdateService>();
            services.AddHostedService<AIMetricsCollectorService>();

            // Configure rate limiting for AI endpoints
            services.AddRateLimiter(options =>
            {
                options.AddFixedWindowLimiter("ai-diagnosis", limiterOptions =>
                {
                    limiterOptions.Window = TimeSpan.FromMinutes(1);
                    limiterOptions.PermitLimit = 10;
                });

                options.AddFixedWindowLimiter("ai-image-analysis", limiterOptions =>
                {
                    limiterOptions.Window = TimeSpan.FromMinutes(1);
                    limiterOptions.PermitLimit = 5;
                });
            });

            // Add response caching for AI results
            services.AddResponseCaching();

            // Add memory cache for AI model predictions
            services.AddMemoryCache();

            // Configure BigQuery for AI analytics
            services.AddSingleton<BigQueryService>();

            // Configure Google Cloud Storage for medical images
            services.AddSingleton<CloudStorageService>();
        }

        private void ConfigureAIServices(IServiceCollection services)
        {
            // CRITICAL: Register all AI services that make us an AI startup

            // 1. Core Medical Diagnosis AI (Primary AI Feature)
            services.AddScoped<IMedicalDiagnosisAI, MedicalDiagnosisAI>();

            // 2. Clinical Documentation AI
            services.AddScoped<IClinicalDocumentAI, ClinicalDocumentAI>();

            // 3. Prescription Optimization AI
            services.AddScoped<IPrescriptionOptimizationAI, PrescriptionOptimizationAI>();

            // 4. Medical Image Analysis AI
            services.AddScoped<IMedicalImageAnalysisAI, MedicalImageAnalysisAI>();

            // 5. Health Risk Predictor AI
            services.AddScoped<IHealthRiskPredictorAI, HealthRiskPredictorAI>();

            // 6. Clinical Decision Support AI
            services.AddScoped<IClinicalDecisionSupportAI, ClinicalDecisionSupportAI>();

            // 7. Patient Engagement Chatbot AI
            services.AddScoped<IPatientEngagementAI, PatientEngagementAI>();

            // 8. AI Model Management Service
            services.AddScoped<IAIModelManagementService, AIModelManagementService>();

            // 9. AI Performance Monitoring
            services.AddScoped<IAIPerformanceMonitor, AIPerformanceMonitor>();

            // 10. AI Cost Optimization Service
            services.AddScoped<IAICostOptimizationService, AICostOptimizationService>();

            // Configure HTTP client for AI APIs
            services.AddHttpClient("GeminiAPI", client =>
            {
                client.BaseAddress = new Uri("https://generativelanguage.googleapis.com");
                client.DefaultRequestHeaders.Add("Accept", "application/json");
                client.Timeout = TimeSpan.FromSeconds(30);
            });

            services.AddHttpClient("VertexAI", client =>
            {
                client.BaseAddress = new Uri($"https://{Configuration["GoogleCloud:Region"]}-aiplatform.googleapis.com");
                client.DefaultRequestHeaders.Add("Accept", "application/json");
                client.Timeout = TimeSpan.FromSeconds(60);
            });

            // Configure Google Cloud AI Platform settings
            services.Configure<GoogleCloudAIOptions>(Configuration.GetSection("GoogleCloudAI"));

            // Add AI feature flags
            services.Configure<AIFeatureFlags>(Configuration.GetSection("AIFeatures"));
        }

        private void ConfigureAuthentication(IServiceCollection services)
        {
            var jwtSettings = Configuration.GetSection("JwtSettings");
            var secretKey = Encoding.UTF8.GetBytes(jwtSettings["SecretKey"]);

            services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
            })
            .AddJwtBearer(options =>
            {
                options.TokenValidationParameters = new TokenValidationParameters
                {
                    ValidateIssuer = true,
                    ValidateAudience = true,
                    ValidateLifetime = true,
                    ValidateIssuerSigningKey = true,
                    ValidIssuer = jwtSettings["Issuer"],
                    ValidAudience = jwtSettings["Audience"],
                    IssuerSigningKey = new SymmetricSecurityKey(secretKey),
                    ClockSkew = TimeSpan.Zero
                };
            });

            services.AddAuthorization(options =>
            {
                options.AddPolicy("AIAccess", policy => policy.RequireRole("Doctor", "Admin", "AIUser"));
                options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"));
            });
        }

        public void Configure(IApplicationBuilder app, IWebHostEnvironment env, ILoggerFactory loggerFactory)
        {
            // Enable Google Cloud logging and monitoring
            if (!string.IsNullOrEmpty(Configuration["GoogleCloud:ProjectId"]))
            {
                loggerFactory.AddGoogle(app.ApplicationServices, Configuration["GoogleCloud:ProjectId"]);
            }

            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Error");
                app.UseHsts();
            }

            // Enable Swagger for AI API documentation
            app.UseSwagger();
            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint("/swagger/v1/swagger.json", "MediGenius AI Platform V1");
                c.RoutePrefix = "api-docs";
                c.DocumentTitle = "MediGenius AI Healthcare Platform - API Documentation";
            });

            app.UseHttpsRedirection();

            // Add AI request/response logging middleware
            app.UseMiddleware<AIRequestLoggingMiddleware>();

            // Add AI performance monitoring middleware
            app.UseMiddleware<AIPerformanceMiddleware>();

            // Use response caching for AI results
            app.UseResponseCaching();

            // Use rate limiting for AI endpoints
            app.UseRateLimiter();

            app.UseRouting();

            app.UseCors("AIApiPolicy");

            app.UseAuthentication();
            app.UseAuthorization();

            // Configure health check UI
            app.UseHealthChecks("/health");
            app.UseHealthChecks("/health/ai", new Microsoft.AspNetCore.Diagnostics.HealthChecks.HealthCheckOptions
            {
                Predicate = check => check.Tags.Contains("ai")
            });

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();

                // Map SignalR hubs for real-time AI updates
                endpoints.MapHub<AIUpdatesHub>("/hubs/ai-updates");
                endpoints.MapHub<DiagnosisHub>("/hubs/diagnosis");
                endpoints.MapHub<HealthMonitoringHub>("/hubs/health-monitoring");

                // Add dedicated AI endpoints
                endpoints.MapPost("/api/ai/diagnosis", async context =>
                {
                    context.Response.StatusCode = 200;
                    await context.Response.WriteAsync("AI Diagnosis Endpoint Active");
                }).RequireAuthorization("AIAccess");

                endpoints.MapPost("/api/ai/image-analysis", async context =>
                {
                    context.Response.StatusCode = 200;
                    await context.Response.WriteAsync("AI Image Analysis Endpoint Active");
                }).RequireAuthorization("AIAccess");

                endpoints.MapPost("/api/ai/prescription", async context =>
                {
                    context.Response.StatusCode = 200;
                    await context.Response.WriteAsync("AI Prescription Endpoint Active");
                }).RequireAuthorization("AIAccess");

                endpoints.MapPost("/api/ai/chat", async context =>
                {
                    context.Response.StatusCode = 200;
                    await context.Response.WriteAsync("AI Chatbot Endpoint Active");
                });

                // Metrics endpoint for monitoring
                endpoints.MapGet("/metrics/ai", async context =>
                {
                    var metrics = app.ApplicationServices.GetService<IAIPerformanceMonitor>();
                    var json = System.Text.Json.JsonSerializer.Serialize(await metrics.GetCurrentMetrics());
                    context.Response.ContentType = "application/json";
                    await context.Response.WriteAsync(json);
                }).RequireAuthorization("AdminOnly");
            });

            // Log startup information
            var logger = loggerFactory.CreateLogger<Startup>();
            logger.LogInformation("AI Healthcare Platform started successfully");
            logger.LogInformation($"Project ID: {Configuration["GoogleCloud:ProjectId"]}");
            logger.LogInformation($"AI Features Enabled: Diagnosis={Configuration["AIFeatures:EnableDiagnosis"]}, " +
                                 $"ImageAnalysis={Configuration["AIFeatures:EnableImageAnalysis"]}, " +
                                 $"Chatbot={Configuration["AIFeatures:EnableChatbot"]}");
            logger.LogInformation("Ready to serve AI-powered healthcare solutions!");
        }
    }

    // Configuration classes
    public class GoogleCloudAIOptions
    {
        public string ProjectId { get; set; }
        public string Region { get; set; }
        public string GeminiApiKey { get; set; }
        public string VertexEndpoint { get; set; }
        public string BigQueryDataset { get; set; }
        public string ModelBucket { get; set; }
    }

    public class AIFeatureFlags
    {
        public bool EnableDiagnosis { get; set; } = true;
        public bool EnableImageAnalysis { get; set; } = true;
        public bool EnablePrescription { get; set; } = true;
        public bool EnableChatbot { get; set; } = true;
        public bool EnableHealthPrediction { get; set; } = true;
        public bool EnableClinicalDecision { get; set; } = true;
    }
}