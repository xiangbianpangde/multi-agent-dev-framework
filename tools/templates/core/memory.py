"""
记忆管理器

功能：
- 短期记忆（内存/Redis）
- 中期记忆（文件/数据库）
- 长期记忆（知识库）
- 记忆检索
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
from pathlib import Path
from collections import OrderedDict
import hashlib

logger = logging.getLogger(__name__)


class MemoryDuration(Enum):
    """记忆持续时间"""
    SHORT = "short"      # 短期（会话级）
    MEDIUM = "medium"    # 中期（项目级）
    LONG = "long"        # 长期（永久）


@dataclass
class MemoryItem:
    """记忆项"""
    id: str
    content: str
    category: str = "general"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    expires_at: Optional[datetime] = None
    importance: float = 0.5  # 0-1
    
    def access(self):
        """访问记忆"""
        self.accessed_at = datetime.now()
        self.access_count += 1
    
    def is_expired(self) -> bool:
        """是否过期"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "category": self.category,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "accessed_at": self.accessed_at.isoformat(),
            "access_count": self.access_count,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "importance": self.importance
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryItem':
        """从字典创建"""
        return cls(
            id=data.get("id", ""),
            content=data.get("content", ""),
            category=data.get("category", "general"),
            metadata=data.get("metadata", {}),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            accessed_at=datetime.fromisoformat(data["accessed_at"]) if data.get("accessed_at") else datetime.now(),
            access_count=data.get("access_count", 0),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
            importance=data.get("importance", 0.5)
        )


