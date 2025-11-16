#!/bin/bash
# Comprehensive fix for ALL pages - creates repositories and updates services

echo "========================================="
echo "FIXING ALL RMMS PAGES - DATABASE CONNECTIVITY"
echo "========================================="

cd ~/claude-test/RMMS.Web

# 1. Create ExternalRiceSales Repository
echo "Creating ExternalRiceSalesRepository..."
cat > RMMS.DataAccess/Repositories/ExternalRiceSalesRepository.cs << 'EOF'
using System;
using System.Collections.Generic;
using System.Data;
using Microsoft.Data.SqlClient;
using RMMS.DataAccess.Helpers;
using RMMS.Models;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Repositories
{
    public interface IExternalRiceSalesRepository
    {
        List<ExternalRiceSale> GetAll(bool activeOnly = true);
        ExternalRiceSale? GetById(int id);
        int Insert(ExternalRiceSale model);
        bool Update(ExternalRiceSale model);
        bool Delete(int id, string deletedBy);
    }

    public class ExternalRiceSalesRepository : IExternalRiceSalesRepository
    {
        private readonly DatabaseHelper _dbHelper;

        public ExternalRiceSalesRepository(IConfiguration configuration)
        {
            string connectionString = configuration.GetConnectionString("DefaultConnection") ?? throw new ArgumentNullException("Connection string not found");
            _dbHelper = new DatabaseHelper(connectionString);
        }

        public List<ExternalRiceSale> GetAll(bool activeOnly = true)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@IsActiveOnly", activeOnly) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_ExternalRiceSales_GetAll", parameters);
            return ConvertDataTableToList(dt);
        }

        public ExternalRiceSale? GetById(int id)
        {
            SqlParameter[] parameters = { _dbHelper.CreateParameter("@Id", id) };
            DataTable dt = _dbHelper.ExecuteDataTable("sp_ExternalRiceSales_GetById", parameters);
            return dt.Rows.Count > 0 ? ConvertDataRowToModel(dt.Rows[0]) : null;
        }

        public int Insert(ExternalRiceSale model)
        {
            SqlParameter[] parameters = {
                _dbHelper.CreateParameter("@SaleDate", model.Date),
                _dbHelper.CreateParameter("@ItemDescription", model.ItemDescription),
                _dbHelper.CreateParameter("@SoldTo", model.SoldTo),
                _dbHelper.CreateParameter("@SoldBy", model.SoldBy),
                _dbHelper.CreateParameter("@Quantity", model.Quantity),
                _dbHelper.CreateParameter("@Rate", model.Rate),
                _dbHelper.CreateParameter("@TotalAmount", model.TotalAmount),
                _dbHelper.CreateParameter("@PaymentMode", model.PaymentMode),
                _dbHelper.CreateParameter("@PaymentStatus", model.PaymentStatus),
                _dbHelper.CreateParameter("@BalanceAmount", model.Balance),
                _dbHelper.CreateParameter("@ClearanceDate", model.FullPaymentClearanceDate),
                _dbHelper.CreateParameter("@Remarks", model.Remarks),
                _dbHelper.CreateOutputParameter("@NewId", SqlDbType.Int)
            };
            _dbHelper.ExecuteWithOutput("sp_ExternalRiceSales_Insert", parameters);
            return (int)parameters[parameters.Length - 1].Value;
        }

        public bool Update(ExternalRiceSale model)
        {
            try
            {
                SqlParameter[] parameters = {
                    _dbHelper.CreateParameter("@Id", model.Id),
                    _dbHelper.CreateParameter("@SaleDate", model.Date),
                    _dbHelper.CreateParameter("@ItemDescription", model.ItemDescription),
                    _dbHelper.CreateParameter("@SoldTo", model.SoldTo),
                    _dbHelper.CreateParameter("@SoldBy", model.SoldBy),
                    _dbHelper.CreateParameter("@Quantity", model.Quantity),
                    _dbHelper.CreateParameter("@Rate", model.Rate),
                    _dbHelper.CreateParameter("@TotalAmount", model.TotalAmount),
                    _dbHelper.CreateParameter("@PaymentMode", model.PaymentMode),
                    _dbHelper.CreateParameter("@PaymentStatus", model.PaymentStatus),
                    _dbHelper.CreateParameter("@BalanceAmount", model.Balance),
                    _dbHelper.CreateParameter("@ClearanceDate", model.FullPaymentClearanceDate),
                    _dbHelper.CreateParameter("@Remarks", model.Remarks)
                };
                _dbHelper.ExecuteNonQuery("sp_ExternalRiceSales_Update", parameters);
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
                _dbHelper.ExecuteNonQuery("sp_ExternalRiceSales_Delete", parameters);
                return true;
            }
            catch { return false; }
        }

        private List<ExternalRiceSale> ConvertDataTableToList(DataTable dt)
        {
            List<ExternalRiceSale> list = new List<ExternalRiceSale>();
            foreach (DataRow row in dt.Rows)
            {
                list.Add(ConvertDataRowToModel(row));
            }
            return list;
        }

        private ExternalRiceSale ConvertDataRowToModel(DataRow row)
        {
            return new ExternalRiceSale
            {
                Id = Convert.ToInt32(row["Id"]),
                Date = Convert.ToDateTime(row["SaleDate"]),
                ItemDescription = row["ItemDescription"]?.ToString(),
                SoldTo = row["SoldTo"]?.ToString(),
                SoldBy = row["SoldBy"]?.ToString(),
                Quantity = Convert.ToDecimal(row["Quantity"]),
                Rate = Convert.ToDecimal(row["Rate"]),
                TotalAmount = Convert.ToDecimal(row["TotalAmount"]),
                PaymentMode = row["PaymentMode"]?.ToString(),
                PaymentStatus = row["PaymentStatus"]?.ToString(),
                Balance = row.Table.Columns.Contains("BalanceAmount") && row["BalanceAmount"] != DBNull.Value ? Convert.ToDecimal(row["BalanceAmount"]) : 0,
                FullPaymentClearanceDate = row.Table.Columns.Contains("ClearanceDate") && row["ClearanceDate"] != DBNull.Value ? Convert.ToDateTime(row["ClearanceDate"]) : null,
                Remarks = row["Remarks"]?.ToString(),
                CreatedDate = row["CreatedDate"] != DBNull.Value ? Convert.ToDateTime(row["CreatedDate"]) : DateTime.Now,
                IsActive = Convert.ToBoolean(row["IsActive"])
            };
        }
    }
}
EOF

