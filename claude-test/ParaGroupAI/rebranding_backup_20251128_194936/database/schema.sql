-- ============================================================================
-- DATABASE-FIRST CONTEXT MANAGEMENT SCHEMA
-- ============================================================================
--
-- PostgreSQL schema for ULTRATHINK context management
-- Supports multi-project, multi-instance architecture
-- Production-ready with ACID compliance
--
-- Author: ULTRATHINK System
-- Date: 2025-11-19
-- Version: 1.0.0
--
-- ============================================================================

-- Drop existing tables if they exist (for clean reinstall)
DROP TABLE IF EXISTS context_snapshots CASCADE;
DROP TABLE IF EXISTS active_instances CASCADE;
DROP TABLE IF EXISTS phases CASCADE;
DROP TABLE IF EXISTS projects CASCADE;

-- ============================================================================
-- PROJECTS TABLE
-- ============================================================================
-- Stores project metadata and high-level information
-- Each project can have multiple phases and instances

CREATE TABLE projects (
    project_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    total_story_points INTEGER DEFAULT 0,
    completed_story_points INTEGER DEFAULT 0,
    total_phases INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Constraints
    CONSTRAINT valid_story_points CHECK (total_story_points >= 0),
    CONSTRAINT valid_completed_points CHECK (completed_story_points >= 0),
    CONSTRAINT valid_phases CHECK (total_phases > 0),
    CONSTRAINT valid_completion CHECK (completed_story_points <= total_story_points)
);

-- Indexes for fast lookups
CREATE INDEX idx_projects_created ON projects(created_at DESC);
CREATE INDEX idx_projects_story_points ON projects(total_story_points);
CREATE INDEX idx_projects_name ON projects(name);

-- Comments
COMMENT ON TABLE projects IS 'Stores project metadata for multi-project context management';
COMMENT ON COLUMN projects.project_id IS 'Unique project identifier (e.g., proj_20251119_142446_abc123)';
COMMENT ON COLUMN projects.metadata IS 'Flexible JSONB field for additional project data';


-- ============================================================================
-- PHASES TABLE
-- ============================================================================
-- Tracks project phases for organizing work

CREATE TABLE phases (
    phase_id SERIAL PRIMARY KEY,
    project_id VARCHAR(50) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    phase_number INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    story_points INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Constraints
    CONSTRAINT valid_phase_number CHECK (phase_number > 0),
    CONSTRAINT valid_phase_status CHECK (status IN ('pending', 'in_progress', 'completed', 'blocked')),
    CONSTRAINT valid_phase_points CHECK (story_points >= 0),

    -- Unique constraint
    UNIQUE(project_id, phase_number)
);

-- Indexes
CREATE INDEX idx_phases_project ON phases(project_id, phase_number);
CREATE INDEX idx_phases_status ON phases(status);

-- Comments
COMMENT ON TABLE phases IS 'Tracks project phases for organizing work into manageable chunks';
COMMENT ON COLUMN phases.status IS 'Phase status: pending, in_progress, completed, blocked';


-- ============================================================================
-- CONTEXT SNAPSHOTS TABLE
-- ============================================================================
-- Stores ALL project context (code, decisions, dependencies, etc.)
-- This is the heart of the database-first architecture

