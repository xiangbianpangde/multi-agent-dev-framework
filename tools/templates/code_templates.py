"""
常用代码模板集合

包含：
- 任务调度器模板
- 消息总线模板
- 状态机模板
- 记忆管理模板
"""

# ========== 任务调度器模板 ==========

TASK_DISPATCHER_TEMPLATE = '''
"""
任务调度器

功能：
- 接收任务
- 分配给Agent
- 跟踪进度
- 处理结果
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """任务定义"""
    id: str
    name: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    assignee: Optional[str] = None
    priority: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class TaskDispatcher:
    """任务调度器"""
    
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, Any] = {}
        self.running_count = 0
    
    def submit(self, task: Task) -> str:
        """提交任务"""
        self.tasks[task.id] = task
        logger.info(f"任务提交: {task.id}")
        return task.id
    
    def dispatch(self) -> bool:
        """调度任务"""
        # 找出待执行的任务
        pending = [
            t for t in self.tasks.values()
            if t.status == TaskStatus.PENDING
        ]
        
        if not pending:
            return False
        
        # 按优先级排序
        pending.sort(key=lambda t: t.priority)
        
        # 分配任务
        for task in pending:
            if self.running_count >= self.max_concurrent:
                break
            
            if self._assign_task(task):
                self.running_count += 1
        
        return True
    
    def _assign_task(self, task: Task) -> bool:
        """分配任务给Agent"""
        # 找到合适的Agent
        agent = self._find_available_agent(task)
        if not agent:
            return False
        
        # 更新任务状态
        task.status = TaskStatus.RUNNING
        task.assignee = agent.id
        task.started_at = datetime.now()
        
        # 发送任务给Agent
        # agent.execute(task)
        
        logger.info(f"任务分配: {task.id} -> {agent.id}")
        return True
    
    def _find_available_agent(self, task: Task) -> Optional[Any]:
        """找到可用的Agent"""
        # TODO: 实现Agent选择逻辑
        return None
    
    def complete(self, task_id: str, result: Dict[str, Any]):
        """完成任务"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.result = result
        self.running_count -= 1
        
        logger.info(f"任务完成: {task_id}")
    
    def fail(self, task_id: str, error: str):
        """任务失败"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        task.status = TaskStatus.FAILED
        task.error = error
        self.running_count -= 1
        
        logger.error(f"任务失败: {task_id}, 错误: {error}")
'''


# ========== 消息总线模板 ==========

MESSAGE_BUS_TEMPLATE = '''
"""
消息总线

功能：
- Agent间消息传递
- 消息路由
- 消息过滤
"""
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import asyncio

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """消息类型"""
    TASK = "task"
    NOTIFICATION = "notification"
    QUERY = "query"
    RESPONSE = "response"
    ERROR = "error"


@dataclass
class Message:
    """消息定义"""
    id: str
    sender: str
    receiver: str
    type: MessageType
    content: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 3
    requires_reply: bool = False
    reply_to: Optional[str] = None


class MessageBus:
    """消息总线"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.permission_matrix: Dict[str, List[str]] = {}
    
    def register(self, agent_id: str, callback: Callable):
        """注册Agent"""
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(callback)
        logger.info(f"Agent注册: {agent_id}")
    
    def set_permissions(self, sender: str, allowed_receivers: List[str]):
        """设置权限"""
        self.permission_matrix[sender] = allowed_receivers
    
    def can_send(self, sender: str, receiver: str) -> bool:
        """检查发送权限"""
        if sender not in self.permission_matrix:
            return False
        return receiver in self.permission_matrix[sender]
    
    async def send(self, message: Message) -> bool:
        """发送消息"""
        # 检查权限
        if not self.can_send(message.sender, message.receiver):
            logger.warning(f"消息发送被拒绝: {message.sender} -> {message.receiver}")
            return False
        
        # 加入队列
        await self.message_queue.put(message)
        return True
    
    async def process(self):
        """处理消息队列"""
        while True:
            message = await self.message_queue.get()
            
            # 路由到接收者
            if message.receiver in self.subscribers:
                for callback in self.subscribers[message.receiver]:
                    try:
                        await callback(message)
                    except Exception as e:
                        logger.error(f"消息处理失败: {e}")
            
            self.message_queue.task_done()
    
    async def broadcast(self, sender: str, message_type: MessageType, 
                        content: Dict[str, Any]):
        """广播消息"""
        for receiver in self.subscribers:
            if receiver != sender and self.can_send(sender, receiver):
                await self.send(Message(
                    id=f"msg-{datetime.now().timestamp()}",
                    sender=sender,
                    receiver=receiver,
                    type=message_type,
                    content=content
                ))
'''


# ========== 状态机模板 ==========

