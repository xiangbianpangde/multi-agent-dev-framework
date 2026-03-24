# 知识图谱设计

> **版本**: 1.0.0
> **用途**: 多Agent项目开发知识管理

---

## 一、概述

知识图谱是多Agent项目开发框架的核心组件，用于存储和管理项目、Agent、技能、决策、模式、问题和知识之间的关系。

### 核心价值

```
┌─────────────────────────────────────────────────────────────┐
│ 知识图谱的价值                                               │
├─────────────────────────────────────────────────────────────┤
│ 1. 知识关联 - Agent能力、技能、项目之间的关系               │
│ 2. 经验沉淀 - 成功模式、失败教训、最佳实践                  │
│ 3. 智能推荐 - 根据历史推荐架构方案、模型选择                │
│ 4. 上下文理解 - 新项目可参考相似历史项目                    │
│ 5. 决策追溯 - 记录每个重要决策的依据和影响                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、节点类型

### 2.1 节点清单

| 节点类型 | 标签 | 说明 |
|----------|------|------|
| 项目 | Project | 开发的多Agent项目 |
| Agent | Agent | 系统中的Agent角色 |
| 技能 | Skill | Agent具备的能力 |
| 决策 | Decision | 开发过程中的决策 |
| 模式 | Pattern | 可复用的设计模式 |
| 问题 | Problem | 遇到的问题及解决方案 |
| 知识 | Knowledge | 沉淀的知识点 |

### 2.2 节点属性

#### Project（项目）

```yaml
属性:
  id: string           # 唯一标识
  name: string         # 项目名称
  description: string  # 项目描述
  status: string       # planning, developing, completed, archived
  tech_stack: list     # 技术栈
  repository_url: string # 仓库地址
  team_members: list   # 团队成员
  created_at: datetime
  updated_at: datetime
```

#### Agent

```yaml
属性:
  id: string           # 唯一标识
  name: string         # Agent名称
  role: string         # decision, audit, execution
  department: string   # 所属部门
  model: string        # 使用的模型
  capabilities: list   # 能力列表
  skills: list         # 技能列表
  status: string       # idle, busy, offline
  performance_score: float # 绩效分数
```

#### Skill（技能）

```yaml
属性:
  id: string           # 唯一标识
  name: string         # 技能名称
  description: string  # 技能描述
  category: string     # analysis, generation, design, operation
  version: string      # 版本号
  parameters: dict     # 参数定义
  dependencies: list   # 依赖
```

#### Decision（决策）

```yaml
属性:
  id: string           # 唯一标识
  name: string         # 决策标题
  title: string        # 决策主题
  content: string      # 决策内容
  made_by: string      # 决策者Agent ID
  project_id: string   # 所属项目
  alternatives: list   # 备选方案
  impact: string       # low, medium, high, critical
  status: string       # made, approved, rejected
```

#### Pattern（模式）

```yaml
属性:
  id: string           # 唯一标识
  name: string         # 模式名称
  description: string  # 模式描述
  category: string     # architectural, design, implementation
  applicable_scenarios: list # 适用场景
  prerequisites: list  # 前置条件
  success_rate: float  # 成功率
  usage_count: int     # 使用次数
  example_projects: list # 示例项目
```

#### Problem（问题）

```yaml
属性:
  id: string           # 唯一标识
  name: string         # 问题标题
  title: string        # 问题主题
  description: string  # 问题描述
  severity: string     # low, medium, high, critical
  status: string       # open, solved, archived
  solution: string     # 解决方案
  solved_by: string    # 解决者Agent ID
  related_problems: list # 相关问题
```

#### Knowledge（知识）

```yaml
属性:
  id: string           # 唯一标识
  name: string         # 知识标题
  title: string        # 知识主题
  content: string      # 知识内容
  category: string     # technical, business, process
  tags: list           # 标签
  source: string       # 来源
  confidence: float    # 置信度
  verified: bool       # 是否验证
```

---

## 三、关系类型

### 3.1 关系清单

| 关系 | 起点 | 终点 | 说明 |
|------|------|------|------|
| HAS_AGENT | Project | Agent | 项目包含Agent |
| USES_SKILL | Agent | Skill | Agent使用技能 |
| DEPENDS_ON | Agent | Agent | Agent依赖关系 |
| CALLS | Agent | Agent | Agent调用关系 |
| MADE_DECISION | Agent | Decision | Agent做出决策 |
| AFFECTS | Decision | Agent/Project | 决策影响范围 |
| BASED_ON | Decision | Knowledge | 决策基于知识 |
| APPLIES_PATTERN | Project | Pattern | 项目应用模式 |
| SOLVES | Pattern | Problem | 模式解决问题 |
| LEARNS_FROM | Agent | Problem | 从问题学习 |
| REFERENCES | Decision/Knowledge | Knowledge | 参考引用 |
| EXTENDS | Agent | Agent | Agent扩展 |
| INHERITS | Skill | Skill | 技能继承 |

### 3.2 关系属性

```yaml
HAS_AGENT:
  role: string         # primary, secondary
  added_at: datetime

USES_SKILL:
  proficiency: float   # 熟练度 0-1
  last_used: datetime

MADE_DECISION:
  timestamp: datetime
  context: string

