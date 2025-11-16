using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface ILoansAdvancesRepository
    {
        List<LoanAdvance> GetAll(bool activeOnly = true);
        LoanAdvance? GetById(int id);
        int Insert(LoanAdvance model);
        bool Update(LoanAdvance model);
        bool Delete(int id, string deletedBy);
    }

    public class LoansAdvancesRepository : ILoansAdvancesRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public LoansAdvancesRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<LoanAdvance> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_LoansAdvances_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public LoanAdvance? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_LoansAdvances_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(LoanAdvance model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@TransactionDate", model.Date),  // Fixed: Database column is TransactionDate
                _dbHelper.CreateParameter("@VoucherNumber", model.VoucherNumber ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@Particulars", model.Particulars),
                _dbHelper.CreateParameter("@PartyName", model.PartyName),
                _dbHelper.CreateParameter("@AmountGiven", model.AmountGiven),
                _dbHelper.CreateParameter("@Repayment", model.Repayment),
                _dbHelper.CreateParameter("@RepaymentDate", model.RepaymentDate ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@Balance", model.Balance),
                _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_LoansAdvances_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(LoanAdvance model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@TransactionDate", model.Date),  // Fixed: Database column is TransactionDate
                    _dbHelper.CreateParameter("@VoucherNumber", model.VoucherNumber ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@Particulars", model.Particulars),
                    _dbHelper.CreateParameter("@PartyName", model.PartyName),
                    _dbHelper.CreateParameter("@AmountGiven", model.AmountGiven),
                    _dbHelper.CreateParameter("@Repayment", model.Repayment),
                    _dbHelper.CreateParameter("@RepaymentDate", model.RepaymentDate ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@Balance", model.Balance),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value)
                };
                _dbHelper.ExecuteNonQuery("sp_LoansAdvances_Update", parameters);
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
                _dbHelper.ExecuteNonQuery("sp_LoansAdvances_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<LoanAdvance> ConvertDataTableToList(DataTable dt)
        {
            List<LoanAdvance> list = new List<LoanAdvance>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private LoanAdvance ConvertDataRowToModel(DataRow row)
        {
            return new LoanAdvance
            {
                Id = Convert.ToInt32(row["Id"]),
                Date = Convert.ToDateTime(row["TransactionDate"]),  // Fixed: Database column is TransactionDate
                VoucherNumber = row["VoucherNumber"] != DBNull.Value ? row["VoucherNumber"].ToString() : null,
                Particulars = row["Particulars"]?.ToString(),
                PartyName = row["PartyName"]?.ToString(),
                AmountGiven = Convert.ToDecimal(row["AmountGiven"]),
                Repayment = Convert.ToDecimal(row["Repayment"]),
                RepaymentDate = row["RepaymentDate"] != DBNull.Value ? Convert.ToDateTime(row["RepaymentDate"]) : null,
                Balance = Convert.ToDecimal(row["Balance"]),
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}
