using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using FHIRHealthcareAPI.Services.Clinical;
using Hl7.Fhir.Model;

namespace FHIRHealthcareAPI.Controllers
{
    [Authorize]
    [Route("api/care-plan")]
    [ApiController]
    public class CarePlanController : ControllerBase
    {
        private readonly CarePlanManagementService _carePlanService;

        public CarePlanController(CarePlanManagementService carePlanService)
        {
            _carePlanService = carePlanService;
        }

        /// <summary>
        /// Creates a diabetes care plan with evidence-based activities
        /// </summary>
        [Authorize(Roles = "Doctor,Admin")]
        [HttpPost("diabetes")]
        public async Task<IActionResult> CreateDiabetesCarePlan([FromBody] CreateDiabetesCarePlanRequest request)
        {
            try
            {
                var carePlan = await _carePlanService.CreateDiabetesCarePlan(
                    request.PatientId,
                    request.ConditionId,
                    request.PractitionerId);

                return Ok(new
                {
                    success = true,
                    carePlanId = carePlan.Id,
                    title = carePlan.Title,
                    totalActivities = carePlan.Activity?.Count ?? 0,
                    message = "Diabetes care plan created with evidence-based activities"
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Creates a hypertension care plan
        /// </summary>
        [Authorize(Roles = "Doctor,Admin")]
        [HttpPost("hypertension")]
        public async Task<IActionResult> CreateHypertensionCarePlan([FromBody] CreateHypertensionCarePlanRequest request)
        {
            try
            {
                var carePlan = await _carePlanService.CreateHypertensionCarePlan(
                    request.PatientId,
                    request.ConditionId,
                    request.PractitionerId,
                    request.CurrentSystolic,
                    request.CurrentDiastolic);

                return Ok(new
                {
                    success = true,
                    carePlanId = carePlan.Id,
                    title = carePlan.Title,
                    currentBP = $"{request.CurrentSystolic}/{request.CurrentDiastolic}",
                    message = "Hypertension care plan created"
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Updates activity status in care plan
        /// </summary>
        [Authorize(Roles = "Doctor,Nurse,Admin")]
        [HttpPut("{carePlanId}/activity/{activityIndex}")]
        public async Task<IActionResult> UpdateActivityStatus(
            string carePlanId,
            int activityIndex,
            [FromBody] UpdateActivityRequest request)
        {
            try
            {
                var carePlan = await _carePlanService.UpdateActivityStatus(
                    carePlanId,
                    activityIndex,
                    request.Status,
                    request.Notes);

                return Ok(new
                {
                    success = true,
                    carePlanId = carePlan.Id,
                    activityIndex = activityIndex,
                    newStatus = request.Status.ToString(),
                    message = "Activity status updated"
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Gets care plan progress report
        /// </summary>
        [HttpGet("{carePlanId}/progress")]
        public async Task<IActionResult> GetProgressReport(string carePlanId)
        {
            try
            {
                var report = await _carePlanService.GenerateProgressReport(carePlanId);
                return Ok(report);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
    }

    // Request models
    public class CreateDiabetesCarePlanRequest
    {
        public string PatientId { get; set; }
        public string ConditionId { get; set; }
        public string PractitionerId { get; set; }
    }

    public class CreateHypertensionCarePlanRequest
    {
        public string PatientId { get; set; }
        public string ConditionId { get; set; }
        public string PractitionerId { get; set; }
        public int CurrentSystolic { get; set; }
        public int CurrentDiastolic { get; set; }
    }

    public class UpdateActivityRequest
    {
        public CarePlan.CarePlanActivityStatus Status { get; set; }
        public string Notes { get; set; }
    }
}