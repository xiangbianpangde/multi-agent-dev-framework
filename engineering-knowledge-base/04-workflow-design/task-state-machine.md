# 任务状态机

> **版本**: 1.0.0
> **用途**: 任务状态流转控制规范

---

## 一、状态定义

### 1.1 状态列表

| 状态 | 英文标识 | 说明 | 负责部门 |
|------|----------|------|----------|
| 草稿 | draft | 需求已提交，待分析 | 中书省 |
| 规划中 | planning | 中书省正在设计方案 | 中书省 |
| 审核中 | review | 门下省正在审核 | 门下省 |
| 已封驳 | rejected | 门下省驳回，需重做 | 中书省 |
| 已派发 | dispatched | 尚书省已派发任务 | 尚书省 |
| 执行中 | executing | 六部正在执行 | 六部 |
| 审查中 | checking | 门下省正在验收 | 门下省 |
| 已通过 | accepted | 验收通过 | 尚书省 |
| 已完成 | done | 任务完成 | - |
| 已取消 | cancelled | 任务被取消 | - |
| 已阻塞 | blocked | 任务被阻塞 | 中书省 |

### 1.2 状态分组

```
┌─────────────────────────────────────────────────────────────┐
│ 初始状态                                                    │
├─────────────────────────────────────────────────────────────┤
│ draft - 所有任务的起点                                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 处理中状态                                                  │
├─────────────────────────────────────────────────────────────┤
│ planning, review, dispatched, executing, checking           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 暂态                                                        │
├─────────────────────────────────────────────────────────────┤
│ rejected, blocked - 需要处理后才能继续                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 终态                                                        │
├─────────────────────────────────────────────────────────────┤
│ done, cancelled - 任务结束                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、状态转换

### 2.1 转换图

```
                         ┌──────────────────────────────────────┐
                         │                                      │
                         ▼                                      │
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     │
│  draft  │────→│planning │────→│ review  │────→│dispatched│    │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     │
                      │              │               │           │
                      │              │ rejected      │           │
                      │              ▼               │           │
                      │        ┌─────────┐          │           │
                      │        │rejected │──────────┘           │
                      │        └─────────┘                      │
                      │              │                          │
                      └──────────────┘                          │
                                                                │
                                            ┌───────────────────┘
                                            │
                                            ▼
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  done   │←────│accepted │←────│checking │←────│executing│
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                      │
                                      │ 返回修改
                                      ▼
                              ┌─────────────┐
                              │  executing  │
                              └─────────────┘

任意状态 ─────────────────────→ cancelled (取消)
                     或
任意状态 ─────────────────────→ blocked (阻塞)
```

### 2.2 合法转换表

```python
VALID_TRANSITIONS = {
    "draft": ["planning", "cancelled"],
    "planning": ["review", "cancelled", "blocked"],
    "review": ["dispatched", "rejected", "cancelled"],
    "rejected": ["planning", "cancelled"],
    "dispatched": ["executing", "cancelled", "blocked"],
    "executing": ["checking", "cancelled", "blocked"],
    "checking": ["accepted", "executing", "cancelled"],
    "accepted": ["done"],
    "done": [],  # 终态
    "cancelled": [],  # 终态
    "blocked": ["planning", "cancelled"],  # 阻塞后可恢复或取消
}
```

### 2.3 转换条件

| 从状态 | 到状态 | 触发条件 | 操作者 |
|--------|--------|----------|--------|
| draft | planning | 需求确认 | 中书省 |
| planning | review | 方案完成 | 中书省 |
| review | dispatched | 审核通过 | 门下省 |
| review | rejected | 审核不通过 | 门下省 |
| rejected | planning | 返工修改 | 中书省 |
| dispatched | executing | 任务开始 | 尚书省 |
| executing | checking | 执行完成 | 六部 |
| checking | accepted | 验收通过 | 门下省 |
| checking | executing | 需要修改 | 门下省 |
| accepted | done | 确认完成 | 尚书省 |
| 任意 | cancelled | 取消任务 | 中书省/门下省 |
| 任意 | blocked | 遇到阻塞 | 任意 |
| blocked | planning | 恢复任务 | 中书省 |

---

## 三、状态机实现

### 3.1 核心代码

```python
from enum import Enum
from typing import Optional
from datetime import datetime

class TaskState(Enum):
    """任务状态枚举"""
    DRAFT = "draft"
    PLANNING = "planning"
    REVIEW = "review"
    REJECTED = "rejected"
    DISPATCHED = "dispatched"
    EXECUTING = "executing"
    CHECKING = "checking"
    ACCEPTED = "accepted"
    DONE = "done"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"

