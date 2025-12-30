---
name: terminal-error-patterns
description: Terminal Error Learning skill - common error patterns, solutions, and learning protocol for AI to prevent recurring errors. CRITICAL for Terminal Error Learning system.
---

# Terminal Error Patterns

## Overview
This skill enables AI to learn from terminal errors and prevent recurring mistakes. Part of the Terminal Error Learning system.

## Learning Protocol

When a terminal error occurs:

1. **Recognize** the error pattern
2. **Check** error-database.json for similar past errors
3. **Apply** known solutions if available
4. **Record** new errors and their solutions
5. **Alert** if error is recurring (3+ times)

## Common Error Patterns

### 1. File Not Found (ENOENT)
```
Error: ENOENT: no such file or directory
Cannot find module './path/to/file'
```

**Common Causes:**
- Wrong file path
- File not created yet
- Typo in path

**Solutions:**
- Check if file exists: `Test-Path ./file.js`
- Create the file first
- Verify import path

### 2. Permission Denied (EACCES)
```
Error: EACCES: permission denied
Access is denied
```

**Common Causes:**
- No write permission
- File locked by another process
- Directory not owned

**Solutions:**
- Run as administrator (Windows)
- Check file permissions
- Close other programs using file

### 3. NPM Errors
```
npm ERR! code ERESOLVE
npm ERR! peer dependencies
```

**Common Causes:**
- Conflicting dependencies
- Wrong Node version
- Corrupted node_modules

**Solutions:**
```bash
# Clear npm cache
npm cache clean --force

# Delete and reinstall
Remove-Item -Recurse node_modules, package-lock.json
npm install

# Try legacy peer deps
npm install --legacy-peer-deps
```

### 4. Module Not Found
```
Error: Cannot find module 'express'
Module not found: Can't resolve '@/components'
```

**Common Causes:**
- Package not installed
- Wrong import path
- TypeScript path alias not configured

**Solutions:**
- Install package: `npm install express`
- Check import path
- Verify tsconfig.json paths

### 5. Port Already in Use
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Common Causes:**
- Another instance running
- Previous server didn't stop
- Another app using port

**Solutions:**
```bash
# Windows: Find and kill process
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
$env:PORT=3001; npm run dev
```

### 6. Git Errors
```
fatal: not a git repository
error: failed to push some refs
```

**Common Causes:**
- Not in git repo
- Remote changes not pulled
- Branch protection

**Solutions:**
```bash
# Initialize repo
git init

# Pull before push
git pull origin main --rebase

# Check remote
git remote -v
```

### 7. TypeScript Errors
```
error TS2304: Cannot find name 'x'
error TS2307: Cannot find module
```

**Common Causes:**
- Missing type definitions
- Wrong tsconfig
- Missing import

**Solutions:**
```bash
# Install types
npm install @types/node @types/react

# Check tsconfig
npx tsc --noEmit
```

### 8. Build Errors
```
Build failed
Webpack error
```

**Common Causes:**
- Syntax error in code
- Module resolution issue
- Environment variable missing

**Solutions:**
- Check error location
- Fix syntax
- Verify .env file

## Error Database Schema

Errors are stored in `~/.claude/data/error-database.json`:

```json
{
  "version": "1.0",
  "errors": [
    {
      "id": "uuid",
      "command": "npm install express",
      "pattern": "npm install {package}",
      "errorMessage": "npm ERR! peer dependencies...",
      "errorType": "NPM_ERROR",
      "errorCategory": "NPM",
      "suggestion": "Try: npm install --legacy-peer-deps",
      "project": "C:/projects/myapp",
      "timestamp": "2025-01-01T12:00:00Z",
      "lastSeen": "2025-01-01T12:00:00Z",
      "solution": "Used --legacy-peer-deps flag",
      "status": "solved",
      "occurrences": 3
    }
  ],
  "lastUpdated": "2025-01-01T12:00:00Z"
}
```

## Status Values

- **pending**: Error recorded, solution not found yet
- **solved**: Error resolved, solution recorded
- **recurring**: Error happened 3+ times without resolution

## AI Instructions

When encountering an error:

1. **Before command execution**: Check pre-bash.ps1 output for warnings about similar past errors

2. **After error occurs**: 
   - Read the track-error.ps1 output
   - Note the suggested solution
   - Try the suggestion first

3. **When solved**: 
   - The system automatically marks as solved when same command succeeds
   - Document what worked in your response

4. **For recurring errors**:
   - Try a completely different approach
   - Ask user for guidance
   - Check external documentation

| Git fatal | Verify git repo status |
| TS error | npm install @types/* |

## Self-Healing & AI-Telemetry (2025)

### Automated Recovery
When an error matches a known pattern, the agent should:
1. **Analyze:** Check if it's a transient (network) or logical (code) error.
2. **Recover:** Auto-switch methods (e.g., if a command fails, try with an alternative tool/flag).
3. **Log:** Update the `error-database.json` with the self-healed outcome.

### Error Telemetry for Agents
Use AI to correlate terminal errors with:
- **Deployment metadata:** Did this start after commit `x`?
- **Prompt Injection checks:** Was the command altered by malicious input?
- **Environment drift:** Did a system update break a dependency?
