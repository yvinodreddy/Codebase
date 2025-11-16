#!/usr/bin/env python3
"""
SwarmCare API Documentation Generator
Phase 09: Automated API Documentation Generation

Generates comprehensive API documentation from code and OpenAPI specifications.

Usage:
    python3 generate_api_docs.py
    python3 generate_api_docs.py --output docs/api
    python3 generate_api_docs.py --format all
"""

import sys
import os
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime


class APIDocGenerator:
    """Generates API documentation"""

    def __init__(self, output_dir="docs/api", formats=None):
        self.output_dir = Path(output_dir)
        self.formats = formats or ["openapi", "swagger", "redoc"]
        self.timestamp = datetime.now().isoformat()

    def generate_all(self):
        """Generate all API documentation"""
        print("=" * 80)
        print("SwarmCare API Documentation Generator")
        print("=" * 80)
        print(f"Started: {self.timestamp}")
        print(f"Output: {self.output_dir}")
        print(f"Formats: {', '.join(self.formats)}")
        print("=" * 80)
        print()

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate OpenAPI specification
        if "openapi" in self.formats:
            self._generate_openapi_spec()

        # Generate Swagger UI files
        if "swagger" in self.formats:
            self._generate_swagger_ui()

        # Generate ReDoc files
        if "redoc" in self.formats:
            self._generate_redoc()

        # Generate SDK documentation
        if "sdk" in self.formats:
            self._generate_sdk_docs()

        print()
        print("=" * 80)
        print("✅ API Documentation Generation Complete!")
        print("=" * 80)

    def _generate_openapi_spec(self):
        """Generate OpenAPI 3.1.0 specification"""
        print("Generating OpenAPI Specification...")

        spec = {
            "openapi": "3.1.0",
            "info": {
                "title": "SwarmCare API",
                "version": "2.1.0",
                "description": "SwarmCare Enterprise Healthcare AI Platform API",
                "contact": {
                    "name": "SwarmCare API Support",
                    "url": "https://support.swarmcare.io",
                    "email": "api@swarmcare.io"
                },
                "license": {
                    "name": "Proprietary"
                }
            },
            "servers": [
                {
                    "url": "https://api.swarmcare.io/v1",
                    "description": "Production server"
                },
                {
                    "url": "https://staging-api.swarmcare.io/v1",
                    "description": "Staging server"
                }
            ],
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                },
                "schemas": {
                    "Error": {
                        "type": "object",
                        "properties": {
                            "error": {
                                "type": "string",
                                "description": "Error message"
                            },
                            "code": {
                                "type": "string",
                                "description": "Error code"
                            }
                        },
                        "required": ["error", "code"]
                    },
                    "Health": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["healthy", "unhealthy"]
                            },
                            "version": {
                                "type": "string"
                            },
                            "timestamp": {
                                "type": "string",
                                "format": "date-time"
                            }
                        }
                    }
                }
            },
            "security": [
                {"BearerAuth": []}
            ],
            "paths": {
                "/health": {
                    "get": {
                        "summary": "Health Check",
                        "description": "Returns the health status of the API",
                        "operationId": "getHealth",
                        "tags": ["System"],
                        "security": [],
                        "responses": {
                            "200": {
                                "description": "API is healthy",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Health"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/api/v1/agents": {
                    "get": {
                        "summary": "List Agents",
                        "description": "Returns a list of all SwarmCare AI agents",
                        "operationId": "listAgents",
                        "tags": ["Agents"],
                        "responses": {
                            "200": {
                                "description": "List of agents",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string"},
                                                    "name": {"type": "string"},
                                                    "type": {"type": "string"},
                                                    "status": {"type": "string"}
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "Unauthorized",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Error"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/api/v1/documentation": {
                    "get": {
                        "summary": "Get Documentation",
                        "description": "Returns available documentation",
                        "operationId": "getDocumentation",
                        "tags": ["Documentation"],
                        "responses": {
                            "200": {
                                "description": "Documentation available",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "types": {
                                                    "type": "array",
                                                    "items": {"type": "string"}
                                                },
                                                "count": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "tags": [
                {
                    "name": "System",
                    "description": "System endpoints"
                },
                {
                    "name": "Agents",
                    "description": "AI agent management"
                },
                {
                    "name": "Documentation",
                    "description": "Documentation endpoints"
                }
            ]
        }

        # Write YAML
        output_file = self.output_dir / "openapi.yaml"
        with open(output_file, 'w') as f:
            yaml.dump(spec, f, default_flow_style=False, sort_keys=False)

        print(f"  ✅ OpenAPI specification: {output_file}")

        # Write JSON
        json_file = self.output_dir / "openapi.json"
        with open(json_file, 'w') as f:
            json.dump(spec, f, indent=2)

        print(f"  ✅ OpenAPI JSON: {json_file}")

    def _generate_swagger_ui(self):
        """Generate Swagger UI configuration"""
        print("Generating Swagger UI...")

        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SwarmCare API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
    <style>
        html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
        *, *:before, *:after { box-sizing: inherit; }
        body { margin:0; padding:0; }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
    <script>
    window.onload = function() {
        const ui = SwaggerUIBundle({
            url: "openapi.yaml",
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout"
        });
        window.ui = ui;
    };
    </script>
</body>
</html>
"""

        output_file = self.output_dir / "swagger.html"
        with open(output_file, 'w') as f:
            f.write(html_content)

        print(f"  ✅ Swagger UI: {output_file}")

    def _generate_redoc(self):
        """Generate ReDoc configuration"""
        print("Generating ReDoc...")

        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>SwarmCare API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; }
    </style>
</head>
<body>
    <redoc spec-url='openapi.yaml'></redoc>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
"""

        output_file = self.output_dir / "redoc.html"
        with open(output_file, 'w') as f:
            f.write(html_content)

        print(f"  ✅ ReDoc: {output_file}")

    def _generate_sdk_docs(self):
        """Generate SDK documentation"""
        print("Generating SDK Documentation...")

        sdk_readme = """
# SwarmCare SDK Documentation

## Python SDK

```python
from swarmcare import SwarmCareClient

# Initialize client
client = SwarmCareClient(api_key="your-api-key")

# List agents
agents = client.agents.list()
for agent in agents:
    print(f"{agent.name}: {agent.status}")

# Get documentation
docs = client.documentation.list()
```

## JavaScript SDK

```javascript
import { SwarmCareClient } from '@swarmcare/sdk';

// Initialize client
const client = new SwarmCareClient({ apiKey: 'your-api-key' });

// List agents
const agents = await client.agents.list();
agents.forEach(agent => {
    console.log(`${agent.name}: ${agent.status}`);
});
```

## Authentication

All API requests require a Bearer token:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.swarmcare.io/v1/agents
```
"""

        output_file = self.output_dir / "SDK_DOCUMENTATION.md"
        with open(output_file, 'w') as f:
            f.write(sdk_readme)

        print(f"  ✅ SDK Documentation: {output_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Generate SwarmCare API Documentation")
    parser.add_argument("--output", "-o", default="docs/api",
                       help="Output directory (default: docs/api)")
    parser.add_argument("--format", "-f", nargs='+',
                       choices=["openapi", "swagger", "redoc", "sdk", "all"],
                       default=["all"],
                       help="Documentation formats to generate")

    args = parser.parse_args()

    # Handle 'all' format
    if "all" in args.format:
        formats = ["openapi", "swagger", "redoc", "sdk"]
    else:
        formats = args.format

    # Generate documentation
    generator = APIDocGenerator(output_dir=args.output, formats=formats)
    generator.generate_all()


if __name__ == "__main__":
    main()
