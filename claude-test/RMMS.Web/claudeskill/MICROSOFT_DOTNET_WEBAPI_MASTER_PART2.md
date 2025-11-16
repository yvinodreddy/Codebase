# Microsoft .NET Web API Master - Part 2
## Advanced Patterns, JavaScript Integration & Production Features

**Continuation of**: MICROSOFT_DOTNET_WEBAPI_MASTER.md
**Last Updated**: 2025-10-23

---

## 📱 SIGNALR REAL-TIME PATTERNS

### NotificationHub.cs

```csharp
using Microsoft.AspNetCore.SignalR;
using Microsoft.AspNetCore.Authorization;

namespace YourProject.Web.Hubs
{
    [Authorize]
    public class NotificationHub : Hub
    {
        private readonly ILogger<NotificationHub> _logger;

        public NotificationHub(ILogger<NotificationHub> logger)
        {
            _logger = logger;
        }

        public override async Task OnConnectedAsync()
        {
            var userId = Context.User?.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (userId != null)
            {
                await Groups.AddToGroupAsync(Context.ConnectionId, $"user-{userId}");
                _logger.LogInformation("User {UserId} connected to NotificationHub", userId);
            }
            await base.OnConnectedAsync();
        }

        public override async Task OnDisconnectedAsync(Exception? exception)
        {
            var userId = Context.User?.FindFirst(ClaimTypes.NameIdentifier)?.Value;
            if (userId != null)
            {
                await Groups.RemoveFromGroupAsync(Context.ConnectionId, $"user-{userId}");
                _logger.LogInformation("User {UserId} disconnected from NotificationHub", userId);
            }
            await base.OnDisconnectedAsync(exception);
        }

        public async Task SendNotificationToUser(string userId, string message)
        {
            await Clients.Group($"user-{userId}").SendAsync("ReceiveNotification", message);
        }

        public async Task BroadcastNotification(string message)
        {
            await Clients.All.SendAsync("ReceiveNotification", message);
        }
    }
}
```

### Client-Side SignalR Integration

```javascript
// wwwroot/js/signalr-client.js
(function ($) {
    'use strict';

    // SignalR Connection Manager
    const SignalRManager = {
        connection: null,
        isConnected: false,

        init: function() {
            console.log('Initializing SignalR connection...');

            // Create connection
            this.connection = new signalR.HubConnectionBuilder()
                .withUrl("/hubs/notifications", {
                    accessTokenFactory: () => {
                        // Get JWT token from localStorage or cookie
                        return localStorage.getItem('access_token') || '';
                    }
                })
                .withAutomaticReconnect()
                .configureLogging(signalR.LogLevel.Information)
                .build();

            // Setup event handlers
            this.setupEventHandlers();

            // Start connection
            this.start();
        },

        setupEventHandlers: function() {
            // Receive notification
            this.connection.on("ReceiveNotification", function(message) {
                console.log('Notification received:', message);

                // Show toast notification
                toastr.info(message, 'Notification');
            });

            // Reconnecting
            this.connection.onreconnecting((error) => {
                console.log('SignalR reconnecting...', error);
                toastr.warning('Reconnecting...', 'Connection');
            });

            // Reconnected
            this.connection.onreconnected((connectionId) => {
                console.log('SignalR reconnected:', connectionId);
                toastr.success('Reconnected!', 'Connection');
                this.isConnected = true;
            });

            // Closed
            this.connection.onclose((error) => {
                console.log('SignalR connection closed', error);
                this.isConnected = false;
                toastr.error('Connection closed', 'Connection');
            });
        },

        start: async function() {
            try {
                await this.connection.start();
                console.log('SignalR Connected');
                this.isConnected = true;
                toastr.success('Real-time connection established', 'Connected');
            } catch (err) {
                console.error('SignalR Connection Error:', err);
                toastr.error('Failed to establish real-time connection', 'Error');

                // Retry after 5 seconds
                setTimeout(() => this.start(), 5000);
            }
        },

        sendNotification: async function(userId, message) {
            if (this.isConnected) {
                try {
                    await this.connection.invoke("SendNotificationToUser", userId, message);
                } catch (err) {
                    console.error('Error sending notification:', err);
                }
            }
        },

        broadcastNotification: async function(message) {
            if (this.isConnected) {
                try {
                    await this.connection.invoke("BroadcastNotification", message);
                } catch (err) {
                    console.error('Error broadcasting notification:', err);
                }
            }
        }
    };

    // Initialize on document ready
    $(document).ready(function() {
        SignalRManager.init();

        // Make globally available
        window.SignalRManager = SignalRManager;
    });

})(jQuery);
```

