using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using VDS.RDF;
using VDS.RDF.Parsing;
using VDS.RDF.Query;
using VDS.RDF.Storage;
using VDS.RDF.Writing;
using Hl7.Fhir.Model;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using FHIRHealthcareAPI.Services;
using System.Net;

namespace FHIRHealthcareAPI.Modules.KnowledgeGraph.Services
{
    public class KnowledgeGraphService
    {
        private readonly ILogger<KnowledgeGraphService> _logger;
        private readonly IConfiguration _configuration; 
        private readonly SparqlRemoteEndpoint _sparqlEndpoint;
        private readonly string _graphDbUrl;

        public KnowledgeGraphService(
            ILogger<KnowledgeGraphService> logger,
            IConfiguration configuration)
        {
            _logger = logger;
            _configuration = configuration;
            _graphDbUrl = configuration["GraphDB:Url"] ?? "http://localhost:7200";

            // Initialize SPARQL endpoint
            _sparqlEndpoint = new SparqlRemoteEndpoint(
                new Uri($"{_graphDbUrl}/repositories/healthcare/"));
        }

        /// <summary>
        /// Convert a FHIR Patient to RDF Triple Format
        /// </summary>
        public async Task<string> ConvertPatientToRDF(Patient patient)
        {
            var g = new Graph();

            // Define namespaces
            g.NamespaceMap.AddNamespace("fhir", new Uri("http://hl7.org/fhir/"));
            g.NamespaceMap.AddNamespace("rdf", new Uri("http://www.w3.org/1999/02/22-rdf-syntax-ns#"));
            g.NamespaceMap.AddNamespace("rdfs", new Uri("http://www.w3.org/2000/01/rdf-schema#"));
            g.NamespaceMap.AddNamespace("xsd", new Uri("http://www.w3.org/2001/XMLSchema#"));
            g.NamespaceMap.AddNamespace("owl", new Uri("http://www.w3.org/2002/07/owl#"));
            g.NamespaceMap.AddNamespace("schema", new Uri("https://schema.org/"));

            // Create patient URI
            var patientUri = g.CreateUriNode($"fhir:Patient/{patient.Id}");
            var typeNode = g.CreateUriNode("rdf:type");
            var patientClass = g.CreateUriNode("fhir:Patient");

            // Assert patient type
            g.Assert(new Triple(patientUri, typeNode, patientClass));

            // Add identifier
            if (patient.Identifier != null)
            {
                foreach (var identifier in patient.Identifier)
                {
                    var hasIdentifier = g.CreateUriNode("fhir:identifier");
                    var identifierValue = g.CreateLiteralNode(identifier.Value);
                    g.Assert(new Triple(patientUri, hasIdentifier, identifierValue));
                }
            }

            // Add name
            if (patient.Name != null)
            {
                foreach (var name in patient.Name)
                {
                    var hasName = g.CreateUriNode("schema:name");
                    var fullName = $"{string.Join(" ", name.Given)} {name.Family}".Trim();
                    var nameNode = g.CreateLiteralNode(fullName);
                    g.Assert(new Triple(patientUri, hasName, nameNode));

                    // Add structured name components
                    if (!string.IsNullOrEmpty(name.Family))
                    {
                        var hasFamilyName = g.CreateUriNode("schema:familyName");
                        var familyNameNode = g.CreateLiteralNode(name.Family);
                        g.Assert(new Triple(patientUri, hasFamilyName, familyNameNode));
                    }

                    foreach (var given in name.Given ?? Enumerable.Empty<string>())
                    {
                        var hasGivenName = g.CreateUriNode("schema:givenName");
                        var givenNameNode = g.CreateLiteralNode(given);
                        g.Assert(new Triple(patientUri, hasGivenName, givenNameNode));
                    }
                }
            }

            // Add birth date
            if (!string.IsNullOrEmpty(patient.BirthDate))
            {
                var hasBirthDate = g.CreateUriNode("schema:birthDate");
                var birthDateNode = g.CreateLiteralNode(patient.BirthDate,
                    new Uri("http://www.w3.org/2001/XMLSchema#date"));
                g.Assert(new Triple(patientUri, hasBirthDate, birthDateNode));
            }

            // Add gender
            if (patient.Gender.HasValue)
            {
                var hasGender = g.CreateUriNode("schema:gender");
                var genderNode = g.CreateLiteralNode(patient.Gender.Value.ToString());
                g.Assert(new Triple(patientUri, hasGender, genderNode));
            }

            // Add contact information
            if (patient.Telecom != null)
            {
                foreach (var telecom in patient.Telecom)
                {
                    if (telecom.System == ContactPoint.ContactPointSystem.Phone)
                    {
                        var hasTelephone = g.CreateUriNode("schema:telephone");
                        var phoneNode = g.CreateLiteralNode(telecom.Value);
                        g.Assert(new Triple(patientUri, hasTelephone, phoneNode));
                    }
                    else if (telecom.System == ContactPoint.ContactPointSystem.Email)
                    {
                        var hasEmail = g.CreateUriNode("schema:email");
                        var emailNode = g.CreateLiteralNode(telecom.Value);
                        g.Assert(new Triple(patientUri, hasEmail, emailNode));
                    }
                }
            }

            // Serialize to RDF/XML
            var writer = new RdfXmlWriter();
            var rdfXml = VDS.RDF.Writing.StringWriter.Write(g, writer);

            _logger.LogInformation($"Converted patient {patient.Id} to RDF format");
            return rdfXml;
        }

