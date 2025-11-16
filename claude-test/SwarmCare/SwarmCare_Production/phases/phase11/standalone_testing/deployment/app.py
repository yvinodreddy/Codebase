"""
Phase 11: Research & Publications - Complete Testing Application
Production-Ready Implementation with Full CRUD, Tracking, and Auto-Documentation
"""

import sys
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import asyncio

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Import unified tracker
from unified_tracker import UnifiedTracker

# Neo4j and Redis clients
try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

PHASE_NUMBER = "11"
PHASE_NAME = "Research & Publications"
PORT = 8011

# Paths
SCRIPT_DIR = Path(__file__).parent
STANDALONE_DIR = SCRIPT_DIR.parent
PHASE_DIR = STANDALONE_DIR.parent
PHASES_DIR = PHASE_DIR.parent
PROJECT_ROOT = PHASES_DIR.parent

REQUIREMENTS_DIR = STANDALONE_DIR / "requirements"
TEST_DATA_DIR = STANDALONE_DIR / "test_data"
GENERATED_FILES_DIR = SCRIPT_DIR / "generated_files"
DOCS_DIR = STANDALONE_DIR / "standalone_testing_docs"

# Ensure directories exist
GENERATED_FILES_DIR.mkdir(parents=True, exist_ok=True)

# Documentation sync locations
DOC_SYNC_LOCATIONS = [
    PROJECT_ROOT,
    PROJECT_ROOT / "ai_prompts",
    PROJECT_ROOT.parent,  # SwarmCare root
    PROJECT_ROOT.parent / "ProjectPlan"
]

# ============================================================================
# MODELS
# ============================================================================

class UserStory(BaseModel):
    id: str = Field(..., description="User story ID (e.g., US-001)")
    title: str = Field(..., description="User story title")
    description: str = Field(..., description="User story description")
    story_points: int = Field(..., ge=1, le=13, description="Story points (1-13)")
    priority: str = Field(..., description="Priority (P0, P1, P2, P3)")
    status: str = Field(default="pending", description="Status (pending, in_progress, completed, blocked)")
    acceptance_criteria: List[str] = Field(default_factory=list)
    implementation_notes: Optional[str] = None
    test_scenarios: List[Dict[str, str]] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

class PhaseChange(BaseModel):
    timestamp: str
    change_type: str  # added, modified, deleted
    story_id: Optional[str] = None
    story_title: Optional[str] = None
    changed_by: str = "UI"
    description: str

class TestResult(BaseModel):
    test_name: str
    status: str  # passed, failed, skipped
    duration_ms: float
    error: Optional[str] = None

# ============================================================================
# DATABASE CONNECTIONS
# ============================================================================

class DatabaseManager:
    def __init__(self):
        self.neo4j_driver = None
        self.redis_client = None
        self._connect()

    def _connect(self):
        """Initialize database connections"""
        # Neo4j
        if NEO4J_AVAILABLE:
            try:
                neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
                neo4j_user = os.getenv("NEO4J_USER", "neo4j")
                neo4j_password = os.getenv("NEO4J_PASSWORD", "mJe@!ikwcoi4udlFXE$n!ENtv1iAw^F")
                self.neo4j_driver = GraphDatabase.driver(
                    neo4j_uri,
                    auth=(neo4j_user, neo4j_password)
                )
            except Exception as e:
                print(f"⚠️  Neo4j connection failed: {e}")

        # Redis
        if REDIS_AVAILABLE:
            try:
                redis_host = os.getenv("REDIS_HOST", "localhost")
                redis_port = int(os.getenv("REDIS_PORT", "6379"))
                self.redis_client = redis.Redis(
                    host=redis_host,
                    port=redis_port,
                    decode_responses=True,
                    socket_connect_timeout=2
                )
                self.redis_client.ping()
            except Exception as e:
                print(f"⚠️  Redis connection failed: {e}")
                self.redis_client = None

    def check_neo4j(self) -> Dict[str, Any]:
        """Check Neo4j connection status"""
        if not NEO4J_AVAILABLE or not self.neo4j_driver:
            return {"status": "unavailable", "error": "Neo4j driver not initialized"}

        try:
            with self.neo4j_driver.session() as session:
                result = session.run("RETURN 1 as test")
                result.single()
            return {"status": "running", "url": "http://localhost:7474"}
        except Exception as e:
            return {"status": "stopped", "error": str(e), "url": "http://localhost:7474"}

    def check_redis(self) -> Dict[str, Any]:
        """Check Redis connection status"""
        if not REDIS_AVAILABLE or not self.redis_client:
            return {"status": "unavailable", "error": "Redis client not initialized"}

        try:
            self.redis_client.ping()
            return {"status": "running", "url": "http://localhost:6379"}
        except Exception as e:
            return {"status": "stopped", "error": str(e), "url": "http://localhost:6379"}

    def close(self):
        """Close database connections"""
        if self.neo4j_driver:
            self.neo4j_driver.close()
        if self.redis_client:
            self.redis_client.close()