CREATE TABLE context_snapshots (
    snapshot_id SERIAL PRIMARY KEY,
    project_id VARCHAR(50) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES phases(phase_id) ON DELETE SET NULL,
    sequence_number INTEGER NOT NULL,
    content_type VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    token_count INTEGER NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_priority CHECK (priority IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
    CONSTRAINT valid_content_type CHECK (content_type IN ('code', 'config', 'dependency', 'decision', 'architecture', 'test', 'documentation', 'error', 'fix', 'optimization')),
    CONSTRAINT valid_token_count CHECK (token_count >= 0),
    CONSTRAINT valid_sequence CHECK (sequence_number > 0)
);

-- Composite indexes for fast retrieval
CREATE INDEX idx_snapshots_project_phase ON context_snapshots(project_id, phase_id);
CREATE INDEX idx_snapshots_priority ON context_snapshots(priority);
CREATE INDEX idx_snapshots_sequence ON context_snapshots(project_id, sequence_number);
CREATE INDEX idx_snapshots_content_type ON context_snapshots(content_type);
CREATE INDEX idx_snapshots_created ON context_snapshots(created_at DESC);

-- Comments
COMMENT ON TABLE context_snapshots IS 'Stores all project context with priority-based organization';
COMMENT ON COLUMN context_snapshots.priority IS 'Priority level: CRITICAL (load first), HIGH, MEDIUM, LOW';
COMMENT ON COLUMN context_snapshots.content IS 'Actual context data stored as JSON string';
COMMENT ON COLUMN context_snapshots.token_count IS 'Estimated token count for this snapshot';


-- ============================================================================
-- ACTIVE INSTANCES TABLE
-- ============================================================================
-- Tracks all running instances for multi-instance coordination

CREATE TABLE active_instances (
    instance_id VARCHAR(50) PRIMARY KEY,
    project_id VARCHAR(50) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES phases(phase_id) ON DELETE SET NULL,
    hostname VARCHAR(255),
    process_id INTEGER,
    started_at TIMESTAMP DEFAULT NOW(),
    last_heartbeat TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    current_token_usage INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Constraints
    CONSTRAINT valid_status CHECK (status IN ('active', 'idle', 'crashed', 'stopped')),
    CONSTRAINT valid_tokens CHECK (current_token_usage BETWEEN 0 AND 200000),
    CONSTRAINT valid_process_id CHECK (process_id > 0)
);

-- Indexes
CREATE INDEX idx_instances_project ON active_instances(project_id);
CREATE INDEX idx_instances_heartbeat ON active_instances(last_heartbeat);
CREATE INDEX idx_instances_status ON active_instances(status);

-- Comments
COMMENT ON TABLE active_instances IS 'Tracks all running instances for multi-instance coordination';
COMMENT ON COLUMN active_instances.last_heartbeat IS 'Last heartbeat timestamp for crash detection';
COMMENT ON COLUMN active_instances.current_token_usage IS 'Current token usage (0-200000)';


-- ============================================================================
-- VIEWS
-- ============================================================================

-- View: Project summary with instance count
CREATE VIEW v_project_summary AS
SELECT
    p.project_id,
    p.name,
    p.total_story_points,
    p.completed_story_points,
    COUNT(DISTINCT ai.instance_id) as active_instances,
    COUNT(DISTINCT cs.snapshot_id) as total_snapshots,
    SUM(cs.token_count) as total_tokens,
    p.created_at,
    p.updated_at
FROM projects p
LEFT JOIN active_instances ai ON p.project_id = ai.project_id AND ai.status = 'active'
LEFT JOIN context_snapshots cs ON p.project_id = cs.project_id
GROUP BY p.project_id, p.name, p.total_story_points, p.completed_story_points, p.created_at, p.updated_at;

COMMENT ON VIEW v_project_summary IS 'Summary view of projects with instance and snapshot counts';


-- View: Instance health monitoring
CREATE VIEW v_instance_health AS
SELECT
    ai.instance_id,
    ai.project_id,
    p.name as project_name,
    ai.hostname,
    ai.status,
    ai.current_token_usage,
    ROUND((ai.current_token_usage::float / 200000 * 100)::numeric, 2) as token_usage_percent,
    ai.last_heartbeat,
    EXTRACT(EPOCH FROM (NOW() - ai.last_heartbeat)) as seconds_since_heartbeat,
    CASE
        WHEN EXTRACT(EPOCH FROM (NOW() - ai.last_heartbeat)) > 300 THEN 'stale'
        WHEN EXTRACT(EPOCH FROM (NOW() - ai.last_heartbeat)) > 60 THEN 'warning'
        ELSE 'healthy'
    END as health_status
FROM active_instances ai
JOIN projects p ON ai.project_id = p.project_id;

COMMENT ON VIEW v_instance_health IS 'Health monitoring view for all instances';


-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function: Update project timestamps
CREATE OR REPLACE FUNCTION update_project_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-update project timestamps
CREATE TRIGGER trg_update_project_timestamp
    BEFORE UPDATE ON projects
    FOR EACH ROW
    EXECUTE FUNCTION update_project_timestamp();


-- Function: Cleanup stale instances
CREATE OR REPLACE FUNCTION cleanup_stale_instances(stale_threshold_seconds INTEGER DEFAULT 600)
RETURNS INTEGER AS $$
DECLARE
    affected_rows INTEGER;
BEGIN
    UPDATE active_instances
    SET status = 'crashed'
    WHERE status = 'active'
    AND EXTRACT(EPOCH FROM (NOW() - last_heartbeat)) > stale_threshold_seconds;

    GET DIAGNOSTICS affected_rows = ROW_COUNT;
    RETURN affected_rows;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION cleanup_stale_instances IS 'Marks instances as crashed if no heartbeat received within threshold (default 600s)';


-- Function: Get context for instance
CREATE OR REPLACE FUNCTION get_context_for_instance(
    p_project_id VARCHAR(50),
    p_phase_id INTEGER DEFAULT NULL,
    p_priority VARCHAR(20) DEFAULT NULL
)
RETURNS TABLE (
    snapshot_id INTEGER,
    content_type VARCHAR(50),
    priority VARCHAR(20),
    token_count INTEGER,
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        cs.snapshot_id,
        cs.content_type,
        cs.priority,
        cs.token_count,
        cs.content,
        cs.metadata,
        cs.created_at
    FROM context_snapshots cs
    WHERE cs.project_id = p_project_id
    AND (p_phase_id IS NULL OR cs.phase_id = p_phase_id)
    AND (p_priority IS NULL OR cs.priority = p_priority)
    ORDER BY
        CASE cs.priority
            WHEN 'CRITICAL' THEN 1
            WHEN 'HIGH' THEN 2
            WHEN 'MEDIUM' THEN 3
            WHEN 'LOW' THEN 4
        END,
        cs.sequence_number ASC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_context_for_instance IS 'Retrieves context snapshots for an instance with optional priority filtering';


-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Insert a default example project (can be deleted)
INSERT INTO projects (project_id, name, description, total_story_points)
VALUES ('proj_example_001', 'Example Project', 'This is an example project to demonstrate the database-first architecture', 100);

-- Insert example phase
INSERT INTO phases (project_id, phase_number, name, story_points, status)
VALUES ('proj_example_001', 1, 'Phase 1: Initial Setup', 20, 'completed');

-- Insert example context snapshot
INSERT INTO context_snapshots (project_id, phase_id, sequence_number, content_type, priority, token_count, content)
VALUES (
    'proj_example_001',
    (SELECT phase_id FROM phases WHERE project_id = 'proj_example_001' AND phase_number = 1),
    1,
    'documentation',
    'HIGH',
    50,
    '{"type": "example", "message": "This is an example context snapshot. Real snapshots will contain actual project context."}'
);


-- ============================================================================
-- PERMISSIONS (Optional - for production)
-- ============================================================================

-- Create dedicated user (optional)
-- CREATE USER ultrathink_user WITH PASSWORD 'your_secure_password_here';
-- GRANT CONNECT ON DATABASE ultrathink TO ultrathink_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ultrathink_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ultrathink_user;


-- ============================================================================
-- SCHEMA VERSION TRACKING
-- ============================================================================

CREATE TABLE IF NOT EXISTS schema_version (
    version VARCHAR(10) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT NOW(),
    description TEXT
);

INSERT INTO schema_version (version, description)
VALUES ('1.0.0', 'Initial database-first context management schema');


-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Verification queries
SELECT 'Schema created successfully!' as status;
SELECT COUNT(*) as total_tables FROM information_schema.tables WHERE table_schema = 'public';
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;
