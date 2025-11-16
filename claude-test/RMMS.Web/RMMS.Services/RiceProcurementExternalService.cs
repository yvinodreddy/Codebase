using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface IRiceProcurementExternalService
    {
        List<RiceProcurementExternal> GetAll();
        RiceProcurementExternal? GetById(int id);
        void Create(RiceProcurementExternal model, string username);
        void Update(RiceProcurementExternal model, string username);
        void Delete(int id, string username);
    }

    public class RiceProcurementExternalService : IRiceProcurementExternalService
    {
        private readonly IRiceProcurementExternalRepository _repository;

        public RiceProcurementExternalService(IRiceProcurementExternalRepository repository)
        {
            _repository = repository;
        }

        public List<RiceProcurementExternal> GetAll()
        {
            return _repository.GetAll(activeOnly: true);
        }

        public RiceProcurementExternal? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(RiceProcurementExternal model, string username)
        {
            model.TotalAmount = model.Quantity * model.Rate;
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;
            _repository.Insert(model);
        }

        public void Update(RiceProcurementExternal model, string username)
        {
            model.TotalAmount = model.Quantity * model.Rate;
            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            _repository.Delete(id, username);
        }
    }
}
