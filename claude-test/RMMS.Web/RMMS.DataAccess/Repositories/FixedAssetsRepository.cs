using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IFixedAssetsRepository
    {
        List<FixedAsset> GetAll(bool activeOnly = true);
        FixedAsset? GetById(int id);
        int Insert(FixedAsset model);
        bool Update(FixedAsset model);
        bool Delete(int id, string deletedBy);
    }

    public class FixedAssetsRepository : IFixedAssetsRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public FixedAssetsRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<FixedAsset> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_FixedAssets_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public FixedAsset? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_FixedAssets_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(FixedAsset model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@AssetCode", model.AssetId),  // Fixed: Database column is AssetCode
                _dbHelper.CreateParameter("@PurchaseDate", model.PurchaseDate),
                _dbHelper.CreateParameter("@AssetName", model.AssetName),
                _dbHelper.CreateParameter("@Description", model.Description ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@Supplier", model.Supplier),
                _dbHelper.CreateParameter("@PurchaseValue", model.PurchaseValue),
                _dbHelper.CreateParameter("@DepreciationRate", model.DepreciationRate),
                _dbHelper.CreateParameter("@AccumulatedDepreciation", model.AccumulatedDepreciation),
                _dbHelper.CreateParameter("@NetBookValue", model.NetBookValue),
                _dbHelper.CreateParameter("@PresentValueApprox", model.PresentValueApprox),
                _dbHelper.CreateParameter("@AssetStatus", model.Status ?? (object)DBNull.Value),  // Fixed: Database column is AssetStatus
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_FixedAssets_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(FixedAsset model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@AssetCode", model.AssetId),  // Fixed: Database column is AssetCode
                    _dbHelper.CreateParameter("@PurchaseDate", model.PurchaseDate),
                    _dbHelper.CreateParameter("@AssetName", model.AssetName),
                    _dbHelper.CreateParameter("@Description", model.Description ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@Supplier", model.Supplier),
                    _dbHelper.CreateParameter("@PurchaseValue", model.PurchaseValue),
                    _dbHelper.CreateParameter("@DepreciationRate", model.DepreciationRate),
                    _dbHelper.CreateParameter("@AccumulatedDepreciation", model.AccumulatedDepreciation),
                    _dbHelper.CreateParameter("@NetBookValue", model.NetBookValue),
                    _dbHelper.CreateParameter("@PresentValueApprox", model.PresentValueApprox),
                    _dbHelper.CreateParameter("@Status", model.Status ?? (object)DBNull.Value)
                };
                _dbHelper.ExecuteNonQuery("sp_FixedAssets_Update", parameters);
                return true;
            }
            catch { return false; }
        }

        public bool Delete(int id, string deletedBy)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", id),
                    _dbHelper.CreateParameter("@DeletedBy", deletedBy)
                };
                _dbHelper.ExecuteNonQuery("sp_FixedAssets_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<FixedAsset> ConvertDataTableToList(DataTable dt)
        {
            List<FixedAsset> list = new List<FixedAsset>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private FixedAsset ConvertDataRowToModel(DataRow row)
        {
            return new FixedAsset
            {
                Id = Convert.ToInt32(row["Id"]),
                AssetId = row["AssetId"]?.ToString(),  // Database column is AssetId
                PurchaseDate = Convert.ToDateTime(row["PurchaseDate"]),
                AssetName = row["AssetName"]?.ToString(),
                Description = row["Description"] != DBNull.Value ? row["Description"].ToString() : null,
                Supplier = row["Supplier"]?.ToString(),
                PurchaseValue = Convert.ToDecimal(row["PurchaseValue"]),
                DepreciationRate = Convert.ToDecimal(row["DepreciationRate"]),
                AccumulatedDepreciation = Convert.ToDecimal(row["AccumulatedDepreciation"]),
                NetBookValue = Convert.ToDecimal(row["NetBookValue"]),
                PresentValueApprox = Convert.ToDecimal(row["PresentValueApprox"]),
                Status = row["Status"] != DBNull.Value ? row["Status"].ToString() : null,  // Database column is Status
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}
