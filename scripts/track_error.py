#!/usr/bin/env python3
"""
Track Error - Error logging and solution suggestion system
Runs as PostToolUse hook.

Usage: python track_error.py "<command>" "<exit_code>" "<output>" [project_path]
"""

import json
import sys
import re
import os
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
ERROR_DB_FILE = DATA_DIR / "error-database.json"

# Error type patterns
ERROR_PATTERNS = {
    "NPM_ERROR": r"npm ERR!|ERESOLVE|E404|ENOENT",
    "TypeScript": r"TS\d+|type .+ is not assignable|Cannot find module",
    "Build": r"build failed|compilation error|webpack|vite.*error",
    "Permission": r"EACCES|permission denied|access denied",
    "Network": r"ECONNREFUSED|timeout|ETIMEDOUT|getaddrinfo",
    "Syntax": r"SyntaxError|Unexpected token|ParseError",
    "Runtime": r"ReferenceError|TypeError|Cannot read property",
    "Database": r"ECONNREFUSED.*:5432|connection refused|database.*error",
    "Git": r"fatal:|error: .+git",
}

# Auto solutions
AUTO_SOLUTIONS = {
    "NPM_ERROR": "npm cache clean --force && rm -rf node_modules && npm install",
    "TypeScript": "npx tsc --noEmit to check types",
    "Build": "Check build configuration and dependencies",
    "Permission": "Run with elevated permissions or check file ownership",
    "Network": "Check network connection and firewall settings",
    "Database": "Ensure database server is running: docker-compose up -d",
}


def ensure_data_dir():
    """Create data directory."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_error_database() -> Dict[str, Any]:
    """Load error database."""
    if ERROR_DB_FILE.exists():
        try:
            return json.loads(ERROR_DB_FILE.read_text(encoding="utf-8-sig"))
        except:
            return json.loads(ERROR_DB_FILE.read_text(encoding="utf-8"))
    return {"version": "1.0", "errors": [], "lastUpdated": datetime.now().isoformat()}


def save_error_database(db: Dict[str, Any]):
    """Save error database."""
    ensure_data_dir()
    db["lastUpdated"] = datetime.now().isoformat()
    ERROR_DB_FILE.write_text(json.dumps(db, indent=4, ensure_ascii=False), encoding="utf-8")


def detect_error_type(output: str) -> str:
    """Detect error type."""
    for error_type, pattern in ERROR_PATTERNS.items():
        if re.search(pattern, output, re.IGNORECASE):
            return error_type
    return "UNKNOWN"


def extract_error_message(output: str) -> str:
    """Extract error message."""
    # Try to find error line
    patterns = [
        r"error[:\s]+(.+?)(?:\n|$)",
        r"Error[:\s]+(.+?)(?:\n|$)",
        r"ERR![:\s]+(.+?)(?:\n|$)",
        r"failed[:\s]+(.+?)(?:\n|$)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            return match.group(1).strip()[:200]
    
    # Fallback: first 200 chars
    return output[:200].strip() if output else "Unknown error"


def get_error_category(error_type: str) -> str:
    """Determine error category."""
    categories = {
        "NPM_ERROR": "NPM",
        "TypeScript": "TypeScript",
        "Build": "Build",
        "Permission": "System",
        "Network": "Network",
        "Syntax": "Code",
        "Runtime": "Code",
        "Database": "Database",
        "Git": "Git",
        "UNKNOWN": "Unknown"
    }
    return categories.get(error_type, "Unknown")


def normalize_command(cmd: str) -> str:
    """Normalize command for pattern matching."""
    normalized = cmd
    normalized = re.sub(r'npm install\s+[\w@/-]+', 'npm install {package}', normalized)
    normalized = re.sub(r'pip install\s+[\w-]+', 'pip install {package}', normalized)
    normalized = re.sub(r'[A-Za-z]:\\[\w\\/.-]+', '{path}', normalized)
    normalized = re.sub(r':\d{4,5}', ':{port}', normalized)
    normalized = re.sub(r'localhost|127\.0\.0\.1', '{host}', normalized)
    return normalized.strip()


def main():
    """Main function."""
    if len(sys.argv) < 4:
        print("Usage: python track_error.py \"<command>\" \"<exit_code>\" \"<output>\" [project_path]")
        sys.exit(0)
    
    command = sys.argv[1]
    exit_code = sys.argv[2]
    output = sys.argv[3]
    project_path = sys.argv[4] if len(sys.argv) > 4 else os.getcwd()
    
    try:
        # Skip if not an error
        if exit_code == "0" and not re.search(r"error|Error|ERROR|failed|Failed", output):
            sys.exit(0)
        
        # Load database
        error_db = load_error_database()
        errors = error_db.get("errors", [])
        
        # Detect error type
        error_type = detect_error_type(output)
        error_message = extract_error_message(output)
        error_category = get_error_category(error_type)
        pattern = normalize_command(command)
        
        # Check for similar error
        similar_error = None
        for err in errors:
            if err.get("pattern") == pattern or (
                err.get("errorType") == error_type and 
                err.get("errorMessage", "")[:50] == error_message[:50]
            ):
                similar_error = err
                break
        
        if similar_error:
            # Update existing error
            similar_error["occurrences"] = similar_error.get("occurrences", 1) + 1
            similar_error["lastSeen"] = datetime.now().isoformat()
            if similar_error["occurrences"] >= 3:
                similar_error["status"] = "recurring"
            print(f"🔄 Recurring error: {error_type} (x{similar_error['occurrences']})")
        else:
            # Create new error entry
            new_error = {
                "id": str(uuid.uuid4()),
                "command": command,
                "pattern": pattern,
                "errorMessage": error_message,
                "errorType": error_type,
                "errorCategory": error_category,
                "suggestion": AUTO_SOLUTIONS.get(error_type, "Review the error message and check documentation."),
                "project": project_path,
                "timestamp": datetime.now().isoformat(),
                "lastSeen": datetime.now().isoformat(),
                "solution": None,
                "status": "pending",
                "occurrences": 1,
                "exitCode": int(exit_code) if exit_code.isdigit() else 1
            }
            errors.append(new_error)
            print(f"📝 New error tracked: {error_type}")
            
            # Show suggestion
            if error_type in AUTO_SOLUTIONS:
                print(f"💡 Suggestion: {AUTO_SOLUTIONS[error_type]}")
        
        # Save database
        error_db["errors"] = errors
        save_error_database(error_db)
        
    except Exception as e:
        print(f"Track error warning: {e}", file=sys.stderr)
    
    sys.exit(0)


if __name__ == "__code__" or __name__ == "__main__":
    try:
        if sys.platform == "win32":
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass
    main()