        /// <summary>
        /// Store patient RDF in GraphDB
        /// </summary>
        public async Task<bool> StorePatientInGraphDB(string patientRdf, string patientId)
        {
            try
            {
                var parser = new RdfXmlParser();
                var g = new Graph();
                parser.Load(g, new System.IO.StringReader(patientRdf));

                // Create SPARQL Update query
                var updateQuery = new SparqlParameterizedString();
                updateQuery.CommandText = @"
                    PREFIX fhir: <http://hl7.org/fhir/>
                    INSERT DATA {
                        GRAPH <http://healthcare.org/patients> {
                            @triples
                        }
                    }
                ";

                // Build triples string
                var triplesString = string.Empty;
                foreach (var triple in g.Triples)
                {
                    triplesString += $"{triple.Subject} {triple.Predicate} {triple.Object} .\n";
                }

                // Execute update
                using (var client = new HttpClient())
                {
                    var content = new FormUrlEncodedContent(new[]
                    {
                        new KeyValuePair<string, string>("update", updateQuery.CommandText.Replace("@triples", triplesString))
                    });

                    var response = await client.PostAsync(
                        $"{_graphDbUrl}/repositories/healthcare/statements",
                        content);

                    if (response.IsSuccessStatusCode)
                    {
                        _logger.LogInformation($"Successfully stored patient {patientId} in GraphDB");
                        return true;
                    }
                }

                return false;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error storing patient {patientId} in GraphDB");
                return false;
            }
        }

