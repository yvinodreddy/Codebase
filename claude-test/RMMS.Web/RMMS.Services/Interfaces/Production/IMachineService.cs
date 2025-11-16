using RMMS.Models.Production;
using System.Collections.Generic;

namespace RMMS.Services.Interfaces.Production
{
    public interface IMachineService
    {
        // Basic CRUD operations
        List<Machine> GetAllMachines(bool activeOnly = true);
        Machine? GetMachineById(int id);
        Machine? GetMachineByCode(string machineCode);
        int CreateMachine(Machine machine, string createdBy);
        bool UpdateMachine(Machine machine, string modifiedBy);
        bool DeleteMachine(int id, string deletedBy);

        // Query operations
        List<Machine> GetMachinesByType(string machineType);
        List<Machine> GetMachinesByStatus(string status);
        List<Machine> GetOperationalMachines();
        List<Machine> GetMachinesInMaintenance();
        List<Machine> GetMachinesWithBreakdown();
        List<Machine> GetMachinesDueForMaintenance();
        List<Machine> SearchMachines(string searchTerm);

        // Business operations
        bool RecordMaintenance(int machineId, string performedBy, string remarks);
        bool UpdateRunningHours(int machineId, decimal hours);
        bool ChangeStatus(int machineId, string newStatus, string modifiedBy);
        string GenerateMachineCode();

        // Statistics
        int GetTotalMachinesCount();
        int GetOperationalMachinesCount();
        int GetMachinesInMaintenanceCount();
        decimal GetTotalMachineValue();
        decimal GetAverageDepreciation();
    }
}
