---
name: security-checklist
description: Security audit checklist covering OWASP Top 10, authentication, and secure coding practices.
allowed-tools: Read, Glob, Grep
---

# Security Checklist

> Quick reference checklist for security audits.

---

## 1. OWASP Top 10 (2021+)

### A01: Broken Access Control
- [ ] Authorization on all protected routes
- [ ] Deny by default
- [ ] Rate limiting implemented
- [ ] CORS properly configured

### A02: Cryptographic Failures
- [ ] Passwords hashed (bcrypt/argon2, cost 12+)
- [ ] Sensitive data encrypted at rest
- [ ] TLS 1.2+ for all connections
- [ ] No secrets in code/logs

### A03: Injection
- [ ] Parameterized queries
- [ ] Input validation on all user data
- [ ] Output encoding for XSS
- [ ] No eval() or dynamic code execution

### A04: Insecure Design
- [ ] Threat modeling done
- [ ] Security requirements defined
- [ ] Business logic validated

### A05: Security Misconfiguration
- [ ] Unnecessary features disabled
- [ ] Error messages sanitized
- [ ] Security headers configured
- [ ] Default credentials changed

### A06: Vulnerable Components
- [ ] Dependencies up to date
- [ ] No known vulnerabilities
- [ ] Unused dependencies removed

### A07: Authentication Failures
- [ ] MFA available
- [ ] Session invalidation on logout
- [ ] Session timeout implemented
- [ ] Brute force protection

### A08: Integrity Failures
- [ ] Dependency integrity verified
- [ ] CI/CD pipeline secured
- [ ] Update mechanism secured

### A09: Logging Failures
- [ ] Security events logged
- [ ] Logs protected
- [ ] No sensitive data in logs
- [ ] Alerting configured

### A10: SSRF
- [ ] URL validation implemented
- [ ] Allow-list for external calls
- [ ] Network segmentation

---

## 2. Authentication Checklist

- [ ] Strong password policy
- [ ] Account lockout
- [ ] Secure password reset
- [ ] Session management
- [ ] Token expiration
- [ ] Logout invalidation

---

## 3. API Security Checklist

- [ ] Authentication required
- [ ] Authorization per endpoint
- [ ] Input validation
- [ ] Rate limiting
- [ ] Output sanitization
- [ ] Error handling

---

## 4. Data Protection Checklist

- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Key management
- [ ] Data minimization
- [ ] Secure deletion

---

## 5. Security Headers

| Header | Purpose |
|--------|---------|
| **Content-Security-Policy** | XSS prevention |
| **X-Content-Type-Options** | MIME sniffing |
| **X-Frame-Options** | Clickjacking |
| **Strict-Transport-Security** | Force HTTPS |
| **Referrer-Policy** | Referrer control |

---

## 6. Audit Commands Reference

| Check | What to Look For |
|-------|------------------|
| Secrets in code | password, api_key, secret |
| Dangerous patterns | eval, innerHTML, SQL concat |
| Dependency issues | npm audit, snyk |

---

> **Remember:** Checklists catch obvious issues. Deep testing requires methodology.
