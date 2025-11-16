using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IVouchersRepository
    {
        List<Voucher> GetAll(bool activeOnly = true);
        Voucher? GetById(int id);
        int Insert(Voucher model);
        bool Update(Voucher model);
        bool Delete(int id, string deletedBy);
    }

    public class VouchersRepository : IVouchersRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public VouchersRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<Voucher> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_Vouchers_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public Voucher? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_Vouchers_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(Voucher model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@VoucherDate", model.VoucherDate),
                _dbHelper.CreateParameter("@VoucherNumber", model.VoucherNumber),
                _dbHelper.CreateParameter("@VoucherType", model.VoucherType),
                _dbHelper.CreateParameter("@Particulars", model.Particulars),
                _dbHelper.CreateParameter("@Amount", model.Amount),
                _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@CreatedBy", model.CreatedBy ?? (object)DBNull.Value),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_Vouchers_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(Voucher model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@VoucherDate", model.VoucherDate),
                    _dbHelper.CreateParameter("@VoucherNumber", model.VoucherNumber),
                    _dbHelper.CreateParameter("@VoucherType", model.VoucherType),
                    _dbHelper.CreateParameter("@Particulars", model.Particulars),
                    _dbHelper.CreateParameter("@Amount", model.Amount),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value)
                };
                _dbHelper.ExecuteNonQuery("sp_Vouchers_Update", parameters);
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
                _dbHelper.ExecuteNonQuery("sp_Vouchers_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<Voucher> ConvertDataTableToList(DataTable dt)
        {
            List<Voucher> list = new List<Voucher>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private Voucher ConvertDataRowToModel(DataRow row)
        {
            return new Voucher
            {
                Id = Convert.ToInt32(row["Id"]),
                VoucherDate = Convert.ToDateTime(row["VoucherDate"]),
                VoucherNumber = row["VoucherNumber"]?.ToString(),
                VoucherType = row["VoucherType"]?.ToString(),
                Particulars = row["Particulars"]?.ToString(),
                Amount = Convert.ToDecimal(row["Amount"]),
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                CreatedBy = row.Table.Columns.Contains("CreatedBy") && row["CreatedBy"] != DBNull.Value ? row["CreatedBy"].ToString() : null,
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}
