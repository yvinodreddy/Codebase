using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using RMMS.DataAccess.Context;
using Microsoft.EntityFrameworkCore;
using RMMS.Models.Monitoring;

namespace RMMS.Web.Controllers.Phase4
{
    [AllowAnonymous] // Temporarily enabled for testing
    public class SignalRConsoleController : Controller
    {
        private readonly ILogger<SignalRConsoleController> _logger;
        private readonly ApplicationDbContext _context;
        private static readonly List<SignalRMessage> _messageLog = new();
        private static int _totalMessagesSent = 0;
        private static int _activeConnections = 0;

        public SignalRConsoleController(ILogger<SignalRConsoleController> logger,
            ApplicationDbContext context)
        {
            _logger = logger;
            _context = context;
        }

        public IActionResult Index()
        {
            try
            {
                // SignalR console statistics
                ViewBag.ActiveConnections = _activeConnections;
                ViewBag.TotalMessagesSent = _totalMessagesSent;
                ViewBag.MessagesInLog = _messageLog.Count;
                ViewBag.LastMessageTime = _messageLog.Any()
                    ? _messageLog.Last().Timestamp.ToString("HH:mm:ss")
                    : "N/A";

                // Message statistics
                var last24Hours = DateTime.Now.AddHours(-24);
                var recentMessages = _messageLog.Where(m => m.Timestamp >= last24Hours).ToList();

                ViewBag.Messages24Hours = recentMessages.Count;
                ViewBag.BroadcastMessages = recentMessages.Count(m => m.Type == "Broadcast");
                ViewBag.DirectMessages = recentMessages.Count(m => m.Type == "Direct");
                ViewBag.GroupMessages = recentMessages.Count(m => m.Type == "Group");

                // Average message rate
                var messagesPerHour = recentMessages.Any()
                    ? Math.Round(recentMessages.Count / 24.0, 2)
                    : 0;
                ViewBag.MessagesPerHour = messagesPerHour;

                // Message types distribution
                var byType = recentMessages.GroupBy(m => m.Type)
                    .Select(g => new {
                        Type = g.Key,
                        Count = g.Count()
                    })
                    .OrderByDescending(x => x.Count)
                    .ToList();

                ViewBag.MessageTypes = byType.Count;
                ViewBag.TopMessageType = byType.FirstOrDefault()?.Type ?? "N/A";

                // Performance metrics
                ViewBag.SystemStatus = _activeConnections > 0 ? "Active" : "Idle";
                ViewBag.StatusClass = _activeConnections > 0 ? "success" : "secondary";

                return View(_messageLog.TakeLast(50).Reverse().ToList());
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading SignalR console");
                TempData["Error"] = "Error loading SignalR console: " + ex.Message;
                return View(new List<SignalRMessage>());
            }
        }