APPLIES_PATTERN:
  applied_at: datetime
  customizations: string
  success: bool

SOLVES:
  effectiveness: float # 效果 0-1
  notes: string
```

---

## 四、图谱示例

### 4.1 项目知识图谱

```
                    ┌─────────────┐
                    │  Project    │
                    │ 用户认证系统 │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │ HAS_AGENT     │ HAS_AGENT     │ HAS_AGENT
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ AuthAgent│    │ UserAgent│    │ LogAgent │
    │  认证    │    │  用户    │    │  日志    │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
    USES_SKILL      USES_SKILL      USES_SKILL
         │               │               │
         ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │jwt_auth  │    │crud_op   │    │log_write │
    │ JWT认证  │    │ CRUD操作 │    │ 日志写入 │
    └──────────┘    └──────────┘    └──────────┘
```

### 4.2 决策知识图谱

```
    ┌────────────────────────────────────────┐
    │              Decision                  │
    │  "选择JWT作为认证方案"                  │
    │  made_by: 中书省                        │
    └───────────────────┬────────────────────┘
                        │
           ┌────────────┼────────────┐
           │ BASED_ON   │ AFFECTS    │ ALTERNATIVE_TO
           ▼            ▼            ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │Knowledge │  │ AuthAgent│  │ Decision │
    │JWT最佳实践│  │ 需实现JWT│  │ Session方案│
    └──────────┘  └──────────┘  └──────────┘
```

---

## 五、使用示例

### 5.1 初始化知识图谱

```python
from tools.templates.core.knowledge_graph import KnowledgeGraph

# 创建连接
kg = KnowledgeGraph(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password"
)
kg.connect()
```

### 5.2 创建项目

```python
from tools.templates.core.knowledge_graph import ProjectNode, AgentNode

# 创建项目
project = ProjectNode(
    id="proj-001",
    name="用户认证系统",
    description="完整的用户认证和授权系统",
    tech_stack=["FastAPI", "PostgreSQL", "Redis"]
)
kg.create_project(project)

# 创建Agent
auth_agent = AgentNode(
    id="agent-auth",
    name="认证Agent",
    role="execution",
    department="兵部",
    model="gpt-4",
    capabilities=["认证", "授权", "Token管理"]
)
kg.create_agent(auth_agent)

# 添加Agent到项目
kg.add_agent_to_project("proj-001", "agent-auth", role="primary")
```

### 5.3 记录决策

```python
from tools.templates.core.knowledge_graph import DecisionNode

# 创建决策
decision = DecisionNode(
    id="dec-001",
    title="认证方案选择",
    content="选择JWT作为主要认证方案，理由：无状态、可扩展、安全性好",
    made_by="agent-zhongshu",
    project_id="proj-001"
)

# 记录决策，指定影响的Agent
kg.record_decision(
    decision,
    affected_nodes=[
        ("Agent", "agent-auth"),
        ("Agent", "agent-user")
    ]
)
```

### 5.4 推荐模式

```python
# 根据场景推荐模式
patterns = kg.suggest_patterns("实现用户认证系统")
for pattern in patterns:
    print(f"模式: {pattern['name']}, 成功率: {pattern['success_rate']}")

# 记录模式使用
kg.record_pattern_usage("pattern-jwt-auth", "proj-001", success=True)
```

### 5.5 知识检索

```python
# 搜索知识
results = kg.search_knowledge("JWT认证最佳实践", category="technical")
for knowledge in results:
    print(f"{knowledge['title']}: {knowledge['content'][:100]}")

# 获取相关决策
decisions = kg.get_project_decisions("proj-001")
for decision in decisions:
    print(f"决策: {decision['title']}")
```

---

## 六、与三省六部集成

### 6.1 中书省使用

```python
# 规划时查询相似项目
similar_projects = kg.find_similar_projects(requirements)

# 获取推荐模式
patterns = kg.suggest_patterns(requirements)

# 查看Agent能力
agent_skills = kg.get_agent_skills("agent-id")

# 记录架构决策
kg.record_decision(decision, affected_nodes)
```

### 6.2 门下省使用

```python
# 审核时检查历史决策
history_decisions = kg.get_project_decisions(project_id)

# 验证模式适用性
pattern_stats = kg.get_pattern_usage("pattern-id")

# 发现潜在风险
similar_problems = kg.find_similar_problems("...")
```

### 6.3 六部使用

```python
# 获取技能知识
skill_knowledge = kg.get_related_knowledge("Skill", "skill-id")

# 记录问题解决
problem = ProblemNode(...)
kg.record_problem(problem, solution="...")

# 更新经验
kg.record_pattern_usage("pattern-id", "project-id", success=True)
```

---

## 七、配置说明

### 7.1 Neo4j配置

```yaml
# config/knowledge_graph.yaml
neo4j:
  uri: bolt://localhost:7687
  user: neo4j
  password: password
  max_connection_pool_size: 50
  connection_timeout: 30
```

### 7.2 Docker部署

```yaml
# docker-compose.yml
version: "3.8"
services:
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      NEO4J_AUTH: neo4j/password
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs

volumes:
  neo4j_data:
  neo4j_logs:
```

---

*最后更新: 2026-03-24*