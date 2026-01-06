#!/usr/bin/env python3
"""
Maestro Auto-Update System - Safe GitHub repository synchronization

This script handles:
- Checking for updates on GitHub
- Safely pulling changes with local change protection
- Handling remote file deletions
- Automatic reinstallation after update
- Rollback on failure

Usage:
    python auto_update.py check           # Check for updates
    python auto_update.py update          # Update to latest
    python auto_update.py update --force  # Force update (discards local changes)
    python auto_update.py status          # Show update status
"""

import os
import sys
import json
import subprocess
import shutil
import platform
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

# Check for Rich library
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Confirm, Prompt
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


class UpdateStatus(Enum):
    """Update status enum."""
    UP_TO_DATE = "up_to_date"
    UPDATE_AVAILABLE = "update_available"
    ERROR = "error"
    HAS_LOCAL_CHANGES = "has_local_changes"


@dataclass
class UpdateInfo:
    """Update information."""
    current_commit: str
    remote_commit: str
    current_version: str
    remote_version: str
    local_changes: List[str]
    remote_changes: List[str]
    deleted_files: List[str]
    status: UpdateStatus
    behind_by: int = 0


class MaestroUpdater:
    """Maestro Auto-Updater with safe operations."""

    # Maestro-specific paths and files to update
    MAESTRO_PATHS = ('agents/', 'commands/', 'scripts/', 'skills/')
    MAESTRO_FILES = ('CHANGELOG.md', 'CLAUDE.md', 'Makefile')

    # User's .claude directory for syncing updates
    USER_CLAUDE_DIR = Path.home() / ".claude"

    def __init__(self, repo_dir: Optional[Path] = None, silent: bool = False, cwd: Optional[Path] = None):
        """Initialize updater.

        Args:
            repo_dir: Repository directory. Defaults to script parent's parent.
            silent: If True, suppress all output messages.
            cwd: Current working directory where notification file will be created.
        """
        if repo_dir is None:
            script_path = Path(__file__).resolve()
            self.repo_dir = script_path.parent.parent
        else:
            self.repo_dir = Path(repo_dir)

        self.silent = silent
        self.cwd = Path(cwd) if cwd else Path.cwd()  # User's current directory
        self.backup_dir = self.repo_dir / ".maestro_backup"
        self.metadata_file = self.repo_dir / ".maestro_update_metadata.json"

    def print_msg(self, msg: str, style: str = ""):
        """Print message with optional styling."""
        if self.silent:
            return
        if RICH_AVAILABLE and console:
            console.print(msg, style=style)
        else:
            print(msg)

    def print_error(self, msg: str):
        """Print error message."""
        self.print_msg(f"[red]Error:[/red] {msg}" if RICH_AVAILABLE else f"Error: {msg}")

    def print_success(self, msg: str):
        """Print success message."""
        self.print_msg(f"[green]{msg}[/green]" if RICH_AVAILABLE else msg)

    def print_warning(self, msg: str):
        """Print warning message."""
        self.print_msg(f"[yellow]Warning:[/yellow] {msg}" if RICH_AVAILABLE else f"Warning: {msg}")

    def _run_git_command(self, args: List[str], capture: bool = True) -> Tuple[bool, str]:
        """Run git command and return (success, output).

        Args:
            args: Git command arguments
            capture: Whether to capture output

        Returns:
            Tuple of (success boolean, output string)
        """
        try:
            cmd = ["git"] + args
            result = subprocess.run(
                cmd,
                cwd=self.repo_dir,
                capture_output=capture,
                text=True,
                check=False
            )

            if capture:
                output = result.stdout.strip() or result.stderr.strip()
                return result.returncode == 0, output
            else:
                return result.returncode == 0, ""

        except Exception as e:
            return False, str(e)

    def _get_current_commit(self) -> str:
        """Get current git commit hash."""
        success, output = self._run_git_command(["rev-parse", "HEAD"])
        return output if success else "unknown"

    def _get_remote_commit(self) -> str:
        """Get remote HEAD commit hash."""
        success, output = self._run_git_command(["ls-remote", "origin", "HEAD"])
        if success and output:
            return output.split()[0]
        return "unknown"

    def _get_local_changes(self) -> List[str]:
        """Get list of locally changed files."""
        success, output = self._run_git_command(["status", "--porcelain"])
        if success and output:
            return [line.strip() for line in output.split("\n") if line.strip()]
        return []

    def _filter_maestro_files(self, files: List[str]) -> List[str]:
        """Filter files to only Maestro-specific paths and files.

        Args:
            files: List of file paths to filter

        Returns:
            Filtered list containing only Maestro files
        """
        return [
            f for f in files
            if f.startswith(self.MAESTRO_PATHS) or
            any(f == mf or f.startswith(mf) for mf in self.MAESTRO_FILES)
        ]

    def _get_remote_changes(self) -> Tuple[List[str], List[str], int]:
        """Get list of changed and deleted files from remote.

        Returns:
            Tuple of (changed_files, deleted_files, commits_behind)
        """
        # Fetch first to get latest info
        self._run_git_command(["fetch", "origin"], capture=False)

        # Get commits behind
        success, behind_output = self._run_git_command(["rev-list", "--count", "HEAD..origin/main"])
        behind = int(behind_output) if success and behind_output.isdigit() else 0

        if behind == 0:
            return [], [], 0

        # Get changed files (what would be updated)
        success, changes = self._run_git_command(["diff", "--name-only", "HEAD", "origin/main"])
        changed_files = changes.split("\n") if success and changes else []

        # Get deleted files (files in local but not in remote)
        success, deleted = self._run_git_command([
            "diff", "--name-only", "--diff-filter=D", "HEAD", "origin/main"
        ])
        deleted_files = deleted.split("\n") if success and deleted else []

        # Filter to only Maestro-specific files
        changed_files = self._filter_maestro_files(changed_files)
        deleted_files = self._filter_maestro_files(deleted_files)

        return changed_files, deleted_files, behind

    def _get_version_info(self) -> Tuple[str, str]:
        """Get current and remote version from git tags or commits.

        Returns:
            Tuple of (current_version, remote_version)
        """
        # Try to get latest tag
        success, current_tag = self._run_git_command(["describe", "--tags", "--abbrev=0"])
        if not success:
            current_tag = self._get_current_commit()[:8]

        success, remote_tag = self._run_git_command(["describe", "--tags", "--abbrev=0", "origin/main"])
        if not success:
            remote_tag = self._get_remote_commit()[:8]

        return current_tag, remote_tag

    def _create_backup(self) -> bool:
        """Create backup of critical files before update.

        Returns:
            True if backup successful
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / timestamp
            backup_path.mkdir(parents=True, exist_ok=True)

            # Files to backup
            critical_files = [
                "CLAUDE.md",
                "CODEBASE.md",
                ".git",
            ]

            # Backup scripts
            scripts_dir = self.repo_dir / "scripts"
            if scripts_dir.exists():
                shutil.copytree(scripts_dir, backup_path / "scripts", dirs_exist_ok=True)

            # Backup settings
            settings_file = Path.home() / ".claude" / "settings.json"
            if settings_file.exists():
                shutil.copy2(settings_file, backup_path / "settings.json")

            # Save metadata
            metadata = {
                "timestamp": timestamp,
                "commit": self._get_current_commit(),
                "backup_path": str(backup_path)
            }
            self.metadata_file.write_text(json.dumps(metadata, indent=2))

            return True

        except Exception as e:
            self.print_error(f"Backup failed: {e}")
            return False

    def _rollback(self) -> bool:
        """Rollback to previous state using backup.

        Returns:
            True if rollback successful
        """
        try:
            if not self.metadata_file.exists():
                self.print_error("No backup metadata found")
                return False

            metadata = json.loads(self.metadata_file.read_text())
            backup_path = Path(metadata.get("backup_path", ""))
            previous_commit = metadata.get("commit", "")

            if not backup_path.exists():
                self.print_error(f"Backup not found: {backup_path}")
                return False

            self.print_warning("Rolling back to previous state...")

            # Reset to previous commit
            success, _ = self._run_git_command(["reset", "--hard", previous_commit])
            if not success:
                self.print_error("Git reset failed")
                return False

            # Restore scripts from backup
            scripts_backup = backup_path / "scripts"
            if scripts_backup.exists():
                local_scripts = self.repo_dir / "scripts"
                shutil.copytree(scripts_backup, local_scripts, dirs_exist_ok=True)

            # Restore settings
            settings_backup = backup_path / "settings.json"
            if settings_backup.exists():
                local_settings = Path.home() / ".claude" / "settings.json"
                shutil.copy2(settings_backup, local_settings)

            self.print_success("Rollback completed")
            return True

        except Exception as e:
            self.print_error(f"Rollback failed: {e}")
            return False

    def _handle_local_changes(self, local_changes: List[str], force: bool = False) -> bool:
        """Handle local changes before update.

        Args:
            local_changes: List of changed files
            force: If True, discard local changes

        Returns:
            True if safe to proceed
        """
        if not local_changes:
            return True

        self.print_warning(f"Found {len(local_changes)} local change(s):")

        for change in local_changes[:10]:  # Show first 10
            status = change[:2]
            file = change[3:]
            status_icon = {"M": "Modified", "A": "Added", "D": "Deleted", "??": "Untracked"}.get(status, status)
            self.print_msg(f"  [{status_icon}] {file}")

        if len(local_changes) > 10:
            self.print_msg(f"  ... and {len(local_changes) - 10} more")

        print()

        if force:
            self.print_warning("--force specified, discarding local changes")
            return True

        if RICH_AVAILABLE:
            proceed = Confirm.ask(
                "How would you like to proceed?",
                default=True
            )

            if not proceed:
                return False

            choice = Prompt.ask(
                "Choose option",
                choices=["stash", "commit", "discard"],
                default="stash"
            )
        else:
            print("Choose option:")
            print("  1. stash    - Stash changes temporarily")
            print("  2. commit   - Commit changes first")
            print("  3. discard  - Discard local changes")
            print()

            response = input("Your choice [stash]: ").strip().lower()
            choice = response or "stash"

        if choice == "stash":
            success, _ = self._run_git_command(["stash", "save", f"maestro_auto_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}"])
            if success:
                self.print_success("Changes stashed. Use 'git stash pop' after update to restore.")
                return True
            else:
                self.print_error("Stash failed")
                return False

        elif choice == "commit":
            self.print_warning("Please commit your changes first, then run update again.")
            return False

        elif choice == "discard":
            success, _ = self._run_git_command(["reset", "--hard", "HEAD"])
            # Only clean Maestro-specific paths
            for path in self.MAESTRO_PATHS:
                self._run_git_command(["clean", "-fd", path.rstrip('/')])
            if success:
                self.print_success("Local changes discarded")
                return True
            else:
                self.print_error("Discard failed")
                return False

        return False

    def _perform_update(self) -> bool:
        """Perform the actual update operation.

        Returns:
            True if update successful
        """
        try:
            self.print_msg("\n[cyan]Pulling updates from GitHub...[/cyan]" if RICH_AVAILABLE else "Pulling updates from GitHub...")

            # Pull with rebase to maintain clean history
            success, output = self._run_git_command(["pull", "--rebase", "origin", "main"])
            if not success:
                self.print_error(f"Git pull failed: {output}")
                return False

            # Clean up deleted files (only Maestro-specific paths)
            self.print_msg("\n[cyan]Cleaning up deleted files...[/cyan]" if RICH_AVAILABLE else "Cleaning up deleted files...")
            for path in self.MAESTRO_PATHS:
                self._run_git_command(["clean", "-fd", path.rstrip('/')])

            # Reinstall if setup.py exists
            setup_script = self.repo_dir / "scripts" / "setup.py"
            if setup_script.exists():
                self.print_msg("\n[cyan]Reinstalling Maestro...[/cyan]" if RICH_AVAILABLE else "Reinstalling Maestro...")
                result = subprocess.run(
                    [sys.executable, str(setup_script), "--quick"],
                    cwd=self.repo_dir,
                    capture_output=True
                )
                if result.returncode == 0:
                    self.print_success("Reinstallation complete")
                else:
                    self.print_warning("Reinstallation had issues (may be okay)")

            return True

        except Exception as e:
            self.print_error(f"Update failed: {e}")
            return False

    def _sync_to_user_claude_dir(self, info: UpdateInfo):
        """Sync updated files to user's .claude directory.

        This ensures updates from the repo are reflected in the user's local
        .claude directory (agents/, skills/, scripts/, etc.)

        Args:
            info: UpdateInfo with changed/deleted files
        """
        try:
            user_claude_dir = self.USER_CLAUDE_DIR
            if not user_claude_dir.exists():
                return  # No .claude dir, skip sync

            # Sync updated files
            for rel_path in info.remote_changes:
                src = self.repo_dir / rel_path
                dst = user_claude_dir / rel_path

                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)

            # Remove deleted files
            for rel_path in info.deleted_files:
                dst = user_claude_dir / rel_path
                if dst.exists():
                    dst.unlink()
                    # Remove empty parent directories
                    try:
                        dst.parent.rmdir()
                    except OSError:
                        pass  # Directory not empty, skip

        except Exception as e:
            # Don't fail the update if sync fails
            if not self.silent:
                self.print_warning(f"Could not sync to user directory: {e}")

    def sync_all(self) -> bool:
        """Sync ALL Maestro files from repo to user's .claude directory.

        This copies all agents, skills, scripts, commands to user's .claude
        directory regardless of update status.

        Returns:
            True if sync successful
        """
        try:
            user_claude_dir = self.USER_CLAUDE_DIR
            user_claude_dir.mkdir(parents=True, exist_ok=True)

            synced_count = 0
            deleted_count = 0

            self.print_msg("\n[cyan]Syncing Maestro files...[/cyan]" if RICH_AVAILABLE else "Syncing Maestro files...")

            # Sync directories
            for dir_path in self.MAESTRO_PATHS:
                src_dir = self.repo_dir / dir_path.rstrip('/')
                dst_dir = user_claude_dir / dir_path.rstrip('/')

                if src_dir.exists():
                    # Copy entire directory
                    for src_file in src_dir.rglob('*'):
                        if src_file.is_file():
                            rel_path = src_file.relative_to(src_dir)
                            dst_file = dst_dir / rel_path
                            dst_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(src_file, dst_file)
                            synced_count += 1

            # Sync individual files
            for file_name in self.MAESTRO_FILES:
                src_file = self.repo_dir / file_name
                dst_file = user_claude_dir / file_name

                if src_file.exists():
                    shutil.copy2(src_file, dst_file)
                    synced_count += 1

            # Create notification in user's current directory
            self._create_sync_notification(synced_count, deleted_count)

            self.print_success(f"Synced {synced_count} files to {user_claude_dir}")
            return True

        except Exception as e:
            self.print_error(f"Sync failed: {e}")
            return False

    def _create_sync_notification(self, synced: int, deleted: int):
        """Create sync notification file."""
        try:
            notification_file = self.cwd / "update_notification.txt"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            content = f"""# Maestro Update

