using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public class ByProductSalesRepository : IByProductSalesRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public ByProductSalesRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<ByProductSales> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@IsActiveOnly", activeOnly)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_ByProductSales_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public ByProductSales? GetById(int id)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@Id", id)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_ByProductSales_GetById", parameters);

            if (dt.Rows.Count > 0)
            {
                return ConvertDataRowToModel(dt.Rows[0]);
            }

            return null;
        }

        public int Insert(ByProductSales model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@SaleDate", model.SaleDate),
                _dbHelper.CreateParameter("@ProductType", model.ProductType),
                _dbHelper.CreateParameter("@BuyerName", model.BuyerName),
                _dbHelper.CreateParameter("@BuyerContact", model.BuyerContact ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@Quantity", model.Quantity),
                _dbHelper.CreateParameter("@Rate", model.Rate),
                _dbHelper.CreateParameter("@TotalAmount", model.TotalAmount),
                _dbHelper.CreateParameter("@PaymentMode", model.PaymentMode),
                _dbHelper.CreateParameter("@PaymentStatus", model.PaymentStatus),
                _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                _dbHelper.CreateParameter("@CreatedBy", model.CreatedBy ?? "System"),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };

            _dbHelper.ExecuteWithOutput("sp_ByProductSales_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(ByProductSales model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@SaleDate", model.SaleDate),
                    _dbHelper.CreateParameter("@ProductType", model.ProductType),
                    _dbHelper.CreateParameter("@BuyerName", model.BuyerName),
                    _dbHelper.CreateParameter("@BuyerContact", model.BuyerContact ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@Quantity", model.Quantity),
                    _dbHelper.CreateParameter("@Rate", model.Rate),
                    _dbHelper.CreateParameter("@TotalAmount", model.TotalAmount),
                    _dbHelper.CreateParameter("@PaymentMode", model.PaymentMode),
                    _dbHelper.CreateParameter("@PaymentStatus", model.PaymentStatus),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks ?? (object)DBNull.Value),
                    _dbHelper.CreateParameter("@ModifiedBy", model.ModifiedBy ?? "System")
                };

                _dbHelper.ExecuteNonQuery("sp_ByProductSales_Update", parameters);
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

                _dbHelper.ExecuteNonQuery("sp_ByProductSales_Delete", parameters);
                return true;
            }
            catch
            {
                return false;
            }
        }

        public List<ByProductSales> GetByProductType(string productType)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@ProductType", productType)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_ByProductSales_GetByProductType", parameters);
            return ConvertDataTableToList(dt);
        }

        public List<ByProductSales> GetByDateRange(DateTime startDate, DateTime endDate)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@StartDate", startDate),
                _dbHelper.CreateParameter("@EndDate", endDate)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_ByProductSales_GetByDateRange", parameters);
            return ConvertDataTableToList(dt);
        }

        public List<ByProductSales> GetPendingPayments()
        {
            DataTable dt = _dbHelper.ExecuteDataTable("sp_ByProductSales_GetPendingPayments");
            return ConvertDataTableToList(dt);
        }

        public decimal GetTotalSalesByProduct(string productType, DateTime startDate, DateTime endDate)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@ProductType", productType),
                _dbHelper.CreateParameter("@StartDate", startDate),
                _dbHelper.CreateParameter("@EndDate", endDate)
            };

            return _dbHelper.ExecuteScalar<decimal>("sp_ByProductSales_GetTotalByProduct", parameters);
        }

        public string GenerateTransactionNumber()
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateOutputParameter("@TransactionNumber", SqlDbType.NVarChar)
            };
            parameters[0].Size = 50;

            _dbHelper.ExecuteWithOutput("sp_ByProductSales_GenerateTransactionNumber", parameters);
            return parameters[0].Value?.ToString() ?? string.Empty;
        }

        private List<ByProductSales> ConvertDataTableToList(DataTable dt)
        {
            List<ByProductSales> list = new List<ByProductSales>();

            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }

            return list;
        }

        private ByProductSales ConvertDataRowToModel(DataRow row)
        {
            return new ByProductSales
            {
                Id = Convert.ToInt32(row["Id"]),
                SaleDate = Convert.ToDateTime(row["SaleDate"]),
                TransactionNumber = row.Table.Columns.Contains("InvoiceNumber") && row["InvoiceNumber"] != DBNull.Value ? row["InvoiceNumber"].ToString() : null,
                ProductType = row["ProductType"].ToString() ?? string.Empty,
                BuyerName = row["BuyerName"].ToString() ?? string.Empty,
                BuyerContact = row.Table.Columns.Contains("BuyerAddress") && row["BuyerAddress"] != DBNull.Value ? row["BuyerAddress"].ToString() : null,
                Quantity = Convert.ToDecimal(row["Quantity"]),
                Rate = row.Table.Columns.Contains("UnitPrice") ? Convert.ToDecimal(row["UnitPrice"]) : 0,
                TotalAmount = Convert.ToDecimal(row["TotalAmount"]),
                PaymentMode = row["PaymentMode"] != DBNull.Value ? row["PaymentMode"].ToString() : null,
                PaymentStatus = row["PaymentStatus"] != DBNull.Value ? row["PaymentStatus"].ToString() : "Pending",
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                CreatedBy = row.Table.Columns.Contains("CreatedBy") && row["CreatedBy"] != DBNull.Value ? row["CreatedBy"].ToString() : null,
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                ModifiedBy = row.Table.Columns.Contains("ModifiedBy") && row["ModifiedBy"] != DBNull.Value ? row["ModifiedBy"].ToString() : null,
                ModifiedDate = row.Table.Columns.Contains("ModifiedDate") && row["ModifiedDate"] != DBNull.Value ? Convert.ToDateTime(row["ModifiedDate"]) : null,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}