# CLAUDE.md — Agency v2

> Claude Code 个性化增强包。内置工作流、Agent 库、Skill 库、费用追踪。
> 纯对话交互，所有功能通过 `/` 命令或自然语言触发。

## 核心命令

| 命令 | 作用 |
|------|------|
| `/cost` | 查看今日/本周/本月费用 |
| `/history` | 查看 Agent 执行记录 |
| `/help [topic]` | 查看使用说明 |

## Agent 路由

任务自动匹配 Agent（见 `AGENTS.md`）。也可手动指定：
- `@architect <任务>` — 架构设计
- `@coder <任务>` — 写代码
- `@reviewer <任务>` — 代码审查
- `@debugger <任务>` — 调试
- `@explorer <任务>` — 代码搜索

## 工作流

9 阶段全栈开发流程（见 `docs/workflow.md`）：
灵感 → 需求 → Spec → 技术选型 → API设计 → 后端 → 前端 → 联调 → 部署

切模型提醒：`source scripts/workflow.sh <stage>`

## 费用追踪

每次会话结束自动记录费用到 `~/.agency/agency.db`。
`/cost` 命令查询。停止追踪：删掉 `~/.claude/settings.json` 中的 Stop hook。

## 文件布局

```
agency-v2/
├── CLAUDE.md           # 你正在读的文件
├── AGENTS.md           # Agent 路由矩阵
├── agents/             # Agent 定义（.md）
├── skills/             # Skill 定义
├── docs/               # 使用说明书
├── scripts/            # 脚本（workflow.sh, install.sh）
└── agency/             # Python 包（cost, history, db, hooks）
```