🔄 Maestro files synced successfully!

📅 Date: {timestamp}
📁 Synced: {synced} files
🗑️ Removed: {deleted} files
📂 Target: {self.USER_CLAUDE_DIR}

---
This file was auto-generated by Maestro Sync.
You can safely delete this file.
"""
            notification_file.write_text(content, encoding="utf-8")
        except Exception:
            pass  # Ignore notification errors

    def _create_update_notification(self, info: UpdateInfo):
        """Create update notification file in user's current working directory.

        Args:
            info: UpdateInfo with update details
        """
        try:
            notification_file = self.cwd / "update_notification.txt"

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            content = f"""# Maestro Update

🎉 Maestro has been updated successfully!

📅 Date: {timestamp}
📦 Version: {info.current_version} → {info.remote_version}
📊 Commits: {info.behind_by} new commit(s)

"""
            if info.remote_changes:
                content += "## Updated Files\n"
                for f in info.remote_changes[:20]:
                    content += f"  ✓ {f}\n"
                if len(info.remote_changes) > 20:
                    content += f"  ... and {len(info.remote_changes) - 20} more\n"
                content += "\n"

            if info.deleted_files:
                content += "## Removed Files\n"
                for f in info.deleted_files[:10]:
                    content += f"  ✗ {f}\n"
                if len(info.deleted_files) > 10:
                    content += f"  ... and {len(info.deleted_files) - 10} more\n"
                content += "\n"

            content += """---
