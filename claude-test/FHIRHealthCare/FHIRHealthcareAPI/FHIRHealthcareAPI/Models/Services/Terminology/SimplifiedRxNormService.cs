using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using FHIRHealthcareAPI.Services.Cache;
using Microsoft.Extensions.Logging;

namespace FHIRHealthcareAPI.Services.Terminology
{
    public class SimplifiedRxNormService
    {
        private readonly HttpClient _httpClient;
        private readonly ICacheService _cacheService;
        private readonly ILogger<SimplifiedRxNormService> _logger;
        private const string BASE_URL = "https://rxnav.nlm.nih.gov/REST";

        public SimplifiedRxNormService(
            HttpClient httpClient,
            ICacheService cacheService,
            ILogger<SimplifiedRxNormService> logger)
        {
            _httpClient = httpClient;
            _cacheService = cacheService;
            _logger = logger;
        }

        public async Task<DrugInfo> GetDrugInfo(string rxcui)
        {
            var cacheKey = $"rxnorm:drug:{rxcui}";

            return await _cacheService.GetOrSetAsync(cacheKey, async () =>
            {
                try
                {
                    var url = $"{BASE_URL}/rxcui/{rxcui}/properties.json";
                    var response = await _httpClient.GetAsync(url);

                    if (response.IsSuccessStatusCode)
                    {
                        var json = await response.Content.ReadAsStringAsync();
                        using var document = JsonDocument.Parse(json);
                        var root = document.RootElement;

                        if (root.TryGetProperty("properties", out var properties))
                        {
                            return new DrugInfo
                            {
                                RxCui = rxcui,
                                Name = GetJsonString(properties, "name"),
                                Synonym = GetJsonString(properties, "synonym"),
                                Tty = GetJsonString(properties, "tty"),
                                IsValid = true
                            };
                        }
                    }

                    _logger.LogWarning($"Drug not found: {rxcui}");
                    return new DrugInfo { RxCui = rxcui, IsValid = false };
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, $"Error fetching drug info for {rxcui}");
                    throw;
                }
            }, TimeSpan.FromHours(24));
        }

        public async Task<List<DrugInteractionInfo>> GetInteractions(List<string> rxcuis)
        {
            if (rxcuis == null || !rxcuis.Any())
                return new List<DrugInteractionInfo>();

            var rxcuiList = string.Join("+", rxcuis);
            var url = $"{BASE_URL}/interaction/list.json?rxcuis={rxcuiList}";

            try
            {
                var response = await _httpClient.GetAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    var json = await response.Content.ReadAsStringAsync();
                    using var document = JsonDocument.Parse(json);
                    var root = document.RootElement;

                    var interactions = new List<DrugInteractionInfo>();

                    if (root.TryGetProperty("fullInteractionTypeGroup", out var groups))
                    {
                        foreach (var group in groups.EnumerateArray())
                        {
                            var sourceName = GetJsonString(group, "sourceName");

                            if (group.TryGetProperty("fullInteractionType", out var types))
                            {
                                foreach (var type in types.EnumerateArray())
                                {
                                    if (type.TryGetProperty("interactionPair", out var pairs))
                                    {
                                        foreach (var pair in pairs.EnumerateArray())
                                        {
                                            interactions.Add(new DrugInteractionInfo
                                            {
                                                Description = GetJsonString(pair, "description"),
                                                Severity = GetJsonString(pair, "severity"),
                                                Source = sourceName
                                            });
                                        }
                                    }
                                }
                            }
                        }
                    }

                    return interactions;
                }

                return new List<DrugInteractionInfo>();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error fetching drug interactions");
                return new List<DrugInteractionInfo>();
            }
        }

        public async Task<bool> ValidateRxCui(string rxcui)
        {
            var drug = await GetDrugInfo(rxcui);
            return drug.IsValid;
        }

        private string GetJsonString(JsonElement element, string propertyName)
        {
            if (element.TryGetProperty(propertyName, out var value))
            {
                return value.GetString() ?? string.Empty;
            }
            return string.Empty;
        }
    }

    // Models specific to this service
    public class DrugInfo
    {
        public string RxCui { get; set; }
        public string Name { get; set; }
        public string Synonym { get; set; }
        public string Tty { get; set; }
        public bool IsValid { get; set; }
    }

    public class DrugInteractionInfo
    {
        public string Description { get; set; }
        public string Severity { get; set; }
        public string Source { get; set; }
    }
}