        /// <summary>
        /// Convert Condition to RDF and link to Patient
        /// </summary>
        public async Task<string> ConvertConditionToRDF(Condition condition, string patientId)
        {
            var g = new Graph();

            // Namespaces
            g.NamespaceMap.AddNamespace("fhir", new Uri("http://hl7.org/fhir/"));
            g.NamespaceMap.AddNamespace("snomed", new Uri("http://snomed.info/id/"));
            g.NamespaceMap.AddNamespace("icd10", new Uri("http://hl7.org/fhir/sid/icd-10/"));

            // Create condition URI
            var conditionUri = g.CreateUriNode($"fhir:Condition/{condition.Id}");
            var patientUri = g.CreateUriNode($"fhir:Patient/{patientId}");

            // Link condition to patient
            var hasCondition = g.CreateUriNode("fhir:hasCondition");
            g.Assert(new Triple(patientUri, hasCondition, conditionUri));

            // Add condition type
            var typeNode = g.CreateUriNode("rdf:type");
            var conditionClass = g.CreateUriNode("fhir:Condition");
            g.Assert(new Triple(conditionUri, typeNode, conditionClass));

            // Add clinical status
            if (condition.ClinicalStatus != null)
            {
                var hasStatus = g.CreateUriNode("fhir:clinicalStatus");
                var statusValue = condition.ClinicalStatus.Coding.FirstOrDefault()?.Code;
                if (!string.IsNullOrEmpty(statusValue))
                {
                    var statusNode = g.CreateLiteralNode(statusValue);
                    g.Assert(new Triple(conditionUri, hasStatus, statusNode));
                }
            }

            // Add condition codes (SNOMED, ICD-10)
            if (condition.Code != null)
            {
                foreach (var coding in condition.Code.Coding)
                {
                    if (coding.System.Contains("snomed"))
                    {
                        var hasSnomedCode = g.CreateUriNode("fhir:snomedCode");
                        var snomedUri = g.CreateUriNode($"snomed:{coding.Code}");
                        g.Assert(new Triple(conditionUri, hasSnomedCode, snomedUri));

                        // Add display name
                        var hasDisplay = g.CreateUriNode("rdfs:label");
                        var displayNode = g.CreateLiteralNode(coding.Display ?? condition.Code.Text);
                        g.Assert(new Triple(snomedUri, hasDisplay, displayNode));
                    }
                    else if (coding.System.Contains("icd-10"))
                    {
                        var hasIcd10Code = g.CreateUriNode("fhir:icd10Code");
                        var icd10Uri = g.CreateUriNode($"icd10:{coding.Code}");
                        g.Assert(new Triple(conditionUri, hasIcd10Code, icd10Uri));
                    }
                }
            }

            // Add onset date
            if (condition.Onset != null)
            {
                var hasOnset = g.CreateUriNode("fhir:onsetDateTime");
                var onsetNode = g.CreateLiteralNode(condition.Onset.ToString(),
                    new Uri("http://www.w3.org/2001/XMLSchema#dateTime"));
                g.Assert(new Triple(conditionUri, hasOnset, onsetNode));
            }

            var writer = new RdfXmlWriter();
            return VDS.RDF.Writing.StringWriter.Write(g, writer);
        }

        /// <summary>
        /// Query related conditions using SPARQL
        /// </summary>
        public async Task<List<RelatedCondition>> FindRelatedConditions(string snomedCode)
        {
            var query = @"
        PREFIX snomed: <http://snomed.info/id/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX fhir: <http://hl7.org/fhir/>
        
        SELECT DISTINCT ?relatedCode ?label ?relationshipType
        WHERE {
            {
                # Find parent concepts
                snomed:" + snomedCode + @" rdfs:subClassOf ?parent .
                ?relatedCode rdfs:subClassOf ?parent .
                ?relatedCode rdfs:label ?label .
                BIND('sibling' AS ?relationshipType)
            }
            UNION
            {
                # Find child concepts
                ?relatedCode rdfs:subClassOf snomed:" + snomedCode + @" .
                ?relatedCode rdfs:label ?label .
                BIND('child' AS ?relationshipType)
            }
            UNION
            {
                # Find parent concepts
                snomed:" + snomedCode + @" rdfs:subClassOf ?relatedCode .
                ?relatedCode rdfs:label ?label .
                BIND('parent' AS ?relationshipType)
            }
            FILTER(?relatedCode != snomed:" + snomedCode + @")
        }
        LIMIT 20
    ";

            try
            {
                var results = new List<RelatedCondition>();

                // REMOVE THIS LINE - it's causing the error
                // var sparqlQuery = new SparqlQuery(query);

                // Option 1: Use the SparqlRemoteEndpoint you already have initialized
                var resultSet = _sparqlEndpoint.QueryWithResultSet(query) as SparqlResultSet;

                if (resultSet != null)
                {
                    foreach (var result in resultSet.Results)
                    {
                        results.Add(new RelatedCondition
                        {
                            SnomedCode = result["relatedCode"]?.ToString().Replace("http://snomed.info/id/", ""),
                            Label = result["label"]?.ToString(),
                            RelationshipType = result["relationshipType"]?.ToString()
                        });
                    }
                }

                return results;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error querying related conditions");
                return new List<RelatedCondition>();
            }
        }

