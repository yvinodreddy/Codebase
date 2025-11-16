using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using FHIRHealthcareAPI.Services.Terminology;

namespace FHIRHealthcareAPI.Controllers
{
    [ApiController]
    [Route("api/snomed-test")]
    [AllowAnonymous] // For testing
    public class SnomedTestController : ControllerBase
    {
        private readonly SnomedService _snomedService;

        public SnomedTestController(SnomedService snomedService)
        {
            _snomedService = snomedService;
        }

        /// <summary>
        /// Test SNOMED code validation
        /// Try: 44054006 (Type 2 diabetes), 38341003 (Hypertension), 195967001 (Asthma)
        /// </summary>
        [HttpGet("validate/{snomedCode}")]
        public async Task<IActionResult> ValidateSnomedCode(string snomedCode)
        {
            try
            {
                var concept = await _snomedService.ValidateConditionCode(snomedCode);

                return Ok(new
                {
                    success = concept.IsValid,
                    snomedCode = snomedCode,
                    preferredTerm = concept.PreferredTerm,
                    isValid = concept.IsValid,
                    source = "Snowstorm SNOMED Server",
                    timestamp = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new
                {
                    success = false,
                    error = ex.Message,
                    snomedCode = snomedCode
                });
            }
        }

        /// <summary>
        /// Test multiple common condition codes
        /// </summary>
        [HttpGet("test-common")]
        public async Task<IActionResult> TestCommonConditions()
        {
            var commonCodes = new[]
            {
                "44054006",  // Type 2 diabetes mellitus
                "38341003",  // Essential hypertension  
                "195967001", // Asthma
                "73211009",  // Diabetes mellitus
                "22298006",  // Myocardial infarction
                "53741008"   // Coronary artery disease
            };

            var results = new List<object>();

            foreach (var code in commonCodes)
            {
                try
                {
                    var concept = await _snomedService.ValidateConditionCode(code);
                    results.Add(new
                    {
                        code = code,
                        preferredTerm = concept.PreferredTerm,
                        isValid = concept.IsValid
                    });
                }
                catch (Exception ex)
                {
                    results.Add(new
                    {
                        code = code,
                        error = ex.Message,
                        isValid = false
                    });
                }
            }

            return Ok(new
            {
                success = true,
                message = "Common SNOMED condition codes test",
                results = results,
                timestamp = DateTime.UtcNow
            });
        }
    }
}