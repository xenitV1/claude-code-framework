---
name: deployment-procedures
description: Production deployment procedures including pre-deployment checklist, deployment workflow, post-deployment verification, and rollback procedures. CRITICAL skill for safe deployments.
---

# Deployment Procedures

⚠️ **CRITICAL SKILL**: This skill handles production deployments. Always follow procedures carefully.

## Overview
This skill provides step-by-step procedures for safe production deployments.

## Pre-Deployment Checklist

Before ANY deployment, verify:

```markdown
## Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing (unit, integration, e2e)
- [ ] Code reviewed and approved
- [ ] No linting errors
- [ ] No TypeScript errors
- [ ] No console.log statements

### Build
- [ ] Production build successful
- [ ] Bundle size acceptable
- [ ] No build warnings

### Environment
- [ ] All environment variables configured
- [ ] Secrets up to date
- [ ] Database migrations ready
- [ ] Feature flags set correctly

### Communication
- [ ] Team notified of deployment
- [ ] Stakeholders informed (if major)
- [ ] Support team aware

### Safety
- [ ] Rollback plan documented
- [ ] Database backup completed
- [ ] Current version noted
- [ ] Monitoring dashboard open
```

## Deployment Workflow

### Step 1: BACKUP
```bash
# Note current version
pm2 list
git log -1 --oneline

# Backup current deployment
cp -r /app/current /backup/app-$(date +%Y%m%d-%H%M%S)

# Database backup (if applicable)
pg_dump -h localhost -U dbuser dbname > backup-$(date +%Y%m%d).sql
```

### Step 2: BUILD
```bash
# Pull latest code
git pull origin main

# Install dependencies
npm ci --production

# Build application
npm run build

# Run migrations (if any)
npm run migrate
```

### Step 3: DEPLOY
```bash
# Reload with zero-downtime
pm2 reload ecosystem.config.js --update-env

# Or for Docker
docker-compose pull
docker-compose up -d
```

### Step 4: VERIFY
```bash
# Check process status
pm2 list

# Check health endpoint
curl -s http://localhost:3000/health

# Check logs for errors
pm2 logs app-name --lines 50

# Verify key endpoints
curl -s http://localhost:3000/api/status
```

### Step 5: CONFIRM OR ROLLBACK
```
If issues detected → Execute Rollback Procedure
If all good → Confirm deployment complete
```

## Post-Deployment Verification

```bash
#!/bin/bash
# post-deploy-check.sh

echo "=== Post-Deployment Verification ==="

# 1. Health check
echo -n "Health Check: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health)
if [ "$STATUS" = "200" ]; then
    echo "✅ PASS"
else
    echo "❌ FAIL (Status: $STATUS)"
    exit 1
fi

# 2. API Status
echo -n "API Status: "
API_STATUS=$(curl -s http://localhost:3000/api/status | jq -r '.status')
if [ "$API_STATUS" = "ok" ]; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
    exit 1
fi

# 3. Check for errors in logs
echo -n "Error Check: "
ERRORS=$(pm2 logs app-name --lines 100 --nostream 2>&1 | grep -c "ERROR\|Error\|error")
if [ "$ERRORS" -lt 5 ]; then
    echo "✅ PASS ($ERRORS errors)"
else
    echo "⚠️ WARNING ($ERRORS errors detected)"
fi

# 4. Memory usage
echo -n "Memory Usage: "
pm2 show app-name | grep "heap"

echo "=== Verification Complete ==="
```

## Rollback Procedure

### Quick Rollback
```bash
#!/bin/bash
# rollback.sh

echo "⚠️ Starting Rollback..."

# Stop current version
pm2 stop app-name

# Restore previous version
LATEST_BACKUP=$(ls -t /backup/ | head -1)
rm -rf /app/current/*
cp -r /backup/$LATEST_BACKUP/* /app/current/

# Restart
pm2 start app-name

# Verify
curl -s http://localhost:3000/health

echo "✅ Rollback Complete"
```

### Database Rollback
```bash
# Restore database (CAUTION: Destructive)
psql -h localhost -U dbuser -d dbname < /backup/latest.sql

# Or run down migration
npm run migrate:down
```

## PM2 Commands Reference

```bash
# Process Management
pm2 start ecosystem.config.js    # Start all apps
pm2 reload app-name              # Zero-downtime restart
pm2 restart app-name             # Hard restart
pm2 stop app-name                # Stop app
pm2 delete app-name              # Remove from PM2

# Monitoring
pm2 list                         # List processes
pm2 monit                        # Real-time monitoring
pm2 logs app-name                # View logs
pm2 show app-name                # Process details

# Cluster
pm2 scale app-name 4             # Scale to 4 instances

# Persistence
pm2 save                         # Save process list
pm2 startup                      # Generate startup script
```

## Emergency Procedures

### Service Completely Down
```bash
# 1. Check if process is running
pm2 list

# 2. Check system resources
df -h && free -m && top -bn1 | head -20

# 3. Check logs
pm2 logs app-name --err --lines 200

# 4. Attempt restart
pm2 restart app-name

# 5. If still down, rollback
./rollback.sh

# 6. Notify team
# "🚨 Emergency rollback executed at $(date)"
```

### High CPU/Memory
```bash
# Identify issue
pm2 monit

# Scale down if needed
pm2 scale app-name 1

# Restart to clear memory
pm2 restart app-name

# Increase instances if load issue
pm2 scale app-name +2
```

## Modern Deployment & AIOps (2025)

### AI-Monitored Canary Release
1. Shift **1%** traffic to 'Green' environment.
2. AI monitor analyzes logs/metrics for **60 seconds**.
3. If anomaly score > **threshold**, trigger auto-rollback.
4. Else, increase traffic to **10%**, then **100%**.

### Predictive Incident Management
- Use AI to scan logs during deployment for "Silent Failures" (errors that don't trigger HTTP 500s but show logical drift).
- **Auto-Mitigation:** AI can auto-scale instances if it predicts a traffic spike based on deployment-related latency increase.

### Infrastructure-as-Code (2025)
- **Pulumi/Terraform:** Use AI-generated, security-hardened templates with least-privilege IAM roles.

## Best Practices

1. **Never deploy on Fridays** (unless urgent)
2. **Always have rollback plan** ready
3. **Monitor for 15+ minutes** after deploy
4. **Small, frequent deploys** over big releases
5. **Use feature flags** for risky changes
6. **Document all deployments** in changelog
