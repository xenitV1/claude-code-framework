# 📚 Claude Code Full-Stack Developer Ekibi - Kaynakça ve Proje Dokümantasyonu

## 🎯 Planın Amacı

Bu plan, **Claude Code CLI**'yı tam özellikli bir **AI Full-Stack Development Team**'e dönüştürmek için hazırlanmıştır.

**Ana Hedefler:**
1. Tek başına girişim kurmak isteyen geliştiricilere tam bir AI ekibi sağlamak
2. Frontend, backend, mobile, database, DevOps, testing, security alanlarında uzmanlık
3. Otomatik workflow automation (hooks, agents, skills)
4. Terminal hatalarından öğrenen self-improving sistem
5. Production-ready, test edilebilir, güvenli kod üretimi

**Hedef Kitle:**
- Solo entrepreneurs (tek başına startup kuran geliştiriciler)
- Full-stack developers (tüm stack'i tek başına yönetenler)
- Small teams (küçük ekipler, çok alanlı destek ihtiyacı)
- Rapid prototyping (hızlı prototip geliştirme)

**Kullanım Senaryosu:**
Kullanıcı, tek bir AI'ya (Claude Code CLI) plan dosyasındaki MASTER PROMPT'u verir. AI otomatik olarak 10 specialized agent spawn eder ve paralel çalışarak tüm sistemi kurar:
- 6 PowerShell hook script
- 10 specialized subagent
- 26 agent skill
- 9 slash command
- Terminal Error Learning database

---

## 📖 Birincil Kaynaklar

### 1. Claude Code Resmi Dokümantasyonu
**Dosya**: `C:\Users\Mehmet\.claude\claudecodedoc.md`
**Kullanım**: Ana referans dokümantasyon
**Kapsadığı Konular**:
- Claude Code CLI architecture
- Hooks (lifecycle events: SessionStart, PreToolUse, PostToolUse, etc.)
- Subagents (specialized AI assistants with separate contexts)
- Agent Skills (markdown-based knowledge files with YAML frontmatter)
- Slash Commands (custom shortcuts)
- MCP (Model Context Protocol) servers
- Settings configuration (hooks, custom API endpoints, etc.)

**Kritik Bilgiler Alınan Alanlar**:
- Hook sistemi ve lifecycle events (satır: ~50-150)
- Subagent tanımlama formatı (YAML frontmatter + markdown content)
- Skill yapısı (progressive disclosure pattern)
- Tool approval system ve security
- Windows PowerShell integration

---

### 2. Mevcut Claude Code Konfigürasyonu
**Dosya**: `C:\Users\Mehmet\.claude\settings.json`
**Kullanım**: Kullanıcının mevcut setup'ını analiz
**Elde Edilen Bilgiler**:
- Custom API endpoint: Z.AI (GLM modelleri kullanılıyor)
- 5 hook tanımlı ama script dosyaları yok:
  - `onSessionStart`: session-start.ps1
  - `onPromptSubmit`: analyze-prompt.ps1
  - `onPostToolUse`: track-error.ps1
  - `onPreToolUse`: check-prevention.ps1
  - `onSessionEnd`: session-end.ps1
- MCP servers: Context7, filesystem, sequential-thinking
- Windows ortamı (PowerShell 5.1+)

**Planlamada Kullanımı**:
- Hook script'leri bu tanımlara göre tasarlandı
- Windows PowerShell uyumlu scriptler
- GLM model uyumluluğu göz önüne alındı

---

## 🌟 GitHub Kaynakları

### 1. obra/superpowers ⭐⭐⭐⭐⭐ (ÇOK KRİTİK)
**URL**: https://github.com/obra/superpowers
**Lisans**: MIT License (Kullanılabilir)
**Yıldız Sayısı**: ~1,000+ stars

**Kullanılan Skills**:
1. **brainstorming.md** (300 satır)
   - Socratic dialogue tekniği
   - Requirements clarification
   - Scope creep önleme
   - "What problem are you solving?" yaklaşımı

2. **plan-writing.md** (350 satır)
   - Task breakdown (2-5 dakikalık chunks)
   - Autonomous execution için bite-sized tasks
   - Dependency identification
   - Verification criteria

3. **tdd-workflow.md** (300 satır)
   - RED-GREEN-REFACTOR enforcement
   - Test-skipping prevention
   - Technical debt önleme
   - TDD cycle examples

4. **systematic-debugging.md** (250 satır)
   - 4-phase root cause analysis
   - Evidence-based verification
   - "Test results, not claims"

5. **parallel-agents.md** (200 satır)
   - Concurrent subagent workflows
   - Multi-tasking capability
   - 2-stage review (spec compliance + code quality)

**Neden Önemli**:
- Workflow **enforcement** (zorunlu), suggestion değil
- Otomatik aktivasyon
- Production-tested patterns
- MIT lisanslı, direkt kullanılabilir

**Planlamada Kullanımı**:
- Tüm bu skill'ler direkt skills/ dizinine eklendi
- Brainstorming ve plan-writing "ÇOK ÖNEMLİ" olarak işaretlendi
- TDD workflow tüm test-engineer agent'ına entegre edildi

---

### 2. jeremylongshore/claude-code-plugins-plus-skills ⭐⭐⭐⭐⭐
**URL**: https://github.com/jeremylongshore/claude-code-plugins-plus-skills
**Kapsam**: 258 plugin, 239 Agent Skill, 11 production playbook

**Kullanılan Plugin Packs**:
1. **devops-automation-pack**
   - CI/CD workflows
   - Deployment automation
   - Server management

2. **security-pack**
   - Code auditing
   - Vulnerability scanning
   - OWASP Top 10 checks

3. **api-development-pack**
   - FastAPI tooling
   - Node.js/Express helpers
   - OpenAPI/Swagger generation

4. **testing-pack**
   - Automated test generation
   - Coverage analysis
   - Test fixture patterns

**Kullanılan MCP Plugins**:
1. **project-health-auditor**
   - Codebase health analysis
   - Technical debt detection

2. **conversational-api-debugger**
   - API failure diagnosis
   - Interactive debugging

3. **git-commit-smart**
   - Intelligent commit messages
   - Conventional commits

**CLI Tool**: `ccpi` (Claude Code Plugin Installer)
**Kurulum**: `npm install -g ccpi`

**Planlamada Kullanımı**:
- Plugin installation guide eklendi (Faz 3)
- ccpi CLI kurulumu hızlı başlangıç adımlarına eklendi
- Recommended plugin packs listelendi

---

### 3. travisvn/awesome-claude-skills ⭐⭐⭐⭐
**URL**: https://github.com/travisvn/awesome-claude-skills

**Kullanılan Skills**:
1. **webapp-testing** (300 satır)
   - Playwright ile UI verification
   - E2E testing patterns
   - Visual regression testing

2. **artifacts-builder** (250 satır)
   - React/Tailwind/shadcn component construction
   - Component library patterns
   - Design system integration

3. **frontend-design** (200 satır)
   - "AI slop" avoidance
   - Design aesthetics
   - UX best practices
   - Accessibility-first design

4. **mcp-builder** (250 satır)
   - External API/service integration
   - MCP server creation guide
   - Tool integration patterns

5. **git-worktrees** (200 satır)
   - Isolated parallel development
   - Multiple branches simultaneously
   - Branch management

**Unique Pattern**: **Progressive Disclosure**
- Skills önce metadata (~100 tokens)
- Full instructions sadece gerektiğinde (<5k tokens)
- Token efficiency optimization

**Planlamada Kullanımı**:
- Tüm skill'ler skills/ dizinine eklendi
- Progressive disclosure pattern skill formatında kullanıldı

---

### 4. google/adk-samples ⭐⭐⭐ (Referans)
**URL**: https://github.com/google/adk-samples
**Kullanım**: Architecture patterns referansı

**Öğrenilen Patterns**:
1. **Domain Specialization**
   - Narrow, task-specific agents
   - Expertise boundaries
   - Clear agent responsibilities

2. **Multi-Language Architecture**
   - TypeScript, Python, Go examples
   - Language-agnostic patterns
   - Polyglot agent design

3. **Production-Ready Examples**
   - Toy implementations değil
   - Real-world use cases
   - Error handling, logging, monitoring

4. **Tool Integration Patterns**
   - External tool wrapping
   - API integration
   - Service mesh patterns

**Planlamada Kullanımı**:
- Agent specialization (10 ayrı uzman agent)
- Tool assignment (her agent'a specific tools)
- Production-ready kod emphasis

---

### 5. google-labs-code/jules-awesome-list ⭐⭐ (Referans)
**URL**: https://github.com/google-labs-code/jules-awesome-list

**Öğrenilen Patterns**:
1. **Category-Based Prompt Organization**
   - Clear kategorilendirme
   - Hiyerarşik yapı
   - Easy navigation

2. **Contextual Subsections**
   - When/why to apply
   - Use case scenarios
   - Decision trees

3. **Task Granularity**
   - Specific vs broad tasks
   - Task sizing
   - Dependency management

4. **Progressive Complexity**
   - Basit → Karmaşık
   - Learning curve
   - Incremental adoption

**Planlamada Kullanımı**:
- Skill kategorilendirmesi (Core, obra/superpowers, awesome-claude-skills)
- Faz bazlı implementation (Faz 1-4)
- Progressive implementation approach

---

## 🛠️ Metodolojiler ve Best Practices

### 1. Hook-Based Automation
**Kaynak**: Claude Code documentation + obra/superpowers
**Pattern**: Lifecycle event hooks
**Implementation**:
- `SessionStart` → Context loading, project detection
- `PreToolUse` → Risk prevention, error learning check
- `PostToolUse` → Error tracking, solution recording
- `SessionEnd` → Cleanup, statistics

### 2. Specialized Agents Pattern
**Kaynak**: google/adk-samples + Claude Code docs
**Pattern**: Single Responsibility Principle for AI agents
**Implementation**:
- 10 specialized agents (frontend, backend, database, etc.)
- Each with specific tools, skills, expertise
- YAML frontmatter + markdown content
- Clear agent boundaries

### 3. Progressive Disclosure
**Kaynak**: travisvn/awesome-claude-skills
**Pattern**: Load metadata first, full content on-demand
**Benefits**:
- Token efficiency
- Faster loading
- Scalable skill library
**Implementation**: YAML frontmatter (~100 tokens) + full content (<5k tokens)

### 4. Terminal Error Learning (YENİ - Orijinal)
**Kaynak**: Kullanıcı talebi + özel tasarım
**Pattern**: Self-improving AI through error tracking
**Components**:
- `pre-bash.ps1` → Pre-command error check
- `track-error.ps1` → Error + solution recording
- `error-database.json` → Pattern-based error storage
- `terminal-error-patterns` skill → Learning protocol

**Nasıl Çalışır**:
1. AI terminal komutu çalıştıracak
2. pre-bash.ps1 otomatik çalışır
3. error-database.json kontrol edilir
4. Geçmişte benzer hata varsa warning
5. Hata oluşursa track-error.ps1 kaydeder
6. AI çözerse, çözüm de kaydedilir
7. Bir sonraki sefere aynı hata yapılmaz

### 5. Parallel Agent Execution
**Kaynak**: obra/superpowers parallel-agents skill
**Pattern**: Concurrent task execution
**Implementation**: MASTER PROMPT'ta 10 agent paralel spawn
**Benefits**:
- Hız (paralel vs sequential)
- Resource utilization
- Independent task handling

---

## 🔧 Teknik Stack ve Teknolojiler

### Frontend
**Kaynaklar**: react-patterns, nextjs-best-practices, tailwind-patterns skills
**Teknolojiler**:
- React 18+ (Hooks, Suspense, Concurrent Mode)
- Next.js 14+ (App Router, Server Components, RSC)
- Tailwind CSS (Utility-first, responsive design)
- TypeScript (Type safety, developer experience)
- React Query, Zustand (State management)

### Backend
**Kaynaklar**: nodejs-best-practices, python-patterns skills
**Teknolojiler**:
- Node.js/Express (RESTful APIs)
- Python/FastAPI (High-performance APIs)
- Django (Full-stack framework)
- Authentication (JWT, OAuth, session-based)
- Error handling, logging, monitoring

### Database
**Kaynaklar**: database-design skill
**Teknolojiler**:
- PostgreSQL (Primary database)
- Schema design (Normalization, 3NF)
- Indexing (B-tree, Hash, GiST)
- Migrations (Version control for schema)
- Query optimization (EXPLAIN ANALYZE)

### DevOps
**Kaynaklar**: deployment-procedures, server-management skills + devops-automation-pack
**Teknolojiler**:
- PM2 (Process management)
- SSH (Secure server access)
- CI/CD (Automated pipelines)
- Monitoring (Logs, metrics, alerts)
- Rollback procedures (Emergency recovery)

### Testing
**Kaynaklar**: testing-patterns, tdd-workflow, webapp-testing skills
**Teknolojiler**:
- Jest (JavaScript unit testing)
- Pytest (Python unit testing)
- Playwright (E2E, UI testing)
- AAA pattern (Arrange-Act-Assert)
- Test factories, mocks, stubs

### Security
**Kaynaklar**: security-checklist skill + security-pack plugin
**Frameworks**:
- OWASP Top 10 (Web application security)
- SQL injection prevention
- XSS prevention
- CSRF protection
- Authentication & authorization best practices

### Mobile
**Kaynaklar**: mobile-patterns skill
**Teknolojiler**:
- React Native (Cross-platform)
- Flutter (High-performance mobile)
- Platform-specific code (iOS/Android)
- Mobile-first design

---

## 📋 Plan Yapısı ve Organizasyon

### Ana Bölümler

1. **Hedef ve Mevcut Durum Analizi**
   - Güçlü yanlar, eksikler
   - Kullanıcının mevcut setup'ı

2. **Kurulacak Bileşenler**
   - 6 PowerShell hooks
   - 10 specialized subagents
   - 26 agent skills
   - 9 slash commands
   - Plugins (official + community)

3. **Dosya Yapısı**
   - scripts/, agents/, skills/, .claude/commands/, data/
   - Her dosya için satır sayısı ve öncelik

4. **Uygulama Öncelikleri**
   - Faz 1: Temel Altyapı (1. Hafta)
   - Faz 2: Genişletme (2. Hafta)
   - Faz 3: Plugin Enhancement (3. Hafta)
   - Faz 4: Dokümantasyon (Ongoing)

5. **Kritik Dosyalar**
   - devops-engineer.md, deployment-procedures skill
   - session-start.ps1, deploy.md
   - pre-bash.ps1, track-error.ps1 (Terminal Error Learning)

6. **İmplementasyon Adımları**
   - Step-by-step PowerShell komutları
   - Test planları
   - Kullanım örnekleri

7. **Terminal Error Learning System**
   - Detaylı açıklama
   - Nasıl çalışır
   - Faydaları
   - Database yapısı

8. **GitHub Kaynakları**
   - obra/superpowers, jeremylongshore, travisvn, Google ADK
   - Her kaynak için detaylar

9. **Başarı Metrikleri**
   - Kurulum başarı kriterleri
   - Feature checklist

10. **Sürekli İyileştirme**
    - Haftalık, aylık, quarterly review

11. **Hızlı Başlangıç**
    - İlk 30 dakika adımları

12. **MASTER IMPLEMENTATION PROMPT**
    - Tek prompt ile tüm sistemi kurmak için
    - 10 agent paralel execution
    - Her agent'ın task'ı detaylı

---

## 🎓 Öğrenilen ve Uygulanan İlkeler

### 1. Single Responsibility Principle (SRP)
**Kaynak**: google/adk-samples
**Uygulama**: Her agent sadece bir alandan sorumlu
**Örnek**: frontend-specialist sadece React/Next.js, backend-specialist sadece Node/Python

### 2. Don't Repeat Yourself (DRY)
**Kaynak**: Best practices + obra/superpowers
**Uygulama**: Skill'ler reusable, agent'lar skill'leri kullanır
**Örnek**: deployment-procedures skill hem devops-engineer hem de deploy.md tarafından kullanılır

### 3. Progressive Enhancement
**Kaynak**: travisvn/awesome-claude-skills
**Uygulama**: Önce temel, sonra advanced features
**Örnek**: Faz 1 → Faz 2 → Faz 3 → Faz 4

### 4. Fail-Safe Defaults
**Kaynak**: Claude Code docs + security best practices
**Uygulama**: Riskli operasyonları önle, warning ver
**Örnek**: check-prevention.ps1, force operations detection

### 5. Self-Improving Systems
**Kaynak**: Kullanıcı talebi + ML/AI best practices
**Uygulama**: Terminal Error Learning
**Örnek**: AI hatalarından öğrenir, tekrar etmez

### 6. Separation of Concerns
**Kaynak**: Software architecture best practices
**Uygulama**: Hooks, agents, skills, commands ayrı dizinlerde
**Örnek**: scripts/, agents/, skills/, .claude/commands/

### 7. Convention Over Configuration
**Kaynak**: Claude Code docs
**Uygulama**: Standard dosya yapısı, naming conventions
**Örnek**: SKILL.md, YAML frontmatter, markdown content

---

## 🚀 İmplementasyon Stratejisi

### Paralel Execution (10 Agent)
**Kaynak**: obra/superpowers parallel-agents
**Strateji**: Tek message'da 10 Task tool call
**Agents**:
1. Agent 1: 6 PowerShell hooks
2. Agent 2: frontend-specialist
3. Agent 3: backend-specialist
4. Agent 4: database-architect
5. Agent 5: devops-engineer
6. Agent 6: 5 remaining agents
7. Agent 7: İlk 9 core skills + terminal-error-patterns
8. Agent 8: 9 remaining skills
9. Agent 9: 8 GitHub skills
10. Agent 10: 9 slash commands

**Neden Paralel**:
- Hız (10x faster than sequential)
- Independent tasks
- Resource optimization
- No dependencies between agents

### Error Handling
**Kaynak**: Best practices + Terminal Error Learning
**Strateji**:
1. Robust error handling her script'te
2. Hataları database'e kaydet
3. Çözümleri kaydet
4. Pattern matching
5. Recurring error detection

### Testing Strategy
**Kaynak**: tdd-workflow skill + testing-patterns
**Strateji**:
1. Hook testing (PowerShell manual test)
2. Agent testing (Use agent in conversation)
3. Slash command testing (Execute commands)
4. Integration testing (Full workflow)
5. Terminal Error Learning testing (Simulate errors)

---

## 📊 Success Metrics (Başarı Kriterleri)

### Technical Metrics
1. ✅ 6 PowerShell script oluşturuldu ve çalışıyor
2. ✅ 10 agent markdown dosyası oluşturuldu
3. ✅ 26 skill SKILL.md dosyası oluşturuldu
4. ✅ 9 slash command markdown dosyası oluşturuldu
5. ✅ error-database.json initialized
6. ✅ Tüm dosyalar belirtilen path'lerde
7. ✅ Her dosya production-ready

### Functional Metrics
1. ✅ Session başlangıcında context otomatik yükleniyor
2. ✅ Prompt yazdığında agent/skill önerisi geliyor
3. ✅ Brainstorming otomatik başlıyor
4. ✅ Implementation plan otomatik yazılıyor
5. ✅ `/review` komutu çalışıyor
6. ✅ `/test` komutu test generate edip çalıştırıyor
7. ✅ TDD workflow enforce ediliyor
8. ✅ `/deploy` güvenli deploy yapıyor
9. ✅ Terminal hatalarından öğreniliyor
10. ✅ Riskli operasyonlar warning veriyor

### Quality Metrics
1. ✅ Agent'lar doğru skill'leri kullanıyor
2. ✅ LSP plugins code intelligence sağlıyor
3. ✅ Parallel agents concurrent çalışıyor
4. ✅ Session sonu özeti kaydediliyor
5. ✅ Error learning system effectiveness (kaç hata önlendi)

---

## ⚠️ Önemli Notlar ve Kısıtlamalar

### Generic Implementation
**Not**: Tüm Owl-App spesifik referanslar kaldırıldı
**Neden**: Plan genel kullanım için, tek projeye özgü değil
**Değişiklikler**:
- ❌ Production server IP (46.224.36.165) → Kaldırıldı
- ❌ `/owl` command → Kaldırıldı
- ❌ Owl-App specific paths → Generic examples

### Windows Ortam
**Kısıt**: PowerShell 5.1+ gerekli
**Not**: Path'ler Windows formatında (backslash)
**Alternatif**: Linux/Mac için bash scriptleri gerekli (plan kapsamı dışı)

### GLM Models
**Not**: Z.AI endpoint, standard Claude modelleri değil
**Potansiyel Sorun**: Bazı Claude özellikleri farklı çalışabilir
**Çözüm**: Test ederek doğrulamak gerekli

### Token Limitations
**Not**: MASTER PROMPT çok uzun olabilir
**Alternatif**: İlk 5 agent, sonra kalan 5 agent şeklinde bölebilirsiniz
**Çözüm**: Plan'da belirtildi

### Security
**Kritik**: PowerShell scriptleri otomatik çalışıyor
**Gerekli**: Security review
**Önlem**: check-prevention.ps1 riskli operasyonları engeller

---

## 📅 Geliştirme Zaman Çizelgesi (Tahmini)

### Faz 1: Temel Altyapı (1 Hafta)
- Gün 1-2: PowerShell hooks (6 script)
- Gün 3-6: İlk 5 core agent
- Gün 7: İlk 9 core skill + terminal-error-patterns

### Faz 2: Genişletme (1 Hafta)
- Gün 1-2: Kalan 5 agent
- Gün 3-5: Kalan 17 skill
- Gün 6-7: 9 slash command

### Faz 3: Plugin Enhancement (1 Hafta)
- Gün 1: Official Anthropic plugins
- Gün 2-3: Community plugins (ccpi)
- Gün 4: GitHub integration (obra/superpowers)
- Gün 5-7: Project context files, testing

### Faz 4: Dokümantasyon (Ongoing)
- Master README
- Testing & Refinement
- Continuous improvement

**Toplam**: ~3 hafta (intensive), veya ~6 hafta (part-time)

---

## 🔄 Bakım ve Güncelleme

### Haftalık
- Error log review
- Hook performance check
- Workflow shortcuts için feedback

### Aylık
- Agent prompt optimization
- Yeni skill'ler (öğrenilen patterns)
- Slash command expansion
- Terminal error patterns → skill migration

### Quarterly
- Tüm agent'ları review ve update
- Skill effectiveness measurement
- Yeni plugin research
- Error learning system metrics

---

## 📞 Destek ve Topluluk Kaynakları

### Official
- Claude Code GitHub: https://github.com/anthropics/claude-code
- Claude Code Issues: https://github.com/anthropics/claude-code/issues
- Anthropic Documentation: https://docs.anthropic.com/

### Community
- obra/superpowers: https://github.com/obra/superpowers
- claude-code-plugins: https://github.com/jeremylongshore/claude-code-plugins-plus-skills
- awesome-claude-skills: https://github.com/travisvn/awesome-claude-skills

### Tools
- ccpi CLI: npm package for plugin installation
- Context7 MCP server: Context management
- Sequential-thinking MCP: Structured reasoning

---

## 🎯 Sonuç

Bu plan, aşağıdaki kaynaklara dayalı olarak hazırlanmıştır:

1. **Primary Sources**:
   - Claude Code resmi dokümantasyonu
   - Mevcut kullanıcı konfigürasyonu (settings.json)

2. **GitHub Repositories** (5 repo):
   - obra/superpowers (MIT licensed, 5 kritik skill)
   - jeremylongshore/claude-code-plugins-plus-skills (plugin ecosystem)
   - travisvn/awesome-claude-skills (progressive disclosure pattern)
   - google/adk-samples (architecture patterns)
   - google-labs-code/jules-awesome-list (organization patterns)

3. **Best Practices**:
   - Software architecture principles (SRP, DRY, separation of concerns)
   - AI/ML best practices (self-improving systems)
   - Security best practices (fail-safe defaults, risk prevention)
   - DevOps best practices (CI/CD, monitoring, rollback)

4. **Orijinal Katkılar**:
   - **Terminal Error Learning System** (tamamen orijinal tasarım)
   - Generic implementation (project-agnostic)
   - Paralel agent execution strategy
   - Turkish language support (encoding fixes)

**Plan Amacı**: Solo entrepreneurs için production-ready, self-improving, full-stack AI development team.

**İmplementasyon**: Tek MASTER PROMPT ile 10 agent paralel execution → 3 hafta çıktı.

**Bakım**: Self-improving (Terminal Error Learning) + continuous improvement (haftalık/aylık/quarterly).

---

**Hazırlayan**: AI Assistant (Claude Sonnet 4.5)
**Tarih**: 2025-01-XX
**Versiyon**: 1.0
**Lisans**: Plana katkı sağlayan GitHub repoları MIT lisanslı (kullanılabilir)

Başarılar! 🚀