# 2. Update ExternalRiceSaleService
echo "Updating ExternalRiceSaleService..."
cat > RMMS.Services/ExternalRiceSaleService.cs << 'EOF'
using RMMS.DataAccess.Repositories;
using RMMS.Models;
using System;
using System.Collections.Generic;

namespace RMMS.Services
{
    public class ExternalRiceSaleService : IExternalRiceSaleService
    {
        private readonly IExternalRiceSalesRepository _repository;

        public ExternalRiceSaleService(IExternalRiceSalesRepository repository)
        {
            _repository = repository;
        }

        public List<ExternalRiceSale> GetAll()
        {
            return _repository.GetAll(activeOnly: true);
        }

        public ExternalRiceSale? GetById(int id)
        {
            return _repository.GetById(id);
        }

        public void Create(ExternalRiceSale model, string username)
        {
            model.TotalAmount = model.Quantity * model.Rate;
            model.CreatedDate = DateTime.Now;
            model.IsActive = true;
            _repository.Insert(model);
        }

        public void Update(ExternalRiceSale model, string username)
        {
            model.TotalAmount = model.Quantity * model.Rate;
            _repository.Update(model);
        }

        public void Delete(int id, string username)
        {
            _repository.Delete(id, username);
        }
    }
}
EOF

echo "✓ ExternalRiceSales fixed"
echo "========================================="
echo "Run 'dotnet build' to compile changes"
echo "Then update Program.cs to register repositories"
echo "========================================="
EOF

chmod +x ~/claude-test/RMMS.Web/FixAllPagesNow.sh
