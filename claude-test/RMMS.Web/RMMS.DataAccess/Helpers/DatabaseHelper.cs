// RMMS.DataAccess/Helpers/DatabaseHelper.cs
using System;
using System.Data;
using Microsoft.Data.SqlClient;
using System.Configuration;
using Microsoft.Extensions.Configuration;

namespace RMMS.DataAccess.Helpers
{
    public class DatabaseHelper(string connectionString) // Fix for IDE0290: Use primary constructor  
    {
        private readonly string _connectionString = connectionString;

        // Execute a stored procedure that returns a DataTable
        public DataTable ExecuteDataTable(string procedureName, SqlParameter[]? parameters = null)
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                using (SqlCommand command = new SqlCommand(procedureName, connection))
                {
                    command.CommandType = CommandType.StoredProcedure;

                    if (parameters != null)
                    {
                        command.Parameters.AddRange(parameters);
                    }

                    SqlDataAdapter adapter = new SqlDataAdapter(command);
                    DataTable dataTable = new DataTable();
                    adapter.Fill(dataTable);

                    return dataTable;
                }
            }
        }

        // Execute a stored procedure that returns a single value
        public T? ExecuteScalar<T>(string procedureName, SqlParameter[]? parameters = null)
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                using (SqlCommand command = new SqlCommand(procedureName, connection))
                {
                    command.CommandType = CommandType.StoredProcedure;

                    if (parameters != null)
                    {
                        command.Parameters.AddRange(parameters);
                    }

                    connection.Open();
                    object result = command.ExecuteScalar();

                    if (result == null || result == DBNull.Value)
                        return default(T);

                    return (T)Convert.ChangeType(result, typeof(T));
                }
            }
        }

        // Execute a stored procedure that doesn't return data
        public int ExecuteNonQuery(string procedureName, SqlParameter[]? parameters = null)
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                using (SqlCommand command = new SqlCommand(procedureName, connection))
                {
                    command.CommandType = CommandType.StoredProcedure;

                    if (parameters != null)
                    {
                        command.Parameters.AddRange(parameters);
                    }

                    connection.Open();
                    return command.ExecuteNonQuery();
                }
            }
        }

        // Execute a stored procedure with output parameters  
        public void ExecuteWithOutput(string procedureName, SqlParameter[] parameters)
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                using (SqlCommand command = new SqlCommand(procedureName, connection))
                {
                    command.CommandType = CommandType.StoredProcedure;
                    command.Parameters.AddRange(parameters);

                    connection.Open();
                    command.ExecuteNonQuery();
                }
            }
        }

        // Create a SQL parameter
        public SqlParameter CreateParameter(string name, object? value)
        {
            return new SqlParameter(name, value ?? DBNull.Value);
        }

        // Create an output parameter  
        public SqlParameter CreateOutputParameter(string name, SqlDbType type)
        {
            return new SqlParameter
            {
                ParameterName = name,
                SqlDbType = type,
                Direction = ParameterDirection.Output
            };
        }
    }
}