# 代码规范

> **版本**: 1.0.0
> **用途**: 多Agent项目开发的代码编写规范

---

## 一、文件规范

### 1.1 文件头部

```python
"""
模块名称 - 简短描述

功能说明：
- 功能1
- 功能2

作者: xxx
创建时间: YYYY-MM-DD
版本: x.x.x
"""
```

### 1.2 文件命名

```
命名规则:
- 模块文件: 小写下划线 (user_service.py)
- 类文件: 大驼峰对应的下划线 (user_auth.py)
- 测试文件: test_前缀 (test_user_service.py)
- 配置文件: 小写下划线 (database_config.py)

禁止:
- 中文文件名
- 空格和特殊字符
- 过长的文件名 (>50字符)
```

### 1.3 目录结构

```
模块目录结构:
module_name/
├── __init__.py          # 模块初始化，导出公共接口
├── main.py              # 主要实现
├── models.py            # 数据模型
├── utils.py             # 工具函数
├── exceptions.py        # 自定义异常
└── tests/
    ├── __init__.py
    ├── test_main.py
    └── test_utils.py
```

---

## 二、命名规范

### 2.1 基本规则

| 类型 | 命名风格 | 示例 |
|------|----------|------|
| 模块 | 小写下划线 | `user_service` |
| 类 | 大驼峰 | `UserService` |
| 函数 | 小写下划线 | `get_user_by_id` |
| 方法 | 小写下划线 | `calculate_total` |
| 变量 | 小写下划线 | `user_count` |
| 常量 | 全大写下划线 | `MAX_RETRY_COUNT` |
| 私有属性 | 单下划线前缀 | `_internal_state` |
| 私有方法 | 单下划线前缀 | `_validate_input` |

### 2.2 命名原则

```
┌─────────────────────────────────────────────────────────────┐
│ 命名原则                                                    │
├─────────────────────────────────────────────────────────────┤
│ 1. 描述性 - 名称要表达意图                                 │
│    好: get_active_users()                                  │
│    差: get_data()                                          │
│                                                             │
│ 2. 一致性 - 同类命名风格统一                               │
│    好: user_id, order_id, product_id                       │
│    差: user_id, orderId, productID                         │
│                                                             │
│ 3. 避免缩写 - 除非是通用缩写                               │
│    好: database_connection                                 │
│    差: db_conn                                             │
│                                                             │
│ 4. 布尔值 - 使用is/has/can前缀                             │
│    好: is_active, has_permission, can_edit                 │
│    差: active, permission, edit                            │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 特殊命名

```python
# 类名：名词，表示实体
class UserAccount:
class TaskDispatcher:
class MemoryManager:

# 函数名：动词开头，表示动作
def create_user():
def delete_task():
def calculate_score():

# 返回布尔值的函数：is/has/can开头
def is_valid():
def has_permission():
def can_execute():

# 获取函数：get开头
def get_user_by_id():
def get_all_tasks():

# 设置函数：set开头
def set_user_status():
set_configuration():

# 创建函数：create开头
def create_new_task():
def create_session():

# 删除函数：delete/remove开头
def delete_user():
def remove_item():
```

---

## 三、代码风格

### 3.1 缩进与空格

```python
# 使用4个空格缩进，不用Tab
def example():
    if condition:
        do_something()

# 运算符两边加空格
result = a + b * c

# 逗号后加空格
items = [1, 2, 3]
params = (a, b, c)

# 函数参数默认值等号两边不加空格
def func(name, default=None):
    pass

# 冒号前不加空格，字典冒号后加空格
data = {"key": "value"}
```

### 3.2 行长度

```
最大行长度: 100字符

长行处理:
# 换行与缩进
result = some_function(
    param1,
    param2,
    param3
)

# 链式调用
result = (items
    .filter(active=True)
    .order_by(created_at)
    .limit(10))

# 长条件
if (user.is_active and 
    user.has_permission("admin") and
    not user.is_blocked):
    do_something()
```

### 3.3 空行规则

```python
# 模块级别：2个空行
class ClassA:
    pass


class ClassB:
    pass


# 类级别：1个空行
class Example:
    def method1(self):
        pass
    
    def method2(self):
        pass
    
    # 逻辑分组可以用额外空行
    def public_method(self):
        pass
    
    def _private_method(self):
        pass