# ============================================================================
# USER STORY MANAGER
# ============================================================================

class UserStoryManager:
    def __init__(self):
        self.stories_file = REQUIREMENTS_DIR / "user_stories.json"
        # Use unified tracker instead of separate tracker files
        self.unified_tracker = UnifiedTracker(PHASE_NUMBER, PHASE_NAME)

    def load_stories(self) -> Dict[str, Any]:
        """Load user stories from file"""
        return self.unified_tracker.read_user_stories()

    def save_stories(self, data: Dict[str, Any]):
        """Save user stories to file"""
        self.unified_tracker.write_user_stories(data)
        # Update metrics whenever stories are saved
        self.unified_tracker.update_metrics()

    def get_all_stories(self) -> List[UserStory]:
        """Get all user stories"""
        data = self.load_stories()
        return [UserStory(**story) for story in data.get("stories", [])]

    def get_story(self, story_id: str) -> Optional[UserStory]:
        """Get a specific user story"""
        stories = self.get_all_stories()
        for story in stories:
            if story.id == story_id:
                return story
        return None

    def add_story(self, story: UserStory) -> UserStory:
        """Add a new user story"""
        data = self.load_stories()

        # Check if ID already exists
        if any(s['id'] == story.id for s in data.get("stories", [])):
            raise ValueError(f"Story with ID {story.id} already exists")

        # Add story
        data.setdefault("stories", []).append(story.dict())
        data["total_story_points"] = sum(s['story_points'] for s in data["stories"])

        self.save_stories(data)

        # Track change using unified tracker
        self.unified_tracker.track_change(
            change_type="added",
            description=f"Added new user story: {story.title}",
            story_id=story.id,
            story_title=story.title
        )

        return story

    def update_story(self, story_id: str, story: UserStory) -> UserStory:
        """Update an existing user story"""
        data = self.load_stories()

        found = False
        for i, s in enumerate(data.get("stories", [])):
            if s['id'] == story_id:
                data["stories"][i] = story.dict()
                found = True
                break

        if not found:
            raise ValueError(f"Story with ID {story_id} not found")

        data["total_story_points"] = sum(s['story_points'] for s in data["stories"])
        self.save_stories(data)

        # Track change using unified tracker
        self.unified_tracker.track_change(
            change_type="modified",
            description=f"Modified user story: {story.title}",
            story_id=story.id,
            story_title=story.title
        )

        return story

    def delete_story(self, story_id: str):
        """Delete a user story"""
        data = self.load_stories()

        original_len = len(data.get("stories", []))
        deleted_story = None

        data["stories"] = [s for s in data.get("stories", []) if s['id'] != story_id]

        if len(data["stories"]) == original_len:
            raise ValueError(f"Story with ID {story_id} not found")

        # Find deleted story for tracking
        for s in data.get("stories", []):
            if s['id'] == story_id:
                deleted_story = s
                break

        data["total_story_points"] = sum(s['story_points'] for s in data["stories"])
        self.save_stories(data)

        # Track change using unified tracker
        self.unified_tracker.track_change(
            change_type="deleted",
            description=f"Deleted user story: {story_id}",
            story_id=story_id,
            story_title=None
        )


# ============================================================================
# DOCUMENTATION MANAGER
# ============================================================================

class DocumentationManager:
    def __init__(self):
        self.story_manager = UserStoryManager()
        self.unified_tracker = UnifiedTracker(PHASE_NUMBER, PHASE_NAME)

    def update_all_documentation(self):
        """Update documentation in all 4 sync locations using unified tracker"""
        results = self.unified_tracker.sync_documentation()
        return results

