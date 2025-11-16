using RMMS.Models.Production;
using System.Collections.Generic;

namespace RMMS.DataAccess.Repositories.Production
{
    public interface IMachineRepository
    {
        // Basic CRUD operations
        List<Machine> GetAllMachines(bool activeOnly = true);
        Machine? GetMachineById(int id);
        Machine? GetMachineByCode(string machineCode);
        int CreateMachine(Machine machine);
        bool UpdateMachine(Machine machine);
        bool DeleteMachine(int id);

        // Query operations
        List<Machine> GetMachinesByType(string machineType);
        List<Machine> GetMachinesByStatus(string status);
        List<Machine> GetOperationalMachines();
        List<Machine> GetMachinesInMaintenance();
        List<Machine> GetMachinesWithBreakdown();
        List<Machine> GetMachinesDueForMaintenance();
        List<Machine> SearchMachines(string searchTerm);

        // Code generation
        string GenerateMachineCode();

        // Statistics
        int GetTotalMachinesCount();
        int GetOperationalMachinesCount();
        int GetMachinesInMaintenanceCount();
        decimal GetTotalMachineValue();
    }
}
