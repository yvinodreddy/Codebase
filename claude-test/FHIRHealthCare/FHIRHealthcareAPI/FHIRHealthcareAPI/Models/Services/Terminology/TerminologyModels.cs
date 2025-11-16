using System;
using System.Collections.Generic;

namespace FHIRHealthcareAPI.Models.Terminology
{
    // All terminology models in one place
    public class CodeValidationRequest
    {
        public string Code { get; set; }
        public string System { get; set; }
    }

    public class CodeValidationResult
    {
        public string Code { get; set; }
        public string System { get; set; }
        public bool IsValid { get; set; }
        public string Display { get; set; }
        public object Details { get; set; }
        public string Error { get; set; }
    }

    public class DrugInteractionRequest
    {
        public List<string> RxCuis { get; set; } = new List<string>();
        public string PatientId { get; set; }
    }

    public class UnifiedSearchResult
    {
        public List<SnomedConcept> SnomedConcepts { get; set; } = new List<SnomedConcept>();
        public List<RxNormConcept> RxNormConcepts { get; set; } = new List<RxNormConcept>();
        public List<LoincCode> LoincCodes { get; set; } = new List<LoincCode>();
    }

    public class ValidateSnomedRequest
    {
        public string ConceptId { get; set; }
        public bool IncludeRelationships { get; set; }
    }

    public class MedicationSearchRequest
    {
        public string SearchTerm { get; set; }
        public bool IncludeGenericEquivalents { get; set; }
        public bool CheckInteractions { get; set; }
    }

    public class CarePlanRequest
    {
        public string PatientId { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public List<string> ConditionIds { get; set; } = new List<string>();
        public List<CarePlanActivity> Activities { get; set; } = new List<CarePlanActivity>();
    }

    public class CarePlanActivity
    {
        public string Title { get; set; }
        public string SnomedCode { get; set; }
        public string Frequency { get; set; }
        public string Instructions { get; set; }
    }

    // RxNorm Response Models
    public class RxNormPropertiesResponse
    {
        public RxNormProperties Properties { get; set; }
    }

    public class RxNormProperties
    {
        public string Rxcui { get; set; }
        public string Name { get; set; }
        public string Synonym { get; set; }
        public string Tty { get; set; }
        public string Suppress { get; set; }
    }

    public class InteractionResponse
    {
        public List<InteractionTypeGroup> InteractionTypeGroup { get; set; }
    }

    public class InteractionTypeGroup
    {
        public string SourceName { get; set; }
        public List<InteractionType> InteractionType { get; set; }
    }

    public class InteractionType
    {
        public List<InteractionPair> InteractionPair { get; set; }
    }

    public class InteractionPair
    {
        public string Description { get; set; }
        public string Severity { get; set; }
        public List<InteractionConcept> InteractionConcept { get; set; }
    }

    public class InteractionConcept
    {
        public SourceConceptItem SourceConceptItem { get; set; }
    }

    public class SourceConceptItem
    {
        public string Name { get; set; }
    }

    public class DrugSearchResponse
    {
        public DrugGroup DrugGroup { get; set; }
    }

    public class DrugGroup
    {
        public List<ConceptGroup> ConceptGroup { get; set; }
    }

    public class ConceptGroup
    {
        public List<RxNormConcept> ConceptProperties { get; set; }
    }

    public class RelatedDrugsResponse
    {
        public RelatedGroup RelatedGroup { get; set; }
    }

    public class RelatedGroup
    {
        public List<ConceptGroup> ConceptGroup { get; set; }
    }

    // Additional concept models
    public class SnomedConcept
    {
        public string ConceptId { get; set; }
        public string Fsn { get; set; }
        public string Pt { get; set; }
        public bool Active { get; set; }
    }

    public class RxNormConcept
    {
        public string RxCui { get; set; }
        public string Name { get; set; }
        public string Tty { get; set; }
    }

    public class LoincCode
    {
        public string Code { get; set; }
        public string Display { get; set; }
        public string Component { get; set; }
        public string Property { get; set; }
        public string System { get; set; }
        public string Status { get; set; }
    }
}