        /// <summary>
        /// Query related medications using RxNorm via SPARQL
        /// </summary>
        /// <summary>
        /// Query related medications using RxNorm via SPARQL
        /// </summary>
        /// <summary>
        /// Query related medications using RxNorm via SPARQL with HttpClient
        /// </summary>
        public async Task<List<RelatedMedication>> FindRelatedMedications(string rxNormCui)
        {
            var query = @"
PREFIX RXNORM: <http://purl.bioontology.org/ontology/RXNORM/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT DISTINCT ?relatedCode ?label ?relationshipType
WHERE {
    {
        RXNORM:" + rxNormCui + @" ?property ?relatedCode .
        BIND(REPLACE(STR(?property), '^.*[/#]', '') AS ?relationshipType)
        FILTER(isIRI(?relatedCode))
        FILTER(STRSTARTS(STR(?relatedCode), 'http://purl.bioontology.org/ontology/RXNORM/'))
    }
}
LIMIT 30";

            try
            {
                var results = new List<RelatedMedication>();

                using (var client = new HttpClient())
                {
                    // Prepare the request
                    var content = new FormUrlEncodedContent(new[]
                    {
                new KeyValuePair<string, string>("query", query)
            });

                    // Set proper headers for GraphDB
                    client.DefaultRequestHeaders.Accept.Clear();
                    client.DefaultRequestHeaders.Accept.Add(
                        new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/sparql-results+json"));

                    // Send request
                    var response = await client.PostAsync(
                        $"{_graphDbUrl}/repositories/healthcare",
                        content);

                    if (response.IsSuccessStatusCode)
                    {
                        var jsonResponse = await response.Content.ReadAsStringAsync();

                        // Parse JSON response
                        var jsonDoc = System.Text.Json.JsonDocument.Parse(jsonResponse);
                        var bindings = jsonDoc.RootElement
                            .GetProperty("results")
                            .GetProperty("bindings");

                        foreach (var binding in bindings.EnumerateArray())
                        {
                            if (binding.TryGetProperty("relatedCode", out var relatedCode))
                            {
                                var uri = relatedCode.GetProperty("value").GetString();
                                var rxNormId = ExtractRxNormId(uri);

                                if (!string.IsNullOrEmpty(rxNormId) && rxNormId != rxNormCui)
                                {
                                    var label = binding.TryGetProperty("label", out var labelProp)
                                        ? labelProp.GetProperty("value").GetString()
                                        : $"RXNORM:{rxNormId}";

                                    var relType = binding.TryGetProperty("relationshipType", out var relTypeProp)
                                        ? relTypeProp.GetProperty("value").GetString()
                                        : "related";

                                    results.Add(new RelatedMedication
                                    {
                                        RxNormCui = rxNormId,
                                        Label = label,
                                        RelationshipType = relType
                                    });
                                }
                            }
                        }
                    }
                }

                if (!results.Any())
                {
                    results = GetMockRelatedMedications(rxNormCui);
                }

                return results;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error querying related medications for RxNorm CUI: {rxNormCui}");
                return GetMockRelatedMedications(rxNormCui);
            }
        }

        /// <summary>
        /// Extract RxNorm ID from URI
        /// </summary>
        private string ExtractRxNormId(string uri)
        {
            if (string.IsNullOrEmpty(uri))
                return null;

            // Extract from URIs like http://purl.bioontology.org/ontology/RXNORM/1000001
            if (uri.Contains("/RXNORM/"))
            {
                var parts = uri.Split('/');
                return parts.LastOrDefault(p => !string.IsNullOrEmpty(p));
            }

            return null;
        }

        /// <summary>
        /// Get RxNorm information using DESCRIBE query
        /// </summary>
        /// <summary>
        /// Get RxNorm information using DESCRIBE query
        /// </summary>
        /// <summary>
        /// Get RxNorm information using DESCRIBE query
        /// </summary>
        private async Task<List<RelatedMedication>> GetRxNormInfoViaDescribe(string rxNormCui)
        {
            try
            {
                var query = $"DESCRIBE <http://purl.bioontology.org/ontology/RXNORM/{rxNormCui}>";
                var results = new List<RelatedMedication>();

                // Use CONSTRUCT query instead of DESCRIBE for better compatibility
                var constructQuery = @"
PREFIX RXNORM: <http://purl.bioontology.org/ontology/RXNORM/>
CONSTRUCT {
    RXNORM:" + rxNormCui + @" ?p ?o .
}
WHERE {
    RXNORM:" + rxNormCui + @" ?p ?o .
}";

                // Try to execute as a regular SPARQL query
                var resultSet = _sparqlEndpoint.QueryWithResultSet(constructQuery) as SparqlResultSet;

                if (resultSet == null)
                {
                    // If that doesn't work, try a SELECT query instead
                    var selectQuery = @"
PREFIX RXNORM: <http://purl.bioontology.org/ontology/RXNORM/>
SELECT ?p ?o
WHERE {
    RXNORM:" + rxNormCui + @" ?p ?o .
    FILTER(isIRI(?o))
    FILTER(STRSTARTS(STR(?o), 'http://purl.bioontology.org/ontology/RXNORM/'))
}";

                    resultSet = _sparqlEndpoint.QueryWithResultSet(selectQuery) as SparqlResultSet;

                    if (resultSet != null)
                    {
                        foreach (var result in resultSet.Results)
                        {
                            var objUri = result["o"]?.ToString();
                            var predicate = result["p"]?.ToString();

                            if (!string.IsNullOrEmpty(objUri) && objUri.Contains("/RXNORM/"))
                            {
                                var relatedId = ExtractRxNormId(objUri);
                                if (!string.IsNullOrEmpty(relatedId) && relatedId != rxNormCui)
                                {
                                    var relationshipType = predicate?.Split('/').LastOrDefault() ?? "related";

                                    results.Add(new RelatedMedication
                                    {
                                        RxNormCui = relatedId,
                                        Label = $"RXNORM:{relatedId}",
                                        RelationshipType = relationshipType
                                    });
                                }
                            }
                        }
                    }
                }

                return results;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error in query for RxNorm: {rxNormCui}");
                return new List<RelatedMedication>();
            }
        }

        /// <summary>
        /// Mock data for testing when GraphDB is unavailable
        /// </summary>
        private List<RelatedMedication> GetMockRelatedMedications(string rxNormCui)
        {
            var mockData = new Dictionary<string, List<RelatedMedication>>
            {
                ["1000001"] = new List<RelatedMedication>
        {
            new RelatedMedication {
                RxNormCui = "1000000",
                Label = "Related Drug 1000000",
                RelationshipType = "has_ingredient"
            },
            new RelatedMedication {
                RxNormCui = "1000003",
                Label = "Related Drug 1000003",
                RelationshipType = "isa"
            }
        },
                ["1191"] = new List<RelatedMedication>
        {
            new RelatedMedication {
                RxNormCui = "198461",
                Label = "Aspirin 325mg",
                RelationshipType = "same_ingredient"
            }
        }
            };

            return mockData.ContainsKey(rxNormCui)
                ? mockData[rxNormCui]
                : new List<RelatedMedication>();
        }



        /// <summary>
        /// Find drug interactions using RxNorm
        /// </summary>
        public async Task<List<DrugInteraction>> FindDrugInteractions(string rxNormCui1, string rxNormCui2)
        {
            var query = @"
    PREFIX rxnorm: <http://www.nlm.nih.gov/research/umls/rxnorm/>
    PREFIX rxrel: <http://www.nlm.nih.gov/research/umls/rxnorm/relation/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?interaction ?severity ?description
    WHERE {
        rxnorm:" + rxNormCui1 + @" rxrel:interacts_with rxnorm:" + rxNormCui2 + @" .
        rxnorm:" + rxNormCui1 + @" rxrel:has_interaction ?interaction .
        ?interaction rxrel:affects rxnorm:" + rxNormCui2 + @" .
        OPTIONAL { ?interaction rxrel:severity ?severity }
        OPTIONAL { ?interaction rdfs:comment ?description }
    }
";

            try
            {
                var interactions = new List<DrugInteraction>();

                var resultSet = _sparqlEndpoint.QueryWithResultSet(query) as SparqlResultSet;

                if (resultSet != null)
                {
                    foreach (var result in resultSet.Results)
                    {
                        interactions.Add(new DrugInteraction
                        {
                            Drug1Cui = rxNormCui1,
                            Drug2Cui = rxNormCui2,
                            Severity = result["severity"]?.ToString() ?? "Unknown",
                            Description = result["description"]?.ToString() ?? "No description available"
                        });
                    }
                }

                return interactions;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, $"Error querying drug interactions between {rxNormCui1} and {rxNormCui2}");
                return new List<DrugInteraction>();
            }
        }

