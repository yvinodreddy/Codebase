# Security Guidelines for ULTRATHINK

## HTTPS Enforcement

### API Communication
All communication with the Claude API uses HTTPS by default:
- Anthropic SDK enforces HTTPS
- No configuration needed
- TLS 1.2+ required

### Best Practices
1. **Never disable SSL verification** in production
2. **Use environment variables** for API keys (never hardcode)
3. **Rotate API keys** regularly (every 90 days recommended)
4. **Monitor API usage** for unexpected spikes

### Verification
```python
# The Anthropic SDK handles HTTPS automatically
import anthropic
client = anthropic.Anthropic(api_key=key)  # Always uses HTTPS
```

## Security Features Implemented

### Input Validation
- ✅ S2: Prompt injection detection (3 versions)
- ✅ S3: File path validation (prevents directory traversal)
- ✅ S1: API key masking in logs

### Rate Limiting
- ✅ S4: 500 calls per 6 minutes (~83/min)
- Prevents cost overruns and DoS

### Logging
- ✅ S5: Dedicated security event logging
- ✅ S9: Error message sanitization

### Dependency Security
- ✅ S7: Vulnerability scanning support
- Supports pip-audit and safety tools

## Incident Response

If you suspect a security issue:
1. Check `logs/security_events.log`
2. Review recent API usage
3. Rotate API keys if compromised
4. Update dependencies: `pip install --upgrade`

## Compliance
- OWASP Top 10 protections implemented
- Privacy: No PII/PHI logging
- Data retention: Logs rotate automatically

Last updated: 2025-01-09
