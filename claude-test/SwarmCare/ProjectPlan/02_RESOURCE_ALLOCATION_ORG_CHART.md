# RESOURCE ALLOCATION & ORGANIZATIONAL CHART
## RAG Heat & SWARMCARE - Team Structure & Role Definitions

**Document Version:** 2.1 Ultimate
**Date:** October 31, 2025
**Total Resources:** 22 core team members (±2)

---

## ORGANIZATIONAL HIERARCHY

```
                    PROJECT DIRECTOR (You)
                            |
        ___________________|___________________
       |                   |                   |
  TECH LEAD          TECH LEAD           BUSINESS DEV
  RAG Heat          SWARMCARE               LEAD
  (10 people)       (12 people)          (Advisory Board)
       |                   |                   |
   [Team Below]        [Team Below]      [Outreach Team]
```

---

## DETAILED ORGANIZATIONAL CHART

### EXECUTIVE LEVEL

#### **Project Director** (You)
**Responsibilities:**
- Overall project strategy and vision
- Final decision-making authority
- Stakeholder management (United Health Group, advisors)
- Research paper mentorship and LaTeX training
- Budget approval and resource allocation
- Risk escalation handling
- Monthly milestone presentations

**Time Allocation:**
- RAG Heat: 40%
- SWARMCARE: 40%
- Advisory Board/Business: 15%
- Research Mentorship: 5%

**Key Deliverables:**
- Weekly project status reports
- Monthly stakeholder presentations
- Quarterly strategy reviews
- Research paper co-authorship (all 4 papers)

---

### PROJECT LEADERSHIP TEAM

#### **1. Technical Lead - RAG Heat**
**Reports To:** Project Director
**Direct Reports:** 9 team members

**Responsibilities:**
- Technical architecture decisions for RAG Heat
- Sprint planning and task allocation
- Code review and quality assurance
- Performance optimization
- Team mentorship and 1-on-1s
- Integration with Neo4j and vector DBs
- API design and implementation oversight

**Required Skills:**
- 5+ years Python development
- RAG/LangChain/LlamaIndex expertise
- Neo4j/graph database experience
- System design and architecture
- Team leadership

**KPIs:**
- Sprint completion rate >90%
- Team satisfaction >4/5
- Code quality score >80
- API performance <2s response time

---

#### **2. Technical Lead - SWARMCARE**
**Reports To:** Project Director
**Direct Reports:** 11 team members

**Responsibilities:**
- Technical architecture decisions for SWARMCARE
- Sprint planning and task allocation
- Code review and quality assurance
- Multi-agent system design
- Team mentorship and 1-on-1s
- Integration with healthcare workflows
- Real-time coordination architecture

**Required Skills:**
- 5+ years backend development
- Multi-agent systems experience
- Real-time systems (WebSockets, SignalR)
- Distributed systems knowledge
- Team leadership

**KPIs:**
- Sprint completion rate >90%
- Team satisfaction >4/5
- Code quality score >80
- System uptime >99.5%

---

#### **3. Research Lead**
**Reports To:** Project Director
**Direct Reports:** 2 Research Engineers (dual role)

**Responsibilities:**
- Research paper planning and execution
- Literature review and novelty assessment
- Experiment design and validation
- Paper writing and submission management
- Collaboration with academic advisors
- LaTeX and writing workshop facilitation

**Required Skills:**
- PhD or Master's in CS/AI/Healthcare Informatics
- Published research papers (3+ papers)
- LaTeX expertise
- Academic writing and peer review process
- Statistical analysis

**KPIs:**
- 4+ papers submitted/published by end of project
- Paper acceptance rate >50%
- Research engineer productivity
- Quality of publications (tier of venues)

---

#### **4. Business Development Lead**
**Reports To:** Project Director
**Focus:** Advisory Board & Partnerships

**Responsibilities:**
- Advisory board member recruitment (target: 5-7)
- Daily outreach (5 emails/day minimum)
- Meeting coordination and scheduling
- Pitch deck creation and refinement
- Partnership negotiation support
- United Health Group relationship management
- Investor relations (if applicable)

