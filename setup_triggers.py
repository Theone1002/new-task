#!/usr/bin/env python3
"""
Setup common remote triggers for Claude Code desktop-mobile integration.

This script helps configure remote triggers that allow you to
control your local Claude Code session from your mobile device
(via claude.ai/code web interface).

Usage:
    python3 setup_triggers.py [--list | --create | --run <trigger_id>]
"""

import json
import subprocess
import sys
import os


# Common trigger templates for desktop-mobile integration
TRIGGER_TEMPLATES = {
    "run-tests": {
        "name": "Run Tests",
        "description": "从手机端触发本地测试运行",
        "command": "npm test",  # Customize per project
    },
    "git-status": {
        "name": "Git Status",
        "description": "从手机端查看本地 Git 状态",
        "command": "git status && git log --oneline -5",
    },
    "build": {
        "name": "Build Project",
        "description": "从手机端触发本地项目构建",
        "command": "npm run build",  # Customize per project
    },
    "lint": {
        "name": "Lint Code",
        "description": "从手机端触发代码检查",
        "command": "npm run lint",  # Customize per project
    },
    "deploy-staging": {
        "name": "Deploy to Staging",
        "description": "从手机端触发部署到测试环境",
        "command": "echo 'Deploy command here'",  # Customize per project
    },
}


def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("  Claude Code 桌面端-移动端串联设置工具")
    print("  Desktop-Mobile Integration Setup")
    print("=" * 60)
    print()


def list_templates():
    """List available trigger templates."""
    print("可用的触发器模板 / Available trigger templates:")
    print("-" * 50)
    for key, template in TRIGGER_TEMPLATES.items():
        print(f"  {key}:")
        print(f"    名称: {template['name']}")
        print(f"    描述: {template['description']}")
        print(f"    命令: {template['command']}")
        print()


def detect_project_type():
    """Detect the project type to suggest appropriate triggers."""
    project_info = {
        "type": "unknown",
        "test_cmd": None,
        "build_cmd": None,
        "lint_cmd": None,
    }

    # Check for package.json (Node.js project)
    if os.path.exists("package.json"):
        project_info["type"] = "nodejs"
        try:
            with open("package.json") as f:
                pkg = json.load(f)
                scripts = pkg.get("scripts", {})
                if "test" in scripts:
                    project_info["test_cmd"] = "npm test"
                if "build" in scripts:
                    project_info["build_cmd"] = "npm run build"
                if "lint" in scripts:
                    project_info["lint_cmd"] = "npm run lint"
        except (json.JSONDecodeError, IOError):
            pass

    # Check for pyproject.toml or setup.py (Python project)
    elif os.path.exists("pyproject.toml") or os.path.exists("setup.py"):
        project_info["type"] = "python"
        project_info["test_cmd"] = "pytest"
        project_info["lint_cmd"] = "ruff check ."

    # Check for Cargo.toml (Rust project)
    elif os.path.exists("Cargo.toml"):
        project_info["type"] = "rust"
        project_info["test_cmd"] = "cargo test"
        project_info["build_cmd"] = "cargo build"
        project_info["lint_cmd"] = "cargo clippy"

    # Check for go.mod (Go project)
    elif os.path.exists("go.mod"):
        project_info["type"] = "go"
        project_info["test_cmd"] = "go test ./..."
        project_info["build_cmd"] = "go build ./..."
        project_info["lint_cmd"] = "golangci-lint run"

    return project_info


def print_setup_instructions():
    """Print instructions for setting up desktop-mobile integration."""
    print_banner()

    print("📱 如何从手机端控制电脑端 Claude Code:")
    print()
    print("步骤 1: 在电脑端启动 Claude Code CLI")
    print("  $ claude")
    print()
    print("步骤 2: 在手机端打开 claude.ai/code")
    print("  连接到同一个项目仓库")
    print()
    print("步骤 3: 使用 Remote Triggers 从手机端触发电脑端操作")
    print("  在手机端的 Claude Code 会话中，可以创建和运行触发器")
    print()

    # Detect project type
    project = detect_project_type()
    if project["type"] != "unknown":
        print(f"检测到项目类型: {project['type']}")
        print("推荐的触发器配置:")
        if project["test_cmd"]:
            print(f"  测试: {project['test_cmd']}")
        if project["build_cmd"]:
            print(f"  构建: {project['build_cmd']}")
        if project["lint_cmd"]:
            print(f"  检查: {project['lint_cmd']}")
        print()

    list_templates()

    print("提示: 你可以在 Claude Code 会话中直接管理触发器，")
    print("或修改此脚本中的 TRIGGER_TEMPLATES 来自定义触发器。")


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--list":
            list_templates()
        elif sys.argv[1] == "--detect":
            project = detect_project_type()
            print(json.dumps(project, indent=2, ensure_ascii=False))
        else:
            print_setup_instructions()
    else:
        print_setup_instructions()


if __name__ == "__main__":
    main()
