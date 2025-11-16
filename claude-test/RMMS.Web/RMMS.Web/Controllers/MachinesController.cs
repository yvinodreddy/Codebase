using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using RMMS.Common.Extensions;
using RMMS.Common.Pagination;
using RMMS.Models.Production;
using RMMS.Services.Interfaces.Production;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Web.Controllers
{
    // [Authorize] -- TEMPORARILY DISABLED FOR TESTING
    public class MachinesController : Controller
    {
        private readonly IMachineService _machineService;
        private readonly ILogger<MachinesController> _logger;

        public MachinesController(IMachineService machineService, ILogger<MachinesController> logger)
        {
            _machineService = machineService;
            _logger = logger;
        }

        // GET: Machines
        public IActionResult Index(string searchTerm, int page = 1, string sortBy = "MachineName", string sortOrder = "asc")
        {
            try
            {
                const int pageSize = 16;

                List<Machine> machines;

                if (!string.IsNullOrWhiteSpace(searchTerm))
                {
                    machines = _machineService.SearchMachines(searchTerm);
                }
                else
                {
                    machines = _machineService.GetAllMachines();
                }

                // Apply sorting
                var machinesQuery = machines.AsQueryable().OrderByDynamic(sortBy, sortOrder);

                // Apply paging
                var pagedResult = PagedResult<Machine>.Create(machinesQuery, page, pageSize, sortBy, sortOrder);

                ViewBag.SearchTerm = searchTerm;
                ViewBag.CurrentSort = sortBy;
                ViewBag.CurrentOrder = sortOrder;

                // Statistics
                ViewBag.TotalMachines = machines.Count;
                ViewBag.OperationalCount = _machineService.GetOperationalMachinesCount();
                ViewBag.MaintenanceCount = _machineService.GetMachinesInMaintenanceCount();
                ViewBag.TotalValue = _machineService.GetTotalMachineValue();
                ViewBag.MaintenanceDueCount = _machineService.GetMachinesDueForMaintenance().Count;

                return View(pagedResult);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error loading machines");
                TempData["Error"] = "Error loading machines: " + ex.Message;
                return View(new PagedResult<Machine>());
            }
        }

        // GET: Machines/Details/5
        public IActionResult Details(int id)
        {
            try
            {
                var machine = _machineService.GetMachineById(id);
                if (machine == null)
                    return NotFound();

                return View(machine);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading machine {id}");
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Machines/Create
        public IActionResult Create()
        {
            var machine = new Machine
            {
                MachineCode = _machineService.GenerateMachineCode(),
                Status = "Operational",
                CapacityUnit = "tons/hour",
                RunningHours = 0
            };

            LoadDropdownData();
            return View(machine);
        }

        // POST: Machines/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Create(Machine machine)
        {
            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var machineId = _machineService.CreateMachine(machine, username);

                    TempData["Success"] = $"Machine {machine.MachineCode} created successfully!";
                    return RedirectToAction(nameof(Index));
                }

                LoadDropdownData();
                return View(machine);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating machine");
                ModelState.AddModelError("", "Error creating machine: " + ex.Message);
                LoadDropdownData();
                return View(machine);
            }
        }

        // GET: Machines/Edit/5
        public IActionResult Edit(int id)
        {
            try
            {
                var machine = _machineService.GetMachineById(id);
                if (machine == null)
                    return NotFound();

                LoadDropdownData();
                return View(machine);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading machine {id} for editing");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Machines/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Edit(int id, Machine machine)
        {
            if (id != machine.Id)
                return NotFound();

            try
            {
                if (ModelState.IsValid)
                {
                    var username = User.Identity?.Name ?? "System";
                    var success = _machineService.UpdateMachine(machine, username);

                    if (success)
                    {
                        TempData["Success"] = "Machine updated successfully!";
                        return RedirectToAction(nameof(Index));
                    }
                    else
                    {
                        ModelState.AddModelError("", "Failed to update machine");
                    }
                }

                LoadDropdownData();
                return View(machine);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error updating machine {id}");
                ModelState.AddModelError("", "Error updating machine: " + ex.Message);
                LoadDropdownData();
                return View(machine);
            }
        }

        // GET: Machines/Delete/5
        public IActionResult Delete(int id)
        {
            try
            {
                var machine = _machineService.GetMachineById(id);
                if (machine == null)
                    return NotFound();

                return View(machine);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading machine {id} for deletion");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Machines/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public IActionResult DeleteConfirmed(int id)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var success = _machineService.DeleteMachine(id, username);
                if (success)
                {
                    TempData["Success"] = "Machine deleted successfully!";
                }
                else
                {
                    TempData["Error"] = "Failed to delete machine";
                }
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error deleting machine {id}");
                TempData["Error"] = "Error deleting machine: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // GET: Machines/Maintenance/5
        public IActionResult Maintenance(int id)
        {
            try
            {
                var machine = _machineService.GetMachineById(id);
                if (machine == null)
                    return NotFound();

                return View(machine);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error loading machine {id} for maintenance");
                return RedirectToAction(nameof(Index));
            }
        }

        // POST: Machines/Maintenance/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Maintenance(int id, string remarks)
        {
            try
            {
                var username = User.Identity?.Name ?? "System";
                var success = _machineService.RecordMaintenance(id, username, remarks);

                if (success)
                {
                    TempData["Success"] = "Maintenance recorded successfully! Machine is now operational.";
                }
                else
                {
                    TempData["Error"] = "Failed to record maintenance";
                }

                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error recording maintenance for machine {id}");
                TempData["Error"] = "Error recording maintenance: " + ex.Message;
                return RedirectToAction(nameof(Index));
            }
        }

        // Helper method to load dropdown data
        private void LoadDropdownData()
        {
            // Machine Types
            ViewBag.MachineTypes = new List<SelectListItem>
            {
                new SelectListItem { Value = "Cleaner", Text = "Cleaner" },
                new SelectListItem { Value = "Husker", Text = "Husker/De-Husker" },
                new SelectListItem { Value = "Polisher", Text = "Polisher" },
                new SelectListItem { Value = "Grader", Text = "Grader/Sorter" },
                new SelectListItem { Value = "Separator", Text = "Separator" },
                new SelectListItem { Value = "Dryer", Text = "Dryer" },
                new SelectListItem { Value = "Weighbridge", Text = "Weighbridge" }
            };

            // Status Options
            ViewBag.StatusOptions = new List<SelectListItem>
            {
                new SelectListItem { Value = "Operational", Text = "Operational" },
                new SelectListItem { Value = "Maintenance", Text = "Under Maintenance" },
                new SelectListItem { Value = "Breakdown", Text = "Breakdown" },
                new SelectListItem { Value = "Idle", Text = "Idle" }
            };

            // Capacity Units
            ViewBag.CapacityUnits = new List<SelectListItem>
            {
                new SelectListItem { Value = "tons/hour", Text = "tons/hour" },
                new SelectListItem { Value = "bags/hour", Text = "bags/hour" },
                new SelectListItem { Value = "kg/hour", Text = "kg/hour" },
                new SelectListItem { Value = "quintals/hour", Text = "quintals/hour" }
            };
        }
    }
}
