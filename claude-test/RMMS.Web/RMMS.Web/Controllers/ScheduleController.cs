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
    public class ScheduleController : Controller
    {
        private readonly ILogger<ScheduleController> _logger;
        private readonly ApplicationDbContext _context;

        public ScheduleController(ILogger<ScheduleController> logger, ApplicationDbContext context)
        {
            _logger = logger;
            _context = context;
        }

        /// <summary>
        /// Production Schedule Calendar - Phase 2 Feature
        /// </summary>
        public IActionResult Calendar()
        {
            _logger.LogInformation("Production schedule calendar accessed");
            return View();
        }

        /// <summary>
        /// Get calendar events (API endpoint)
        /// </summary>
        [HttpGet]
        public async Task<IActionResult> GetEvents(DateTime? start, DateTime? end)
        {
            try
            {
                _logger.LogInformation($"Getting calendar events from {start} to {end}");

                var query = _context.ScheduleEvents
                    .Where(e => e.IsActive);

                // Filter by date range if provided
                if (start.HasValue)
                {
                    query = query.Where(e => e.StartDateTime >= start.Value || (e.EndDateTime.HasValue && e.EndDateTime.Value >= start.Value));
                }

                if (end.HasValue)
                {
                    query = query.Where(e => e.StartDateTime <= end.Value);
                }

                var events = await query.ToListAsync();

                // Transform to FullCalendar format
                var calendarEvents = events.Select(e => new
                {
                    id = e.Id,
                    title = e.Title,
                    start = e.StartDateTime.ToString("yyyy-MM-ddTHH:mm:ss"),
                    end = e.EndDateTime?.ToString("yyyy-MM-ddTHH:mm:ss"),
                    allDay = e.AllDay,
                    backgroundColor = e.Color ?? GetColorForEventType(e.EventType),
                    borderColor = e.Color ?? GetColorForEventType(e.EventType),
                    extendedProps = new
                    {
                        description = e.Description,
                        type = e.EventType,
                        status = e.Status,
                        location = e.Location,
                        assignedTo = e.AssignedTo,
                        referenceNumber = e.ReferenceNumber
                    }
                }).ToList();

                return Json(calendarEvents);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting calendar events");
                return Json(new { success = false, message = "Error loading events" });
            }
        }

        /// <summary>
        /// Save calendar event (API endpoint)
        /// </summary>
        [HttpPost]
        public async Task<IActionResult> SaveEvent([FromBody] ScheduleEventDto eventData)
        {
            try
            {
                _logger.LogInformation("Saving calendar event");

                var scheduleEvent = new ScheduleEvent
                {
                    Title = eventData.Title,
                    EventType = eventData.Type,
                    StartDateTime = DateTime.Parse(eventData.Start),
                    EndDateTime = !string.IsNullOrEmpty(eventData.End) ? DateTime.Parse(eventData.End) : null,
                    AllDay = eventData.AllDay,
                    Description = eventData.Description,
                    Color = GetColorForEventType(eventData.Type),
                    Status = "Planned",
                    CreatedDate = DateTime.Now,
                    IsActive = true
                };

                _context.ScheduleEvents.Add(scheduleEvent);
                await _context.SaveChangesAsync();

                return Json(new
                {
                    success = true,
                    message = "Event saved successfully",
                    eventId = scheduleEvent.Id
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error saving calendar event");
                return Json(new { success = false, message = "Error saving event" });
            }
        }

        /// <summary>
        /// Update calendar event (API endpoint)
        /// </summary>
        [HttpPut]
        public async Task<IActionResult> UpdateEvent(int id, [FromBody] ScheduleEventDto eventData)
        {
            try
            {
                var scheduleEvent = await _context.ScheduleEvents.FindAsync(id);

                if (scheduleEvent == null)
                {
                    return Json(new { success = false, message = "Event not found" });
                }

                scheduleEvent.Title = eventData.Title;
                scheduleEvent.EventType = eventData.Type;
                scheduleEvent.StartDateTime = DateTime.Parse(eventData.Start);
                scheduleEvent.EndDateTime = !string.IsNullOrEmpty(eventData.End) ? DateTime.Parse(eventData.End) : null;
                scheduleEvent.AllDay = eventData.AllDay;
                scheduleEvent.Description = eventData.Description;
                scheduleEvent.Color = GetColorForEventType(eventData.Type);
                scheduleEvent.UpdatedDate = DateTime.Now;

                await _context.SaveChangesAsync();

                return Json(new { success = true, message = "Event updated successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating calendar event {id}");
                return Json(new { success = false, message = "Error updating event" });
            }
        }

        /// <summary>
        /// Delete calendar event (API endpoint)
        /// </summary>
        [HttpDelete]
        public async Task<IActionResult> DeleteEvent(int id)
        {
            try
            {
                var scheduleEvent = await _context.ScheduleEvents.FindAsync(id);

                if (scheduleEvent == null)
                {
                    return Json(new { success = false, message = "Event not found" });
                }

                // Soft delete
                scheduleEvent.IsActive = false;
                await _context.SaveChangesAsync();

                return Json(new { success = true, message = "Event deleted successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting calendar event {id}");
                return Json(new { success = false, message = "Error deleting event" });
            }
        }

        /// <summary>
        /// Move/resize event (drag & drop support)
        /// </summary>
        [HttpPost]
        public async Task<IActionResult> MoveEvent(int id, [FromBody] MoveEventDto moveData)
        {
            try
            {
                var scheduleEvent = await _context.ScheduleEvents.FindAsync(id);

                if (scheduleEvent == null)
                {
                    return Json(new { success = false, message = "Event not found" });
                }

                scheduleEvent.StartDateTime = DateTime.Parse(moveData.Start);

                if (!string.IsNullOrEmpty(moveData.End))
                {
                    scheduleEvent.EndDateTime = DateTime.Parse(moveData.End);
                }

                scheduleEvent.UpdatedDate = DateTime.Now;
                await _context.SaveChangesAsync();

                return Json(new { success = true, message = "Event moved successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error moving calendar event {id}");
                return Json(new { success = false, message = "Error moving event" });
            }
        }

        private string GetColorForEventType(string eventType)
        {
            return eventType switch
            {
                "production" => "#28a745",      // Green
                "procurement" => "#0090d2",     // Blue
                "delivery" => "#ffc107",         // Yellow
                "maintenance" => "#dc3545",      // Red
                "quality" => "#17a2b8",          // Info
                _ => "#6c757d"                   // Gray
            };
        }
    }

    // DTO classes for API
    public class ScheduleEventDto
    {
        public string Title { get; set; } = string.Empty;
        public string Type { get; set; } = string.Empty;
        public string Start { get; set; } = string.Empty;
        public string? End { get; set; }
        public bool AllDay { get; set; }
        public string? Description { get; set; }
    }

    public class MoveEventDto
    {
        public string Start { get; set; } = string.Empty;
        public string? End { get; set; }
    }
}
