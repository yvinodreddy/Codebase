using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IPayablesOverdueRepository
    {
        List<PayableOverdue> GetAll(bool activeOnly = true);
        PayableOverdue? GetById(int id);
        int Insert(PayableOverdue model);
        bool Update(PayableOverdue model);
        bool Delete(int id, string deletedBy);
    }

    public class PayablesOverdueRepository : IPayablesOverdueRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public PayablesOverdueRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<PayableOverdue> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_PayablesOverdue_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public PayableOverdue? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_PayablesOverdue_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(PayableOverdue model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@PurchaseDate", model.PurchaseDate),
                _dbHelper.CreateParameter("@InvoiceNumber", model.InvoiceNumber),
                _dbHelper.CreateParameter("@SupplierName", model.SupplierName),
                _dbHelper.CreateParameter("@ItemPurchased", model.ItemPurchased),
                _dbHelper.CreateParameter("@InvoiceAmount", model.InvoiceAmount),
                _dbHelper.CreateParameter("@AmountPaid", model.AmountPaid),
                _dbHelper.CreateParameter("@BalancePayable", model.BalancePayable),
                _dbHelper.CreateParameter("@DueDate", model.DueDate),
                _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_PayablesOverdue_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(PayableOverdue model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@PurchaseDate", model.PurchaseDate),
                    _dbHelper.CreateParameter("@InvoiceNumber", model.InvoiceNumber),
                    _dbHelper.CreateParameter("@SupplierName", model.SupplierName),
                    _dbHelper.CreateParameter("@ItemPurchased", model.ItemPurchased),
                    _dbHelper.CreateParameter("@InvoiceAmount", model.InvoiceAmount),
                    _dbHelper.CreateParameter("@AmountPaid", model.AmountPaid),
                    _dbHelper.CreateParameter("@BalancePayable", model.BalancePayable),
                    _dbHelper.CreateParameter("@DueDate", model.DueDate),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value)
                };
                _dbHelper.ExecuteNonQuery("sp_PayablesOverdue_Update", parameters);
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
                _dbHelper.ExecuteNonQuery("sp_PayablesOverdue_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<PayableOverdue> ConvertDataTableToList(DataTable dt)
        {
            List<PayableOverdue> list = new List<PayableOverdue>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private PayableOverdue ConvertDataRowToModel(DataRow row)
        {
            return new PayableOverdue
            {
                Id = Convert.ToInt32(row["Id"]),
                PurchaseDate = Convert.ToDateTime(row["PurchaseDate"]),
                InvoiceNumber = row["InvoiceNumber"]?.ToString(),
                SupplierName = row["SupplierName"]?.ToString(),
                ItemPurchased = row["ItemPurchased"]?.ToString(),
                InvoiceAmount = Convert.ToDecimal(row["InvoiceAmount"]),
                AmountPaid = Convert.ToDecimal(row["AmountPaid"]),
                BalancePayable = Convert.ToDecimal(row["BalancePayable"]),
                DueDate = Convert.ToDateTime(row["DueDate"]),
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}