**Required Skills:**
- Healthcare industry connections
- Business development experience
- Excellent communication and persuasion
- Network building
- Presentation skills

**KPIs:**
- Advisory board size: 5-7 members
- Outreach emails sent: 5/day minimum
- Meeting conversion rate: >20%
- United Health Group engagement milestone met

---

#### **5. Compliance Officer (Part-time or Consultant)**
**Reports To:** Project Director
**Focus:** HIPAA & Legal Compliance

**Responsibilities:**
- HIPAA compliance framework implementation
- Security audit and penetration testing coordination
- Legal review coordination (with lawyer advisor)
- Data privacy policy creation
- Audit log monitoring
- Incident response planning
- Training team on compliance requirements

**Required Skills:**
- HIPAA compliance expertise
- Healthcare IT security
- Legal/regulatory background
- Audit and risk assessment

**KPIs:**
- Zero HIPAA violations
- Compliance checklist 100% complete
- Security audit passed
- Legal review signed off

---

## RAG HEAT TEAM STRUCTURE (10 RESOURCES)

### **Technical Lead - RAG Heat** (covered above)
**Compensation Tier:** 1 (₹60,000-80,000/month)

---

### **Senior Backend Engineer #1 - RAG Systems**
**Reports To:** Tech Lead - RAG Heat
**Role ID:** RH-BE-01

**Responsibilities:**
- Core RAG pipeline development (LangChain/LlamaIndex)
- Retrieval optimization and chunking strategies
- Prompt engineering and template management
- Integration with OpenAI/Claude APIs
- Performance optimization for embedding generation
- Code review for backend team

**Required Skills:**
- 4+ years Python development
- LangChain/LlamaIndex expertise
- Vector database experience (Pinecone/Weaviate)
- FastAPI or Flask
- Strong understanding of transformer models

**Key Deliverables:**
- RAG pipeline implementation (Sprint 2-4)
- Embedding generation system (Sprint 2)
- Retrieval optimization (Sprint 5-6)
- API endpoints for RAG operations (Sprint 3)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **Senior Backend Engineer #2 - API Development**
**Reports To:** Tech Lead - RAG Heat
**Role ID:** RH-BE-02

**Responsibilities:**
- REST API design and implementation (FastAPI)
- Authentication and authorization (JWT, OAuth)
- Rate limiting and API gateway setup
- API documentation (Swagger/OpenAPI)
- Integration testing
- Monitoring and logging setup

**Required Skills:**
- 4+ years Python backend development
- FastAPI/Flask expert
- PostgreSQL or similar RDBMS
- Redis for caching
- Docker and containerization

**Key Deliverables:**
- API framework setup (Sprint 1)
- Authentication system (Sprint 2)
- Core API endpoints (Sprint 2-4)
- API documentation (ongoing)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **Backend Engineer #3 - Integration**
**Reports To:** Tech Lead - RAG Heat
**Role ID:** RH-BE-03

**Responsibilities:**
- Third-party API integrations
- Data pipeline orchestration
- ETL process implementation
- Error handling and retry logic
- Background job processing (Celery)
- Service-to-service communication

**Required Skills:**
- 2-3 years Python development
- API integration experience
- Message queues (RabbitMQ/Kafka)
- Airflow or similar orchestration
- Error handling and resilience patterns

**Key Deliverables:**
- Data ingestion pipelines (Sprint 1-2)
- Third-party integrations (Sprint 3-4)
- Background job system (Sprint 2)
- Error handling framework (Sprint 2)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **AI/ML Engineer #1 - Model Optimization**
**Reports To:** Tech Lead - RAG Heat
**Role ID:** RH-ML-01

**Responsibilities:**
- LLM fine-tuning and optimization
- Prompt engineering and evaluation
- Model selection and benchmarking
- RAG system evaluation metrics
- Embedding model optimization
- Cost optimization for API calls

**Required Skills:**
- 3+ years ML/AI experience
- Fine-tuning experience (LoRA, QLoRA)
- Hugging Face ecosystem
- MLOps practices
- Evaluation frameworks

