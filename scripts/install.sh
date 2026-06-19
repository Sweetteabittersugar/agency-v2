#!/bin/bash
# install.sh — Agency v2 one-command install
# Usage: bash install.sh
#
# What it does:
#   1. pip install the agency package
#   2. Register Stop hook in ~/.claude/settings.json
#   3. Initialize database
#   4. Print success message

set -e

AGENCY_DIR="$HOME/.agency"
SETTINGS_FILE="$HOME/.claude/settings.json"

echo "═══ Agency v2 — Install ═══"
echo ""

# ── Step 1: pip install ──
echo "→ Installing agency package..."
pip install -e "$(dirname "$0")/.." 2>/dev/null || pip install "$(dirname "$0")/.."
echo "  ✓ agency package installed"

# ── Step 2: Register Stop hook ──
echo "→ Registering Stop hook..."

if [ -f "$SETTINGS_FILE" ]; then
    # Check if hook already registered (checks both simple and nested formats)
    if python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    s = json.load(f)
stop_hooks = s.get('hooks', {}).get('Stop', [])
found = False
for h in stop_hooks:
    # Simple format: {'command': '...'}
    if 'agency.hooks.stop' in h.get('command', ''):
        found = True
    # Nested format: {'hooks': [{'command': '...'}]}
    for sub in h.get('hooks', []):
        if 'agency.hooks.stop' in sub.get('command', ''):
            found = True
exit(1 if found else 0)
" 2>/dev/null; then
        # Hook not yet registered — add it
        python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    s = json.load(f)
hooks = s.setdefault('hooks', {})
stop_hooks = hooks.setdefault('Stop', [])
stop_hooks.append({'command': 'python -m agency.hooks.stop'})
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(s, f, indent=2)
"
        echo "  ✓ Stop hook registered"
    else
        echo "  • Stop hook already registered (skipping)"
    fi
else
    # Create new settings.json
    mkdir -p "\$(dirname \"$SETTINGS_FILE\")"
    python3 -c "
import json
s = {'hooks': {'Stop': [{'command': 'python -m agency.hooks.stop'}]}}
with open('$SETTINGS_FILE', 'w') as f:
    json.dump(s, f, indent=2)
"
    echo "  ✓ Created $SETTINGS_FILE with Stop hook"
fi

# ── Step 3: Initialize database ──
echo "→ Initializing database..."
python3 -c "
from agency.db import get_db
conn = get_db()
conn.close()
"
echo "  ✓ Database ready at $AGENCY_DIR/agency.db"

# ── Step 4: Add Agency reference to global CLAUDE.md ──
GLOBAL_CLAUDE="$HOME/.claude/CLAUDE.md"
AGENCY_HINT="<!-- AGENCY-V2 --> Agency v2 已安装。可用命令: /cost(费用) /history(记录) /help(说明) @agent名(路由)。运行 python -m agency.check 诊断。"

if [ -f "$GLOBAL_CLAUDE" ]; then
    if ! grep -q "AGENCY-V2" "$GLOBAL_CLAUDE" 2>/dev/null; then
        echo "" >> "$GLOBAL_CLAUDE"
        echo "$AGENCY_HINT" >> "$GLOBAL_CLAUDE"
        echo "  ✓ Agency reference added to ~/.claude/CLAUDE.md"
    else
        echo "  • Already in ~/.claude/CLAUDE.md (skipping)"
    fi
else
    mkdir -p "$(dirname "$GLOBAL_CLAUDE")"
    echo "$AGENCY_HINT" > "$GLOBAL_CLAUDE"
    echo "  ✓ Created ~/.claude/CLAUDE.md"
fi

# ── Done ──
echo ""
echo "══════════════════════════════════════"
echo "  Agency v2 安装完成！"
echo "══════════════════════════════════════"
echo ""
echo "📦 你现在拥有的功能："
echo ""
echo "  费用追踪（自动，静默）："
echo "    /cost        → 今日/本周/本月费用"
echo ""
echo "  执行记录："
echo "    /history     → Agent 干了什么、花了多少"
echo ""
echo "  内置说明书："
echo "    /help        → 所有功能说明"
echo "    /help agents → Agent 列表"
echo "    /help skills → Skill 列表"
echo ""
echo "  Agent 路由："
echo "    @coder 帮我写个函数  → 自动派给编码 Agent"
echo "    @reviewer 审查这段代码 → 自动派给审查 Agent"
echo "    （共 9 个 Agent，描述任务自动匹配）"
echo ""
echo "⚙️  管理命令（终端里跑）："
echo "    python -m agency.check   → 环境诊断"
echo "    python -m agency.cost    → 费用查询"
echo "    python -m agency.history → 执行记录"
echo ""
echo "💡 下一步：在 Claude Code 里输入 /help 开始探索"
echo ""
echo "📁 数据: $AGENCY_DIR/"
echo "🔧 Hook: $SETTINGS_FILE"
