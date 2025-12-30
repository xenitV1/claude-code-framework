#!/usr/bin/env python3
"""
Pre-Bash Hook - Terminal Error Learning System
Runs BEFORE every terminal command and learns from past errors.

Usage: python pre_bash.py "<command>" [project_path]
"""

import json
import sys
import re
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
ERROR_DB_FILE = DATA_DIR / "error-database.json"

# Rich support (optional)
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich import box
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False


def ensure_data_dir():
    """Create data directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def initialize_error_database():
    """Create error database if it doesn't exist."""
    if not ERROR_DB_FILE.exists():
        initial_db = {
            "version": "1.0",
            "errors": [],
            "lastUpdated": datetime.now().isoformat()
        }
        ensure_data_dir()
        ERROR_DB_FILE.write_text(json.dumps(initial_db, indent=2, ensure_ascii=False), encoding="utf-8")


def load_error_database() -> Dict[str, Any]:
    """Load error database."""
    initialize_error_database()
    try:
        return json.loads(ERROR_DB_FILE.read_text(encoding="utf-8-sig"))
    except:
        return json.loads(ERROR_DB_FILE.read_text(encoding="utf-8"))


def normalize_command(cmd: str) -> str:
    """Normalize command for pattern matching."""
    normalized = cmd
    
    # Package names
    normalized = re.sub(r'npm install\s+[\w@/-]+', 'npm install {package}', normalized)
    normalized = re.sub(r'npm i\s+[\w@/-]+', 'npm install {package}', normalized)
    normalized = re.sub(r'yarn add\s+[\w@/-]+', 'yarn add {package}', normalized)
    normalized = re.sub(r'pip install\s+[\w-]+', 'pip install {package}', normalized)
    
    # Git commands
    normalized = re.sub(r'git push\s+\w+\s+\w+', 'git push {remote} {branch}', normalized)
    normalized = re.sub(r'git checkout\s+[\w/-]+', 'git checkout {branch}', normalized)
    normalized = re.sub(r'git merge\s+[\w/-]+', 'git merge {branch}', normalized)
    
    # File paths
    normalized = re.sub(r'[A-Za-z]:\\[\w\\/.-]+', '{path}', normalized)
    normalized = re.sub(r'/[\w/.-]+', '{path}', normalized)
    
    # Port numbers
    normalized = re.sub(r':\d{4,5}', ':{port}', normalized)
    normalized = re.sub(r'port\s+\d+', 'port {port}', normalized)
    
    # Localhost
    normalized = re.sub(r'localhost', '{host}', normalized)
    normalized = re.sub(r'127\.0\.0\.1', '{host}', normalized)
    
    return normalized.strip()


def calculate_similarity(str1: str, str2: str) -> int:
    """Calculate similarity between two strings."""
    words1 = set(str1.lower().split())
    words2 = set(str2.lower().split())
    
    if not words1 or not words2:
        return 0
    
    common = len(words1 & words2)
    total = max(len(words1), len(words2))
    
    return round((common / total) * 100)


def find_similar_errors(cmd: str, normalized_cmd: str, project: str, errors: List[Dict]) -> List[Dict]:
    """Find similar errors."""
    similar_errors = []
    
    for error in errors:
        similarity = 0
        match_type = ""
        
        # Exact command match
        if error.get("command") == cmd:
            similarity = 100
            match_type = "EXACT_COMMAND"
        # Exact pattern match
        elif error.get("pattern") == normalized_cmd:
            similarity = 95
            match_type = "EXACT_PATTERN"
        # High similarity pattern match
        else:
            pattern_similarity = calculate_similarity(error.get("pattern", ""), normalized_cmd)
            if pattern_similarity >= 80:
                similarity = pattern_similarity
                match_type = "PATTERN_MATCH"
        
        # Project-specific boost
        if error.get("project") == project and similarity > 0:
            similarity = min(100, similarity + 5)
            match_type += "_PROJECT"
        
        if similarity >= 80:
            similar_errors.append({
                "error": error,
                "similarity": similarity,
                "matchType": match_type
            })
    
    # Sort by similarity
    return sorted(similar_errors, key=lambda x: x["similarity"], reverse=True)


def print_warnings_rich(similar_errors: List[Dict], command: str):
    """Display warnings with Rich formatting."""
    console.print()
    console.print(Panel(
        "[bold cyan]TERMINAL ERROR LEARNING SYSTEM[/]",
        box=box.DOUBLE
    ))
    
    for match in similar_errors:
        err = match["error"]
        similarity = match["similarity"]
        
        status = err.get("status", "pending")
        status_icon = {"solved": "✅", "recurring": "⚠️"}.get(status, "🔴")
        
        error_msg = err.get("errorMessage", "")[:100]
        if len(err.get("errorMessage", "")) > 100:
            error_msg += "..."
        
        console.print()
        console.print(f"{status_icon} [bold red]LEARNED ERROR[/] (Similarity: {similarity}%)")
        console.print(f"   Command: [yellow]{err.get('command', 'N/A')}[/]")
        console.print(f"   Error: [red]{error_msg}[/]")
        console.print(f"   Occurrences: {err.get('occurrences', 1)}")
        
        if err.get("solution") and status == "solved":
            console.print()
            console.print(f"[green]✅ SOLUTION: {err['solution']}[/]")
        
        if status == "recurring":
            console.print()
            console.print("[yellow]⚠️ WARNING: This error keeps recurring! Consider a different approach.[/]")
    
    console.print()
    console.print(f"[dim]Consider this learned experience before proceeding with: {command}[/]")
    console.print()


def print_warnings_simple(similar_errors: List[Dict], command: str):
    """Display warnings with simple text."""
    print()
    print("=" * 64)
    print("  [*] TERMINAL ERROR LEARNING SYSTEM")
    print("=" * 64)
    
    for match in similar_errors:
        err = match["error"]
        similarity = match["similarity"]
        
        status = err.get("status", "pending")
        status_icon = {"solved": "[+]", "recurring": "[!]"}.get(status, "[*]")
        
        error_msg = err.get("errorMessage", "")[:100]
        if len(err.get("errorMessage", "")) > 100:
            error_msg += "..."
        
        print()
        print(f"{status_icon} [LEARNED ERROR] (Similarity: {similarity}%)")
        print(f"  Command: {err.get('command', 'N/A')}")
        print(f"  Error: {error_msg}")
        print(f"  Occurrences: {err.get('occurrences', 1)}")
        
        if err.get("solution") and status == "solved":
            print()
            print(f"[+] SOLUTION: {err['solution']}")
        
        if status == "recurring":
            print()
            print("[!] WARNING: This error keeps recurring! Consider a different approach.")
    
    print()
    print("-" * 64)
    print(f"Consider this learned experience before proceeding with: {command}")
    print()


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python pre_bash.py \"<command>\" [project_path]")
        sys.exit(0)
    
    command = sys.argv[1]
    project_path = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    
    try:
        # Load error database
        error_db = load_error_database()
        errors = error_db.get("errors", [])
        
        # Normalize command
        normalized_cmd = normalize_command(command)
        
        # Find similar errors
        similar_errors = find_similar_errors(command, normalized_cmd, project_path, errors)
        
        # Print warnings if found
        if similar_errors:
            if RICH_AVAILABLE:
                print_warnings_rich(similar_errors, command)
            else:
                print_warnings_simple(similar_errors, command)
        
        # Always allow command to proceed
        sys.exit(0)
        
    except Exception as e:
        # Don't block commands if error learning fails
        print(f"Pre-bash hook warning: {e}", file=sys.stderr)
        sys.exit(0)


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
