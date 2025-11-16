using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IReceivablesOverdueRepository
    {
        List<ReceivableOverdue> GetAll(bool activeOnly = true);
        ReceivableOverdue? GetById(int id);
        int Insert(ReceivableOverdue model);
        bool Update(ReceivableOverdue model);
        bool Delete(int id, string deletedBy);
    }

    public class ReceivablesOverdueRepository : IReceivablesOverdueRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public ReceivablesOverdueRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<ReceivableOverdue> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_ReceivablesOverdue_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public ReceivableOverdue? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_ReceivablesOverdue_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(ReceivableOverdue model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@InvoiceDate", model.InvoiceDate),
                _dbHelper.CreateParameter("@InvoiceNumber", model.InvoiceNumber),
                _dbHelper.CreateParameter("@CustomerName", model.CustomerName),
                _dbHelper.CreateParameter("@ItemSupplied", model.ItemSupplied),
                _dbHelper.CreateParameter("@InvoiceAmount", model.InvoiceAmount),
                _dbHelper.CreateParameter("@AmountReceived", model.AmountReceived),
                _dbHelper.CreateParameter("@BalanceDue", model.BalanceDue),
                _dbHelper.CreateParameter("@DueDate", model.DueDate),
                _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_ReceivablesOverdue_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(ReceivableOverdue model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@InvoiceDate", model.InvoiceDate),
                    _dbHelper.CreateParameter("@InvoiceNumber", model.InvoiceNumber),
                    _dbHelper.CreateParameter("@CustomerName", model.CustomerName),
                    _dbHelper.CreateParameter("@ItemSupplied", model.ItemSupplied),
                    _dbHelper.CreateParameter("@InvoiceAmount", model.InvoiceAmount),
                    _dbHelper.CreateParameter("@AmountReceived", model.AmountReceived),
                    _dbHelper.CreateParameter("@BalanceDue", model.BalanceDue),
                    _dbHelper.CreateParameter("@DueDate", model.DueDate),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value)
                };
                _dbHelper.ExecuteNonQuery("sp_ReceivablesOverdue_Update", parameters);
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
                _dbHelper.ExecuteNonQuery("sp_ReceivablesOverdue_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<ReceivableOverdue> ConvertDataTableToList(DataTable dt)
        {
            List<ReceivableOverdue> list = new List<ReceivableOverdue>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private ReceivableOverdue ConvertDataRowToModel(DataRow row)
        {
            return new ReceivableOverdue
            {
                Id = Convert.ToInt32(row["Id"]),
                InvoiceDate = Convert.ToDateTime(row["InvoiceDate"]),
                InvoiceNumber = row["InvoiceNumber"]?.ToString(),
                CustomerName = row["CustomerName"]?.ToString(),
                ItemSupplied = row["ItemSupplied"]?.ToString(),
                InvoiceAmount = Convert.ToDecimal(row["InvoiceAmount"]),
                AmountReceived = Convert.ToDecimal(row["AmountReceived"]),
                BalanceDue = Convert.ToDecimal(row["BalanceDue"]),
                DueDate = Convert.ToDateTime(row["DueDate"]),
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}