---

## 🎨 COMPLETE JAVASCRIPT PATTERNS

### DataTables Integration (Production-Ready)

```javascript
// wwwroot/js/datatables-config.js
(function ($) {
    'use strict';

    /**
     * Initialize DataTables with advanced features
     */
    function initializeDataTables() {
        console.log('Initializing DataTables...');

        if (!$.fn.DataTable) {
            console.warn('DataTables plugin not loaded');
            return;
        }

        $('.datatable').each(function () {
            var $table = $(this);

            // Skip if already initialized
            if ($.fn.DataTable.isDataTable($table)) {
                $table.DataTable().destroy();
            }

            // Get custom options from data attributes
            var pageLength = $table.data('page-length') || 10;
            var ordering = $table.data('ordering') !== false;
            var searching = $table.data('searching') !== false;
            var paging = $table.data('paging') !== false;
            var exportButtons = $table.data('export') !== false;

            // Build buttons array
            var buttons = [];
            if (exportButtons) {
                buttons = [
                    {
                        extend: 'copy',
                        className: 'btn btn-sm btn-secondary',
                        text: '<i class="fas fa-copy"></i> Copy'
                    },
                    {
                        extend: 'excel',
                        className: 'btn btn-sm btn-success',
                        text: '<i class="fas fa-file-excel"></i> Excel'
                    },
                    {
                        extend: 'csv',
                        className: 'btn btn-sm btn-info',
                        text: '<i class="fas fa-file-csv"></i> CSV'
                    },
                    {
                        extend: 'pdf',
                        className: 'btn btn-sm btn-danger',
                        text: '<i class="fas fa-file-pdf"></i> PDF'
                    },
                    {
                        extend: 'print',
                        className: 'btn btn-sm btn-primary',
                        text: '<i class="fas fa-print"></i> Print'
                    }
                ];
            }

            // Initialize DataTable
            var dataTable = $table.DataTable({
                // Display settings
                pageLength: pageLength,
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],

                // Feature control
                ordering: ordering,
                searching: searching,
                paging: paging,
                info: true,
                autoWidth: false,

                // Buttons
                buttons: buttons,
                dom: "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
                     "<'row'<'col-sm-12'B>>" +
                     "<'row'<'col-sm-12'tr>>" +
                     "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",

                // Responsive settings
                responsive: {
                    details: {
                        type: 'column',
                        target: 'tr'
                    }
                },

                // Column definitions
                columnDefs: [
                    {
                        responsivePriority: 1,
                        targets: 0
                    },
                    {
                        responsivePriority: 2,
                        targets: -1
                    }
                ],

                // Language customization
                language: {
                    search: "Search:",
                    searchPlaceholder: "Type to search...",
                    lengthMenu: "Show _MENU_ entries",
                    info: "Showing _START_ to _END_ of _TOTAL_ entries",
                    infoEmpty: "Showing 0 to 0 of 0 entries",
                    infoFiltered: "(filtered from _MAX_ total entries)",
                    paginate: {
                        first: "First",
                        last: "Last",
                        next: "Next",
                        previous: "Previous"
                    },
                    emptyTable: "No data available",
                    zeroRecords: "No matching records found",
                    loadingRecords: "Loading...",
                    processing: "Processing..."
                }
            });

            console.log('DataTable initialized:', $table.attr('id'));
        });
    }

    // Initialize on document ready
    $(document).ready(function() {
        initializeDataTables();
    });

    // Reinitialize on AJAX updates
    $(document).on('ajaxComplete', function() {
        setTimeout(initializeDataTables, 100);
    });

})(jQuery);
```

### SweetAlert2 Integration

