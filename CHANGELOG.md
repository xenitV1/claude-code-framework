# Maestro Changelog

## [0.3.2] - 2026-01-09

### 🔧 Documentation Reduction & Workflow Improvements

### Changed

#### Documentation Generation
- **`documentation-writer.md`** → Now triggers ONLY on explicit user request (not auto-invoked)
- **`parallel-agents/SKILL.md`** → Narrowed trigger phrases: "write docs" instead of "docs"
- **`orchestrator.md`** → Documentation agent marked as "explicit request only"

#### Plan File System
- **Location:** `docs/PLAN-*.md` → `./[task-slug].md` (project root)
- **Naming:** Dynamic based on task, no `PLAN-` prefix required
- **`plan-writing/SKILL.md`** → Complete rewrite: Principles over templates
  - 5 Planning Principles (SHORT, SPECIFIC, DYNAMIC, PROJECT-SPECIFIC SCRIPTS, SIMPLE VERIFICATION)
  - Removed fixed Phase 1-2-3-4 template
  - Removed verbose examples (~100 lines removed)

#### Approval Flow
- **`project-planner.md`** → Removed "STOP and ASK 3 questions" rule
- **`orchestrator.md`** → Simplified to "Quick Context Check"
- **`create.md`** → Removed "STOP and ask for approval" checkpoint
- Plans now created and work proceeds without piece-by-piece approval

### Added

#### Agent Self-Check (`clean-code/SKILL.md`)
```
| Check | Question |
| Goal met? | Did I do exactly what user asked? |
| Files edited? | Did I modify all necessary files? |
| Code works? | Did I test/verify the change? |
| No errors? | Lint and TypeScript pass? |
| Nothing forgotten? | Any edge cases missed? |
```

#### Dependency Awareness (`clean-code/SKILL.md`)
- Before editing ANY file, agents must think:
  - What imports this file?
  - What does this file import?
  - What tests cover this?
  - Is this a shared component?
- Rule: Edit file + all dependent files in SAME task

#### Script Execution Rules (`clean-code/SKILL.md`)
- **Agent → Script Mapping:** Each agent runs ONLY their own skill's scripts
- **Output Handling:** READ → SUMMARIZE → ASK (not auto-fix)
  - Parse script output
  - Summarize errors/warnings/passes
  - Ask user: "Should I fix the X errors?"
  - Wait for confirmation

#### OS Detection for Commands (`project-planner.md`)
- Planner now reads `CODEBASE.md` first to check OS field
- Windows → Use Claude Write tool for files, PowerShell for commands
- macOS/Linux → Can use `touch`, `mkdir -p`, bash commands
- Prevents Unix commands failing on Windows (e.g., `cat <<EOF`)

### Removed
- Phase 4: Documentation from plan template (now optional)
- Fixed plan examples (API Endpoint Implementation example)
- Verbose verification script lists from plan template

---

## [0.3.1] - 2026-01-09

### Fixed

#### Windows Console Encoding
- **13 Python scripts** updated to remove emoji characters causing `UnicodeEncodeError` on Windows cp1254 consoles
- Added `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` for UTF-8 safety
- Affected scripts: `i18n_checker.py`, `type_coverage.py`, `geo_checker.py`, `playwright_runner.py`, `security_scan.py`, `api_validator.py`, `lighthouse_audit.py`, `session_manager.py`, `session_hooks.py`, `explorer_helper.py`, `auto_preview.py`, `dependency_scanner.py`, `setup.py`

#### SEO/GEO Script Bugs
- **`geo_checker.py`** → Complete rewrite: Now only analyzes public web pages (HTML/JSX/TSX), not markdown documentation files
- **`seo_checker.py`** → Improved page detection: Only analyzes files in `pages/`, `app/`, `routes/` directories
- Both scripts now skip config files, tests, utilities, and node_modules

#### SessionEnd Hook Deprecated (Issue #3)
- **`SessionEnd`** hook replaced with **`Stop`** per Claude Code CLI 2.1.2+ requirements
- Updated: `settings.example.unix.json`, `settings.example.windows.json`, `README.md`, docs

