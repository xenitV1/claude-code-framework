---
name: documentation-templates
description: Documentation templates for README, API docs, and code comments.
---

# Documentation Templates

## README Template

```markdown
# Project Name

Brief description of the project.

## Features

- Feature 1
- Feature 2

## Quick Start

\`\`\`bash
npm install
npm run dev
\`\`\`

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| PORT | Server port | 3000 |

## API Documentation

See [API Docs](./docs/api.md)

## Contributing

1. Fork the repo
2. Create feature branch
3. Commit changes
4. Open PR

## License

MIT
```

## JSDoc Template

```typescript
/**
 * Creates a new user.
 * 
 * @param {Object} data - User data
 * @param {string} data.email - User email
 * @param {string} data.name - User name
 * @returns {Promise<User>} Created user
 * @throws {ValidationError} If data is invalid
 * 
 * @example
 * const user = await createUser({
 *   email: 'test@example.com',
 *   name: 'Test User'
 * });
 */
```

## AI-Friendly Documentation (2025)

### llms.txt Template
Used by AI crawlers and agents to quickly understand project structure.
```markdown
# [Project Name]
> Brief one-line objective.

## Core Files
- [file_a.ts]: Main entry point.
- [schema.sql]: Database structure.

## Context
See [docs/architecture.md] for system design logic.
```

### Model Context Protocol (MCP) Integration
Ensure documentation is indexable by MCP servers for Retrieval Augmented Generation (RAG).
- Use clear H1-H3 headers.
- Provide JSON/YAML examples for all data structures.
- Use Mermaid diagrams for flow visualization.

## Changelog Template

```markdown
# Changelog

## [1.2.0] - 2025-01-01
### Added
- New feature X

### Changed
- Updated dependency Y

### Fixed
- Bug in component Z

## [1.1.0] - 2024-12-01
...
```