```javascript
// wwwroot/js/sweetalert-helpers.js
(function (window, $) {
    'use strict';

    const SweetAlertHelper = {
        /**
         * Confirmation dialog
         */
        confirm: function(options) {
            const defaults = {
                title: 'Are you sure?',
                text: "You won't be able to revert this!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel'
            };

            const settings = $.extend({}, defaults, options);

            return Swal.fire(settings);
        },

        /**
         * Delete confirmation
         */
        confirmDelete: async function(url, itemName = 'item') {
            const result = await Swal.fire({
                title: `Delete ${itemName}?`,
                text: "This action cannot be undone!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Yes, delete it!',
                cancelButtonText: 'Cancel'
            });

            if (result.isConfirmed) {
                try {
                    const response = await $.ajax({
                        url: url,
                        type: 'DELETE',
                        headers: {
                            'RequestVerificationToken': $('input[name="__RequestVerificationToken"]').val()
                        }
                    });

                    Swal.fire({
                        title: 'Deleted!',
                        text: `${itemName} has been deleted.`,
                        icon: 'success',
                        timer: 2000,
                        showConfirmButton: false
                    });

                    return true;
                } catch (error) {
                    Swal.fire({
                        title: 'Error!',
                        text: 'Failed to delete the item.',
                        icon: 'error'
                    });
                    return false;
                }
            }

            return false;
        },

        /**
         * Success message
         */
        success: function(message, title = 'Success!') {
            return Swal.fire({
                title: title,
                text: message,
                icon: 'success',
                timer: 3000,
                showConfirmButton: false
            });
        },

        /**
         * Error message
         */
        error: function(message, title = 'Error!') {
            return Swal.fire({
                title: title,
                text: message,
                icon: 'error'
            });
        },

        /**
         * Loading indicator
         */
        loading: function(title = 'Processing...', text = 'Please wait') {
            Swal.fire({
                title: title,
                text: text,
                allowOutsideClick: false,
                allowEscapeKey: false,
                showConfirmButton: false,
                willOpen: () => {
                    Swal.showLoading();
                }
            });
        },

        /**
         * Close loading
         */
        close: function() {
            Swal.close();
        }
    };

    // Make globally available
    window.SweetAlertHelper = SweetAlertHelper;

    // jQuery integration
    $.fn.confirmDelete = function(itemName) {
        return this.each(function() {
            const $btn = $(this);
            const url = $btn.data('url') || $btn.attr('href');

            $btn.on('click', async function(e) {
                e.preventDefault();
                const deleted = await SweetAlertHelper.confirmDelete(url, itemName);
                if (deleted) {
                    // Reload page or remove row
                    location.reload();
                }
            });
        });
    };

})(window, jQuery);

// Usage Examples:
// SweetAlertHelper.success('Customer saved successfully!');
// SweetAlertHelper.error('An error occurred');
// await SweetAlertHelper.confirmDelete('/api/customers/123', 'Customer');
// $('.delete-btn').confirmDelete('Customer');
```

### Select2 Integration

```javascript
// wwwroot/js/select2-config.js
(function ($) {
    'use strict';

    /**
     * Initialize Select2 on all select elements
     */
    function initializeSelect2() {
        console.log('Initializing Select2...');

        if (!$.fn.select2) {
            console.warn('Select2 plugin not loaded');
            return;
        }

        // Basic select2
        $('.select2').each(function() {
            const $select = $(this);

            $select.select2({
                theme: 'bootstrap-5',
                width: '100%',
                placeholder: $select.data('placeholder') || 'Select an option',
                allowClear: true
            });
        });

        // Select2 with AJAX
        $('.select2-ajax').each(function() {
            const $select = $(this);
            const url = $select.data('url');

            $select.select2({
                theme: 'bootstrap-5',
                width: '100%',
                placeholder: $select.data('placeholder') || 'Search...',
                allowClear: true,
                minimumInputLength: 2,
                ajax: {
                    url: url,
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return {
                            search: params.term,
                            page: params.page || 1
                        };
                    },
                    processResults: function (data, params) {
                        params.page = params.page || 1;

                        return {
                            results: data.items,
                            pagination: {
                                more: (params.page * 10) < data.totalCount
                            }
                        };
                    },
                    cache: true
                }
            });
        });
    }

    // Initialize on document ready
    $(document).ready(function() {
        initializeSelect2();
    });

})(jQuery);
```

