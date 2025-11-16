// RMMS.DataAccess/Repositories/PaddyProcurementRepository.cs
using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using System.Linq;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IPaddyProcurementRepository
    {
        List<PaddyProcurement> GetAll(bool activeOnly = true);
        PaddyProcurement? GetById(int id);
        int Insert(PaddyProcurement model);
        bool Update(PaddyProcurement model);
        bool Delete(int id, string deletedBy);
        List<PaddyProcurement> Search(string supplierName, string variety, DateTime? startDate, DateTime? endDate, string voucherNumber);
        DataTable GetStockSummary();
        string GenerateVoucherNumber();
    }

    public class PaddyProcurementRepository : IPaddyProcurementRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public PaddyProcurementRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<PaddyProcurement> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@IsActiveOnly", activeOnly)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_PaddyProcurement_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public PaddyProcurement? GetById(int id)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@Id", id)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_PaddyProcurement_GetById", parameters);

            if (dt.Rows.Count > 0)
            {
                return ConvertDataRowToModel(dt.Rows[0]);
            }

            return null;
        }

        public int Insert(PaddyProcurement model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@ReceiptDate", model.ReceiptDate),
                _dbHelper.CreateParameter("@VoucherNumber", model.VoucherNumber),
                _dbHelper.CreateParameter("@SupplierName", model.SupplierName),
                _dbHelper.CreateParameter("@PurchaseOrderNumber", model.PurchaseOrderNumber),
                _dbHelper.CreateParameter("@PaddyVariety", model.PaddyVariety),
                _dbHelper.CreateParameter("@Grade", model.Grade),
                _dbHelper.CreateParameter("@MoistureContent", model.MoistureContent),
                _dbHelper.CreateParameter("@QuantityReceived", model.QuantityReceived),
                _dbHelper.CreateParameter("@WeightPerBag", model.WeightPerBag),
                _dbHelper.CreateParameter("@TotalNetWeight", model.TotalNetWeight),
                _dbHelper.CreateParameter("@StorageDate", model.StorageDate),
                _dbHelper.CreateParameter("@StorageLocation", model.StorageLocation),
                _dbHelper.CreateParameter("@OpeningStock", model.OpeningStock),
                _dbHelper.CreateParameter("@Issues", model.Issues),
                _dbHelper.CreateParameter("@ClosingStock", model.ClosingStock),
                _dbHelper.CreateParameter("@LossShrinkage", model.LossShrinkage),
                _dbHelper.CreateParameter("@Remarks", model.Remarks),
                _dbHelper.CreateParameter("@ResponsiblePerson", model.ResponsiblePerson),
                _dbHelper.CreateParameter("@CreatedBy", model.CreatedBy),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };

            _dbHelper.ExecuteWithOutput("sp_PaddyProcurement_Insert", parameters);

            // Get the output parameter value
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(PaddyProcurement model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@ReceiptDate", model.ReceiptDate),
                    _dbHelper.CreateParameter("@VoucherNumber", model.VoucherNumber),
                    _dbHelper.CreateParameter("@SupplierName", model.SupplierName),
                    _dbHelper.CreateParameter("@PurchaseOrderNumber", model.PurchaseOrderNumber),
                    _dbHelper.CreateParameter("@PaddyVariety", model.PaddyVariety),
                    _dbHelper.CreateParameter("@Grade", model.Grade),
                    _dbHelper.CreateParameter("@MoistureContent", model.MoistureContent),
                    _dbHelper.CreateParameter("@QuantityReceived", model.QuantityReceived),
                    _dbHelper.CreateParameter("@WeightPerBag", model.WeightPerBag),
                    _dbHelper.CreateParameter("@TotalNetWeight", model.TotalNetWeight),
                    _dbHelper.CreateParameter("@StorageDate", model.StorageDate),
                    _dbHelper.CreateParameter("@StorageLocation", model.StorageLocation),
                    _dbHelper.CreateParameter("@OpeningStock", model.OpeningStock),
                    _dbHelper.CreateParameter("@Issues", model.Issues),
                    _dbHelper.CreateParameter("@ClosingStock", model.ClosingStock),
                    _dbHelper.CreateParameter("@LossShrinkage", model.LossShrinkage),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks),
                    _dbHelper.CreateParameter("@ResponsiblePerson", model.ResponsiblePerson),
                    _dbHelper.CreateParameter("@ModifiedBy", model.ModifiedBy)
                };

                _dbHelper.ExecuteNonQuery("sp_PaddyProcurement_Update", parameters);
                return true;
            }
            catch
            {
                return false;
            }
        }

        public bool Delete(int id, string deletedBy)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", id),
                    _dbHelper.CreateParameter("@DeletedBy", deletedBy)
                };

                _dbHelper.ExecuteNonQuery("sp_PaddyProcurement_Delete", parameters);
                return true;
            }
            catch
            {
                return false;
            }
        }

        public List<PaddyProcurement> Search(string supplierName, string variety, DateTime? startDate, DateTime? endDate, string voucherNumber)
        { 

            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@SupplierName", supplierName),
                _dbHelper.CreateParameter("@PaddyVariety", variety),
                _dbHelper.CreateParameter("@StartDate", startDate),
                _dbHelper.CreateParameter("@EndDate", endDate),
                _dbHelper.CreateParameter("@VoucherNumber", voucherNumber)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_PaddyProcurement_Search", parameters);
            return ConvertDataTableToList(dt);
        }

        public DataTable GetStockSummary()
        {
            return _dbHelper.ExecuteDataTable("sp_PaddyProcurement_GetStockSummary");
        }

        public string GenerateVoucherNumber()
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateOutputParameter("@VoucherNumber", SqlDbType.NVarChar)
            };
            parameters[0].Size = 50;

            _dbHelper.ExecuteWithOutput("sp_PaddyProcurement_GenerateVoucherNumber", parameters);

            return parameters[0].Value?.ToString() ?? string.Empty;
        }

        // Helper method to convert DataTable to List
        private List<PaddyProcurement> ConvertDataTableToList(DataTable dt)
        {
            List<PaddyProcurement> list = new List<PaddyProcurement>();

            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }

            return list;
        }

        // Helper method to convert DataRow to Model
        private PaddyProcurement ConvertDataRowToModel(DataRow row)
        {
            return new PaddyProcurement
            {
                Id = Convert.ToInt32(row["Id"]),
                ReceiptDate = Convert.ToDateTime(row["ReceiptDate"]),
                VoucherNumber = row["VoucherNumber"].ToString() ?? string.Empty,
                SupplierName = row["SupplierName"].ToString() ?? string.Empty,
                PurchaseOrderNumber = row["PurchaseOrderNumber"] != DBNull.Value ? row["PurchaseOrderNumber"].ToString() : null,
                PaddyVariety = row["PaddyVariety"].ToString() ?? string.Empty,
                Grade = row["Grade"] != DBNull.Value ? row["Grade"].ToString() : null,
                MoistureContent = row["MoistureContent"] != DBNull.Value ? Convert.ToDecimal(row["MoistureContent"]) : (decimal?)null,
                QuantityReceived = Convert.ToDecimal(row["QuantityReceived"]),
                WeightPerBag = row["WeightPerBag"] != DBNull.Value ? Convert.ToDecimal(row["WeightPerBag"]) : (decimal?)null,
                TotalNetWeight = Convert.ToDecimal(row["TotalNetWeight"]),
                StorageDate = row["StorageDate"] != DBNull.Value ? Convert.ToDateTime(row["StorageDate"]) : (DateTime?)null,
                StorageLocation = row["StorageLocation"] != DBNull.Value ? row["StorageLocation"].ToString() : null,
                OpeningStock = row["OpeningStock"] != DBNull.Value ? Convert.ToDecimal(row["OpeningStock"]) : (decimal?)null,
                Issues = row["Issues"] != DBNull.Value ? Convert.ToDecimal(row["Issues"]) : (decimal?)null,
                ClosingStock = row["ClosingStock"] != DBNull.Value ? Convert.ToDecimal(row["ClosingStock"]) : (decimal?)null,
                LossShrinkage = row["LossShrinkage"] != DBNull.Value ? Convert.ToDecimal(row["LossShrinkage"]) : (decimal?)null,
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                ResponsiblePerson = row["ResponsiblePerson"] != DBNull.Value ? row["ResponsiblePerson"].ToString() : null,

                // Check if system columns exist before accessing them
                CreatedDate = row.Table.Columns.Contains("CreatedDate") && row["CreatedDate"] != DBNull.Value
                    ? Convert.ToDateTime(row["CreatedDate"])
                    : DateTime.Now,

                ModifiedDate = row.Table.Columns.Contains("ModifiedDate") && row["ModifiedDate"] != DBNull.Value
                    ? Convert.ToDateTime(row["ModifiedDate"])
                    : (DateTime?)null,

                CreatedBy = row.Table.Columns.Contains("CreatedBy") && row["CreatedBy"] != DBNull.Value
                    ? row["CreatedBy"].ToString()
                    : null,

                ModifiedBy = row.Table.Columns.Contains("ModifiedBy") && row["ModifiedBy"] != DBNull.Value
                    ? row["ModifiedBy"].ToString()
                    : null,

                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}