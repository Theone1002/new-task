# Claude Code 桌面端与移动端串联指南

## 概述

Claude Code 支持在**手机端**（通过 GitHub / claude.ai/code 网页）和**电脑端**（本地 CLI）之间进行协作。核心机制是 **Remote Triggers（远程触发器）**。

## 工作原理

```
┌─────────────┐    Remote Trigger     ┌─────────────────┐
│  手机端       │  ──────────────────►  │   电脑端（本地）   │
│  claude.ai   │                       │   Claude Code CLI │
│  /code 网页   │  ◄──────────────────  │   本地文件系统     │
│  GitHub      │    结果返回            │   本地开发环境     │
└─────────────┘                       └─────────────────┘
```

### 什么是 Remote Triggers?

Remote Triggers 允许你：
- 从手机端网页会话（claude.ai/code）**远程触发**电脑端本地的 Claude Code 执行任务
- 电脑端 Claude Code 在本地运行命令、读写文件、执行测试等
- 结果自动返回到手机端

## 使用步骤

### 1. 电脑端准备

在电脑端安装并启动 Claude Code CLI：

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 在你的项目目录中启动
cd /your/project
claude
```

### 2. 创建远程触发器

你可以在电脑端 Claude Code 中创建触发器，然后从手机端调用：

```bash
# 在 Claude Code 中使用 /triggers 命令管理触发器
```

### 3. 手机端使用

在手机上打开 claude.ai/code，连接到同一个项目，即可触发电脑端的操作。

## 常见使用场景

| 场景 | 手机端操作 | 电脑端执行 |
|------|-----------|-----------|
| 运行测试 | 触发 "run tests" | 本地执行 pytest/npm test |
| 部署 | 触发 "deploy" | 本地执行部署脚本 |
| 代码检查 | 触发 "lint" | 本地运行 linter |
| 构建项目 | 触发 "build" | 本地执行构建命令 |
| Git 操作 | 触发 "git sync" | 本地执行 git pull/push |

## 示例：设置常用触发器

参见 `setup_triggers.py` 脚本，可以快速配置常用的远程触发器。

## 限制

- 手机端（claude.ai/code 网页版）不能直接访问本地文件系统
- 需要电脑端 Claude Code 保持运行状态
- Remote Triggers 需要网络连接

## 总结

虽然手机端不能直接操作本地文件，但通过 Remote Triggers 机制，你可以从手机端**远程控制**电脑端的 Claude Code，实现真正的桌面-移动端协作。