class StateMachine:
    """任务状态机"""
    
    VALID_TRANSITIONS = {
        TaskState.DRAFT: [TaskState.PLANNING, TaskState.CANCELLED],
        TaskState.PLANNING: [TaskState.REVIEW, TaskState.CANCELLED, TaskState.BLOCKED],
        TaskState.REVIEW: [TaskState.DISPATCHED, TaskState.REJECTED, TaskState.CANCELLED],
        TaskState.REJECTED: [TaskState.PLANNING, TaskState.CANCELLED],
        TaskState.DISPATCHED: [TaskState.EXECUTING, TaskState.CANCELLED, TaskState.BLOCKED],
        TaskState.EXECUTING: [TaskState.CHECKING, TaskState.CANCELLED, TaskState.BLOCKED],
        TaskState.CHECKING: [TaskState.ACCEPTED, TaskState.EXECUTING, TaskState.CANCELLED],
        TaskState.ACCEPTED: [TaskState.DONE],
        TaskState.DONE: [],
        TaskState.CANCELLED: [],
        TaskState.BLOCKED: [TaskState.PLANNING, TaskState.CANCELLED],
    }
    
    def __init__(self, initial_state: TaskState = TaskState.DRAFT):
        self.current_state = initial_state
        self.history = [(initial_state, datetime.now(), "初始化")]
    
    def can_transition_to(self, target: TaskState) -> bool:
        """检查是否可以转换到目标状态"""
        return target in self.VALID_TRANSITIONS[self.current_state]
    
    def transition(self, target: TaskState, reason: str = "") -> bool:
        """执行状态转换"""
        if not self.can_transition_to(target):
            raise InvalidTransitionError(
                f"不能从 {self.current_state.value} 转换到 {target.value}"
            )
        
        old_state = self.current_state
        self.current_state = target
        self.history.append((target, datetime.now(), reason))
        
        # 记录日志
        log_transition(old_state, target, reason)
        
        return True
    
    def get_history(self) -> list:
        """获取状态历史"""
        return self.history.copy()
    
    def is_terminal(self) -> bool:
        """是否为终态"""
        return self.current_state in [TaskState.DONE, TaskState.CANCELLED]

class InvalidTransitionError(Exception):
    """非法状态转换异常"""
    pass
```

### 3.2 状态验证中间件

```python
def validate_transition(func):
    """状态转换验证装饰器"""
    def wrapper(self, *args, **kwargs):
        # 检查是否可以转换
        if not self.state_machine.can_transition_to(kwargs.get('target_state')):
            raise InvalidTransitionError(
                f"状态转换非法: {self.state_machine.current_state} -> {kwargs.get('target_state')}"
            )
        return func(self, *args, **kwargs)
    return wrapper

class Task:
    """任务类"""
    
    def __init__(self, task_id: str, title: str):
        self.task_id = task_id
        self.title = title
        self.state_machine = StateMachine()
        self.assignee = None
        self.data = {}
    
    @validate_transition
    def change_state(self, target_state: TaskState, reason: str = ""):
        """变更任务状态"""
        self.state_machine.transition(target_state, reason)
    
    def assign(self, assignee: str):
        """分配任务"""
        if self.state_machine.current_state != TaskState.DISPATCHED:
            raise ValueError("只能在dispatched状态分配任务")
        self.assignee = assignee
```

---

## 四、状态监控

### 4.1 监控指标

```yaml
监控指标:
  task_state_duration:
    # 各状态停留时间
    type: histogram
    labels: [state]
    description: 任务在各状态的停留时间
  
  task_transition_count:
    # 状态转换次数
    type: counter
    labels: [from_state, to_state]
    description: 状态转换计数
  
  task_rejection_rate:
    # 封驳率
    type: gauge
    description: 任务被封驳的比例
  
  task_completion_rate:
    # 完成率
    type: gauge
    description: 任务完成比例
```

### 4.2 告警规则

```yaml
告警规则:
  - name: task_stuck_in_planning
    condition: task_state_duration{state="planning"} > 3600
    severity: warning
    message: "任务在规划状态停留超过1小时"
  
  - name: task_rejected_too_many_times
    condition: task_rejection_count > 3
    severity: error
    message: "任务被封驳超过3次，可能需要人工介入"
  
  - name: high_rejection_rate
    condition: task_rejection_rate > 0.3
    severity: warning
    message: "任务封驳率超过30%，检查规划质量"
  
  - name: task_blocked
    condition: task_state == "blocked"
    severity: warning
    message: "任务被阻塞，需要处理"
