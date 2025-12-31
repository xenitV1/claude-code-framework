# 🎼 Maestro

> **AI Development Orchestrator** - Transform Claude into a powerful development team with specialized agents, intelligent skills, and automated workflows.

[![Agents](https://img.shields.io/badge/Agents-14-blue)](#-agents)
[![Skills](https://img.shields.io/badge/Skills-37-green)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-8-orange)](#-commands)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](#-scripts)

---

## ✨ Features

- 🤖 **14 Specialized Agents** - Expert AI personas for frontend, backend, mobile, DevOps, and more
-  **37 Skills** - Domain knowledge resources with patterns, best practices, and templates |
- ⚡ **8 Slash Commands** - Quick actions for creating apps, debugging, testing, and deploying
- 🐍 **9 Python Scripts** - Automation hooks for error learning, session management, and progress tracking
- 🎯 **Clean Code Standards** - CRITICAL skill for concise, direct, solution-focused code
- 🎭 **6 Behavioral Modes** - Adaptive AI behavior: Brainstorm, Implement, Debug, Review, Teach, Ship
- 🔄 **Error Learning System** - Automatically learns from past mistakes and prevents recurring issues
- 🧩 **Parallel Orchestration** - Run multiple specialized agents concurrently for different perspectives
- 🧠 **Synthesis Reporting** - Automatically combines multi-agent outputs into cohesive project reports

---

## 🚀 Quick Start

### Create an Application

```bash
/create e-commerce site with product listing and cart
```

The framework will:
1. Analyze your request
2. Plan the project structure
3. Coordinate specialized agents
4. Generate production-ready code
5. Start a preview server

### Add Features

```bash
/enhance add dark mode
/enhance build admin panel
```

### Other Commands

```bash
/brainstorm authentication options    # Explore ideas
/debug login not working              # Investigate issues
/test user service                    # Generate tests
/deploy production                    # Deploy safely
```

---

## 📁 Project Structure

```
maestro/
├── agents/              # 12 specialized AI agents
│   ├── frontend-specialist.md
│   ├── backend-specialist.md
│   ├── mobile-developer.md
│   ├── devops-engineer.md
│   └── ...
├── skills/              # 31 knowledge resources
│   ├── app-builder/
│   ├── behavioral-modes/
│   ├── react-patterns/
│   ├── templates/
│   │   ├── nextjs-fullstack/
│   │   ├── express-api/
│   │   ├── react-native-app/
│   │   └── nextjs-static/
│   └── ...
├── commands/            # 8 slash commands
│   ├── create.md
│   ├── enhance.md
│   ├── debug.md
│   └── ...
├── scripts/             # 7 Python automation scripts
│   ├── session_hooks.py
│   ├── pre_bash.py
│   ├── track_error.py
│   └── ...
├── data/                # Runtime state and error database
├── settings.json        # Hook configuration
├── CLAUDE.md           # AI behavior configuration
└── README.md           # This file
```

---

## 🔄 Hook System Flow

The framework uses an intelligent hook system that automatically detects projects, learns from errors, and prevents mistakes:

```mermaid
flowchart LR
    Start([claude]) --> SessionStart[SessionStart Hook]
    SessionStart --> Detect[Detect Project<br/>& Tech Stack]
    Detect --> Ready[Ready for Commands]
    
    Ready --> UserCmd{User Action}
    UserCmd -->|Bash Command| PreHook[PreToolUse Hook<br/>Check History]
    PreHook --> Execute[Execute Command]
    Execute --> PostHook[PostToolUse Hook<br/>Learn from Result]
    PostHook --> Ready
    
    UserCmd -->|Exit| SessionEnd[SessionEnd Hook<br/>Save Session]
    SessionEnd --> End([Exit])
    
    style SessionStart fill:#4CAF50,color:#fff
    style PreHook fill:#FF9800,color:#fff
    style PostHook fill:#2196F3,color:#fff
    style SessionEnd fill:#9C27B0,color:#fff
```

**Key Features:**
- 🔍 **Auto-Detection:** Finds your project type (Next.js, React Native, Python, etc.)
- 🛡️ **Error Prevention:** Warns about commands that failed before
- 🚫 **Safety Checks:** Blocks dangerous operations
- 📊 **Learning System:** Improves over time by tracking patterns

For detailed hook architecture, see **[scripts/README.md](scripts/README.md#hook-system-architecture)**.

---

## 🤖 Agents

Specialized AI agents that handle different aspects of development:

| Agent | Expertise | Lines |
|-------|-----------|-------|
| **explorer-agent** | Codebase exploration, dependency research | 210 |
| **debugger** | Root cause analysis, systematic debugging | 250+ |
| **api-designer** | REST/GraphQL, OpenAPI, API security | 521 |
| **mobile-developer** | React Native, Flutter, Expo, App Store | 354 |
| **devops-engineer** | PM2, deployment, CI/CD, rollback | 275 |
| **test-engineer** | Testing strategies, TDD, coverage | 268 |
| **security-auditor** | Security review, vulnerabilities | 229 |
| **orchestrator** | Multi-agent coordination | 209 |
| **database-architect** | Schema design, Prisma, migrations | 189 |
| **backend-specialist** | Node.js, Express, FastAPI | 187 |
| **frontend-specialist** | React, Next.js, Tailwind | 149 |
| **project-planner** | Task breakdown, planning | 140 |
| **performance-optimizer** | Performance profiling | 132 |
| **documentation-writer** | README, API docs | 98 |

Each agent includes:
- Domain expertise and best practices
- Code patterns and examples
- Review checklists
- Trigger keywords for automatic selection

---

## 📚 Skills

Knowledge resources that agents reference for domain expertise:

### 🏗️ Architecture & Patterns
- `api-patterns` - REST/GraphQL design patterns
- `react-patterns` - React component patterns
- `mobile-patterns` - Mobile development patterns
- `nodejs-best-practices` - Node.js 23 patterns (Native TS, SQLite)
- `nextjs-best-practices` - Next.js 15 App Router & React 19 patterns
- `frontend-design` - 2025 Design Precision (8-point grid, Golden Ratio)

### 🎨 Templates
| Template | Description | Tech Stack |
|----------|-------------|------------|
| **nextjs-fullstack** | Full-stack web app | Next.js, Prisma, TypeScript, Tailwind |
| **express-api** | REST API | Express, JWT, Zod, Prisma |
| **react-native-app** | Mobile app | Expo, React Query, Zustand |
| **nextjs-static** | Landing page | Next.js, Framer Motion, Tailwind |

### 🛠️ Operations
- `server-management` - Server administration
- `deployment-procedures` - Safe deployment
- `performance-profiling` - Performance analysis
- `systematic-debugging` - Debugging methodology
- `mobile-ux-patterns` - Touch gestures, haptics, accessibility

---

## ⚡ Commands

| Command | Description | Mode |
|---------|-------------|------|
| `/create` | Create new application from natural language | IMPLEMENT |
| `/enhance` | Add features to existing app | IMPLEMENT |
| `/preview` | Start/stop preview server | UTILITY |
| `/status` | Show project and agent status | UTILITY |
| `/brainstorm` | Structured idea exploration | BRAINSTORM |
| `/debug` | Systematic problem investigation | DEBUG |
| `/test` | Generate and run tests | IMPLEMENT |
| `/deploy` | Production deployment with safety checks | SHIP |

---

## 🐍 Scripts

Python automation scripts that provide intelligent hooks:

### Hook Scripts (Automatic)
| Script | Hook | Purpose |
|--------|------|---------|
| `session_hooks.py` | SessionStart/End | Project detection, session tracking |
| `pre_bash.py` | PreToolUse | Error learning - warns about known issues |
| `parallel_orchestrator.py` | CLI | Multi-agent parallel execution engine |
| `check_prevention.py` | PreToolUse | Blocks dangerous commands |
| `track_error.py` | PostToolUse | Records errors for learning |

### Utility Scripts (Manual)
| Script | Purpose |
|--------|---------|
| `progress_reporter.py` | Agent status board with rich UI |
| `parallel_orchestrator.py` | Manual parallel execution with synthesis |
| `session_manager.py` | Project state management |
| `auto_preview.py` | Preview server control |
| `explorer_helper.py` | Proactive codebase discovery |
| `track_error.py` | Systematic error tracking |

### Dependencies

```bash
pip install rich pydantic
```

---

## 🎭 Behavioral Modes

The framework adapts its behavior based on context:

| Mode | Trigger Keywords | Behavior |
|------|------------------|----------|
| **BRAINSTORM** | "ideas", "options", "what if" | Explore alternatives, ask questions |
| **IMPLEMENT** | "build", "create", "add" | Fast execution, production code |
| **DEBUG** | "error", "not working", "bug" | Systematic investigation |
| **REVIEW** | "review", "check", "audit" | Thorough constructive analysis |
| **TEACH** | "explain", "how does" | Educational explanations |
| **SHIP** | "deploy", "production" | Pre-flight checks, safety first |

---

## 🔄 Error Learning System

The framework learns from mistakes to prevent recurring issues:

1. **Track** - Errors are automatically recorded with command context
2. **Learn** - Patterns are extracted and stored in error database
3. **Warn** - Similar commands trigger warnings with past error info
4. **Suggest** - Solutions from resolved errors are recommended

```
⚠️ Warning: Similar command failed before
   Command: npm install broken-package
   Error: npm ERR! 404 Not Found
   Suggestion: Check package name spelling or try npm cache clean
```

---

## 🧠 Multi-Agent Orchestration

The framework supports true parallel execution through the `parallel_orchestrator.py` engine:

1. **Decomposition**: The orchestrator splits complex tasks into domain-specific sub-tasks.
2. **Parallel Dispatch**: Specialized agents (Backend, Frontend, Security, etc.) are spawned concurrently.
3. **State Sharing**: Agents communicate via `data/orchestrator-state.json` to avoid conflicts.
4. **Synthesis**: A final report is generated in `data/reports/` summarizing all findings from parallel agents.

```bash
python scripts/parallel_orchestrator.py "Build a secure payment flow" --agents 3
```

---

## ⚙️ Configuration

Hooks are configured in `settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "command": "python scripts/session_hooks.py start" }
    ],
    "PreToolUse": [
      { "command": "python scripts/pre_bash.py \"$TOOL_INPUT\"" },
      { "command": "python scripts/check_prevention.py \"$TOOL_INPUT\"" }
    ],
    "PostToolUse": [
      { "command": "python scripts/track_error.py ..." }
    ],
    "SessionEnd": [
      { "command": "python scripts/session_hooks.py end" }
    ]
  }
}
```

---

## 📊 Statistics

| Category | Count |
|----------|-------|
| Agents | 14 |
| Skills | 37 |
| Commands | 8 |
| Scripts | 9 |
| Templates | 12 |
| Behavioral Modes | 6 |
| Hook Scripts | 4 |

---

---

## 🔧 Troubleshooting

### ❌ Hooks Not Working?

If your `SessionStart` or `SessionEnd` hooks are not triggering, you likely need to add the `matcher` property to your hook configuration.

**See [HOOKS-TROUBLESHOOTING.md](HOOKS-TROUBLESHOOTING.md) for detailed solutions.**

**Quick Fix:**

❌ **Wrong (won't work):**
```json
"SessionStart": [
  {
    "command": "python script.py"
  }
]
```

✅ **Correct (will work):**
```json
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
```

**Debug your hooks:**
```bash
claude --debug
```

Check the debug log at `~/.claude/debug/[session-id].txt` and look for:
- `Found 1 hook matchers` ✅ (not `Found 0` ❌)

For complete troubleshooting guide, see **[HOOKS-TROUBLESHOOTING.md](HOOKS-TROUBLESHOOTING.md)**.

---

## 🛠️ Requirements

- Python 3.10+
- Node.js 23+ (for native TypeScript & SQLite support)
- Claude Code or compatible AI assistant

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please read the documentation in each directory's README.md for specific guidelines.

---

<p align="center">
  <b>🎼 Maestro - Built with ❤️ for AI-assisted development</b><br/>
  <a href="https://x.com/xenit_v0">@xenit_v0</a>
</p>
