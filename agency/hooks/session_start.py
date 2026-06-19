#!/usr/bin/env python3
"""Agency SessionStart hook — model reminder + lessons injection.

Called by Claude Code at session start via settings.json:
    {
      "hooks": {
        "SessionStart": [{"command": "python -m agency.hooks.session_start"}]
      }
    }

Reads handoff.md for current stage → model mismatch reminder.
Reads ~/.claude/lessons.md recent entries → injects into context.
Silent on failure — never blocks session start.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# ── Stage → Model mapping (must match workflow.sh) ──
STAGE_MODEL = {
    "-1": "DeepSeek V4 Pro",
    "0": "DeepSeek V4 Pro",
    "1": "DeepSeek V4 Pro",
    "2": "DeepSeek V4 Pro",
    "3": "DeepSeek V4 Pro",
    "4": "DeepSeek V4 Pro",
    "5": "MiMo V2.5 Pro",
    "6": "DeepSeek V4 Pro",
    "7": "MiMo V2.5 Pro",
    "8": "DeepSeek V4 Pro",
    "9": "DeepSeek V4 Pro",
}


def find_handoff(cwd):
    """Search for handoff.md from cwd upward."""
    p = Path(cwd)
    while p != p.parent:
        candidate = p / ".context" / "handoff.md"
        if candidate.exists():
            return candidate
        p = p.parent
    return None


def extract_stage(handoff_path):
    """Extract current stage number from handoff.md.

    Expected format: ## stage: N  (line starts with exactly this)
    """
    try:
        text = handoff_path.read_text(encoding="utf-8")
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("## stage:") or line.startswith("## Stage:"):
                # Extract number after colon
                after = line.split(":", 1)[1].strip()
                # Take first numeric part (handles "-1" or "3" or "9 (复盘)")
                import re
                m = re.search(r"(-?\d+)", after)
                if m:
                    return m.group(1)
    except Exception:
        pass
    return None


def recent_lessons(limit=5):
    """Read L3-always lessons (always injected) + recent L2 lessons.

    Lesson directory structure:
      ~/.claude/lessons/
        L3-always/   ← always injected (core behavioral rules)
        L2-tagged/   ← injected when context matches tags
        L1-archived/ ← never auto-injected (historical)
    """
    lessons_dir = Path.home() / ".claude" / "lessons"

    parts = []

    # L3-always: inject all (these are core rules, ≤5 files by convention)
    l3_dir = lessons_dir / "L3-always"
    if l3_dir.is_dir():
        for f in sorted(l3_dir.glob("*.md")):
            try:
                content = f.read_text(encoding="utf-8").strip()
                if content:
                    parts.append(content)
            except Exception:
                pass

    # L2-tagged: inject only recent 2 (too many = context bloat)
    l2_dir = lessons_dir / "L2-tagged"
    if l2_dir.is_dir():
        l2_files = sorted(l2_dir.glob("*.md"), key=lambda p: p.name, reverse=True)
        for f in l2_files[:2]:
            try:
                content = f.read_text(encoding="utf-8").strip()
                if content:
                    parts.append(content)
            except Exception:
                pass

    if parts:
        return "=== 最近教训 (SessionStart 自动注入) ===\n\n" + "\n\n---\n\n".join(parts)
    return ""


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return

        hook_data = json.loads(raw)
        cwd = hook_data.get("cwd", "")

        parts = []

        # ── Model reminder ──
        handoff = find_handoff(cwd) if cwd else None
        if handoff:
            stage = extract_stage(handoff)
            if stage and stage in STAGE_MODEL:
                expected = STAGE_MODEL[stage]
                parts.append(
                    f"[Agency] 当前阶段 {stage} → 推荐模型: {expected}。"
                    f"运行 source scripts/workflow.sh {stage} 切换。"
                )

        # ── Lessons injection ──
        lessons = recent_lessons()
        if lessons.strip():
            parts.append(f"=== 最近教训 (SessionStart 自动注入) ===\n{lessons}")

        if parts:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": "\n\n".join(parts),
                }
            }
            print(json.dumps(output, ensure_ascii=False))

        # ── Sync check (after output, as stderr info) ──
        # Check if deployed agents are older than source (agency-v2 repo)
        src_agents = Path(__file__).resolve().parent.parent.parent.parent / "agents"
        deployed_agents = Path.home() / ".claude" / "agents"
        if src_agents.is_dir() and deployed_agents.is_dir():
            try:
                src_newest = max(f.stat().st_mtime for f in src_agents.glob("*.md"))
                deployed_newest = max(f.stat().st_mtime for f in deployed_agents.glob("*.md"))
                if src_newest > deployed_newest + 60:  # >1 min newer = source updated
                    reminder = (
                        "[Agency] agents/skills 有更新。运行 bash install.sh --sync 同步。"
                    )
                    print(json.dumps({
                        "hookSpecificOutput": {
                            "hookEventName": "SessionStart",
                            "additionalContext": reminder,
                        }
                    }, ensure_ascii=False))
            except Exception:
                pass

    except Exception:
        # Never block session start
        pass


if __name__ == "__main__":
    main()