STATE_MACHINE_TEMPLATE = '''
"""
任务状态机

功能：
- 状态定义
- 状态转换
- 状态验证
"""
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TaskState(Enum):
    """任务状态"""
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


# 合法状态转换
VALID_TRANSITIONS: Dict[TaskState, List[TaskState]] = {
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


@dataclass
class StateRecord:
    """状态记录"""
    state: TaskState
    timestamp: datetime
    reason: str = ""


class StateMachine:
    """状态机"""
    
    def __init__(self, initial_state: TaskState = TaskState.DRAFT):
        self.current_state = initial_state
        self.history: List[StateRecord] = [
            StateRecord(state=initial_state, timestamp=datetime.now(), reason="初始化")
        ]
    
    def can_transition_to(self, target: TaskState) -> bool:
        """检查是否可以转换"""
        return target in VALID_TRANSITIONS.get(self.current_state, [])
    
    def transition(self, target: TaskState, reason: str = "") -> bool:
        """执行状态转换"""
        if not self.can_transition_to(target):
            logger.error(f"非法状态转换: {self.current_state} -> {target}")
            return False
        
        old_state = self.current_state
        self.current_state = target
        self.history.append(StateRecord(
            state=target,
            timestamp=datetime.now(),
            reason=reason
        ))
        
        logger.info(f"状态转换: {old_state.value} -> {target.value}, 原因: {reason}")
        return True
    
    def is_terminal(self) -> bool:
        """是否为终态"""
        return self.current_state in [TaskState.DONE, TaskState.CANCELLED]
    
    def get_history(self) -> List[Dict]:
        """获取历史记录"""
        return [
            {
                "state": record.state.value,
                "timestamp": record.timestamp.isoformat(),
                "reason": record.reason
            }
            for record in self.history
        ]
'''


# ========== 记忆管理模板 ==========

MEMORY_MANAGER_TEMPLATE = '''
"""
记忆管理器

功能：
- 短期记忆（内存/Redis）
- 中期记忆（文件/数据库）
- 长期记忆（知识库）
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class MemoryItem:
    """记忆项"""
    id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None


class ShortTermMemory:
    """短期记忆（内存）"""
    
    def __init__(self, max_items: int = 1000):
        self.max_items = max_items
        self.items: Dict[str, MemoryItem] = {}
    
    def set(self, key: str, value: str, metadata: Dict = None):
        """存储"""
        self.items[key] = MemoryItem(
            id=key,
            content=value,
            metadata=metadata or {}
        )
        
        # 检查容量
        if len(self.items) > self.max_items:
            self._evict_oldest()
    
    def get(self, key: str) -> Optional[str]:
        """获取"""
        if key in self.items:
            return self.items[key].content
        return None
    
    def delete(self, key: str):
        """删除"""
        if key in self.items:
            del self.items[key]
    
    def _evict_oldest(self):
        """淘汰最旧的"""
        if not self.items:
            return
        
        oldest_key = min(self.items.keys(), 
                         key=lambda k: self.items[k].created_at)
        del self.items[oldest_key]


class MediumTermMemory:
    """中期记忆（文件）"""
    
    def __init__(self, storage_path: str = "./memory"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def save(self, key: str, value: Dict[str, Any]):
        """保存"""
        file_path = self.storage_path / f"{key}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2, default=str)
        
        logger.debug(f"中期记忆保存: {key}")
    
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """加载"""
        file_path = self.storage_path / f"{key}.json"
        if not file_path.exists():
            return None
        
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def delete(self, key: str):
        """删除"""
        file_path = self.storage_path / f"{key}.json"
        if file_path.exists():
            file_path.unlink()
    
    def list_keys(self) -> List[str]:
        """列出所有key"""
        return [f.stem for f in self.storage_path.glob("*.json")]


class LongTermMemory:
    """长期记忆（知识库）"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge-base"):
        self.kb_path = Path(knowledge_base_path)
        self.kb_path.mkdir(parents=True, exist_ok=True)
    
    def store_knowledge(self, category: str, key: str, content: str):
        """存储知识"""
        category_path = self.kb_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        file_path = category_path / f"{key}.md"
        file_path.write_text(content, encoding="utf-8")
        
        logger.info(f"知识存储: {category}/{key}")
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """搜索知识"""
        results = []
        
        for md_file in self.kb_path.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            if query.lower() in content.lower():
                results.append({
                    "path": str(md_file.relative_to(self.kb_path)),
                    "content": content[:500]  # 截取前500字符
                })
        
        return results


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, storage_path: str = "./memory"):
        self.short_term = ShortTermMemory()
        self.medium_term = MediumTermMemory(storage_path)
        self.long_term = LongTermMemory(f"{storage_path}/knowledge-base")
    
    def remember(self, key: str, value: Any, duration: str = "short"):
        """记忆"""
        if duration == "short":
            self.short_term.set(key, str(value))
        elif duration == "medium":
            self.medium_term.save(key, {"value": value})
        elif duration == "long":
            # 需要额外参数
            pass
    
    def recall(self, key: str, duration: str = "all") -> Optional[Any]:
        """回忆"""
        if duration in ["short", "all"]:
            value = self.short_term.get(key)
            if value:
                return value
        
        if duration in ["medium", "all"]:
            value = self.medium_term.load(key)
            if value:
                return value.get("value")
        
        return None
    
    def forget(self, key: str):
        """遗忘"""
        self.short_term.delete(key)
        self.medium_term.delete(key)
'''


# 导出所有模板
TEMPLATES = {
    "task_dispatcher": TASK_DISPATCHER_TEMPLATE,
    "message_bus": MESSAGE_BUS_TEMPLATE,
    "state_machine": STATE_MACHINE_TEMPLATE,
    "memory_manager": MEMORY_MANAGER_TEMPLATE,
}


def get_template(name: str) -> str:
    """获取模板"""
    return TEMPLATES.get(name, "")


def list_templates() -> List[str]:
    """列出所有模板"""
    return list(TEMPLATES.keys())


if __name__ == "__main__":
    print("可用模板:")
    for name in list_templates():
        print(f"  - {name}")