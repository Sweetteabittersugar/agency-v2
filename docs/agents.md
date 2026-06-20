# AGENTS.md — Agent 路由矩阵

> 任务关键词 → Agent 映射。Agency 自动匹配最合适的 Agent。

## 路由表

| 任务类型 | 关键词 | Agent | 说明 |
|---------|--------|-------|------|
| 架构设计 | 架构、设计、选型、重构方案 | `architect` | 只出方案不写代码 |
| 写代码 | 实现、写、改、新建、功能 | `coder` | 直接写代码，手术式修改 |
| 代码审查 | 审查、review、检查代码 | `reviewer` | 四维度审查 |
| 调试 | bug、报错、调试、排查、修 | `debugger` | 六步结构化调试 |
| 搜索代码 | 查找、搜索、在哪、有哪些 | `explorer` | 代码库搜索，只读 |
| 测试 | 测试、test、用例、覆盖 | `test-writer` | 生成单元/集成测试 |
| DevOps | 部署、CI、Docker、环境 | `devops` | 基础设施 |
| 文档 | 文档、README、注释、CHANGELOG | `doc-writer` | 文档编写更新 |
| 安全 | 安全、漏洞、审计、注入 | `security-reviewer` | 安全审计 |

## 路由规则

1. 用户消息匹配关键词 → 派发对应 Agent
2. 无匹配 → 默认 Claude Code 直接处理
3. 手动 `@agent名` 指定 → 跳过路由，直接派发
4. 一个任务跨多领域 → 派给匹配度最高的 Agent

## Agent 定义

所有 Agent 定义文件在 `agents/` 目录：
```
agents/
├── architect.md
├── coder.md
├── reviewer.md
├── debugger.md
├── explorer.md
├── test-writer.md
├── devops.md
├── doc-writer.md
└── security-reviewer.md
```
