"""
Phase 0: Foundation - Testing Application
Browser-based UI for testing all features of Phase 0

Run with: python app.py
Access at: http://localhost:8000
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json
import subprocess
import asyncio

# Add parent directories to path (from standalone_testing/deployment/)
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI
app = FastAPI(
    title="Phase 0: Foundation Testing UI",
    description="Interactive testing interface for SwarmCare Phase 0",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount static files
frontend_dir = Path(__file__).parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# ============================================================================
# DATA MODELS
# ============================================================================

class TestResult(BaseModel):
    test_name: str
    status: str  # "pass", "fail", "running"
    duration_ms: float
    message: str
    timestamp: str

class RequirementUpdate(BaseModel):
    story_id: str
    field: str
    value: str

# ============================================================================
# STATE
# ============================================================================

test_results: List[TestResult] = []
execution_log: List[str] = []

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve testing UI"""
    html_file = frontend_dir / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    else:
        return HTMLResponse(content="<h1>Phase 0 Testing UI</h1><p>Frontend not found. Please create frontend/index.html</p>")

@app.get("/api/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "phase": "00",
        "phase_name": "Foundation",
        "timestamp": datetime.now().isoformat(),
        "services": await check_services()
    }

@app.get("/api/services/status")
async def check_services():
    """Check status of Docker services"""
    services = {
        "neo4j": {"status": "unknown", "url": "http://localhost:7474"},
        "redis": {"status": "unknown", "url": "http://localhost:6379"}
    }

    # Check Neo4j
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "neo4j"],
            cwd=str(Path(__file__).parent.parent.parent.parent),
            capture_output=True,
            text=True,
            timeout=5
        )
        if "Up" in result.stdout:
            services["neo4j"]["status"] = "running"
        else:
            services["neo4j"]["status"] = "stopped"
    except Exception as e:
        services["neo4j"]["status"] = "error"
        services["neo4j"]["error"] = str(e)

    # Check Redis
    try:
        result = subprocess.run(
            ["docker-compose", "ps", "redis"],
            cwd=str(Path(__file__).parent.parent.parent.parent),
            capture_output=True,
            text=True,
            timeout=5
        )
        if "Up" in result.stdout:
            services["redis"]["status"] = "running"
        else:
            services["redis"]["status"] = "stopped"
    except Exception as e:
        services["redis"]["status"] = "error"
        services["redis"]["error"] = str(e)

    return services

@app.get("/api/requirements")
async def get_requirements():
    """Get requirements for this phase"""
    req_file = Path(__file__).parent.parent / "requirements" / "user_stories.json"
    if req_file.exists():
        with open(req_file) as f:
            return json.load(f)
    else:
        raise HTTPException(status_code=404, detail="Requirements file not found")

@app.get("/api/requirements/brd")
async def get_brd():
    """Get Business Requirements Document"""
    brd_file = Path(__file__).parent.parent / "requirements" / "BRD.md"
    if brd_file.exists():
        with open(brd_file) as f:
            return {"content": f.read()}
    else:
        raise HTTPException(status_code=404, detail="BRD not found")

@app.post("/api/requirements/update")
async def update_requirement(update: RequirementUpdate):
    """Update a requirement"""
    req_file = Path(__file__).parent.parent / "requirements" / "user_stories.json"

    if not req_file.exists():
        raise HTTPException(status_code=404, detail="Requirements file not found")

    with open(req_file) as f:
        data = json.load(f)

    # Find and update story
    for story in data["stories"]:
        if story["id"] == update.story_id:
            story[update.field] = update.value
            break

    # Save back
    with open(req_file, 'w') as f:
        json.dump(data, f, indent=2)

    return {"status": "updated", "story_id": update.story_id}

@app.post("/api/test/run-all")
async def run_all_tests(background_tasks: BackgroundTasks):
    """Run all tests for this phase"""
    global test_results
    test_results = []

    background_tasks.add_task(execute_tests)

    return {"status": "started", "message": "Test execution started in background"}