### Added

#### Game Development Enhancement
- **`game-development/game-art/SKILL.md`** → Visual style selection, asset pipelines, color theory, animation principles
- **`game-development/game-audio/SKILL.md`** → Sound design, music integration, adaptive audio, 3D audio
- Both skills use decision trees and principle tables (no code examples)

#### GEO Checker 2025 Updates (Research-Based)
- **Entity Recognition** → Checks for Organization, LocalBusiness, Brand schema
- **Original Statistics/Data** → Detects percentages, dollar amounts, research citations
- **Direct Answer Patterns** → Detects LLM-friendly content ("is defined as", "refers to", etc.)

#### Dynamic Plan File Naming
- **`project-planner.md`** → Plan files now named dynamically: `docs/PLAN-{task-slug}.md`
- **`commands/plan.md`** → Updated with naming convention and examples
- Allows multiple plan files per project

### Changed
- **`game-development/SKILL.md`** → Restructured as orchestrator with sub-skill routing tables
- **`game-developer.md`** → Added `game-art` and `game-audio` to skills list (now 12 sub-skills)
- **`tailwind-patterns/SKILL.md`** → Complete rewrite for Tailwind v4 (2025): CSS-first config, container queries, OKLCH colors

### Removed
- **`security-checklist/`** → Merged into `vulnerability-scanner/checklists.md`
- Updated `security-auditor.md` and `penetration-tester.md` agent skills accordingly

---

## [0.3.0] - 2026-01-09

### 🏗️ Modular Architecture Overhaul

SKILL.md files have been streamlined and content moved to modular structure.

### Added

#### 🔧 allowed-tools System
- **`allowed-tools: Read, Grep, Glob`** → When a skill is active, Claude can ONLY use these tools. Can read/search files but cannot modify them. Provides read-only security.

#### 📁 New Files
- **`/plan` command** → Planning-only mode without writing code. Triggers project-planner agent. Added because Claude Code CLI's built-in Plan tool was bypassing Maestro system.
- **`ARCHITECTURE.md`** → Complete system architecture document. Agent, skill, script relationships.
- **`docs/` directory** → Official Claude Code reference documents (`claude-code-reference.md`, `aget-skills.md`).
- **`skills/i18n-localization/`** → New skill for multi-language support (internationalization).
- **`skills/bash-linux/`** → Bash terminal skill for macOS/Linux users.
- **22+ new modular files** → SKILL.md files streamlined, details moved to separate .md files (Progressive Disclosure).

#### 🐍 Python Scripts (Zero-Context Execution)

Python scripts added under skills. **How it works:**
1. Claude does NOT read the script into context (token savings)
2. Claude EXECUTES the script directly (`python scripts/xyz.py`)
3. Only script OUTPUT enters context
4. Result: Consistent, tested, fast execution

| Skill | Script | Purpose |
|-------|--------|---------|
| `webapp-testing` | `playwright_runner.py` | Headless browser tests |
| `frontend-design` | `accessibility_checker.py` | WCAG compliance check |
| `frontend-design` | `ux_audit.py` | UX standards audit |
| `mobile-design` | `mobile_audit.py` | Touch target, ergonomics check |
| `performance-profiling` | `lighthouse_audit.py` | Core Web Vitals measurement |
| `vulnerability-scanner` | `security_scan.py` | Security vulnerability scanning |
| `geo-fundamentals` | `scripts/` | GEO metrics analysis |
| `seo-fundamentals` | `scripts/` | SEO scoring scripts |
| `database-design` | `scripts/` | Schema validation |
| `lint-and-validate` | `scripts/` | Multi-linter runner |
| `testing-patterns` | `scripts/` | Test coverage analysis |

