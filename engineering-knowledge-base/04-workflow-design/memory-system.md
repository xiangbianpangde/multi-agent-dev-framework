# 记忆系统设计

> **版本**: 1.0.0
> **用途**: 多Agent项目开发过程中的知识管理

---

## 一、记忆分层

### 1.1 三层记忆架构

```
┌─────────────────────────────────────────────────────────────┐
│ 长期记忆 (Long-term Memory)                                 │
│ - 存储周期: 永久                                           │
│ - 存储内容: 总结后的知识、最佳实践、经验教训               │
│ - 存储介质: 知识图谱 + Markdown文件 + 数据库               │
│ - 访问频率: 低                                             │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ 总结沉淀
┌─────────────────────────────────────────────────────────────┐
│ 中期记忆 (Medium-term Memory)                               │
│ - 存储周期: 项目周期                                       │
│ - 存储内容: 项目相关文档、会议记录、设计决策               │
│ - 存储介质: 知识图谱 + Markdown文件 + 数据库               │
│ - 访问频率: 中                                             │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ 会话整合
┌─────────────────────────────────────────────────────────────┐
│ 短期记忆 (Short-term Memory)                                │
│ - 存储周期: 会话期间                                       │
│ - 存储内容: 当前对话上下文、临时变量                       │
│ - 存储介质: 内存 + Redis                                   │
│ - 访问频率: 高                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 层级对比

| 维度 | 短期记忆 | 中期记忆 | 长期记忆 |
|------|----------|----------|----------|
| 周期 | 会话级 | 项目级 | 永久 |
| 容量 | 有限(上下文窗口) | 中等 | 无限 |
| 速度 | 毫秒 | 秒 | 秒-分钟 |
| 精度 | 原始细节 | 结构化 | 抽象总结 |
| 用途 | 当前任务 | 项目协作 | 跨项目复用 |

---

## 二、短期记忆

### 2.1 定义

```
┌─────────────────────────────────────────────────────────────┐
│ 短期记忆                                                    │
├─────────────────────────────────────────────────────────────┤
│ 触发: 每次会话开始                                          │
│ 存储: 当前对话的所有信息                                    │
│ 生命周期: 会话结束即清除                                    │
│ 容量: 受模型上下文窗口限制                                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 存储内容

```
短期记忆包含:
├── 用户输入历史
├── Agent响应历史
├── 工具调用记录
├── 中间计算结果
├── 临时状态变量
└── 当前任务上下文
```

### 2.3 技术实现

```python
# 内存存储（当前会话）
class ShortTermMemory:
    """短期记忆管理"""
    
    def __init__(self, max_tokens: int = 128000):
        self.max_tokens = max_tokens
        self.messages = []  # 消息历史
        self.variables = {}  # 临时变量
        self.tool_calls = []  # 工具调用记录
    
    def add_message(self, role: str, content: str):
        """添加消息"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now()
        })
        self._check_overflow()
    
    def set_variable(self, key: str, value: Any):
        """设置临时变量"""
        self.variables[key] = value
    
    def get_variable(self, key: str) -> Any:
        """获取临时变量"""
        return self.variables.get(key)
    
    def _check_overflow(self):
        """检查是否超出上下文窗口"""
        current_tokens = self._count_tokens()
        if current_tokens > self.max_tokens * 0.9:
            # 触发中期记忆同步
            self._sync_to_medium_term()

# Redis存储（跨Agent共享）
class RedisShortTermMemory:
    """Redis短期记忆（用于Agent间共享）"""
    
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.ttl = 3600  # 1小时过期
    
    def set(self, session_id: str, key: str, value: Any):
        self.redis.hset(f"session:{session_id}", key, json.dumps(value))
        self.redis.expire(f"session:{session_id}", self.ttl)
    
    def get(self, session_id: str, key: str) -> Any:
        value = self.redis.hget(f"session:{session_id}", key)
        return json.loads(value) if value else None
```

### 2.4 溢出处理

```
当短期记忆接近上限时：

1. 评估重要性
   ├── 核心需求信息 → 保留
   ├── 中间过程信息 → 压缩或归档
   └── 已完成任务 → 归档到中期记忆

2. 压缩策略
   ├── 摘要生成: 长对话 → 简短摘要
   ├── 关键提取: 提取关键决策和结论
   └── 引用替换: 详细内容 → 引用链接

3. 归档策略
   └── 同步到中期记忆
```

---

## 三、中期记忆

### 3.1 定义

