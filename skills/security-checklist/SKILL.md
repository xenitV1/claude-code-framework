---
name: security-checklist
description: Comprehensive security checklist covering OWASP Top 10, input validation, authentication, and secure coding practices. Use for security audits and reviews.
---

# Security Checklist

## OWASP Top 10 (2021)

### A01: Broken Access Control
- [ ] Authorization checks on all protected routes
- [ ] Deny by default
- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] Directory listing disabled

### A02: Cryptographic Failures
- [ ] Passwords hashed with bcrypt/argon2 (cost 12+)
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.2+ for all connections
- [ ] No secrets in code/logs
- [ ] Strong random number generation

### A03: Injection
- [ ] Parameterized queries only
- [ ] Input validation on all user data
- [ ] Output encoding for XSS prevention
- [ ] No eval() or dynamic code execution
- [ ] Command injection prevented

### A04: Insecure Design
- [ ] Threat modeling done
- [ ] Security requirements defined
- [ ] Secure development lifecycle followed
- [ ] Business logic validated

### A05: Security Misconfiguration
- [ ] Unnecessary features disabled
- [ ] Error messages don't reveal info
- [ ] Security headers configured
- [ ] Default credentials changed
- [ ] Latest security patches applied

### A06: Vulnerable Components
- [ ] Dependencies up to date
- [ ] No known vulnerabilities (npm audit)
- [ ] License compliance checked
- [ ] Unused dependencies removed

### A07: Authentication Failures
- [ ] Multi-factor authentication available
- [ ] Session invalidation on logout
- [ ] Session timeout implemented
- [ ] Password policy enforced
- [ ] Brute force protection

### A08: Integrity Failures
- [ ] Dependency integrity verified
- [ ] CI/CD pipeline secured
- [ ] Code signing implemented
- [ ] Update mechanism secured

### A09: Logging Failures
- [ ] Security events logged
- [ ] Logs protected from tampering
- [ ] No sensitive data in logs
- [ ] Alerting configured

### A10: SSRF
- [ ] URL validation implemented
- [ ] Allow-list for external calls
- [ ] Network segmentation

## Quick Audit Commands

```bash
# NPM security audit
npm audit

# Check for secrets in code
grep -r "password\s*=" --include="*.ts"
grep -r "api[_-]?key" --include="*.ts"

# Check for dangerous functions
grep -r "eval\(" --include="*.ts"
grep -r "dangerouslySetInnerHTML" --include="*.tsx"
```

## Security Headers

```typescript
// helmet.js configuration
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
    }
  },
  hsts: { maxAge: 31536000, includeSubDomains: true },
  noSniff: true,
  frameguard: { action: 'deny' }
}));
```