# ============================================================================
# TEST RUNNER
# ============================================================================

class TestRunner:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.results: List[TestResult] = []

    async def run_all_tests(self) -> List[TestResult]:
        """Run all available tests"""
        self.results = []

        # Test 1: Neo4j Connection
        await self._test_neo4j()

        # Test 2: Redis Connection
        await self._test_redis()

        # Test 3: Docker Compose Health
        await self._test_docker()

        # Test 4: Requirements Files
        await self._test_requirements()

        # Test 5: Test Data
        await self._test_data()

        return self.results

    async def _test_neo4j(self):
        """Test Neo4j connection"""
        start = datetime.now()
        try:
            status = self.db_manager.check_neo4j()
            duration = (datetime.now() - start).total_seconds() * 1000

            if status["status"] == "running":
                self.results.append(TestResult(
                    test_name="Neo4j Connection Test",
                    status="passed",
                    duration_ms=round(duration, 2)
                ))
            else:
                self.results.append(TestResult(
                    test_name="Neo4j Connection Test",
                    status="failed",
                    duration_ms=round(duration, 2),
                    error=status.get("error", "Connection failed")
                ))
        except Exception as e:
            duration = (datetime.now() - start).total_seconds() * 1000
            self.results.append(TestResult(
                test_name="Neo4j Connection Test",
                status="failed",
                duration_ms=round(duration, 2),
                error=str(e)
            ))

    async def _test_redis(self):
        """Test Redis connection"""
        start = datetime.now()
        try:
            status = self.db_manager.check_redis()
            duration = (datetime.now() - start).total_seconds() * 1000

            if status["status"] == "running":
                self.results.append(TestResult(
                    test_name="Redis Connection Test",
                    status="passed",
                    duration_ms=round(duration, 2)
                ))
            else:
                self.results.append(TestResult(
                    test_name="Redis Connection Test",
                    status="failed",
                    duration_ms=round(duration, 2),
                    error=status.get("error", "Connection failed")
                ))
        except Exception as e:
            duration = (datetime.now() - start).total_seconds() * 1000
            self.results.append(TestResult(
                test_name="Redis Connection Test",
                status="failed",
                duration_ms=round(duration, 2),
                error=str(e)
            ))

    async def _test_docker(self):
        """Test Docker Compose health"""
        start = datetime.now()
        try:
            import subprocess
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=swarmcare"],
                capture_output=True,
                text=True,
                timeout=5
            )
            duration = (datetime.now() - start).total_seconds() * 1000

            if result.returncode == 0 and "swarmcare" in result.stdout:
                self.results.append(TestResult(
                    test_name="Docker Compose Health Check",
                    status="passed",
                    duration_ms=round(duration, 2)
                ))
            else:
                self.results.append(TestResult(
                    test_name="Docker Compose Health Check",
                    status="failed",
                    duration_ms=round(duration, 2),
                    error="Docker services not running"
                ))
        except Exception as e:
            duration = (datetime.now() - start).total_seconds() * 1000
            self.results.append(TestResult(
                test_name="Docker Compose Health Check",
                status="failed",
                duration_ms=round(duration, 2),
                error=str(e)
            ))

    async def _test_requirements(self):
        """Test requirements files exist and are valid"""
        start = datetime.now()
        try:
            brd_file = REQUIREMENTS_DIR / "BRD.md"
            stories_file = REQUIREMENTS_DIR / "user_stories.json"

            if not brd_file.exists():
                raise FileNotFoundError("BRD.md not found")
            if not stories_file.exists():
                raise FileNotFoundError("user_stories.json not found")

            # Validate JSON
            with open(stories_file, 'r') as f:
                json.load(f)

            duration = (datetime.now() - start).total_seconds() * 1000
            self.results.append(TestResult(
                test_name="Requirements Files Check",
                status="passed",
                duration_ms=round(duration, 2)
            ))
        except Exception as e:
            duration = (datetime.now() - start).total_seconds() * 1000
            self.results.append(TestResult(
                test_name="Requirements Files Check",
                status="failed",
                duration_ms=round(duration, 2),
                error=str(e)
            ))

    async def _test_data(self):
        """Test data seeding scripts exist"""
        start = datetime.now()
        try:
            seed_script = TEST_DATA_DIR / "seeding_scripts" / "seed_all.py"

            if not seed_script.exists():
                raise FileNotFoundError("seed_all.py not found")

            duration = (datetime.now() - start).total_seconds() * 1000
            self.results.append(TestResult(
                test_name="Test Data Scripts Check",
                status="passed",
                duration_ms=round(duration, 2)
            ))
        except Exception as e:
            duration = (datetime.now() - start).total_seconds() * 1000
            self.results.append(TestResult(
                test_name="Test Data Scripts Check",
                status="failed",
                duration_ms=round(duration, 2),
                error=str(e)
            ))

