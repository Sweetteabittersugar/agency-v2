# Security Policy

## 报告漏洞

发现安全漏洞请私密报告，不要开公开 issue。

邮件：在 GitHub 个人资料中查看联系方式。

## 支持版本

| 版本 | 支持 |
|------|------|
| 2.0.x | ✅ 活跃支持 |

## 安全设计

- Agency v2 所有数据存储在本地（`~/.agency/agency.db`），不联网
- Stop hook 只读会话转录，不修改任何系统文件
- 定价数据硬编码在源码中，不依赖外部 API
- 无远程代码执行路径
- 错误日志只写本地文件，不会发送到外部

## 依赖

零第三方 Python 依赖。只使用 Python 标准库（sqlite3、json、os、pathlib、subprocess）。
