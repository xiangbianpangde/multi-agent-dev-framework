"""
核心模块 - 多Agent项目核心实现

包含：
- 调度器
- 状态机
- 消息总线
- 记忆管理
"""

__version__ = "1.0.0"

from .dispatcher import TaskDispatcher
from .state_machine import StateMachine, TaskState
from .message_bus import MessageBus, Message, MessageType
from .memory import MemoryManager

__all__ = [
    "TaskDispatcher",
    "StateMachine", 
    "TaskState",
    "MessageBus",
    "Message",
    "MessageType",
    "MemoryManager",
]