# ⚡ Maestro Commands

Slash commands for common development workflows.

## Available Commands

| Command | Description | Mode |
|---------|-------------|------|
| [/create](create.md) | Create new application | IMPLEMENT |
| [/enhance](enhance.md) | Add features to existing app | IMPLEMENT |
| [/orchestrate](orchestrate.md) | Multi-agent coordination | ORCHESTRATE |
| [/preview](preview.md) | Start/stop preview server | UTILITY |
| [/status](status.md) | Show project and agent status | UTILITY |
| [/brainstorm](brainstorm.md) | Structured idea exploration | BRAINSTORM |
| [/debug](debug.md) | Systematic problem investigation | DEBUG |
| [/test](test.md) | Generate and run tests | IMPLEMENT |
| [/deploy](deploy.md) | Production deployment | SHIP |

## Usage

```
/create e-commerce app with product listing
/enhance add dark mode
/orchestrate multi-agent review of authentication
/preview start
/status
/brainstorm authentication options
/debug login not working
/test user service
/deploy production
```

## Command Format

```yaml
---
description: Brief description of the command
---

# /command - Title

$ARGUMENTS

## Task
[What the command does]

## Examples
[Usage examples]
```

## Behavioral Modes

Commands map to behavioral modes:

- **BRAINSTORM**: Explore options before deciding
- **IMPLEMENT**: Write code, build features
- **ORCHESTRATE**: Coordinate multiple agents
- **DEBUG**: Investigate problems systematically
- **SHIP**: Deploy with safety checks