# 函数内部：逻辑分组用空行
def process_data(data):
    # 验证
    validate_input(data)
    
    # 处理
    result = transform(data)
    
    # 返回
    return result
```

---

## 四、注释规范

### 4.1 文档字符串

```python
def process_task(task_id: str, priority: int = 3) -> TaskResult:
    """
    处理指定任务
    
    执行任务的完整处理流程，包括验证、执行和结果记录。
    
    Args:
        task_id: 任务唯一标识符
        priority: 任务优先级，范围1-5，默认为3
    
    Returns:
        TaskResult: 包含处理结果的对象
    
    Raises:
        TaskNotFoundError: 任务不存在
        TaskAlreadyRunningError: 任务已在运行中
    
    Example:
        >>> result = process_task("task-001", priority=1)
        >>> print(result.status)
        "completed"
    """
    pass


class TaskManager:
    """
    任务管理器
    
    负责任务的创建、调度、执行和监控。
    
    Attributes:
        max_tasks: 最大并发任务数
        timeout: 任务超时时间（秒）
    
    Example:
        >>> manager = TaskManager(max_tasks=10)
        >>> manager.create_task("process_data")
    """
    
    def __init__(self, max_tasks: int = 5, timeout: int = 300):
        """初始化任务管理器"""
        pass
```

### 4.2 行内注释

```python
# 好：解释为什么，而不是做什么
# 使用批量插入提高性能
batch_insert(items)

# 差：重复代码内容
# 遍历用户列表
for user in users:

# 好：解释复杂逻辑
# 使用双指针算法，时间复杂度O(n)
while left < right:
    process(left, right)

# TODO注释格式
# TODO(username): 描述待办事项
# TODO(zhangsan): 添加缓存支持
```

### 4.3 注释原则

```
┌─────────────────────────────────────────────────────────────┐
│ 注释原则                                                    │
├─────────────────────────────────────────────────────────────┤
│ 1. 解释为什么，而不是做什么                                │
│ 2. 保持注释与代码同步                                       │
│ 3. 复杂逻辑必须注释                                         │
│ 4. 公共接口必须文档化                                       │
│ 5. 避免无意义的注释                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 五、类型注解

### 5.1 基本类型

```python
from typing import List, Dict, Optional, Union, Any

# 基本类型
def func(name: str, age: int, score: float, active: bool) -> str:
    pass

# 容器类型
def get_users() -> List[str]:
    pass

def get_config() -> Dict[str, Any]:
    pass

# 可选类型
def find_user(user_id: str) -> Optional[User]:
    pass

# 联合类型
def process(data: Union[str, bytes]) -> str:
    pass
```

### 5.2 函数签名

```python
from typing import Callable, TypeVar, Generic

# 回调类型
def register_callback(callback: Callable[[str], None]) -> None:
    pass

# 泛型
T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, item: T):
        self.item = item
    
    def get(self) -> T:
        return self.item

# 自引用
class Node:
    def __init__(self, value: int, next: Optional['Node'] = None):
        self.value = value
        self.next = next
```

### 5.3 类型别名

```python
from typing import TypeAlias, NewType

# 类型别名
UserId: TypeAlias = str
TaskId: TypeAlias = str
Config: TypeAlias = Dict[str, Any]

# 新类型（更严格的类型检查）
UserName = NewType('UserName', str)
TaskPriority = NewType('TaskPriority', int)

def create_user(name: UserName) -> UserId:
    pass

# 使用
user_name = UserName("张三")
user_id = create_user(user_name)
```

---

## 六、异常处理

### 6.1 异常定义

```python
# 自定义异常基类
class AppError(Exception):
    """应用异常基类"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or "UNKNOWN_ERROR"
        super().__init__(self.message)

# 业务异常
class TaskNotFoundError(AppError):
    """任务不存在"""
    def __init__(self, task_id: str):
        super().__init__(
            message=f"任务不存在: {task_id}",
            code="TASK_NOT_FOUND"
        )

class TaskAlreadyRunningError(AppError):
    """任务已在运行"""
    def __init__(self, task_id: str):
        super().__init__(
            message=f"任务已在运行中: {task_id}",
            code="TASK_ALREADY_RUNNING"
        )
```

### 6.2 异常捕获

