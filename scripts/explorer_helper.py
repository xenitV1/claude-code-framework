import os
import io
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Debug logging
DEBUG_LOG = Path.home() / ".claude" / "data" / "hook_debug.log"

def debug_log(message: str):
    """Write debug log."""
    try:
        DEBUG_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DEBUG_LOG, "a", encoding="utf-8") as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] explorer_helper.py: {message}\n")
    except Exception as e:
        sys.stderr.write(f"DEBUG_LOG_ERROR: {e}\n")

def get_project_tree(path, max_depth=5, current_depth=0):
    if current_depth > max_depth:
        return "..."
    
    tree = {}
    try:
        for item in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            if item.name.startswith(('.', 'node_modules', 'venv', '__pycache__')):
                continue
                
            if item.is_dir():
                tree[item.name] = get_project_tree(item, max_depth, current_depth + 1)
            else:
                tree[item.name] = "file"
    except PermissionError:
        return "🔒 Access Denied"
    
    return tree

def get_project_survey(root_path=".", max_depth=5):
    root = Path(root_path).resolve()
    survey = {
        "root": str(root),
        "tech_stack": [],
        "entry_points": [],
        "dependencies": {},
        "structure": get_project_tree(root, max_depth=max_depth)
    }

    # Tech Stack Detection (looking deep)
    tech_identifiers = {
        "package.json": "Node.js/NPM",
        "tsconfig.json": "TypeScript",
        "requirements.txt": "Python (pip)",
        "pyproject.toml": "Python (Poetry/Flit)",
        "next.config.js": "Next.js",
        "next.config.mjs": "Next.js",
        "tailwind.config.js": "Tailwind CSS",
        "prisma/schema.prisma": "Prisma ORM",
        "expo.json": "Expo/React Native",
        "app.json": "React Native/Expo",
        "docker-compose.yml": "Docker Compose",
        "settings.json": "Maestro (Settings)",
        "CLAUDE.md": "Maestro (Context)",
        ".env": "Environment Config"
    }

    # Deep tech detection
    def detect_tech(path, depth=0):
        if depth > 3: return # Don't look too deep for tech config
        try:
            for item in path.iterdir():
                if item.name in tech_identifiers:
                    tech = tech_identifiers[item.name]
                    if tech not in survey["tech_stack"]:
                        survey["tech_stack"].append(tech)
                    
                    if item.name == "package.json":
                        try:
                            with open(item, 'r') as f:
                                pkg = json.load(f)
                                survey["dependencies"]["npm"] = list(pkg.get("dependencies", {}).keys())
                        except:
                            pass
                elif item.is_dir() and not item.name.startswith('.'):
                    detect_tech(item, depth + 1)
        except:
            pass

    detect_tech(root)

    # Entry Point Identification (looking deep)
    possible_entries = ["src/index.ts", "src/main.ts", "src/index.js", "index.js", "app.py", "main.py", "app.js"]
    for entry in possible_entries:
        if (root / entry).exists():
            survey["entry_points"].append(entry)

    return survey

def main():
    debug_log(f"MAIN called: argv={sys.argv}")

    parser = argparse.ArgumentParser(description="Deep project discovery for Claude Code CLI.")
    parser.add_argument("path", nargs="?", default=".", help="Root path to scan")
    parser.add_argument("depth", type=int, nargs="?", default=5, help="Scan depth")
    parser.add_argument("--silent", action="store_true", help="Suppress terminal output")

    args = parser.parse_args()

    debug_log(f"Parsed: path={args.path}, depth={args.depth}, silent={args.silent}")

    try:
        # For Windows terminal unicode support
        if sys.platform == "win32":
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

    try:
        report = get_project_survey(args.path, max_depth=args.depth)
        debug_log(f"Survey completed: {len(report.get('tech_stack', []))} techs found")

        # Project-based data directory
        CLAUDE_DIR = Path.home() / ".claude"
        DATA_DIR = CLAUDE_DIR / "data"
        PROJECTS_DIR = DATA_DIR / "projects"
        
        # Convert project name to safe file name
        project_name = Path(report["root"]).name
        safe_name = "".join(c if c.isalnum() or c in '-_' else '_' for c in project_name)
        project_dir = PROJECTS_DIR / safe_name
        project_dir.mkdir(parents=True, exist_ok=True)

        output_file = project_dir / "discovery-report.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        debug_log(f"Report saved to {output_file}")

        if not args.silent:
            print(f"✅ Deep project discovery completed (Depth: {args.depth}).")
            print(f"Report saved to {output_file}")
            print(f"Tech Stack Detected: {', '.join(report['tech_stack'])}")

        debug_log("EXPLORER completed successfully")
    except Exception as e:
        debug_log(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        debug_log(f"TRACEBACK: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()