### Chart.js Integration

```javascript
// wwwroot/js/charts-config.js
(function (window, $) {
    'use strict';

    const ChartHelper = {
        /**
         * Create a line chart
         */
        createLineChart: function(canvasId, data, options = {}) {
            const ctx = document.getElementById(canvasId).getContext('2d');

            const defaultOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Chart'
                    }
                }
            };

            const settings = $.extend(true, {}, defaultOptions, options);

            return new Chart(ctx, {
                type: 'line',
                data: data,
                options: settings
            });
        },

        /**
         * Create a bar chart
         */
        createBarChart: function(canvasId, data, options = {}) {
            const ctx = document.getElementById(canvasId).getContext('2d');

            const defaultOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                }
            };

            const settings = $.extend(true, {}, defaultOptions, options);

            return new Chart(ctx, {
                type: 'bar',
                data: data,
                options: settings
            });
        },

        /**
         * Create a pie chart
         */
        createPieChart: function(canvasId, data, options = {}) {
            const ctx = document.getElementById(canvasId).getContext('2d');

            const defaultOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    }
                }
            };

            const settings = $.extend(true, {}, defaultOptions, options);

            return new Chart(ctx, {
                type: 'pie',
                data: data,
                options: settings
            });
        },

        /**
         * Fetch data and create chart
         */
        createChartFromApi: async function(canvasId, url, chartType = 'line', options = {}) {
            try {
                const response = await $.ajax({
                    url: url,
                    type: 'GET',
                    dataType: 'json'
                });

                const data = {
                    labels: response.labels,
                    datasets: response.datasets
                };

                switch(chartType) {
                    case 'bar':
                        return this.createBarChart(canvasId, data, options);
                    case 'pie':
                        return this.createPieChart(canvasId, data, options);
                    default:
                        return this.createLineChart(canvasId, data, options);
                }
            } catch (error) {
                console.error('Error loading chart data:', error);
                return null;
            }
        }
    };

    // Make globally available
    window.ChartHelper = ChartHelper;

})(window, jQuery);

// Usage:
// ChartHelper.createLineChart('salesChart', chartData);
// ChartHelper.createChartFromApi('revenueChart', '/api/analytics/revenue', 'bar');
```

### Dropzone File Upload Integration

```javascript
// wwwroot/js/dropzone-config.js
(function ($) {
    'use strict';

    /**
     * Initialize Dropzone
     */
    function initializeDropzone() {
        console.log('Initializing Dropzone...');

        if (typeof Dropzone === 'undefined') {
            console.warn('Dropzone not loaded');
            return;
        }

        // Disable auto-discover
        Dropzone.autoDiscover = false;

        // Initialize all dropzone elements
        $('.dropzone-uploader').each(function() {
            const $element = $(this);
            const url = $element.data('url') || '/api/upload';
            const maxFiles = $element.data('max-files') || 5;
            const maxFileSize = $element.data('max-size') || 10; // MB
            const acceptedFiles = $element.data('accepted') || 'image/*,application/pdf';

            const dropzone = new Dropzone($element[0], {
                url: url,
                maxFiles: maxFiles,
                maxFilesize: maxFileSize,
                acceptedFiles: acceptedFiles,
                addRemoveLinks: true,
                dictDefaultMessage: "Drop files here or click to upload",
                dictRemoveFile: "Remove",
                dictCancelUpload: "Cancel",
                headers: {
                    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                },
                init: function() {
                    this.on("success", function(file, response) {
                        console.log('File uploaded:', response);
                        toastr.success('File uploaded successfully');
                    });

                    this.on("error", function(file, errorMessage) {
                        console.error('Upload error:', errorMessage);
                        toastr.error('Failed to upload file');
                    });

                    this.on("maxfilesexceeded", function(file) {
                        this.removeFile(file);
                        toastr.warning(`Maximum ${maxFiles} files allowed`);
                    });
                }
            });

            $element.data('dropzone', dropzone);
        });
    }

    // Initialize on document ready
    $(document).ready(function() {
        initializeDropzone();
    });

})(jQuery);
```

