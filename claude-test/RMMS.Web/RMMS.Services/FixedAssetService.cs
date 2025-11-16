using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RMMS.Services
{
    public class FixedAssetService : IFixedAssetService
    {
        private readonly IFixedAssetsRepository _repository;

        public FixedAssetService(IFixedAssetsRepository repository)
        {
            _repository = repository;
        }

        public List<FixedAsset> GetAll()
        {
            return _repository.GetAll(activeOnly: true).OrderBy(f => f.AssetId).ToList();
        }

        public FixedAsset? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(FixedAsset model, string username)
        {
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;
            model.Status = "Active";

            // Calculate initial values
            model.AccumulatedDepreciation = 0;
            model.NetBookValue = model.PurchaseValue;
            model.PresentValueApprox = model.PurchaseValue;

            _repository.Insert(model);
        }

        public void Update(FixedAsset model, string username)
        {
            var existing = _repository.GetById(model.Id);
            if (existing == null)
            {
                throw new ArgumentException($"Fixed asset with ID {model.Id} not found.");
            }

            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            var asset = _repository.GetById(id);
            if (asset == null)
            {
                throw new ArgumentException($"Fixed asset with ID {id} not found.");
            }

            asset.IsActive = false;
            asset.Status = "Disposed";
            _repository.Update(asset);
        }

        public void CalculateDepreciation(int id)
        {
            var asset = _repository.GetById(id);
            if (asset == null)
            {
                throw new ArgumentException($"Fixed asset with ID {id} not found.");
            }

            if (asset.DepreciationRate > 0)
            {
                // Calculate years since purchase
                int yearsElapsed = DateTime.Now.Year - asset.PurchaseDate.Year;

                // Simple straight-line depreciation calculation
                decimal yearlyDepreciation = (asset.PurchaseValue * asset.DepreciationRate) / 100;
                asset.AccumulatedDepreciation = yearlyDepreciation * yearsElapsed;

                // Ensure depreciation doesn't exceed asset value
                if (asset.AccumulatedDepreciation > asset.PurchaseValue)
                {
                    asset.AccumulatedDepreciation = asset.PurchaseValue;
                }

                asset.NetBookValue = asset.PurchaseValue - asset.AccumulatedDepreciation;
                _repository.Update(asset);
            }
        }

        public decimal GetTotalAssetValue()
        {
            return _repository.GetAll(activeOnly: true)
                .Where(f => f.Status == "Active")
                .Sum(f => f.PurchaseValue);
        }

        public decimal GetTotalDepreciation()
        {
            return _repository.GetAll(activeOnly: true)
                .Sum(f => f.AccumulatedDepreciation);
        }

        public List<FixedAsset> GetActiveAssets()
        {
            return _repository.GetAll(activeOnly: true)
                .Where(f => f.Status == "Active")
                .OrderBy(f => f.AssetName)
                .ToList();
        }
    }
}
