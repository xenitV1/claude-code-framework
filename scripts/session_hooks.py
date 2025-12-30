#!/usr/bin/env python3
"""
Session Hooks - Session start and end management
Unified script for SessionStart and SessionEnd hooks.

Usage:
    python session_hooks.py start [project_path]
    python session_hooks.py end [project_path]
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Debug logging
DEBUG_LOG = Path.home() / ".claude" / "data" / "hook_debug.log"

def debug_log(message: str):
    """Write debug log."""
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] session_hooks.py: {message}\n")
    except Exception as e:
        # If can't write log, write to stderr (fallback)
        sys.stderr.write(f"DEBUG_LOG_ERROR: {e}\n")

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
PROJECTS_DIR = DATA_DIR / "projects"
CURRENT_PROJECT_FILE = DATA_DIR / "current-project.json"
GLOBAL_STATS_FILE = DATA_DIR / "global-stats.json"


def get_project_dir(project_path: str) -> Path:
    """Return data directory for project."""
    project_name = Path(project_path).name
    # Convert project name to safe filename
    safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in project_name)
    return PROJECTS_DIR / safe_name


def ensure_project_data_dir(project_path: str) -> Path:
    """Create and return data directory for project."""
    project_dir = get_project_dir(project_path)
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


def detect_project_type(project_path: str, max_depth: int = 3) -> Dict[str, Any]:
    """Detect project type (with recursive search)."""
    path = Path(project_path)
    analysis = {
        "projectType": None,
        "framework": None,
        "platform": None,
        "detectedAt": None  # Which directory was it detected in
    }
    
    def find_project_files(current_path: Path, depth: int = 0) -> Optional[Dict[str, Any]]:
        """Recursively search for project files."""
        if depth > max_depth:
            return None
            
        # Node.js project
        package_json = current_path / "package.json"
        if package_json.exists():
            try:
                pkg = json.loads(package_json.read_text())
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                
                result = {
                    "projectType": "node",
                    "framework": None,
                    "platform": None,
                    "detectedAt": str(current_path)
                }
                
                if "react-native" in deps or "expo" in deps:
                    result["framework"] = "react-native"
                    result["platform"] = "mobile"
                elif "next" in deps:
                    result["framework"] = "nextjs"
                    result["platform"] = "web"
                elif "react" in deps:
                    result["framework"] = "react"
                    result["platform"] = "web"
                elif "express" in deps:
                    result["framework"] = "express"
                    result["platform"] = "api"
                elif "fastify" in deps:
                    result["framework"] = "fastify"
                    result["platform"] = "api"
                elif "vue" in deps:
                    result["framework"] = "vue"
                    result["platform"] = "web"
                else:
                    result["framework"] = "node"
                    result["platform"] = "general"
                    
                return result
            except:
                pass
        
        # Python project
        if (current_path / "requirements.txt").exists() or (current_path / "pyproject.toml").exists():
            result = {
                "projectType": "python",
                "framework": "python",
                "platform": "general",
                "detectedAt": str(current_path)
            }
            if (current_path / "manage.py").exists():
                result["framework"] = "django"
                result["platform"] = "web"
            elif (current_path / "app.py").exists() or (current_path / "main.py").exists():
                result["framework"] = "flask-or-fastapi"
                result["platform"] = "api"
            return result
        
        # Rust project
        if (current_path / "Cargo.toml").exists():
            return {
                "projectType": "rust",
                "framework": "rust",
                "platform": "general",
                "detectedAt": str(current_path)
            }
        
        # Go project
        if (current_path / "go.mod").exists():
            return {
                "projectType": "go",
                "framework": "go",
                "platform": "general",
                "detectedAt": str(current_path)
            }
        
        # Search in subdirectories
        try:
            for item in current_path.iterdir():
                if item.is_dir() and not item.name.startswith('.') and item.name not in ['node_modules', 'venv', '__pycache__', 'dist', 'build']:
                    result = find_project_files(item, depth + 1)
                    if result:
                        return result
        except PermissionError:
            pass
            
        return None
    
    # Start recursive search
    result = find_project_files(path)
    if result:
        analysis.update(result)
    
    return analysis


def get_recent_errors(project_path: str, limit: int = 3) -> list:
    """Get recent errors for project."""
    project_dir = get_project_dir(project_path)
    error_tracker_file = project_dir / "error-tracker.json"
    
    if not error_tracker_file.exists():
        return []
    
    try:
        tracker = json.loads(error_tracker_file.read_text())
        errors = tracker.get("errors", [])
        
        # Get last N errors
        recent = errors[-limit:] if errors else []
        
        return [
            {
                "type": e.get("errorType"),
                "pattern": e.get("pattern"),
                "solution": e.get("solution")
            }
            for e in recent
        ]
    except:
        return []


def session_start(project_path: str, silent: bool = False):
    """Session start."""
    debug_log(f"SESSION_START called: project_path={project_path}, silent={silent}")

    # Create project-based data directory
    project_dir = ensure_project_data_dir(project_path)

    # Detect project
    analysis = detect_project_type(project_path)
    recent_errors = get_recent_errors(project_path)

    # Create session info
    session_info = {
        "projectPath": project_path,
        "projectName": Path(project_path).name,
        "timestamp": datetime.now().isoformat(),
        "analysis": analysis,
        "recentErrors": recent_errors
    }

    # Save session stats to project directory
    session_stats_file = project_dir / "session-stats.json"
    session_stats_file.write_text(json.dumps(session_info, indent=2, ensure_ascii=False))
    
    # Also save current project reference globally
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CURRENT_PROJECT_FILE.write_text(json.dumps({
        "projectPath": project_path,
        "projectName": Path(project_path).name,
        "dataDir": str(project_dir),
        "lastAccess": datetime.now().isoformat()
    }, indent=2, ensure_ascii=False))

    # Output for Claude
    output = {
        "projectPath": project_path,
        "timestamp": datetime.now().isoformat(),
        "analysis": analysis
    }

    if recent_errors:
        output["recentErrors"] = recent_errors

    sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")

    # Human readable output (only if not silent)
    if not silent:
        if analysis.get("framework"):
            print(f"\n📁 Project: {Path(project_path).name}")
            print(f"🔧 Framework: {analysis['framework']}")
            if analysis.get("platform"):
                print(f"🎯 Platform: {analysis['platform']}")

        if recent_errors:
            print(f"\n⚠️ Recent errors in this project: {len(recent_errors)}")


def session_end(project_path: str, silent: bool = False):
    """Session end."""
    # Project-based data directory
    project_dir = get_project_dir(project_path)
    session_stats_file = project_dir / "session-stats.json"
    error_tracker_file = project_dir / "error-tracker.json"

    # Load current session
    session_stats = {}
    if session_stats_file.exists():
        try:
            session_stats = json.loads(session_stats_file.read_text())
        except:
            pass

    # Calculate session duration
    started_at = session_stats.get("timestamp")
    duration = None
    if started_at:
        try:
            start_time = datetime.fromisoformat(started_at)
            duration = str(datetime.now() - start_time)
        except:
            pass

    # Update tracker with session end
    if error_tracker_file.exists():
        try:
            tracker = json.loads(error_tracker_file.read_text())
            tracker["lastSessionEnd"] = datetime.now().isoformat()
            error_tracker_file.write_text(json.dumps(tracker, indent=2, ensure_ascii=False))
        except:
            pass

    # Output
    output = {
        "timestamp": datetime.now().isoformat(),
        "projectPath": project_path,
        "status": "completed"
    }

    if duration:
        output["duration"] = duration

    sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")

    if not silent:
        print(f"\n✅ Session completed")
        if duration:
            print(f"⏱️ Duration: {duration}")


def main():
    """Main function."""
    debug_log(f"MAIN called: argv={sys.argv}")

    if len(sys.argv) < 2:
        print("Usage: python session_hooks.py [start|end] [--silent] [project_path]")
        sys.exit(1)

    # Check for --silent flag
    silent = "--silent" in sys.argv
    # Remove --silent from args for processing
    args = [a for a in sys.argv if a != "--silent"]

    # args[0] is script name, args[1] is command, args[2] is project path
    command = args[1].lower() if len(args) > 1 else "start"
    project_path = args[2] if len(args) > 2 else os.getcwd()

    debug_log(f"Parsed: command={command}, project_path={project_path}, silent={silent}")

    try:
        if command == "start":
            session_start(project_path, silent=silent)
            debug_log("SESSION_START completed successfully")
        elif command == "end":
            session_end(project_path, silent=silent)
            debug_log("SESSION_END completed successfully")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python session_hooks.py [start|end] [--silent] [project_path]")
            sys.exit(1)
    except Exception as e:
        debug_log(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        debug_log(f"TRACEBACK: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    try:
        # Windows terminal unicode support
        if sys.platform == "win32":
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass
    main()
