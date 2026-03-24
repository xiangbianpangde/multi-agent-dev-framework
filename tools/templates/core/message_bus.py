"""
消息总线

功能：
- Agent间消息传递
- 消息路由
- 消息过滤
- 权限控制
"""
from typing import Dict, Any, List, Callable, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import asyncio
import uuid
from collections import defaultdict

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """消息类型"""
    TASK = "task"                    # 任务消息
    NOTIFICATION = "notification"    # 通知消息
    QUERY = "query"                  # 查询消息
    RESPONSE = "response"            # 响应消息
    ERROR = "error"                  # 错误消息
    CONTROL = "control"              # 控制消息
    HEARTBEAT = "heartbeat"          # 心跳消息


class MessagePriority(Enum):
    """消息优先级"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


@dataclass
class Message:
    """消息定义"""
    id: str = field(default_factory=lambda: f"msg-{uuid.uuid4().hex[:8]}")
    sender: str = ""
    receiver: str = ""
    type: MessageType = MessageType.NOTIFICATION
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    priority: MessagePriority = MessagePriority.NORMAL
    requires_reply: bool = False
    reply_to: Optional[str] = None
    ttl: int = 3600  # 消息有效期（秒）
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "requires_reply": self.requires_reply,
            "reply_to": self.reply_to,
            "ttl": self.ttl,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Message':
        """从字典创建"""
        return cls(
            id=data.get("id", ""),
            sender=data.get("sender", ""),
            receiver=data.get("receiver", ""),
            type=MessageType(data.get("type", "notification")),
            content=data.get("content", {}),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else datetime.now(),
            priority=MessagePriority(data.get("priority", 3)),
            requires_reply=data.get("requires_reply", False),
            reply_to=data.get("reply_to"),
            ttl=data.get("ttl", 3600),
            metadata=data.get("metadata", {})
        )


@dataclass
class AgentEndpoint:
    """Agent端点"""
    agent_id: str
    callback: Callable
    subscriptions: Set[MessageType] = field(default_factory=set)
    status: str = "online"  # online, offline, busy


class MessageBus:
    """消息总线"""
    
    def __init__(self):
        self.endpoints: Dict[str, AgentEndpoint] = {}
        self.permission_matrix: Dict[str, Set[str]] = {}  # sender -> allowed_receivers
        self.message_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.message_history: List[Message] = []
        self.max_history = 1000
        self._running = False
    
    def register(self, agent_id: str, callback: Callable,
                 subscriptions: List[MessageType] = None):
        """
        注册Agent
        
        Args:
            agent_id: Agent ID
            callback: 消息回调函数
            subscriptions: 订阅的消息类型
        """
        endpoint = AgentEndpoint(
            agent_id=agent_id,
            callback=callback,
            subscriptions=set(subscriptions) if subscriptions else set()
        )
        self.endpoints[agent_id] = endpoint
        logger.info(f"Agent注册到消息总线: {agent_id}")
    
    def unregister(self, agent_id: str):
        """注销Agent"""
        if agent_id in self.endpoints:
            del self.endpoints[agent_id]
            logger.info(f"Agent从消息总线注销: {agent_id}")
    
    def set_permissions(self, sender: str, allowed_receivers: List[str]):
        """
        设置发送权限
        
        Args:
            sender: 发送者ID
            allowed_receivers: 允许发送的接收者列表
        """
        self.permission_matrix[sender] = set(allowed_receivers)
    
    def can_send(self, sender: str, receiver: str) -> bool:
        """检查发送权限"""
        # 广播消息总是允许
        if receiver == "*":
            return True
        
        if sender not in self.permission_matrix:
            return False
        
        return receiver in self.permission_matrix[sender]
    
    async def send(self, message: Message) -> bool:
        """
        发送消息
        
        Args:
            message: 消息对象
            
        Returns:
            是否发送成功
        """
        # 检查权限
        if not self.can_send(message.sender, message.receiver):
            logger.warning(
                f"消息发送被拒绝: {message.sender} -> {message.receiver} (无权限)"
            )
            return False
        
        # 检查接收者是否存在
        if message.receiver != "*" and message.receiver not in self.endpoints:
            logger.warning(f"接收者不存在: {message.receiver}")
            return False
        
        # 加入优先级队列
        await self.message_queue.put((message.priority.value, message))
        
        # 记录历史
        self.message_history.append(message)
        if len(self.message_history) > self.max_history:
            self.message_history.pop(0)
        
        logger.debug(f"消息入队: {message.id} ({message.sender} -> {message.receiver})")
        return True
    
    async def send_and_wait(self, message: Message, timeout: float = 30.0) -> Optional[Message]:
        """
        发送消息并等待响应
        
        Args:
            message: 消息对象
            timeout: 超时时间（秒）
            
        Returns:
            响应消息，超时返回None
        """
        message.requires_reply = True
        
        # 创建等待事件
        reply_event = asyncio.Event()
        reply_message = None
        
        async def reply_callback(msg: Message):
            nonlocal reply_message
            if msg.reply_to == message.id:
                reply_message = msg
                reply_event.set()
        
        # 临时注册回调
        original_callback = None
        if message.sender in self.endpoints:
            original_callback = self.endpoints[message.sender].callback
            self.endpoints[message.sender].callback = reply_callback
        
        # 发送消息
        await self.send(message)
        
        # 等待响应
        try:
            await asyncio.wait_for(reply_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            logger.warning(f"消息等待超时: {message.id}")
            reply_message = None
        finally:
            # 恢复原回调
            if original_callback and message.sender in self.endpoints:
                self.endpoints[message.sender].callback = original_callback
        
        return reply_message
    
    async def broadcast(self, sender: str, message_type: MessageType,
                        content: Dict[str, Any]) -> int:
        """
        广播消息
        
        Args:
            sender: 发送者
            message_type: 消息类型
            content: 消息内容
            
        Returns:
            成功发送的数量
        """
        sent = 0
        for receiver in self.endpoints:
            if receiver != sender and self.can_send(sender, receiver):
                message = Message(
                    sender=sender,
                    receiver=receiver,
                    type=message_type,
                    content=content
                )
                if await self.send(message):
                    sent += 1
        return sent
    
    async def process(self):
        """处理消息队列"""
        self._running = True
        
        while self._running:
            try:
                # 从队列获取消息
                priority, message = await asyncio.wait_for(
                    self.message_queue.get(),
                    timeout=1.0
                )
                
                # 路由消息
                await self._route_message(message)
                
                self.message_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"消息处理错误: {e}")
    
    async def _route_message(self, message: Message):
        """路由消息到接收者"""
        if message.receiver == "*":
            # 广播
            for endpoint in self.endpoints.values():
                if endpoint.agent_id != message.sender:
                    await self._deliver(endpoint, message)
        else:
            # 单播
            if message.receiver in self.endpoints:
                endpoint = self.endpoints[message.receiver]
                await self._deliver(endpoint, message)
    
    async def _deliver(self, endpoint: AgentEndpoint, message: Message):
        """投递消息"""
        # 检查订阅
        if endpoint.subscriptions and message.type not in endpoint.subscriptions:
            return
        
        try:
            # 调用回调
            if asyncio.iscoroutinefunction(endpoint.callback):
                await endpoint.callback(message)
            else:
                endpoint.callback(message)
            
            logger.debug(f"消息投递成功: {message.id} -> {endpoint.agent_id}")
            
        except Exception as e:
            logger.error(f"消息投递失败: {message.id} -> {endpoint.agent_id}, 错误: {e}")
    
    def stop(self):
        """停止处理"""
        self._running = False
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "registered_agents": len(self.endpoints),
            "queue_size": self.message_queue.qsize(),
            "history_size": len(self.message_history),
            "permission_rules": len(self.permission_matrix)
        }
    
    def get_history(self, agent_id: str = None, limit: int = 100) -> List[Dict]:
        """获取消息历史"""
        history = self.message_history[-limit:]
        
        if agent_id:
            history = [
                msg for msg in history
                if msg.sender == agent_id or msg.receiver == agent_id
            ]
        
        return [msg.to_dict() for msg in history]


# 消息构建器
class MessageBuilder:
    """消息构建器"""
    
    def __init__(self):
        self._sender = ""
        self._receiver = ""
        self._type = MessageType.NOTIFICATION
        self._content = {}
        self._priority = MessagePriority.NORMAL
        self._requires_reply = False
        self._reply_to = None
    
    def from_agent(self, agent_id: str) -> 'MessageBuilder':
        self._sender = agent_id
        return self
    
    def to_agent(self, agent_id: str) -> 'MessageBuilder':
        self._receiver = agent_id
        return self
    
    def with_type(self, msg_type: MessageType) -> 'MessageBuilder':
        self._type = msg_type
        return self
    
    def with_content(self, content: Dict) -> 'MessageBuilder':
        self._content = content
        return self
    
    def with_priority(self, priority: MessagePriority) -> 'MessageBuilder':
        self._priority = priority
        return self
    
    def requires_reply(self, requires: bool = True) -> 'MessageBuilder':
        self._requires_reply = requires
        return self
    
    def reply_to_msg(self, message_id: str) -> 'MessageBuilder':
        self._reply_to = message_id
        return self
    
    def build(self) -> Message:
        return Message(
            sender=self._sender,
            receiver=self._receiver,
            type=self._type,
            content=self._content,
            priority=self._priority,
            requires_reply=self._requires_reply,
            reply_to=self._reply_to
        )