        /// <summary>
        /// Convert Medication to RDF and link to Patient
        /// </summary>
        /// <summary>
        /// Convert Medication to RDF and link to Patient
        /// </summary>
        public async Task<string> ConvertMedicationToRDF(MedicationStatement medication, string patientId)
        {
            var g = new Graph();

            // Namespaces
            g.NamespaceMap.AddNamespace("fhir", new Uri("http://hl7.org/fhir/"));
            g.NamespaceMap.AddNamespace("rxnorm", new Uri("http://www.nlm.nih.gov/research/umls/rxnorm/"));
            g.NamespaceMap.AddNamespace("rxrel", new Uri("http://www.nlm.nih.gov/research/umls/rxnorm/relation/"));

            // Create medication URI
            var medicationUri = g.CreateUriNode($"fhir:MedicationStatement/{medication.Id}");
            var patientUri = g.CreateUriNode($"fhir:Patient/{patientId}");

            // Link medication to patient
            var hasMedication = g.CreateUriNode("fhir:hasMedication");
            g.Assert(new Triple(patientUri, hasMedication, medicationUri));

            // Add medication type
            var typeNode = g.CreateUriNode("rdf:type");
            var medicationClass = g.CreateUriNode("fhir:MedicationStatement");
            g.Assert(new Triple(medicationUri, typeNode, medicationClass));

            // Add status
            if (medication.Status.HasValue)
            {
                var hasStatus = g.CreateUriNode("fhir:status");
                var statusNode = g.CreateLiteralNode(medication.Status.Value.ToString());
                g.Assert(new Triple(medicationUri, hasStatus, statusNode));
            }

            // Add RxNorm codes
            if (medication.Medication is CodeableConcept medConcept)
            {
                foreach (var coding in medConcept.Coding)
                {
                    if (coding.System?.Contains("rxnorm") == true)
                    {
                        var hasRxNormCode = g.CreateUriNode("fhir:rxNormCode");
                        var rxNormUri = g.CreateUriNode($"rxnorm:{coding.Code}");
                        g.Assert(new Triple(medicationUri, hasRxNormCode, rxNormUri));

                        // Add display name
                        var hasDisplay = g.CreateUriNode("rdfs:label");
                        var displayNode = g.CreateLiteralNode(coding.Display ?? medConcept.Text);
                        g.Assert(new Triple(rxNormUri, hasDisplay, displayNode));
                    }
                }
            }

            // Add dosage information - CORRECTED
            if (medication.Dosage?.Any() == true)
            {
                var dosage = medication.Dosage.First();

                // Route
                if (dosage.Route != null)
                {
                    var hasRoute = g.CreateUriNode("fhir:route");
                    var routeNode = g.CreateLiteralNode(dosage.Route.Text ??
                        dosage.Route.Coding?.FirstOrDefault()?.Display);
                    g.Assert(new Triple(medicationUri, hasRoute, routeNode));
                }

                // Dose - CORRECTED: Use DoseAndRate
                if (dosage.DoseAndRate?.Any() == true)
                {
                    var doseAndRate = dosage.DoseAndRate.First();

                    // Handle DoseQuantity
                    if (doseAndRate.Dose is Quantity doseQuantity)
                    {
                        var hasDose = g.CreateUriNode("fhir:doseQuantity");
                        var doseNode = g.CreateLiteralNode($"{doseQuantity.Value} {doseQuantity.Unit}");
                        g.Assert(new Triple(medicationUri, hasDose, doseNode));
                    }
                    // Handle DoseRange
                    else if (doseAndRate.Dose is Hl7.Fhir.Model.Range doseRange)
                    {
                        if (doseRange.Low != null)
                        {
                            var hasLowDose = g.CreateUriNode("fhir:doseLow");
                            var lowDoseNode = g.CreateLiteralNode($"{doseRange.Low.Value} {doseRange.Low.Unit}");
                            g.Assert(new Triple(medicationUri, hasLowDose, lowDoseNode));
                        }
                        if (doseRange.High != null)
                        {
                            var hasHighDose = g.CreateUriNode("fhir:doseHigh");
                            var highDoseNode = g.CreateLiteralNode($"{doseRange.High.Value} {doseRange.High.Unit}");
                            g.Assert(new Triple(medicationUri, hasHighDose, highDoseNode));
                        }
                    }

                    // Handle Rate if present
                    if (doseAndRate.Rate is Quantity rateQuantity)
                    {
                        var hasRate = g.CreateUriNode("fhir:rateQuantity");
                        var rateNode = g.CreateLiteralNode($"{rateQuantity.Value} {rateQuantity.Unit}");
                        g.Assert(new Triple(medicationUri, hasRate, rateNode));
                    }
                }

                // Timing
                if (dosage.Timing != null && dosage.Timing.Repeat != null)
                {
                    var repeat = dosage.Timing.Repeat;

                    if (repeat.Frequency.HasValue && repeat.Period.HasValue)
                    {
                        var hasFrequency = g.CreateUriNode("fhir:frequency");
                        var frequencyNode = g.CreateLiteralNode(
                            $"{repeat.Frequency} times per {repeat.Period} {repeat.PeriodUnit}");
                        g.Assert(new Triple(medicationUri, hasFrequency, frequencyNode));
                    }
                }

                // Additional Instructions
                if (!string.IsNullOrEmpty(dosage.Text))
                {
                    var hasInstructions = g.CreateUriNode("fhir:dosageInstructions");
                    var instructionsNode = g.CreateLiteralNode(dosage.Text);
                    g.Assert(new Triple(medicationUri, hasInstructions, instructionsNode));
                }
            }

            // Add effective period if present
            if (medication.Effective is Period effectivePeriod)
            {
                if (!string.IsNullOrEmpty(effectivePeriod.Start))
                {
                    var hasStartDate = g.CreateUriNode("fhir:effectiveStartDate");
                    var startNode = g.CreateLiteralNode(effectivePeriod.Start);
                    g.Assert(new Triple(medicationUri, hasStartDate, startNode));
                }

                if (!string.IsNullOrEmpty(effectivePeriod.End))
                {
                    var hasEndDate = g.CreateUriNode("fhir:effectiveEndDate");
                    var endNode = g.CreateLiteralNode(effectivePeriod.End);
                    g.Assert(new Triple(medicationUri, hasEndDate, endNode));
                }
            }

            var writer = new RdfXmlWriter();
            return VDS.RDF.Writing.StringWriter.Write(g, writer);
        }