---

## 🔐 AUTHENTICATION & SECURITY PATTERNS

### JWT Service

```csharp
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace YourProject.Services.Implementations
{
    public class JwtTokenService : IJwtTokenService
    {
        private readonly IConfiguration _configuration;
        private readonly ILogger<JwtTokenService> _logger;

        public JwtTokenService(IConfiguration configuration, ILogger<JwtTokenService> logger)
        {
            _configuration = configuration;
            _logger = logger;
        }

        public string GenerateToken(User user)
        {
            var jwtSettings = _configuration.GetSection("JwtSettings");
            var secretKey = jwtSettings["SecretKey"];
            var issuer = jwtSettings["Issuer"];
            var audience = jwtSettings["Audience"];
            var expirationMinutes = int.Parse(jwtSettings["TokenExpirationMinutes"]);

            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Name, user.Username),
                new Claim(ClaimTypes.Email, user.Email),
                new Claim(JwtRegisteredClaimNames.Sub, user.Username),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
                new Claim(JwtRegisteredClaimNames.Iat, DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString())
            };

            // Add role claims
            foreach (var role in user.Roles)
            {
                claims.Add(new Claim(ClaimTypes.Role, role.Name));
            }

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var token = new JwtSecurityToken(
                issuer: issuer,
                audience: audience,
                claims: claims,
                expires: DateTime.UtcNow.AddMinutes(expirationMinutes),
                signingCredentials: creds
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public string GenerateRefreshToken()
        {
            var randomNumber = new byte[32];
            using var rng = System.Security.Cryptography.RandomNumberGenerator.Create();
            rng.GetBytes(randomNumber);
            return Convert.ToBase64String(randomNumber);
        }

        public ClaimsPrincipal? GetPrincipalFromExpiredToken(string token)
        {
            var jwtSettings = _configuration.GetSection("JwtSettings");
            var secretKey = jwtSettings["SecretKey"];

            var tokenValidationParameters = new TokenValidationParameters
            {
                ValidateAudience = false,
                ValidateIssuer = false,
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey)),
                ValidateLifetime = false // Don't validate expiration
            };

            var tokenHandler = new JwtSecurityTokenHandler();
            try
            {
                var principal = tokenHandler.ValidateToken(token, tokenValidationParameters, out SecurityToken securityToken);

                if (securityToken is not JwtSecurityToken jwtSecurityToken ||
                    !jwtSecurityToken.Header.Alg.Equals(SecurityAlgorithms.HmacSha256, StringComparison.InvariantCultureIgnoreCase))
                {
                    throw new SecurityTokenException("Invalid token");
                }

                return principal;
            }
            catch
            {
                return null;
            }
        }
    }
}
```

### Password Hasher

```csharp
namespace YourProject.Services.Helpers
{
    public static class PasswordHasher
    {
        public static string HashPassword(string password)
        {
            return BCrypt.Net.BCrypt.HashPassword(password, BCrypt.Net.BCrypt.GenerateSalt(12));
        }

        public static bool VerifyPassword(string password, string hashedPassword)
        {
            return BCrypt.Net.BCrypt.Verify(password, hashedPassword);
        }
    }
}
```

### Security Headers Middleware

```csharp
namespace YourProject.Web.Middleware
{
    public class SecurityHeadersMiddleware
    {
        private readonly RequestDelegate _next;

        public SecurityHeadersMiddleware(RequestDelegate next)
        {
            _next = next;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            // X-Content-Type-Options
            context.Response.Headers.Add("X-Content-Type-Options", "nosniff");

            // X-Frame-Options
            context.Response.Headers.Add("X-Frame-Options", "DENY");

            // X-XSS-Protection
            context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");

            // Referrer-Policy
            context.Response.Headers.Add("Referrer-Policy", "strict-origin-when-cross-origin");

            // Content-Security-Policy
            context.Response.Headers.Add("Content-Security-Policy",
                "default-src 'self'; " +
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://code.jquery.com https://cdn.datatables.net https://unpkg.com https://cdnjs.cloudflare.com; " +
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://cdn.datatables.net https://cdnjs.cloudflare.com https://unpkg.com; " +
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; " +
                "img-src 'self' data: https:; " +
                "connect-src 'self'; " +
                "frame-ancestors 'none';");

            // Remove Server header
            context.Response.Headers.Remove("Server");

            await _next(context);
        }
    }
}
```

