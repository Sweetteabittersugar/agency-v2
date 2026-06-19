# Changelog

## [2.0.0] — 2026-06-19

### Added
- 三层架构：指令层（agents/skills/docs）+ 脚本层（cost/history）+ 服务层（stop hook）
- 9 个 Agent 定义（architect/coder/reviewer/debugger/explorer/test-writer/devops/doc-writer/security-reviewer）
- 7 个 Skill 定义（review/debug/cost/history/help/workflow/agent）
- `/cost` 命令：今日/本周/本月费用查询
- `/history` 命令：Agent 执行记录查询
- `/help` 命令：使用说明书
- Stop hook：会话结束自动解析 JSONL 转录，计算费用写入 SQLite
- DeepSeek V4 Pro + MiMo V2.5 Pro 双模型定价支持
- 一键安装脚本 `scripts/install.sh`
- 6 份使用文档（quickstart/commands/agents/skills/workflow/faq）
- 9 阶段全栈开发工作流 + 模型分工

### Design Decisions
- 纯对话，零 GUI
- 成本追踪自己写而不依赖第三方（cc-ledger 等工具与 Python + Windows 技术栈不匹配）
- 不设 HTTP Server（纯对话模式下 slash command + CLI 脚本即可）
- SQLite 单文件存储（~/.agency/agency.db）
- 零第三方 Python 依赖