**Key Deliverables:**
- Model evaluation framework (Sprint 2)
- Prompt optimization (Sprint 3-5)
- Fine-tuned models (Sprint 6-8)
- Cost optimization report (Sprint 8)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **AI/ML Engineer #2 - NLP & Healthcare**
**Reports To:** Tech Lead - RAG Heat
**Role ID:** RH-ML-02

**Responsibilities:**
- Medical NLP pipeline development
- Named entity recognition (NER) for medical terms
- Ontology integration (SNOMED-CT, ICD-10, etc.)
- Clinical text understanding
- Medical concept extraction
- Healthcare-specific model training

**Required Skills:**
- 3+ years NLP experience
- Healthcare domain knowledge (preferred)
- spaCy, NLTK, Hugging Face Transformers
- Medical ontologies familiarity
- Entity linking and resolution

**Key Deliverables:**
- Medical NER system (Sprint 3-4)
- Ontology integration (Sprint 4-6)
- Clinical concept extraction (Sprint 5-7)
- Healthcare model fine-tuning (Sprint 7-8)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **Data Engineer - Neo4j Specialist**
**Reports To:** Tech Lead - RAG Heat
**Role ID:** RH-DE-01

**Responsibilities:**
- Neo4j database design and schema
- Knowledge graph construction
- Cypher query optimization
- Ontology loading and mapping
- Graph algorithms implementation
- Data pipeline for graph ingestion
- Graph visualization setup

**Required Skills:**
- 3+ years data engineering
- Neo4j expert-level knowledge
- Cypher query language mastery
- Graph algorithms (PageRank, community detection)
- Python data processing (Pandas, PySpark)

**Key Deliverables:**
- Neo4j schema design (Sprint 1)
- Ontology loading scripts (Sprint 2-3)
- Knowledge graph population (Sprint 3-5)
- Query optimization (Sprint 6)
- Graph APIs (Sprint 4-6)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **Frontend Engineer**
**Reports To:** Tech Lead - RAG Heat
**Role ID:** RH-FE-01

**Responsibilities:**
- React/Next.js frontend development
- UI/UX implementation based on designs
- State management (Redux/Zustand)
- API integration with backend
- Responsive design implementation
- Frontend testing (Jest, React Testing Library)

**Required Skills:**
- 2-3 years React development
- TypeScript proficiency
- Modern CSS (Tailwind or Material-UI)
- REST API consumption
- Frontend testing

**Key Deliverables:**
- UI framework setup (Sprint 1)
- Core pages implementation (Sprint 2-4)
- RAG interface (Sprint 4-6)
- Dashboard and visualization (Sprint 6-8)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **QA Engineer**
**Reports To:** Tech Lead - RAG Heat
**Role ID:** RH-QA-01

**Responsibilities:**
- Test plan creation and execution
- Automated test development (Pytest, Selenium)
- API testing (Postman, REST Assured)
- Performance testing (Locust, JMeter)
- Bug tracking and triage
- CI/CD pipeline testing integration

**Required Skills:**
- 2+ years QA experience
- Test automation (Pytest, Selenium)
- API testing tools
- Performance testing
- Bug tracking (Jira)

**Key Deliverables:**
- Test plan (Sprint 1)
- Automated test suite (ongoing)
- Performance test suite (Sprint 6)
- Weekly QA reports

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **Research Engineer (Dual Role: Dev + Research)**
**Reports To:** Tech Lead (development) + Research Lead (research)
**Role ID:** RH-RES-01

**Responsibilities:**
- 50% Development work (assigned stories)
- 50% Research paper contribution
- Experiment implementation
- Data analysis and visualization
- Literature review
- Paper writing (co-author on 2 papers)

**Required Skills:**
- Master's or PhD student (preferred)
- Strong Python development
- Research methodology
- Academic writing
- Statistical analysis

**Key Deliverables:**
- Development tasks (half capacity)
- Co-author Paper #1 and Paper #3
- Experiment results documentation
- Research contributions

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

## SWARMCARE TEAM STRUCTURE (12 RESOURCES)

