// RMMS.Web/Controllers/AccountController.cs
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Mvc;
using RMMS.DataAccess.Helpers;
using RMMS.Models.ViewModels;
using System.Data;
using Microsoft.Data.SqlClient;
using System.Security.Claims;

namespace RMMS.Web.Controllers
{
    public class AccountController : Controller
    {
        private readonly IConfiguration _configuration;
        private readonly DatabaseHelper _dbHelper;

        public AccountController(IConfiguration configuration)
        {
            _configuration = configuration;
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        [HttpGet]
        public IActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Login(LoginViewModel model)
        {
            if (!ModelState.IsValid)
                return View(model);

            // Hash the password (use BCrypt or similar in production)
            string passwordHash = HashPassword(model.Password);

            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@Username", model.Username),
                _dbHelper.CreateParameter("@PasswordHash", passwordHash)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_User_ValidateLogin", parameters);

            if (dt.Rows.Count > 0)
            {
                DataRow user = dt.Rows[0];

                // Create claims with null checks
                var claims = new List<Claim>
                {
                    new Claim(ClaimTypes.Name, user["Username"]?.ToString() ?? ""),
                    new Claim(ClaimTypes.Email, user["Email"]?.ToString() ?? ""),
                    new Claim(ClaimTypes.Role, user["Role"]?.ToString() ?? ""),
                    new Claim("FullName", user["FullName"]?.ToString() ?? "")
                };

                var claimsIdentity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);

                await HttpContext.SignInAsync(
                    CookieAuthenticationDefaults.AuthenticationScheme,
                    new ClaimsPrincipal(claimsIdentity));

                return RedirectToAction("Index", "Home");
            }

            ModelState.AddModelError("", "Invalid username or password");
            return View(model);
        }

        public async Task<IActionResult> Logout()
        {
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            return RedirectToAction("Login");
        }

        private string HashPassword(string password)
        {
            // Use BCrypt.Net in production
            return BCrypt.Net.BCrypt.HashPassword(password);
        }
    }
}