### Changed
- **`orchestrator.md`** (+174 lines) → Mandatory PLAN.md check, Socratic Gate (3 questions), Conflict Resolution
- **`project-planner.md`** (+268 lines) → ROOT PLAN concept, 10-point planning framework
- **`orchestrate.md`** → Minimum 3 agent rule (1 agent = delegation, 3+ = orchestration), EXIT GATE
- **`CLAUDE.md`** (-117 lines net) → Streamlined, modular script references added
- **42 SKILL.md files** → Long content moved to separate files, Progressive Disclosure applied

### Removed

| File | Why Removed |
|------|-------------|
| `scripts/lint_check.py` | `npm run lint && npx tsc --noEmit` native commands are faster and dependency-free |
| `skills/api-security-testing/` | Consolidated under `api-patterns/security-testing.md` |
| `skills/artifacts-builder/` | Became redundant with built-in Claude Code artifacts feature |
| `skills/conversation-manager/` | Integrated into orchestrator agent, separate skill unnecessary |
| `skills/git-worktrees/` | Rarely used, standard git commands sufficient |
| 12 template files | `skills/templates/` → moved to `app-builder/templates/` (single location) |

### Summary
- 56 files changed + 47 new files + 16 deleted files
- Skills now modular: SKILL.md (main) + separate .md files + scripts/
- Zero-Context Execution: Python scripts run without consuming context

---


## [0.2.4] - 2026-01-06

### 📱 Comprehensive Mobile Development Expansion

### 🧠 Mobile Psychology & Engineering Culture (CRITICAL)
- **Touch Psychology & Ergonomics**:
  - Implemented **Fitts' Law** and **Thumb Zone** principles for layout decisions.
  - Buttons and interactables now strictly follow specific hit-area and placement rules for optimal user reachability.
  - New skill `skills/mobile-design/touch-psychology.md` serves as the primary ergonomic reference.
- **Professional Testing & Debugging**:
  - Introduced "Production-Grade" testing culture: Not just "writing tests," but defining strategies.
  - Added specialized toolchains for **Detox, Maestro, Flipper, and Reactotron**.
  - New skills: `mobile-testing.md` (E2E/Unit strategies) and `mobile-debugging.md` (Native vs JS logs).

### Added
- **13 New Specialized Mobile Skills (Complete Inventory)** 📚
  - **Core Strategy**:
    - `SKILL.md`: Central hub with anti-patterns and mandatory checkpoints.
    - `mobile-design-thinking.md`: Anti-memorization protocols and deep context analysis.
    - `decision-trees.md`: Context-based decision frameworks for stack/state/nav selection.
  - **Platform Mastery**:
    - `platform-ios.md`: iOS Human Interface Guidelines (HIG), SF Symbols, and patterns.
    - `platform-android.md`: Material Design 3, Adaptive layouts, and Android specifics.
  - **Engineering & Operations**:
    - `mobile-testing.md`: E2E (Detox/Maestro), Testing Pyramid, Offline/Network testing.
    - `mobile-debugging.md`: Native vs JS logs, Flipper, Reactotron, adb logcat, Xcode.
    - `mobile-backend.md`: Offline Sync (TanStack Query), Push Notifications, API security.
    - `mobile-performance.md`: Frame drops, memory leaks, list virtualization (FlashList).
  - **UX & Design Systems**:
    - `touch-psychology.md`: Ergonomics, Fitts' Law, Thumb Zones.
    - `mobile-navigation.md`: Tab/Stack/Drawer patterns, Deep Linking.
    - `mobile-typography.md`: Dynamic Type (iOS), SP units (Android), readable scales.
    - `mobile-color-system.md`: Dark mode, OLED optimization, contrast ratios.

- **Mandatory Build Verification Loop** 🛡️
  - **Absolute Rule**: Agents CANNOT mark a mobile task as complete without successfully running a native build (`run-android` / `run-ios`).
- **Framework Detection Expansion** 🔍
  - Added **Flutter** detection via `pubspec.yaml`.
  - Added **Ionic / Capacitor** detection (@ionic/react, @capacitor/core).

