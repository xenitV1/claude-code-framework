# Scripts

Python automation scripts for hooks and utilities.

## Hook Scripts

These run automatically via `settings.json` hooks:

| Script | Hook | Purpose |
|--------|------|---------|
| [session_hooks.py](session_hooks.py) | SessionStart/End | Project detection, session tracking |
| [pre_bash.py](pre_bash.py) | PreToolUse | Error learning - warns about known issues |
| [check_prevention.py](check_prevention.py) | PreToolUse | Blocks dangerous commands |
| [track_error.py](track_error.py) | PostToolUse | Records errors for learning |

## Utility Scripts

| Script | Purpose |
|--------|---------|
| [progress_reporter.py](progress_reporter.py) | Agent status board (rich UI) |
| [session_manager.py](session_manager.py) | Project state management |
| [auto_preview.py](auto_preview.py) | Preview server control |
| [explorer_helper.py](explorer_helper.py) | Automatic codebase discovery |

## Usage

### Hook Scripts (automatic)
```bash
# Configured in settings.json, runs automatically
python session_hooks.py start
python pre_bash.py "npm install package"
python track_error.py "command" "exit_code" "output"
```

### Utility Scripts (manual)
```bash
# Progress reporter
python progress_reporter.py status

# Session manager
python session_manager.py init --path /project --type nextjs
python session_manager.py status

# Auto preview
python auto_preview.py start
python auto_preview.py stop
python auto_preview.py status
```

## Dependencies

```bash
pip install rich pydantic
```

- **rich**: Beautiful terminal output
- **pydantic**: Type-safe data models

## Data Files

Scripts read/write to `~/.claude/data/`:
- `error-tracker.json` - Project-based error history
- `session-stats.json` - Session metadata per project
- `current-project.json` - Global project reference
- `discovery-report.json` - Project structure analysis

---

# 🔄 Hook System Architecture

## System Flow Diagram

