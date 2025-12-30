---
name: server-management
description: Server management procedures including PM2, monitoring, and log management. CRITICAL for production operations.
---

# Server Management

## PM2 Commands

### Process Management
```bash
# Start application
pm2 start ecosystem.config.js

# List processes
pm2 list

# Restart (zero-downtime)
pm2 reload app-name

# Stop
pm2 stop app-name

# Delete from PM2
pm2 delete app-name
```

### Monitoring
```bash
# Real-time monitoring
pm2 monit

# Process details
pm2 show app-name

# View logs
pm2 logs app-name --lines 100

# Error logs only
pm2 logs app-name --err
```

### Cluster Mode
```bash
# Scale to 4 instances
pm2 scale app-name 4

# Max instances (CPU cores)
pm2 start app.js -i max
```

## Ecosystem Config

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'app-name',
    script: './dist/index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production'
    },
    max_memory_restart: '500M',
    log_date_format: 'YYYY-MM-DD HH:mm:ss'
  }]
};
```

## Log Management

```bash
# Rotate logs
pm2 install pm2-logrotate

# Configure rotation
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
```

## Health Checks

```bash
# Basic health check
curl http://localhost:3000/health

# Check all processes
pm2 list | grep -E "online|stopped|errored"
```

## Persistence

```bash
# Save process list
pm2 save

# Generate startup script
pm2 startup

# Restore after reboot
pm2 resurrect
```
