#!/usr/bin/env python3
"""
Cross-platform setup script for Claude Code Maestro.
Automatically detects OS and configures hooks appropriately.
"""

import os
import sys
import shutil
import platform
from pathlib import Path


def get_claude_dir() -> Path:
    """Get the .claude directory path based on OS."""
    if platform.system() == "Windows":
        base = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    return Path(base) / ".claude"


def get_settings_source(repo_dir: Path) -> Path:
    """Get the appropriate settings file based on OS."""
    if platform.system() == "Windows":
        return repo_dir / "settings.example.windows.json"
    else:
        return repo_dir / "settings.example.unix.json"


def setup_scripts(repo_dir: Path, claude_dir: Path) -> None:
    """Copy scripts to ~/.claude/scripts/"""
    scripts_src = repo_dir / "scripts"
    scripts_dst = claude_dir / "scripts"

    scripts_dst.mkdir(parents=True, exist_ok=True)

    script_files = [
        "session_hooks.py",
        "pre_bash.py",
        "track_error.py",
        "explorer_helper.py",
        "check_prevention.py",
        "parallel_orchestrator.py",
        "session_manager.py",
        "auto_preview.py",
    ]

    for script in script_files:
        src = scripts_src / script
        dst = scripts_dst / script
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  Copied: {script}")
        else:
            print(f"  Warning: {script} not found")


def setup_settings(repo_dir: Path, claude_dir: Path) -> None:
    """Copy the appropriate settings file."""
    src = get_settings_source(repo_dir)
    dst = claude_dir / "settings.json"

    if dst.exists():
        backup = claude_dir / "settings.json.backup"
        shutil.copy2(dst, backup)
        print(f"  Backed up existing settings to: settings.json.backup")

    if src.exists():
        shutil.copy2(src, dst)
        print(f"  Installed: settings.json (from {src.name})")
    else:
        print(f"  Error: Settings file not found: {src}")
        sys.exit(1)


def setup_data_dir(claude_dir: Path) -> None:
    """Create data directory structure."""
    data_dir = claude_dir / "data"
    subdirs = ["projects", "reports"]

    for subdir in subdirs:
        (data_dir / subdir).mkdir(parents=True, exist_ok=True)

    print(f"  Created: data directory structure")


def main():
    print(f"\nClaude Code Maestro Setup")
    print(f"{'=' * 40}")
    print(f"Platform: {platform.system()} ({platform.machine()})")

    # Detect repo directory (parent of scripts/)
    script_path = Path(__file__).resolve()
    repo_dir = script_path.parent.parent

    if not (repo_dir / "agents").exists():
        print(f"Error: Could not find repo root at {repo_dir}")
        sys.exit(1)

    print(f"Repository: {repo_dir}")

    claude_dir = get_claude_dir()
    print(f"Claude dir: {claude_dir}")

    print(f"\n1. Setting up scripts...")
    setup_scripts(repo_dir, claude_dir)

    print(f"\n2. Setting up settings...")
    setup_settings(repo_dir, claude_dir)

    print(f"\n3. Setting up data directories...")
    setup_data_dir(claude_dir)

    print(f"\n{'=' * 40}")
    print(f"Setup complete!")
    print(f"\nNext steps:")
    print(f"  1. Restart Claude Code CLI")
    print(f"  2. Run 'claude --debug' to verify hooks are loaded")


if __name__ == "__main__":
    main()
