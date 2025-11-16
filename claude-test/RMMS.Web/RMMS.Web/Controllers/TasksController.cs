using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers
{
    public class TasksController : Controller
    {
        private readonly ILogger<TasksController> _logger;
        private readonly ApplicationDbContext _context;

        public TasksController(ILogger<TasksController> logger, ApplicationDbContext context)
        {
            _logger = logger;
            _context = context;
        }

        /// <summary>
        /// Tasks Index Page
        /// </summary>
        public IActionResult Index(string? status = null)
        {
            ViewBag.Status = status;
            return View();
        }

        /// <summary>
        /// Get tasks list (API)
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetTasks(
            string? status = null,
            string? priority = null,
            string? category = null,
            bool? overdue = null)
        {
            try
            {
                var query = _context.TaskItems
                    .Where(t => t.IsActive && !t.IsDeleted);

                // Filter by status
                if (!string.IsNullOrEmpty(status) && status != "all")
                {
                    query = query.Where(t => t.Status == status);
                }

                // Filter by priority
                if (!string.IsNullOrEmpty(priority) && priority != "all")
                {
                    query = query.Where(t => t.Priority == priority);
                }

                // Filter by category
                if (!string.IsNullOrEmpty(category) && category != "all")
                {
                    query = query.Where(t => t.Category == category);
                }

                // Filter overdue
                if (overdue.HasValue && overdue.Value)
                {
                    var now = DateTime.Now;
                    query = query.Where(t =>
                        t.DueDate.HasValue &&
                        t.DueDate.Value < now &&
                        t.Status != "Completed" &&
                        t.Status != "Cancelled");
                }

                var tasks = await query
                    .OrderByDescending(t => t.CreatedDate)
                    .Select(t => new
                    {
                        id = t.Id,
                        title = t.Title,
                        description = t.Description,
                        priority = t.Priority,
                        status = t.Status,
                        category = t.Category,
                        dueDate = t.DueDate.HasValue ? t.DueDate.Value.ToString("yyyy-MM-dd") : null,
                        assignedTo = t.AssignedToName,
                        progress = t.ProgressPercentage,
                        isOverdue = t.IsOverdue,
                        createdDate = t.CreatedDate.ToString("yyyy-MM-dd HH:mm"),
                        priorityBadgeClass = t.PriorityBadgeClass,
                        statusBadgeClass = t.StatusBadgeClass
                    })
                    .ToListAsync();

                return Json(new { success = true, tasks });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting tasks");
                return Json(new { success = false, message = "Error loading tasks" });
            }
        }

        /// <summary>
        /// Create new task (API)
        /// </summary>
        [HttpPost]
        public async Task<IActionResult> CreateTask([FromBody] TaskItemDto taskData)
        {
            try
            {
                var task = new TaskItem
                {
                    Title = taskData.Title,
                    Description = taskData.Description,
                    Priority = taskData.Priority ?? "Medium",
                    Status = "Pending",
                    Category = taskData.Category,
                    DueDate = !string.IsNullOrEmpty(taskData.DueDate) ? DateTime.Parse(taskData.DueDate) : null,
                    AssignedToName = taskData.AssignedTo,
                    CreatedDate = DateTime.Now,
                    IsActive = true,
                    IsDeleted = false,
                    ProgressPercentage = 0
                };

                _context.TaskItems.Add(task);
                await _context.SaveChangesAsync();

                return Json(new
                {
                    success = true,
                    message = "Task created successfully",
                    taskId = task.Id
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating task");
                return Json(new { success = false, message = "Error creating task" });
            }
        }

        /// <summary>
        /// Update task (API)
        /// </summary>
        [HttpPut]
        public async Task<IActionResult> UpdateTask(int id, [FromBody] TaskItemDto taskData)
        {
            try
            {
                var task = await _context.TaskItems.FindAsync(id);

                if (task == null || task.IsDeleted)
                {
                    return Json(new { success = false, message = "Task not found" });
                }

                task.Title = taskData.Title;
                task.Description = taskData.Description;
                task.Priority = taskData.Priority ?? "Medium";
                task.Status = taskData.Status ?? task.Status;
                task.Category = taskData.Category;
                task.DueDate = !string.IsNullOrEmpty(taskData.DueDate) ? DateTime.Parse(taskData.DueDate) : null;
                task.AssignedToName = taskData.AssignedTo;
                task.ProgressPercentage = taskData.Progress ?? task.ProgressPercentage;
                task.Notes = taskData.Notes;
                task.LastUpdatedDate = DateTime.Now;

                // If status changed to Completed, set completion date
                if (task.Status == "Completed" && task.CompletedDate == null)
                {
                    task.CompletedDate = DateTime.Now;
                    task.ProgressPercentage = 100;
                }

                await _context.SaveChangesAsync();

                return Json(new { success = true, message = "Task updated successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating task {id}");
                return Json(new { success = false, message = "Error updating task" });
            }
        }

        /// <summary>
        /// Delete task (API)
        /// </summary>
        [HttpDelete]
        public async Task<IActionResult> DeleteTask(int id)
        {
            try
            {
                var task = await _context.TaskItems.FindAsync(id);

                if (task == null)
                {
                    return Json(new { success = false, message = "Task not found" });
                }

                // Soft delete
                task.IsDeleted = true;
                task.IsActive = false;
                await _context.SaveChangesAsync();

                return Json(new { success = true, message = "Task deleted successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting task {id}");
                return Json(new { success = false, message = "Error deleting task" });
            }
        }

        /// <summary>
        /// Update task status (Quick update)
        /// </summary>
        [HttpPost]
        public async Task<IActionResult> UpdateStatus(int id, [FromBody] StatusUpdateDto data)
        {
            try
            {
                var task = await _context.TaskItems.FindAsync(id);

                if (task == null || task.IsDeleted)
                {
                    return Json(new { success = false, message = "Task not found" });
                }

                task.Status = data.Status;
                task.LastUpdatedDate = DateTime.Now;

                if (data.Status == "Completed")
                {
                    task.CompletedDate = DateTime.Now;
                    task.ProgressPercentage = 100;
                }
                else if (data.Status == "InProgress" && task.ProgressPercentage == 0)
                {
                    task.ProgressPercentage = 25;
                }

                await _context.SaveChangesAsync();

                return Json(new { success = true, message = "Status updated successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating task status {id}");
                return Json(new { success = false, message = "Error updating status" });
            }
        }

        /// <summary>
        /// Update task progress
        /// </summary>
        [HttpPost]
        public async Task<IActionResult> UpdateProgress(int id, [FromBody] ProgressUpdateDto data)
        {
            try
            {
                var task = await _context.TaskItems.FindAsync(id);

                if (task == null || task.IsDeleted)
                {
                    return Json(new { success = false, message = "Task not found" });
                }

                task.ProgressPercentage = data.Progress;
                task.LastUpdatedDate = DateTime.Now;

                // Auto-update status based on progress
                if (data.Progress == 100)
                {
                    task.Status = "Completed";
                    task.CompletedDate = DateTime.Now;
                }
                else if (data.Progress > 0 && task.Status == "Pending")
                {
                    task.Status = "InProgress";
                }

                await _context.SaveChangesAsync();

                return Json(new { success = true, message = "Progress updated successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating task progress {id}");
                return Json(new { success = false, message = "Error updating progress" });
            }
        }

        /// <summary>
        /// Get task details
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetTaskDetails(int id)
        {
            try
            {
                var task = await _context.TaskItems.FindAsync(id);

                if (task == null || task.IsDeleted)
                {
                    return Json(new { success = false, message = "Task not found" });
                }

                var taskDetails = new
                {
                    id = task.Id,
                    title = task.Title,
                    description = task.Description,
                    priority = task.Priority,
                    status = task.Status,
                    category = task.Category,
                    dueDate = task.DueDate?.ToString("yyyy-MM-dd"),
                    assignedTo = task.AssignedToName,
                    progress = task.ProgressPercentage,
                    notes = task.Notes,
                    tags = task.Tags,
                    createdDate = task.CreatedDate.ToString("yyyy-MM-dd HH:mm:ss"),
                    completedDate = task.CompletedDate?.ToString("yyyy-MM-dd HH:mm:ss"),
                    isOverdue = task.IsOverdue
                };

                return Json(new { success = true, task = taskDetails });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error getting task details {id}");
                return Json(new { success = false, message = "Error loading task details" });
            }
        }

        /// <summary>
        /// Get task statistics
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetStatistics()
        {
            try
            {
                var stats = new
                {
                    total = await _context.TaskItems.CountAsync(t => t.IsActive && !t.IsDeleted),
                    pending = await _context.TaskItems.CountAsync(t => t.IsActive && !t.IsDeleted && t.Status == "Pending"),
                    inProgress = await _context.TaskItems.CountAsync(t => t.IsActive && !t.IsDeleted && t.Status == "InProgress"),
                    completed = await _context.TaskItems.CountAsync(t => t.IsActive && !t.IsDeleted && t.Status == "Completed"),
                    overdue = await _context.TaskItems.CountAsync(t =>
                        t.IsActive &&
                        !t.IsDeleted &&
                        t.DueDate.HasValue &&
                        t.DueDate.Value < DateTime.Now &&
                        t.Status != "Completed" &&
                        t.Status != "Cancelled")
                };

                return Json(new { success = true, stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting task statistics");
                return Json(new { success = false, message = "Error loading statistics" });
            }
        }
    }

    // DTO classes
    public class TaskItemDto
    {
        public string Title { get; set; } = string.Empty;
        public string? Description { get; set; }
        public string? Priority { get; set; }
        public string? Status { get; set; }
        public string? Category { get; set; }
        public string? DueDate { get; set; }
        public string? AssignedTo { get; set; }
        public int? Progress { get; set; }
        public string? Notes { get; set; }
    }

    public class StatusUpdateDto
    {
        public string Status { get; set; } = string.Empty;
    }

    public class ProgressUpdateDto
    {
        public int Progress { get; set; }
    }
}