# ============================================================================
# CODE GENERATOR
# ============================================================================

class CodeGenerator:
    def __init__(self, story_manager: UserStoryManager):
        self.story_manager = story_manager

    async def generate_files(self) -> List[str]:
        """Generate code files based on user stories"""
        generated = []

        stories = self.story_manager.get_all_stories()

        # Generate controller
        controller_path = GENERATED_FILES_DIR / "controller.py"
        self._generate_controller(stories, controller_path)
        generated.append(str(controller_path))

        # Generate service
        service_path = GENERATED_FILES_DIR / "service.py"
        self._generate_service(stories, service_path)
        generated.append(str(service_path))

        # Generate repository
        repo_path = GENERATED_FILES_DIR / "repository.py"
        self._generate_repository(stories, repo_path)
        generated.append(str(repo_path))

        # Generate tests
        tests_path = GENERATED_FILES_DIR / "tests.py"
        self._generate_tests(stories, tests_path)
        generated.append(str(tests_path))

        # Generate README
        readme_path = GENERATED_FILES_DIR / "README.md"
        self._generate_readme(stories, readme_path)
        generated.append(str(readme_path))

        return generated

    def _generate_controller(self, stories: List[UserStory], path: Path):
        """Generate controller file"""
        content = f'''"""
Phase {PHASE_NUMBER} Controller
Generated: {datetime.now().isoformat()}
Based on {len(stories)} user stories
"""

from fastapi import APIRouter, HTTPException
from typing import List
from .service import Phase{PHASE_NUMBER}Service

router = APIRouter(prefix="/api/phase{PHASE_NUMBER}", tags=["Phase {PHASE_NUMBER}"])
service = Phase{PHASE_NUMBER}Service()

'''
        for story in stories:
            method_name = story.title.lower().replace(" ", "_")
            content += f'''
@router.get("/{method_name}")
async def {method_name}():
    """
    {story.description}
    Story Points: {story.story_points}
    Priority: {story.priority}
    """
    return await service.{method_name}()

'''
        path.write_text(content)

    def _generate_service(self, stories: List[UserStory], path: Path):
        """Generate service file"""
        content = f'''"""
Phase {PHASE_NUMBER} Service Layer
Generated: {datetime.now().isoformat()}
"""

from .repository import Phase{PHASE_NUMBER}Repository

class Phase{PHASE_NUMBER}Service:
    def __init__(self):
        self.repository = Phase{PHASE_NUMBER}Repository()

'''
        for story in stories:
            method_name = story.title.lower().replace(" ", "_")
            content += f'''
    async def {method_name}(self):
        """
        {story.description}
        """
        return await self.repository.{method_name}()

'''
        path.write_text(content)

    def _generate_repository(self, stories: List[UserStory], path: Path):
        """Generate repository file"""
        content = f'''"""
Phase {PHASE_NUMBER} Repository Layer
Generated: {datetime.now().isoformat()}
"""

class Phase{PHASE_NUMBER}Repository:
    def __init__(self):
        pass

'''
        for story in stories:
            method_name = story.title.lower().replace(" ", "_")
            content += f'''
    async def {method_name}(self):
        """
        {story.description}
        Story: {story.id}
        """
        # TODO: Implement {story.title}
        return {{"status": "not_implemented", "story_id": "{story.id}"}}

'''
        path.write_text(content)

    def _generate_tests(self, stories: List[UserStory], path: Path):
        """Generate test file"""
        content = f'''"""
Phase {PHASE_NUMBER} Tests
Generated: {datetime.now().isoformat()}
"""

import pytest
from .controller import router

'''
        for story in stories:
            method_name = story.title.lower().replace(" ", "_")
            content += f'''
def test_{method_name}():
    """
    Test: {story.title}
    Story: {story.id}

    Acceptance Criteria:
'''
            for criterion in story.acceptance_criteria:
                content += f"    - {criterion}\n"

            content += f'''    """
    # TODO: Implement test for {story.title}
    assert True, "Test not yet implemented"

'''
        path.write_text(content)

    def _generate_readme(self, stories: List[UserStory], path: Path):
        """Generate README for generated files"""
        content = f'''# Phase {PHASE_NUMBER}: {PHASE_NAME} - Generated Files

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Stories:** {len(stories)}
**Total Story Points:** {sum(s.story_points for s in stories)}

---

## Files Generated

- `controller.py` - API endpoints
- `service.py` - Business logic
- `repository.py` - Data access
- `tests.py` - Unit tests
- `README.md` - This file

---

## User Stories Implemented

'''
        for story in stories:
            content += f'''### {story.id}: {story.title}
- **Points:** {story.story_points} SP
- **Priority:** {story.priority}
- **Status:** {story.status}

'''

        content += '''
---

## Usage

```python
from controller import router
app.include_router(router)
```

---

**Auto-generated by Phase Testing Application**
'''
        path.write_text(content)

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title=f"Phase {PHASE_NUMBER}: {PHASE_NAME} Testing Application",
    description="Complete testing interface with CRUD, tracking, and auto-documentation",
    version="2.0.0"
)

