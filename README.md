# Agency v2

> Claude Code 个性化增强包——内置工作流、Agent 库、Skill 库、费用追踪。
> 纯对话，零 GUI。一条命令安装，所有功能通过对话触发。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/Sweetteabittersugar/agency-v2/releases)
[![Zero Dependencies](https://img.shields.io/badge/deps-0-brightgreen.svg)]()

## 是什么

Agency v2 = Claude Code + 你的个性化增强包。安装后 Claude Code 自动拥有：费用追踪、Agent 路由、Skill 库、工作流引擎、执行记录、使用说明书。

**对比**：

| | 裸 Claude Code | 装 Agency v2 |
|---|---|---|
| 费用追踪 | ❌ 不知道花了多少 | ✅ `/cost` 今日/本周/本月 |
| Agent 路由 | ❌ 手动派发 | ✅ 关键词自动匹配 |
| Skill 库 | ❌ 自己写 prompt | ✅ 7 个预设流程 |
| 工作流 | ❌ 无章法 | ✅ 9 阶段全栈 + 模型分工 |
| 说明书 | ❌ 网上搜 | ✅ `/help` 内置 |

## 快速开始

```bash
# 前提：Claude Code + CC Switch + DeepSeek API Key 已配置
git clone https://github.com/Sweetteabittersugar/agency-v2.git
cd agency-v2 && bash scripts/install.sh
```

安装后在 Claude Code 里：

```
/cost       → 今日/本周/本月费用
/history    → Agent 执行记录
/help       → 查看所有功能
@coder 帮我写个函数
```

一条命令完成：pip 安装 + Hook 注册 + 数据库初始化。

## 架构

```
Agency v2 = Claude Code + 三层增强

指令层（静态）: CLAUDE.md + agents/ + skills/ + docs/
脚本层（按需）: workflow.sh + cost.py + history.py
服务层（静默）: hooks/stop.py → ~/.agency/agency.db
```

## 包含什么

| 模块 | 内容 | 数量 |
|------|------|------|
| Agent 库 | architect / coder / reviewer / debugger / explorer / test-writer / devops / doc-writer / security-reviewer | 9 |
| Skill 库 | review / debug / cost / history / help / workflow / agent | 7 |
| 文档 | quickstart / commands / agents / skills / workflow / faq | 6 |
| 工作流 | 9 阶段全栈开发（灵感 → 部署），双模型分工 | 1 |
| 后端 | cost.py / history.py / db.py / stop hook / install.sh | 5 |

## 依赖

- Claude Code（运行时）
- CC Switch（模型切换）
- Python ≥ 3.8（费用追踪）
- DeepSeek V4 Pro + MiMo V2.5 Pro API Key

Agency 本身**零第三方 Python 依赖**——只用了 sqlite3、json、os、pathlib、subprocess。

## 卸载

```bash
# 1. 删 hook：编辑 ~/.claude/settings.json，删掉含 "agency.hooks.stop" 的条目
# 2. 删数据：
rm ~/.agency/agency.db
# 3. 删包：
pip uninstall agency-v2
```

## License

MIT © 2026
