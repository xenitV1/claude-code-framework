import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich import print as rprint

console = Console()

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def lint_check(file_path):
    path = Path(file_path).absolute()
    if not path.exists():
        console.print(f"[bold red]❌ File not found:[/bold red] {file_path}")
        return
    
    ext = path.suffix.lower()
    project_root = path.parent
    for parent in path.parents:
        if (parent / ".git").exists() or (parent / "package.json").exists() or (parent / "pyproject.toml").exists():
            project_root = parent
            break

    console.print(Panel.fit(
        f"[bold cyan]Maestro Quality Audit V5[/bold cyan]\n"
        f"📁 [yellow]Target:[/yellow] {file_path}\n"
        f"🏠 [yellow]Root:[/yellow] {project_root}",
        title="🕵️ Audit Initiation", border_style="blue"
    ))
    
    results = {"errors": 0, "warnings": 0, "security_issues": 0}
    audit_table = Table(title="🔍 Audit Results", expand=True)
    audit_table.add_column("Tool", style="cyan")
    audit_table.add_column("Type", style="magenta")
    audit_table.add_column("Status", justify="center")
    audit_table.add_column("Details", style="white")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        if ext in ['.ts', '.tsx', '.js', '.jsx']:
            # ESLint
            progress.add_task(description="⚡ ESLint analysis...", total=None)
            code, out, err = run_command(f"npx eslint \"{path}\" --fix", cwd=project_root)
            status = "[green]✅ Clean[/green]" if code == 0 else "[red]❌ Issues[/red]"
            audit_table.add_row("ESLint", "Style/Logic", status, out[:100] + "..." if out else "Success")
            if code != 0: results["errors"] += 1

            # TypeScript
            if ext in ['.ts', '.tsx']:
                progress.add_task(description="⚡ TSC type check...", total=None)
                code, out, err = run_command("npx tsc --noEmit", cwd=project_root)
                status = "[green]✅ Valid[/green]" if code == 0 else "[red]❌ Errors[/red]"
                audit_table.add_row("TSC", "Types", status, out[:100] + "..." if out else "Success")
                if code != 0: results["errors"] += 1

            # Security
            progress.add_task(description="⚡ NPM Audit scan...", total=None)
            code, out, err = run_command("npm audit --audit-level=high", cwd=project_root)
            status = "[green]✅ Secure[/green]" if code == 0 else "[yellow]⚠️ Warning[/yellow]"
            audit_table.add_row("NPM Audit", "Security", status, "High vuln found" if code != 0 else "Clean")
            if code != 0: results["security_issues"] += 1

        elif ext == '.py':
            # Ruff
            progress.add_task(description="⚡ Ruff analysis...", total=None)
            code, out, err = run_command(f"ruff check \"{path}\" --fix", cwd=project_root)
            status = "[green]✅ Pass[/green]" if code == 0 else "[red]❌ Issues[/red]"
            audit_table.add_row("Ruff", "Logic/Style", status, out[:100] + "..." if out else "Success")
            if code != 0: results["errors"] += 1

            # Bandit
            progress.add_task(description="⚡ Bandit security scan...", total=None)
            code, out, err = run_command(f"bandit -r \"{path}\" -ll", cwd=project_root)
            status = "[green]✅ Secure[/green]" if code == 0 else "[red]🛡️ Threat[/red]"
            audit_table.add_row("Bandit", "Security", status, "Flaws detected" if code != 0 else "Clean")
            if code != 0: results["security_issues"] += 1

            # MyPy
            progress.add_task(description="⚡ MyPy type check...", total=None)
            code, out, err = run_command(f"mypy \"{path}\" --ignore-missing-imports", cwd=project_root)
            status = "[green]✅ Valid[/green]" if code == 0 else "[red]❌ Errors[/red]"
            audit_table.add_row("MyPy", "Types", status, out[:100] + "..." if out else "Success")
            if code != 0: results["errors"] += 1

    console.print(audit_table)

    # Summary Panel
    summary_color = "green" if results["errors"] == 0 and results["security_issues"] == 0 else "red"
    summary_text = "[bold]🌟 PERFECT:[/bold] Code meets all standards." if summary_color == "green" else \
                   f"[bold]⚠️ TOTAL ISSUES:[/bold] {results['errors'] + results['security_issues']}\n" \
                   f"Logic/Style: {results['errors']} | Security: {results['security_issues']}"
    
    console.print(Panel(summary_text, title="📊 Final Audit Report", border_style=summary_color))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        rprint("[bold yellow]Usage:[/bold yellow] python scripts/lint_check.py <file_path>")
        sys.exit(1)
    
    lint_check(sys.argv[1])
