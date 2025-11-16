using Microsoft.EntityFrameworkCore;
using RMMS.DataAccess.Context;
using RMMS.Models.Production;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.DataAccess.Repositories.Production
{
    public class MachineRepository : IMachineRepository
    {
        private readonly ApplicationDbContext _context;

        public MachineRepository(ApplicationDbContext context)
        {
            _context = context;
        }

        public List<Machine> GetAllMachines(bool activeOnly = true)
        {
            var query = _context.Machines.AsQueryable();

            if (activeOnly)
            {
                query = query.Where(m => m.IsActive);
            }

            return query.OrderBy(m => m.MachineCode).ToList();
        }

        public Machine? GetMachineById(int id)
        {
            return _context.Machines.FirstOrDefault(m => m.Id == id);
        }

        public Machine? GetMachineByCode(string machineCode)
        {
            return _context.Machines.FirstOrDefault(m => m.MachineCode == machineCode);
        }

        public int CreateMachine(Machine machine)
        {
            _context.Machines.Add(machine);
            _context.SaveChanges();
            return machine.Id;
        }

        public bool UpdateMachine(Machine machine)
        {
            _context.Machines.Update(machine);
            return _context.SaveChanges() > 0;
        }

        public bool DeleteMachine(int id)
        {
            var machine = GetMachineById(id);
            if (machine == null) return false;

            machine.IsActive = false;
            return UpdateMachine(machine);
        }

        public List<Machine> GetMachinesByType(string machineType)
        {
            return _context.Machines
                .Where(m => m.IsActive && m.MachineType == machineType)
                .OrderBy(m => m.MachineName)
                .ToList();
        }

        public List<Machine> GetMachinesByStatus(string status)
        {
            return _context.Machines
                .Where(m => m.IsActive && m.Status == status)
                .OrderBy(m => m.MachineCode)
                .ToList();
        }

        public List<Machine> GetOperationalMachines()
        {
            return GetMachinesByStatus("Operational");
        }

        public List<Machine> GetMachinesInMaintenance()
        {
            return GetMachinesByStatus("Maintenance");
        }

        public List<Machine> GetMachinesWithBreakdown()
        {
            return GetMachinesByStatus("Breakdown");
        }

        public List<Machine> GetMachinesDueForMaintenance()
        {
            var sevenDaysFromNow = DateTime.Now.AddDays(7);
            return _context.Machines
                .Where(m => m.IsActive &&
                           m.NextMaintenanceDue.HasValue &&
                           m.NextMaintenanceDue.Value <= sevenDaysFromNow)
                .OrderBy(m => m.NextMaintenanceDue)
                .ToList();
        }

        public List<Machine> SearchMachines(string searchTerm)
        {
            var lowerSearchTerm = searchTerm.ToLower();
            return _context.Machines
                .Where(m => m.IsActive &&
                           (m.MachineCode.ToLower().Contains(lowerSearchTerm) ||
                            m.MachineName.ToLower().Contains(lowerSearchTerm) ||
                            (m.MachineType != null && m.MachineType.ToLower().Contains(lowerSearchTerm)) ||
                            (m.Manufacturer != null && m.Manufacturer.ToLower().Contains(lowerSearchTerm))))
                .OrderBy(m => m.MachineCode)
                .ToList();
        }

        public string GenerateMachineCode()
        {
            var lastMachine = _context.Machines
                .OrderByDescending(m => m.Id)
                .FirstOrDefault();

            if (lastMachine == null)
            {
                return "MACH0001";
            }

            // Extract number from last code (e.g., MACH0001 -> 0001)
            var lastCode = lastMachine.MachineCode;
            var numberPart = lastCode.Substring(4); // Skip "MACH"

            if (int.TryParse(numberPart, out int lastNumber))
            {
                var newNumber = lastNumber + 1;
                return $"MACH{newNumber:D4}";
            }

            return "MACH0001";
        }

        public int GetTotalMachinesCount()
        {
            return _context.Machines.Count(m => m.IsActive);
        }

        public int GetOperationalMachinesCount()
        {
            return _context.Machines.Count(m => m.IsActive && m.Status == "Operational");
        }

        public int GetMachinesInMaintenanceCount()
        {
            return _context.Machines.Count(m => m.IsActive && m.Status == "Maintenance");
        }

        public decimal GetTotalMachineValue()
        {
            return _context.Machines
                .Where(m => m.IsActive && m.CurrentValue.HasValue)
                .Sum(m => m.CurrentValue ?? 0);
        }
    }
}
