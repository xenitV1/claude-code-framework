#!/usr/bin/env python3
"""
Error Formatter - Human-friendly error messages for Maestro hooks.

Transforms cryptic error messages into actionable suggestions.

Usage:
    python error_formatter.py format "<error_message>"
    python error_formatter.py analyze "<command>" "<error_output>"
"""

import sys
import re
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Error patterns and their human-friendly explanations
ERROR_PATTERNS: List[Dict] = [
    # Node.js / npm errors
    {
        "pattern": r"npm ERR! code ENOENT",
        "title": "File Not Found",
        "explanation": "npm couldn't find a required file (usually package.json)",
        "suggestions": [
            "Run `npm init -y` to create package.json",
            "Check if you're in the correct directory",
            "Verify the file path exists"
        ]
    },
    {
        "pattern": r"npm ERR! code E404",
        "title": "Package Not Found",
        "explanation": "The npm package doesn't exist or name is misspelled",
        "suggestions": [
            "Check package name spelling on npmjs.com",
            "Verify the package is published",
            "Try `npm search <package-name>`"
        ]
    },
    {
        "pattern": r"npm ERR! ERESOLVE",
        "title": "Dependency Conflict",
        "explanation": "Package versions have conflicting requirements",
        "suggestions": [
            "Try `npm install --legacy-peer-deps`",
            "Update conflicting packages",
            "Check package.json for version mismatches"
        ]
    },
    {
        "pattern": r"EACCES.*permission denied",
        "title": "Permission Denied",
        "explanation": "Insufficient permissions to access file/directory",
        "suggestions": [
            "Check file/folder permissions",
            "Don't use sudo with npm (fix npm permissions instead)",
            "Run `npm config set prefix ~/.npm-global`"
        ]
    },
    {
        "pattern": r"node:internal/modules/cjs/loader.*Cannot find module",
        "title": "Module Not Found",
        "explanation": "Node.js can't find the required module",
        "suggestions": [
            "Run `npm install` to install dependencies",
            "Check if the module is in package.json",
            "Verify import/require path is correct"
        ]
    },

    # Python errors
    {
        "pattern": r"ModuleNotFoundError: No module named",
        "title": "Python Module Not Found",
        "explanation": "Python can't find the imported module",
        "suggestions": [
            "Run `pip install <module-name>`",
            "Check if virtual environment is activated",
            "Verify module name spelling"
        ]
    },
    {
        "pattern": r"pip.*No matching distribution found",
        "title": "Package Not Found (pip)",
        "explanation": "The Python package doesn't exist on PyPI",
        "suggestions": [
            "Check package name on pypi.org",
            "Try `pip search <package>` (if available)",
            "Check for typos in package name"
        ]
    },
    {
        "pattern": r"SyntaxError:",
        "title": "Python Syntax Error",
        "explanation": "Invalid Python syntax in your code",
        "suggestions": [
            "Check for missing colons, parentheses, or quotes",
            "Verify indentation is consistent",
            "Look at the line number in the error"
        ]
    },

    # Git errors
    {
        "pattern": r"fatal: not a git repository",
        "title": "Not a Git Repository",
        "explanation": "Current directory is not initialized as a git repo",
        "suggestions": [
            "Run `git init` to initialize",
            "Navigate to your project root",
            "Check if .git folder exists"
        ]
    },
    {
        "pattern": r"fatal: refusing to merge unrelated histories",
        "title": "Unrelated Git Histories",
        "explanation": "Trying to merge branches with no common ancestor",
        "suggestions": [
            "Use `git pull origin main --allow-unrelated-histories`",
            "This often happens with new repos"
        ]
    },
    {
        "pattern": r"error: failed to push some refs",
        "title": "Git Push Rejected",
        "explanation": "Remote has changes you don't have locally",
        "suggestions": [
            "Run `git pull --rebase` first",
            "Then try `git push` again",
            "Check for merge conflicts"
        ]
    },

    # Docker errors
    {
        "pattern": r"Cannot connect to the Docker daemon",
        "title": "Docker Not Running",
        "explanation": "Docker daemon is not started",
        "suggestions": [
            "Start Docker Desktop",
            "Run `sudo systemctl start docker` (Linux)",
            "Check Docker installation"
        ]
    },
    {
        "pattern": r"port is already allocated",
        "title": "Port Already in Use",
        "explanation": "Another process is using the requested port",
        "suggestions": [
            "Find process: `lsof -i :<port>` or `netstat -tulpn`",
            "Kill the process or use a different port",
            "Stop other containers using the port"
        ]
    },

    # Build errors
    {
        "pattern": r"error TS\d+:",
        "title": "TypeScript Error",
        "explanation": "TypeScript compilation failed",
        "suggestions": [
            "Check the error code (e.g., TS2304 = name not found)",
            "Verify types are correctly imported",
            "Run `npx tsc --noEmit` for detailed errors"
        ]
    },
    {
        "pattern": r"SyntaxError: Unexpected token",
        "title": "JavaScript Syntax Error",
        "explanation": "Invalid JavaScript syntax",
        "suggestions": [
            "Check for missing brackets or semicolons",
            "Verify JSON files are valid",
            "Look for unsupported syntax for your Node version"
        ]
    },

    # Network errors
    {
        "pattern": r"ECONNREFUSED",
        "title": "Connection Refused",
        "explanation": "Can't connect to the server/service",
        "suggestions": [
            "Check if the service is running",
            "Verify the port number is correct",
            "Check firewall settings"
        ]
    },
    {
        "pattern": r"ETIMEDOUT|ESOCKETTIMEDOUT",
        "title": "Connection Timeout",
        "explanation": "Server took too long to respond",
        "suggestions": [
            "Check your internet connection",
            "Server might be down or overloaded",
            "Try again later"
        ]
    },

    # Database errors
    {
        "pattern": r"SQLITE_BUSY",
        "title": "Database Locked",
        "explanation": "SQLite database is locked by another process",
        "suggestions": [
            "Close other connections to the database",
            "Check for hanging processes",
            "Use WAL mode: `PRAGMA journal_mode=WAL`"
        ]
    },
    {
        "pattern": r"relation .* does not exist",
        "title": "Table Not Found",
        "explanation": "Database table doesn't exist",
        "suggestions": [
            "Run database migrations",
            "Check table name spelling",
            "Verify database connection"
        ]
    },
]


