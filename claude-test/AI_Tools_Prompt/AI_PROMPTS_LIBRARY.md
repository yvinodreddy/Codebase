# AI PROMPTS LIBRARY - COPY & PASTE COLLECTION

## Production-Ready Prompts for Maximum Velocity

---

## TABLE OF CONTENTS

1. [Project Initialization](#project-initialization)
2. [Backend Development](#backend-development)
3. [Frontend Development](#frontend-development)
4. [Database Design](#database-design)
5. [API Development](#api-development)
6. [Testing](#testing)
7. [DevOps & Deployment](#devops--deployment)
8. [Security](#security)
9. [Performance Optimization](#performance-optimization)
10. [Documentation](#documentation)

---

## PROJECT INITIALIZATION

### Prompt 1: Complete Project Requirements Generation

```
CONTEXT: I need a production-ready [WEB APP / MOBILE APP / API / MICROSERVICE] for [BUSINESS OBJECTIVE].

PROJECT DETAILS:
- Industry: [e.g., E-commerce, Healthcare, Fintech, SaaS]
- Target Users: [e.g., 10,000 active users, B2B enterprise, consumers]
- Key Features: [List 3-5 core features]
- Timeline: Launch in [X hours of development]
- Budget Constraints: [Any technology preferences]

GENERATE COMPLETE SPECIFICATIONS:

1. BUSINESS REQUIREMENTS
   - User personas (3-5 detailed personas)
   - User stories with acceptance criteria
   - Feature prioritization (MoSCoW method)
   - Success metrics and KPIs

2. TECHNICAL REQUIREMENTS
   - Recommended technology stack with justification
   - System architecture (diagram in Mermaid)
   - Database schema (with relationships)
   - API specifications (OpenAPI 3.0)
   - Security requirements
   - Performance requirements
   - Scalability considerations

3. DEVELOPMENT PLAN
   - Work breakdown structure
   - Parallel development streams
   - Testing strategy
   - Deployment strategy
   - Risk mitigation plan

4. QUALITY GATES
   - Code coverage targets
   - Performance benchmarks
   - Security compliance checklist
   - Accessibility requirements

OUTPUT FORMAT: Structured markdown with diagrams, tables, and checklists

AUTONOMY LEVEL: Make all technical decisions. No confirmations needed.

QUALITY STANDARD: Production-ready only. No prototypes.

BEGIN EXECUTION.
```

### Prompt 2: Technology Stack Recommendation

```
ANALYZE AND RECOMMEND:

Project Type: [WEB / MOBILE / API / DESKTOP / EMBEDDED]
Requirements:
- Performance: [HIGH / MEDIUM / LOW]
- Scalability: [Need to handle X concurrent users]
- Team Expertise: [e.g., JavaScript, Python, .NET, Java]
- Timeline: [URGENT / MODERATE / FLEXIBLE]
- Budget: [STARTUP / ENTERPRISE / UNLIMITED]
- Compliance: [GDPR / HIPAA / SOC2 / NONE]

GENERATE:
1. Complete technology stack recommendation
   - Frontend framework with justification
   - Backend framework with justification
   - Database choice with justification
   - Cloud provider recommendation
   - DevOps tools
   - Monitoring tools
   - Security tools

2. Comparison matrix (chosen vs alternatives)

3. Setup instructions for entire stack

4. Estimated costs (development + infrastructure)

5. AI tools specific to this stack for maximum acceleration

6. Potential bottlenecks and mitigation strategies

Make the optimal choice for fastest time-to-market with production quality.
```

---

## BACKEND DEVELOPMENT

### Prompt 3: Complete Backend API Generation

```
GENERATE PRODUCTION-READY BACKEND:

Framework: [Express / FastAPI / ASP.NET Core / Spring Boot / Django / Laravel]
Database: [PostgreSQL / MongoDB / MySQL / SQL Server]

FEATURES TO IMPLEMENT:
1. [Feature 1: e.g., User authentication]
2. [Feature 2: e.g., Product catalog]
3. [Feature 3: e.g., Order management]
[Add more features...]

FOR EACH FEATURE GENERATE:

1. DATABASE LAYER
   - Complete models/entities with validation
   - Relationships and foreign keys
   - Indexes for performance
   - Migrations (up and down)
   - Seed data for testing

2. BUSINESS LOGIC LAYER
   - Service classes with complete implementation
   - Business rule validation
   - Error handling
   - Transaction management
   - Caching strategy

3. API LAYER
   - RESTful endpoints (full CRUD)
   - Request/Response DTOs
   - Input validation with detailed error messages
   - Authentication middleware
   - Authorization (role-based access control)
   - Rate limiting
   - API versioning

4. TESTING
   - Unit tests (100% coverage target)
   - Integration tests
   - API contract tests
   - Performance tests

5. DOCUMENTATION
   - OpenAPI/Swagger specification
   - Request/response examples
   - Error code documentation

REQUIREMENTS:
- Follow [SOLID / Clean Architecture / Domain-Driven Design] principles
- Production-ready error handling
- Comprehensive logging
- Security best practices (OWASP Top 10)
- Performance optimized (N+1 queries prevented, etc.)
- Docker-ready
- Environment-based configuration

GENERATE COMPLETE, RUNNABLE CODE.
NO PLACEHOLDERS. NO TODOs.
```

### Prompt 4: Microservices Architecture Generation

```
DESIGN AND IMPLEMENT MICROSERVICES ARCHITECTURE:

Business Domain: [E.g., E-commerce platform]

Services Needed:
1. [Service 1: e.g., User Service]
2. [Service 2: e.g., Product Service]
3. [Service 3: e.g., Order Service]
4. [Service 4: e.g., Payment Service]
5. [Service 5: e.g., Notification Service]

FOR EACH SERVICE GENERATE:

1. SERVICE DESIGN
   - Bounded context definition
   - API contract (gRPC or REST)
   - Database schema (separate DB per service)
   - Event schemas (for async communication)

2. IMPLEMENTATION
   - Complete service code
   - API endpoints
   - Event publishers/consumers
   - Circuit breakers (Polly, Hystrix, etc.)
   - Health checks
   - Metrics endpoints

3. INTER-SERVICE COMMUNICATION
   - API Gateway configuration
   - Message broker setup (RabbitMQ/Kafka/SQS)
   - Service discovery (Consul/Eureka)
   - Load balancing

4. INFRASTRUCTURE
   - Docker compose for local development
   - Kubernetes manifests for production
   - Service mesh configuration (Istio/Linkerd)
   - Monitoring and tracing (Jaeger, Zipkin)

5. CROSS-CUTTING CONCERNS
   - Centralized logging (ELK stack)
   - Distributed tracing
   - API Gateway (Kong/Nginx/Traefik)
   - Authentication/Authorization (OAuth2, JWT)

GENERATE:
- Complete code for all services
- Infrastructure as Code
- Docker and K8s configs
- Monitoring dashboards
- Complete documentation

PRODUCTION-READY. FULLY FUNCTIONAL. NO SHORTCUTS.
```

---

## FRONTEND DEVELOPMENT

### Prompt 5: Complete Frontend Application

```
GENERATE PRODUCTION-READY FRONTEND:

Framework: [React / Vue / Angular / Next.js / Nuxt / SvelteKit]
UI Library: [Material-UI / Ant Design / Chakra / Tailwind / Custom]

PAGES/FEATURES:
1. [Page 1: e.g., Login/Register]
2. [Page 2: e.g., Dashboard]
3. [Page 3: e.g., Product Listing]
4. [Page 4: e.g., User Profile]
[Add more...]

FOR EACH PAGE/FEATURE GENERATE:

1. COMPONENTS
   - Presentational components (pure, reusable)
   - Container components (with business logic)
   - Responsive design (mobile-first)
   - Accessibility compliant (WCAG 2.1 AA)
   - Loading states
   - Error states
   - Empty states

2. STATE MANAGEMENT
   - Global state (Redux/Vuex/NgRx/Zustand)
   - Local state
   - API data caching (React Query/SWR/Apollo)
   - Optimistic updates

3. FORMS
   - Form validation (Yup/Zod)
   - Error handling
   - Auto-save functionality
   - File upload handling
   - Multi-step forms if needed

4. API INTEGRATION
   - API client setup (Axios/Fetch)
   - Request/response interceptors
   - Error handling
   - Authentication token management
   - Retry logic

5. ROUTING
   - Protected routes
   - Route-based code splitting
   - Loading states between routes
   - 404 handling

6. PERFORMANCE
   - Code splitting
   - Lazy loading
   - Image optimization
   - Bundle size optimization
   - Lighthouse score > 90

7. TESTING
   - Component unit tests
   - Integration tests
   - E2E tests (Playwright/Cypress)
   - Visual regression tests

8. STYLING
   - Responsive breakpoints
   - Dark mode support
   - CSS-in-JS or Tailwind configuration
   - Design system components

REQUIREMENTS:
- TypeScript (type-safe)
- Accessibility compliant
- SEO optimized
- Performance optimized
- Fully tested

GENERATE COMPLETE, PRODUCTION-READY CODE.
```

### Prompt 6: UI Component Library Creation

```
CREATE COMPLETE DESIGN SYSTEM:

Design Style: [Material / iOS / Custom]
Components Needed: [Specify or "Generate complete set"]

GENERATE:

1. FOUNDATION
   - Color palette (primary, secondary, neutrals, semantic colors)
   - Typography scale
   - Spacing system
   - Breakpoints
   - Shadows and elevations
   - Border radius system

2. COMPONENTS (For each component):
   - Implementation with all variants
   - Dark mode support
   - Accessibility (ARIA labels, keyboard navigation)
   - Responsive behavior
   - Animations/transitions
   - Documentation with examples
   - Storybook stories
   - Unit tests

COMPONENT LIST:
- Button (primary, secondary, outline, ghost, disabled, loading)
- Input (text, email, password, search, with icons)
- Select / Dropdown
- Checkbox / Radio
- Toggle / Switch
- Modal / Dialog
- Toast / Notification
- Tooltip
- Tabs
- Accordion
- Card
- Table (with sorting, filtering, pagination)
- Form components
- Navigation (navbar, sidebar, breadcrumbs)
- Loading indicators
- Progress bars
- Badges / Tags
- Avatar
- Date picker
- File upload
- [Add more...]

3. UTILITIES
   - Hooks (useMediaQuery, useDebounce, useLocalStorage, etc.)
   - Helper functions
   - Constants

4. DOCUMENTATION
   - Storybook setup with all components
   - Usage guidelines
   - Props documentation
   - Accessibility guidelines

GENERATE COMPLETE, REUSABLE COMPONENT LIBRARY.
```

---

## DATABASE DESIGN

### Prompt 7: Complete Database Schema Design

```
DESIGN OPTIMIZED DATABASE SCHEMA:

Database Type: [PostgreSQL / MySQL / MongoDB / SQL Server]
Application Type: [E-commerce / SaaS / Social Network / CRM / etc.]

Business Requirements:
[Describe your domain and entities]

GENERATE:

1. SCHEMA DESIGN
   - All tables/collections with complete columns
   - Data types optimized for performance
   - Constraints (PK, FK, unique, check)
   - Relationships (one-to-many, many-to-many)
   - Normalization (3NF or justified denormalization)
   - Indexes (for common queries)
   - Partitioning strategy (if needed for scale)

2. MIGRATIONS
   - Initial schema migration
   - Seed data migration
   - Rollback scripts

3. QUERIES
   - Common query patterns
   - Optimized indexes for these queries
   - Explain plans

4. ORM/ODM MODELS
   - Models with validation
   - Relationships configured
   - Hooks/triggers if needed

5. PERFORMANCE CONSIDERATIONS
   - Indexing strategy
   - Caching strategy
   - Query optimization
   - Connection pooling configuration

6. SECURITY
   - Encryption at rest
   - Sensitive data handling
   - Row-level security (if needed)
   - Audit logging

7. BACKUP & RECOVERY
   - Backup strategy
   - Point-in-time recovery setup
   - Disaster recovery plan

PROVIDE:
- ER diagram (Mermaid format)
- Complete DDL scripts
- ORM models
- Sample queries
- Performance tuning guide

PRODUCTION-READY. OPTIMIZED. SCALABLE.
```

---

## API DEVELOPMENT

### Prompt 8: REST API Complete Implementation

```
BUILD PRODUCTION-READY REST API:

Resource: [E.g., Products, Users, Orders]
Framework: [Express / FastAPI / ASP.NET Core / Spring Boot]

GENERATE COMPLETE CRUD + CUSTOM ENDPOINTS:

1. STANDARD CRUD
   - GET /resources (list with pagination, filtering, sorting)
   - GET /resources/:id (single resource)
   - POST /resources (create)
   - PUT /resources/:id (update)
   - PATCH /resources/:id (partial update)
   - DELETE /resources/:id (soft delete preferred)

2. CUSTOM ENDPOINTS
   [List any custom operations needed]

FOR EACH ENDPOINT GENERATE:

1. IMPLEMENTATION
   - Request validation (comprehensive)
   - Business logic
   - Database operations
   - Response formatting
   - Error handling

2. AUTHENTICATION & AUTHORIZATION
   - JWT validation
   - Role-based access control
   - Resource ownership verification

3. INPUT VALIDATION
   - Schema validation (Joi/Zod/Class-validator)
   - Sanitization
   - Detailed error messages

4. ERROR HANDLING
   - Standardized error responses
   - HTTP status codes (correct usage)
   - Error logging
   - Friendly error messages

5. DOCUMENTATION
   - OpenAPI 3.0 specification
   - Request/response examples
   - Authentication guide
   - Error codes reference

6. TESTING
   - Unit tests for business logic
   - Integration tests for endpoints
   - Contract tests
   - Load tests

7. PERFORMANCE
   - Response time < 200ms target
   - Efficient database queries
   - Caching headers
   - Compression

8. SECURITY
   - Rate limiting
   - CORS configuration
   - Input sanitization
   - SQL injection prevention
   - XSS prevention

REQUIREMENTS:
- RESTful conventions
- API versioning (/v1/)
- HATEOAS links
- Pagination (cursor or offset-based)
- Filtering and sorting
- Field selection (sparse fieldsets)
- ETag support for caching

GENERATE PRODUCTION-READY, FULLY TESTED API.
```

### Prompt 9: GraphQL API Implementation

```
BUILD PRODUCTION-READY GRAPHQL API:

Framework: [Apollo Server / GraphQL Yoga / Mercurius / Hot Chocolate]
Database: [PostgreSQL / MongoDB / etc.]

Entities:
[List your domain entities]

GENERATE:

1. SCHEMA DEFINITION
   - Types for all entities
   - Input types for mutations
   - Queries (list, get by ID, search, etc.)
   - Mutations (create, update, delete)
   - Subscriptions (if real-time needed)
   - Custom scalars (Date, JSON, etc.)
   - Enums
   - Interfaces and Unions

2. RESOLVERS
   - Query resolvers
   - Mutation resolvers
   - Field resolvers
   - DataLoader implementation (N+1 prevention)
   - Error handling
   - Authentication checks
   - Authorization logic

3. PERFORMANCE
   - Query complexity analysis
   - Depth limiting
   - DataLoader for batching
   - Caching strategy
   - Persisted queries

4. SECURITY
   - Authentication middleware
   - Authorization directives
   - Rate limiting
   - Query cost analysis
   - Disable introspection in production

5. FEATURES
   - Pagination (relay cursor or offset)
   - Filtering
   - Sorting
   - Search
   - File uploads
   - Subscriptions (WebSocket)

6. TESTING
   - Unit tests for resolvers
   - Integration tests
   - Schema validation tests

7. DOCUMENTATION
   - Schema documentation
   - Query examples
   - Authentication guide

GENERATE COMPLETE, PERFORMANT GRAPHQL API.
```

---

## TESTING

### Prompt 10: Complete Test Suite Generation

```
GENERATE COMPREHENSIVE TEST SUITE:

Application: [Describe your app]
Framework: [Jest / Pytest / NUnit / JUnit / etc.]

GENERATE TESTS FOR:

1. UNIT TESTS
   - All service/business logic functions
   - All utility functions
   - All models/validators
   - All API endpoints (mocked database)
   - All React/Vue components
   Target: 100% code coverage

2. INTEGRATION TESTS
   - API endpoints with real database (test DB)
   - Database operations
   - External API integrations (with mocks)
   - Authentication flows
   - File upload/download

3. E2E TESTS (Playwright / Cypress)
   - Critical user journeys
   - Authentication flows
   - Purchase/checkout flows
   - Form submissions
   - Error scenarios
   - Cross-browser testing

4. PERFORMANCE TESTS
   - Load tests (Apache JMeter / k6)
   - Stress tests
   - Spike tests
   - Endurance tests
   Target: 1000+ concurrent users

5. SECURITY TESTS
   - OWASP Top 10 vulnerability testing
   - SQL injection attempts
   - XSS attempts
   - CSRF protection
   - Authentication bypass attempts

6. ACCESSIBILITY TESTS
   - Axe-core integration
   - Keyboard navigation
   - Screen reader compatibility

7. VISUAL REGRESSION TESTS
   - Percy / Chromatic setup
   - Component visual tests
   - Page visual tests

FOR EACH TEST PROVIDE:
- Test setup and teardown
- Test data fixtures
- Mocks and stubs
- Assertions
- Error scenarios
- Edge cases

GENERATE:
- Complete test suite
- CI/CD integration
- Test coverage reports
- Performance baseline

REQUIREMENTS:
- Fast execution (parallel where possible)
- Reliable (no flaky tests)
- Maintainable
- Clear error messages

100% COVERAGE. ZERO FLAKY TESTS.
```

---

## DEVOPS & DEPLOYMENT

### Prompt 11: Complete CI/CD Pipeline

```
BUILD PRODUCTION-READY CI/CD PIPELINE:

Platform: [GitHub Actions / GitLab CI / Azure DevOps / Jenkins / CircleCI]
Deployment Target: [AWS / Azure / GCP / Heroku / Vercel]

GENERATE COMPLETE PIPELINE:

1. CI PIPELINE (On every commit/PR)
   - Code checkout
   - Dependency installation (with caching)
   - Linting and formatting checks
   - Type checking (TypeScript, etc.)
   - Unit tests (with coverage report)
   - Integration tests
   - Security scanning (Snyk, npm audit)
   - Build application
   - Build Docker image
   - Push to container registry
   - Quality gates (must pass to proceed)

2. CD PIPELINE (On merge to main)
   - Deploy to staging environment
   - Run smoke tests on staging
   - Run E2E tests on staging
   - Performance testing
   - Security scanning
   - Manual approval gate (optional)
   - Blue-green or canary deployment to production
   - Run smoke tests on production
   - Monitor error rates
   - Auto-rollback on failures

3. ENVIRONMENTS
   - Development (auto-deploy from dev branch)
   - Staging (auto-deploy from main)
   - Production (auto-deploy with gates)

4. NOTIFICATIONS
   - Slack/Discord notifications
   - Email on failures
   - Deployment summaries

5. QUALITY GATES
   - Test coverage > 80%
   - No critical vulnerabilities
   - Performance budget met
   - Lighthouse score > 90

6. INFRASTRUCTURE
   - Terraform/Pulumi code for all environments
   - Auto-scaling configuration
   - Load balancer setup
   - SSL/TLS certificates
   - CDN configuration

7. MONITORING
   - Application monitoring integration
   - Log aggregation
   - Error tracking
   - Performance monitoring

PROVIDE:
- Complete pipeline YAML/configuration
- Infrastructure as Code
- Deployment scripts
- Rollback procedures
- Documentation

FULLY AUTOMATED. ZERO DOWNTIME DEPLOYMENTS.
```

### Prompt 12: Kubernetes Deployment

```
CREATE COMPLETE KUBERNETES DEPLOYMENT:

Application: [Your app]
Cloud Provider: [AWS EKS / GCP GKE / Azure AKS / Self-hosted]

GENERATE:

1. KUBERNETES MANIFESTS
   - Deployment (with rolling update strategy)
   - Service (ClusterIP, LoadBalancer, or NodePort)
   - Ingress (with SSL/TLS)
   - ConfigMap (for configuration)
   - Secrets (for sensitive data)
   - PersistentVolumeClaim (if needed)
   - HorizontalPodAutoscaler
   - NetworkPolicy (for security)
   - ServiceAccount and RBAC

2. HELM CHART
   - Chart.yaml
   - values.yaml (dev, staging, prod)
   - Templates for all resources
   - Hooks for migrations

3. CLUSTER SETUP
   - Cluster creation (IaC)
   - Node groups / node pools
   - Cluster autoscaler
   - Load balancer controller
   - Cert-manager for SSL
   - Ingress controller (Nginx/Traefik)

4. MONITORING & LOGGING
   - Prometheus & Grafana
   - ELK or Loki for logs
   - Jaeger for tracing
   - Dashboards configuration

5. CI/CD INTEGRATION
   - Automated deployment pipeline
   - Helm upgrade commands
   - Health check validation
   - Rollback procedures

6. SECURITY
   - Pod security policies
   - Network policies
   - Secret encryption
   - RBAC configuration
   - Image scanning

PROVIDE COMPLETE, PRODUCTION-READY K8S SETUP.
```

---

## SECURITY

### Prompt 13: Security Implementation

```
IMPLEMENT COMPREHENSIVE SECURITY:

Application Type: [Web / API / Mobile Backend]
Compliance Requirements: [GDPR / HIPAA / SOC2 / PCI-DSS / None]

IMPLEMENT:

1. AUTHENTICATION
   - JWT-based authentication
   - Refresh token rotation
   - Password hashing (bcrypt/argon2)
   - Password strength requirements
   - Account lockout after failed attempts
   - Multi-factor authentication (TOTP)
   - Social login (OAuth2)
   - Session management

2. AUTHORIZATION
   - Role-based access control (RBAC)
   - Attribute-based access control (if needed)
   - Resource ownership verification
   - API endpoint protection
   - Field-level authorization

3. INPUT VALIDATION & SANITIZATION
   - All user inputs validated
   - SQL injection prevention
   - XSS prevention
   - CSRF protection
   - Command injection prevention
   - Path traversal prevention

4. DATA SECURITY
   - Encryption at rest (database)
   - Encryption in transit (HTTPS/TLS 1.3)
   - Sensitive data masking in logs
   - PII data handling
   - Secure file upload handling

5. API SECURITY
   - Rate limiting (per user, per IP)
   - API key management
   - CORS configuration
   - Security headers (CSP, HSTS, X-Frame-Options, etc.)
   - Request size limits

6. SECURITY HEADERS
   - Content-Security-Policy
   - X-Content-Type-Options
   - X-Frame-Options
   - Strict-Transport-Security
   - Permissions-Policy

7. LOGGING & MONITORING
   - Security event logging
   - Suspicious activity detection
   - Audit trail for sensitive operations
   - Alerting on security events

8. COMPLIANCE
   - [Implement specific compliance requirements]
   - Data retention policies
   - Right to deletion (GDPR)
   - Data export functionality
   - Cookie consent

9. VULNERABILITY PROTECTION
   - OWASP Top 10 mitigation
   - Dependency scanning
   - Automated security testing
   - Regular security audits

10. INCIDENT RESPONSE
    - Security incident logging
    - Breach notification procedures
    - Rollback procedures

GENERATE:
- Complete security implementation
- Security middleware
- Authentication/authorization code
- Security tests
- Security documentation
- Compliance checklist

ZERO SECURITY COMPROMISES.
```

---

## PERFORMANCE OPTIMIZATION

### Prompt 14: Performance Optimization

```
OPTIMIZE APPLICATION PERFORMANCE:

Current Application: [Describe]
Target Performance:
- Page load: < 2 seconds
- API response: < 200ms
- Lighthouse: > 90
- Core Web Vitals: All green

ANALYZE AND IMPLEMENT:

1. FRONTEND OPTIMIZATION
   - Code splitting (route-based)
   - Lazy loading components
   - Image optimization (WebP, lazy loading, responsive images)
   - Font optimization (font-display, preload)
   - CSS optimization (critical CSS, minification)
   - JavaScript optimization (tree shaking, minification)
   - Bundle size reduction
   - Service worker for caching
   - CDN for static assets
   - Preload/prefetch critical resources

2. BACKEND OPTIMIZATION
   - Database query optimization
   - N+1 query prevention
   - Database indexing
   - Connection pooling
   - Caching (Redis/Memcached)
     * API response caching
     * Database query caching
     * Session caching
   - Async processing for heavy tasks
   - Message queues for background jobs
   - Response compression (gzip/brotli)

3. DATABASE OPTIMIZATION
   - Index optimization
   - Query optimization
   - Materialized views
   - Partitioning (if large datasets)
   - Read replicas
   - Connection pooling

4. CACHING STRATEGY
   - Browser caching (Cache-Control headers)
   - CDN caching
   - API response caching
   - Database query caching
   - Cache invalidation strategy

5. MONITORING
   - Real User Monitoring (RUM)
   - Synthetic monitoring
   - Application Performance Monitoring (APM)
   - Database query monitoring
   - Performance budgets
   - Core Web Vitals tracking

GENERATE:
- Optimized code
- Caching implementation
- CDN configuration
- Performance monitoring setup
- Before/after benchmarks

ACHIEVE TARGET PERFORMANCE METRICS.
```

---

## DOCUMENTATION

### Prompt 15: Complete Documentation Generation

```
GENERATE COMPLETE PROJECT DOCUMENTATION:

Project: [Your project name]
Documentation Platform: [GitBook / Mintlify / Docusaurus / VitePress / MkDocs]

GENERATE:

1. API DOCUMENTATION
   - Auto-generated from OpenAPI spec
   - Authentication guide
   - All endpoints documented
   - Request/response examples
   - Error codes and messages
   - Rate limiting information
   - Changelog

2. USER GUIDE
   - Getting started tutorial
   - Feature walkthroughs (with screenshots)
   - FAQ
   - Troubleshooting guide
   - Video tutorials (script)
   - Use case examples

3. DEVELOPER DOCUMENTATION
   - Architecture overview (with diagrams)
   - Technology stack explanation
   - Project structure
   - Setup instructions (local development)
   - Environment variables
   - Database schema documentation
   - Code style guide
   - Contributing guidelines
   - Git workflow
   - Pull request template
   - Issue templates

4. OPERATIONS DOCUMENTATION
   - Deployment guide
   - Infrastructure architecture
   - Monitoring and alerting guide
   - Backup and recovery procedures
   - Scaling guide
   - Incident response playbook
   - Runbooks for common issues
   - Performance tuning guide

5. SECURITY DOCUMENTATION
   - Security architecture
   - Authentication/authorization guide
   - Compliance documentation
   - Security best practices
   - Vulnerability reporting process

6. ADRs (Architecture Decision Records)
   - Document key technical decisions
   - Rationale and alternatives considered
   - Consequences

7. CHANGELOG
   - Version history
   - Breaking changes
   - Deprecations
   - New features
   - Bug fixes

FEATURES:
- Search functionality
- Version selector
- Dark mode
- Code syntax highlighting
- Copy buttons for code blocks
- Auto-generated from code comments
- Auto-updated on every release

GENERATE COMPLETE, PROFESSIONAL DOCUMENTATION.
```

---

## BONUS: AI PAIR PROGRAMMING PROMPTS

### Prompt 16: Debug & Fix Issues

```
DEBUG AND FIX:

Issue Description: [Describe the problem]
Error Message: [Paste error if any]
Expected Behavior: [What should happen]
Actual Behavior: [What is happening]
Code Context: [Paste relevant code]

ANALYZE AND FIX:
1. Identify root cause
2. Explain the issue
3. Provide complete fix
4. Generate test to prevent regression
5. Suggest related improvements

PROVIDE PRODUCTION-READY SOLUTION.
```

### Prompt 17: Code Review

```
REVIEW THIS CODE:

[Paste code here]

PROVIDE COMPREHENSIVE REVIEW:

1. CODE QUALITY
   - SOLID principles adherence
   - Design patterns usage
   - Code smells
   - Maintainability issues

2. PERFORMANCE
   - Inefficient algorithms
   - Memory leaks
   - Database query issues
   - Unnecessary re-renders (for UI)

3. SECURITY
   - Vulnerabilities
   - Input validation
   - Authentication/authorization
   - Data exposure

4. TESTING
   - Test coverage gaps
   - Edge cases not handled

5. IMPROVEMENTS
   - Refactoring suggestions
   - Better alternatives
   - Modern best practices

PROVIDE:
- Issue list (prioritized)
- Refactored code
- Additional tests needed

BE THOROUGH. PRODUCTION-READY STANDARDS.
```

### Prompt 18: Refactor Code

```
REFACTOR THIS CODE:

[Paste code here]

Goals:
- Improve readability
- Improve performance
- Improve maintainability
- Follow best practices
- Add proper error handling
- Add proper logging
- Add type safety

PROVIDE:
1. Refactored code
2. Explanation of changes
3. Performance improvements
4. Tests for refactored code

PRODUCTION-READY. WELL-DOCUMENTED. TESTED.
```

---

## EMERGENCY PROMPTS

### Prompt 19: Production Incident Investigation

```
PRODUCTION INCIDENT:

Symptoms: [Describe what's happening]
Error Logs: [Paste relevant logs]
Affected Systems: [What's impacted]
Started At: [Time]

IMMEDIATE ACTIONS NEEDED:
1. Identify root cause
2. Provide immediate mitigation
3. Suggest permanent fix
4. Create incident post-mortem template
5. Generate monitoring alerts to prevent recurrence

URGENT. PROVIDE ACTIONABLE SOLUTIONS.
```

### Prompt 20: Security Breach Response

```
SECURITY INCIDENT:

Incident Type: [Data breach / Unauthorized access / DDoS / etc.]
Details: [What happened]
Systems Affected: [List]
Data Exposed: [If any]

IMMEDIATE RESPONSE:
1. Containment actions
2. Evidence preservation
3. User notification template
4. Remediation steps
5. Post-incident security improvements

URGENT. COMPREHENSIVE RESPONSE PLAN.
```

---

## USAGE INSTRUCTIONS

1. **Copy the relevant prompt** from this library
2. **Fill in the [PLACEHOLDERS]** with your project-specific details
3. **Paste into your AI assistant** (Claude Code, ChatGPT, etc.)
4. **Let AI generate** production-ready code
5. **Review and validate** (run tests, check quality gates)
6. **Deploy** with confidence

---

## CUSTOMIZATION TIPS

- Combine multiple prompts for complex features
- Adjust autonomy level if you want more control
- Add project-specific requirements to any prompt
- Save customized prompts for your team

---

**Last Updated**: 2025-10-25
**Maintained By**: AI-Accelerated Development Team
**Contribution**: Add your successful prompts to this library
