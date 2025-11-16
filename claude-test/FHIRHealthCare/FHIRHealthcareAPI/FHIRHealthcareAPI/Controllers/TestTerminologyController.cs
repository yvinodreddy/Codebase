using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using FHIRHealthcareAPI.Services.Terminology;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace FHIRHealthcareAPI.Controllers
{
    [ApiController]
    [Route("api/test/terminology")]
    [AllowAnonymous]
    public class TestTerminologyController : ControllerBase
    {
        private readonly SimplifiedRxNormService _rxNormService;
        private readonly LoincService _loincService;

        public TestTerminologyController(
            SimplifiedRxNormService rxNormService,
            LoincService loincService)
        {
            _rxNormService = rxNormService;
            _loincService = loincService;
        }

        [HttpGet("drug/{rxcui}")]
        public async Task<IActionResult> GetDrugInfo(string rxcui)
        {
            try
            {
                var drug = await _rxNormService.GetDrugInfo(rxcui);

                if (!drug.IsValid)
                    return NotFound($"Drug with RxCUI {rxcui} not found");

                return Ok(drug);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }

        [HttpPost("interactions")]
        public async Task<IActionResult> CheckInteractions([FromBody] InteractionRequest request)
        {
            try
            {
                var interactions = await _rxNormService.GetInteractions(request.RxCuis);

                return Ok(new
                {
                    drugCount = request.RxCuis.Count,
                    interactionCount = interactions.Count,
                    hasCriticalInteractions = interactions.Exists(i =>
                        i.Severity?.ToLower() == "high" || i.Severity?.ToLower() == "severe"),
                    interactions = interactions
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }

        [HttpGet("loinc/{code}")]
        public async Task<IActionResult> ValidateLoincCode(string code)
        {
            try
            {
                var labTest = await _loincService.GetLabTestByCode(code);

                if (!labTest.IsValid)
                    return NotFound($"LOINC code {code} not found");

                return Ok(labTest);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = ex.Message });
            }
        }
    }

    public class InteractionRequest
    {
        public List<string> RxCuis { get; set; } = new List<string>();
    }
}