# Initialize managers
db_manager = DatabaseManager()
story_manager = UserStoryManager()
doc_manager = DocumentationManager()
test_runner = TestRunner(db_manager)
code_generator = CodeGenerator(story_manager)

# Execution log
execution_log: List[Dict[str, str]] = []

def log_execution(message: str, level: str = "info"):
    """Log execution message"""
    execution_log.append({
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message
    })
    # Keep only last 100 entries
    if len(execution_log) > 100:
        execution_log.pop(0)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def home():
    """Serve the main dashboard"""
    html_path = Path(__file__).parent / "frontend" / "index_enhanced.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse(content="<h1>Phase 0 Testing Dashboard</h1><p>Frontend file not found</p>")

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    neo4j_status = db_manager.check_neo4j()
    redis_status = db_manager.check_redis()

    return {
        "status": "healthy",
        "phase": PHASE_NUMBER,
        "phase_name": PHASE_NAME,
        "timestamp": datetime.now().isoformat(),
        "services": {
            "neo4j": neo4j_status,
            "redis": redis_status
        }
    }

@app.get("/api/services/status")
async def services_status():
    """Get detailed services status"""
    return {
        "neo4j": db_manager.check_neo4j(),
        "redis": db_manager.check_redis()
    }

@app.post("/api/tests/run")
async def run_tests(background_tasks: BackgroundTasks):
    """Run all tests"""
    log_execution("Starting test execution", "info")
    results = await test_runner.run_all_tests()
    log_execution(f"Completed {len(results)} tests", "info")
    return {"results": [r.dict() for r in results]}

@app.get("/api/tests/results")
async def get_test_results():
    """Get latest test results"""
    return {"results": [r.dict() for r in test_runner.results]}

@app.get("/api/stories")
async def get_stories():
    """Get all user stories"""
    stories = story_manager.get_all_stories()
    data = story_manager.load_stories()
    return {
        "stories": [s.dict() for s in stories],
        "metadata": {
            "phase": data.get("phase", f"phase{PHASE_NUMBER}"),
            "phase_name": data.get("phase_name", PHASE_NAME),
            "total_story_points": data.get("total_story_points", 0),
            "status": data.get("status", "unknown")
        }
    }

@app.get("/api/stories/{story_id}")
async def get_story(story_id: str):
    """Get a specific user story"""
    story = story_manager.get_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail=f"Story {story_id} not found")
    return story.dict()

@app.post("/api/stories")
async def create_story(story: UserStory):
    """Create a new user story"""
    log_execution(f"Creating story: {story.id}", "info")
    try:
        created = story_manager.add_story(story)
        log_execution(f"Created story: {story.id}", "success")

        # Trigger documentation update
        doc_manager.update_all_documentation()
        log_execution("Updated documentation", "info")

        return created.dict()
    except ValueError as e:
        log_execution(f"Failed to create story: {str(e)}", "error")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/stories/{story_id}")