```mermaid
flowchart TD
    Start([User runs: claude]) --> Init[Claude Code CLI Starts]
    Init --> LoadSettings[Load ~/.claude/settings.json]
    LoadSettings --> CheckHooks{Hooks Configured?}
    
    CheckHooks -->|No| NoHooks[Run without hooks]
    CheckHooks -->|Yes| SessionStart[ğŸ¯ SessionStart Hook Triggered<br/>matcher: startup]
    
    SessionStart --> Hook1[ğŸ“ Hook 1: session_hooks.py start]
    SessionStart --> Hook2[ğŸ“ Hook 2: explorer_helper.py]
    
    Hook1 --> DetectProject[ğŸ” Detect Project Type<br/>- Recursive search<br/>- Find package.json<br/>- Find requirements.txt<br/>- Max depth: 3]
    
    DetectProject --> ProjectFound{Project Found?}
    ProjectFound -->|Yes| AnalyzeProject[ğŸ“Š Analyze Project<br/>- Framework detection<br/>- Platform detection<br/>- Dependencies]
    ProjectFound -->|No| NullAnalysis[Return null analysis]
    
    AnalyzeProject --> CreateDataDir[ğŸ“ Create Project Data Dir<br/>~/.claude/data/projects/project-name/]
    NullAnalysis --> CreateDataDir
    
    CreateDataDir --> SaveStats[ğŸ’¾ Save session-stats.json<br/>- projectPath<br/>- projectName<br/>- timestamp<br/>- analysis<br/>- recentErrors]
    
    SaveStats --> SaveGlobalRef[ğŸŒ Save current-project.json<br/>~/.claude/data/<br/>- projectPath<br/>- dataDir<br/>- lastAccess]
    
    Hook2 --> ScanProject[ğŸ” Deep Project Scan<br/>- Tech stack detection<br/>- Entry points<br/>- Dependencies<br/>- Directory structure]
    
    ScanProject --> SaveReport[ğŸ“„ Save discovery-report.json<br/>~/.claude/data/projects/project-name/<br/>- root<br/>- tech_stack<br/>- entry_points<br/>- structure]
    
    SaveGlobalRef --> HooksComplete[âœ… SessionStart Hooks Complete]
    SaveReport --> HooksComplete
    
    HooksComplete --> WaitUser[â¸ï¸ Wait for User Input]
    NoHooks --> WaitUser
    
    WaitUser --> UserCommand{User Action}
    
    UserCommand -->|Chat Message| AIResponse[ğŸ¤– AI Response]
    UserCommand -->|Bash Command| PreToolHook[âš¡ PreToolUse Hook<br/>matcher: Bash]
    
    PreToolHook --> PreBash[ğŸ“ pre_bash.py<br/>Check error history]
    PreToolHook --> CheckPrevention[ğŸ“ check_prevention.py<br/>Block dangerous commands]
    
    PreBash --> LoadErrorTracker[ğŸ“– Load error-tracker.json<br/>~/.claude/data/projects/project-name/]
    LoadErrorTracker --> CheckSimilar{Similar Error<br/>Found?}
    
    CheckSimilar -->|Yes| WarnUser[âš ï¸ Warn User<br/>- Past error pattern<br/>- Suggested solution]
    CheckSimilar -->|No| AllowCommand
    
    CheckPrevention --> DangerousCheck{Dangerous<br/>Command?}
    DangerousCheck -->|Yes| BlockCommand[ğŸš« Block Command<br/>Return error]
    DangerousCheck -->|No| AllowCommand[âœ… Allow Command]
    
    WarnUser --> AllowCommand
    AllowCommand --> ExecuteBash[ğŸ’» Execute Bash Command]
    
    ExecuteBash --> CommandResult{Exit Code}
    
    CommandResult -->|0 Success| PostToolSuccess[âœ… PostToolUse Hook<br/>Success Path]
    CommandResult -->|Non-zero| PostToolError[âŒ PostToolUse Hook<br/>Error Path]
    
    PostToolSuccess --> TrackSuccess[ğŸ“ track_error.py<br/>Track successful execution]
    PostToolError --> TrackError[ğŸ“ track_error.py<br/>Record error details]
    
    TrackError --> ParseError[ğŸ” Parse Error<br/>- Error type<br/>- Pattern extraction<br/>- Context]
    
    ParseError --> UpdateTracker[ğŸ’¾ Update error-tracker.json<br/>- errors[]<br/>- patterns<br/>- solutions]
    
    TrackSuccess --> ContinueSession
    UpdateTracker --> ContinueSession[Continue Session]
    
    AIResponse --> ContinueSession
    BlockCommand --> ContinueSession
    
    ContinueSession --> UserCommand
    
    UserCommand -->|/exit or Ctrl+C| SessionEndHook[ğŸ SessionEnd Hook<br/>matcher: empty]
    
    SessionEndHook --> EndScript[ğŸ“ session_hooks.py end]
    
    EndScript --> LoadSession[ğŸ“– Load session-stats.json]
    LoadSession --> CalcDuration[â±ï¸ Calculate Duration<br/>end - start time]
    CalcDuration --> UpdateEndTime[ğŸ’¾ Update Tracker<br/>lastSessionEnd timestamp]
    
    UpdateEndTime --> CleanupResources[ğŸ§¹ Cleanup Resources]
    CleanupResources --> Exit([ğŸ‘‹ Exit Claude Code])
    
    style SessionStart fill:#4CAF50,color:#fff
    style Hook1 fill:#2196F3,color:#fff
    style Hook2 fill:#2196F3,color:#fff
    style PreToolHook fill:#FF9800,color:#fff
    style PreBash fill:#FFC107,color:#000
    style CheckPrevention fill:#FFC107,color:#000
    style PostToolSuccess fill:#4CAF50,color:#fff
    style PostToolError fill:#F44336,color:#fff
    style TrackError fill:#E91E63,color:#fff
    style SessionEndHook fill:#9C27B0,color:#fff
    style CreateDataDir fill:#00BCD4,color:#fff
    style SaveStats fill:#00BCD4,color:#fff
```

## 📋 Detailed Component Breakdown

### 1. SessionStart Hook (Startup)

**Triggers:** When Claude Code starts
**Scripts:** 
- `session_hooks.py start --silent`
- `explorer_helper.py . --silent`

**Process:**
1. Detect current working directory
2. Recursively search for project files (depth: 3)
3. Identify framework (React Native, Next.js, Django, etc.)
4. Create project-specific data directory
5. Save session metadata
6. Scan project structure and dependencies

**Output:**
```
~/.claude/data/
â”œâ”€â”€ projects/
â”‚   â””â”€â”€ {project-name}/
â”‚       â”œâ”€â”€ session-stats.json
â”‚       â””â”€â”€ discovery-report.json
â””â”€â”€ current-project.json
```

---

### 2. PreToolUse Hook (Before Bash Command)

**Triggers:** Before any Bash command execution
**Scripts:**
- `pre_bash.py "$TOOL_INPUT"`
- `check_prevention.py "$TOOL_INPUT"`

