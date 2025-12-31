#!/usr/bin/env python3
"""
Token Tracker - Track and estimate token usage per session.

This hook tracks tool usage and estimates token consumption.
Called after each tool use to accumulate statistics.

Usage:
    python token_tracker.py track <tool_name> <input_size> <output_size>
    python token_tracker.py summary
    python token_tracker.py reset

Environment:
    TOOL_NAME: Name of the tool used
    TOOL_INPUT: Input provided to the tool
    TOOL_OUTPUT: Output from the tool
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Paths
CLAUDE_DIR = Path.home() / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
CURRENT_PROJECT_FILE = DATA_DIR / "current-project.json"
GLOBAL_TOKEN_STATS = DATA_DIR / "token-stats.json"
TOKEN_HISTORY = DATA_DIR / "token-history.json"

# Token estimation constants
CHARS_PER_TOKEN = 4  # Average characters per token (conservative estimate)

# Cost estimates (USD per 1M tokens) - Claude 3.5 Sonnet pricing
COST_PER_1M_INPUT = 3.00
COST_PER_1M_OUTPUT = 15.00


def estimate_tokens(text: str) -> int:
    """Estimate token count from text."""
    if not text:
        return 0
    return max(1, len(text) // CHARS_PER_TOKEN)


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    """Estimate cost in USD."""
    input_cost = (input_tokens / 1_000_000) * COST_PER_1M_INPUT
    output_cost = (output_tokens / 1_000_000) * COST_PER_1M_OUTPUT
    return input_cost + output_cost


def get_current_project() -> Optional[Dict[str, Any]]:
    """Get current project info."""
    if CURRENT_PROJECT_FILE.exists():
        try:
            return json.loads(CURRENT_PROJECT_FILE.read_text())
        except:
            pass
    return None


def get_project_stats_file() -> Path:
    """Get token stats file for current project."""
    project = get_current_project()
    if project and project.get("dataDir"):
        return Path(project["dataDir"]) / "token-stats.json"
    return GLOBAL_TOKEN_STATS


def load_stats(stats_file: Path) -> Dict[str, Any]:
    """Load stats from file."""
    if stats_file.exists():
        try:
            return json.loads(stats_file.read_text())
        except:
            pass

    return {
        "sessionStart": datetime.now().isoformat(),
        "totalInputTokens": 0,
        "totalOutputTokens": 0,
        "totalCost": 0.0,
        "toolCalls": [],
        "toolStats": {}
    }


def save_stats(stats: Dict[str, Any], stats_file: Path):
    """Save stats to file."""
    stats_file.parent.mkdir(parents=True, exist_ok=True)
    stats_file.write_text(json.dumps(stats, indent=2, ensure_ascii=False))


def track_usage(tool_name: str, input_text: str, output_text: str):
    """Track a single tool usage."""
    stats_file = get_project_stats_file()
    stats = load_stats(stats_file)

    # Estimate tokens
    input_tokens = estimate_tokens(input_text)
    output_tokens = estimate_tokens(output_text)
    cost = estimate_cost(input_tokens, output_tokens)

    # Update totals
    stats["totalInputTokens"] += input_tokens
    stats["totalOutputTokens"] += output_tokens
    stats["totalCost"] += cost
    stats["lastUpdate"] = datetime.now().isoformat()

    # Track per-tool statistics
    if tool_name not in stats["toolStats"]:
        stats["toolStats"][tool_name] = {
            "count": 0,
            "inputTokens": 0,
            "outputTokens": 0,
            "cost": 0.0
        }

    stats["toolStats"][tool_name]["count"] += 1
    stats["toolStats"][tool_name]["inputTokens"] += input_tokens
    stats["toolStats"][tool_name]["outputTokens"] += output_tokens
    stats["toolStats"][tool_name]["cost"] += cost

    # Keep last 50 tool calls for detail
    stats["toolCalls"].append({
        "tool": tool_name,
        "timestamp": datetime.now().isoformat(),
        "inputTokens": input_tokens,
        "outputTokens": output_tokens,
        "cost": cost
    })

    # Trim to last 50
    if len(stats["toolCalls"]) > 50:
        stats["toolCalls"] = stats["toolCalls"][-50:]

    save_stats(stats, stats_file)

    # Output tracking confirmation (JSON for Claude)
    result = {
        "tracked": True,
        "tool": tool_name,
        "inputTokens": input_tokens,
        "outputTokens": output_tokens,
        "sessionTotal": {
            "inputTokens": stats["totalInputTokens"],
            "outputTokens": stats["totalOutputTokens"],
            "estimatedCost": f"${stats['totalCost']:.4f}"
        }
    }

    return result


def show_summary(verbose: bool = False):
    """Show session summary."""
    stats_file = get_project_stats_file()
    stats = load_stats(stats_file)

    total_input = stats.get("totalInputTokens", 0)
    total_output = stats.get("totalOutputTokens", 0)
    total_cost = stats.get("totalCost", 0.0)
    tool_stats = stats.get("toolStats", {})

    # Calculate session duration
    duration = "unknown"
    if stats.get("sessionStart"):
        try:
            start = datetime.fromisoformat(stats["sessionStart"])
            duration = str(datetime.now() - start).split(".")[0]  # Remove microseconds
        except:
            pass

    print("\n" + "=" * 50)
    print("📊 TOKEN USAGE SUMMARY")
    print("=" * 50)
    print(f"⏱️  Session Duration: {duration}")
    print(f"📥 Input Tokens:  {total_input:,}")
    print(f"📤 Output Tokens: {total_output:,}")
    print(f"📦 Total Tokens:  {total_input + total_output:,}")
    print(f"💰 Estimated Cost: ${total_cost:.4f}")
    print("-" * 50)

    if tool_stats:
        print("\n🔧 BY TOOL:")
        # Sort by cost (descending)
        sorted_tools = sorted(
            tool_stats.items(),
            key=lambda x: x[1]["cost"],
            reverse=True
        )

        for tool_name, data in sorted_tools[:10]:  # Top 10
            count = data["count"]
            tool_cost = data["cost"]
            pct = (tool_cost / total_cost * 100) if total_cost > 0 else 0
            print(f"   {tool_name}: {count}x calls, ${tool_cost:.4f} ({pct:.1f}%)")

    print("=" * 50 + "\n")

    # Also output JSON for Claude
    return {
        "summary": {
            "duration": duration,
            "inputTokens": total_input,
            "outputTokens": total_output,
            "totalTokens": total_input + total_output,
            "estimatedCost": f"${total_cost:.4f}",
            "toolBreakdown": tool_stats
        }
    }


def reset_stats():
    """Reset session stats."""
    stats_file = get_project_stats_file()

    # Archive current stats before reset
    if stats_file.exists():
        try:
            old_stats = json.loads(stats_file.read_text())

            # Append to history
            history_file = TOKEN_HISTORY
            history = []
            if history_file.exists():
                try:
                    history = json.loads(history_file.read_text())
                except:
                    pass

            old_stats["archivedAt"] = datetime.now().isoformat()
            history.append(old_stats)

            # Keep last 100 sessions
            if len(history) > 100:
                history = history[-100:]

            history_file.parent.mkdir(parents=True, exist_ok=True)
            history_file.write_text(json.dumps(history, indent=2, ensure_ascii=False))
        except:
            pass

    # Create fresh stats
    fresh_stats = {
        "sessionStart": datetime.now().isoformat(),
        "totalInputTokens": 0,
        "totalOutputTokens": 0,
        "totalCost": 0.0,
        "toolCalls": [],
        "toolStats": {}
    }

    save_stats(fresh_stats, stats_file)
    print("✅ Token stats reset for new session")

    return {"reset": True, "timestamp": datetime.now().isoformat()}


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python token_tracker.py track <tool_name> <input> <output>")
        print("  python token_tracker.py summary")
        print("  python token_tracker.py reset")
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command == "track":
            # Get tool info from args or environment
            tool_name = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("TOOL_NAME", "unknown")
            input_text = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("TOOL_INPUT", "")
            output_text = sys.argv[4] if len(sys.argv) > 4 else os.environ.get("TOOL_OUTPUT", "")

            result = track_usage(tool_name, input_text, output_text)
            # Silent output - just track

        elif command == "summary":
            result = show_summary(verbose="--verbose" in sys.argv or "-v" in sys.argv)

        elif command == "reset":
            result = reset_stats()

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        # Windows terminal unicode support
        if sys.platform == "win32":
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass
    main()
