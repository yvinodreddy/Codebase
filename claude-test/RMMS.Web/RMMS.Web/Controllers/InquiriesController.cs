using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using RMMS.Models.Sales;
using RMMS.Services.Interfaces.Sales;
using RMMS.Services.Interfaces.Masters;
using System;
using System.Threading.Tasks;

namespace RMMS.Web.Controllers
{
    public class InquiriesController : Controller
    {
        private readonly IInquiryService _inquiryService;
        private readonly ICustomerService _customerService;
        private readonly IEmployeeService _employeeService;

        public InquiriesController(
            IInquiryService inquiryService,
            ICustomerService customerService,
            IEmployeeService employeeService)
        {
            _inquiryService = inquiryService;
            _customerService = customerService;
            _employeeService = employeeService;
        }

        // GET: Inquiries
        public async Task<IActionResult> Index(string searchTerm, string status, int page = 1)
        {
            try
            {
                const int pageSize = 16;
                IEnumerable<Inquiry> inquiries;

                if (!string.IsNullOrEmpty(searchTerm))
                {
                    inquiries = await _inquiryService.SearchInquiriesAsync(searchTerm);
                }
                else if (!string.IsNullOrEmpty(status))
                {
                    inquiries = await _inquiryService.GetInquiriesByStatusAsync(status);
                }
                else
                {
                    inquiries = await _inquiryService.GetAllInquiriesAsync();
                }

                // Get statistics for dashboard
                var stats = await _inquiryService.GetInquiryStatisticsAsync();
                ViewBag.Statistics = stats;
                ViewBag.SearchTerm = searchTerm;
                ViewBag.SelectedStatus = status;

                // Apply pagination
                var totalRecords = inquiries.Count();
                var totalPages = (int)Math.Ceiling(totalRecords / (double)pageSize);
                var pagedInquiries = inquiries.Skip((page - 1) * pageSize).Take(pageSize).ToList();

                ViewBag.CurrentPage = page;
                ViewBag.TotalPages = totalPages;
                ViewBag.TotalRecords = totalRecords;

                return View(pagedInquiries);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading inquiries: {ex.Message}";
                return View(new List<Inquiry>());
            }
        }

        // GET: Inquiries/Details/5
        public async Task<IActionResult> Details(int id)
        {
            try
            {
                var inquiry = await _inquiryService.GetInquiryByIdAsync(id);
                if (inquiry == null)
                {
                    TempData["ErrorMessage"] = "Inquiry not found.";
                    return RedirectToAction(nameof(Index));
                }

                return View(inquiry);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading inquiry: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Inquiries/Create
        public IActionResult Create()
        {
            PopulateDropdowns();
            return View();
        }

        // POST: Inquiries/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create(Inquiry inquiry)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var createdBy = User.Identity?.Name ?? "System";
                    await _inquiryService.CreateInquiryAsync(inquiry, createdBy);

                    TempData["SuccessMessage"] = $"Inquiry {inquiry.InquiryNumber} created successfully.";
                    return RedirectToAction(nameof(Index));
                }

                PopulateDropdowns();
                return View(inquiry);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error creating inquiry: {ex.Message}";
                PopulateDropdowns();
                return View(inquiry);
            }
        }

