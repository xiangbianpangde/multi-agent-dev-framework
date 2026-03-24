#!/usr/bin/env python3
"""
多Agent项目核心模块使用示例

演示：
- 任务调度
- 状态机
- 消息总线
- 记忆管理
"""

import asyncio
import sys
from pathlib import Path

# 添加模板路径
sys.path.insert(0, str(Path(__file__).parent / "templates"))

from core import (
    TaskDispatcher, Task, TaskPriority,
    StateMachine, TaskState,
    MessageBus, Message, MessageType, MessageBuilder,
    MemoryManager, MemoryDuration
)


def example_dispatcher():
    """任务调度器示例"""
    print("\n" + "=" * 60)
    print("任务调度器示例")
    print("=" * 60)
    
    # 创建调度器
    dispatcher = TaskDispatcher(max_concurrent=3)
    
    # 注册回调
    def on_task_created(task: Task):
        print(f"  [事件] 任务创建: {task.name}")
    
    dispatcher.on("on_task_created", on_task_created)
    
    # 创建任务
    task1 = dispatcher.create_task("分析用户需求", "分析用户提交的需求文档", TaskPriority.HIGH)
    task2 = dispatcher.create_task("设计系统架构", "设计系统整体架构", TaskPriority.NORMAL)
    task3 = dispatcher.create_task("编写单元测试", "为核心模块编写测试", TaskPriority.LOW)
    
    # 调度任务
    print("\n调度任务...")
    assigned = dispatcher.dispatch()
    print(f"  已分配任务数: {assigned}")
    
    # 获取统计
    stats = dispatcher.get_stats()
    print(f"\n统计信息:")
    print(f"  总任务数: {stats['total_tasks']}")
    print(f"  待处理: {stats['pending']}")
    print(f"  执行中: {stats['running']}")


def example_state_machine():
    """状态机示例"""
    print("\n" + "=" * 60)
    print("状态机示例")
    print("=" * 60)
    
    # 创建状态机
    sm = StateMachine()
    print(f"初始状态: {sm.current_state.value}")
    print(f"状态描述: {sm.get_state_description()}")
    
    # 执行状态转换
    print("\n执行状态转换:")
    
    sm.transition(TaskState.PLANNING, "开始规划")
    print(f"  -> {sm.current_state.value}")
    
    sm.transition(TaskState.REVIEW, "提交审核")
    print(f"  -> {sm.current_state.value}")
    
    sm.transition(TaskState.DISPATCHED, "审核通过")
    print(f"  -> {sm.current_state.value}")
    
    sm.transition(TaskState.EXECUTING, "开始执行")
    print(f"  -> {sm.current_state.value}")
    
    sm.transition(TaskState.CHECKING, "执行完成")
    print(f"  -> {sm.current_state.value}")
    
    sm.transition(TaskState.ACCEPTED, "验收通过")
    print(f"  -> {sm.current_state.value}")
    
    sm.transition(TaskState.DONE, "任务完成")
    print(f"  -> {sm.current_state.value}")
    
    # 查看历史
    print(f"\n状态历史:")
    for record in sm.get_history():
        print(f"  {record['state']}: {record['reason']}")
    
    print(f"\n是否为终态: {sm.is_terminal()}")


async def example_message_bus():
    """消息总线示例"""
    print("\n" + "=" * 60)
    print("消息总线示例")
    print("=" * 60)
    
    # 创建消息总线
    bus = MessageBus()
    
    # 注册Agent
    async def zhongshu_callback(message: Message):
        print(f"  [中书省] 收到消息: {message.content}")
    
    async def menxia_callback(message: Message):
        print(f"  [门下省] 收到消息: {message.content}")
    
    bus.register("zhongshu", zhongshu_callback)
    bus.register("menxia", menxia_callback)
    
    # 设置权限
    bus.set_permissions("zhongshu", ["menxia"])
    bus.set_permissions("menxia", ["zhongshu"])
    
    # 发送消息
    print("\n发送消息:")
    
    # 使用构建器创建消息
    msg = (MessageBuilder()
           .from_agent("zhongshu")
           .to_agent("menxia")
           .with_type(MessageType.TASK)
           .with_content({"task": "审核方案", "priority": "high"})
           .build())
    
    await bus.send(msg)
    
    # 处理消息
    await bus._route_message(msg)
    
    # 获取统计
    stats = bus.get_stats()
    print(f"\n消息总线统计:")
    print(f"  已注册Agent: {stats['registered_agents']}")


def example_memory():
    """记忆管理示例"""
    print("\n" + "=" * 60)
    print("记忆管理示例")
    print("=" * 60)
    
    # 创建记忆管理器
    memory = MemoryManager(storage_path="./example_memory")
    
    # 短期记忆
    print("\n短期记忆:")
    memory.remember("current_task", "分析用户需求", MemoryDuration.SHORT)
    value = memory.recall("current_task")
    print(f"  存入: '分析用户需求'")
    print(f"  取出: '{value}'")
    
    # 中期记忆
    print("\n中期记忆:")
    memory.remember("project_config", {
        "name": "多Agent项目",
        "version": "1.0.0"
    }, MemoryDuration.MEDIUM, {"category": "config"})
    
    config = memory.recall("project_config")
    print(f"  项目配置: {config}")
    
    # 搜索
    print("\n搜索记忆:")
    results = memory.search("项目", MemoryDuration.MEDIUM)
    print(f"  搜索 '项目' 结果数: {len(results)}")
    
    # 统计
    stats = memory.get_stats()
    print(f"\n记忆统计:")
    print(f"  短期记忆使用: {stats['short_term']['usage_percent']:.1f}%")
    print(f"  中期记忆条目: {stats['medium_term']['total_keys']}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("多Agent项目核心模块使用示例")
    print("=" * 60)
    
    # 运行示例
    example_dispatcher()
    example_state_machine()
    asyncio.run(example_message_bus())
    example_memory()
    
    print("\n" + "=" * 60)
    print("示例运行完成")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()