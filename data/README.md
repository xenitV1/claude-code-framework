# Data

Runtime data and state files for the framework.

## Files

| File | Purpose | Updated By |
|------|---------|------------|
| `error-database.json` | Learned errors for prevention | track_error.py, pre_bash.py |
| `error-tracker.json` | Prevention rules | track_error.py |
| `session-stats.json` | Current session info | session_hooks.py |

## Directories

| Directory | Purpose |
|-----------|---------|
| `sessions/` | Session history |
| `patterns/` | Error patterns |

## Format Examples

### error-database.json
```json
{
  "version": "1.0",
  "errors": [
    {
      "id": "uuid",
      "command": "npm install broken",
      "pattern": "npm install {package}",
      "errorMessage": "npm ERR! 404 Not Found",
      "errorType": "NPM_ERROR",
      "suggestion": "npm cache clean --force",
      "occurrences": 2,
      "status": "pending"
    }
  ],
  "lastUpdated": "2025-12-30T09:00:00Z"
}
```

### session-stats.json
```json
{
  "projectPath": "C:/projects/my-app",
  "projectName": "my-app",
  "timestamp": "2025-12-30T09:00:00Z",
  "analysis": {
    "projectType": "node",
    "framework": "nextjs",
    "platform": "web"
  }
}
```

## Notes

- All files are JSON format
- Scripts handle missing files gracefully
- UTF-8-sig encoding for Windows compatibility
