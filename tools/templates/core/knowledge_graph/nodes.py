"""
知识图谱节点定义

定义知识图谱中所有节点类型及其属性
"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class NodeType(Enum):
    """节点类型"""
    PROJECT = "Project"
    AGENT = "Agent"
    SKILL = "Skill"
    DECISION = "Decision"
    PATTERN = "Pattern"
    PROBLEM = "Problem"
    KNOWLEDGE = "Knowledge"


@dataclass
class BaseNode:
    """节点基类"""
    id: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def get_labels(self) -> List[str]:
        """获取Neo4j标签"""
        return [self.__class__.__name__]


@dataclass
class ProjectNode(BaseNode):
    """项目节点"""
    description: str = ""
    status: str = "planning"  # planning, developing, completed, archived
    tech_stack: List[str] = field(default_factory=list)
    repository_url: str = ""
    team_members: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "description": self.description,
            "status": self.status,
            "tech_stack": self.tech_stack,
            "repository_url": self.repository_url,
            "team_members": self.team_members
        })
        return data


@dataclass
class AgentNode(BaseNode):
    """Agent节点"""
    role: str = "execution"  # decision, audit, execution
    department: str = ""
    model: str = "gpt-4"
    capabilities: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    status: str = "idle"  # idle, busy, offline
    performance_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "role": self.role,
            "department": self.department,
            "model": self.model,
            "capabilities": self.capabilities,
            "skills": self.skills,
            "status": self.status,
            "performance_score": self.performance_score
        })
        return data


@dataclass
class SkillNode(BaseNode):
    """技能节点"""
    description: str = ""
    category: str = "general"  # analysis, generation, design, operation
    version: str = "1.0.0"
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "parameters": self.parameters,
            "dependencies": self.dependencies
        })
        return data


@dataclass
class DecisionNode(BaseNode):
    """决策节点"""
    title: str = ""
    content: str = ""
    made_by: str = ""  # Agent ID
    project_id: str = ""
    alternatives: List[str] = field(default_factory=list)
    impact: str = "medium"  # low, medium, high, critical
    status: str = "made"  # made, approved, rejected
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "title": self.title,
            "content": self.content,
            "made_by": self.made_by,
            "project_id": self.project_id,
            "alternatives": self.alternatives,
            "impact": self.impact,
            "status": self.status
        })
        return data


@dataclass
class PatternNode(BaseNode):
    """模式节点"""
    description: str = ""
    category: str = "architectural"  # architectural, design, implementation
    applicable_scenarios: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    success_rate: float = 0.0
    usage_count: int = 0
    example_projects: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "description": self.description,
            "category": self.category,
            "applicable_scenarios": self.applicable_scenarios,
            "prerequisites": self.prerequisites,
            "success_rate": self.success_rate,
            "usage_count": self.usage_count,
            "example_projects": self.example_projects
        })
        return data


@dataclass
class ProblemNode(BaseNode):
    """问题节点"""
    title: str = ""
    description: str = ""
    severity: str = "medium"  # low, medium, high, critical
    status: str = "open"  # open, solved, archived
    solution: str = ""
    solved_by: str = ""  # Agent ID
    related_problems: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "status": self.status,
            "solution": self.solution,
            "solved_by": self.solved_by,
            "related_problems": self.related_problems
        })
        return data


@dataclass
class KnowledgeNode(BaseNode):
    """知识节点"""
    title: str = ""
    content: str = ""
    category: str = "general"  # technical, business, process
    tags: List[str] = field(default_factory=list)
    source: str = ""
    confidence: float = 0.0
    verified: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "source": self.source,
            "confidence": self.confidence,
            "verified": self.verified
        })
        return data