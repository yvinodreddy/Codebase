using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using FHIRHealthcareAPI.Services.Terminology;

namespace FHIRHealthcareAPI.Controllers
{
    [ApiController]
    [Route("api/loinc-test")]
    [AllowAnonymous] // For testing
    public class LoincTestController : ControllerBase
    {
        private readonly LoincService _loincService;

        public LoincTestController(LoincService loincService)
        {
            _loincService = loincService;
        }

        /// <summary>
        /// Test LOINC code validation via CSIRO Ontoserver
        /// </summary>
        [HttpGet("validate/{loincCode}")]
        public async Task<IActionResult> ValidateLoincCode(string loincCode)
        {
            try
            {
                var isValid = await _loincService.ValidateLoincCode(loincCode);

                return Ok(new
                {
                    success = true,
                    loincCode = loincCode,
                    isValid = isValid,
                    source = "CSIRO Ontoserver FHIR",
                    timestamp = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new
                {
                    success = false,
                    error = ex.Message,
                    loincCode = loincCode
                });
            }
        }

        /// <summary>
        /// Get detailed lab test information
        /// </summary>
        [HttpGet("details/{loincCode}")]
        public async Task<IActionResult> GetLabTestDetails(string loincCode)
        {
            try
            {
                var labTest = await _loincService.GetLabTestByCode(loincCode);

                return Ok(new
                {
                    success = labTest.IsValid,
                    labTest = labTest,
                    source = "CSIRO Ontoserver FHIR",
                    timestamp = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new
                {
                    success = false,
                    error = ex.Message,
                    loincCode = loincCode
                });
            }
        }
        /// <summary>
        /// Detailed debugging for LOINC issues
        /// </summary>
        [HttpGet("debug/{loincCode}")]
        public async Task<IActionResult> DebugLoincCode(string loincCode)
        {
            try
            {
                var labTest = await _loincService.GetLabTestByCode(loincCode);

                return Ok(new
                {
                    success = true,
                    loincCode = loincCode,
                    result = new
                    {
                        code = labTest.Code,
                        display = labTest.Display,
                        isValid = labTest.IsValid
                    },
                    debugInfo = new
                    {
                        server = "https://r4.ontoserver.csiro.au/fhir",
                        operation = "CodeSystem/$lookup",
                        timestamp = DateTime.UtcNow
                    }
                });
            }
            catch (Exception ex)
            {
                return Ok(new  // Return 200 OK so we can see the error details
                {
                    success = false,
                    loincCode = loincCode,
                    error = ex.Message,
                    stackTrace = ex.StackTrace,
                    innerException = ex.InnerException?.Message,
                    timestamp = DateTime.UtcNow
                });
            }
        }
        /// <summary>
        /// Test multiple common lab codes
        /// </summary>
        [HttpGet("test-common")]
        public async Task<IActionResult> TestCommonLabCodes()
        {
            var commonCodes = new[]
            {
                "33747-0",  // Glucose [Mass/volume] in Blood
                "2085-9",   // Cholesterol [Mass/volume] in Serum or Plasma
                "718-7",    // Hemoglobin [Mass/volume] in Blood
                "6690-2",   // Leukocytes [#/volume] in Blood by Automated count
                "777-3",    // Platelets [#/volume] in Blood by Automated count
                "2160-0"    // Creatinine [Mass/volume] in Serum or Plasma
            };

            var results = new List<object>();

            foreach (var code in commonCodes)
            {
                try
                {
                    var labTest = await _loincService.GetLabTestByCode(code);
                    results.Add(new
                    {
                        code = code,
                        display = labTest.Display,
                        isValid = labTest.IsValid
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
                message = "Common lab codes test",
                results = results,
                timestamp = DateTime.UtcNow
            });
        }
    }
}