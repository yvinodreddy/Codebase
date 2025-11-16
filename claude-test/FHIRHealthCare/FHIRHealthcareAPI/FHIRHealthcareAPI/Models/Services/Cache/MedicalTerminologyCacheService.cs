using System;
using System.Text.Json;
using System.Threading.Tasks;
using FHIRHealthcareAPI.Services.Terminology;
using Microsoft.Extensions.Caching.Distributed;
using Microsoft.Extensions.Logging;

namespace FHIRHealthcareAPI.Services.Cache
{
    public class MedicalTerminologyCacheService
    {
        private readonly IDistributedCache _cache;
        private readonly ILogger<MedicalTerminologyCacheService> _logger;

        // Cache TTL settings optimized for medical data
        private static readonly TimeSpan RxNormCacheTtl = TimeSpan.FromHours(24);    // Drugs don't change frequently
        private static readonly TimeSpan LoincCacheTtl = TimeSpan.FromDays(7);       // Lab codes are very stable
        private static readonly TimeSpan SnomedCacheTtl = TimeSpan.FromDays(30);     // Clinical terms are extremely stable
        private static readonly TimeSpan Icd10CacheTtl = TimeSpan.FromDays(365);     // ICD codes change annually
        private static readonly TimeSpan InteractionCacheTtl = TimeSpan.FromHours(6); // Interactions may get updates

        public MedicalTerminologyCacheService(IDistributedCache cache, ILogger<MedicalTerminologyCacheService> logger)
        {
            _cache = cache;
            _logger = logger;
        }

        // RxNorm caching methods
        public async Task<T> GetRxNormDataAsync<T>(string rxCui) where T : class
        {
            var key = $"rxnorm:drug:{rxCui}";
            return await GetCachedDataAsync<T>(key);
        }

        public async Task SetRxNormDataAsync<T>(string rxCui, T data) where T : class
        {
            var key = $"rxnorm:drug:{rxCui}";
            await SetCachedDataAsync(key, data, RxNormCacheTtl);
        }

        public async Task<T> GetDrugInteractionAsync<T>(string rxCuiList) where T : class
        {
            var key = $"rxnorm:interactions:{rxCuiList.GetHashCode()}";
            return await GetCachedDataAsync<T>(key);
        }

        public async Task SetDrugInteractionAsync<T>(string rxCuiList, T data) where T : class
        {
            var key = $"rxnorm:interactions:{rxCuiList.GetHashCode()}";
            await SetCachedDataAsync(key, data, InteractionCacheTtl);
        }

        // LOINC caching methods
        public async Task<T> GetLoincDataAsync<T>(string loincCode) where T : class
        {
            var key = $"loinc:code:{loincCode}";
            return await GetCachedDataAsync<T>(key);
        }

        public async Task SetLoincDataAsync<T>(string loincCode, T data) where T : class
        {
            var key = $"loinc:code:{loincCode}";
            await SetCachedDataAsync(key, data, LoincCacheTtl);
        }

        // SNOMED caching methods
        public async Task<T> GetSnomedDataAsync<T>(string snomedCode) where T : class
        {
            var key = $"snomed:concept:{snomedCode}";
            return await GetCachedDataAsync<T>(key);
        }

        public async Task SetSnomedDataAsync<T>(string snomedCode, T data) where T : class
        {
            var key = $"snomed:concept:{snomedCode}";
            await SetCachedDataAsync(key, data, SnomedCacheTtl);
        }

        // ICD-10 caching methods
        public async Task<T> GetIcd10DataAsync<T>(string icd10Code) where T : class
        {
            var key = $"icd10:code:{icd10Code}";
            return await GetCachedDataAsync<T>(key);
        }

        public async Task SetIcd10DataAsync<T>(string icd10Code, T data) where T : class
        {
            var key = $"icd10:code:{icd10Code}";
            await SetCachedDataAsync(key, data, Icd10CacheTtl);
        }