**Process:**

#### pre_bash.py
1. Load project error tracker
2. Parse incoming command
3. Check against known error patterns
4. Warn user if similar error occurred before
5. Suggest solution from history

#### check_prevention.py
1. Parse command
2. Check against dangerous patterns:
   - `rm -rf /`
   - `sudo` without context
   - Unguarded destructive operations
3. Block if dangerous
4. Allow if safe

**Decision Tree:**
```
Bash Command â†’ pre_bash â†’ error history check â†’ warn if needed
            â†“
            check_prevention â†’ safety check â†’ block if dangerous
            â†“
            Execute if safe
```

---

### 3. Command Execution

**Normal Flow:**
```
PreToolUse Hooks â†’ Bash Execution â†’ Exit Code â†’ PostToolUse Hook
```

**Exit Codes:**
- `0` â†’ Success path
- `1-255` â†’ Error path

---

### 4. PostToolUse Hook (After Bash Command)

**Triggers:** After Bash command completes
**Script:** `track_error.py "$TOOL_INPUT" "$EXIT_CODE" "$TOOL_OUTPUT"`

**Process:**

#### On Success (Exit Code 0)
1. Log successful execution
2. Update success counter
3. Mark pattern as resolved (if previously errored)

#### On Error (Exit Code â‰  0)
1. Parse error output
2. Extract error type and pattern
3. Store in project error tracker
4. Link to command that caused it
5. Increment error counter

**Error Tracker Structure:**
```json
{
  "errors": [
    {
      "timestamp": "2025-12-30T...",
      "command": "npm install",
      "exitCode": 1,
      "errorType": "ENOENT",
      "pattern": "Cannot find module",
      "output": "...",
      "solution": "Run npm install first"
    }
  ],
  "patterns": {
    "ENOENT": 3,
    "ECONNREFUSED": 1
  },
  "lastSessionEnd": "2025-12-30T..."
}
```

---

### 5. SessionEnd Hook (Exit)

**Triggers:** When user exits Claude Code
**Script:** `session_hooks.py end --silent`

**Process:**
1. Load session start time from `session-stats.json`
2. Calculate total session duration
3. Update error tracker with session end timestamp
4. Output session summary (if not silent)

**Output Example:**
```
âœ… Session completed
â±ï¸ Duration: 0:45:23
```

---

## ğŸ—„ï¸ Data Storage Structure

```
~/.claude/data/
â”œâ”€â”€ projects/
â”‚   â”œâ”€â”€ project-a/
â”‚   â”‚   â”œâ”€â”€ session-stats.json        # Session metadata
â”‚   â”‚   â”œâ”€â”€ discovery-report.json     # Project structure
â”‚   â”‚   â””â”€â”€ error-tracker.json        # Error history
â”‚   â”‚
â”‚   â””â”€â”€ project-b/
â”‚       â”œâ”€â”€ session-stats.json
â”‚       â”œâ”€â”€ discovery-report.json
â”‚       â””â”€â”€ error-tracker.json
â”‚
â”œâ”€â”€ current-project.json              # Global reference
â””â”€â”€ hook_debug.log                    # Debug log
```

---

## ğŸ” Security & Safety Features

1. **Command Prevention:** Blocks destructive commands
2. **Error Learning:** Warns about repeated mistakes
3. **Project Isolation:** Separate data per project
4. **Silent Mode:** No user interruption
5. **Debug Logging:** Full audit trail

---

## ğŸ¯ Key Benefits

âœ… **Automatic Project Detection** - No manual configuration
âœ… **Error Prevention** - Learn from past mistakes
âœ… **Project Context** - Remembers each project separately
âœ… **Zero User Intervention** - Runs silently in background
âœ… **Debugging Support** - Full logging for troubleshooting

---

## ğŸ› Known Limitations (Claude Code v2.0.64)

1. **SessionStart Context Issue:** Output not injected into new conversations
   - **Workaround:** Use `/clear` or `/compact` to trigger properly

2. **Hook Output Visibility:** Only visible with `--debug` flag
   - **Workaround:** Run `claude --debug` to see execution

3. **Matcher Required:** Must use `matcher` + `hooks` structure
   - **Solution:** See [HOOKS-TROUBLESHOOTING.md](HOOKS-TROUBLESHOOTING.md)

---

**Last Updated:** 2025-12-30  
**Version:** 1.0  
**Claude Code:** v2.0.64
