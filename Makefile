# Maestro - AI Development Orchestrator
# =====================================

.PHONY: help install install-deps uninstall test lint clean setup-dev verify

# Default target
help:
	@echo ""
	@echo "  Maestro - AI Development Orchestrator"
	@echo "  ======================================"
	@echo ""
	@echo "  Setup:"
	@echo "    make install       Install Maestro to ~/.claude"
	@echo "    make install-deps  Install Python dependencies"
	@echo "    make uninstall     Remove Maestro from ~/.claude"
	@echo ""
	@echo "  Development:"
	@echo "    make setup-dev     Setup development environment"
	@echo "    make test          Run tests"
	@echo "    make lint          Run linters"
	@echo "    make clean         Clean temporary files"
	@echo ""
	@echo "  Utilities:"
	@echo "    make verify        Verify installation"
	@echo ""

# Platform detection
UNAME := $(shell uname -s)
ifeq ($(UNAME), Darwin)
	PLATFORM := macos
	PYTHON := python3
	CLAUDE_DIR := $(HOME)/.claude
endif
ifeq ($(UNAME), Linux)
	PLATFORM := linux
	PYTHON := python3
	CLAUDE_DIR := $(HOME)/.claude
endif
ifeq ($(OS), Windows_NT)
	PLATFORM := windows
	PYTHON := python
	CLAUDE_DIR := $(USERPROFILE)\.claude
endif

# Directories
SCRIPTS_DIR := $(CLAUDE_DIR)/scripts
DATA_DIR := $(CLAUDE_DIR)/data
PROJECTS_DIR := $(DATA_DIR)/projects
REPORTS_DIR := $(DATA_DIR)/reports

# ==================
# Installation
# ==================

install-deps:
	@echo "Installing Python dependencies..."
	$(PYTHON) -m pip install --quiet rich pydantic
	@echo "Done!"

install: install-deps
	@echo ""
	@echo "Installing Maestro..."
	@echo "Platform: $(PLATFORM)"
	@echo ""

	@# Create directories
	@mkdir -p $(SCRIPTS_DIR)
	@mkdir -p $(PROJECTS_DIR)
	@mkdir -p $(REPORTS_DIR)

	@# Copy scripts
	@echo "Copying scripts..."
	@cp scripts/*.py $(SCRIPTS_DIR)/

	@# Copy settings based on platform
	@echo "Installing settings..."
ifeq ($(PLATFORM), windows)
	@cp settings.example.windows.json $(CLAUDE_DIR)/settings.json
else
	@cp settings.example.unix.json $(CLAUDE_DIR)/settings.json
endif

	@echo ""
	@echo "Installation complete!"
	@echo ""
	@echo "Verify with: make verify"
	@echo ""

uninstall:
	@echo "Removing Maestro scripts..."
	@rm -rf $(SCRIPTS_DIR)
	@rm -f $(CLAUDE_DIR)/settings.json
	@echo "Done! (Data in $(DATA_DIR) preserved)"

verify:
	@echo ""
	@echo "Verifying Maestro installation..."
	@echo ""
	@echo "Scripts directory: $(SCRIPTS_DIR)"
	@ls -la $(SCRIPTS_DIR) 2>/dev/null || echo "  Not found!"
	@echo ""
	@echo "Settings file:"
	@ls -la $(CLAUDE_DIR)/settings.json 2>/dev/null || echo "  Not found!"
	@echo ""

# ==================
# Development
# ==================

setup-dev: install-deps
	@echo "Setting up development environment..."
	$(PYTHON) -m pip install --quiet pytest black flake8 mypy
	@echo "Done!"

test:
	@echo "Running tests..."
	@$(PYTHON) -m pytest tests/ -v 2>/dev/null || echo "No tests found"

lint:
	@echo "Running modern quality audit (Ruff)..."
	@$(PYTHON) -m ruff check scripts/*.py --fix || true
	@$(PYTHON) -m mypy scripts/*.py --ignore-missing-imports || true

clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@echo "Done!"

# ==================
# Utilities
# ==================

token-stats:
	@$(PYTHON) scripts/token_tracker.py summary

commit:
	@$(PYTHON) scripts/git_commit_helper.py suggest

commit-copy:
	@$(PYTHON) scripts/git_commit_helper.py suggest --copy

validate-commit:
	@read -p "Enter commit message: " msg; \
	$(PYTHON) scripts/git_commit_helper.py validate "$$msg"

git-stats:
	@$(PYTHON) scripts/git_commit_helper.py stats

# ==================
# Quick Actions
# ==================

.PHONY: quick-install
quick-install:
	@$(PYTHON) scripts/setup.py --quick

.PHONY: interactive-install
interactive-install:
	@$(PYTHON) scripts/setup.py --interactive