class ShortTermMemory:
    """短期记忆（内存LRU缓存）"""
    
    def __init__(self, max_items: int = 1000):
        self.max_items = max_items
        self.items: OrderedDict[str, MemoryItem] = OrderedDict()
    
    def set(self, key: str, value: str, metadata: Dict = None,
            ttl_seconds: int = 3600) -> str:
        """
        存储记忆
        
        Args:
            key: 键
            value: 值
            metadata: 元数据
            ttl_seconds: 有效期（秒）
            
        Returns:
            记忆ID
        """
        memory_id = self._generate_id(key)
        
        expires_at = None
        if ttl_seconds:
            expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        
        item = MemoryItem(
            id=memory_id,
            content=value,
            metadata=metadata or {},
            expires_at=expires_at
        )
        
        # 添加到缓存
        if memory_id in self.items:
            del self.items[memory_id]
        
        self.items[memory_id] = item
        
        # 检查容量，淘汰最旧的
        while len(self.items) > self.max_items:
            self.items.popitem(last=False)
        
        return memory_id
    
    def get(self, key: str) -> Optional[str]:
        """获取记忆"""
        memory_id = self._generate_id(key)
        
        if memory_id not in self.items:
            return None
        
        item = self.items[memory_id]
        
        # 检查是否过期
        if item.is_expired():
            del self.items[memory_id]
            return None
        
        # 更新访问信息，移到末尾
        item.access()
        self.items.move_to_end(memory_id)
        
        return item.content
    
    def delete(self, key: str):
        """删除记忆"""
        memory_id = self._generate_id(key)
        if memory_id in self.items:
            del self.items[memory_id]
    
    def clear(self):
        """清空记忆"""
        self.items.clear()
    
    def cleanup_expired(self) -> int:
        """清理过期记忆，返回清理数量"""
        expired = [
            k for k, v in self.items.items()
            if v.is_expired()
        ]
        for k in expired:
            del self.items[k]
        return len(expired)
    
    def _generate_id(self, key: str) -> str:
        """生成ID"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_items": len(self.items),
            "max_items": self.max_items,
            "usage_percent": len(self.items) / self.max_items * 100
        }


class MediumTermMemory:
    """中期记忆（文件存储）"""
    
    def __init__(self, storage_path: str = "./memory"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.index: Dict[str, str] = {}  # key -> file_path
        self._load_index()
    
    def _load_index(self):
        """加载索引"""
        index_file = self.storage_path / "index.json"
        if index_file.exists():
            try:
                self.index = json.loads(index_file.read_text())
            except Exception as e:
                logger.error(f"加载索引失败: {e}")
                self.index = {}
    
    def _save_index(self):
        """保存索引"""
        index_file = self.storage_path / "index.json"
        index_file.write_text(json.dumps(self.index, ensure_ascii=False, indent=2))
    
    def save(self, key: str, value: Dict[str, Any], category: str = "general"):
        """保存记忆"""
        # 分类目录
        category_path = self.storage_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        # 文件路径
        file_name = f"{self._sanitize_key(key)}.json"
        file_path = category_path / file_name
        
        # 添加元数据
        value["_metadata"] = {
            "key": key,
            "category": category,
            "saved_at": datetime.now().isoformat()
        }
        
        # 写入文件
        file_path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8"
        )
        
        # 更新索引
        self.index[key] = str(file_path.relative_to(self.storage_path))
        self._save_index()
        
        logger.debug(f"中期记忆保存: {key}")
    
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """加载记忆"""
        if key not in self.index:
            return None
        
        file_path = self.storage_path / self.index[key]
        if not file_path.exists():
            del self.index[key]
            self._save_index()
            return None
        
        try:
            content = file_path.read_text(encoding="utf-8")
            return json.loads(content)
        except Exception as e:
            logger.error(f"加载记忆失败: {key}, 错误: {e}")
            return None
    
    def delete(self, key: str):
        """删除记忆"""
        if key not in self.index:
            return
        
        file_path = self.storage_path / self.index[key]
        if file_path.exists():
            file_path.unlink()
        
        del self.index[key]
        self._save_index()
    
    def search(self, query: str, category: str = None) -> List[Dict]:
        """搜索记忆"""
        results = []
        
        search_path = self.storage_path / category if category else self.storage_path
        
        for json_file in search_path.rglob("*.json"):
            if json_file.name == "index.json":
                continue
            
            try:
                content = json_file.read_text(encoding="utf-8")
                data = json.loads(content)
                
                # 简单文本搜索
                if query.lower() in content.lower():
                    results.append({
                        "path": str(json_file.relative_to(self.storage_path)),
                        "data": data
                    })
            except Exception:
                continue
        
        return results
    
    def list_keys(self, category: str = None) -> List[str]:
        """列出所有key"""
        if category:
            return [k for k, v in self.index.items() if v.startswith(f"{category}/")]
        return list(self.index.keys())
    
    def _sanitize_key(self, key: str) -> str:
        """清理key"""
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in key)


class LongTermMemory:
    """长期记忆（知识库）"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge-base"):
        self.kb_path = Path(knowledge_base_path)
        self.kb_path.mkdir(parents=True, exist_ok=True)
    
    def store_knowledge(self, category: str, key: str, content: str,
                        metadata: Dict = None):
        """存储知识"""
        category_path = self.kb_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        # 创建Markdown文件
        file_path = category_path / f"{self._sanitize_key(key)}.md"
        
        # 构建内容
        md_content = f"""# {key}

> 存储时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{content}

"""
        if metadata:
            md_content += f"""
---

## 元数据

```json
{json.dumps(metadata, ensure_ascii=False, indent=2)}
```
"""
        
        file_path.write_text(md_content, encoding="utf-8")
        logger.info(f"知识存储: {category}/{key}")
    
    def search(self, query: str, category: str = None) -> List[Dict[str, str]]:
        """搜索知识"""
        results = []
        
        search_path = self.kb_path / category if category else self.kb_path
        
        for md_file in search_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                if query.lower() in content.lower():
                    # 提取摘要
                    lines = content.split("\n")
                    summary = "\n".join(lines[:20])
                    
                    results.append({
                        "path": str(md_file.relative_to(self.kb_path)),
                        "title": md_file.stem,
                        "summary": summary,
                        "full_content": content
                    })
            except Exception:
                continue
        
        return results
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return [d.name for d in self.kb_path.iterdir() if d.is_dir()]
    
    def _sanitize_key(self, key: str) -> str:
        """清理key"""
        return "".join(c if c.isalnum() or c in "-_" else "_" for c in key)


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, storage_path: str = "./memory"):
        self.short_term = ShortTermMemory()
        self.medium_term = MediumTermMemory(storage_path)
        self.long_term = LongTermMemory(f"{storage_path}/knowledge-base")
    
    def remember(self, key: str, value: Any, duration: MemoryDuration = MemoryDuration.SHORT,
                 metadata: Dict = None):
        """
        记忆
        
        Args:
            key: 键
            value: 值
            duration: 持续时间
            metadata: 元数据
        """
        if duration == MemoryDuration.SHORT:
            self.short_term.set(key, str(value), metadata)
        
        elif duration == MemoryDuration.MEDIUM:
            self.medium_term.save(key, {
                "value": value,
                "metadata": metadata
            })
        
        elif duration == MemoryDuration.LONG:
            self.long_term.store_knowledge(
                category=metadata.get("category", "general") if metadata else "general",
                key=key,
                content=str(value),
                metadata=metadata
            )
    
    def recall(self, key: str, duration: MemoryDuration = None) -> Optional[Any]:
        """
        回忆
        
        Args:
            key: 键
            duration: 持续时间（None表示依次查找）
            
        Returns:
            记忆值
        """
        if duration == MemoryDuration.SHORT or duration is None:
            value = self.short_term.get(key)
            if value is not None:
                return value
        
        if duration == MemoryDuration.MEDIUM or duration is None:
            data = self.medium_term.load(key)
            if data is not None:
                return data.get("value")
        
        return None
    
    def forget(self, key: str, duration: MemoryDuration = None):
        """
        遗忘
        
        Args:
            key: 键
            duration: 持续时间（None表示全部删除）
        """
        if duration in [MemoryDuration.SHORT, None]:
            self.short_term.delete(key)
        
        if duration in [MemoryDuration.MEDIUM, None]:
            self.medium_term.delete(key)
    
    def search(self, query: str, duration: MemoryDuration = None) -> List[Dict]:
        """
        搜索记忆
        
        Args:
            query: 查询字符串
            duration: 搜索范围
            
        Returns:
            搜索结果
        """
        results = []
        
        if duration in [MemoryDuration.LONG, None]:
            results.extend(self.long_term.search(query))
        
        if duration in [MemoryDuration.MEDIUM, None]:
            results.extend(self.medium_term.search(query))
        
        return results
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "short_term": self.short_term.get_stats(),
            "medium_term": {
                "total_keys": len(self.medium_term.index)
            },
            "long_term": {
                "categories": self.long_term.get_categories()
            }
        }