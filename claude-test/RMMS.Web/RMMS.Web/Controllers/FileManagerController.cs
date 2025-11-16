using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers
{
    public class FileManagerController : Controller
    {
        private readonly ILogger<FileManagerController> _logger;
        private readonly ApplicationDbContext _context;
        private readonly IWebHostEnvironment _environment;

        public FileManagerController(
            ILogger<FileManagerController> logger,
            ApplicationDbContext context,
            IWebHostEnvironment environment)
        {
            _logger = logger;
            _context = context;
            _environment = environment;
        }

        /// <summary>
        /// File Manager Index Page
        /// </summary>
        public IActionResult Index(string? category = null)
        {
            ViewBag.Category = category;
            return View();
        }

        /// <summary>
        /// Get files list (API)
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetFiles(string? category = null, string? searchTerm = null)
        {
            try
            {
                var query = _context.DocumentFiles
                    .Where(f => f.IsActive);

                if (!string.IsNullOrEmpty(category) && category != "all")
                {
                    query = query.Where(f => f.Category == category);
                }

                if (!string.IsNullOrEmpty(searchTerm))
                {
                    query = query.Where(f =>
                        f.OriginalFileName.Contains(searchTerm) ||
                        (f.Description != null && f.Description.Contains(searchTerm)) ||
                        (f.Tags != null && f.Tags.Contains(searchTerm)));
                }

                var files = await query
                    .OrderByDescending(f => f.UploadedDate)
                    .Select(f => new
                    {
                        id = f.Id,
                        fileName = f.OriginalFileName,
                        category = f.Category,
                        fileSize = f.FileSizeFormatted,
                        uploadedDate = f.UploadedDate.ToString("yyyy-MM-dd HH:mm"),
                        description = f.Description,
                        fileExtension = f.FileExtension,
                        downloadCount = f.DownloadCount,
                        tags = f.Tags
                    })
                    .ToListAsync();

                return Json(new { success = true, files });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting files");
                return Json(new { success = false, message = "Error loading files" });
            }
        }

        /// <summary>
        /// Upload file (API)
        /// </summary>
        [HttpPost]
        public async Task<IActionResult> UploadFile(
            IFormFile file,
            [FromForm] string category,
            [FromForm] string? description = null,
            [FromForm] string? tags = null)
        {
            try
            {
                if (file == null || file.Length == 0)
                {
                    return Json(new { success = false, message = "No file uploaded" });
                }

                // Create uploads directory if it doesn't exist
                var uploadsPath = Path.Combine(_environment.WebRootPath, "uploads", category ?? "general");
                Directory.CreateDirectory(uploadsPath);

                // Generate unique filename
                var uniqueFileName = $"{Guid.NewGuid()}_{Path.GetFileName(file.FileName)}";
                var filePath = Path.Combine(uploadsPath, uniqueFileName);

                // Save file
                using (var stream = new FileStream(filePath, FileMode.Create))
                {
                    await file.CopyToAsync(stream);
                }

                // Save to database
                var documentFile = new DocumentFile
                {
                    FileName = uniqueFileName,
                    OriginalFileName = file.FileName,
                    FilePath = $"/uploads/{category ?? "general"}/{uniqueFileName}",
                    FileExtension = Path.GetExtension(file.FileName),
                    FileSize = file.Length,
                    MimeType = file.ContentType,
                    Category = category ?? "General",
                    Description = description,
                    Tags = tags,
                    UploadedDate = DateTime.Now,
                    IsActive = true
                };

                _context.DocumentFiles.Add(documentFile);
                await _context.SaveChangesAsync();

                return Json(new
                {
                    success = true,
                    message = "File uploaded successfully",
                    fileId = documentFile.Id,
                    fileName = documentFile.OriginalFileName
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error uploading file");
                return Json(new { success = false, message = $"Error uploading file: {ex.Message}" });
            }
        }

        /// <summary>
        /// Download file
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> Download(int id)
        {
            try
            {
                var file = await _context.DocumentFiles.FindAsync(id);

                if (file == null || !file.IsActive)
                {
                    return NotFound();
                }

                var filePath = Path.Combine(_environment.WebRootPath, file.FilePath.TrimStart('/'));

                if (!System.IO.File.Exists(filePath))
                {
                    return NotFound("File not found on disk");
                }

                // Update download count
                file.DownloadCount++;
                file.LastDownloadDate = DateTime.Now;
                await _context.SaveChangesAsync();

                var memory = new MemoryStream();
                using (var stream = new FileStream(filePath, FileMode.Open))
                {
                    await stream.CopyToAsync(memory);
                }
                memory.Position = 0;

                return File(memory, file.MimeType ?? "application/octet-stream", file.OriginalFileName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error downloading file {id}");
                return StatusCode(500, "Error downloading file");
            }
        }

        /// <summary>
        /// Delete file
        /// </summary>
        [HttpDelete]
        public async Task<IActionResult> DeleteFile(int id)
        {
            try
            {
                var file = await _context.DocumentFiles.FindAsync(id);

                if (file == null)
                {
                    return Json(new { success = false, message = "File not found" });
                }

                // Soft delete
                file.IsActive = false;
                file.DeletedDate = DateTime.Now;
                await _context.SaveChangesAsync();

                // Optionally delete physical file
                // var filePath = Path.Combine(_environment.WebRootPath, file.FilePath.TrimStart('/'));
                // if (System.IO.File.Exists(filePath))
                // {
                //     System.IO.File.Delete(filePath);
                // }

                return Json(new { success = true, message = "File deleted successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting file {id}");
                return Json(new { success = false, message = "Error deleting file" });
            }
        }

        /// <summary>
        /// Get file details
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetFileDetails(int id)
        {
            try
            {
                var file = await _context.DocumentFiles.FindAsync(id);

                if (file == null || !file.IsActive)
                {
                    return Json(new { success = false, message = "File not found" });
                }

                var fileDetails = new
                {
                    id = file.Id,
                    originalFileName = file.OriginalFileName,
                    category = file.Category,
                    fileSize = file.FileSizeFormatted,
                    fileSizeBytes = file.FileSize,
                    fileExtension = file.FileExtension,
                    mimeType = file.MimeType,
                    description = file.Description,
                    tags = file.Tags,
                    uploadedDate = file.UploadedDate.ToString("yyyy-MM-dd HH:mm:ss"),
                    downloadCount = file.DownloadCount,
                    lastDownloadDate = file.LastDownloadDate?.ToString("yyyy-MM-dd HH:mm:ss"),
                    version = file.Version,
                    isPublic = file.IsPublic
                };

                return Json(new { success = true, file = fileDetails });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting file details {id}");
                return Json(new { success = false, message = "Error loading file details" });
            }
        }

        /// <summary>
        /// Update file metadata
        /// </summary>
        [HttpPut]
        public async Task<IActionResult> UpdateFileMetadata(
            int id,
            [FromBody] UpdateFileMetadataDto data)
        {
            try
            {
                var file = await _context.DocumentFiles.FindAsync(id);

                if (file == null || !file.IsActive)
                {
                    return Json(new { success = false, message = "File not found" });
                }

                file.Description = data.Description;
                file.Tags = data.Tags;
                file.Category = data.Category;

                await _context.SaveChangesAsync();

                return Json(new { success = true, message = "File metadata updated successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating file metadata {id}");
                return Json(new { success = false, message = "Error updating file metadata" });
            }
        }
    }

    // DTO for file metadata update
    public class UpdateFileMetadataDto
    {
        public string? Description { get; set; }
        public string? Tags { get; set; }
        public string Category { get; set; } = "General";
    }
}