```
┌─────────────────────────────────────────────────────────────┐
│ 中期记忆                                                    │
├─────────────────────────────────────────────────────────────┤
│ 触发: 项目开始                                              │
│ 存储: 项目相关的所有知识和决策                              │
│ 生命周期: 项目完成前持续存在                                │
│ 容量: 中等，按项目隔离                                      │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 存储内容

```
中期记忆包含:
├── 项目需求文档
├── 架构设计决策
├── 会议记录
├── 代码评审记录
├── 问题跟踪记录
├── 测试结果
└── 用户反馈
```

### 3.3 目录结构

```
memory/
├── daily/                     # 日记（按日期）
│   ├── 2026-03-24.md
│   └── 2026-03-25.md
├── sessions/                  # 会话记录
│   ├── session-001.json
│   └── session-002.json
├── knowledge/                 # 知识沉淀
│   ├── decisions/             # 决策记录
│   │   ├── arch-decision-001.md
│   │   └── tech-choice-001.md
│   ├── problems/              # 问题记录
│   │   ├── bug-001.md
│   │   └── solution-001.md
│   └── patterns/              # 模式沉淀
│       ├── auth-pattern.md
│       └── api-pattern.md
└── project-context.json       # 项目上下文
```

### 3.4 技术实现

```python
# Markdown文件存储
class MediumTermMemory:
    """中期记忆管理"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.memory_path = self.project_path / "memory"
        self._init_structure()
    
    def save_decision(self, decision: Decision):
        """保存决策记录"""
        path = self.memory_path / "knowledge" / "decisions" / f"{decision.id}.md"
        content = self._format_decision(decision)
        path.write_text(content)
    
    def save_problem(self, problem: Problem):
        """保存问题记录"""
        path = self.memory_path / "knowledge" / "problems" / f"{problem.id}.md"
        content = self._format_problem(problem)
        path.write_text(content)
    
    def search(self, query: str) -> List[SearchResult]:
        """搜索记忆"""
        results = []
        for md_file in self.memory_path.rglob("*.md"):
            content = md_file.read_text()
            if query.lower() in content.lower():
                results.append(SearchResult(
                    path=str(md_file),
                    snippet=self._extract_snippet(content, query)
                ))
        return results

# 知识图谱存储
class KnowledgeGraph:
    """知识图谱（用于关联知识）"""
    
    def __init__(self, neo4j_url: str):
        self.driver = GraphDatabase.driver(neo4j_url)
    
    def add_node(self, label: str, properties: dict):
        """添加节点"""
        with self.driver.session() as session:
            session.run(
                f"CREATE (n:{label} $props)",
                props=properties
            )
    
    def add_relation(self, from_id: str, to_id: str, relation: str):
        """添加关系"""
        with self.driver.session() as session:
            session.run(
                f"MATCH (a {{id: $from_id}}), (b {{id: $to_id}}) "
                f"CREATE (a)-[:{relation}]->(b)",
                from_id=from_id, to_id=to_id
            )
    
    def find_related(self, node_id: str, depth: int = 2) -> List[dict]:
        """查找相关节点"""
        with self.driver.session() as session:
            result = session.run(
                f"MATCH (n {{id: $id}})-[*1..{depth}]-(related) "
                "RETURN related",
                id=node_id
            )
            return [record["related"] for record in result]
```

---

## 四、长期记忆

### 4.1 定义

```
┌─────────────────────────────────────────────────────────────┐
│ 长期记忆                                                    │
├─────────────────────────────────────────────────────────────┤
│ 触发: 项目完成后总结                                        │
│ 存储: 可复用的知识、模式、最佳实践                          │
│ 生命周期: 永久                                              │
│ 容量: 无限                                                  │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 存储内容

```
长期记忆包含:
├── 成功模式
│   ├── 架构模式
│   ├── 代码模式
│   └── 流程模式
├── 经验教训
│   ├── 常见错误
│   └── 解决方案
├── 最佳实践
│   ├── 代码规范
│   └── 文档模板
└── 领域知识
    ├── 技术知识
    └── 业务知识
```

### 4.3 知识沉淀流程

```
项目完成
    │
    ▼
┌─────────────────┐
│ 回顾项目历程   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 提取有价值的知识 │
│ - 成功做法      │
│ - 失败教训      │
│ - 可复用模式    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 结构化整理      │
│ - 分类         │
│ - 标签         │
│ - 关联         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 存入长期记忆    │
│ - 知识图谱      │
│ - Markdown文件  │
│ - 数据库        │
└─────────────────┘
```

### 4.4 知识检索

```python
class LongTermMemory:
    """长期记忆管理"""
    
    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.index = self._build_index()
    
    def query(self, query: str, top_k: int = 5) -> List[KnowledgeItem]:
        """查询长期记忆"""
        # 语义搜索
        query_embedding = self._embed(query)
        results = self.index.search(query_embedding, top_k)
        return results
    
    def add_knowledge(self, knowledge: KnowledgeItem):
        """添加知识到长期记忆"""
        # 生成嵌入向量
        embedding = self._embed(knowledge.content)
        
        # 存储到索引
        self.index.add(embedding, knowledge)
        
        # 存储到文件
        path = self._get_storage_path(knowledge)
        path.write_text(knowledge.to_markdown())
    
    def link_knowledge(self, from_id: str, to_id: str, relation: str):
        """建立知识关联"""
        self.knowledge_graph.add_relation(from_id, to_id, relation)
```

---

## 五、记忆流转

### 5.1 流转规则

```
┌─────────────────────────────────────────────────────────────┐
│ 短期 → 中期                                                 │
├─────────────────────────────────────────────────────────────┤
│ 触发条件:                                                   │
│ - 会话结束                                                  │
│ - 短期记忆溢出                                              │
│ - 重要决策产生                                              │
│                                                             │
│ 转换内容:                                                   │
│ - 会话摘要                                                  │
│ - 重要决策                                                  │
│ - 待办事项                                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 中期 → 长期                                                 │
├─────────────────────────────────────────────────────────────┤
│ 触发条件:                                                   │
│ - 项目完成                                                  │
│ - 里程碑达成                                                │
│ - 人工标记                                                  │
│                                                             │
│ 转换内容:                                                   │
│ - 成功模式                                                  │
│ - 经验教训                                                  │
│ - 最佳实践                                                  │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 自动化流程

```python
class MemoryManager:
    """记忆管理器"""
    
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.medium_term = MediumTermMemory()
        self.long_term = LongTermMemory()
    
    def sync_to_medium(self):
        """同步短期记忆到中期"""
        # 生成会话摘要
        summary = self._generate_summary(self.short_term.messages)
        
        # 提取决策
        decisions = self._extract_decisions(self.short_term.messages)
        
        # 保存到中期记忆
        self.medium_term.save_session_summary(summary)
        for decision in decisions:
            self.medium_term.save_decision(decision)
    
    def archive_to_long(self, project_id: str):
        """归档中期记忆到长期"""
        # 收集项目知识
        knowledge = self.medium_term.collect_project_knowledge(project_id)
        
        # 提取可复用模式
        patterns = self._extract_patterns(knowledge)
        
        # 提取经验教训
        lessons = self._extract_lessons(knowledge)
        
        # 存入长期记忆
        for pattern in patterns:
            self.long_term.add_knowledge(pattern)
        for lesson in lessons:
            self.long_term.add_knowledge(lesson)
```

---

## 六、知识图谱

### 6.1 节点类型

```yaml
节点类型:
  Decision:
    # 决策节点
    properties:
      id: string
      title: string
      content: string
      made_by: string
      timestamp: datetime
      context: string
  
  Problem:
    # 问题节点
    properties:
      id: string
      title: string
      description: string
      severity: string
      status: string
      solution: string
  
  Pattern:
    # 模式节点
    properties:
      id: string
      name: string
      description: string
      applicable_scenarios: list
      example: string
  
  Knowledge:
    # 知识节点
    properties:
      id: string
      title: string
      content: string
      tags: list
      source: string
```

### 6.2 关系类型

```yaml
关系类型:
  LEADS_TO:
    # 决策导致
    from: Decision
    to: Decision | Problem
  
  SOLVES:
    # 解决
    from: Solution
    to: Problem
  
  RELATES_TO:
    # 相关
    from: any
    to: any
  
  DERIVED_FROM:
    # 派生自
    from: Pattern
    to: Knowledge
  
  APPLIES_TO:
    # 适用于
    from: Pattern
    to: Scenario
```

---

## 七、检索策略

### 7.1 检索优先级

```
检索顺序:
1. 短期记忆（最快，最相关）
   └── 当前会话上下文

2. 中期记忆（项目相关）
   └── 项目知识库

3. 长期记忆（通用知识）
   └── 可复用模式
```

### 7.2 检索接口

```python
def recall(query: str, context: dict = None) -> RecallResult:
    """
    记忆检索接口
    
    Args:
        query: 查询内容
        context: 上下文信息（项目ID等）
    
    Returns:
        RecallResult: 检索结果
    """
    results = []
    
    # 1. 检索短期记忆
    short_term_results = short_term_memory.search(query)
    results.extend(short_term_results)
    
    # 2. 检索中期记忆（如果有项目上下文）
    if context and "project_id" in context:
        medium_term_results = medium_term_memory.search(
            query, 
            project_id=context["project_id"]
        )
        results.extend(medium_term_results)
    
    # 3. 检索长期记忆
    long_term_results = long_term_memory.query(query)
    results.extend(long_term_results)
    
    # 4. 排序和去重
    results = rank_and_deduplicate(results)
    
    return RecallResult(
        items=results[:10],  # 返回前10条
        sources=["short_term", "medium_term", "long_term"]
    )
```

---

## 八、配置示例

### 8.1 记忆配置

```json
{
  "memory": {
    "short_term": {
      "max_tokens": 128000,
      "storage": "memory",
      "redis": {
        "url": "redis://localhost:6379",
        "ttl": 3600
      }
    },
    "medium_term": {
      "storage": "file",
      "path": "./memory",
      "knowledge_graph": {
        "url": "bolt://localhost:7687",
        "user": "neo4j",
        "password": "password"
      }
    },
    "long_term": {
      "storage": "file",
      "path": "./knowledge-base",
      "vector_db": {
        "type": "milvus",
        "url": "http://localhost:19530"
      }
    }
  }
}
```

---

*最后更新: 2026-03-24*