```

---

## 五、状态持久化

### 5.1 存储格式

```json
{
  "task_id": "TASK-001",
  "title": "实现用户认证模块",
  "state": "executing",
  "state_history": [
    {
      "state": "draft",
      "timestamp": "2026-03-24T10:00:00Z",
      "reason": "创建任务"
    },
    {
      "state": "planning",
      "timestamp": "2026-03-24T10:05:00Z",
      "reason": "开始规划"
    },
    {
      "state": "review",
      "timestamp": "2026-03-24T10:30:00Z",
      "reason": "提交审核"
    },
    {
      "state": "dispatched",
      "timestamp": "2026-03-24T10:45:00Z",
      "reason": "审核通过"
    },
    {
      "state": "executing",
      "timestamp": "2026-03-24T11:00:00Z",
      "reason": "开始执行"
    }
  ],
  "current_assignee": "兵部",
  "metadata": {
    "priority": 1,
    "estimated_hours": 8
  }
}
```

### 5.2 恢复机制

```python
class TaskRecovery:
    """任务恢复"""
    
    @staticmethod
    def from_storage(data: dict) -> Task:
        """从存储恢复任务"""
        task = Task(data["task_id"], data["title"])
        
        # 恢复状态
        current_state = TaskState(data["state"])
        task.state_machine.current_state = current_state
        
        # 恢复历史
        for record in data["state_history"]:
            task.state_machine.history.append(
                (TaskState(record["state"]), 
                 datetime.fromisoformat(record["timestamp"]),
                 record["reason"])
            )
        
        # 恢复其他属性
        task.assignee = data.get("current_assignee")
        task.data = data.get("metadata", {})
        
        return task
    
    @staticmethod
    def to_storage(task: Task) -> dict:
        """保存任务到存储"""
        return {
            "task_id": task.task_id,
            "title": task.title,
            "state": task.state_machine.current_state.value,
            "state_history": [
                {
                    "state": s.value,
                    "timestamp": t.isoformat(),
                    "reason": r
                }
                for s, t, r in task.state_machine.history
            ],
            "current_assignee": task.assignee,
            "metadata": task.data
        }
```

---

## 六、并发控制

### 6.1 并发问题

```
可能的问题:
1. 多个Agent同时修改状态
2. 状态转换竞争条件
3. 历史记录丢失
```

### 6.2 解决方案

```python
import threading

class ConcurrentStateMachine:
    """线程安全的状态机"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.state_machine = StateMachine()
    
    def transition(self, target: TaskState, reason: str = "") -> bool:
        """线程安全的状态转换"""
        with self._lock:
            return self.state_machine.transition(target, reason)
    
    def get_state(self) -> TaskState:
        """获取当前状态"""
        with self._lock:
            return self.state_machine.current_state

# 使用数据库乐观锁
class DatabaseStateMachine:
    """基于数据库的状态机（乐观锁）"""
    
    def transition(self, task_id: str, target: TaskState, reason: str, version: int) -> bool:
        """乐观锁状态转换"""
        # UPDATE tasks 
        # SET state = ?, version = version + 1 
        # WHERE task_id = ? AND version = ?
        result = db.execute(
            "UPDATE tasks SET state = ?, version = version + 1, "
            "updated_at = ? WHERE task_id = ? AND version = ?",
            [target.value, datetime.now(), task_id, version]
        )
        
        if result.rowcount == 0:
            raise ConcurrentModificationError(
                "任务已被其他进程修改，请刷新后重试"
            )
        
        return True
```

---

## 七、最佳实践

### 7.1 设计原则

```
┌─────────────────────────────────────────────────────────────┐
│ 状态机设计原则                                              │
├─────────────────────────────────────────────────────────────┤
│ 1. 明确边界 - 每个状态有清晰定义                            │
│ 2. 最少状态 - 不引入不必要的状态                            │
│ 3. 合法转换 - 所有转换必须明确允许                          │
│ 4. 可追溯 - 记录所有状态变更历史                            │
│ 5. 可恢复 - 支持从异常状态恢复                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 常见错误

| 错误 | 表现 | 解决方案 |
|------|------|----------|
| 状态跳跃 | 从draft直接到executing | 严格执行合法转换表 |
| 状态膨胀 | 引入过多中间状态 | 合并相似状态 |
| 无限循环 | rejected和planning循环 | 设置循环次数限制 |
| 状态不一致 | 多处状态不同步 | 使用单一数据源 |

---

*最后更新: 2026-03-24*