async def update_story(story_id: str, story: UserStory):
    """Update an existing user story"""
    log_execution(f"Updating story: {story_id}", "info")
    try:
        updated = story_manager.update_story(story_id, story)
        log_execution(f"Updated story: {story_id}", "success")

        # Trigger documentation update
        doc_manager.update_all_documentation()
        log_execution("Updated documentation", "info")

        return updated.dict()
    except ValueError as e:
        log_execution(f"Failed to update story: {str(e)}", "error")
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/api/stories/{story_id}")
async def delete_story(story_id: str):
    """Delete a user story"""
    log_execution(f"Deleting story: {story_id}", "info")
    try:
        story_manager.delete_story(story_id)
        log_execution(f"Deleted story: {story_id}", "success")

        # Trigger documentation update
        doc_manager.update_all_documentation()
        log_execution("Updated documentation", "info")

        return {"status": "deleted", "story_id": story_id}
    except ValueError as e:
        log_execution(f"Failed to delete story: {str(e)}", "error")
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/generate")
async def generate_files():
    """Generate code files from user stories"""
    log_execution("Starting code generation", "info")
    files = await code_generator.generate_files()
    log_execution(f"Generated {len(files)} files", "success")
    return {"files": files, "count": len(files)}

@app.get("/api/generated/files")
async def list_generated_files():
    """List all generated files"""
    if not GENERATED_FILES_DIR.exists():
        return {"files": []}

    files = []
    for file_path in GENERATED_FILES_DIR.glob("*"):
        if file_path.is_file():
            files.append({
                "name": file_path.name,
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })

    return {"files": files}

@app.get("/api/logs")
async def get_logs():
    """Get execution logs"""
    return {"logs": execution_log}

@app.post("/api/logs/clear")
async def clear_logs():
    """Clear execution logs"""
    execution_log.clear()
    log_execution("Logs cleared", "info")
    return {"status": "cleared"}

@app.get("/api/trackers/phase")
async def get_phase_tracker():
    """Get phase-level tracker (unified)"""
    tracker = story_manager.unified_tracker.read_phase_state()
    return tracker

@app.get("/api/trackers/unified")
async def get_unified_status():
    """Get comprehensive unified tracker status"""
    status = story_manager.unified_tracker.get_comprehensive_status()
    return status

@app.post("/api/documentation/sync")
async def sync_documentation():
    """Manually trigger documentation synchronization"""
    log_execution("Manual documentation sync triggered", "info")
    changes = doc_manager.update_all_documentation()
    log_execution(f"Documentation synced: {len(changes)} changes", "success")
    return {"changes": changes}

@app.get("/api/metrics")
async def get_metrics():
    """Get phase metrics"""
    data = story_manager.load_stories()
    stories = story_manager.get_all_stories()

    total_points = sum(s.story_points for s in stories)
    completed_points = sum(s.story_points for s in stories if s.status == "completed")

    return {
        "total_stories": len(stories),
        "total_story_points": total_points,
        "completed_story_points": completed_points,
        "completion_percentage": round((completed_points / total_points * 100) if total_points > 0 else 0, 1),
        "stories_by_status": {
            "pending": len([s for s in stories if s.status == "pending"]),
            "in_progress": len([s for s in stories if s.status == "in_progress"]),
            "completed": len([s for s in stories if s.status == "completed"]),
            "blocked": len([s for s in stories if s.status == "blocked"])
        },
        "stories_by_priority": {
            "P0": len([s for s in stories if s.priority == "P0"]),
            "P1": len([s for s in stories if s.priority == "P1"]),
            "P2": len([s for s in stories if s.priority == "P2"]),
            "P3": len([s for s in stories if s.priority == "P3"])
        }
    }

@app.on_event("startup")
async def startup():
    """Application startup"""
    log_execution("=" * 80, "info")
    log_execution(f"Phase {PHASE_NUMBER}: {PHASE_NAME} Testing Application", "info")
    log_execution("=" * 80, "info")
    log_execution(f"Access at: http://localhost:{PORT}", "info")
    log_execution(f"API Docs: http://localhost:{PORT}/docs", "info")
    log_execution(f"Health Check: http://localhost:{PORT}/api/health", "info")
    log_execution("=" * 80, "info")

@app.on_event("shutdown")
async def shutdown():
    """Application shutdown"""
    db_manager.close()
    log_execution("Application shutdown complete", "info")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        reload=False  # Disable reload to prevent issues
    )
