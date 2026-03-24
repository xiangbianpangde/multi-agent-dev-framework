"""
核心模块 - 多Agent项目核心实现

包含：
- 调度器
- 状态机
- 消息总线
- 记忆管理
- 知识图谱
"""

__version__ = "1.0.0"

from .dispatcher import TaskDispatcher
from .state_machine import StateMachine, TaskState
from .message_bus import MessageBus, Message, MessageType
from .memory import MemoryManager

# 知识图谱模块（可选依赖）
try:
    from .knowledge_graph import (
        KnowledgeGraph,
        ProjectNode, AgentNode, SkillNode,
        DecisionNode, PatternNode, ProblemNode, KnowledgeNode,
        RelationType
    )
    _knowledge_graph_available = True
except ImportError:
    _knowledge_graph_available = False

__all__ = [
    "TaskDispatcher",
    "StateMachine", 
    "TaskState",
    "MessageBus",
    "Message",
    "MessageType",
    "MemoryManager",
]

# 知识图谱可选导出
if _knowledge_graph_available:
    __all__.extend([
        "KnowledgeGraph",
        "ProjectNode",
        "AgentNode",
        "SkillNode", 
        "DecisionNode",
        "PatternNode",
        "ProblemNode",
        "KnowledgeNode",
        "RelationType",
    ])