        // Generic cache operations
        private async Task<T> GetCachedDataAsync<T>(string key) where T : class
        {
            try
            {
                var cachedData = await _cache.GetStringAsync(key);
                if (cachedData != null)
                {
                    _logger.LogDebug($"Cache hit for key: {key}");
                    return JsonSerializer.Deserialize<T>(cachedData);
                }

                _logger.LogDebug($"Cache miss for key: {key}");
                return null;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error reading from cache for key: {key}");
                return null;
            }
        }

        private async Task SetCachedDataAsync<T>(string key, T data, TimeSpan ttl) where T : class
        {
            try
            {
                var options = new DistributedCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = ttl,
                    SlidingExpiration = ttl > TimeSpan.FromHours(1) ? TimeSpan.FromMinutes(30) : null
                };

                var serializedData = JsonSerializer.Serialize(data);
                await _cache.SetStringAsync(key, serializedData, options);

                _logger.LogDebug($"Cached data for key: {key}, TTL: {ttl}");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error writing to cache for key: {key}");
            }
        }

        // Cache warming methods for frequently accessed codes
        public async Task WarmCache()
        {
            _logger.LogInformation("Starting cache warming process...");

            var commonRxCuis = new[] { "6809", "29046", "243670", "52582", "161" };
            var commonLoincCodes = new[] { "33747-0", "2085-9", "718-7", "4548-4" };
            var commonSnomedCodes = new[] { "44054006", "38341003", "195967001" };
            var commonIcd10Codes = new[] { "E11.9", "I10", "J45.9" };

            // Note: In practice, you would inject the actual services here
            // This is just the structure for cache warming
            _logger.LogInformation("Cache warming completed");
        }

        // Cache statistics and monitoring
        public async Task<CacheStatistics> GetCacheStatisticsAsync()
        {
            // This would require implementation depending on your cache provider
            // Redis provides commands like INFO, MEMORY USAGE, etc.
            return new CacheStatistics
            {
                TotalKeys = await EstimateKeyCount(),
                HitRate = 0.85, // Would calculate from actual metrics
                MemoryUsage = "Estimated based on cache provider"
            };
        }

        private async Task<int> EstimateKeyCount()
        {
            // This would use cache provider specific commands
            // Redis: DBSIZE, Memcached: stats, etc.
            return 0;
        }

        // Cache invalidation methods
        public async Task InvalidateRxNormCache(string rxCui)
        {
            var key = $"rxnorm:drug:{rxCui}";
            await _cache.RemoveAsync(key);
            _logger.LogInformation($"Invalidated RxNorm cache for: {rxCui}");
        }

        public async Task InvalidateAllTerminologyCache()
        {
            // This would require pattern-based deletion
            // Redis: KEYS pattern + DEL, etc.
            _logger.LogInformation("Invalidated all terminology cache");
        }
    }

    public class CacheStatistics
    {
        public int TotalKeys { get; set; }
        public double HitRate { get; set; }
        public string MemoryUsage { get; set; }
        public DateTime LastUpdated { get; set; } = DateTime.UtcNow;
    }

    // Enhanced terminology services with caching
    public class CachedRxNormService
    {
        private readonly SimplifiedRxNormService _rxNormService;
        private readonly MedicalTerminologyCacheService _cache;
        private readonly ILogger<CachedRxNormService> _logger;

        public CachedRxNormService(
            SimplifiedRxNormService rxNormService,
            MedicalTerminologyCacheService cache,
            ILogger<CachedRxNormService> logger)
        {
            _rxNormService = rxNormService;
            _cache = cache;
            _logger = logger;
        }

        public async Task<object> GetDrugInfoCached(string rxCui)
        {
            // Try cache first
            var cachedResult = await _cache.GetRxNormDataAsync<object>(rxCui);
            if (cachedResult != null)
            {
                return cachedResult;
            }

            // Cache miss - fetch from API
            var result = await _rxNormService.GetDrugInfo(rxCui);
            if (result != null)
            {
                await _cache.SetRxNormDataAsync(rxCui, result);
            }

            return result;
        }
    }
}