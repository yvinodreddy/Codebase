using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface ICashBookRepository
    {
        List<CashBook> GetAll(bool activeOnly = true);
        CashBook? GetById(int id);
        int Insert(CashBook model);
        bool Update(CashBook model);
        bool Delete(int id, string deletedBy);
    }

    public class CashBookRepository : ICashBookRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public CashBookRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<CashBook> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_CashBook_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public CashBook? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_CashBook_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(CashBook model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@TransactionDate", model.TransactionDate),
                _dbHelper.CreateParameter("@VoucherNumber", model.VoucherNumber ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@Particulars", model.Particulars),
                _dbHelper.CreateParameter("@Receipts", model.Receipts),
                _dbHelper.CreateParameter("@Payments", model.Payments),
                _dbHelper.CreateParameter("@Balance", model.Balance),
                _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@CreatedBy", model.CreatedBy ?? (object)DBNull.Value),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_CashBook_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(CashBook model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@TransactionDate", model.TransactionDate),
                    _dbHelper.CreateParameter("@VoucherNumber", model.VoucherNumber ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@Particulars", model.Particulars),
                    _dbHelper.CreateParameter("@Receipts", model.Receipts),
                    _dbHelper.CreateParameter("@Payments", model.Payments),
                    _dbHelper.CreateParameter("@Balance", model.Balance),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value)
                };
                _dbHelper.ExecuteNonQuery("sp_CashBook_Update", parameters);
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
                _dbHelper.ExecuteNonQuery("sp_CashBook_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<CashBook> ConvertDataTableToList(DataTable dt)
        {
            List<CashBook> list = new List<CashBook>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private CashBook ConvertDataRowToModel(DataRow row)
        {
            return new CashBook
            {
                Id = Convert.ToInt32(row["Id"]),
                TransactionDate = Convert.ToDateTime(row["TransactionDate"]),
                VoucherNumber = row["VoucherNumber"] != DBNull.Value ? row["VoucherNumber"].ToString() : null,
                Particulars = row["Particulars"]?.ToString(),
                Receipts = Convert.ToDecimal(row["Receipts"]),
                Payments = Convert.ToDecimal(row["Payments"]),
                Balance = Convert.ToDecimal(row["Balance"]),
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                CreatedBy = row.Table.Columns.Contains("CreatedBy") && row["CreatedBy"] != DBNull.Value ? row["CreatedBy"].ToString() : null,
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}
