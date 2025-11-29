"""
Security audit logging
"""
import logging
from datetime import datetime
from typing import Dict

logging.basicConfig(
    filename='security_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_security_event(event_type: str, details: Dict):
    """Log security event"""
    logging.info(f"SECURITY_EVENT: {event_type} - {details}")

def log_access(user: str, resource: str, action: str):
    """Log access attempt"""
    log_security_event("ACCESS", {
        "user": user,
        "resource": resource,
        "action": action,
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    log_access("test_user", "test_resource", "read")
    print("Audit logging configured")
