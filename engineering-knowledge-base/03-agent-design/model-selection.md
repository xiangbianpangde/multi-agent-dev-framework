# 模型选择指南

> **版本**: 1.0.0
> **用途**: 多Agent项目开发的模型选择建议

---

## 一、模型能力对比

### 1.1 综合能力

| 模型 | 推理能力 | 代码能力 | 长文本 | 中文 | 速度 | 成本 |
|------|----------|----------|--------|------|------|------|
| GPT-4 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | 高 |
| Claude-3 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | 高 |
| Gemini Pro | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 中 |
| Gemini Flash | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 低 |
| Qwen | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中 |
| Kimi | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中 |
| 文心 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中 |
| 通义 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中 |
| MiniMax | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中 |
| GLM-4 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中 |

### 1.2 上下文窗口

| 模型 | 上下文长度 | 适用场景 |
|------|------------|----------|
| GPT-4 Turbo | 128K | 长文档分析 |
| Claude-3 | 200K | 超长文档 |
| Gemini Pro | 1M | 海量上下文 |
| Kimi | 200K | 长对话 |
| GLM-4 | 128K | 长文档 |

---

## 二、按任务选择

### 2.1 架构设计

```yaml
推荐模型:
  primary: GPT-4 / Claude-3
  fallback: Gemini Pro / Qwen
  
原因:
  - 需要强推理能力
  - 需要综合考虑多因素
  - 决策影响范围大
  
示例任务:
  - 系统架构设计
  - 技术选型决策
  - 模块划分
```

### 2.2 代码开发

```yaml
推荐模型:
  primary: GPT-4 / Claude-3 / Qwen
  fallback: Gemini Pro
  
原因:
  - 需要代码生成能力
  - 需要理解代码逻辑
  - 需要调试能力
  
示例任务:
  - 功能开发
  - Bug修复
  - 代码重构
```

### 2.3 文档编写

```yaml
推荐模型:
  primary: Kimi / GLM-4 / MiniMax
  fallback: Qwen / 通义
  
原因:
  - 中文表达流畅
  - 结构化输出
  - 成本较低
  
示例任务:
  - 技术文档
  - API文档
  - 用户手册
```

### 2.4 安全审计

```yaml
推荐模型:
  primary: Claude-3 / GPT-4
  fallback: Gemini Pro
  
原因:
  - 需要深度推理
  - 需要识别潜在风险
  - 结果准确性要求高
  
示例任务:
  - 代码安全审查
  - 漏洞分析
  - 合规检查
```

### 2.5 快速响应

```yaml
推荐模型:
  primary: Gemini Flash
  fallback: GLM-4
  
原因:
  - 响应速度快
  - 成本低
  - 适合简单任务
  
示例任务:
  - 简单问答
  - 信息提取
  - 格式转换
```

---

## 三、按Agent角色选择

### 3.1 中书省

```yaml
角色: 决策调度
任务类型:
  - 需求分析
  - 架构设计
  - 任务分解

模型选择:
  primary: GPT-4
  fallback: Claude-3
  
配置:
  temperature: 0.7  # 保持一定创造性
  max_tokens: 4096
  
原因:
  - 决策需要强推理
  - 规划需要全局视角
  - 错误代价高
```

### 3.2 门下省

```yaml
角色: 监察审核
任务类型:
  - 方案审核
  - 质量把控
  - 风险识别

模型选择:
  primary: Claude-3
  fallback: GPT-4
  
配置:
  temperature: 0.3  # 更严谨
  max_tokens: 4096
  
原因:
  - 审核需要严谨
  - 需要识别问题
  - 可靠性要求高
```

### 3.3 尚书省

```yaml
角色: 任务派发协调
任务类型:
  - 任务调度
  - 进度跟踪
  - 结果汇总

模型选择:
  primary: Gemini Pro
  fallback: Qwen
  
配置:
  temperature: 0.5
  max_tokens: 2048
  
原因:
  - 需要理解任务上下文
  - 需要协调能力
  - 中等复杂度
```

### 3.4 六部

```yaml
兵部 (代码开发):
  primary: Qwen / GPT-4
  reason: 代码能力强

礼部 (文档管理):
  primary: Kimi / GLM-4
  reason: 中文能力强，长文本

户部 (数据管理):
  primary: GPT-4 / Gemini Pro
  reason: 数据处理能力

刑部 (安全审计):
  primary: Claude-3
  reason: 安全审查严谨

工部 (运维部署):
  primary: Qwen / Gemini Pro
  reason: 配置生成

吏部 (人事管理):
  primary: Gemini Pro
  reason: 任务分配
```

---

## 四、成本优化

### 4.1 成本对比

