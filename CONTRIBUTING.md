# Contributing

## 快速开始

```bash
git clone https://github.com/Sweetteabittersugar/agency-v2.git
cd agency-v2
pip install -e .
```

## 开发

- Python ≥ 3.8，零额外依赖
- 代码风格：PEP 8，4 空格缩进
- 改代码后跑 `python -m py_compile` 检查所有 .py 文件
- 改 stop.py 后跑 `python -m agency.hooks.stop` 手动测试（需要 stdin 输入 mock 数据）

## 提 PR

1. Fork → Branch → PR
2. PR 描述写清楚：做了什么、为什么、怎么测
3. 确保 `python -m py_compile` 全部通过

## 添加新 Agent

1. 在 `agents/` 下创建 `<name>.md`
2. 在 `AGENTS.md` 路由表添加一行
3. 在 `docs/agents.md` 添加一行

## 添加新 Skill

1. 在 `skills/` 下创建 `<name>.md`
2. 在 `docs/skills.md` 添加一行

## 添加新模型定价

编辑 `agency/cost.py` 中的 `PRICING_CNY_PER_M` 字典。同步更新 `agency/hooks/stop.py` 中的内联定价。
