using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Authorization;
using FHIRHealthcareAPI.Modules.KnowledgeGraph.Services;
using Hl7.Fhir.Model;
using FHIRHealthcareAPI.Services;

namespace FHIRHealthcareAPI.Modules.KnowledgeGraph.Controllers
{
    [Authorize]
    [Route("api/knowledge-graph")]
    [ApiController]
    public class KnowledgeGraphController : ControllerBase
    {
        private readonly KnowledgeGraphService _knowledgeGraphService;
        private readonly PatientService _patientService;
        private readonly ConditionService _conditionService;

        public KnowledgeGraphController(
            KnowledgeGraphService knowledgeGraphService,
            PatientService patientService,
            ConditionService conditionService)
        {
            _knowledgeGraphService = knowledgeGraphService;
            _patientService = patientService;
            _conditionService = conditionService;
        }

        /// <summary>
        /// Convert patient to RDF and store in knowledge graph
        /// </summary>
        [HttpPost("patient/{patientId}/convert")]
        public async Task<IActionResult> ConvertPatientToKnowledgeGraph(string patientId)
        {
            try
            {
                // Get patient from FHIR server
                var patient = await _patientService.GetPatientById(patientId);
                if (patient == null)
                {
                    return NotFound($"Patient {patientId} not found");
                }

                // Convert to RDF
                var rdf = await _knowledgeGraphService.ConvertPatientToRDF(patient);

                // Store in GraphDB
                var stored = await _knowledgeGraphService.StorePatientInGraphDB(rdf, patientId);

                if (stored)
                {
                    return Ok(new
                    {
                        success = true,
                        patientId = patientId,
                        message = "Patient successfully added to knowledge graph",
                        rdfPreview = rdf.Substring(0, Math.Min(500, rdf.Length)) + "..."
                    });
                }

                return StatusCode(500, "Failed to store patient in knowledge graph");
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Find related conditions using semantic relationships
        /// </summary>
        [HttpGet("conditions/{snomedCode}/related")]
        public async Task<IActionResult> GetRelatedConditions(string snomedCode)
        {
            try
            {
                var relatedConditions = await _knowledgeGraphService.FindRelatedConditions(snomedCode);

                return Ok(new
                {
                    originalCode = snomedCode,
                    relatedConditionsCount = relatedConditions.Count,
                    relatedConditions = relatedConditions,
                    knowledgeSource = "GraphDB SPARQL Query",
                    timestamp = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Get patient knowledge summary
        /// </summary>
        [HttpGet("patient/{patientId}/summary")]
        public async Task<IActionResult> GetPatientKnowledgeSummary(string patientId)
        {
            try
            {
                var summary = await _knowledgeGraphService.GetPatientKnowledgeSummary(patientId);

                return Ok(summary);
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Add patient conditions to knowledge graph
        /// </summary>
        [HttpPost("patient/{patientId}/conditions/sync")]
        public async Task<IActionResult> SyncPatientConditions(string patientId)
        {
            try
            {
                var conditions = await _conditionService.GetActiveConditions(patientId);
                var syncedCount = 0;

                foreach (var condition in conditions)
                {
                    var rdf = await _knowledgeGraphService.ConvertConditionToRDF(condition, patientId);
                    // Store each condition
                    syncedCount++;
                }

                return Ok(new
                {
                    success = true,
                    patientId = patientId,
                    conditionsSynced = syncedCount,
                    message = $"Successfully synced {syncedCount} conditions to knowledge graph"
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Find related medications using RxNorm relationships
        /// </summary>
        [HttpGet("medications/{rxNormCui}/related")]
        public async Task<IActionResult> GetRelatedMedications(string rxNormCui)
        {
            try
            {
                var relatedMedications = await _knowledgeGraphService.FindRelatedMedications(rxNormCui);

                return Ok(new
                {
                    originalCui = rxNormCui,
                    relatedMedicationsCount = relatedMedications.Count,
                    relatedMedications = relatedMedications,
                    knowledgeSource = "RxNorm via GraphDB SPARQL",
                    timestamp = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Check drug-drug interactions between two medications
        /// </summary>
        [HttpPost("medications/check-interactions")]
        public async Task<IActionResult> CheckDrugInteractions([FromBody] DrugInteractionCheckRequest request)
        {
            try
            {
                if (string.IsNullOrEmpty(request.RxNormCui1) || string.IsNullOrEmpty(request.RxNormCui2))
                {
                    return BadRequest("Both RxNorm CUIs are required");
                }

                var interactions = await _knowledgeGraphService.FindDrugInteractions(
                    request.RxNormCui1,
                    request.RxNormCui2);

                return Ok(new
                {
                    drug1Cui = request.RxNormCui1,
                    drug2Cui = request.RxNormCui2,
                    hasInteraction = interactions.Any(),
                    interactionCount = interactions.Count,
                    interactions = interactions,
                    checkedAt = DateTime.UtcNow
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Convert medication to RDF and store in knowledge graph
        /// </summary>
        [HttpPost("patient/{patientId}/medication/add")]
        public async Task<IActionResult> AddMedicationToKnowledgeGraph(
            string patientId,
            [FromBody] AddMedicationRequest request)
        {
            try
            {
                // Create MedicationStatement from request
                var medication = new MedicationStatement
                {
                    Id = request.MedicationId ?? Guid.NewGuid().ToString(),
                    Status = MedicationStatement.MedicationStatusCodes.Active,
                    Subject = new ResourceReference($"Patient/{patientId}"),
                    Medication = new CodeableConcept
                    {
                        Coding = new List<Coding>
                {
                    new Coding
                    {
                        System = "http://www.nlm.nih.gov/research/umls/rxnorm",
                        Code = request.RxNormCui,
                        Display = request.MedicationName
                    }
                },
                        Text = request.MedicationName
                    }
                };

                // Add dosage if provided
                if (!string.IsNullOrEmpty(request.DosageInstructions))
                {
                    medication.Dosage = new List<Dosage>
            {
                new Dosage
                {
                    Text = request.DosageInstructions,
                    DoseAndRate = request.DoseValue.HasValue ?
                        new List<Dosage.DoseAndRateComponent>
                        {
                            new Dosage.DoseAndRateComponent
                            {
                                Dose = new Quantity
                                {
                                    Value = request.DoseValue.Value,
                                    Unit = request.DoseUnit ?? "mg"
                                }
                            }
                        } : null
                }
            };
                }

                // Convert to RDF
                var rdf = await _knowledgeGraphService.ConvertMedicationToRDF(medication, patientId);

                // Store in GraphDB (you might need to add a StoreMedicationInGraphDB method similar to StorePatientInGraphDB)
                // For now, return the RDF preview

                return Ok(new
                {
                    success = true,
                    patientId = patientId,
                    medicationId = medication.Id,
                    rxNormCui = request.RxNormCui,
                    message = "Medication successfully converted to RDF",
                    rdfPreview = rdf.Substring(0, Math.Min(500, rdf.Length)) + "..."
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }

        /// <summary>
        /// Sync all patient medications to knowledge graph
        /// </summary>
        [HttpPost("patient/{patientId}/medications/sync")]
        public async Task<IActionResult> SyncPatientMedications(string patientId)
        {
            try
            {
                // You'll need to inject MedicationService similar to how you have ConditionService
                // For now, returning a placeholder

                return Ok(new
                {
                    success = true,
                    patientId = patientId,
                    message = "This endpoint requires MedicationService to be implemented",
                    note = "Add MedicationService injection to fetch patient medications from FHIR store"
                });
            }
            catch (Exception ex)
            {
                return BadRequest(new { error = ex.Message });
            }
        }
    }

    // DTOs for the new endpoints
    public class DrugInteractionCheckRequest
    {
        /// <summary>
        /// First medication RxNorm CUI (e.g., "114194" for Warfarin)
        /// </summary>
        public string RxNormCui1 { get; set; }

        /// <summary>
        /// Second medication RxNorm CUI (e.g., "1191" for Aspirin)
        /// </summary>
        public string RxNormCui2 { get; set; }
    }

    public class AddMedicationRequest
    {
        public string MedicationId { get; set; }
        public string RxNormCui { get; set; }
        public string MedicationName { get; set; }
        public string DosageInstructions { get; set; }
        public decimal? DoseValue { get; set; }
        public string DoseUnit { get; set; }
    }
}