#!/usr/bin/env python3
"""
Progress Reporter - Real-time agent status and progress tracking
Usage: python progress_reporter.py [command] [args]

Commands:
    status      - Show current status
    update      - Update agent status
    complete    - Mark task as complete
    fail        - Mark task as failed
    reset       - Reset status
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

# If rich library is missing, use simple output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.panel import Panel
    from rich.live import Live
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
STATUS_FILE = DATA_DIR / "agent-status.json"
QUEUE_FILE = DATA_DIR / "agent-queue.json"

# Status icons
ICONS = {
    "idle": "⏳",
    "running": "🔄",
    "completed": "✅",
    "failed": "❌",
    "blocked": "🔒",
    "waiting": "⌛"
}


def ensure_data_dir():
    """Create data directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_status() -> Dict[str, Any]:
    """Load status file."""
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
    return {
        "session_id": datetime.now().isoformat(),
        "started_at": datetime.now().isoformat(),
        "agents": {},
        "tasks": [],
        "files_created": 0,
        "files_modified": 0,
        "errors": []
    }


def save_status(status: Dict[str, Any]):
    """Save status file."""
    ensure_data_dir()
    status["last_updated"] = datetime.now().isoformat()
    STATUS_FILE.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")


def update_agent(agent_name: str, state: str, task: str = "", progress: int = 0):
    """Update agent status."""
    status = load_status()
    status["agents"][agent_name] = {
        "state": state,
        "task": task,
        "progress": progress,
        "updated_at": datetime.now().isoformat()
    }
    save_status(status)


def add_task(task_id: str, name: str, agent: str, estimated_time: str = ""):
    """Add new task."""
    status = load_status()
    status["tasks"].append({
        "id": task_id,
        "name": name,
        "agent": agent,
        "state": "pending",
        "estimated_time": estimated_time,
        "created_at": datetime.now().isoformat()
    })
    save_status(status)


def complete_task(task_id: str):
    """Complete task."""
    status = load_status()
    for task in status["tasks"]:
        if task["id"] == task_id:
            task["state"] = "completed"
            task["completed_at"] = datetime.now().isoformat()
    save_status(status)


def increment_files(created: int = 0, modified: int = 0):
    """Increment file counter."""
    status = load_status()
    status["files_created"] = status.get("files_created", 0) + created
    status["files_modified"] = status.get("files_modified", 0) + modified
    save_status(status)


def add_error(error_msg: str, agent: str = ""):
    """Add error."""
    status = load_status()
    status["errors"].append({
        "message": error_msg,
        "agent": agent,
        "timestamp": datetime.now().isoformat()
    })
    save_status(status)


def print_status_rich():
    """Display status with Rich formatting."""
    console = Console()
    status = load_status()
    
    # Agent Status Table
    table = Table(title="[bold cyan]Agent Status Board[/]", box=box.ROUNDED)
    table.add_column("Agent", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Task", style="yellow")
    table.add_column("Progress", style="green")
    
    for agent_name, agent_info in status.get("agents", {}).items():
        icon = ICONS.get(agent_info.get("state", "idle"), "❓")
        state = agent_info.get("state", "idle")
        task = agent_info.get("task", "-")
        progress = agent_info.get("progress", 0)
        
        progress_bar = f"[{'█' * (progress // 10)}{'░' * (10 - progress // 10)}] {progress}%"
        
        table.add_row(
            agent_name,
            f"{icon} {state.upper()}",
            task[:40] + "..." if len(task) > 40 else task,
            progress_bar if state == "running" else "-"
        )
    
    console.print(table)
    
    # Summary
    completed = len([t for t in status.get("tasks", []) if t.get("state") == "completed"])
    total = len(status.get("tasks", []))
    files_created = status.get("files_created", 0)
    files_modified = status.get("files_modified", 0)
    errors = len(status.get("errors", []))
    
    console.print()
    console.print(Panel(
        f"[green]✅ Completed:[/] {completed}/{total} tasks\n"
        f"[blue]📁 Files:[/] {files_created} created, {files_modified} modified\n"
        f"[red]❌ Errors:[/] {errors}",
        title="Summary",
        border_style="blue"
    ))


def print_status_simple():
    """Display simple text status."""
    status = load_status()
    
    print("\n=== Agent Status Board ===\n")
    
    for agent_name, agent_info in status.get("agents", {}).items():
        icon = ICONS.get(agent_info.get("state", "idle"), "?")
        state = agent_info.get("state", "idle")
        task = agent_info.get("task", "-")
        progress = agent_info.get("progress", 0)
        
        print(f"{icon} {agent_name}: {state.upper()}")
        if task:
            print(f"   Task: {task}")
        if state == "running":
            print(f"   Progress: {progress}%")
        print()
    
    # Summary
    completed = len([t for t in status.get("tasks", []) if t.get("state") == "completed"])
    total = len(status.get("tasks", []))
    
    print("=== Summary ===")
    print(f"Completed: {completed}/{total} tasks")
    print(f"Files: {status.get('files_created', 0)} created, {status.get('files_modified', 0)} modified")
    print(f"Errors: {len(status.get('errors', []))}")


def print_status():
    """Display status (with Rich if available, otherwise simple)."""
    if RICH_AVAILABLE:
        print_status_rich()
    else:
        print_status_simple()


def reset_status():
    """Reset status."""
    status = {
        "session_id": datetime.now().isoformat(),
        "started_at": datetime.now().isoformat(),
        "agents": {},
        "tasks": [],
        "files_created": 0,
        "files_modified": 0,
        "errors": []
    }
    save_status(status)
    print("Status reset.")


def main():
    """Main function - CLI operations."""
    if len(sys.argv) < 2:
        print_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        print_status()
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: progress_reporter.py update <agent> <state> [task] [progress]")
            return
        agent = sys.argv[2]
        state = sys.argv[3]
        task = sys.argv[4] if len(sys.argv) > 4 else ""
        progress = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        update_agent(agent, state, task, progress)
        print(f"✓ {agent} updated: {state}")
    
    elif command == "task":
        if len(sys.argv) < 5:
            print("Usage: progress_reporter.py task <id> <name> <agent>")
            return
        add_task(sys.argv[2], sys.argv[3], sys.argv[4])
        print(f"✓ Task added: {sys.argv[2]}")
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Usage: progress_reporter.py complete <task_id>")
            return
        complete_task(sys.argv[2])
        print(f"✓ Task completed: {sys.argv[2]}")
    
    elif command == "files":
        created = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        modified = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        increment_files(created, modified)
        print(f"✓ File counter updated: +{created} created, +{modified} modified")
    
    elif command == "error":
        if len(sys.argv) < 3:
            print("Usage: progress_reporter.py error <message> [agent]")
            return
        agent = sys.argv[3] if len(sys.argv) > 3 else ""
        add_error(sys.argv[2], agent)
        print(f"✗ Error recorded")
    
    elif command == "reset":
        reset_status()
    
    elif command == "json":
        status = load_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