This file was auto-generated by Maestro Auto-Update.
You can safely delete this file.
"""

            notification_file.write_text(content, encoding="utf-8")

        except Exception as e:
            # Don't fail the update if notification fails
            if not self.silent:
                self.print_warning(f"Could not create notification file: {e}")

    def check_for_updates(self) -> UpdateInfo:
        """Check for available updates.

        Returns:
            UpdateInfo with status and details
        """
        current_commit = self._get_current_commit()
        remote_commit = self._get_remote_commit()
        current_version, remote_version = self._get_version_info()
        local_changes = self._get_local_changes()
        changed_files, deleted_files, behind = self._get_remote_changes()

        status = UpdateStatus.UP_TO_DATE
        if behind > 0:
            status = UpdateStatus.UPDATE_AVAILABLE
        elif local_changes:
            status = UpdateStatus.HAS_LOCAL_CHANGES

        return UpdateInfo(
            current_commit=current_commit,
            remote_commit=remote_commit,
            current_version=current_version,
            remote_version=remote_version,
            local_changes=local_changes,
            remote_changes=changed_files,
            deleted_files=deleted_files,
            status=status,
            behind_by=behind
        )

    def display_update_info(self, info: UpdateInfo):
        """Display update information to user.

        Args:
            info: UpdateInfo to display
        """
        if not RICH_AVAILABLE or not console:
            self._display_simple_update_info(info)
            return

        if info.status == UpdateStatus.UP_TO_DATE:
            console.print(Panel(
                "[bold green]✓ Up to Date[/bold green]\n\n"
                f"Current version: [cyan]{info.current_version}[/cyan]\n"
                f"Commit: [dim]{info.current_commit[:8]}[/dim]",
                title="Update Status",
                border_style="green"
            ))
            return

        # Build status table
        table = Table(title="Update Available", show_header=True)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Current Version", f"[dim]{info.current_version}[/dim]")
        table.add_row("Latest Version", f"[green]{info.remote_version}[/green]")
        table.add_row("Commits Behind", f"[yellow]{info.behind_by}[/yellow]")

        if info.local_changes:
            table.add_row("Local Changes", f"[red]{len(info.local_changes)} files[/red]")
        else:
            table.add_row("Local Changes", "[green]None[/green]")

        console.print(table)

        # Show file changes
        if info.remote_changes:
            console.print(f"\n[bold]Files to update:[/bold] [cyan]{len(info.remote_changes)}[/cyan]")
            for file in info.remote_changes[:10]:
                console.print(f"  • {file}")
            if len(info.remote_changes) > 10:
                console.print(f"  ... and {len(info.remote_changes) - 10} more")

        # Show deleted files
        if info.deleted_files:
            console.print(f"\n[bold red]Files to be deleted locally:[/bold red] [red]{len(info.deleted_files)}[/red]")
            for file in info.deleted_files[:10]:
                console.print(f"  • [red]{file}[/red]")
            if len(info.deleted_files) > 10:
                console.print(f"  ... and {len(info.deleted_files) - 10} more")

    def _display_simple_update_info(self, info: UpdateInfo):
        """Display update info without Rich."""
        if info.status == UpdateStatus.UP_TO_DATE:
            print("\n✓ Up to Date")
            print(f"Current version: {info.current_version}")
            print(f"Commit: {info.current_commit[:8]}")
            return

        print(f"\nUpdate Available!")
        print(f"Current: {info.current_version}")
        print(f"Latest:  {info.remote_version}")
        print(f"Behind:  {info.behind_by} commits")

        if info.local_changes:
            print(f"Local changes: {len(info.local_changes)} files")

        if info.remote_changes:
            print(f"\nFiles to update: {len(info.remote_changes)}")
            for file in info.remote_changes[:5]:
                print(f"  • {file}")

        if info.deleted_files:
            print(f"\nFiles to be deleted: {len(info.deleted_files)}")
            for file in info.deleted_files[:5]:
                print(f"  • {file}")

    def update(self, force: bool = False, silent: bool = False) -> bool:
        """Perform update to latest version.

        Args:
            force: If True, discard local changes without asking
            silent: If True, suppress all output (for auto-update from hooks)

        Returns:
            True if update successful
        """
        # Check for updates
        info = self.check_for_updates()

        if info.status == UpdateStatus.UP_TO_DATE:
            if not silent:
                self.display_update_info(info)
            return True

        if not silent:
            self.display_update_info(info)

        # Handle local changes
        if not self._handle_local_changes(info.local_changes, force):
            if not silent:
                self.print_warning("Update cancelled")
            return False

        # Show deleted files warning (only if not force and not silent)
        if info.deleted_files and not force and not silent:
            self.print_warning(f"\n⚠️  {len(info.deleted_files)} file(s) will be deleted from your local system:")
            for file in info.deleted_files[:5]:
                self.print_msg(f"    [red]• {file}[/red]" if RICH_AVAILABLE else f"    • {file}")
            if len(info.deleted_files) > 5:
                self.print_msg(f"    ... and {len(info.deleted_files) - 5} more")

            if RICH_AVAILABLE:
                proceed = Confirm.ask("\nContinue with deletion?", default=True)
            else:
                response = input("\nContinue with deletion? [Y/n]: ").strip().lower()
                proceed = response in ("", "y", "yes")

            if not proceed:
                self.print_warning("Update cancelled")
                return False

        # Create backup
        if not silent:
            self.print_msg("\n[cyan]Creating backup...[/cyan]" if RICH_AVAILABLE else "Creating backup...")
        if not self._create_backup():
            if not silent:
                self.print_warning("Backup failed, proceeding anyway...")

        # Perform update
        if not self._perform_update():
            if not silent:
                self.print_error("\nUpdate failed! Attempting rollback...")
            self._rollback()
            return False

        # Sync updates to user's .claude directory
        self._sync_to_user_claude_dir(info)

        # Create notification file in user's current working directory
        self._create_update_notification(info)

        # Success message
        if not silent:
            if RICH_AVAILABLE:
                console.print(Panel(
                    "[bold green]✓ Update Complete![/bold green]\n\n"
                    f"Updated from [dim]{info.current_version}[/dim] to [cyan]{info.remote_version}[/cyan]\n\n"
                    "[dim]Backup saved to: .maestro_backup/[/dim]\n"
                    "[yellow]Please restart Claude Code CLI[/yellow]",
                    title="Success",
                    border_style="green"
                ))
            else:
                print("\n" + "=" * 50)
                print("✓ Update Complete!")
                print(f"Updated from {info.current_version} to {info.remote_version}")
                print("Backup saved to: .maestro_backup/")
                print("Please restart Claude Code CLI")
                print("=" * 50)

        return True


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Maestro Auto-Update System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python auto_update.py check              # Check for updates
  python auto_update.py update             # Update to latest
  python auto_update.py update --force     # Force update (discards local changes)
  python auto_update.py update --silent    # Silent update (no output)
        """
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="status",
        choices=["check", "update", "status", "sync"],
        help="Command to run"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force update, discarding local changes"
    )
    parser.add_argument(
        "--silent", "-s",
        action="store_true",
        help="Silent mode (no output, for automation)"
    )
    parser.add_argument(
        "--repo-dir",
        type=Path,
        help="Repository directory (default: auto-detected)"
    )
    parser.add_argument(
        "--cwd",
        type=Path,
        help="Current working directory for notification file (default: current dir)"
    )

    args = parser.parse_args()

    updater = MaestroUpdater(args.repo_dir, silent=args.silent, cwd=args.cwd)

    if args.command == "check":
        info = updater.check_for_updates()
        updater.display_update_info(info)
        sys.exit(0 if info.status != UpdateStatus.ERROR else 1)

    elif args.command == "update":
        success = updater.update(force=args.force, silent=args.silent)
        sys.exit(0 if success else 1)

    elif args.command == "sync":
        success = updater.sync_all()
        sys.exit(0 if success else 1)

    else:  # status
        info = updater.check_for_updates()
        updater.display_update_info(info)
        sys.exit(0 if info.status != UpdateStatus.ERROR else 1)


if __name__ == "__main__":
    main()
