"""
知识图谱模块

功能：
- 项目、Agent、技能、决策、模式的知识管理
- 知识关联和检索
- 智能推荐
"""

__version__ = "1.0.0"

from .graph import KnowledgeGraph
from .nodes import (
    ProjectNode, AgentNode, SkillNode, DecisionNode,
    PatternNode, ProblemNode, KnowledgeNode
)
from .relations import RelationType

__all__ = [
    "KnowledgeGraph",
    "ProjectNode",
    "AgentNode", 
    "SkillNode",
    "DecisionNode",
    "PatternNode",
    "ProblemNode",
    "KnowledgeNode",
    "RelationType",
]