### **Technical Lead - SWARMCARE** (covered above)
**Compensation Tier:** 1 (₹60,000-80,000/month)

---

### **Senior Backend Engineer #1 - Multi-Agent Systems**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-BE-01

**Responsibilities:**
- Multi-agent framework design (AutoGen, CrewAI)
- Agent coordination and communication
- Task delegation and workflow orchestration
- Agent state management
- Inter-agent messaging protocols
- Agent behavior monitoring

**Required Skills:**
- 4+ years Python development
- Multi-agent systems experience
- Distributed systems knowledge
- Event-driven architecture
- Message queues (RabbitMQ, Kafka)

**Key Deliverables:**
- Multi-agent framework (Sprint 2-3)
- Agent orchestration system (Sprint 3-4)
- Agent communication layer (Sprint 2)
- Workflow engine (Sprint 4-5)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **Senior Backend Engineer #2 - Real-time Systems**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-BE-02

**Responsibilities:**
- WebSocket/SignalR implementation
- Real-time collaboration features
- Event streaming architecture
- Notification system
- Live updates and synchronization
- Connection management and scalability

**Required Skills:**
- 4+ years backend development
- WebSocket/SignalR expertise
- Real-time systems (Socket.io, SignalR)
- Redis Pub/Sub
- Load balancing for WebSockets

**Key Deliverables:**
- WebSocket infrastructure (Sprint 2)
- Real-time notification system (Sprint 3-4)
- Live collaboration features (Sprint 5-6)
- Scalability optimization (Sprint 7-8)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **Backend Engineer #3 - API Development**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-BE-03

**Responsibilities:**
- REST API implementation (FastAPI/Express)
- Healthcare workflow APIs
- FHIR compatibility layer
- API security and rate limiting
- API documentation
- Integration testing

**Required Skills:**
- 3+ years backend development
- FastAPI or Node.js/Express
- FHIR standard knowledge (preferred)
- API design best practices
- Authentication/authorization

**Key Deliverables:**
- Core API framework (Sprint 1)
- Healthcare workflow APIs (Sprint 2-4)
- FHIR integration (Sprint 5-6)
- API documentation (ongoing)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **Backend Engineer #4 - Integration & Services**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-BE-04

**Responsibilities:**
- Third-party service integrations
- EHR system integration preparation
- Data synchronization services
- Background job processing
- Service orchestration
- Error handling and monitoring

**Required Skills:**
- 2-3 years backend development
- Integration patterns
- Message queues
- Healthcare systems familiarity
- API integration experience

**Key Deliverables:**
- Integration framework (Sprint 1-2)
- EHR integration layer (Sprint 4-5)
- Background services (Sprint 2-3)
- Monitoring setup (Sprint 3)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **AI/ML Engineer #1 - Agent Intelligence**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-ML-01

**Responsibilities:**
- Agent decision-making logic
- LLM integration for agent reasoning
- Agent learning and adaptation
- Healthcare domain logic implementation
- Agent evaluation metrics
- Intelligent task routing

**Required Skills:**
- 3+ years AI/ML experience
- Multi-agent systems
- Reinforcement learning (preferred)
- LLM prompt engineering
- Healthcare domain knowledge

**Key Deliverables:**
- Agent intelligence layer (Sprint 3-4)
- Decision-making framework (Sprint 4-5)
- Agent evaluation system (Sprint 5-6)
- Adaptive behavior implementation (Sprint 6-8)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **AI/ML Engineer #2 - Healthcare AI**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-ML-02

**Responsibilities:**
- Healthcare-specific ML models
- Clinical decision support logic
- Risk prediction models
- Patient triage algorithms
- Medical data processing
- Model validation with clinical data

**Required Skills:**
- 3+ years ML experience
- Healthcare ML models
- Clinical data experience
- Model validation methodologies
- Healthcare regulations awareness

**Key Deliverables:**
- Clinical decision support (Sprint 4-6)
- Risk prediction models (Sprint 5-7)
- Triage algorithms (Sprint 6-8)
- Model validation reports (Sprint 8)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **Data Engineer**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-DE-01

