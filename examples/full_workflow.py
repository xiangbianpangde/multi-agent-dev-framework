#!/usr/bin/env python3
"""
完整工作流示例

演示从需求到交付的完整开发流程
"""
import sys
from pathlib import Path
from datetime import datetime

# 添加核心模块路径
sys.path.insert(0, str(Path(__file__).parent.parent / "tools" / "templates"))

from core.dispatcher import TaskDispatcher, Task, TaskPriority
from core.state_machine import StateMachine, TaskState
from core.memory import MemoryManager, MemoryDuration


class MultiAgentWorkflow:
    """多Agent工作流示例"""
    
    def __init__(self):
        self.dispatcher = TaskDispatcher(max_concurrent=3)
        self.state_machine = StateMachine()
        self.memory = MemoryManager(storage_path="./example_memory")
    
    def run(self):
        """运行完整工作流"""
        print("\n" + "=" * 60)
        print("多Agent项目开发工作流示例")
        print("=" * 60)
        
        # Step 1: 需求讨论
        self.step1_requirements()
        
        # Step 2: 规划
        self.step2_planning()
        
        # Step 3: 审核
        self.step3_review()
        
        # Step 4: 执行
        self.step4_execution()
        
        # Step 5: 验收
        self.step5_acceptance()
        
        # Step 6: 交付
        self.step6_delivery()
    
    def step1_requirements(self):
        """需求讨论"""
        print("\n[Step 1] 需求讨论")
        
        # 记录需求到记忆
        requirements = {
            "project": "用户认证系统",
            "features": ["登录", "注册", "密码找回"],
            "tech_stack": ["FastAPI", "PostgreSQL", "Redis"]
        }
        
        self.memory.remember(
            "requirements",
            requirements,
            MemoryDuration.MEDIUM
        )
        
        # 创建任务
        task = self.dispatcher.create_task(
            name="设计用户认证系统",
            description="设计完整的用户认证系统架构",
            priority=TaskPriority.HIGH
        )
        
        print(f"  需求已记录: {requirements['project']}")
        print(f"  任务已创建: {task.id}")
        
        # 状态转换
        self.state_machine.transition(TaskState.PLANNING, "需求确认，开始规划")
    
    def step2_planning(self):
        """规划阶段"""
        print("\n[Step 2] 规划")
        
        # 回忆需求
        requirements = self.memory.recall("requirements")
        print(f"  回顾需求: {requirements['project']}")
        
        # 模拟规划
        plan = {
            "modules": ["认证模块", "用户模块", "通知模块"],
            "tasks": [
                "设计API接口",
                "实现认证逻辑",
                "编写测试用例"
            ]
        }
        
        self.memory.remember("plan", plan, MemoryDuration.MEDIUM)
        
        print(f"  规划完成: {len(plan['modules'])} 个模块")
        
        # 状态转换
        self.state_machine.transition(TaskState.REVIEW, "规划完成，提交审核")
    
    def step3_review(self):
        """审核阶段"""
        print("\n[Step 3] 审核")
        
        # 获取规划
        plan = self.memory.recall("plan")
        
        # 模拟审核
        review_result = {
            "status": "approved",
            "comments": ["架构设计合理", "模块划分清晰"]
        }
        
        print(f"  审核结果: {review_result['status']}")
        
        # 状态转换
        if review_result["status"] == "approved":
            self.state_machine.transition(TaskState.DISPATCHED, "审核通过")
        else:
            self.state_machine.transition(TaskState.REJECTED, "审核不通过")
    
    def step4_execution(self):
        """执行阶段"""
        print("\n[Step 4] 执行")
        
        # 调度任务
        assigned = self.dispatcher.dispatch()
        print(f"  已分配任务: {assigned} 个")
        
        # 获取统计
        stats = self.dispatcher.get_stats()
        print(f"  任务状态: 待处理 {stats['pending']}, 执行中 {stats['running']}")
        
        # 状态转换
        self.state_machine.transition(TaskState.EXECUTING, "开始执行")
    
    def step5_acceptance(self):
        """验收阶段"""
        print("\n[Step 5] 验收")
        
        # 模拟验收
        acceptance_result = {
            "status": "passed",
            "tests_passed": 10,
            "tests_failed": 0
        }
        
        print(f"  验收结果: {acceptance_result['status']}")
        print(f"  测试通过: {acceptance_result['tests_passed']}")
        
        # 状态转换
        self.state_machine.transition(TaskState.CHECKING, "执行完成，开始验收")
        self.state_machine.transition(TaskState.ACCEPTED, "验收通过")
    
    def step6_delivery(self):
        """交付阶段"""
        print("\n[Step 6] 交付")
        
        # 获取历史
        history = self.state_machine.get_history()
        print(f"  状态历史: {len(history)} 次转换")
        
        # 最终状态
        self.state_machine.transition(TaskState.DONE, "项目完成")
        print(f"  最终状态: {self.state_machine.current_state.value}")
        
        # 记忆统计
        stats = self.memory.get_stats()
        print(f"  记忆条目: {stats['medium_term']['total_keys']}")
        
        print("\n" + "=" * 60)
        print("工作流完成！")
        print("=" * 60)


def main():
    """运行示例"""
    workflow = MultiAgentWorkflow()
    workflow.run()


if __name__ == "__main__":
    main()