```python
# 好：具体异常，明确处理
try:
    result = process_task(task_id)
except TaskNotFoundError:
    logger.warning(f"任务不存在: {task_id}")
    return None
except TaskAlreadyRunningError:
    logger.info(f"任务已在运行: {task_id}")
    return get_existing_result(task_id)

# 好：捕获并重新抛出
try:
    data = fetch_data(url)
except ConnectionError as e:
    logger.error(f"连接失败: {url}, 错误: {e}")
    raise DataFetchError(f"无法获取数据: {url}") from e

# 差：捕获所有异常
try:
    do_something()
except Exception:  # 不推荐
    pass

# 差：空except
try:
    do_something()
except:  # 禁止
    pass
```

### 6.3 异常处理原则

```
┌─────────────────────────────────────────────────────────────┐
│ 异常处理原则                                                │
├─────────────────────────────────────────────────────────────┤
│ 1. 只捕获能处理的异常                                       │
│ 2. 不要吞掉异常                                             │
│ 3. 记录异常日志                                             │
│ 4. 提供有意义的错误信息                                     │
│ 5. 使用自定义异常区分错误类型                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 七、日志规范

### 7.1 日志级别

```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: 调试信息
logger.debug(f"处理用户: {user_id}, 参数: {params}")

# INFO: 正常业务信息
logger.info(f"任务创建成功: {task_id}")

# WARNING: 警告，不影响主流程
logger.warning(f"配置项缺失，使用默认值: {key}")

# ERROR: 错误，影响功能但可恢复
logger.error(f"处理失败: {error}", exc_info=True)

# CRITICAL: 严重错误，系统不稳定
logger.critical(f"数据库连接失败，服务不可用")
```

### 7.2 日志格式

```python
# 格式化配置
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 结构化日志（推荐）
def log_structured(level: str, message: str, **context):
    """结构化日志"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        "message": message,
        "context": context
    }
    print(json.dumps(log_entry))

# 使用示例
log_structured(
    "INFO",
    "任务处理完成",
    task_id="task-001",
    duration_ms=150,
    status="success"
)
```

### 7.3 敏感信息处理

```python
# 敏感字段列表
SENSITIVE_FIELDS = ["password", "token", "secret", "api_key", "credit_card"]

def mask_sensitive(data: dict) -> dict:
    """遮蔽敏感信息"""
    result = data.copy()
    for key in result:
        if any(field in key.lower() for field in SENSITIVE_FIELDS):
            result[key] = "***MASKED***"
    return result

# 日志输出前处理
logger.info(f"用户数据: {mask_sensitive(user_data)}")
```

---

## 八、测试规范

### 8.1 测试命名

```python
# 测试类命名
class TestUserService:
    pass

# 测试方法命名
def test_create_user_success():
    pass

def test_create_user_with_invalid_email():
    pass

def test_create_user_should_raise_error_when_email_exists():
    pass
```

### 8.2 测试结构

```python
import pytest

class TestTaskProcessor:
    """任务处理器测试"""
    
    @pytest.fixture
    def processor(self):
        """创建测试实例"""
        return TaskProcessor()
    
    @pytest.fixture
    def sample_task(self):
        """创建测试数据"""
        return Task(id="test-001", name="测试任务")
    
    def test_process_task_success(self, processor, sample_task):
        """测试正常处理"""
        # Arrange
        expected_status = "completed"
        
        # Act
        result = processor.process(sample_task)
        
        # Assert
        assert result.status == expected_status
        assert result.error is None
    
    def test_process_task_with_invalid_input(self, processor):
        """测试无效输入"""
        with pytest.raises(ValidationError):
            processor.process(None)
```

### 8.3 测试覆盖率

```
覆盖率要求:
- 核心模块: > 90%
- 业务模块: > 80%
- 工具模块: > 70%
- 整体项目: > 80%

运行覆盖率:
pytest --cov=modules --cov-report=html
```

---

## 九、代码检查

### 9.1 工具配置

```toml
# pyproject.toml

[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311']

[tool.isort]
profile = "black"
line_length = 100

[tool.pylint]
max-line-length = 100
disable = ["C0114", "C0115", "C0116"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
```

### 9.2 检查命令

```bash
# 格式化
black .
isort .

# 静态检查
pylint modules/
mypy modules/

# 测试
pytest tests/

# 覆盖率
pytest --cov=modules --cov-report=html

# 安全检查
bandit -r modules/
safety check
```

---

*最后更新: 2026-03-24*