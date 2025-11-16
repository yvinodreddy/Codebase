using System.IO;
using System.Threading.Tasks;

namespace RMMS.Services.Interfaces.Mobile
{
    /// <summary>
    /// Service for optimizing images for mobile devices
    /// </summary>
    public interface IImageOptimizationService
    {
        /// <summary>
        /// Compress an image to reduce file size
        /// </summary>
        Task<byte[]> CompressImageAsync(byte[] imageData, int quality = 80);

        /// <summary>
        /// Generate thumbnail from image
        /// </summary>
        Task<byte[]> GenerateThumbnailAsync(byte[] imageData, int maxWidth, int maxHeight);

        /// <summary>
        /// Resize image to specific dimensions
        /// </summary>
        Task<byte[]> ResizeImageAsync(byte[] imageData, int width, int height, bool maintainAspectRatio = true);

        /// <summary>
        /// Convert image to WebP format (more efficient for mobile)
        /// </summary>
        Task<byte[]> ConvertToWebPAsync(byte[] imageData, int quality = 80);

        /// <summary>
        /// Get image dimensions without loading full image
        /// </summary>
        Task<(int width, int height)> GetImageDimensionsAsync(byte[] imageData);

        /// <summary>
        /// Validate image size and format
        /// </summary>
        Task<(bool isValid, string? errorMessage)> ValidateImageAsync(byte[] imageData, int maxSizeMB = 10);
    }
}
