#!/usr/bin/env python3
"""
多Agent项目开发工具集 - 统一CLI入口

功能：
- 项目生成
- Agent生成
- Skill生成
- 配置管理

使用：
    python cli.py project --name "项目名称"
    python cli.py agent --id "agent_id" --name "显示名称" --role "decision"
    python cli.py skill --name "skill_name" --description "功能描述"
"""

import argparse
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from generators.project_generator import ProjectGenerator
from generators.agent_generator import AgentGenerator
from generators.skill_generator import SkillGenerator


def cmd_project(args):
    """创建项目"""
    generator = ProjectGenerator(args.name, args.output)
    result = generator.generate(args.description, args.author)
    
    print(f"\n✅ 项目创建成功！")
    print(f"📁 项目目录: {result['project_dir']}")
    print(f"📄 创建文件: {len(result['created_files'])} 个")
    print(f"📂 创建目录: {len(result['created_dirs'])} 个")
    
    if args.init_git:
        import subprocess
        print("\n🔧 初始化Git仓库...")
        subprocess.run(["git", "init"], cwd=result['project_dir'])
        print("✅ Git仓库初始化完成")


def cmd_agent(args):
    """创建Agent"""
    import json
    
    generator = AgentGenerator(args.output)
    result = generator.create_agent(
        agent_id=args.id,
        name=args.name,
        role=args.role,
        description=args.description,
        model_primary=args.model_primary,
        model_fallback=args.model_fallback
    )
    
    print(f"\n✅ Agent创建成功！")
    print(f"📄 SOUL.md: {result['soul_path']}")
    print(f"\n📝 配置片段:")
    print(json.dumps(result['config'], indent=2, ensure_ascii=False))


def cmd_skill(args):
    """创建Skill"""
    import json
    
    generator = SkillGenerator(args.output)
    
    params = json.loads(args.params) if args.params else None
    
    result = generator.create_skill(
        name=args.name,
        description=args.description,
        params=params
    )
    
    print(f"\n✅ Skill创建成功！")
    print(f"📁 Skill目录: {result['skill_dir']}")
    print(f"📄 SKILL.md: {result['skill_md']}")
    print(f"📄 main.py: {result['main_py']}")
    print(f"📄 test: {result['test_py']}")


def cmd_list(args):
    """列出可用的模板和资源"""
    print("=" * 60)
    print("多Agent项目开发工具集")
    print("=" * 60)
    
    print("\n📋 支持的Agent角色:")
    print("  - decision: 决策调度层")
    print("  - audit: 监察审核层")
    print("  - execution: 执行层")
    
    print("\n📦 预置Agent模板:")
    agents = ["zhongshu", "menxia", "shangshu", "hubu", "libu", "bingbu", "xingbu", "gongbu"]
    for agent in agents:
        print(f"  - {agent}")
    
    print("\n🔧 推荐模型:")
    print("  - GPT-4: 架构设计、复杂推理")
    print("  - Claude-3: 安全审计、代码审查")
    print("  - Gemini Pro: 任务调度、通用场景")
    print("  - Qwen: 代码开发")
    print("  - Kimi/GLM-4: 文档编写、中文场景")
    
    print("\n📚 工程知识库位置:")
    print("  docs/engineering-knowledge-base/")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="多Agent项目开发工具集",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建新项目
  python cli.py project --name my-project --description "我的项目" --init-git

  # 创建新Agent
  python cli.py agent --id my_agent --name "我的Agent" --role execution

  # 创建新Skill
  python cli.py skill --name code_review --description "代码审查技能"

  # 查看帮助
  python cli.py list
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # project 子命令
    project_parser = subparsers.add_parser("project", help="创建项目")
    project_parser.add_argument("--name", required=True, help="项目名称")
    project_parser.add_argument("--description", default="", help="项目描述")
    project_parser.add_argument("--author", default="", help="作者")
    project_parser.add_argument("--output", default=".", help="输出目录")
    project_parser.add_argument("--init-git", action="store_true", help="初始化Git仓库")
    
    # agent 子命令
    agent_parser = subparsers.add_parser("agent", help="创建Agent")
    agent_parser.add_argument("--id", required=True, help="Agent ID")
    agent_parser.add_argument("--name", required=True, help="Agent显示名称")
    agent_parser.add_argument("--role", required=True, 
                              choices=["decision", "audit", "execution"], 
                              help="Agent角色")
    agent_parser.add_argument("--description", default="", help="Agent描述")
    agent_parser.add_argument("--model-primary", default="gpt-4", help="主模型")
    agent_parser.add_argument("--model-fallback", default="claude-3", help="备用模型")
    agent_parser.add_argument("--output", default=".", help="输出目录")
    
    # skill 子命令
    skill_parser = subparsers.add_parser("skill", help="创建Skill")
    skill_parser.add_argument("--name", required=True, help="技能名称")
    skill_parser.add_argument("--description", required=True, help="功能描述")
    skill_parser.add_argument("--params", help="参数JSON")
    skill_parser.add_argument("--output", default=".", help="输出目录")
    
    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出可用资源")
    
    args = parser.parse_args()
    
    if args.command == "project":
        cmd_project(args)
    elif args.command == "agent":
        cmd_agent(args)
    elif args.command == "skill":
        cmd_skill(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()