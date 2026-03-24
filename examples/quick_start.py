#!/usr/bin/env python3
"""
快速入门示例

演示如何使用框架创建一个简单的多Agent项目
"""
import sys
from pathlib import Path

# 添加工具路径
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from generators.project_generator import ProjectGenerator
from generators.agent_generator import AgentGenerator
from generators.skill_generator import SkillGenerator


def main():
    """快速入门示例"""
    print("=" * 60)
    print("多Agent项目开发框架 - 快速入门")
    print("=" * 60)
    
    # 1. 创建项目
    print("\n1. 创建项目...")
    project_gen = ProjectGenerator("my-first-project", output_dir="./output")
    result = project_gen.generate(
        description="我的第一个多Agent项目",
        author="开发者"
    )
    print(f"   项目创建于: {result['project_dir']}")
    print(f"   创建文件数: {len(result['created_files'])}")
    
    # 2. 创建自定义Agent
    print("\n2. 创建自定义Agent...")
    agent_gen = AgentGenerator(output_dir="./output/my-first-project")
    agent_result = agent_gen.create_agent(
        agent_id="custom_agent",
        name="自定义Agent",
        role="execution",
        description="执行特定任务的Agent"
    )
    print(f"   Agent创建于: {agent_result['soul_path']}")
    
    # 3. 创建技能
    print("\n3. 创建技能...")
    skill_gen = SkillGenerator(output_dir="./output/my-first-project")
    skill_result = skill_gen.create_skill(
        name="data_processing",
        description="数据处理技能"
    )
    print(f"   Skill创建于: {skill_result['skill_dir']}")
    
    print("\n" + "=" * 60)
    print("快速入门完成！")
    print("查看 output/my-first-project 目录了解生成的内容")
    print("=" * 60)


if __name__ == "__main__":
    main()