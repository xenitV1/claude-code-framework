#!/usr/bin/env python3
"""
Git Commit Helper - Generate intelligent commit messages.

Analyzes staged changes and generates conventional commit messages.
Can be used as a standalone script or integrated with git hooks.

Usage:
    python git_commit_helper.py suggest          # Suggest commit message for staged changes
    python git_commit_helper.py suggest --copy   # Copy suggestion to clipboard
    python git_commit_helper.py validate "msg"   # Validate commit message format
    python git_commit_helper.py stats            # Show commit statistics

Conventional Commit Types:
    feat:     New feature
    fix:      Bug fix
    docs:     Documentation only
    style:    Formatting, no code change
    refactor: Code restructuring
    perf:     Performance improvement
    test:     Adding tests
    chore:    Maintenance tasks
    ci:       CI/CD changes
    build:    Build system changes
"""

import json
import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import Counter

# File type to commit type mapping
FILE_TYPE_HINTS = {
    # Documentation
    ".md": "docs",
    ".rst": "docs",
    ".txt": "docs",

    # Tests
    "test_": "test",
    "_test.": "test",
    ".test.": "test",
    "spec.": "test",
    "__tests__": "test",

    # CI/CD
    ".github/workflows": "ci",
    ".gitlab-ci": "ci",
    "Jenkinsfile": "ci",
    ".travis": "ci",

    # Build
    "package.json": "build",
    "requirements.txt": "build",
    "setup.py": "build",
    "pyproject.toml": "build",
    "Cargo.toml": "build",
    "go.mod": "build",
    "Makefile": "build",
    "Dockerfile": "build",

    # Config
    ".config": "chore",
    ".env": "chore",
    ".gitignore": "chore",
    "settings.json": "chore",
}

# Keywords that hint at commit type
KEYWORD_HINTS = {
    "fix": ["fix", "bug", "error", "issue", "crash", "patch"],
    "feat": ["add", "new", "feature", "implement", "create"],
    "refactor": ["refactor", "restructure", "reorganize", "clean", "simplify"],
    "perf": ["performance", "optimize", "speed", "fast", "cache"],
    "docs": ["readme", "documentation", "comment", "docs"],
    "style": ["format", "style", "lint", "prettier", "eslint"],
    "test": ["test", "spec", "coverage", "mock"],
    "chore": ["update", "upgrade", "bump", "dependency", "deps"],
}