### Fixed
- **Explorer Helper & CODEBASE.md** 🐍
  - **CRITICAL FIX**: `node_modules` and other heavy directories are now correctly excluded from file counts.
  - **Context Cleanliness**: AI now sees a clean, focused `CODEBASE.md` without thousands of dependency files.
  - Fixed "Invisible Directory Structure" bug: core project folders (`src`, `lib`) are always expanded.
- **Setup Script** 🛠️
  - Updated internal counters for TUI installer (Skills: 69 → 78).

### Changed
- **README.md & CLAUDE.md**: Updated counts and added documentation for all new mobile capabilities.
- **scripts/README.md**: Updated architecture details and version to 2.1.

---

## [0.2.0] - 2026-01-05

### 🎨 Major Design Philosophy Overhaul

### Added
- **NO AI MEMORY STYLES** 🚫
  - New absolute rule: Only use styles from Maestro skill files
  - Prohibition against using "Aurora Glass", "Cyberpunk", "Swiss", etc. from AI training data
  - All design decisions must come from skill files, not memory
- **PURPLE BAN** 🟣
  - Mandatory "Purple Check" before delivering any design
  - No purple/violet hex codes (#8B5CF6, #A855F7, etc.) allowed
  - No "purple" in gradient names
  - Replace with Teal/Cyan/Emerald alternatives
- **NO TEMPLATE LAYOUTS** 📐
  - Forbidden patterns: Hero → 3-column features → CTA → Footer
  - Forbidden: Centered hero with 2 buttons, Symmetric 3-card grid
  - Required: Asymmetric layouts, Bento grid (mixed sizes), Overlapping elements
  - Full-width sections alternating with constrained, Unusual navigation
- **NO MODERNS SaaS CLICHÉS** ⚖️
  - New "Anti-Safe Harbor" rules
  - Forbidden: Standard Hero Split (Left Text / Right Visual)
  - Forbidden: 70/30 splits (pseudo-radical)
  - Forbidden: Bento Grids (unless for complex data)
  - Forbidden: Mesh/Aurora Gradients, Glassmorphism (standard)
  - Forbidden: Deep Cyan / Fintech Blue (the "safe" escape)
  - Required: Experimental layouts, Massive typography, Brutalist/Neo-Retro styles
- **Full Skill Chain Loading** 🔗
  - Mandatory procedure: Read ALL skills AND their references before starting
  - Check agent's "skills:" field in frontmatter
  - For EACH skill listed: Open SKILL.md, read ALL content, check for references
  - If references exist: READ THOSE TOO (e.g., color-system.md, ux-psychology.md)
  - ONLY AFTER reading FULL CHAIN → Start working
- **READ → UNDERSTAND → APPLY** 🧠
  - Reading is NOT enough - must UNDERSTAND PRINCIPLES and PURPOSE
  - Before coding, declare: "🧠 CHECKPOINT: [Agent] + [Skills read] + [3 principles I'll apply]"
- **Frontend Design Reference Files** 📁
  - 7 new reference documents in `skills/frontend-design/`:
    - `animation-guide.md` - Motion, timing, easing principles
    - `color-system.md` - Color theory, emotion mapping
    - `decision-trees.md` - Context-specific decision templates
    - `motion-graphics.md` - Lottie, GSAP, SVG, 3D, Particles
    - `typography-system.md` - Font pairing, scale decisions
    - `ux-psychology.md` - Hick's Law, Fitts' Law, Trust, Emotion
    - `visual-effects.md` - Glassmorphism, shadows, gradients

### Changed
- **CLAUDE.md** - Complete rewrite with new philosophy
  - Replaced "⚠️ CRITICAL: Use Maestro System" with "🔴 ABSOLUTE RULE: USE MAESTRO - NO EXCEPTIONS"
  - Removed: Quick Start Commands, Agent list, Skills list, Hook Configuration sections
  - Added: Comprehensive rule tables, mindset sections, proof of understanding checkpoints
- **CODEBASE.md** - Streamlined structure
  - Removed: OS commands, Clean Code standards section
  - Simplified: Project structure, File dependencies
  - More concise, reference-focused
- **README.md** - Updated counts
  - Agents: 18 → 17
  - Skills: 50 → 69
  - Scripts: 7 (with Visual Dashboard note)
- **All Agents (17 files)** - Comprehensive updates
  - Added: "CRITICAL: CLARIFY BEFORE CODING" sections
  - Added: "Your Mindset" sections
  - Added: Decision Frameworks / Decision Trees
  - Added: Anti-Patterns sections
  - Less code examples, more principles
  - "Teaches thinking, not copying" emphasis
- **All Skills (50 files)** - Restructured
  - Added: "⚠️ How to Use This Skill" - teaches decision-making, not code copying
  - Added: Decision trees instead of fixed patterns
  - Reduced code examples, increased principle coverage
  - Templates: ~300-400 lines shorter each (more concise)
  - Game dev skills: ~300+ lines simplified
  - mobile-typography: -723 lines
  - modern-design-system: -631 lines
- **Frontend Specialist Agent** - Largest update
  - Added: 🧠 DEEP DESIGN THINKING (MANDATORY - BEFORE ANY DESIGN)
  - Added: The MODERN CLICHÉ SCAN (ANTI-SAFE HARBOR)
  - Added: TOPOLOGICAL HYPOTHESIS selection
  - Added: 🎨 DESIGN COMMITMENT (required output block)
  - Added: 🧠 THE MAESTRO AUDITOR (FINAL GATEKEEPER)
  - Added: Automatic Rejection Triggers table
- **Scripts** - Enhanced
  - `explorer_helper.py`: Smart filtering with EXCLUDE_DIRS, COLLAPSE_DIRS, SmartTreeGenerator
  - `lint_check.py`: Rich UI with tables, panels, progress spinners
- **Commands** - New orchestrate command
  - Added `/orchestrate` command for multi-agent coordination
  - Added "ORCHESTRATE" behavioral mode

### Removed
- **`agents/api-designer.md`** - Functionality migrated to backend-specialist
- **`docs/RESOURCES.md`** - No longer needed
- **`maestro-release-v007.txt`** - Old release file

### Philosophy Changes
- From: "Here are some patterns you can use"
- To: "THINK about the problem, don't copy patterns"
- From: Code-heavy documentation
- To: Principle-heavy, decision-making focused
- From: Generic design defaults
- To: Context-specific, ask-before-assuming approach

### Summary
- 76 files changed
- 9,131 insertions(+)
- 15,395 deletions(-)
- Net: -6,264 lines (more concise, principle-focused content)

---

## [0.0.7] - 2026-01-02

### Added
- **Native Multi-Agent Orchestration** 🤖
  - Migration from external Python scripts to Claude's native Agent tool (subagents)
  - New `commands/orchestrate.md` for triggering multi-agent tasks
  - Improved context sharing and session continuity during parallel execution
- **Game Developer Agent** 🎮
  - New `agents/game-developer.md` specialized in game design and development
  - Comprehensive `skills/game-development/` library including:
    - 2D/3D Games, Mobile, PC, Web, VR/AR, Multiplayer, and Game Design patterns
- **Parallel Agents Skill** ⚡
  - New `skills/parallel-agents/SKILL.md` for subagent coordination patterns

### Changed
- **Orchestrator Agent**: Updated to utilize native subagent capabilities for complex project management
- **Documentation Update**: Global refresh of `CLAUDE.md`, `CODEBASE.md`, and `README.md` with new agent/skill counts
- **Setup Script**: `scripts/setup.py` updated to reflect the new architecture

### Removed
- **`scripts/parallel_orchestrator.py`** 🗑️: Removed because it bypassed native Claude Code CLI features. It has been replaced by the native `orchestrate.md` agent and `commands/orchestrate.md`, which provide better session continuity and context flow.

---

## [0.0.6] - 2026-01-01

### Added
- **Dependency Scanner** 📊
  - New `scripts/dependency_scanner.py` for file relationship tracking
  - Detects imports (ES6, CommonJS, Python), API calls (fetch, axios), DB models (Prisma)
  - Integrated into `session_hooks.py` - runs automatically on session start
  - `@/` alias resolution for React/Next.js projects
  - Relative path resolution (`./`, `../`) with proper normalization
  - **Python import support**: relative imports (`.module`, `..package`), absolute imports
  - Standard library filtering (os, sys, json, etc. automatically skipped)
  - File tree annotations showing dependencies (`file.ts ← A.tsx, B.tsx`)
  - Legend and warning notes in CODEBASE.md output
- **SEO Specialist Agent** 🎯
  - New `agents/seo-specialist.md` for SEO and GEO optimization
  - Uses `seo-fundamentals` and `geo-fundamentals` skills
- **Maestro System Requirements** ⚠️
  - CLAUDE.md now includes mandatory Maestro usage section
  - File Dependency Awareness documentation
  - Requirement to check CODEBASE.md before making changes

### Changed
- Updated skill assignments for 6 existing agents:
  - `frontend-specialist`: +artifacts-builder
  - `orchestrator`: +behavioral-modes
  - `test-engineer`: +code-review-checklist
  - `project-planner`: +conversation-manager
  - `devops-engineer`: +git-worktrees, +powershell-windows
  - `backend-specialist`: +mcp-builder
- Updated counts: 17 agents, 40 skills, 8 scripts
- `setup.py`: added dependency_scanner.py to install list

---

## [0.0.5] - 2026-01-01

### Added
- **Cross-Platform Support** 🌍
  - Added `Makefile` with platform detection (Windows, macOS, Linux)
  - Added `scripts/setup.py` for automated cross-platform installation
  - Added `settings.example.unix.json` for macOS/Linux (python3, ~/.claude/)
  - Added `settings.example.windows.json` for Windows (python, %USERPROFILE%\.claude\)
  - Platform-specific path handling and command execution
  - Automated installation with `make install` command
  - Installation verification with `make verify` command
- **Architecture Skill** 🏗️
  - Added `skills/architecture/SKILL.md` - Architectural decision framework
  - Requirements-driven architecture approach
  - Trade-off analysis and ADR documentation
  - Pattern selection guidelines with decision trees
  - Simplicity-first principle
  - Examples for MVP, SaaS, and Enterprise projects

### Changed
- Split `settings.example.json` into platform-specific files
- Updated setup process to automatically detect OS and use appropriate settings
- Fixed `explorer-agent.md` to reference correct architecture skill

### Removed
- Removed `settings.example.json` (replaced by platform-specific files)

### Contributors
- Special thanks to [@aliihsansepar](https://github.com/aliihsansepar) for the cross-platform contribution! 🙏

---

## [0.0.4] - 2025-12-31

### Added
- **CODEBASE.md** - Project context file
  - Relocated from `.claude/rules.md` to root directory
  - Improves visibility for Claude (`.claude/` directory was not always accessible)
  - Contains project structure and codebase context
- **mobile-typography skill** - New skill for mobile typography
  - Mobile type scale patterns
  - Responsive typography guidelines
  - Font optimization for mobile platforms

### Changed
- Updated CLAUDE.md skills table with mobile-typography
- Updated skills/README.md total count from 40 to 41 skills
- Updated mobile-developer agent to reference mobile-typography skill
- Updated session hooks configuration
- Updated settings.example.json

---

## [0.0.3] - 2025-12-31

### Added
- **OS Detection & Context Injection**
  - Added automatic OS detection (Windows, macOS, Linux) in `session_hooks.py`
  - Added OS-specific terminal commands (PowerShell, bash, zsh)
  - Added dynamic `.claude/rules.md` generation in each project
  - Added `load_clean_code_skill()` to inject clean code standards into project context
  - Added `get_os_info()` and `get_os_commands()` functions
- **Project Structure Discovery**
  - Added `load_discovery_structure()` to inject full project tree into context
  - Discovery report structure now included in auto-generated `.claude/rules.md`
- **Context Loading Documentation**
  - Added "Context Loading Order" section to CLAUDE.md
  - Documents that CLAUDE.md loads first, then .claude/rules.md

### Changed
- Session hooks now create `project/.claude/rules.md` with:
  - Project information (name, framework, type, path)
  - OS information and shell type
  - OS-specific terminal commands
  - Project-specific commands (npm, python, etc.)
  - Complete project structure tree from discovery report
  - Clean code standards from `skills/clean-code/SKILL.md`
- Fixed frontmatter parsing in `load_clean_code_skill()` - now correctly extracts content after YAML

### Fixed
- **Critical:** Fixed `AttributeError: 'NoneType' object has no attribute 'upper'` in `session_hooks.py`
  - Added `safe_upper()` function to handle None values in project type detection
  - Framework projects (like Maestro itself) no longer crash hooks
- Debug log now clears on each session start (`clear_debug_log()` in `main()`)
- Prevents log file from growing indefinitely across sessions

### Removed
- **Terminal Error Learning System** (broken hooks compatibility)
  - Removed `scripts/pre_bash.py` - Error warning system
  - Removed `scripts/check_prevention.py` - Dangerous command blocking
  - Removed `scripts/track_error.py` - Error recording system
  - Removed `skills/terminal-error-patterns/` - Error patterns skill
  - Removed error tracking hooks from `settings.json`
  - Removed error database references from documentation

### Updated Documentation
- Updated README.md - Removed error learning feature
- Updated CLAUDE.md - Removed error tracking references
- Updated scripts/README.md - Simplified hook system documentation
- Updated data/README.md - Removed error database schema
- Updated docs/RESOURCES.md - Removed error learning resources
- Updated agents/debugger.md - Removed terminal-error-patterns skill reference
- Reduced script count from 9 to 5
- Reduced skill count from 40 to 37

---

## [0.0.2] - 2025-12-31

### Added
- **Security Testing**
  - New agent: `penetration-tester.md` for security assessments
  - New skill: `api-security-testing/` - API security patterns
  - New skill: `red-team-tactics/` - Adversary simulation tactics
  - New skill: `vulnerability-scanner/` - Vulnerability scanning procedures
- **Debug Logging**
  - Added `debug_log()` to `check_prevention.py`
  - Added `debug_log()` to `pre_bash.py`
  - Added `debug_log()` to `track_error.py`
  - Added `debug_log()` to `parallel_orchestrator.py`
- **Documentation**
  - Created `docs/RESOURCES.md` - Project resources (Turkish)
  - Created `docs/claude-code-reference.md` - Claude Code documentation

### Changed
- Updated README.md statistics (15 agents, 40+ skills, 8 scripts)
- Updated agents/README.md with new penetration-tester agent
- Updated skills/README.md with new security skills

### Removed
- **`scripts/progress_reporter.py`** - Removed unused script
- Removed `progress_reporter` references from all files
  - `scripts/parallel_orchestrator.py`
  - `README.md`, `CLAUDE.md`
  - `commands/status.md`, `commands/create.md`
  - `scripts/README.md`

### Fixed
- Fixed inaccurate multi-agent orchestration description in README
- Clarified agents work independently, not via JSON message passing

---

## [0.0.1] - 2025-12-30

### Initial Release
- 14 specialized agents
- 37 skills (patterns, templates)
- 9 Python hook scripts
- 8 slash commands
- Error learning system
- Parallel orchestration support
- Session management
- Auto preview server

---

[Unreleased]: https://github.com/xenitV1/claude-code-maestro/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/xenitV1/claude-code-maestro/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/xenitV1/claude-code-maestro/compare/v0.2.4...v0.3.0
[0.2.4]: https://github.com/xenitV1/claude-code-maestro/compare/v0.2.0...v0.2.4
[0.2.0]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.7...v0.2.0
[0.0.7]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/xenitV1/claude-code-maestro/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/xenitV1/claude-code-maestro/releases/tag/v0.0.1

