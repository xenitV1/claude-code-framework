---
description: Check and apply Maestro updates from GitHub. Run to sync latest agents, skills, and scripts.
---

# /up - Maestro Update

$ARGUMENTS

---

## Task

Check for Maestro updates from GitHub and apply them.

### What It Does

1. **Check GitHub** for new commits
2. **Display** what files will be updated
3. **Pull** changes with automatic backup
4. **Sync** files to user's `.claude` directory
5. **Create** `update_notification.txt` in current directory

---

## Usage

```bash
/up              # Interactive update (confirms before applying)
/up --force      # Force update without prompts
/up check        # Only check if updates available
```

---

## How to Run

Execute the update script:

```powershell
# Windows
python "%USERPROFILE%\.claude\scripts\auto_update.py" update

# macOS/Linux
python ~/.claude/scripts/auto_update.py update
```

Or check status first:

```powershell
python "%USERPROFILE%\.claude\scripts\auto_update.py" check
```

---

## Example Output

```
┌─ Update Available ─┐
│                    │
│ Current: v1.2.0    │
│ Latest:  v1.3.0    │
│ Behind:  5 commits │
│                    │
└────────────────────┘

Files to update: 12
  • agents/frontend-specialist.md
  • agents/backend-specialist.md
  • skills/nextjs/SKILL.md
  • skills/react/SKILL.md
  • scripts/setup.py
  ... and 7 more

Continue with update? [Y/n]: Y

✓ Update Complete!
Updated from v1.2.0 to v1.3.0
Backup saved to: .maestro_backup/
Notification saved to: update_notification.txt
```

---

## Notification File

After update, `update_notification.txt` is created in your current directory:

```
# Maestro Update

🎉 Maestro has been updated successfully!

📅 Date: 2026-01-06 14:45:00
📦 Version: v1.2.0 → v1.3.0
📊 Commits: 5 new commit(s)

## Updated Files
  ✓ agents/frontend-specialist.md
  ✓ agents/backend-specialist.md
  ...
```

---

## What Gets Synced

- `agents/` - All agent definitions
- `skills/` - All skill files
- `scripts/` - Helper scripts
- `commands/` - Slash commands
- `CLAUDE.md`, `CHANGELOG.md`
- Settings examples

---

## Safety

- **Automatic backup** before every update
- **Local changes protected** (stash or commit option)
- **Rollback** available if update fails
