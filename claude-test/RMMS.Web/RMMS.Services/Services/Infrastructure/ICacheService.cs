using System;
using System.Threading.Tasks;

namespace RMMS.Services.Services.Infrastructure
{
    /// <summary>
    /// Caching service interface for improving application performance
    /// </summary>
    public interface ICacheService
    {
        /// <summary>
        /// Gets cached value or creates it using the provided factory function
        /// </summary>
        /// <typeparam name="T">Type of the cached value</typeparam>
        /// <param name="key">Cache key</param>
        /// <param name="factory">Factory function to create the value if not in cache</param>
        /// <param name="expiration">Cache expiration time (default: 5 minutes)</param>
        /// <returns>Cached or newly created value</returns>
        Task<T> GetOrCreateAsync<T>(string key, Func<Task<T>> factory, TimeSpan? expiration = null);

        /// <summary>
        /// Removes a specific item from cache
        /// </summary>
        /// <param name="key">Cache key to remove</param>
        void Remove(string key);

        /// <summary>
        /// Clears all items from cache
        /// </summary>
        void Clear();

        /// <summary>
        /// Checks if a key exists in cache
        /// </summary>
        /// <param name="key">Cache key to check</param>
        /// <returns>True if key exists, false otherwise</returns>
        bool Exists(string key);

        /// <summary>
        /// Gets a value from cache without creating it
        /// </summary>
        /// <typeparam name="T">Type of the cached value</typeparam>
        /// <param name="key">Cache key</param>
        /// <param name="value">Output value if found</param>
        /// <returns>True if value was found, false otherwise</returns>
        bool TryGetValue<T>(string key, out T? value);
    }
}
