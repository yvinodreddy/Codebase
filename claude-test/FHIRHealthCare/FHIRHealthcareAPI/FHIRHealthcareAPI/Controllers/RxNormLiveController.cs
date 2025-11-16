using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;

namespace FHIRHealthcareAPI.Controllers
{
    [ApiController]
    [Route("api/rxnorm-live")]
    [AllowAnonymous] // For initial testing
    public class RxNormLiveController : ControllerBase
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<RxNormLiveController> _logger;

        public RxNormLiveController(IHttpClientFactory httpClientFactory, ILogger<RxNormLiveController> logger)
        {
            _httpClient = httpClientFactory.CreateClient();
            _logger = logger;
        }

        /// <summary>
        /// Get drug information from RxNorm API
        /// Test with: 6809 (Metformin), 29046 (Lisinopril), 243670 (Aspirin)
        /// </summary>
        [HttpGet("drug/{rxcui}")]
        public async Task<IActionResult> GetDrugInfo(string rxcui)
        {
            try
            {
                var url = $"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/properties.json";
                var response = await _httpClient.GetAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    var json = await response.Content.ReadAsStringAsync();
                    var drugData = JsonDocument.Parse(json);

                    var result = new
                    {
                        success = true,
                        source = "RxNorm Live API",
                        rxcui = rxcui,
                        drugName = ExtractDrugName(drugData),
                        properties = ExtractDrugProperties(drugData),
                        timestamp = DateTime.UtcNow
                    };

                    _logger.LogInformation($"Retrieved drug info for RxCUI: {rxcui}");
                    return Ok(result);
                }

                return NotFound(new { success = false, message = $"RxCUI {rxcui} not found" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error retrieving drug info for RxCUI: {rxcui}");
                return StatusCode(500, new { success = false, error = ex.Message });
            }
        }

        /// <summary>
        /// Check drug interactions between multiple medications
        /// POST body: { "rxcuis": ["6809", "29046"] }
        /// </summary>
        [HttpPost("interactions")]
        public async Task<IActionResult> CheckInteractions([FromBody] RxNormInteractionRequest request)
        {
            try
            {
                if (request.RxCuis == null || request.RxCuis.Count == 0)
                {
                    return BadRequest("At least one RxCUI is required");
                }

                var rxcuiList = string.Join("+", request.RxCuis);
                var url = $"https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={rxcuiList}";

                var response = await _httpClient.GetAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    var json = await response.Content.ReadAsStringAsync();
                    var interactions = ParseInteractions(json);

                    _logger.LogInformation($"Checked interactions for RxCUIs: {string.Join(", ", request.RxCuis)}");

                    return Ok(new
                    {
                        success = true,
                        drugsChecked = request.RxCuis,
                        interactionCount = interactions.Count,
                        interactions = interactions,
                        timestamp = DateTime.UtcNow
                    });
                }

                return Ok(new { success = true, interactions = new List<object>(), message = "No interactions found" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking drug interactions");
                return StatusCode(500, new { success = false, error = ex.Message });
            }
        }

        /// <summary>
        /// Search for medications by name
        /// </summary>
        [HttpGet("search")]
        public async Task<IActionResult> SearchMedications([FromQuery] string name, [FromQuery] int maxResults = 10)
        {
            try
            {
                if (string.IsNullOrEmpty(name))
                {
                    return BadRequest("Medication name is required");
                }

                var url = $"https://rxnav.nlm.nih.gov/REST/drugs.json?name={Uri.EscapeDataString(name)}";
                var response = await _httpClient.GetAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    var json = await response.Content.ReadAsStringAsync();
                    var searchResults = ParseSearchResults(json, maxResults);

                    return Ok(new
                    {
                        success = true,
                        searchTerm = name,
                        resultCount = searchResults.Count,
                        results = searchResults,
                        timestamp = DateTime.UtcNow
                    });
                }

                return Ok(new { success = true, results = new List<object>(), message = "No medications found" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error searching medications for: {name}");
                return StatusCode(500, new { success = false, error = ex.Message });
            }
        }

        private string ExtractDrugName(JsonDocument drugData)
        {
            try
            {
                if (drugData.RootElement.TryGetProperty("properties", out var properties))
                {
                    if (properties.TryGetProperty("name", out var nameElement))
                    {
                        return nameElement.GetString() ?? "Unknown";
                    }
                }
            }
            catch { }
            return "Unknown";
        }

        private Dictionary<string, object> ExtractDrugProperties(JsonDocument drugData)
        {
            var properties = new Dictionary<string, object>();

            try
            {
                if (drugData.RootElement.TryGetProperty("properties", out var propsElement))
                {
                    foreach (var prop in propsElement.EnumerateObject())
                    {
                        properties[prop.Name] = prop.Value.ToString();
                    }
                }
            }
            catch { }

            return properties;
        }

        private List<object> ParseInteractions(string json)
        {
            var interactions = new List<object>();

            try
            {
                var doc = JsonDocument.Parse(json);
                if (doc.RootElement.TryGetProperty("fullInteractionTypeGroup", out var groupArray))
                {
                    foreach (var group in groupArray.EnumerateArray())
                    {
                        if (group.TryGetProperty("fullInteractionType", out var typeArray))
                        {
                            foreach (var type in typeArray.EnumerateArray())
                            {
                                if (type.TryGetProperty("interactionPair", out var pairArray))
                                {
                                    foreach (var pair in pairArray.EnumerateArray())
                                    {
                                        interactions.Add(new
                                        {
                                            severity = type.TryGetProperty("comment", out var comment) ? comment.GetString() : "Unknown",
                                            description = pair.TryGetProperty("description", out var desc) ? desc.GetString() : "No description available"
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
            }
            catch { }

            return interactions;
        }

        private List<object> ParseSearchResults(string json, int maxResults)
        {
            var results = new List<object>();

            try
            {
                var doc = JsonDocument.Parse(json);
                if (doc.RootElement.TryGetProperty("drugGroup", out var drugGroup))
                {
                    if (drugGroup.TryGetProperty("conceptGroup", out var conceptArray))
                    {
                        foreach (var concept in conceptArray.EnumerateArray())
                        {
                            if (concept.TryGetProperty("conceptProperties", out var propsArray))
                            {
                                foreach (var prop in propsArray.EnumerateArray())
                                {
                                    if (results.Count >= maxResults) break;

                                    results.Add(new
                                    {
                                        rxcui = prop.TryGetProperty("rxcui", out var rxcui) ? rxcui.GetString() : "",
                                        name = prop.TryGetProperty("name", out var name) ? name.GetString() : "",
                                        synonym = prop.TryGetProperty("synonym", out var syn) ? syn.GetString() : ""
                                    });
                                }
                            }
                        }
                    }
                }
            }
            catch { }

            return results;
        }
    }

    public class RxNormInteractionRequest
    {
        public List<string> RxCuis { get; set; } = new List<string>();
    }
}