def run_git_command(args: List[str]) -> Tuple[bool, str]:
    """Run a git command and return success status and output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, "Git not found"


def get_staged_files() -> List[str]:
    """Get list of staged files."""
    success, output = run_git_command(["diff", "--cached", "--name-only"])
    if not success or not output:
        return []
    return output.split("\n")


def get_staged_diff() -> str:
    """Get diff of staged changes."""
    success, output = run_git_command(["diff", "--cached", "--stat"])
    return output if success else ""


def get_staged_diff_content() -> str:
    """Get full diff content of staged changes."""
    success, output = run_git_command(["diff", "--cached"])
    return output if success else ""


def get_recent_commits(limit: int = 10) -> List[str]:
    """Get recent commit messages for style reference."""
    success, output = run_git_command([
        "log", f"-{limit}", "--pretty=format:%s"
    ])
    if not success or not output:
        return []
    return output.split("\n")


def infer_commit_type(files: List[str], diff_content: str) -> str:
    """Infer commit type from changed files and diff content."""
    type_scores: Counter = Counter()

    # Analyze file paths
    for file in files:
        file_lower = file.lower()

        # Check file type hints
        for pattern, commit_type in FILE_TYPE_HINTS.items():
            if pattern in file_lower:
                type_scores[commit_type] += 2

        # Check for deletion (likely fix or refactor)
        if not Path(file).exists():
            type_scores["refactor"] += 1

    # Analyze diff content for keywords
    diff_lower = diff_content.lower()
    for commit_type, keywords in KEYWORD_HINTS.items():
        for keyword in keywords:
            count = diff_lower.count(keyword)
            if count > 0:
                type_scores[commit_type] += count

    # Check diff stats
    if "+++ /dev/null" in diff_content:
        type_scores["refactor"] += 2  # Files deleted

    # Default to feat for new files
    if not type_scores:
        return "feat"

    return type_scores.most_common(1)[0][0]


def infer_scope(files: List[str]) -> Optional[str]:
    """Infer scope from file paths."""
    if not files:
        return None

    # Extract directories
    dirs = []
    for file in files:
        parts = Path(file).parts
        if len(parts) > 1:
            dirs.append(parts[0])
        else:
            # Use file name without extension for root files
            name = Path(file).stem
            dirs.append(name)

    # Find common scope
    if len(set(dirs)) == 1:
        return dirs[0]

    # Check for common prefixes
    common_dirs = Counter(dirs).most_common(1)
    if common_dirs and common_dirs[0][1] > len(files) // 2:
        return common_dirs[0][0]

    return None


def generate_description(files: List[str], diff_content: str, commit_type: str) -> str:
    """Generate commit description based on changes."""
    if not files:
        return "update files"

    # Single file change
    if len(files) == 1:
        file = files[0]
        name = Path(file).stem
        ext = Path(file).suffix

        # Special cases
        if "readme" in file.lower():
            return "update README"
        if "package.json" in file.lower():
            return "update dependencies"
        if commit_type == "test":
            return f"add tests for {name}"
        if commit_type == "docs":
            return f"update {name} documentation"

        # Check if file was added or modified
        success, status = run_git_command(["diff", "--cached", "--name-status"])
        if success:
            for line in status.split("\n"):
                if file in line:
                    if line.startswith("A"):
                        return f"add {name}{ext}"
                    elif line.startswith("D"):
                        return f"remove {name}{ext}"
                    elif line.startswith("R"):
                        return f"rename {name}{ext}"

        return f"update {name}{ext}"

    # Multiple files
    # Group by directory
    dirs = [Path(f).parts[0] if len(Path(f).parts) > 1 else "root" for f in files]
    dir_count = Counter(dirs)

    if len(dir_count) == 1:
        # All files in same directory
        dir_name = list(dir_count.keys())[0]
        return f"update {dir_name} ({len(files)} files)"

    # Multiple directories
    main_dir = dir_count.most_common(1)[0][0]
    return f"update {main_dir} and related files"


def suggest_commit_message(copy_to_clipboard: bool = False) -> Dict:
    """Generate a suggested commit message for staged changes."""
    files = get_staged_files()

    if not files:
        return {
            "success": False,
            "error": "No staged changes found. Use 'git add' first."
        }

    diff_stat = get_staged_diff()
    diff_content = get_staged_diff_content()

    # Infer components
    commit_type = infer_commit_type(files, diff_content)
    scope = infer_scope(files)
    description = generate_description(files, diff_content, commit_type)

    # Build message
    if scope:
        message = f"{commit_type}({scope}): {description}"
    else:
        message = f"{commit_type}: {description}"

    # Get recent commits for reference
    recent = get_recent_commits(5)

    result = {
        "success": True,
        "suggestion": message,
        "type": commit_type,
        "scope": scope,
        "description": description,
        "files": files,
        "fileCount": len(files),
        "diffStat": diff_stat,
        "recentCommits": recent[:3]
    }

    # Copy to clipboard if requested
    if copy_to_clipboard:
        try:
            if sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=message.encode(), check=True)
                result["copied"] = True
            elif sys.platform == "win32":
                subprocess.run(["clip"], input=message.encode(), check=True)
                result["copied"] = True
            else:
                # Linux - try xclip
                subprocess.run(["xclip", "-selection", "clipboard"],
                             input=message.encode(), check=True)
                result["copied"] = True
        except:
            result["copied"] = False

    return result


def validate_commit_message(message: str) -> Dict:
    """Validate commit message against conventional commit format."""
    # Conventional commit pattern
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\([a-zA-Z0-9_-]+\))?: .{1,72}$'

    errors = []
    warnings = []

    # Check format
    if not re.match(pattern, message.split('\n')[0]):
        errors.append("Message doesn't follow conventional commit format")
        errors.append("Expected: type(scope): description")
        errors.append("Types: feat, fix, docs, style, refactor, perf, test, chore, ci, build")

    # Check length
    first_line = message.split('\n')[0]
    if len(first_line) > 72:
        warnings.append(f"First line is {len(first_line)} chars (recommended max: 72)")

    if len(first_line) < 10:
        warnings.append("Message seems too short")

    # Check capitalization
    parts = message.split(': ', 1)
    if len(parts) > 1 and parts[1] and parts[1][0].isupper():
        warnings.append("Description should start with lowercase")

    # Check for period
    if first_line.endswith('.'):
        warnings.append("First line should not end with a period")

    return {
        "valid": len(errors) == 0,
        "message": message,
        "errors": errors,
        "warnings": warnings
    }


def show_commit_stats() -> Dict:
    """Show commit statistics for the repository."""
    stats = {
        "totalCommits": 0,
        "byType": {},
        "topContributors": [],
        "recentActivity": []
    }

    # Total commits
    success, output = run_git_command(["rev-list", "--count", "HEAD"])
    if success:
        stats["totalCommits"] = int(output)

    # Commits by type
    success, output = run_git_command(["log", "--oneline", "-100"])
    if success:
        type_pattern = r'^[a-f0-9]+ (feat|fix|docs|style|refactor|perf|test|chore|ci|build)'
        types = Counter()
        for line in output.split('\n'):
            match = re.match(type_pattern, line)
            if match:
                types[match.group(1)] += 1
        stats["byType"] = dict(types.most_common())

    # Top contributors
    success, output = run_git_command(["shortlog", "-sn", "--no-merges", "-10"])
    if success:
        contributors = []
        for line in output.split('\n'):
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    contributors.append({
                        "commits": int(parts[0].strip()),
                        "name": parts[1].strip()
                    })
        stats["topContributors"] = contributors[:5]

    return stats


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python git_commit_helper.py suggest [--copy]")
        print("  python git_commit_helper.py validate \"commit message\"")
        print("  python git_commit_helper.py stats")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "suggest":
        copy = "--copy" in sys.argv or "-c" in sys.argv
        result = suggest_commit_message(copy_to_clipboard=copy)

        if result["success"]:
            print("\n" + "=" * 50)
            print("💡 SUGGESTED COMMIT MESSAGE")
            print("=" * 50)
            print(f"\n  {result['suggestion']}\n")
            print("-" * 50)
            print(f"📁 Files: {result['fileCount']}")
            print(f"🏷️  Type: {result['type']}")
            if result.get('scope'):
                print(f"📦 Scope: {result['scope']}")
            print("\n📊 Changes:")
            print(result['diffStat'])

            if result.get('copied'):
                print("\n✅ Copied to clipboard!")

            print("\n💾 To commit: git commit -m \"" + result['suggestion'] + "\"")
            print("=" * 50 + "\n")
        else:
            print(f"❌ {result['error']}")
            sys.exit(1)

    elif command == "validate":
        if len(sys.argv) < 3:
            print("Usage: python git_commit_helper.py validate \"commit message\"")
            sys.exit(1)

        message = sys.argv[2]
        result = validate_commit_message(message)

        print("\n" + "=" * 50)
        print("🔍 COMMIT MESSAGE VALIDATION")
        print("=" * 50)
        print(f"\nMessage: {result['message']}")
        print(f"Valid: {'✅ Yes' if result['valid'] else '❌ No'}")

        if result['errors']:
            print("\n❌ Errors:")
            for error in result['errors']:
                print(f"   - {error}")

        if result['warnings']:
            print("\n⚠️  Warnings:")
            for warning in result['warnings']:
                print(f"   - {warning}")

        print("=" * 50 + "\n")

        sys.exit(0 if result['valid'] else 1)

    elif command == "stats":
        result = show_commit_stats()

        print("\n" + "=" * 50)
        print("📊 COMMIT STATISTICS")
        print("=" * 50)
        print(f"\n📝 Total Commits: {result['totalCommits']}")

        if result['byType']:
            print("\n🏷️  By Type (last 100):")
            for commit_type, count in result['byType'].items():
                bar = "█" * (count // 2)
                print(f"   {commit_type:10} {count:3} {bar}")

        if result['topContributors']:
            print("\n👥 Top Contributors:")
            for i, contrib in enumerate(result['topContributors'], 1):
                print(f"   {i}. {contrib['name']} ({contrib['commits']} commits)")

        print("=" * 50 + "\n")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