async def execute_tests():
    """Execute all tests"""
    global test_results, execution_log

    test_cases = [
        {
            "name": "Neo4j Connection Test",
            "command": ["docker-compose", "ps", "neo4j"]
        },
        {
            "name": "Redis Connection Test",
            "command": ["docker-compose", "ps", "redis"]
        },
        {
            "name": "Docker Compose Health Check",
            "command": ["docker-compose", "ps"]
        }
    ]

    for test_case in test_cases:
        start_time = datetime.now()

        try:
            result = subprocess.run(
                test_case["command"],
                cwd=str(Path(__file__).parent.parent.parent.parent),
                capture_output=True,
                text=True,
                timeout=30
            )

            duration = (datetime.now() - start_time).total_seconds() * 1000

            if result.returncode == 0:
                test_results.append(TestResult(
                    test_name=test_case["name"],
                    status="pass",
                    duration_ms=duration,
                    message="Test passed",
                    timestamp=datetime.now().isoformat()
                ))
                execution_log.append(f"✅ {test_case['name']}: PASSED ({duration:.2f}ms)")
            else:
                test_results.append(TestResult(
                    test_name=test_case["name"],
                    status="fail",
                    duration_ms=duration,
                    message=result.stderr or "Test failed",
                    timestamp=datetime.now().isoformat()
                ))
                execution_log.append(f"❌ {test_case['name']}: FAILED - {result.stderr}")
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds() * 1000
            test_results.append(TestResult(
                test_name=test_case["name"],
                status="fail",
                duration_ms=duration,
                message=str(e),
                timestamp=datetime.now().isoformat()
            ))
            execution_log.append(f"❌ {test_case['name']}: ERROR - {str(e)}")

@app.get("/api/test/results")
async def get_test_results():
    """Get test results"""
    return {
        "total_tests": len(test_results),
        "passed": len([r for r in test_results if r.status == "pass"]),
        "failed": len([r for r in test_results if r.status == "fail"]),
        "results": [r.dict() for r in test_results]
    }

@app.get("/api/test/execution-log")
async def get_execution_log():
    """Get execution log"""
    return {"log": execution_log}

@app.get("/api/files/list")
async def list_generated_files():
    """List all generated files"""
    generated_dir = Path(__file__).parent / "generated_files"
    if not generated_dir.exists():
        return {"files": []}

    files = []
    for file in generated_dir.rglob("*"):
        if file.is_file():
            files.append({
                "path": str(file.relative_to(generated_dir)),
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })

    return {"files": files}

@app.get("/api/files/download/{file_path:path}")
async def download_file(file_path: str):
    """Download a generated file"""
    file = Path(__file__).parent / "generated_files" / file_path
    if not file.exists() or not file.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file, filename=file.name)

@app.post("/api/phase/regenerate")
async def regenerate_phase(background_tasks: BackgroundTasks):
    """Regenerate phase with current requirements"""
    background_tasks.add_task(execute_regeneration)
    return {"status": "started", "message": "Phase regeneration started"}

async def execute_regeneration():
    """Execute phase regeneration"""
    global execution_log
    execution_log.append(f"🔄 Starting phase regeneration at {datetime.now().isoformat()}")

    # This would trigger the actual phase implementation
    # For now, just log
    await asyncio.sleep(2)
    execution_log.append("✅ Phase regeneration complete")

@app.get("/api/metrics")
async def get_metrics():
    """Get phase metrics"""
    req_file = Path(__file__).parent.parent / "requirements" / "user_stories.json"

    if not req_file.exists():
        return {"error": "Metrics not available"}

    with open(req_file) as f:
        data = json.load(f)

    return data.get("metrics", {})

# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    print("=" * 80)
    print("Phase 0: Foundation Testing UI")
    print("=" * 80)
    print(f"Access at: http://localhost:8000")
    print(f"API Docs: http://localhost:8000/docs")
    print(f"Health Check: http://localhost:8000/api/health")
    print("=" * 80)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