**Responsibilities:**
- Data pipeline architecture
- ETL processes for healthcare data
- Data warehouse setup
- Neo4j integration for SWARMCARE
- Data quality and validation
- Analytics data preparation

**Required Skills:**
- 2-3 years data engineering
- ETL tools (Airflow, Dagster)
- SQL and NoSQL databases
- Data modeling
- Healthcare data formats (HL7, FHIR)

**Key Deliverables:**
- Data pipeline architecture (Sprint 1-2)
- ETL processes (Sprint 2-4)
- Data warehouse setup (Sprint 3-4)
- Analytics infrastructure (Sprint 5-6)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **Frontend Engineer #1 - Dashboard**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-FE-01

**Responsibilities:**
- React/Next.js development
- Healthcare dashboard implementation
- Real-time updates UI
- Data visualization (Chart.js, D3.js)
- Responsive design
- Accessibility compliance

**Required Skills:**
- 3+ years React development
- TypeScript
- Real-time UI (WebSockets)
- Data visualization libraries
- Healthcare UI/UX understanding

**Key Deliverables:**
- Dashboard framework (Sprint 1-2)
- Core dashboard pages (Sprint 2-4)
- Real-time features (Sprint 4-6)
- Data visualizations (Sprint 5-7)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **Frontend Engineer #2 - Workflow UI**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-FE-02

**Responsibilities:**
- Healthcare workflow interface
- Task management UI
- Collaboration features UI
- Mobile-responsive design
- Form design and validation
- User notification system

**Required Skills:**
- 2-3 years React development
- TypeScript
- Form libraries (Formik, React Hook Form)
- Mobile-first design
- State management

**Key Deliverables:**
- Workflow interface (Sprint 3-5)
- Task management UI (Sprint 4-6)
- Collaboration features (Sprint 5-7)
- Mobile optimization (Sprint 6-8)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **QA Engineer**
**Reports To:** Tech Lead - SWARMCARE
**Role ID:** SC-QA-01

**Responsibilities:**
- Test strategy and planning
- Automated testing (Pytest, Selenium)
- Real-time feature testing
- API and integration testing
- Performance testing
- Security testing coordination

**Required Skills:**
- 2+ years QA experience
- Test automation
- Real-time system testing
- API testing
- Performance testing tools

**Key Deliverables:**
- Test strategy (Sprint 1)
- Automated test suite (ongoing)
- Performance tests (Sprint 6)
- Security test coordination (Sprint 7)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **Research Engineer (Dual Role: Dev + Research)**
**Reports To:** Tech Lead (development) + Research Lead (research)
**Role ID:** SC-RES-01

**Responsibilities:**
- 50% Development work
- 50% Research paper contribution
- Multi-agent system evaluation
- Experiment design and execution
- Data collection and analysis
- Paper writing (co-author on 2 papers)

**Required Skills:**
- Master's or PhD student (preferred)
- Strong Python development
- Research methodology
- Academic writing
- Agent systems knowledge

**Key Deliverables:**
- Development tasks (half capacity)
- Co-author Paper #2 and Paper #4
- Experiment infrastructure
- Research data analysis

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

## SHARED RESOURCES (3 PEOPLE)

### **DevOps Engineer (Shared 50/50)**
**Reports To:** Both Tech Leads
**Role ID:** SHARED-DEVOPS-01

**Responsibilities:**
- CI/CD pipeline setup and maintenance
- Docker containerization
- Kubernetes orchestration
- Cloud infrastructure (GCP/AWS)
- Monitoring and alerting (Prometheus, Grafana)
- Security hardening
- Backup and disaster recovery

**Time Allocation:**
- RAG Heat: 40%
- SWARMCARE: 40%
- Shared infrastructure: 20%

**Required Skills:**
- 3+ years DevOps experience
- Docker and Kubernetes
- Cloud platforms (GCP or AWS)
- CI/CD tools (GitHub Actions, Jenkins)
- Infrastructure as Code (Terraform)