---

## 🗄️ REPOSITORY & SERVICE PATTERNS (COMPLETE)

### Generic Repository with Advanced Features

```csharp
using Microsoft.EntityFrameworkCore;
using System.Linq.Expressions;

namespace YourProject.DataAccess.Repositories
{
    public class Repository<T> : IRepository<T> where T : BaseEntity
    {
        protected readonly ApplicationDbContext _context;
        protected readonly DbSet<T> _dbSet;

        public Repository(ApplicationDbContext context)
        {
            _context = context;
            _dbSet = context.Set<T>();
        }

        public virtual async Task<T?> GetByIdAsync(int id)
        {
            return await _dbSet.FirstOrDefaultAsync(e => e.Id == id && !e.IsDeleted);
        }

        public virtual async Task<IEnumerable<T>> GetAllAsync()
        {
            return await _dbSet.Where(e => !e.IsDeleted).ToListAsync();
        }

        public virtual async Task<IEnumerable<T>> FindAsync(Expression<Func<T, bool>> predicate)
        {
            return await _dbSet.Where(predicate).Where(e => !e.IsDeleted).ToListAsync();
        }

        public virtual async Task<T> AddAsync(T entity)
        {
            entity.CreatedDate = DateTime.UtcNow;
            await _dbSet.AddAsync(entity);
            await _context.SaveChangesAsync();
            return entity;
        }

        public virtual async Task UpdateAsync(T entity)
        {
            entity.ModifiedDate = DateTime.UtcNow;
            _context.Entry(entity).State = EntityState.Modified;
            await _context.SaveChangesAsync();
        }

        public virtual async Task DeleteAsync(int id)
        {
            var entity = await GetByIdAsync(id);
            if (entity != null)
            {
                entity.IsDeleted = true;
                entity.DeletedDate = DateTime.UtcNow;
                await UpdateAsync(entity);
            }
        }

        public virtual async Task HardDeleteAsync(int id)
        {
            var entity = await _dbSet.FindAsync(id);
            if (entity != null)
            {
                _dbSet.Remove(entity);
                await _context.SaveChangesAsync();
            }
        }

        public virtual async Task<bool> ExistsAsync(int id)
        {
            return await _dbSet.AnyAsync(e => e.Id == id && !e.IsDeleted);
        }

        public virtual async Task<int> CountAsync()
        {
            return await _dbSet.CountAsync(e => !e.IsDeleted);
        }

        public virtual async Task<int> CountAsync(Expression<Func<T, bool>> predicate)
        {
            return await _dbSet.Where(predicate).CountAsync(e => !e.IsDeleted);
        }

        public virtual async Task<PaginatedResult<T>> GetPagedAsync(
            int page,
            int pageSize,
            Expression<Func<T, bool>>? filter = null,
            Func<IQueryable<T>, IOrderedQueryable<T>>? orderBy = null,
            string includeProperties = "")
        {
            IQueryable<T> query = _dbSet;

            // Apply filter
            if (filter != null)
            {
                query = query.Where(filter);
            }

            // Soft delete filter
            query = query.Where(e => !e.IsDeleted);

            // Include properties
            foreach (var includeProperty in includeProperties.Split(new char[] { ',' }, StringSplitOptions.RemoveEmptyEntries))
            {
                query = query.Include(includeProperty);
            }

            // Total count
            int totalCount = await query.CountAsync();

            // Apply ordering
            if (orderBy != null)
            {
                query = orderBy(query);
            }

            // Apply paging
            var items = await query
                .Skip((page - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();

            return new PaginatedResult<T>
            {
                Items = items,
                TotalCount = totalCount,
                PageNumber = page,
                PageSize = pageSize,
                TotalPages = (int)Math.Ceiling(totalCount / (double)pageSize)
            };
        }
    }
}
```

---

*[Continue to PART 3 for more advanced features...]*