        // GET: Inquiries/Edit/5
        public async Task<IActionResult> Edit(int id)
        {
            try
            {
                var inquiry = await _inquiryService.GetInquiryByIdAsync(id);
                if (inquiry == null)
                {
                    TempData["ErrorMessage"] = "Inquiry not found.";
                    return RedirectToAction(nameof(Index));
                }

                PopulateDropdowns();
                return View(inquiry);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading inquiry: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Inquiries/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, Inquiry inquiry)
        {
            if (id != inquiry.Id)
            {
                TempData["ErrorMessage"] = "Invalid inquiry ID.";
                return RedirectToAction(nameof(Index));
            }

            try
            {
                if (ModelState.IsValid)
                {
                    var modifiedBy = User.Identity?.Name ?? "System";
                    await _inquiryService.UpdateInquiryAsync(inquiry, modifiedBy);

                    TempData["SuccessMessage"] = $"Inquiry {inquiry.InquiryNumber} updated successfully.";
                    return RedirectToAction(nameof(Details), new { id = inquiry.Id });
                }

                PopulateDropdowns();
                return View(inquiry);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error updating inquiry: {ex.Message}";
                PopulateDropdowns();
                return View(inquiry);
            }
        }

        // GET: Inquiries/Delete/5
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var inquiry = await _inquiryService.GetInquiryByIdAsync(id);
                if (inquiry == null)
                {
                    TempData["ErrorMessage"] = "Inquiry not found.";
                    return RedirectToAction(nameof(Index));
                }

                return View(inquiry);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading inquiry: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Inquiries/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            try
            {
                var deletedBy = User.Identity?.Name ?? "System";
                var result = await _inquiryService.DeleteInquiryAsync(id, deletedBy);

                if (result)
                {
                    TempData["SuccessMessage"] = "Inquiry deleted successfully.";
                }
                else
                {
                    TempData["ErrorMessage"] = "Failed to delete inquiry.";
                }

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error deleting inquiry: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Inquiries/Assign/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Assign(int id, int employeeId)
        {
            try
            {
                var modifiedBy = User.Identity?.Name ?? "System";
                var result = await _inquiryService.AssignInquiryAsync(id, employeeId, modifiedBy);

                if (result)
                {
                    TempData["SuccessMessage"] = "Inquiry assigned successfully.";
                }
                else
                {
                    TempData["ErrorMessage"] = "Failed to assign inquiry.";
                }

                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error assigning inquiry: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: Inquiries/MarkAsLost/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> MarkAsLost(int id, string lostReason)
        {
            try
            {
                var modifiedBy = User.Identity?.Name ?? "System";
                var result = await _inquiryService.MarkAsLostAsync(id, lostReason, modifiedBy);

                if (result)
                {
                    TempData["SuccessMessage"] = "Inquiry marked as lost.";
                }
                else
                {
                    TempData["ErrorMessage"] = "Failed to mark inquiry as lost.";
                }

                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error marking inquiry as lost: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // POST: Inquiries/UpdateFollowUp/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> UpdateFollowUp(int id, DateTime followUpDate)
        {
            try
            {
                var modifiedBy = User.Identity?.Name ?? "System";
                var result = await _inquiryService.UpdateFollowUpDateAsync(id, followUpDate, modifiedBy);

                if (result)
                {
                    TempData["SuccessMessage"] = "Follow-up date updated successfully.";
                }
                else
                {
                    TempData["ErrorMessage"] = "Failed to update follow-up date.";
                }

                return RedirectToAction(nameof(Details), new { id });
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error updating follow-up date: {ex.Message}";
                return RedirectToAction(nameof(Details), new { id });
            }
        }

        // GET: Inquiries/FollowUpDue
        public async Task<IActionResult> FollowUpDue()
        {
            try
            {
                var inquiries = await _inquiryService.GetFollowUpDueInquiriesAsync();
                ViewBag.PageTitle = "Follow-up Due Inquiries";
                return View("Index", inquiries);
            }
            catch (Exception ex)
            {
                TempData["ErrorMessage"] = $"Error loading follow-up due inquiries: {ex.Message}";
                return RedirectToAction(nameof(Index));
            }
        }

        private void PopulateDropdowns()
        {
            // Get customers
            var customers = _customerService.GetAllCustomers();
            ViewBag.Customers = new SelectList(customers, "Id", "CustomerName");

            // Get employees
            var employees = _employeeService.GetAllEmployees();
            ViewBag.Employees = new SelectList(employees, "Id", "EmployeeName");

            // Source options
            ViewBag.Sources = new SelectList(new[]
            {
                "Phone",
                "Email",
                "Walk-in",
                "Website",
                "Referral",
                "Social Media",
                "Advertisement",
                "Other"
            });

            // Status options
            ViewBag.Statuses = new SelectList(new[]
            {
                "New",
                "In Progress",
                "Quoted",
                "Converted",
                "Lost",
                "Closed"
            });

            // Priority options
            ViewBag.Priorities = new SelectList(new[]
            {
                "Low",
                "Normal",
                "High",
                "Urgent"
            });

            // Product types
            ViewBag.ProductTypes = new SelectList(new[]
            {
                "Basmati Rice",
                "Non-Basmati Rice",
                "Broken Rice",
                "Rice Bran",
                "Rice Husk",
                "Other"
            });
        }
    }
}
