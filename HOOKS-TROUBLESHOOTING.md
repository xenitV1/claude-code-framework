# Maestro Hooks Troubleshooting

## Problem: SessionStart/SessionEnd Hooks Not Working

If your hooks are not triggering when you run `claude`, follow these steps:

### Solution: Add `matcher` to Hook Configuration

**WRONG Format (Won't Work):**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "python script.py"
      }
    ]
  }
}
```

**CORRECT Format (Will Work):**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "python script.py"
          }
        ]
      }
    ]
  }
}
```

### How to Debug

1. **Run with debug flag:**
   ```bash
   claude --debug
   ```

2. **Check debug log:**
   - Location: `~/.claude/debug/[session-id].txt`
   - Look for: `Getting matching hook commands for SessionStart`
   - Should see: `Found 1 hook matchers` (not `Found 0`)

3. **Verify in Claude:**
   ```
   /hooks
   ```
   This command shows all configured hooks in the Claude interface.

---

## Hook Structure Reference

### macOS / Linux

#### SessionStart Hook
```json
"SessionStart": [
  {
    "matcher": "startup",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.claude/scripts/session_hooks.py start --silent"
      }
    ]
  }
]
```

#### SessionEnd Hook
```json
"SessionEnd": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.claude/scripts/session_hooks.py end --silent"
      }
    ]
  }
]
```

#### PreToolUse Hook
```json
"PreToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.claude/scripts/pre_bash.py \"$TOOL_INPUT\""
      }
    ]
  }
]
```

#### PostToolUse Hook
```json
"PostToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python3 ~/.claude/scripts/track_error.py \"$TOOL_INPUT\" \"$EXIT_CODE\" \"$TOOL_OUTPUT\""
      }
    ]
  }
]
```

---

### Windows

#### SessionStart Hook
```json
"SessionStart": [
  {
    "matcher": "startup",
    "hooks": [
      {
        "type": "command",
        "command": "python \"%USERPROFILE%\\.claude\\scripts\\session_hooks.py\" start --silent"
      }
    ]
  }
]
```

#### SessionEnd Hook
```json
"SessionEnd": [
  {
    "matcher": "",
    "hooks": [
      {
        "type": "command",
        "command": "python \"%USERPROFILE%\\.claude\\scripts\\session_hooks.py\" end --silent"
      }
    ]
  }
]
```

#### PreToolUse Hook
```json
"PreToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python \"%USERPROFILE%\\.claude\\scripts\\pre_bash.py\" \"$TOOL_INPUT\""
      }
    ]
  }
]
```

#### PostToolUse Hook
```json
"PostToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "python \"%USERPROFILE%\\.claude\\scripts\\track_error.py\" \"$TOOL_INPUT\" \"$EXIT_CODE\" \"$TOOL_OUTPUT\""
      }
    ]
  }
]
```

---

## 💡 Key Points

1. **`matcher` is required** for SessionStart/SessionEnd hooks
2. **`hooks` array** wraps the actual hook commands
3. **`type: "command"`** must be specified for each hook
4. **Path format by OS:**
   - macOS/Linux: Use `~/.claude/scripts/` and `python3`
   - Windows: Use `%USERPROFILE%\.claude\scripts\` and `python`
5. **Hook restart required:** Changes to hooks need Claude CLI restart

---

## Known Issues (Claude Code v2.0.64)

- **Issue #1:** SessionStart hooks don't inject context on NEW conversations
  - **Workaround:** Works with `/clear` or `/compact` commands

- **Issue #2:** Hook output only visible with `--verbose` flag
  - **Workaround:** Run `claude --debug` to see hook execution

- **Issue #3:** "Hook error" displayed even when hooks succeed
  - **Status:** UI display bug, hooks still work correctly

---

## Related GitHub Issues

- [#11939](https://github.com/anthropics/claude-code/issues/11939) - Local plugin SessionStart hooks not executing
- [#10373](https://github.com/anthropics/claude-code/issues/10373) - SessionStart output not processed in new conversations
- [#12671](https://github.com/anthropics/claude-code/issues/12671) - Hook error displayed despite success

---

## Still Not Working?

### macOS / Linux

1. Check Python is in PATH: `python3 --version`
2. Verify script exists: `ls ~/.claude/scripts/`
3. Test script manually:
   ```bash
   python3 ~/.claude/scripts/session_hooks.py start
   ```
4. Check settings.json syntax: Use a JSON validator
5. Create issue on [GitHub](https://github.com/anthropics/claude-code/issues)

### Windows

1. Check Python is in PATH: `python --version`
2. Verify script exists: `dir %USERPROFILE%\.claude\scripts\`
3. Test script manually:
   ```powershell
   python "$env:USERPROFILE\.claude\scripts\session_hooks.py" start
   ```
4. Check settings.json syntax: Use a JSON validator
5. Create issue on [GitHub](https://github.com/anthropics/claude-code/issues)

---

**Last Updated:** 2025-12-31
**Claude Code Version:** v2.0.64
**Platforms:** Windows, macOS, Linux
