"""
任务调度器

功能：
- 接收任务
- 分配给Agent
- 跟踪进度
- 处理结果
"""
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import uuid

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """任务优先级"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


@dataclass
class Task:
    """任务定义"""
    id: str = field(default_factory=lambda: f"task-{uuid.uuid4().hex[:8]}")
    name: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    assignee: Optional[str] = None
    priority: TaskPriority = TaskPriority.NORMAL
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "assignee": self.assignee,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
            "metadata": self.metadata
        }


@dataclass
class AgentInfo:
    """Agent信息"""
    id: str
    name: str
    role: str
    status: str = "idle"  # idle, busy, offline
    current_task: Optional[str] = None
    completed_tasks: int = 0
    capabilities: List[str] = field(default_factory=list)


class TaskDispatcher:
    """任务调度器"""
    
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, AgentInfo] = {}
        self.running_count = 0
        self.callbacks: Dict[str, List[Callable]] = {
            "on_task_created": [],
            "on_task_assigned": [],
            "on_task_completed": [],
            "on_task_failed": [],
        }
    
    def register_agent(self, agent: AgentInfo):
        """注册Agent"""
        self.agents[agent.id] = agent
        logger.info(f"Agent注册: {agent.id} ({agent.name})")
    
    def unregister_agent(self, agent_id: str):
        """注销Agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            logger.info(f"Agent注销: {agent_id}")
    
    def create_task(self, name: str, description: str = "", 
                    priority: TaskPriority = TaskPriority.NORMAL,
                    metadata: Dict = None) -> Task:
        """创建任务"""
        task = Task(
            name=name,
            description=description,
            priority=priority,
            metadata=metadata or {}
        )
        self.tasks[task.id] = task
        logger.info(f"任务创建: {task.id} - {name}")
        self._trigger("on_task_created", task)
        return task
    
    def submit(self, task: Task) -> str:
        """提交任务"""
        self.tasks[task.id] = task
        logger.info(f"任务提交: {task.id}")
        return task.id
    
    def dispatch(self) -> int:
        """调度任务，返回已分配的任务数"""
        # 找出待执行的任务
        pending = [
            t for t in self.tasks.values()
            if t.status == TaskStatus.PENDING
        ]
        
        if not pending:
            return 0
        
        # 按优先级排序
        pending.sort(key=lambda t: t.priority.value)
        
        assigned = 0
        for task in pending:
            if self.running_count >= self.max_concurrent:
                break
            
            if self._assign_task(task):
                self.running_count += 1
                assigned += 1
        
        return assigned
    
    def _assign_task(self, task: Task) -> bool:
        """分配任务给Agent"""
        # 找到合适的Agent
        agent = self._find_available_agent(task)
        if not agent:
            logger.debug(f"未找到可用Agent: {task.id}")
            return False
        
        # 更新状态
        task.status = TaskStatus.RUNNING
        task.assignee = agent.id
        task.started_at = datetime.now()
        
        agent.status = "busy"
        agent.current_task = task.id
        
        logger.info(f"任务分配: {task.id} -> {agent.id}")
        self._trigger("on_task_assigned", task)
        return True
    
    def _find_available_agent(self, task: Task) -> Optional[AgentInfo]:
        """找到可用的Agent"""
        for agent in self.agents.values():
            if agent.status == "idle":
                # TODO: 检查能力匹配
                return agent
        return None
    
    def complete(self, task_id: str, result: Dict[str, Any]):
        """完成任务"""
        if task_id not in self.tasks:
            logger.warning(f"任务不存在: {task_id}")
            return
        
        task = self.tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.result = result
        self.running_count -= 1
        
        # 更新Agent状态
        if task.assignee and task.assignee in self.agents:
            agent = self.agents[task.assignee]
            agent.status = "idle"
            agent.current_task = None
            agent.completed_tasks += 1
        
        logger.info(f"任务完成: {task_id}")
        self._trigger("on_task_completed", task)
    
    def fail(self, task_id: str, error: str):
        """任务失败"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        task.status = TaskStatus.FAILED
        task.error = error
        self.running_count -= 1
        
        # 更新Agent状态
        if task.assignee and task.assignee in self.agents:
            self.agents[task.assignee].status = "idle"
            self.agents[task.assignee].current_task = None
        
        logger.error(f"任务失败: {task_id}, 错误: {error}")
        self._trigger("on_task_failed", task)
    
    def cancel(self, task_id: str):
        """取消任务"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        if task.status == TaskStatus.RUNNING:
            self.running_count -= 1
            if task.assignee and task.assignee in self.agents:
                self.agents[task.assignee].status = "idle"
        
        task.status = TaskStatus.CANCELLED
        logger.info(f"任务取消: {task_id}")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def list_tasks(self, status: TaskStatus = None) -> List[Task]:
        """列出任务"""
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return tasks
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_tasks": len(self.tasks),
            "pending": len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING]),
            "running": len([t for t in self.tasks.values() if t.status == TaskStatus.RUNNING]),
            "completed": len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]),
            "failed": len([t for t in self.tasks.values() if t.status == TaskStatus.FAILED]),
            "total_agents": len(self.agents),
            "idle_agents": len([a for a in self.agents.values() if a.status == "idle"]),
            "busy_agents": len([a for a in self.agents.values() if a.status == "busy"]),
        }
    
    def on(self, event: str, callback: Callable):
        """注册事件回调"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    def _trigger(self, event: str, task: Task):
        """触发事件"""
        for callback in self.callbacks.get(event, []):
            try:
                callback(task)
            except Exception as e:
                logger.error(f"回调执行失败: {e}")