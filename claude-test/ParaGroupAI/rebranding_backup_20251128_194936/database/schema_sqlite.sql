-- ============================================================================
-- DATABASE-FIRST CONTEXT MANAGEMENT SCHEMA (SQLite Version)
-- ============================================================================
--
-- SQLite schema for ULTRATHINK context management
-- Supports multi-project, multi-instance architecture
-- Production-ready with ACID compliance
--
-- Author: ULTRATHINK System
-- Date: 2025-11-19
-- Version: 1.0.0
--
-- Database File: ultrathink_context.db
--
-- ============================================================================

-- Drop existing tables if they exist (for clean reinstall)
DROP TABLE IF EXISTS context_snapshots;
DROP TABLE IF EXISTS active_instances;
DROP TABLE IF EXISTS phases;
DROP TABLE IF EXISTS projects;

-- ============================================================================
-- PROJECTS TABLE
-- ============================================================================

CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    total_story_points INTEGER DEFAULT 0,
    completed_story_points INTEGER DEFAULT 0,
    total_phases INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    metadata TEXT DEFAULT '{}',

    CHECK (total_story_points >= 0),
    CHECK (completed_story_points >= 0),
    CHECK (total_phases > 0),
    CHECK (completed_story_points <= total_story_points)
);

-- Indexes for fast lookups
CREATE INDEX idx_projects_created ON projects(created_at DESC);
CREATE INDEX idx_projects_story_points ON projects(total_story_points);
CREATE INDEX idx_projects_name ON projects(name);


-- ============================================================================
-- PHASES TABLE
-- ============================================================================

CREATE TABLE phases (
    phase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    phase_number INTEGER NOT NULL,
    name TEXT NOT NULL,
    story_points INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending',
    started_at TEXT,
    completed_at TEXT,
    metadata TEXT DEFAULT '{}',

    CHECK (phase_number > 0),
    CHECK (status IN ('pending', 'in_progress', 'completed', 'blocked')),
    CHECK (story_points >= 0),

    UNIQUE(project_id, phase_number)
);

-- Indexes
CREATE INDEX idx_phases_project ON phases(project_id, phase_number);
CREATE INDEX idx_phases_status ON phases(status);


-- ============================================================================
-- CONTEXT SNAPSHOTS TABLE
-- ============================================================================

CREATE TABLE context_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES phases(phase_id) ON DELETE SET NULL,
    sequence_number INTEGER NOT NULL,
    content_type TEXT NOT NULL,
    priority TEXT NOT NULL,
    token_count INTEGER NOT NULL,
    content TEXT NOT NULL,
    metadata TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')),

    CHECK (priority IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
    CHECK (content_type IN ('code', 'config', 'dependency', 'decision', 'architecture', 'test', 'documentation', 'error', 'fix', 'optimization')),
    CHECK (token_count >= 0),
    CHECK (sequence_number > 0)
);

-- Composite indexes for fast retrieval
CREATE INDEX idx_snapshots_project_phase ON context_snapshots(project_id, phase_id);
CREATE INDEX idx_snapshots_priority ON context_snapshots(priority);
CREATE INDEX idx_snapshots_sequence ON context_snapshots(project_id, sequence_number);
CREATE INDEX idx_snapshots_content_type ON context_snapshots(content_type);
CREATE INDEX idx_snapshots_created ON context_snapshots(created_at DESC);


-- ============================================================================
-- ACTIVE INSTANCES TABLE
-- ============================================================================

CREATE TABLE active_instances (
    instance_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    phase_id INTEGER REFERENCES phases(phase_id) ON DELETE SET NULL,
    hostname TEXT,
    process_id INTEGER,
    started_at TEXT DEFAULT (datetime('now')),
    last_heartbeat TEXT DEFAULT (datetime('now')),
    status TEXT NOT NULL DEFAULT 'active',
    current_token_usage INTEGER DEFAULT 0,
    metadata TEXT DEFAULT '{}',

    CHECK (status IN ('active', 'idle', 'crashed', 'stopped')),
    CHECK (current_token_usage BETWEEN 0 AND 200000),
    CHECK (process_id > 0)
);

-- Indexes
CREATE INDEX idx_instances_project ON active_instances(project_id);
CREATE INDEX idx_instances_heartbeat ON active_instances(last_heartbeat);
CREATE INDEX idx_instances_status ON active_instances(status);


-- ============================================================================
-- SCHEMA VERSION TRACKING
-- ============================================================================

CREATE TABLE schema_version (
    version TEXT PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now')),
    description TEXT
);

INSERT INTO schema_version (version, description)
VALUES ('1.0.0', 'Initial SQLite database-first context management schema');


-- ============================================================================
-- INITIAL EXAMPLE DATA
-- ============================================================================

-- Insert a default example project
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
    '{"type": "example", "message": "This is an example context snapshot stored in SQLite. Real snapshots will contain actual project context."}'
);


-- ============================================================================
-- VIEWS (SQLite Compatible)
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


-- View: Instance health monitoring
CREATE VIEW v_instance_health AS
SELECT
    ai.instance_id,
    ai.project_id,
    p.name as project_name,
    ai.hostname,
    ai.status,
    ai.current_token_usage,
    ROUND(CAST(ai.current_token_usage AS REAL) / 200000 * 100, 2) as token_usage_percent,
    ai.last_heartbeat,
    (julianday('now') - julianday(ai.last_heartbeat)) * 86400 as seconds_since_heartbeat,
    CASE
        WHEN (julianday('now') - julianday(ai.last_heartbeat)) * 86400 > 300 THEN 'stale'
        WHEN (julianday('now') - julianday(ai.last_heartbeat)) * 86400 > 60 THEN 'warning'
        ELSE 'healthy'
    END as health_status
FROM active_instances ai
JOIN projects p ON ai.project_id = p.project_id;


-- ============================================================================
-- TRIGGERS (SQLite Compatible)
-- ============================================================================

-- Trigger: Auto-update project timestamps
CREATE TRIGGER trg_update_project_timestamp
    AFTER UPDATE ON projects
    FOR EACH ROW
    BEGIN
        UPDATE projects
        SET updated_at = datetime('now')
        WHERE project_id = NEW.project_id;
    END;


-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Verification
SELECT 'SQLite schema created successfully!' as status;
SELECT COUNT(*) as total_tables FROM sqlite_master WHERE type='table';
SELECT name as table_name FROM sqlite_master WHERE type='table' ORDER BY name;
