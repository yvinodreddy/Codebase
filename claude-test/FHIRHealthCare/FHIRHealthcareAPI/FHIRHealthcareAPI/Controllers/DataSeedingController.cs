using FHIRHealthcareAPI.Services;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace FHIRHealthcareAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class DataSeedingController : ControllerBase
    {
        private readonly DataSeedingService _seedingService;

        public DataSeedingController()
        {
            _seedingService = new DataSeedingService();
        }

        /// <summary>
        /// Seeds comprehensive test data into the FHIR server
        /// GET /api/DataSeeding/seed
        /// </summary>
        [HttpGet("seed")]
        public async Task<IActionResult> SeedData()
        {
            var result = await _seedingService.SeedAllData();

            if (result.Success)
            {
                return Ok(new
                {
                    message = "Data seeding completed successfully",
                    details = new
                    {
                        patientsCreated = result.PatientsCreated,
                        observationsCreated = result.ObservationsCreated,
                        conditionsCreated = result.ConditionsCreated,
                        medicationsCreated = result.MedicationsCreated,
                        carePlansCreated = result.CarePlansCreated,
                        durationSeconds = result.Duration.TotalSeconds
                    }
                });
            }
            else
            {
                return StatusCode(500, new
                {
                    message = "Data seeding failed",
                    error = result.ErrorMessage
                });
            }
        }

        /// <summary>
        /// Health check for data seeding endpoint
        /// GET /api/DataSeeding/status
        /// </summary>
        [HttpGet("status")]
        public IActionResult GetStatus()
        {
            return Ok(new
            {
                service = "Data Seeding Service",
                status = "Ready",
                endpoint = "/api/DataSeeding/seed"
            });
        }
    }
}
