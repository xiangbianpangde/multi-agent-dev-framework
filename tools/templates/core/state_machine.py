"""
任务状态机

功能：
- 状态定义
- 状态转换
- 状态验证
- 历史记录
"""
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class TaskState(Enum):
    """任务状态枚举"""
    DRAFT = "draft"                    # 草稿
    PLANNING = "planning"              # 规划中
    REVIEW = "review"                  # 审核中
    REJECTED = "rejected"              # 已封驳
    DISPATCHED = "dispatched"          # 已派发
    EXECUTING = "executing"            # 执行中
    CHECKING = "checking"              # 审查中
    ACCEPTED = "accepted"              # 已通过
    DONE = "done"                      # 已完成
    CANCELLED = "cancelled"            # 已取消
    BLOCKED = "blocked"                # 已阻塞


# 合法状态转换映射
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

# 状态描述
STATE_DESCRIPTIONS = {
    TaskState.DRAFT: "需求已提交，待分析",
    TaskState.PLANNING: "中书省正在设计方案",
    TaskState.REVIEW: "门下省正在审核",
    TaskState.REJECTED: "门下省驳回，需重做",
    TaskState.DISPATCHED: "尚书省已派发任务",
    TaskState.EXECUTING: "六部正在执行",
    TaskState.CHECKING: "门下省正在验收",
    TaskState.ACCEPTED: "验收通过",
    TaskState.DONE: "任务完成",
    TaskState.CANCELLED: "任务被取消",
    TaskState.BLOCKED: "任务被阻塞",
}


@dataclass
class StateRecord:
    """状态记录"""
    state: TaskState
    timestamp: datetime
    reason: str = ""
    operator: str = ""
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "state": self.state.value,
            "timestamp": self.timestamp.isoformat(),
            "reason": self.reason,
            "operator": self.operator
        }


class InvalidTransitionError(Exception):
    """非法状态转换异常"""
    pass


class StateMachine:
    """任务状态机"""
    
    def __init__(self, initial_state: TaskState = TaskState.DRAFT):
        self.current_state = initial_state
        self.history: List[StateRecord] = [
            StateRecord(
                state=initial_state,
                timestamp=datetime.now(),
                reason="初始化"
            )
        ]
        self._observers: List[callable] = []
    
    def can_transition_to(self, target: TaskState) -> bool:
        """
        检查是否可以转换到目标状态
        
        Args:
            target: 目标状态
            
        Returns:
            是否可以转换
        """
        allowed = VALID_TRANSITIONS.get(self.current_state, [])
        return target in allowed
    
    def transition(self, target: TaskState, reason: str = "", 
                   operator: str = "") -> bool:
        """
        执行状态转换
        
        Args:
            target: 目标状态
            reason: 转换原因
            operator: 操作者
            
        Returns:
            是否转换成功
            
        Raises:
            InvalidTransitionError: 非法转换时抛出
        """
        if not self.can_transition_to(target):
            raise InvalidTransitionError(
                f"不能从 {self.current_state.value} 转换到 {target.value}"
            )
        
        old_state = self.current_state
        self.current_state = target
        
        # 记录历史
        record = StateRecord(
            state=target,
            timestamp=datetime.now(),
            reason=reason,
            operator=operator
        )
        self.history.append(record)
        
        # 记录日志
        logger.info(
            f"状态转换: {old_state.value} -> {target.value}, "
            f"原因: {reason}, 操作者: {operator}"
        )
        
        # 通知观察者
        self._notify_observers(old_state, target, reason)
        
        return True
    
    def force_transition(self, target: TaskState, reason: str = ""):
        """
        强制状态转换（跳过验证）
        
        仅用于管理员操作或恢复场景
        """
        old_state = self.current_state
        self.current_state = target
        self.history.append(StateRecord(
            state=target,
            timestamp=datetime.now(),
            reason=f"[强制] {reason}"
        ))
        logger.warning(f"强制状态转换: {old_state.value} -> {target.value}")
    
    def is_terminal(self) -> bool:
        """是否为终态"""
        return self.current_state in [TaskState.DONE, TaskState.CANCELLED]
    
    def is_active(self) -> bool:
        """是否为活跃状态（正在处理中）"""
        return self.current_state in [
            TaskState.PLANNING,
            TaskState.REVIEW,
            TaskState.EXECUTING,
            TaskState.CHECKING
        ]
    
    def is_blocked(self) -> bool:
        """是否被阻塞"""
        return self.current_state == TaskState.BLOCKED
    
    def get_history(self) -> List[Dict]:
        """获取状态历史"""
        return [record.to_dict() for record in self.history]
    
    def get_state_description(self) -> str:
        """获取当前状态描述"""
        return STATE_DESCRIPTIONS.get(self.current_state, "未知状态")
    
    def get_allowed_transitions(self) -> List[TaskState]:
        """获取允许的转换目标"""
        return VALID_TRANSITIONS.get(self.current_state, []).copy()
    
    def add_observer(self, callback: callable):
        """添加状态变化观察者"""
        self._observers.append(callback)
    
    def _notify_observers(self, old_state: TaskState, new_state: TaskState, 
                          reason: str):
        """通知观察者"""
        for observer in self._observers:
            try:
                observer(old_state, new_state, reason)
            except Exception as e:
                logger.error(f"观察者回调失败: {e}")
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "current_state": self.current_state.value,
            "state_description": self.get_state_description(),
            "is_terminal": self.is_terminal(),
            "is_active": self.is_active(),
            "is_blocked": self.is_blocked(),
            "allowed_transitions": [s.value for s in self.get_allowed_transitions()],
            "history": self.get_history()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StateMachine':
        """从字典恢复"""
        initial_state = TaskState(data.get("current_state", "draft"))
        sm = cls(initial_state)
        
        # 恢复历史
        sm.history = []
        for record in data.get("history", []):
            sm.history.append(StateRecord(
                state=TaskState(record["state"]),
                timestamp=datetime.fromisoformat(record["timestamp"]),
                reason=record.get("reason", ""),
                operator=record.get("operator", "")
            ))
        
        return sm


# 状态检查工具函数
def is_valid_transition(from_state: TaskState, to_state: TaskState) -> bool:
    """检查状态转换是否合法"""
    return to_state in VALID_TRANSITIONS.get(from_state, [])


def get_transition_path(from_state: TaskState, to_state: TaskState) -> List[TaskState]:
    """
    获取状态转换路径
    
    使用BFS算法找到最短转换路径
    """
    if from_state == to_state:
        return [from_state]
    
    if is_valid_transition(from_state, to_state):
        return [from_state, to_state]
    
    # BFS找路径
    from collections import deque
    
    queue = deque([(from_state, [from_state])])
    visited = {from_state}
    
    while queue:
        current, path = queue.popleft()
        
        for next_state in VALID_TRANSITIONS.get(current, []):
            if next_state == to_state:
                return path + [next_state]
            
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))
    
    return []  # 无法到达