// =====================================================
// ADDITIONAL REPOSITORY IMPLEMENTATIONS
// =====================================================

// RMMS.DataAccess/Repositories/RiceSalesRepository.cs
using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IRiceSalesRepository
    {
        List<RiceSales> GetAll(bool activeOnly = true);
        RiceSales? GetById(int id);
        int Insert(RiceSales model);
        bool Update(RiceSales model);
        bool Delete(int id, string deletedBy);
        List<RiceSales> SearchByCustomer(string customerName);
        List<RiceSales> GetPendingPayments();
        decimal GetTotalSalesAmount(DateTime startDate, DateTime endDate);
        string GenerateInvoiceNumber();
    }

    public class RiceSalesRepository : IRiceSalesRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public RiceSalesRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<RiceSales> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@IsActiveOnly", activeOnly)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_RiceSales_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public RiceSales? GetById(int id)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@Id", id)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_RiceSales_GetById", parameters);

            if (dt.Rows.Count > 0)
            {
                return ConvertDataRowToModel(dt.Rows[0]);
            }

            return null;
        }

        public int Insert(RiceSales model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@SaleDate", model.SaleDate),
                _dbHelper.CreateParameter("@InvoiceNumber", model.InvoiceNumber),
                _dbHelper.CreateParameter("@BuyerName", model.BuyerName),
                _dbHelper.CreateParameter("@BuyerAddress", model.BuyerAddress),
                _dbHelper.CreateParameter("@BuyerGSTIN", model.BuyerGSTIN),
                _dbHelper.CreateParameter("@RiceGrade", model.RiceGrade),
                _dbHelper.CreateParameter("@Quantity", model.Quantity),
                _dbHelper.CreateParameter("@UnitPrice", model.UnitPrice),
                _dbHelper.CreateParameter("@Discount", model.Discount),
                _dbHelper.CreateParameter("@CGSTAmount", model.CGSTAmount),
                _dbHelper.CreateParameter("@SGSTAmount", model.SGSTAmount),
                _dbHelper.CreateParameter("@IGSTAmount", model.IGSTAmount),
                _dbHelper.CreateParameter("@FreightCharges", model.FreightCharges),
                _dbHelper.CreateParameter("@OtherCharges", model.OtherCharges),
                _dbHelper.CreateParameter("@PaymentMode", model.PaymentMode),
                _dbHelper.CreateParameter("@DueDate", model.DueDate),
                _dbHelper.CreateParameter("@Remarks", model.Remarks),
                _dbHelper.CreateParameter("@CreatedBy", model.CreatedBy),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };

            _dbHelper.ExecuteWithOutput("sp_RiceSales_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(RiceSales model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@SaleDate", model.SaleDate),
                    _dbHelper.CreateParameter("@BuyerName", model.BuyerName),
                    _dbHelper.CreateParameter("@BuyerAddress", model.BuyerAddress),
                    _dbHelper.CreateParameter("@BuyerGSTIN", model.BuyerGSTIN),
                    _dbHelper.CreateParameter("@RiceGrade", model.RiceGrade),
                    _dbHelper.CreateParameter("@Quantity", model.Quantity),
                    _dbHelper.CreateParameter("@UnitPrice", model.UnitPrice),
                    _dbHelper.CreateParameter("@Discount", model.Discount),
                    _dbHelper.CreateParameter("@CGSTAmount", model.CGSTAmount),
                    _dbHelper.CreateParameter("@SGSTAmount", model.SGSTAmount),
                    _dbHelper.CreateParameter("@IGSTAmount", model.IGSTAmount),
                    _dbHelper.CreateParameter("@FreightCharges", model.FreightCharges),
                    _dbHelper.CreateParameter("@OtherCharges", model.OtherCharges),
                    _dbHelper.CreateParameter("@PaymentMode", model.PaymentMode),
                    _dbHelper.CreateParameter("@DueDate", model.DueDate),
                    _dbHelper.CreateParameter("@PaymentStatus", model.PaymentStatus),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks),
                    _dbHelper.CreateParameter("@ModifiedBy", model.ModifiedBy)
                };

                _dbHelper.ExecuteNonQuery("sp_RiceSales_Update", parameters);
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

                _dbHelper.ExecuteNonQuery("sp_RiceSales_Delete", parameters);
                return true;
            }
            catch
            {
                return false;
            }
        }

        public List<RiceSales> SearchByCustomer(string customerName)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@BuyerName", customerName)
            };

            DataTable dt = _dbHelper.ExecuteDataTable("sp_RiceSales_SearchByCustomer", parameters);
            return ConvertDataTableToList(dt);
        }

        public List<RiceSales> GetPendingPayments()
        {
            DataTable dt = _dbHelper.ExecuteDataTable("sp_RiceSales_GetPendingPayments");
            return ConvertDataTableToList(dt);
        }

        public decimal GetTotalSalesAmount(DateTime startDate, DateTime endDate)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@StartDate", startDate),
                _dbHelper.CreateParameter("@EndDate", endDate)
            };

            return _dbHelper.ExecuteScalar<decimal>("sp_RiceSales_GetTotalSales", parameters);
        }

        public string GenerateInvoiceNumber()
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateOutputParameter("@InvoiceNumber", SqlDbType.NVarChar)
            };
            parameters[0].Size = 50;

            _dbHelper.ExecuteWithOutput("sp_RiceSales_GenerateInvoiceNumber", parameters);
            return parameters[0].Value?.ToString() ?? string.Empty;
        }

        private List<RiceSales> ConvertDataTableToList(DataTable dt)
        {
            List<RiceSales> list = new List<RiceSales>();

            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }

            return list;
        }

        private RiceSales ConvertDataRowToModel(DataRow row)
        {
            return new RiceSales
            {
                Id = Convert.ToInt32(row["Id"]),
                SaleDate = Convert.ToDateTime(row["SaleDate"]),
                InvoiceNumber = row["InvoiceNumber"].ToString() ?? string.Empty,
                BuyerName = row["BuyerName"].ToString() ?? string.Empty,
                BuyerAddress = row["BuyerAddress"] != DBNull.Value ? row["BuyerAddress"].ToString() : null,
                BuyerGSTIN = row["BuyerGSTIN"] != DBNull.Value ? row["BuyerGSTIN"].ToString() : null,
                RiceGrade = row["RiceGrade"].ToString() ?? string.Empty,
                Quantity = Convert.ToDecimal(row["Quantity"]),
                UnitPrice = Convert.ToDecimal(row["UnitPrice"]),
                TotalInvoiceValue = Convert.ToDecimal(row["TotalInvoiceValue"]),
                Discount = Convert.ToDecimal(row["Discount"]),
                TaxableValue = Convert.ToDecimal(row["TaxableValue"]),
                CGSTAmount = Convert.ToDecimal(row["CGSTAmount"]),
                SGSTAmount = Convert.ToDecimal(row["SGSTAmount"]),
                IGSTAmount = Convert.ToDecimal(row["IGSTAmount"]),
                TotalTaxAmount = Convert.ToDecimal(row["TotalTaxAmount"]),
                FreightCharges = Convert.ToDecimal(row["FreightCharges"]),
                OtherCharges = Convert.ToDecimal(row["OtherCharges"]),
                GrossInvoiceAmount = Convert.ToDecimal(row["GrossInvoiceAmount"]),
                PaymentMode = row["PaymentMode"] != DBNull.Value ? row["PaymentMode"].ToString() : null,
                DueDate = row["DueDate"] != DBNull.Value ? Convert.ToDateTime(row["DueDate"]) : (DateTime?)null,
                PaymentStatus = row["PaymentStatus"].ToString() ?? string.Empty,
                Remarks = row["Remarks"] != DBNull.Value ? row["Remarks"].ToString() : null,
                CreatedDate = Convert.ToDateTime(row["CreatedDate"]),
                ModifiedDate = row["ModifiedDate"] != DBNull.Value ? Convert.ToDateTime(row["ModifiedDate"]) : (DateTime?)null,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}