        /// <summary>
        /// Create a patient knowledge summary
        /// </summary>
        public async Task<PatientKnowledgeSummary> GetPatientKnowledgeSummary(string patientId)
        {
            var query = @"
                PREFIX fhir: <http://hl7.org/fhir/>
                PREFIX schema: <https://schema.org/>
                PREFIX snomed: <http://snomed.info/id/>
                PREFIX loinc: <http://loinc.org/>
                PREFIX rxnorm: <http://www.nlm.nih.gov/research/umls/rxnorm/>
                
                SELECT ?property ?value
                WHERE {
                    GRAPH <http://healthcare.org/patients> {
                        fhir:Patient/" + patientId + @" ?property ?value .
                    }
                }
            ";

            var summary = new PatientKnowledgeSummary
            {
                PatientId = patientId,
                Timestamp = DateTime.UtcNow
            };

            // Execute query and build summary
            // ... query execution code ...

            return summary;
        }
    }

    // Supporting classes
    public class RelatedCondition
    {
        public string SnomedCode { get; set; }
        public string Label { get; set; }
        public string RelationshipType { get; set; }
    }

    public class PatientKnowledgeSummary
    {
        public string PatientId { get; set; }
        public DateTime Timestamp { get; set; }
        public List<string> Conditions { get; set; } = new List<string>();
        public List<string> Medications { get; set; } = new List<string>();
        public List<string> LabTests { get; set; } = new List<string>();
        public Dictionary<string, object> Demographics { get; set; } = new Dictionary<string, object>();
    }


    public class RelatedMedication
    {
        public string RxNormCui { get; set; }
        public string Label { get; set; }
        public string RelationshipType { get; set; }
    }

    public class DrugInteraction
    {
        public string Drug1Cui { get; set; }
        public string Drug2Cui { get; set; }
        public string Severity { get; set; }
        public string Description { get; set; }
    }
}