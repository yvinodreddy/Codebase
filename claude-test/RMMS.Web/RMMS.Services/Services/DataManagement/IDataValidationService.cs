using System.Collections.Generic;
using System.Threading.Tasks;

namespace RMMS.Services.Services.DataManagement
{
    public interface IDataValidationService
    {
        Task<List<string>> ValidateEntityAsync(string entityType, object entity);
        Task<bool> AddValidationRuleAsync(string entityType, string ruleName, string ruleExpression);
        Task<List<object>> GetValidationRulesAsync(string entityType);
        Task<bool> ExecuteValidationAsync(int ruleId, object entity);
    }
}
