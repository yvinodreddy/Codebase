using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using RestSharp;
using RestSharp.Authenticators;
using VDS.RDF;
using VDS.RDF.Parsing;
using VDS.RDF.Query;
using VDS.RDF.Writing;

namespace FHIRHealthcareAPI.Infrastructure.GraphDatabase
{
    public class GraphDBConnector
    {
        private readonly RestClient _client;
        private readonly string _repositoryUrl;
        private readonly ILogger<GraphDBConnector> _logger;

        public GraphDBConnector(IConfiguration configuration, ILogger<GraphDBConnector> logger)
        {
            _logger = logger;
            var graphDbUrl = configuration["GraphDB:Url"] ?? "http://localhost:7200";
            var repository = configuration["GraphDB:Repository"] ?? "healthcare";

            _repositoryUrl = $"{graphDbUrl}/repositories/{repository}";
            _client = new RestClient(_repositoryUrl);

            // Add authentication if needed
            var username = configuration["GraphDB:Username"];
            var password = configuration["GraphDB:Password"];
            if (!string.IsNullOrEmpty(username) && !string.IsNullOrEmpty(password))
            {
                var options = new RestClientOptions(_repositoryUrl)
                {
                    Authenticator = new HttpBasicAuthenticator(username, password)
                };
                _client = new RestClient(options);
            }
        }

        /// <summary>
        /// Execute SPARQL SELECT query
        /// </summary>
        public async Task<SparqlResultSet> ExecuteSelectQuery(string sparqlQuery)
        {
            try
            {
                var request = new RestRequest("", Method.Get);
                request.AddParameter("query", sparqlQuery);
                request.AddHeader("Accept", "application/sparql-results+json");

                var response = await _client.ExecuteAsync(request);

                if (response.IsSuccessful)
                {
                    var parser = new SparqlJsonParser();
                    var results = new SparqlResultSet();
                    using (var reader = new StringReader(response.Content))
                    {
                        parser.Load(results, reader);
                    }
                    return results;
                }

                throw new Exception($"Query failed: {response.StatusCode} - {response.Content}");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error executing SPARQL query");
                throw;
            }
        }

        /// <summary>
        /// Execute SPARQL UPDATE query
        /// </summary>
        public async Task<bool> ExecuteUpdateQuery(string sparqlUpdate)
        {
            try
            {
                var request = new RestRequest("statements", Method.Post);
                request.AddParameter("update", sparqlUpdate, ParameterType.RequestBody);
                request.AddHeader("Content-Type", "application/x-www-form-urlencoded");

                var response = await _client.ExecuteAsync(request);

                if (response.IsSuccessful)
                {
                    _logger.LogInformation("SPARQL update executed successfully");
                    return true;
                }

                _logger.LogError($"Update failed: {response.StatusCode} - {response.Content}");
                return false;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error executing SPARQL update");
                return false;
            }
        }

        /// <summary>
        /// Store RDF graph in GraphDB
        /// </summary>
        public async Task<bool> StoreGraph(IGraph graph, string graphUri = null)
        {
            try
            {
                var writer = new NTriplesWriter();
                var rdfData = VDS.RDF.Writing.StringWriter.Write(graph, writer);

                var sparqlUpdate = string.IsNullOrEmpty(graphUri)
                    ? $"INSERT DATA {{ {rdfData} }}"
                    : $"INSERT DATA {{ GRAPH <{graphUri}> {{ {rdfData} }} }}";

                return await ExecuteUpdateQuery(sparqlUpdate);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error storing graph");
                return false;
            }
        }

        /// <summary>
        /// Clear a named graph
        /// </summary>
        public async Task<bool> ClearGraph(string graphUri)
        {
            var sparqlUpdate = $"CLEAR GRAPH <{graphUri}>";
            return await ExecuteUpdateQuery(sparqlUpdate);
        }

        /// <summary>
        /// Check if GraphDB is accessible
        /// </summary>
        public async Task<bool> IsHealthy()
        {
            try
            {
                var request = new RestRequest("/health", Method.Get);
                var response = await _client.ExecuteAsync(request);
                return response.IsSuccessful;
            }
            catch
            {
                return false;
            }
        }
    }
}