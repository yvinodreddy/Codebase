using Microsoft.Extensions.Caching.Distributed;
using Microsoft.Extensions.Logging;
using System;
using System.Text.Json;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Services.Cache
{
    public interface ICacheService
    {
        Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> factory, TimeSpan? expiration = null);
        Task RemoveAsync(string key);
    }

    public class CacheService : ICacheService
    {
        private readonly IDistributedCache _cache;
        private readonly ILogger<CacheService> _logger;
        private readonly TimeSpan _defaultExpiration = TimeSpan.FromMinutes(30);

        public CacheService(IDistributedCache cache, ILogger<CacheService> logger)
        {
            _cache = cache;
            _logger = logger;
        }

        public async Task<T> GetOrSetAsync<T>(string key, Func<Task<T>> factory, TimeSpan? expiration = null)
        {
            try
            {
                var cachedData = await _cache.GetStringAsync(key);

                if (!string.IsNullOrEmpty(cachedData))
                {
                    _logger.LogDebug($"Cache hit for key: {key}");
                    return JsonSerializer.Deserialize<T>(cachedData);
                }

                _logger.LogDebug($"Cache miss for key: {key}");
                var data = await factory();

                if (data != null)
                {
                    var options = new DistributedCacheEntryOptions
                    {
                        AbsoluteExpirationRelativeToNow = expiration ?? _defaultExpiration
                    };

                    var json = JsonSerializer.Serialize(data);
                    await _cache.SetStringAsync(key, json, options);
                }

                return data;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Cache error for key: {key}");
                return await factory();
            }
        }

        public async Task RemoveAsync(string key)
        {
            await _cache.RemoveAsync(key);
        }
    }
}