**Key Deliverables:**
- CI/CD pipeline (Sprint 1)
- Production infrastructure (Sprint 2-3)
- Monitoring setup (Sprint 3)
- Security hardening (Sprint 7)

**Compensation Tier:** 2 (₹45,000-60,000/month)

---

### **UX Designer (Shared 50/50)**
**Reports To:** Both Tech Leads
**Role ID:** SHARED-UX-01

**Responsibilities:**
- User interface design
- User experience optimization
- Design system creation
- Prototyping (Figma)
- User research
- Usability testing

**Time Allocation:**
- RAG Heat: 40%
- SWARMCARE: 40%
- Design system: 20%

**Required Skills:**
- 2-3 years UX design
- Figma expert
- Healthcare UI experience (preferred)
- Responsive design
- Accessibility standards

**Key Deliverables:**
- Design system (Sprint 1-2)
- RAG Heat designs (Sprint 1-4)
- SWARMCARE designs (Sprint 1-5)
- Usability testing reports (ongoing)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

### **Technical Writer**
**Reports To:** Project Director
**Role ID:** SHARED-WRITER-01

**Responsibilities:**
- API documentation
- User guides and tutorials
- Architecture documentation
- Process documentation
- Release notes
- Knowledge base articles

**Time Allocation:**
- RAG Heat: 40%
- SWARMCARE: 40%
- General documentation: 20%

**Required Skills:**
- 2+ years technical writing
- Software documentation experience
- Markdown proficiency
- API documentation (Swagger)
- Healthcare domain familiarity (preferred)

**Key Deliverables:**
- Documentation framework (Sprint 1)
- API docs (ongoing with each sprint)
- User guides (Sprint 4, 8)
- Architecture docs (Sprint 2, 6)

**Compensation Tier:** 3 (₹35,000-45,000/month)

---

## ROLE-BASED ACCESS CONTROL (RBAC)

### GitHub Access:

**Admin Access:**
- Project Director
- Tech Lead - RAG Heat
- Tech Lead - SWARMCARE
- DevOps Engineer

**Write Access (to assigned repos):**
- All engineers (can push to their feature branches)
- Can create PRs to `develop`

**Read Access:**
- All team members (can view all repos)
- Advisory board members (optional, specific repos)

### Infrastructure Access:

**Production Admin:**
- Project Director
- DevOps Engineer

**Production Read:**
- Tech Leads
- Senior Engineers

**Staging/Dev Admin:**
- Tech Leads
- DevOps Engineer
- All Senior Engineers

**Staging/Dev Write:**
- All engineers

### Database Access:

**Production DB:**
- Only through applications (no direct access)
- Emergency access: Project Director, DevOps, Tech Leads

**Staging/Dev DB:**
- Tech Leads, Data Engineers, Backend Engineers (read/write)
- Other engineers (read-only)

### Cloud Console Access:

**Admin:**
- Project Director
- DevOps Engineer

**Editor:**
- Tech Leads

**Viewer:**
- All engineers

---

## COMMUNICATION HIERARCHY

### For Technical Issues:
Developer → Senior Developer → Tech Lead → Project Director

### For Resource/People Issues:
Team Member → Tech Lead → Project Director

### For Research Questions:
Research Engineer → Research Lead → Project Director

### For Business/Advisory:
Business Dev Lead → Project Director → Advisory Board

### For Compliance:
Any Team Member → Compliance Officer → Project Director → Legal Advisor

---

## TEAM DISTRIBUTION SUMMARY

### By Project:
- **RAG Heat:** 10 dedicated resources
- **SWARMCARE:** 12 dedicated resources
- **Shared:** 3 resources (50/50 split)

### By Role:
- **Leadership:** 5 (Director, 2 Tech Leads, Research Lead, Business Dev Lead)
- **Backend Engineers:** 7 (3 RAG Heat, 4 SWARMCARE)
- **AI/ML Engineers:** 4 (2 RAG Heat, 2 SWARMCARE)
- **Data Engineers:** 2 (1 RAG Heat, 1 SWARMCARE)
- **Frontend Engineers:** 3 (1 RAG Heat, 2 SWARMCARE)
- **QA Engineers:** 2 (1 RAG Heat, 1 SWARMCARE)
- **Research Engineers:** 2 (1 RAG Heat, 1 SWARMCARE)
- **Shared Services:** 3 (DevOps, UX, Writer)
- **Compliance:** 1 (part-time/consultant)

