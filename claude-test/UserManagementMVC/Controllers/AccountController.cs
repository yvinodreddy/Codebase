using Microsoft.AspNetCore.Mvc;
using UserManagementMVC.Models;
using UserManagementMVC.Services;

namespace UserManagementMVC.Controllers;

public class AccountController : Controller
{
    private readonly IApiService _apiService;

    public AccountController(IApiService apiService)
    {
        _apiService = apiService;
    }

    // GET: Account/Login
    [HttpGet]
    public IActionResult Login()
    {
        return View();
    }

    // POST: Account/Login
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Login(LoginViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var result = await _apiService.LoginAsync(model.Username, model.Password);

        if (result != null && result.Success)
        {
            // Store user info in session or cookie
            HttpContext.Session.SetString("UserId", result.User!.Id.ToString());
            HttpContext.Session.SetString("Username", result.User.Username);

            TempData["SuccessMessage"] = "Login successful!";
            return RedirectToAction("Dashboard");
        }

        ModelState.AddModelError(string.Empty, result?.Message ?? "Invalid login attempt");
        return View(model);
    }

    // GET: Account/Register
    [HttpGet]
    public IActionResult Register()
    {
        return View();
    }

    // POST: Account/Register
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Register(RegisterViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var result = await _apiService.RegisterAsync(
            model.Username,
            model.Email,
            model.Password,
            model.FirstName,
            model.LastName
        );

        if (result != null)
        {
            TempData["SuccessMessage"] = "Registration successful! Please login.";
            return RedirectToAction("Login");
        }

        ModelState.AddModelError(string.Empty, "Registration failed. Username or email may already exist.");
        return View(model);
    }

    // GET: Account/Dashboard
    [HttpGet]
    public IActionResult Dashboard()
    {
        var username = HttpContext.Session.GetString("Username");

        if (string.IsNullOrEmpty(username))
        {
            return RedirectToAction("Login");
        }

        ViewBag.Username = username;
        return View();
    }

    // POST: Account/Logout
    [HttpPost]
    [ValidateAntiForgeryToken]
    public IActionResult Logout()
    {
        HttpContext.Session.Clear();
        TempData["SuccessMessage"] = "You have been logged out.";
        return RedirectToAction("Login");
    }
}
