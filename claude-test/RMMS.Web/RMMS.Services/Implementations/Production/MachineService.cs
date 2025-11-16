using RMMS.DataAccess.Repositories.Production;
using RMMS.Models.Production;
using RMMS.Services.Interfaces.Production;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services.Implementations.Production
{
    public class MachineService : IMachineService
    {
        private readonly IMachineRepository _machineRepository;

        public MachineService(IMachineRepository machineRepository)
        {
            _machineRepository = machineRepository;
        }

        public List<Machine> GetAllMachines(bool activeOnly = true)
        {
            return _machineRepository.GetAllMachines(activeOnly);
        }

        public Machine? GetMachineById(int id)
        {
            return _machineRepository.GetMachineById(id);
        }

        public Machine? GetMachineByCode(string machineCode)
        {
            return _machineRepository.GetMachineByCode(machineCode);
        }

        public int CreateMachine(Machine machine, string createdBy)
        {
            // Generate machine code if not provided
            if (string.IsNullOrEmpty(machine.MachineCode))
            {
                machine.MachineCode = GenerateMachineCode();
            }

            // Set audit fields
            machine.CreatedDate = DateTime.Now;
            machine.CreatedBy = createdBy;
            machine.IsActive = true;

            // Set initial current value if not provided
            if (!machine.CurrentValue.HasValue && machine.PurchasePrice.HasValue)
            {
                machine.CurrentValue = machine.PurchasePrice;
            }

            // Calculate next maintenance due if maintenance interval is provided
            if (machine.MaintenanceIntervalHours.HasValue && machine.MaintenanceIntervalHours.Value > 0)
            {
                // Estimate based on capacity (assuming 8 hours/day operation)
                var estimatedDaysToMaintenance = (int)(machine.MaintenanceIntervalHours.Value / 8);
                machine.NextMaintenanceDue = DateTime.Now.AddDays(estimatedDaysToMaintenance);
            }

            return _machineRepository.CreateMachine(machine);
        }

        public bool UpdateMachine(Machine machine, string modifiedBy)
        {
            // Set audit fields
            machine.ModifiedDate = DateTime.Now;
            machine.ModifiedBy = modifiedBy;

            return _machineRepository.UpdateMachine(machine);
        }

        public bool DeleteMachine(int id, string deletedBy)
        {
            var machine = _machineRepository.GetMachineById(id);
            if (machine == null) return false;

            machine.ModifiedDate = DateTime.Now;
            machine.ModifiedBy = deletedBy;

            return _machineRepository.DeleteMachine(id);
        }

        public List<Machine> GetMachinesByType(string machineType)
        {
            return _machineRepository.GetMachinesByType(machineType);
        }

        public List<Machine> GetMachinesByStatus(string status)
        {
            return _machineRepository.GetMachinesByStatus(status);
        }

        public List<Machine> GetOperationalMachines()
        {
            return _machineRepository.GetOperationalMachines();
        }

        public List<Machine> GetMachinesInMaintenance()
        {
            return _machineRepository.GetMachinesInMaintenance();
        }

        public List<Machine> GetMachinesWithBreakdown()
        {
            return _machineRepository.GetMachinesWithBreakdown();
        }

        public List<Machine> GetMachinesDueForMaintenance()
        {
            return _machineRepository.GetMachinesDueForMaintenance();
        }

        public List<Machine> SearchMachines(string searchTerm)
        {
            return _machineRepository.SearchMachines(searchTerm);
        }

        public bool RecordMaintenance(int machineId, string performedBy, string remarks)
        {
            var machine = _machineRepository.GetMachineById(machineId);
            if (machine == null) return false;

            // Update maintenance dates
            machine.LastMaintenanceDate = DateTime.Now;

            // Calculate next maintenance due
            if (machine.MaintenanceIntervalHours.HasValue && machine.MaintenanceIntervalHours.Value > 0)
            {
                var estimatedDaysToMaintenance = (int)(machine.MaintenanceIntervalHours.Value / 8);
                machine.NextMaintenanceDue = DateTime.Now.AddDays(estimatedDaysToMaintenance);
            }

            // Reset to operational status
            machine.Status = "Operational";

            // Update remarks
            if (!string.IsNullOrEmpty(remarks))
            {
                machine.Remarks = $"[{DateTime.Now:dd-MMM-yyyy}] Maintenance: {remarks}";
            }

            return UpdateMachine(machine, performedBy);
        }

        public bool UpdateRunningHours(int machineId, decimal hours)
        {
            var machine = _machineRepository.GetMachineById(machineId);
            if (machine == null) return false;

            machine.RunningHours += hours;

            // Check if maintenance is due based on running hours
            if (machine.MaintenanceIntervalHours.HasValue &&
                machine.LastMaintenanceDate.HasValue)
            {
                var hoursSinceLastMaintenance = machine.RunningHours;
                if (hoursSinceLastMaintenance >= machine.MaintenanceIntervalHours.Value)
                {
                    machine.Status = "Maintenance";
                }
            }

            return _machineRepository.UpdateMachine(machine);
        }

        public bool ChangeStatus(int machineId, string newStatus, string modifiedBy)
        {
            var machine = _machineRepository.GetMachineById(machineId);
            if (machine == null) return false;

            machine.Status = newStatus;

            return UpdateMachine(machine, modifiedBy);
        }

        public string GenerateMachineCode()
        {
            return _machineRepository.GenerateMachineCode();
        }

        public int GetTotalMachinesCount()
        {
            return _machineRepository.GetTotalMachinesCount();
        }

        public int GetOperationalMachinesCount()
        {
            return _machineRepository.GetOperationalMachinesCount();
        }

        public int GetMachinesInMaintenanceCount()
        {
            return _machineRepository.GetMachinesInMaintenanceCount();
        }

        public decimal GetTotalMachineValue()
        {
            return _machineRepository.GetTotalMachineValue();
        }

        public decimal GetAverageDepreciation()
        {
            var machines = _machineRepository.GetAllMachines(true);
            if (machines.Count == 0) return 0;

            var depreciatedMachines = machines
                .Where(m => m.PurchasePrice.HasValue && m.PurchasePrice.Value > 0)
                .ToList();

            if (depreciatedMachines.Count == 0) return 0;

            var totalDepreciation = depreciatedMachines.Sum(m => m.DepreciationPercent);
            return totalDepreciation / depreciatedMachines.Count;
        }
    }
}