def find_matching_pattern(error_text: str) -> Optional[Dict]:
    """Find the first matching error pattern."""
    error_lower = error_text.lower()
    for pattern in ERROR_PATTERNS:
        if re.search(pattern["pattern"], error_text, re.IGNORECASE | re.MULTILINE):
            return pattern
    return None


def format_error(error_text: str) -> str:
    """Format an error message with helpful suggestions."""
    pattern = find_matching_pattern(error_text)

    if not pattern:
        return f"Error: {error_text[:200]}"

    lines = [
        "",
        "=" * 50,
        f"❌ {pattern['title']}",
        "=" * 50,
        "",
        f"📋 What happened:",
        f"   {pattern['explanation']}",
        "",
        "💡 Suggestions:",
    ]

    for i, suggestion in enumerate(pattern["suggestions"], 1):
        lines.append(f"   {i}. {suggestion}")

    lines.extend(["", "=" * 50, ""])

    return "\n".join(lines)


def analyze_command_error(command: str, error_output: str) -> Dict:
    """Analyze a command's error output and return structured info."""
    pattern = find_matching_pattern(error_output)

    result = {
        "command": command,
        "hasKnownPattern": pattern is not None,
        "formatted": format_error(error_output) if pattern else None,
    }

    if pattern:
        result["errorType"] = pattern["title"]
        result["explanation"] = pattern["explanation"]
        result["suggestions"] = pattern["suggestions"]

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python error_formatter.py format '<error_message>'")
        print("  python error_formatter.py analyze '<command>' '<error_output>'")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "format":
        if len(sys.argv) < 3:
            print("Usage: python error_formatter.py format '<error_message>'")
            sys.exit(1)
        error_text = sys.argv[2]
        print(format_error(error_text))

    elif command == "analyze":
        if len(sys.argv) < 4:
            print("Usage: python error_formatter.py analyze '<command>' '<error_output>'")
            sys.exit(1)
        cmd = sys.argv[2]
        error_output = sys.argv[3]
        result = analyze_command_error(cmd, error_output)
        print(json.dumps(result, indent=2))

    elif command == "list":
        print("\nKnown Error Patterns:")
        print("-" * 40)
        for p in ERROR_PATTERNS:
            print(f"  • {p['title']}")
        print(f"\nTotal: {len(ERROR_PATTERNS)} patterns")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
