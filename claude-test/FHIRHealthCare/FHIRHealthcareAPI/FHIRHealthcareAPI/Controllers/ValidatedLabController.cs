using FHIRHealthcareAPI.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Threading.Tasks;
using Hl7.Fhir.Model;

namespace FHIRHealthcareAPI.Controllers
{
    [ApiController]
    [Route("api/validated-lab")]
    [AllowAnonymous]
    public class ValidatedLabController : ControllerBase
    {
        private readonly ObservationService _observationService;

        public ValidatedLabController(ObservationService observationService)
        {
            _observationService = observationService;
        }

        [HttpPost("record")]
        public async Task<IActionResult> RecordValidatedLab([FromBody] LabResultRequest request)
        {
            try
            {
                var observation = await _observationService.RecordValidatedLabResult(
                    request.PatientId,
                    request.LoincCode,
                    request.Value,
                    request.Unit,
                    request.Interpretation
                );

                return Ok(new
                {
                    success = true,
                    observationId = observation.Id,
                    message = "Lab result recorded with LOINC validation",
                    timestamp = DateTime.UtcNow
                });
            }
            catch (ArgumentException ex)
            {
                return BadRequest(new { error = ex.Message });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }
    }

    public class LabResultRequest
    {
        public string PatientId { get; set; }
        public string LoincCode { get; set; }
        public decimal Value { get; set; }
        public string Unit { get; set; }
        public string Interpretation { get; set; }
    }
}