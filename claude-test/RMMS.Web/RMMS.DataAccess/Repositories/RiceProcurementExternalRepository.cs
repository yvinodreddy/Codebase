using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IRiceProcurementExternalRepository
    {
        List<RiceProcurementExternal> GetAll(bool activeOnly = true);
        RiceProcurementExternal? GetById(int id);
        int Insert(RiceProcurementExternal model);
        bool Update(RiceProcurementExternal model);
        bool Delete(int id, string deletedBy);
    }

    public class RiceProcurementExternalRepository : IRiceProcurementExternalRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public RiceProcurementExternalRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<RiceProcurementExternal> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_RiceProcurementExternal_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public RiceProcurementExternal? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_RiceProcurementExternal_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(RiceProcurementExternal model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@Date", model.Date),
                _dbHelper.CreateParameter("@ItemDescription", model.ItemDescription),
                _dbHelper.CreateParameter("@ProcuredFrom", model.ProcuredFrom),
                _dbHelper.CreateParameter("@ProcuredBy", model.ProcuredBy),
                _dbHelper.CreateParameter("@Quantity", model.Quantity),
                _dbHelper.CreateParameter("@Rate", model.Rate),
                _dbHelper.CreateParameter("@TotalAmount", model.TotalAmount),
                _dbHelper.CreateParameter("@PaymentMode", model.PaymentMode ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@PaymentStatus", model.PaymentStatus ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@Balance", model.Balance),
                _dbHelper.CreateParameter("@FullPaymentDate", model.FullPaymentDate ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_RiceProcurementExternal_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(RiceProcurementExternal model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@Date", model.Date),
                    _dbHelper.CreateParameter("@ItemDescription", model.ItemDescription),
                    _dbHelper.CreateParameter("@ProcuredFrom", model.ProcuredFrom),
                    _dbHelper.CreateParameter("@ProcuredBy", model.ProcuredBy),
                    _dbHelper.CreateParameter("@Quantity", model.Quantity),
                    _dbHelper.CreateParameter("@Rate", model.Rate),
                    _dbHelper.CreateParameter("@TotalAmount", model.TotalAmount),
                    _dbHelper.CreateParameter("@PaymentMode", model.PaymentMode ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@PaymentStatus", model.PaymentStatus ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@Balance", model.Balance),
                    _dbHelper.CreateParameter("@FullPaymentDate", model.FullPaymentDate ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value)
                };
                _dbHelper.ExecuteNonQuery("sp_RiceProcurementExternal_Update", parameters);
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
                _dbHelper.ExecuteNonQuery("sp_RiceProcurementExternal_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<RiceProcurementExternal> ConvertDataTableToList(DataTable dt)
        {
            List<RiceProcurementExternal> list = new List<RiceProcurementExternal>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private RiceProcurementExternal ConvertDataRowToModel(DataRow row)
        {
            // Helper function to safely get column value
            T? GetValue<T>(string columnName, T? defaultValue = default)
            {
                if (!row.Table.Columns.Contains(columnName) || row[columnName] == DBNull.Value)
                    return defaultValue;
                return (T)Convert.ChangeType(row[columnName], typeof(T));
            }

            return new RiceProcurementExternal
            {
                Id = GetValue<int>("Id", 0),
                Date = GetValue<DateTime>("Date", DateTime.Now), // Handle potential column name mismatch
                ItemDescription = GetValue<string?>("ItemDescription", null) ?? string.Empty,
                ProcuredFrom = GetValue<string?>("ProcuredFrom", null) ?? string.Empty,
                ProcuredBy = GetValue<string?>("ProcuredBy", null) ?? string.Empty,
                Quantity = GetValue<decimal>("Quantity", 0),
                Rate = GetValue<decimal>("Rate", 0),
                TotalAmount = GetValue<decimal>("TotalAmount", 0),
                PaymentMode = GetValue<string?>("PaymentMode", null) ?? string.Empty,
                PaymentStatus = GetValue<string?>("PaymentStatus", null) ?? string.Empty,
                Balance = GetValue<decimal>("Balance", 0),
                FullPaymentDate = row.Table.Columns.Contains("FullPaymentDate") && row["FullPaymentDate"] != DBNull.Value
                    ? (DateTime?)row["FullPaymentDate"]
                    : null,
                Remarks = GetValue<string?>("Remarks", null) ?? string.Empty,
                CreatedDate = GetValue<DateTime>("CreatedDate", DateTime.Now),
                IsActive = GetValue<bool>("IsActive", true)
            };
        }
    }
}
