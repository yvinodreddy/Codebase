namespace FHIRHealthcareAPI.Models
{
    /// <summary>
    /// Configuration for JWT token generation and validation
    /// </summary>
    public class JwtSettings
    {
        public string SecretKey { get; set; }  // Must be at least 32 characters
        public string Issuer { get; set; }  // Your API's identifier
        public string Audience { get; set; }  // Who can use these tokens
        public int ExpirationMinutes { get; set; }  // How long tokens remain valid
    }
}