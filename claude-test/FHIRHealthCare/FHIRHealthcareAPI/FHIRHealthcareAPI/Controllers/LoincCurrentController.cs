using FHIRHealthcareAPI.Services.Terminology;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/loinc-current")]
[AllowAnonymous]
public class LoincCurrentController : ControllerBase
{
    private readonly LoincService _loincService;

    public LoincCurrentController(LoincService loincService)
    {
        _loincService = loincService;
    }

    /// <summary>
    /// Test your existing LOINC service
    /// Try: 33747-0 (Glucose), 2085-9 (Cholesterol), 718-7 (Hemoglobin)
    /// </summary>
    [HttpGet("{loincCode}")]
    public async Task<IActionResult> TestCurrentService(string loincCode)
    {
        var result = await _loincService.GetLabTestByCode(loincCode);

        return Ok(new
        {
            success = result.IsValid,
            source = "CSIRO Ontoserver via FHIR",
            loincTest = result,
            timestamp = DateTime.UtcNow
        });
    }
}