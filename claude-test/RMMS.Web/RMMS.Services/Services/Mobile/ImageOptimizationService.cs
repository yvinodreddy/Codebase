using Microsoft.Extensions.Logging;
using RMMS.Services.Interfaces.Mobile;
using System;
using System.IO;
using System.Threading.Tasks;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Processing;
using SixLabors.ImageSharp.Formats;
using SixLabors.ImageSharp.Formats.Jpeg;
using SixLabors.ImageSharp.Formats.Png;
using SixLabors.ImageSharp.Formats.Webp;

namespace RMMS.Services.Services.Mobile
{
    public class ImageOptimizationService : IImageOptimizationService
    {
        private readonly ILogger<ImageOptimizationService> _logger;

        public ImageOptimizationService(ILogger<ImageOptimizationService> logger)
        {
            _logger = logger;
        }

        public async Task<byte[]> CompressImageAsync(byte[] imageData, int quality = 80)
        {
            try
            {
                using var image = Image.Load(imageData);
                using var outputStream = new MemoryStream();

                var encoder = new JpegEncoder
                {
                    Quality = quality
                };

                await image.SaveAsync(outputStream, encoder);
                return outputStream.ToArray();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error compressing image");
                throw;
            }
        }

        public async Task<byte[]> GenerateThumbnailAsync(byte[] imageData, int maxWidth, int maxHeight)
        {
            try
            {
                using var image = Image.Load(imageData);

                // Calculate thumbnail size maintaining aspect ratio
                double ratioX = (double)maxWidth / image.Width;
                double ratioY = (double)maxHeight / image.Height;
                double ratio = Math.Min(ratioX, ratioY);

                int newWidth = (int)(image.Width * ratio);
                int newHeight = (int)(image.Height * ratio);

                image.Mutate(x => x.Resize(newWidth, newHeight));

                using var outputStream = new MemoryStream();
                var encoder = new JpegEncoder { Quality = 85 };
                await image.SaveAsync(outputStream, encoder);

                return outputStream.ToArray();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error generating thumbnail");
                throw;
            }
        }

        public async Task<byte[]> ResizeImageAsync(byte[] imageData, int width, int height, bool maintainAspectRatio = true)
        {
            try
            {
                using var image = Image.Load(imageData);

                if (maintainAspectRatio)
                {
                    image.Mutate(x => x.Resize(new ResizeOptions
                    {
                        Size = new Size(width, height),
                        Mode = ResizeMode.Max
                    }));
                }
                else
                {
                    image.Mutate(x => x.Resize(width, height));
                }

                using var outputStream = new MemoryStream();
                await image.SaveAsync(outputStream, image.Metadata.DecodedImageFormat ?? JpegFormat.Instance);

                return outputStream.ToArray();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error resizing image");
                throw;
            }
        }

        public async Task<byte[]> ConvertToWebPAsync(byte[] imageData, int quality = 80)
        {
            try
            {
                using var image = Image.Load(imageData);
                using var outputStream = new MemoryStream();

                var encoder = new WebpEncoder
                {
                    Quality = quality
                };

                await image.SaveAsync(outputStream, encoder);
                return outputStream.ToArray();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error converting image to WebP");
                throw;
            }
        }

        public async Task<(int width, int height)> GetImageDimensionsAsync(byte[] imageData)
        {
            try
            {
                var imageInfo = await Image.IdentifyAsync(new MemoryStream(imageData));
                return (imageInfo.Width, imageInfo.Height);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting image dimensions");
                throw;
            }
        }

        public async Task<(bool isValid, string? errorMessage)> ValidateImageAsync(byte[] imageData, int maxSizeMB = 10)
        {
            try
            {
                // Check file size
                double sizeMB = imageData.Length / (1024.0 * 1024.0);
                if (sizeMB > maxSizeMB)
                {
                    return (false, $"Image size ({sizeMB:F2} MB) exceeds maximum allowed size ({maxSizeMB} MB)");
                }

                // Try to load the image to validate format
                using var image = await Image.LoadAsync(new MemoryStream(imageData));

                // Check dimensions (optional - set reasonable limits)
                const int maxDimension = 10000;
                if (image.Width > maxDimension || image.Height > maxDimension)
                {
                    return (false, $"Image dimensions ({image.Width}x{image.Height}) exceed maximum allowed ({maxDimension}x{maxDimension})");
                }

                return (true, null);
            }
            catch (UnknownImageFormatException)
            {
                return (false, "Invalid or unsupported image format");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error validating image");
                return (false, $"Image validation error: {ex.Message}");
            }
        }
    }
}