        [HttpGet]
        public IActionResult GetActiveConnections()
        {
            try
            {
                var connections = new
                {
                    activeCount = _activeConnections,
                    timestamp = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"),
                    status = _activeConnections > 0 ? "Active" : "Idle"
                };

                return Json(new { success = true, data = connections });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting active connections");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public IActionResult GetMessageTrace()
        {
            try
            {
                var messages = _messageLog.TakeLast(100).Reverse()
                    .Select(m => new {
                        timestamp = m.Timestamp.ToString("yyyy-MM-dd HH:mm:ss"),
                        type = m.Type,
                        content = m.Content,
                        sender = m.Sender,
                        recipient = m.Recipient ?? "All"
                    });

                return Json(new { success = true, data = messages });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting message trace");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpGet]
        public IActionResult GetStatistics()
        {
            try
            {
                var now = DateTime.Now;
                var lastHour = now.AddHours(-1);
                var recentMessages = _messageLog.Where(m => m.Timestamp >= lastHour).ToList();

                var stats = new
                {
                    totalMessages = _totalMessagesSent,
                    activeConnections = _activeConnections,
                    messagesInLog = _messageLog.Count,
                    messagesLastHour = recentMessages.Count,
                    byType = _messageLog.GroupBy(m => m.Type)
                        .Select(g => new {
                            type = g.Key,
                            count = g.Count()
                        })
                        .OrderByDescending(x => x.count),
                    recentActivity = recentMessages.GroupBy(m => m.Timestamp.Minute)
                        .Select(g => new {
                            minute = g.Key,
                            count = g.Count()
                        })
                        .OrderBy(x => x.minute)
                };

                return Json(new { success = true, data = stats });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting statistics");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public IActionResult BroadcastMessage(string message)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(message))
                {
                    TempData["Error"] = "Message cannot be empty";
                    return RedirectToAction(nameof(Index));
                }

                var signalRMessage = new SignalRMessage
                {
                    Type = "Broadcast",
                    Content = message,
                    Sender = User.Identity?.Name ?? "System",
                    Timestamp = DateTime.Now
                };

                _messageLog.Add(signalRMessage);
                _totalMessagesSent++;

                // Keep only last 1000 messages
                if (_messageLog.Count > 1000)
                    _messageLog.RemoveAt(0);

                _logger.LogInformation($"Broadcast message sent: {message}");
                TempData["Success"] = "Broadcast message sent successfully!";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error broadcasting message");
                TempData["Error"] = "Error: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public IActionResult SendDirectMessage(string recipient, string message)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(message) || string.IsNullOrWhiteSpace(recipient))
                {
                    return Json(new { success = false, message = "Recipient and message are required" });
                }

                var signalRMessage = new SignalRMessage
                {
                    Type = "Direct",
                    Content = message,
                    Sender = User.Identity?.Name ?? "System",
                    Recipient = recipient,
                    Timestamp = DateTime.Now
                };

                _messageLog.Add(signalRMessage);
                _totalMessagesSent++;

                return Json(new { success = true, message = "Direct message sent successfully" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending direct message");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public IActionResult SendGroupMessage(string groupName, string message)
        {
            try
            {
                var signalRMessage = new SignalRMessage
                {
                    Type = "Group",
                    Content = message,
                    Sender = User.Identity?.Name ?? "System",
                    Recipient = groupName,
                    Timestamp = DateTime.Now
                };

                _messageLog.Add(signalRMessage);
                _totalMessagesSent++;

                return Json(new { success = true, message = $"Group message sent to {groupName}" });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error sending group message");
                return Json(new { success = false, message = ex.Message });
            }
        }

        [HttpPost]
        public IActionResult SimulateConnection()
        {
            _activeConnections++;
            _logger.LogInformation($"Simulated connection added. Total: {_activeConnections}");
            TempData["Success"] = $"Connection simulated. Active connections: {_activeConnections}";
            return RedirectToAction(nameof(Index));
        }

        [HttpPost]
        public IActionResult SimulateDisconnection()
        {
            if (_activeConnections > 0)
                _activeConnections--;
            _logger.LogInformation($"Simulated disconnection. Remaining: {_activeConnections}");
            TempData["Success"] = $"Disconnection simulated. Active connections: {_activeConnections}";
            return RedirectToAction(nameof(Index));
        }

        [HttpPost]
        public IActionResult ClearMessageLog()
        {
            try
            {
                var count = _messageLog.Count;
                _messageLog.Clear();
                TempData["Success"] = $"Cleared {count} messages from log";
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error clearing message log");
                TempData["Error"] = ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        [HttpPost]
        public IActionResult ResetStatistics()
        {
            _totalMessagesSent = 0;
            _activeConnections = 0;
            _messageLog.Clear();
            TempData["Success"] = "Statistics reset successfully";
            return RedirectToAction(nameof(Index));
        }
    }

    // Helper model for SignalR messages
    public class SignalRMessage
    {
        public string Type { get; set; } = string.Empty; // Broadcast, Direct, Group
        public string Content { get; set; } = string.Empty;
        public string Sender { get; set; } = string.Empty;
        public string? Recipient { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
