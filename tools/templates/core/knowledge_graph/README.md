# 知识图谱模块

> 知识图谱核心实现

## 模块说明

本模块提供基于Neo4j的知识图谱管理能力。

## 使用方法

```python
from tools.templates.core.knowledge_graph import (
    KnowledgeGraph,
    ProjectNode, AgentNode, SkillNode,
    DecisionNode, PatternNode, ProblemNode, KnowledgeNode
)

# 连接知识图谱
kg = KnowledgeGraph()
kg.connect()

# 创建项目
project = ProjectNode(
    id="proj-001",
    name="我的项目",
    description="项目描述"
)
kg.create_project(project)

# 创建Agent
agent = AgentNode(
    id="agent-001",
    name="我的Agent",
    role="execution"
)
kg.create_agent(agent)

# 添加Agent到项目
kg.add_agent_to_project("proj-001", "agent-001")

# 查询项目Agent
agents = kg.get_project_agents("proj-001")
```

## 详细文档

参见 [知识图谱设计文档](../../../engineering-knowledge-base/07-knowledge-graph/design.md)