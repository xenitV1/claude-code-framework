#!/usr/bin/env python3
"""
Maestro CLI - Unified command-line interface for Claude Code Maestro.

This wrapper provides convenient shortcuts for common operations
and integrates with Claude Code CLI.

Usage:
    maestro create <description>     Create a new project
    maestro enhance <description>    Add features to current project
    maestro debug <description>      Debug an issue
    maestro test [target]            Generate/run tests
    maestro status                   Show project status
    maestro tokens                   Show token usage
    maestro commit                   Generate commit message
    maestro agents                   List available agents
    maestro skills                   List available skills
    maestro help                     Show this help

Examples:
    maestro create e-commerce site with React
    maestro enhance add dark mode toggle
    maestro debug login form not submitting
    maestro commit
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

# Check for Rich
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


def print_msg(msg: str, style: str = ""):
    """Print message."""
    if RICH_AVAILABLE and console:
        console.print(msg, style=style)
    else:
        print(msg)


def get_maestro_dir() -> Path:
    """Get Maestro installation directory."""
    return Path(__file__).parent.parent


def get_claude_dir() -> Path:
    """Get Claude data directory."""
    return Path.home() / ".claude"


def run_claude_command(prompt: str, interactive: bool = True) -> int:
    """Run Claude Code with a prompt."""
    cmd = ["claude"]

    if interactive:
        cmd.extend(["--prompt", prompt])
    else:
        cmd.extend(["--print", prompt])

    try:
        result = subprocess.run(cmd)
        return result.returncode
    except FileNotFoundError:
        print_msg("[red]Error: Claude Code CLI not found. Install it first.[/red]" if RICH_AVAILABLE else "Error: Claude Code CLI not found")
        return 1


def cmd_create(args: argparse.Namespace) -> int:
    """Create a new project."""
    description = " ".join(args.description)
    prompt = f"/create {description}"

    print_msg(f"\n[cyan]Creating project:[/cyan] {description}\n" if RICH_AVAILABLE else f"\nCreating project: {description}\n")
    return run_claude_command(prompt)


def cmd_enhance(args: argparse.Namespace) -> int:
    """Enhance current project."""
    description = " ".join(args.description)
    prompt = f"/enhance {description}"

    print_msg(f"\n[cyan]Enhancing:[/cyan] {description}\n" if RICH_AVAILABLE else f"\nEnhancing: {description}\n")
    return run_claude_command(prompt)


def cmd_debug(args: argparse.Namespace) -> int:
    """Debug an issue."""
    description = " ".join(args.description)
    prompt = f"/debug {description}"

    print_msg(f"\n[cyan]Debugging:[/cyan] {description}\n" if RICH_AVAILABLE else f"\nDebugging: {description}\n")
    return run_claude_command(prompt)


def cmd_test(args: argparse.Namespace) -> int:
    """Generate or run tests."""
    target = " ".join(args.target) if args.target else ""
    prompt = f"/test {target}".strip()

    print_msg(f"\n[cyan]Testing:[/cyan] {target or 'all'}\n" if RICH_AVAILABLE else f"\nTesting: {target or 'all'}\n")
    return run_claude_command(prompt)


def cmd_status(args: argparse.Namespace) -> int:
    """Show project status."""
    claude_dir = get_claude_dir()
    current_project = claude_dir / "data" / "current-project.json"

    if not current_project.exists():
        print_msg("[yellow]No active project detected[/yellow]" if RICH_AVAILABLE else "No active project detected")
        return 0

    try:
        project = json.loads(current_project.read_text())

        if RICH_AVAILABLE:
            console.print(Panel(
                f"[bold]Project:[/bold] {project.get('projectName', 'Unknown')}\n"
                f"[bold]Path:[/bold] {project.get('projectPath', 'Unknown')}\n"
                f"[bold]Last Access:[/bold] {project.get('lastAccess', 'Unknown')}",
                title="Project Status",
                border_style="cyan"
            ))
        else:
            print(f"\nProject Status:")
            print(f"  Name: {project.get('projectName', 'Unknown')}")
            print(f"  Path: {project.get('projectPath', 'Unknown')}")
            print(f"  Last Access: {project.get('lastAccess', 'Unknown')}")

        # Check for session stats
        data_dir = project.get("dataDir")
        if data_dir:
            session_file = Path(data_dir) / "session-stats.json"
            if session_file.exists():
                session = json.loads(session_file.read_text())
                analysis = session.get("analysis", {})

                if RICH_AVAILABLE:
                    console.print(f"\n[bold]Framework:[/bold] {analysis.get('framework', 'Unknown')}")
                    console.print(f"[bold]Platform:[/bold] {analysis.get('platform', 'Unknown')}")
                else:
                    print(f"  Framework: {analysis.get('framework', 'Unknown')}")
                    print(f"  Platform: {analysis.get('platform', 'Unknown')}")

    except Exception as e:
        print_msg(f"[red]Error reading project status: {e}[/red]" if RICH_AVAILABLE else f"Error: {e}")
        return 1

    return 0


def cmd_tokens(args: argparse.Namespace) -> int:
    """Show token usage statistics."""
    scripts_dir = get_claude_dir() / "scripts"
    token_tracker = scripts_dir / "token_tracker.py"

    if not token_tracker.exists():
        # Try local version
        token_tracker = get_maestro_dir() / "scripts" / "token_tracker.py"

    if not token_tracker.exists():
        print_msg("[red]Token tracker not installed[/red]" if RICH_AVAILABLE else "Token tracker not installed")
        return 1

    return subprocess.run([sys.executable, str(token_tracker), "summary"]).returncode


def cmd_commit(args: argparse.Namespace) -> int:
    """Generate commit message."""
    scripts_dir = get_claude_dir() / "scripts"
    git_helper = scripts_dir / "git_commit_helper.py"

    if not git_helper.exists():
        git_helper = get_maestro_dir() / "scripts" / "git_commit_helper.py"

    if not git_helper.exists():
        print_msg("[red]Git commit helper not installed[/red]" if RICH_AVAILABLE else "Git commit helper not installed")
        return 1

    cmd_args = ["suggest"]
    if args.copy:
        cmd_args.append("--copy")

    return subprocess.run([sys.executable, str(git_helper)] + cmd_args).returncode


def cmd_agents(args: argparse.Namespace) -> int:
    """List available agents."""
    agents_dir = get_maestro_dir() / "agents"

    if not agents_dir.exists():
        print_msg("[red]Agents directory not found[/red]" if RICH_AVAILABLE else "Agents directory not found")
        return 1

    agents = []
    for f in sorted(agents_dir.glob("*.md")):
        if f.name == "README.md":
            continue

        # Parse frontmatter
        content = f.read_text()
        name = f.stem
        description = ""

        if content.startswith("---"):
            try:
                end = content.index("---", 3)
                frontmatter = content[3:end]
                for line in frontmatter.split("\n"):
                    if line.startswith("description:"):
                        description = line.split(":", 1)[1].strip().strip('"\'')
                        break
            except:
                pass

        agents.append({"name": name, "description": description})

    if RICH_AVAILABLE:
        table = Table(title="Available Agents", show_header=True)
        table.add_column("Agent", style="cyan")
        table.add_column("Description", style="white")

        for agent in agents:
            table.add_row(agent["name"], agent["description"][:60] + "..." if len(agent["description"]) > 60 else agent["description"])

        console.print(table)
    else:
        print("\nAvailable Agents:")
        for agent in agents:
            print(f"  {agent['name']}: {agent['description'][:60]}")

    return 0


def cmd_skills(args: argparse.Namespace) -> int:
    """List available skills."""
    skills_dir = get_maestro_dir() / "skills"

    if not skills_dir.exists():
        print_msg("[red]Skills directory not found[/red]" if RICH_AVAILABLE else "Skills directory not found")
        return 1

    skills = []
    for d in sorted(skills_dir.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            skill_file = d / "SKILL.md"
            content = skill_file.read_text()
            name = d.name
            description = ""

            if content.startswith("---"):
                try:
                    end = content.index("---", 3)
                    frontmatter = content[3:end]
                    for line in frontmatter.split("\n"):
                        if line.startswith("description:"):
                            description = line.split(":", 1)[1].strip().strip('"\'')
                            break
                except:
                    pass

            skills.append({"name": name, "description": description})

    # Also check templates
    templates_dir = skills_dir / "templates"
    if templates_dir.exists():
        for d in sorted(templates_dir.iterdir()):
            if d.is_dir() and (d / "TEMPLATE.md").exists():
                skills.append({"name": f"templates/{d.name}", "description": "Project template"})

    if RICH_AVAILABLE:
        table = Table(title="Available Skills", show_header=True)
        table.add_column("Skill", style="cyan")
        table.add_column("Description", style="white")

        for skill in skills:
            desc = skill["description"][:50] + "..." if len(skill["description"]) > 50 else skill["description"]
            table.add_row(skill["name"], desc)

        console.print(table)
        console.print(f"\n[dim]Total: {len(skills)} skills[/dim]")
    else:
        print("\nAvailable Skills:")
        for skill in skills:
            print(f"  {skill['name']}: {skill['description'][:50]}")
        print(f"\nTotal: {len(skills)} skills")

    return 0


def cmd_help(args: argparse.Namespace) -> int:
    """Show help."""
    help_text = """
