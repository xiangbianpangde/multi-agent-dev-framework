# 问题处理规范

> **版本**: 1.0.0
> **用途**: 多Agent项目开发过程中的问题处理指南

---

## 一、问题分类

### 1.1 按严重程度

| 级别 | 名称 | 定义 | 处理时限 |
|------|------|------|----------|
| P0 | 致命 | 系统无法运行 | 立即 |
| P1 | 严重 | 核心功能不可用 | 1小时 |
| P2 | 一般 | 部分功能受影响 | 4小时 |
| P3 | 轻微 | 非核心问题 | 24小时 |
| P4 | 建议 | 优化建议 | 视情况 |

### 1.2 按类型

```
问题类型:
├── 技术问题
│   ├── 代码错误
│   ├── 配置错误
│   ├── 依赖问题
│   └── 性能问题
│
├── 流程问题
│   ├── 任务阻塞
│   ├── 状态异常
│   ├── 权限问题
│   └── 沟通问题
│
├── 资源问题
│   ├── 模型限制
│   ├── 存储不足
│   ├── 网络问题
│   └── 超时问题
│
└── 需求问题
    ├── 需求不清
    ├── 需求变更
    └── 需求冲突
```

---

## 二、问题发现

### 2.1 自动检测

```python
class ProblemDetector:
    """问题检测器"""
    
    def detect(self, context: dict) -> List[Problem]:
        """检测问题"""
        problems = []
        
        # 检测超时
        if self._check_timeout(context):
            problems.append(Problem(
                level="P1",
                type="timeout",
                message="任务执行超时"
            ))
        
        # 检测错误
        if self._check_errors(context):
            problems.append(Problem(
                level="P1",
                type="error",
                message="执行错误"
            ))
        
        # 检测阻塞
        if self._check_block(context):
            problems.append(Problem(
                level="P2",
                type="block",
                message="任务被阻塞"
            ))
        
        return problems
```

### 2.2 人工报告

```markdown
# 问题报告模板

## 基本信息
- 报告人: [姓名/Agent]
- 时间: [YYYY-MM-DD HH:MM]
- 项目: [项目名称]

## 问题描述
- 类型: [技术/流程/资源/需求]
- 级别: [P0-P4]
- 摘要: [一句话描述]

## 详细信息
- 复现步骤:
  1. ...
  2. ...
- 预期结果: ...
- 实际结果: ...
- 错误信息: ...
- 日志/截图: [附件]

## 影响范围
- 影响功能: ...
- 影响用户: ...

## 建议方案
[如果有建议]
```

---

## 三、问题处理流程

### 3.1 标准流程

```
问题发现
    │
    ▼
┌─────────────────┐
│ 问题登记       │
│ - 记录信息     │
│ - 分配编号     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 问题评估       │
│ - 确定级别     │
│ - 确定类型     │
│ - 分配责任人   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 问题分析       │
│ - 定位原因     │
│ - 评估影响     │
│ - 制定方案     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 问题解决       │
│ - 执行方案     │
│ - 验证效果     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 问题关闭       │
│ - 记录总结     │
│ - 更新文档     │
└─────────────────┘
```

### 3.2 紧急流程

```
P0/P1问题快速处理:

发现问题 → 立即通知 → 快速止血 → 根因分析 → 彻底修复

1. 立即通知
   - 通知相关负责人
   - 必要时升级

2. 快速止血
   - 回滚/重启
   - 熔断/降级
   - 临时方案

3. 根因分析
   - 收集日志
   - 分析原因
   - 制定方案

4. 彻底修复
   - 实施修复
   - 测试验证
   - 部署上线
```

---

## 四、常见问题处理

### 4.1 网络受限环境

```bash
# 问题: 无法访问外部资源

解决方案:

1. 使用代理
ssh -f -N -D 1080 -p 5522 user@proxy_server
curl --socks5 localhost:1080 URL

2. 配置镜像源
pip config set global.index-url https://mirrors.xxx.com/pypi/simple

3. 离线安装
pip download -d ./packages package_name
pip install --no-index --find-links=./packages package_name

4. 本地缓存
# 使用缓存的依赖
pip install --no-index --find-links=./cache package_name
```

### 4.2 端口冲突

```bash
# 问题: 端口被占用

解决步骤:

1. 检查端口占用
ss -tlnp | grep PORT
lsof -i :PORT

2. 停止冲突服务
kill -9 PID
systemctl stop service_name

3. 修改配置
# 修改应用端口
PORT=8080

4. 使用不同端口
python server.py --port 8081
```

### 4.3 依赖问题

```bash
# 问题: 依赖版本冲突

解决步骤:

1. 查看错误日志
pip install package_name -v

2. 检查依赖树
pipdeptree

3. 解决方案
# 方案1: 指定版本
pip install package_name==1.2.3

# 方案2: 使用虚拟环境
python -m venv venv
source venv/bin/activate

# 方案3: 使用poetry
poetry install
```

### 4.4 内存不足

