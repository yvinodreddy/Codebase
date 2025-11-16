using FHIRHealthcareAPI.Services;
using Microsoft.Extensions.Hosting;
using System;
using System.Threading;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Infrastructure
{
    /// <summary>
    /// Background service that automatically seeds data when the application starts
    /// </summary>
    public class DataSeedingHostedService : IHostedService
    {
        private readonly DataSeedingService _seedingService;

        public DataSeedingHostedService()
        {
            _seedingService = new DataSeedingService();
        }

        public async Task StartAsync(CancellationToken cancellationToken)
        {
            Console.WriteLine("\n🌱 Starting automatic data seeding...\n");

            try
            {
                // Add a small delay to ensure FHIR server is fully ready
                await Task.Delay(2000, cancellationToken);

                var result = await _seedingService.SeedAllData();

                if (result.Success)
                {
                    Console.WriteLine("\n✅ AUTOMATIC DATA SEEDING SUCCESSFUL");
                    Console.WriteLine("===================================");
                    Console.WriteLine($"API is ready at https://localhost:7012");
                    Console.WriteLine($"Swagger UI: https://localhost:7012/swagger");
                    Console.WriteLine($"Total Resources Created: {result.PatientsCreated + result.ObservationsCreated + result.ConditionsCreated + result.MedicationsCreated + result.CarePlansCreated}");
                }
                else
                {
                    Console.WriteLine($"\n⚠️ Data seeding encountered an issue: {result.ErrorMessage}");
                    Console.WriteLine("You can manually seed data using: GET /api/DataSeeding/seed");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n⚠️ Automatic seeding skipped: {ex.Message}");
                Console.WriteLine("You can manually seed data using: GET /api/DataSeeding/seed");
            }
        }

        public Task StopAsync(CancellationToken cancellationToken)
        {
            return Task.CompletedTask;
        }
    }
}