# Maestro CLI

## Commands

| Command | Description |
|---------|-------------|
| `maestro create <desc>` | Create a new project |
| `maestro enhance <desc>` | Add features |
| `maestro debug <desc>` | Debug an issue |
| `maestro test [target]` | Generate/run tests |
| `maestro status` | Show project status |
| `maestro tokens` | Token usage stats |
| `maestro commit` | Generate commit message |
| `maestro agents` | List agents |
| `maestro skills` | List skills |

## Examples

```bash
maestro create e-commerce site with Next.js
maestro enhance add user authentication
maestro debug form validation not working
maestro commit --copy
```
"""

    if RICH_AVAILABLE:
        console.print(Markdown(help_text))
    else:
        print(__doc__)

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Maestro CLI - Claude Code Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Run 'maestro help' for more information"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create
    p_create = subparsers.add_parser("create", help="Create a new project")
    p_create.add_argument("description", nargs="+", help="Project description")
    p_create.set_defaults(func=cmd_create)

    # enhance
    p_enhance = subparsers.add_parser("enhance", help="Add features")
    p_enhance.add_argument("description", nargs="+", help="Feature description")
    p_enhance.set_defaults(func=cmd_enhance)

    # debug
    p_debug = subparsers.add_parser("debug", help="Debug an issue")
    p_debug.add_argument("description", nargs="+", help="Issue description")
    p_debug.set_defaults(func=cmd_debug)

    # test
    p_test = subparsers.add_parser("test", help="Generate/run tests")
    p_test.add_argument("target", nargs="*", help="Test target")
    p_test.set_defaults(func=cmd_test)

    # status
    p_status = subparsers.add_parser("status", help="Show project status")
    p_status.set_defaults(func=cmd_status)

    # tokens
    p_tokens = subparsers.add_parser("tokens", help="Show token usage")
    p_tokens.set_defaults(func=cmd_tokens)

    # commit
    p_commit = subparsers.add_parser("commit", help="Generate commit message")
    p_commit.add_argument("--copy", "-c", action="store_true", help="Copy to clipboard")
    p_commit.set_defaults(func=cmd_commit)

    # agents
    p_agents = subparsers.add_parser("agents", help="List agents")
    p_agents.set_defaults(func=cmd_agents)

    # skills
    p_skills = subparsers.add_parser("skills", help="List skills")
    p_skills.set_defaults(func=cmd_skills)

    # help
    p_help = subparsers.add_parser("help", help="Show help")
    p_help.set_defaults(func=cmd_help)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
