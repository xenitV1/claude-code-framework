#!/usr/bin/env python3
"""
Parallel Agent Orchestrator - Coordinator that runs multiple local agents in parallel.
Each agent shares status upon completion, and a synthesis report is generated at the end.

Usage:
    python scripts/parallel_orchestrator.py "Your task..." --agents 3
"""

import os
import json
import sys
import uuid
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
ORCHESTRATOR_STATE_FILE = DATA_DIR / "orchestrator-state.json"

# Progress Reporter Import (using script calling method instead of dynamic loading to avoid errors)
SCRIPTS_DIR = Path(__file__).parent
PROGRESS_REPORTER = SCRIPTS_DIR / "progress_reporter.py"

def run_progress_reporter(cmd: str, *args):
    """Call progress_reporter.py script."""
    try:
        subprocess.run([sys.executable, str(PROGRESS_REPORTER), cmd, *args], capture_output=True)
    except Exception:
        pass

class AgentTask:
    def __init__(self, agent_id: str, prompt: str, name: str = ""):
        self.agent_id = agent_id
        self.prompt = prompt
        self.name = name or f"Agent-{agent_id[:4]}"
        self.status = "pending"
        self.result = ""
        self.started_at = None
        self.ended_at = None

    def execute(self, test_mode: bool = False):
        self.status = "running"
        self.started_at = datetime.now().isoformat()
        run_progress_reporter("update", self.name, "running", self.prompt[:50], "10")
        
        try:
            if test_mode:
                # Mock execution
                import random
                sleep_time = random.uniform(2, 5)
                time.sleep(sleep_time)
                self.result = f"MOCK RESULT for {self.name}: Analyzed {self.prompt[:30]}... found 3 issues."
                self.status = "completed"
                run_progress_reporter("update", self.name, "completed", "Mock Done", "100")
            else:
                # Real execution using Claude Code CLI
                process = subprocess.Popen(
                    ["claude", self.prompt],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8"
                )
                
                stdout, stderr = process.communicate()
                
                self.result = stdout
                if process.returncode != 0:
                    self.status = "failed"
                    self.error = stderr
                    run_progress_reporter("update", self.name, "failed", stderr[:50], "100")
                else:
                    self.status = "completed"
                    run_progress_reporter("update", self.name, "completed", "Done", "100")
                
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            run_progress_reporter("update", self.name, "failed", str(e)[:50], "0")
        
        self.ended_at = datetime.now().isoformat()
        return self

class Orchestrator:
    def __init__(self, main_prompt: str, agent_count: int = 3, test_mode: bool = False):
        self.main_prompt = main_prompt
        self.agent_count = agent_count
        self.test_mode = test_mode
        self.session_id = str(uuid.uuid4())
        self.tasks: List[AgentTask] = []
        self.results = {}

    def ensure_dirs(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def initialize_tasks(self):
        """Divide main prompt by agent count and assign to relevant local agent."""
        # Task - Agent matching
        agent_map = [
            {"perspective": "Architecture & Security", "agent": "security-auditor", "skills": "security-checklist, api-patterns"},
            {"perspective": "Backend Implementation", "agent": "backend-specialist", "skills": "nodejs-best-practices, api-patterns"},
            {"perspective": "Frontend & UI/UX", "agent": "frontend-specialist", "skills": "react-patterns, tailwind-patterns"},
            {"perspective": "Testing", "agent": "test-engineer", "skills": "testing-patterns, webapp-testing"},
            {"perspective": "DevOps & Performance", "agent": "devops-engineer", "skills": "deployment-procedures, server-management"}
        ]
        
        for i in range(self.agent_count):
            map_item = agent_map[i % len(agent_map)]
            perspective = map_item["perspective"]
            agent_name = map_item["agent"]
            skills = map_item["skills"]
            
            # Sub-agent tetikleyici komut ekle
            sub_prompt = f"Use the {agent_name} agent with {skills} skills to focus on {perspective}: {self.main_prompt}"
            
            agent_id = str(uuid.uuid4())
            task = AgentTask(agent_id, sub_prompt, f"{agent_name}")
            self.tasks.append(task)

    def save_state(self):
        state = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "main_prompt": self.main_prompt,
            "tasks": [
                {
                    "id": t.agent_id,
                    "name": t.name,
                    "status": t.status,
                    "started_at": t.started_at,
                    "ended_at": t.ended_at,
                    "result_snippet": t.result[:200] if t.result else ""
                } for t in self.tasks
            ]
        }
        ORCHESTRATOR_STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    def run(self):
        self.ensure_dirs()
        self.initialize_tasks()
        self.save_state()
        
        mode_str = " (TEST MODE)" if self.test_mode else ""
        print(f"🚀 Orchestrator started: {self.session_id}{mode_str}")
        print(f"👥 Spawning {self.agent_count} parallel agents...")
        
        with ThreadPoolExecutor(max_workers=self.agent_count) as executor:
            futures = {executor.submit(task.execute, self.test_mode): task for task in self.tasks}
            
            for future in as_completed(futures):
                task = futures[future]
                try:
                    task = future.result()
                    print(f"✅ {task.name} finished: {task.status}")
                except Exception as e:
                    print(f"❌ {task.name} crashed: {e}")
                
                self.save_state()

        self.synthesize()

    def synthesize(self):
        """Collect all agent results and create a synthesis."""
        print("\n🧠 Synthesizing results...")
        
        synthesis_content = f"# Parallel Agents Synthesis Report\n"
        synthesis_content += f"**Session ID**: {self.session_id}\n"
        synthesis_content += f"**Main Objective**: {self.main_prompt}\n\n"
        synthesis_content += "---\n\n"
        
        for t in self.tasks:
            synthesis_content += f"### {t.name}\n"
            synthesis_content += f"- **Task**: {t.prompt[:100]}...\n"
            synthesis_content += f"- **Status**: {t.status}\n"
            synthesis_content += f"- **Key Findings**:\n\n{t.result if t.result else 'No output generated.'}\n\n"
            synthesis_content += "---\n\n"
        
        reports_dir = DATA_DIR / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = reports_dir / f"synthesis_report_{self.session_id[:8]}.md"
        report_file.write_text(synthesis_content, encoding="utf-8")
        
        print(f"✨ Final synthesis report generated: {report_file}")
        
def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/parallel_orchestrator.py \"your task\" [--agents N] [--test]")
        return
    
    prompt = sys.argv[1]
    agents = 3
    test_mode = "--test" in sys.argv
    
    if "--agents" in sys.argv:
        idx = sys.argv.index("--agents")
        if idx + 1 < len(sys.argv):
            try:
                agents = int(sys.argv[idx + 1])
            except ValueError:
                pass
            
    orchestrator = Orchestrator(prompt, agents, test_mode)
    orchestrator.run()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