```bash
# 问题: 内存不足导致OOM

解决步骤:

1. 检查内存使用
free -h
top

2. 释放内存
# 清理缓存
sync && echo 3 > /proc/sys/vm/drop_caches

3. 调整配置
# 减少并发数
MAX_WORKERS=2

# 限制内存
ulimit -v 4194304

4. 增加swap
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

### 4.5 任务超时

```python
# 问题: 任务执行超时

class TimeoutHandler:
    """超时处理器"""
    
    def handle_timeout(self, task_id: str):
        """处理超时"""
        # 1. 记录超时
        logger.warning(f"任务超时: {task_id}")
        
        # 2. 检查任务状态
        task = self.get_task(task_id)
        
        # 3. 尝试恢复
        if self._can_retry(task):
            self._retry_task(task)
        else:
            self._notify_manual_intervention(task)
    
    def _can_retry(self, task) -> bool:
        """是否可以重试"""
        return task.retry_count < task.max_retries
    
    def _retry_task(self, task):
        """重试任务"""
        task.retry_count += 1
        self.dispatcher.redispatch(task)
```

### 4.6 模型调用失败

```python
# 问题: LLM调用失败

class ModelFailureHandler:
    """模型失败处理器"""
    
    def handle_failure(self, error: Exception):
        """处理模型失败"""
        # 1. 识别错误类型
        if isinstance(error, RateLimitError):
            return self._handle_rate_limit(error)
        elif isinstance(error, TimeoutError):
            return self._handle_timeout(error)
        elif isinstance(error, AuthenticationError):
            return self._handle_auth_error(error)
        else:
            return self._handle_unknown_error(error)
    
    def _handle_rate_limit(self, error):
        """处理限流"""
        # 等待后重试
        wait_time = error.retry_after or 60
        time.sleep(wait_time)
        return "retry"
    
    def _handle_timeout(self, error):
        """处理超时"""
        # 切换到备用模型
        self.model_selector.switch_to_fallback()
        return "retry"
    
    def _handle_auth_error(self, error):
        """处理认证错误"""
        # 通知人工
        return "manual"
```

---

## 五、问题升级

### 5.1 升级条件

```
升级条件:
├── 技术层面
│   ├── 超过处理时限未解决
│   ├── 尝试3次仍未解决
│   ├── 需要更高权限
│   └── 需要外部资源
│
├── 影响层面
│   ├── 影响范围扩大
│   ├── 影响核心功能
│   └── 影响多个项目
│
└── 决策层面
    ├── 方案有争议
    ├── 需求不明确
    └── 重大变更
```

### 5.2 升级路径

```
升级路径:

技术问题:
执行者 → 部门负责人 → 中书省 → 人工

流程问题:
执行者 → 尚书省 → 门下省 → 人工

需求问题:
执行者 → 中书省 → 用户
```

---

## 六、问题记录

### 6.1 记录格式

```json
{
  "problem_id": "PROB-20260324-001",
  "timestamp": "2026-03-24T10:30:00",
  "reporter": "bingbu",
  "type": "technical",
  "level": "P2",
  "title": "数据库连接超时",
  "description": "高峰期数据库连接池耗尽",
  "status": "resolved",
  "assignee": "gongbu",
  "root_cause": "连接池配置过小",
  "solution": "增加连接池大小到100",
  "resolution_time": "2026-03-24T11:00:00",
  "lessons_learned": "需要根据负载调整连接池配置"
}
```

### 6.2 知识沉淀

```markdown
# 问题知识库

## 常见问题FAQ

### Q1: 数据库连接超时
**现象**: 高峰期出现连接超时
**原因**: 连接池配置过小
**解决**: 增加连接池大小

### Q2: 任务调度卡住
**现象**: 任务长时间处于pending状态
**原因**: 调度器异常
**解决**: 重启调度器

## 经验教训

### 2026-03-24 数据库连接问题
- 问题: 连接池耗尽
- 影响: 服务不可用30分钟
- 教训: 需要监控连接池使用率

## 最佳实践

- 定期检查资源使用
- 设置合理告警阈值
- 保持配置文档更新
```

---

## 七、预防措施

### 7.1 监控预警

```yaml
监控配置:
  资源监控:
    - CPU使用率 > 80%
    - 内存使用率 > 85%
    - 磁盘使用率 > 90%
  
  性能监控:
    - 响应时间 > 5s
    - 错误率 > 1%
    - 任务积压 > 100
  
  业务监控:
    - 任务成功率 < 95%
    - 审核通过率 < 80%
    - 用户满意度 < 4.0
```

### 7.2 检查清单

```markdown
# 部署前检查

## 功能检查
- [ ] 核心功能测试通过
- [ ] 边界条件测试通过
- [ ] 异常处理测试通过

## 性能检查
- [ ] 压力测试通过
- [ ] 内存泄漏检查
- [ ] 资源限制配置

## 安全检查
- [ ] 敏感信息检查
- [ ] 权限验证检查
- [ ] 输入验证检查

## 配置检查
- [ ] 环境变量配置
- [ ] 日志配置
- [ ] 监控配置
```

---

*最后更新: 2026-03-24*