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
    """Extract current stage number from handoff.md."""
    try:
        text = handoff_path.read_text(encoding="utf-8")
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("当前状态") or line.startswith("进入阶段"):
                # e.g. "Agency v2 技术选型完成，进入阶段 3（数据/API 设计）"
                for ch in line:
                    if ch in "0123456789":
                        return ch
                    if ch == "-":
                        continue
                # Try to find stage number
                import re
                m = re.search(r"阶段\s*(\-?\d+)", line)
                if m:
                    return m.group(1)
    except Exception:
        pass
    return None


def recent_lessons(limit=5):
    """Read last N lessons from ~/.claude/lessons.md."""
    lessons_path = Path.home() / ".claude" / "lessons.md"
    if not lessons_path.exists():
        return ""

    try:
        text = lessons_path.read_text(encoding="utf-8")
        lines = text.strip().split("\n")
        # Return last ~30 lines (approximately 5 lessons)
        if len(lines) > 30:
            return "\n".join(lines[-30:])
        return text
    except Exception:
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

    except Exception:
        # Never block session start
        pass


if __name__ == "__main__":
    main()