### By Seniority:
- **Leadership/Senior:** 9 people
- **Mid-Level:** 8 people
- **Junior:** 5 people

### By Compensation Tier:
- **Tier 1 (₹60-80K):** 5 people
- **Tier 2 (₹45-60K):** 10 people
- **Tier 3 (₹35-45K):** 7 people

---

## CAPACITY PLANNING

### Sprint Capacity (14-day sprint):

**Assumptions:**
- 10 working days per sprint
- 6 productive hours per day
- 60 hours per person per sprint

**Total Team Capacity:**
- 22 people × 60 hours = 1,320 hours/sprint
- Minus 15% overhead (meetings, etc.) = 1,122 hours/sprint
- Minus Research time (2 people × 30 hours) = 1,062 hours/sprint

**Available Development Hours:**
- **RAG Heat:** ~450 hours/sprint
- **SWARMCARE:** ~550 hours/sprint
- **Shared/Overhead:** ~62 hours/sprint

**Story Point Velocity (estimated):**
- 1 Story Point = ~4 hours
- **RAG Heat Velocity:** ~110 points/sprint
- **SWARMCARE Velocity:** ~135 points/sprint

---

## ONBOARDING CHECKLIST (Per Resource)

### Pre-Day 1:
- [ ] Offer letter signed
- [ ] NDA + IP agreement signed
- [ ] Documents collected (Aadhaar, PAN, bank details)
- [ ] Company email created
- [ ] Slack account created
- [ ] GitHub account added to org
- [ ] Welcome package sent

### Day 1:
- [ ] Welcome session attended
- [ ] Team introduction
- [ ] Buddy assigned
- [ ] Laptop/equipment setup
- [ ] Access to all tools confirmed

### Week 1:
- [ ] Development environment setup complete
- [ ] First task assigned
- [ ] Code review completed
- [ ] LaTeX training (if research role)
- [ ] 1-on-1 with Tech Lead

### Week 2:
- [ ] Full sprint participation
- [ ] Sprint planning attended
- [ ] First story completed
- [ ] Knowledge base familiarization

---

## SUCCESSION PLANNING

### Critical Roles - Backup:

**Project Director:**
→ Backup: Tech Lead - RAG Heat (interim)

**Tech Lead - RAG Heat:**
→ Backup: Senior Backend Engineer #1

**Tech Lead - SWARMCARE:**
→ Backup: Senior Backend Engineer #1 (SWARMCARE)

**DevOps Engineer:**
→ Cross-training: Senior Engineers + external consultant

**Data Engineers:**
→ Cross-training: At least 1 backend engineer per project

### Knowledge Transfer:
- All critical systems must have 2 people with knowledge
- Monthly knowledge sharing sessions
- Documentation for all major components
- Pair programming for complex features

---

## PERFORMANCE REVIEW SCHEDULE

### Monthly:
- 1-on-1 with Tech Lead (30 mins)
- Sprint performance review
- Stipend calculation

### Quarterly:
- 1-on-1 with Project Director (30 mins)
- Skills assessment
- Career development discussion
- Compensation review

### End of Project:
- Comprehensive performance review
- Reference letter (if requested)
- Project completion bonus calculation

---

## DOCUMENT REFERENCES

This document is part of the comprehensive project plan:

1. Master Project Plan
2. **Resource Allocation & Organizational Chart** ← YOU ARE HERE
3. Sprint Planning & Execution Framework
4. Technical Architecture & Infrastructure Plan
5. Advisory Board & Stakeholder Engagement Plan
6. Compensation & Performance Metrics Framework
7. Research & Documentation Strategy
8. Risk Management & Compliance Plan
9. Communication & Collaboration Framework
10. Timeline & Milestone Tracker

---

**END OF RESOURCE ALLOCATION & ORGANIZATIONAL CHART**
