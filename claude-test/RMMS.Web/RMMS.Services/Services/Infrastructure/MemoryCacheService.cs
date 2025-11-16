using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using System;
using System.Threading.Tasks;

namespace RMMS.Services.Services.Infrastructure
{
    /// <summary>
    /// Memory-based caching service implementation
    /// </summary>
    public class MemoryCacheService : ICacheService
    {
        private readonly IMemoryCache _cache;
        private readonly ILogger<MemoryCacheService> _logger;
        private static readonly TimeSpan DefaultExpiration = TimeSpan.FromMinutes(5);

        public MemoryCacheService(IMemoryCache cache, ILogger<MemoryCacheService> logger)
        {
            _cache = cache ?? throw new ArgumentNullException(nameof(cache));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        public async Task<T> GetOrCreateAsync<T>(string key, Func<Task<T>> factory, TimeSpan? expiration = null)
        {
            if (string.IsNullOrEmpty(key))
                throw new ArgumentNullException(nameof(key));

            if (factory == null)
                throw new ArgumentNullException(nameof(factory));

            // Try to get from cache
            if (_cache.TryGetValue(key, out T? cachedValue) && cachedValue != null)
            {
                _logger.LogDebug("Cache HIT for key: {CacheKey}", key);
                return cachedValue;
            }

            // Cache miss - create new value
            _logger.LogDebug("Cache MISS for key: {CacheKey}", key);

            try
            {
                var value = await factory();

                var cacheOptions = new MemoryCacheEntryOptions
                {
                    AbsoluteExpirationRelativeToNow = expiration ?? DefaultExpiration,
                    SlidingExpiration = TimeSpan.FromMinutes(2), // Renew if accessed within 2 min of expiry
                    Priority = CacheItemPriority.Normal
                };

                // Set callback for logging when items are removed
                cacheOptions.RegisterPostEvictionCallback((key, value, reason, state) =>
                {
                    _logger.LogDebug("Cache item removed: {CacheKey}, Reason: {Reason}", key, reason);
                });

                _cache.Set(key, value, cacheOptions);
                _logger.LogInformation("Cached item: {CacheKey}, Expires in: {Expiration}", key, expiration ?? DefaultExpiration);

                return value;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating cached value for key: {CacheKey}", key);
                throw;
            }
        }

        public void Remove(string key)
        {
            if (string.IsNullOrEmpty(key))
                return;

            _cache.Remove(key);
            _logger.LogInformation("Removed cache item: {CacheKey}", key);
        }

        public void Clear()
        {
            // Note: IMemoryCache doesn't have a built-in Clear method
            // In production, you might want to track keys separately or use a different cache provider
            _logger.LogWarning("Clear operation called - IMemoryCache doesn't support clearing all entries");
        }

        public bool Exists(string key)
        {
            if (string.IsNullOrEmpty(key))
                return false;

            return _cache.TryGetValue(key, out _);
        }

        public bool TryGetValue<T>(string key, out T? value)
        {
            if (string.IsNullOrEmpty(key))
            {
                value = default;
                return false;
            }

            return _cache.TryGetValue(key, out value);
        }
    }
}
