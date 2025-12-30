#!/usr/bin/env python3
"""
Check Prevention - Checks dangerous commands
Runs as PreToolUse hook.

Usage: python check_prevention.py "<command>" [project_path]
"""

import json
import sys
import re
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
ERROR_TRACKER_FILE = DATA_DIR / "error-tracker.json"

# Dangerous command patterns
DANGEROUS_PATTERNS = {
    "rm -rf /": "System destruction - BLOCKED",
    "rm -rf ~": "Home directory deletion - BLOCKED",
    "rm -rf *": "Mass file deletion - WARNING",
    "DROP DATABASE": "Database deletion - BLOCKED",
    "DROP TABLE": "Table deletion - WARNING",
    "git push --force": "Force push - WARNING",
    "git reset --hard": "Hard reset - WARNING",
    "npm publish": "Package publish - CONFIRMATION REQUIRED",
    "chmod 777": "Insecure permissions - WARNING",
}


def load_prevention_rules() -> list:
    """Load prevention rules."""
    if not ERROR_TRACKER_FILE.exists():
        return []
    
    try:
        tracker = json.loads(ERROR_TRACKER_FILE.read_text())
        return tracker.get("preventionRules", [])
    except:
        return []


def check_dangerous_command(command: str) -> Optional[Dict[str, str]]:
    """Check for dangerous commands."""
    cmd_lower = command.lower()
    
    for pattern, warning in DANGEROUS_PATTERNS.items():
        if pattern.lower() in cmd_lower:
            return {
                "pattern": pattern,
                "warning": warning,
                "severity": "BLOCKED" if "BLOCKED" in warning else "WARNING"
            }
    
    return None


def check_learned_prevention(command: str, rules: list) -> Optional[Dict[str, Any]]:
    """Check learned rules."""
    for rule in rules:
        pattern = rule.get("pattern", "")
        error_type = rule.get("errorType", "")
        
        # Pattern match
        if pattern and (pattern in command or re.search(re.escape(pattern), command, re.IGNORECASE)):
            return {
                "shouldApplyPrevention": True,
                "preventionAction": rule.get("autoSolution", "Review this command carefully"),
                "errorPattern": pattern,
                "errorType": error_type
            }
    
    return None


def main():
    """Ana fonksiyon."""
    if len(sys.argv) < 2:
        print(json.dumps({"shouldApplyPrevention": False}))
        sys.exit(0)
    
    command = sys.argv[1]
    project_path = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
    
    # Check dangerous commands first
    dangerous = check_dangerous_command(command)
    if dangerous:
        result = {
            "shouldApplyPrevention": True,
            "severity": dangerous["severity"],
            "warning": dangerous["warning"],
            "pattern": dangerous["pattern"]
        }
        
        if dangerous["severity"] == "BLOCKED":
            print(f"🚫 BLOCKED: {dangerous['warning']}")
            print(f"   Pattern: {dangerous['pattern']}")
            result["blocked"] = True
        else:
            print(f"⚠️ WARNING: {dangerous['warning']}")
            print(f"   Pattern: {dangerous['pattern']}")
        
        print(json.dumps(result))
        sys.exit(0)
    
    # Check learned prevention rules
    rules = load_prevention_rules()
    prevention = check_learned_prevention(command, rules)
    
    if prevention:
        print(f"⚠️ PREVENTION: Known problematic pattern detected")
        print(f"   Pattern: {prevention['errorPattern']}")
        print(f"   Suggestion: {prevention['preventionAction']}")
        print(json.dumps(prevention))
    else:
        print(json.dumps({"shouldApplyPrevention": False}))
    
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