| 模型 | 输入($/1K tokens) | 输出($/1K tokens) | 相对成本 |
|------|-------------------|-------------------|----------|
| GPT-4 | $0.03 | $0.06 | 基准 |
| Claude-3 | $0.015 | $0.075 | 约1.2x |
| Gemini Pro | $0.00125 | $0.005 | 约0.1x |
| Gemini Flash | $0.000075 | $0.0003 | 约0.01x |
| Qwen | ¥0.008 | ¥0.008 | 约0.05x |
| GLM-4 | ¥0.1 | ¥0.1 | 约0.5x |
| MiniMax | ¥0.03 | ¥0.03 | 约0.2x |

### 4.2 优化策略

```
┌─────────────────────────────────────────────────────────────┐
│ 成本优化策略                                                │
├─────────────────────────────────────────────────────────────┤
│ 1. 任务分级                                                 │
│    - 关键任务: 高性能模型                                   │
│    - 普通任务: 中等模型                                     │
│    - 简单任务: 轻量模型                                     │
│                                                             │
│ 2. 缓存复用                                                 │
│    - 相似请求复用结果                                       │
│    - 减少重复调用                                           │
│                                                             │
│ 3. 提示优化                                                 │
│    - 精简提示词                                             │
│    - 减少无效token                                          │
│                                                             │
│ 4. 批量处理                                                 │
│    - 合并相似请求                                           │
│    - 减少请求次数                                           │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 分级配置

```json
{
  "model_tiers": {
    "critical": {
      "models": ["gpt-4", "claude-3"],
      "use_cases": ["架构设计", "安全审计", "关键决策"]
    },
    "standard": {
      "models": ["gemini-pro", "qwen", "glm-4"],
      "use_cases": ["代码开发", "文档编写", "任务调度"]
    },
    "economy": {
      "models": ["gemini-flash", "minimax"],
      "use_cases": ["简单问答", "格式转换", "信息提取"]
    }
  }
}
```

---

## 五、切换策略

### 5.1 自动切换

```python
class ModelSelector:
    """模型选择器"""
    
    def __init__(self, config: dict):
        self.config = config
        self.primary = config["primary"]
        self.fallback = config["fallback"]
        self.failure_count = 0
        self.max_failures = 3
    
    def get_model(self, task_type: str, complexity: str) -> str:
        """获取合适的模型"""
        # 根据复杂度选择层级
        tier = self._get_tier(complexity)
        
        # 检查主模型是否可用
        if self._is_available(self.primary):
            return self.primary
        
        # 使用备用模型
        return self.fallback
    
    def _get_tier(self, complexity: str) -> str:
        """获取模型层级"""
        tiers = {
            "high": "critical",
            "medium": "standard", 
            "low": "economy"
        }
        return tiers.get(complexity, "standard")
    
    def _is_available(self, model: str) -> bool:
        """检查模型是否可用"""
        if self.failure_count >= self.max_failures:
            return False
        return True
    
    def report_failure(self, model: str):
        """报告模型失败"""
        self.failure_count += 1
        if self.failure_count >= self.max_failures:
            # 切换到备用模型
            self.primary, self.fallback = self.fallback, self.primary
            self.failure_count = 0
```

### 5.2 手动切换

```bash
# 通过配置文件切换
# config/models.json
{
  "agents": {
    "zhongshu": {
      "model": "gpt-4"  # 修改这里
    }
  }
}

# 通过API切换
curl -X POST http://localhost:7891/api/model/switch \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "zhongshu",
    "model": "claude-3"
  }'
```

---

## 六、性能监控

### 6.1 监控指标

```yaml
监控指标:
  - 响应时间
  - 成功率
  - Token消耗
  - 错误类型
  - 成本

告警规则:
  - 响应时间 > 30s
  - 成功率 < 95%
  - Token消耗异常
  - 错误率突增
```

### 6.2 日志记录

```python
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ModelCallLog:
    """模型调用日志"""
    timestamp: datetime
    model: str
    agent: str
    task: str
    input_tokens: int
    output_tokens: int
    duration_ms: int
    success: bool
    error: str = None

class ModelLogger:
    """模型调用日志记录器"""
    
    def log_call(self, log: ModelCallLog):
        """记录调用日志"""
        # 写入文件/数据库
        pass
    
    def get_stats(self, model: str, period: str) -> dict:
        """获取统计数据"""
        return {
            "total_calls": 0,
            "success_rate": 0,
            "avg_duration": 0,
            "total_tokens": 0,
            "estimated_cost": 0
        }
```

---

## 七、最佳实践

### 7.1 选择原则

```
1. 任务优先
   - 根据任务需求选择模型
   - 不是越强越好

2. 成本平衡
   - 关键任务用强模型
   - 普通任务用中模型
   - 简单任务用轻模型

3. 备用机制
   - 始终配置fallback
   - 自动切换失败模型

4. 持续优化
   - 监控模型表现
   - 定期评估调整
```

### 7.2 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 响应慢 | 模型负载高 | 切换到轻量模型 |
| 成本高 | 使用强模型过多 | 分级使用 |
| 质量差 | 模型能力不足 | 升级模型 |
| 频繁失败 | 模型不稳定 | 配置fallback |

---

*最后更新: 2026-03-24*