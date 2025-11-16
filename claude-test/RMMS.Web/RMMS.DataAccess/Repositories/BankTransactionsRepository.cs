using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IBankTransactionsRepository
    {
        List<BankTransaction> GetAll(bool activeOnly = true);
        BankTransaction? GetById(int id);
        int Insert(BankTransaction model);
        bool Update(BankTransaction model);
        bool Delete(int id, string deletedBy);
    }

    public class BankTransactionsRepository : IBankTransactionsRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public BankTransactionsRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<BankTransaction> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_BankTransactions_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public BankTransaction? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_BankTransactions_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(BankTransaction model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@TransactionDate", model.TransactionDate),
                _dbHelper.CreateParameter("@ChequeUtrNumber", model.ChequeUtrNumber ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@BankName", model.BankName),
                _dbHelper.CreateParameter("@AccountNumber", model.AccountNumber),
                _dbHelper.CreateParameter("@Particulars", model.Particulars),
                _dbHelper.CreateParameter("@Deposits", model.Deposits),
                _dbHelper.CreateParameter("@Withdrawals", model.Withdrawals),
                _dbHelper.CreateParameter("@Balance", model.Balance),
                _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_BankTransactions_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(BankTransaction model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@TransactionDate", model.TransactionDate),
                    _dbHelper.CreateParameter("@ChequeUtrNumber", model.ChequeUtrNumber ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@BankName", model.BankName),
                    _dbHelper.CreateParameter("@AccountNumber", model.AccountNumber),
                    _dbHelper.CreateParameter("@Particulars", model.Particulars),
                    _dbHelper.CreateParameter("@Deposits", model.Deposits),
                    _dbHelper.CreateParameter("@Withdrawals", model.Withdrawals),
                    _dbHelper.CreateParameter("@Balance", model.Balance),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value)
                };
                _dbHelper.ExecuteNonQuery("sp_BankTransactions_Update", parameters);
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
                _dbHelper.ExecuteNonQuery("sp_BankTransactions_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<BankTransaction> ConvertDataTableToList(DataTable dt)
        {
            List<BankTransaction> list = new List<BankTransaction>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private BankTransaction ConvertDataRowToModel(DataRow row)
        {
            return new BankTransaction
            {
                Id = Convert.ToInt32(row["Id"]),
                TransactionDate = Convert.ToDateTime(row["TransactionDate"]),
                ChequeUtrNumber = row["ChequeUtrNumber"] != DBNull.Value ? row["ChequeUtrNumber"].ToString() : null,
                BankName = row["BankName"]?.ToString(),
                AccountNumber = row["AccountNumber"]?.ToString(),
                Particulars = row["Particulars"]?.ToString(),
                Deposits = Convert.ToDecimal(row["Deposits"]),
                Withdrawals = Convert.ToDecimal(row["Withdrawals"]),
                Balance = Convert.ToDecimal(row["Balance"]),
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}
