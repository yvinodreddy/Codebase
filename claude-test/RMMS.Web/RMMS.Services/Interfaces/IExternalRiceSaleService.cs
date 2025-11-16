using RMMS.Models;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface IExternalRiceSaleService
    {
        List<ExternalRiceSale> GetAll();
        ExternalRiceSale? GetById(int id);
        void Create(ExternalRiceSale model, string username);
        void Update(ExternalRiceSale model, string username);
        void Delete(int id, string username);
    }
}
