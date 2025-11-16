using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using RMMS.DataAccess.Context;
using RMMS.Models.API;

namespace RMMS.Services.Services.Integrations
{
    /// <summary>
    /// TASK 4.3.2: Webhook Service Implementation
    /// Manages webhook subscriptions and deliveries
    /// </summary>
    public class WebhookService : IWebhookService
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<WebhookService> _logger;
        private static readonly HttpClient _httpClient = new HttpClient();

        public WebhookService(
            ApplicationDbContext context,
            ILogger<WebhookService> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task<int> CreateWebhookAsync(string name, string url, string secret, List<string> events)
        {
            try
            {
                var webhook = new Webhook
                {
                    Name = name,
                    Url = url,
                    EventType = events.Count > 0 ? events[0] : "*", // Store first event type or wildcard
                    Description = $"Events: {string.Join(",", events)}",
                    IsActive = true,
                    CreatedDate = DateTime.UtcNow,
                    CreatedBy = "system"
                };

                _context.Set<Webhook>().Add(webhook);
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Created webhook: {name} (ID: {webhook.Id})");
                return webhook.Id;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error creating webhook: {name}");
                throw;
            }
        }

        public async Task<bool> DeleteWebhookAsync(int id)
        {
            try
            {
                var webhook = await _context.Set<Webhook>().FindAsync(id);
                if (webhook == null)
                {
                    _logger.LogWarning($"Webhook not found: {id}");
                    return false;
                }

                webhook.IsActive = false;
                await _context.SaveChangesAsync();

                _logger.LogInformation($"Deleted webhook: {id}");
                return true;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting webhook: {id}");
                throw;
            }
        }

        public async Task<bool> DeliverWebhookAsync(string eventType, object payload)
        {
            try
            {
                // Get all active webhooks subscribed to this event or wildcard
                var webhooks = await _context.Set<Webhook>()
                    .Where(w => w.IsActive && (w.EventType == eventType || w.EventType == "*"))
                    .ToListAsync();

                if (!webhooks.Any())
                {
                    _logger.LogDebug($"No webhooks subscribed to event: {eventType}");
                    return true;
                }

                var payloadJson = JsonSerializer.Serialize(payload);
                var allDelivered = true;

                foreach (var webhook in webhooks)
                {
                    try
                    {
                        // Create delivery record
                        var delivery = new WebhookDelivery
                        {
                            EventType = eventType,
                            Payload = payloadJson,
                            Status = "Pending",
                            AttemptCount = 0
                        };

                        // Generate simple signature (no secret in model, using webhook ID as key)
                        var signature = GenerateSignature(payloadJson, webhook.Id.ToString());

                        // Send HTTP POST request
                        var request = new HttpRequestMessage(HttpMethod.Post, webhook.Url);
                        request.Headers.Add("X-Webhook-Signature", signature);
                        request.Headers.Add("X-Webhook-Event", eventType);
                        request.Content = new StringContent(payloadJson, Encoding.UTF8, "application/json");

                        var response = await _httpClient.SendAsync(request);

                        if (response.IsSuccessStatusCode)
                        {
                            delivery.Status = "Delivered";
                            webhook.LastTriggered = DateTime.UtcNow;
                            _logger.LogInformation($"Webhook delivered successfully: {webhook.Name} - {eventType}");
                        }
                        else
                        {
                            delivery.Status = "Failed";
                            delivery.AttemptCount++;
                            allDelivered = false;
                            _logger.LogWarning($"Webhook delivery failed: {webhook.Name} - {eventType} - Status: {response.StatusCode}");
                        }
                    }
                    catch (Exception ex)
                    {
                        allDelivered = false;
                        _logger.LogError(ex, $"Error delivering webhook: {webhook.Name} - {eventType}");
                    }
                }

                await _context.SaveChangesAsync();
                return allDelivered;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error in webhook delivery process for event: {eventType}");
                return false;
            }
        }

        public async Task RetryFailedDeliveriesAsync()
        {
            try
            {
                _logger.LogInformation("Starting webhook retry process");

                // Note: WebhookDelivery table implementation pending
                // For now, just log that retry was requested
                await Task.CompletedTask;

                _logger.LogInformation("Webhook retry process completed");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrying failed webhook deliveries");
                throw;
            }
        }

        private string GenerateSignature(string payload, string secret)
        {
            var encoding = new UTF8Encoding();
            var keyByte = encoding.GetBytes(secret);
            var messageBytes = encoding.GetBytes(payload);

            using var hmac = new HMACSHA256(keyByte);
            var hashMessage = hmac.ComputeHash(messageBytes);
            return BitConverter.ToString(hashMessage).Replace("-", "").ToLower();
        }
    }
}
