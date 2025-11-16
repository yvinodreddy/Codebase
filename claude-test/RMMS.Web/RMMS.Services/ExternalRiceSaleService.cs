using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public class ExternalRiceSaleService : IExternalRiceSaleService
    {
        private readonly IExternalRiceSalesRepository _repository;

        public ExternalRiceSaleService(IExternalRiceSalesRepository repository)
        {
            _repository = repository;
        }

        public List<ExternalRiceSale> GetAll()
        {
            return _repository.GetAll(activeOnly: true);
        }

        public ExternalRiceSale? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(ExternalRiceSale model, string username)
        {
            model.TotalAmount = model.Quantity * model.Rate;
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;
            _repository.Insert(model);
        }

        public void Update(ExternalRiceSale model, string username)
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
