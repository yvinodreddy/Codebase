using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public interface IFixedAssetService
    {
        List<FixedAsset> GetAll();
        FixedAsset? GetById(int id);
        void Create(FixedAsset model, string username);
        void Update(FixedAsset model, string username);
        void Delete(int id, string username);
        void CalculateDepreciation(int id);
        decimal GetTotalAssetValue();
        decimal GetTotalDepreciation();
        List<FixedAsset> GetActiveAssets();
    }
}