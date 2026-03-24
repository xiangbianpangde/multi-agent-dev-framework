# Skills设计规范

> **版本**: 1.0.0
> **用途**: Agent技能模块的设计与开发规范

---

## 一、Skill概述

### 1.1 定义

Skill是Agent的可插拔能力模块，用于扩展Agent的功能。

```
┌─────────────────────────────────────────────────────────────┐
│ Agent + Skills                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Agent   │───→│  Skill   │───→│  Output  │              │
│  │ (角色)   │    │ (能力)   │    │ (结果)   │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                                              │
│  Agent = 人格 + 职责 + 权限                                  │
│  Skill = 具体能力 + 实现逻辑                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 设计原则

```
原则:
1. 单一能力 - 每个Skill只做一件事
2. 可复用 - Skill可被多个Agent使用
3. 可配置 - 行为可通过参数调整
4. 可测试 - 有明确的测试方法
5. 可文档 - 有清晰的使用说明
```

---

## 二、目录结构

### 2.1 标准结构

```
skills/
└── skill_name/
    ├── SKILL.md              # 必需：技能说明
    ├── QUICKREF.md           # 可选：快速参考
    ├── src/
    │   ├── __init__.py
    │   └── main.py           # 主要实现
    ├── tests/
    │   ├── __init__.py
    │   └── test_main.py
    ├── examples/
    │   └── example_usage.py
    └── requirements.txt      # 可选：额外依赖
```

### 2.2 目录说明

| 文件/目录 | 必需 | 说明 |
|-----------|------|------|
| SKILL.md | ✅ | 技能说明文档 |
| QUICKREF.md | ⬜ | 快速参考卡片 |
| src/ | ✅ | 源代码目录 |
| tests/ | ⬜ | 测试代码 |
| examples/ | ⬜ | 使用示例 |
| requirements.txt | ⬜ | 额外依赖 |

---

## 三、SKILL.md格式

### 3.1 标准模板

```markdown
# [Skill名称]

> 一句话描述功能

## 功能说明

详细描述这个技能的功能和使用场景。

## 参数说明

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| param1 | string | 是 | - | 参数说明 |
| param2 | int | 否 | 10 | 参数说明 |

## 使用方法

### 命令行
\`\`\`bash
/skill skill_name --param1 value1 --param2 value2
\`\`\`

### API调用
\`\`\`python
from skills.skill_name import Skill

skill = Skill()
result = skill.execute(param1="value1", param2=10)
\`\`\`

## 输出格式

\`\`\`json
{
  "status": "success",
  "result": {
    "key": "value"
  }
}
\`\`\`

## 注意事项

- 注意事项1
- 注意事项2

## 示例

### 示例1：基本用法
输入：
\`\`\`
...
\`\`\`

输出：
\`\`\`
...
\`\`\`

## 更新日志

- v1.0.0 (YYYY-MM-DD): 初始版本
```

### 3.2 完整示例

```markdown
# 代码审查 (code_review)

> 自动审查代码质量，发现潜在问题

## 功能说明

代码审查技能使用静态分析和LLM结合的方式，检查代码的：
- 代码规范
- 潜在Bug
- 安全漏洞
- 性能问题

## 参数说明

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| file_path | string | 是 | - | 要审查的文件路径 |
| language | string | 否 | auto | 编程语言 |
| severity | string | 否 | all | 最低严重级别 |
| format | string | 否 | markdown | 输出格式 |

## 使用方法

### 命令行
\`\`\`bash
/skill code_review --file_path ./main.py --severity high
\`\`\`

### API调用
\`\`\`python
from skills.code_review import CodeReviewSkill

skill = CodeReviewSkill()
result = skill.execute(
    file_path="./main.py",
    severity="high"
)
\`\`\`

## 输出格式

\`\`\`json
{
  "status": "success",
  "file": "main.py",
  "issues": [
    {
      "line": 42,
      "severity": "high",
      "type": "security",
      "message": "SQL注入风险",
      "suggestion": "使用参数化查询"
    }
  ],
  "summary": {
    "total": 1,
    "high": 1,
    "medium": 0,
    "low": 0
  }
}
\`\`\`

## 注意事项

- 大文件可能需要较长处理时间
- 某些语言支持有限
- 建议在提交前运行

## 示例

### 示例1：Python代码审查
输入：
\`\`\`bash
/skill code_review --file_path ./auth.py
\`\`\`

输出：
\`\`\`markdown
# 代码审查报告

**文件**: auth.py
**审查时间**: 2026-03-24 10:30:00

## 发现问题 (2个)

### 高危 (1个)

**Line 15**: SQL注入风险
- 问题: 使用字符串拼接构造SQL
- 建议: 使用参数化查询

### 中危 (1个)

**Line 28**: 密码明文记录
- 问题: 密码被记录到日志
- 建议: 使用logger过滤敏感信息
\`\`\`

## 更新日志

- v1.0.0 (2026-03-24): 初始版本
```

---

## 四、代码实现

### 4.1 基本结构

```python
# skills/code_review/src/main.py

from typing import Dict, Any, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class Issue:
    """问题定义"""
    line: int
    severity: str  # high, medium, low
    type: str      # security, performance, style, bug
    message: str
    suggestion: str

class CodeReviewSkill:
    """代码审查技能"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = "code_review"
        self.version = "1.0.0"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行代码审查
        
        Args:
            file_path: 文件路径
            language: 编程语言
            severity: 最低严重级别
            format: 输出格式
        
        Returns:
            审查结果
        """
        # 验证参数
        self._validate_params(kwargs)
        
        # 读取文件
        code = self._read_file(kwargs["file_path"])
        
        # 执行分析
        issues = self._analyze(code, kwargs)
        
        # 生成结果
        result = self._format_result(issues, kwargs)
        
        return result
    
    def _validate_params(self, params: Dict[str, Any]) -> None:
        """验证参数"""
        if "file_path" not in params:
            raise ValueError("缺少必需参数: file_path")
    
    def _read_file(self, file_path: str) -> str:
        """读取文件内容"""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    
    def _analyze(self, code: str, params: Dict[str, Any]) -> List[Issue]:
        """执行代码分析"""
        issues = []
        
        # 静态分析
        issues.extend(self._static_analysis(code))
        
        # LLM分析
        issues.extend(self._llm_analysis(code, params))
        
        # 过滤严重级别
        severity_filter = params.get("severity", "all")
        if severity_filter != "all":
            severity_order = {"high": 1, "medium": 2, "low": 3}
            issues = [i for i in issues if severity_order[i.severity] <= severity_order[severity_filter]]
        
        return issues
    
    def _static_analysis(self, code: str) -> List[Issue]:
        """静态分析"""
        issues = []
        lines = code.split("\n")
        
        for i, line in enumerate(lines, 1):
            # 检查SQL注入风险
            if "execute(" in line and ("+" in line or "format(" in line or "f\"" in line):
                issues.append(Issue(
                    line=i,
                    severity="high",
                    type="security",
                    message="SQL注入风险",
                    suggestion="使用参数化查询"
                ))
        
        return issues
    
    def _llm_analysis(self, code: str, params: Dict[str, Any]) -> List[Issue]:
        """LLM分析"""
        # 调用LLM进行深度分析
        # 这里是示例，实际需要实现
        return []
    
    def _format_result(self, issues: List[Issue], params: Dict[str, Any]) -> Dict[str, Any]:
        """格式化结果"""
        format_type = params.get("format", "markdown")
        
        result = {
            "status": "success",
            "file": params["file_path"],
            "issues": [
                {
                    "line": i.line,
                    "severity": i.severity,
                    "type": i.type,
                    "message": i.message,
                    "suggestion": i.suggestion
                }
                for i in issues
            ],
            "summary": {
                "total": len(issues),
                "high": len([i for i in issues if i.severity == "high"]),
                "medium": len([i for i in issues if i.severity == "medium"]),
                "low": len([i for i in issues if i.severity == "low"])
            }
        }
        
        return result
```

### 4.2 Skill基类

```python
# skills/base.py

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSkill(ABC):
    """Skill基类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = self.__class__.__name__.replace("Skill", "").lower()
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """执行技能"""
        pass
    
    @abstractmethod
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数"""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        return {
            "name": self.name,
            "version": getattr(self, "version", "1.0.0"),
            "description": self.__doc__
        }
```

---

## 五、Skill管理

### 5.1 安装Skill

```bash
# 本地安装
cp -r ./my_skill /path/to/agent/skills/

# 从URL安装
curl -o skill.zip https://example.com/skills/code_review.zip
unzip skill.zip -d /path/to/agent/skills/
```

### 5.2 注册Skill

```json
// config/agents.json
{
  "agents": {
    "zhongshu": {
      "skills": [
        "architecture_design",
        "task_decomposition",
        "code_review"  // 新增技能
      ]
    }
  }
}
```

### 5.3 调用Skill

```python
# Agent内部调用
class Agent:
    def use_skill(self, skill_name: str, **kwargs):
        skill = self.skills.get(skill_name)
        if not skill:
            raise SkillNotFoundError(skill_name)
        return skill.execute(**kwargs)

# 使用示例
agent = Agent()
result = agent.use_skill("code_review", file_path="./main.py")
```

---

## 六、预置Skills

### 6.1 推荐Skills

| Skill | 功能 | 适用Agent |
|-------|------|-----------|
| code_review | 代码审查 | 门下省、刑部 |
| api_design | API设计 | 礼部 |
| security_audit | 安全审计 | 刑部 |
| doc_generator | 文档生成 | 礼部 |
| test_generator | 测试生成 | 兵部 |
| db_design | 数据库设计 | 户部 |
| deployment | 部署配置 | 工部 |

### 6.2 Skill分类

```
Skills按功能分类:

分析类:
- code_review      代码审查
- security_audit   安全审计
- performance_analysis 性能分析

生成类:
- code_generator   代码生成
- doc_generator    文档生成
- test_generator   测试生成

设计类:
- api_design       API设计
- db_design        数据库设计
- architecture_design 架构设计

运维类:
- deployment       部署配置
- monitoring       监控配置
- logging          日志配置
```

---

## 七、测试规范

### 7.1 测试结构

```python
# skills/code_review/tests/test_main.py

import pytest
from skills.code_review.src.main import CodeReviewSkill

class TestCodeReviewSkill:
    """代码审查技能测试"""
    
    @pytest.fixture
    def skill(self):
        return CodeReviewSkill()
    
    @pytest.fixture
    def sample_code(self, tmp_path):
        code = """
def unsafe_query(user_input):
    query = "SELECT * FROM users WHERE id = " + user_input
    return execute(query)
"""
        file_path = tmp_path / "test_code.py"
        file_path.write_text(code)
        return str(file_path)
    
    def test_execute_success(self, skill, sample_code):
        """测试正常执行"""
        result = skill.execute(file_path=sample_code)
        
        assert result["status"] == "success"
        assert "issues" in result
        assert "summary" in result
    
    def test_detect_sql_injection(self, skill, sample_code):
        """测试SQL注入检测"""
        result = skill.execute(file_path=sample_code)
        
        sql_issues = [i for i in result["issues"] if i["type"] == "security"]
        assert len(sql_issues) > 0
    
    def test_invalid_params(self, skill):
        """测试无效参数"""
        with pytest.raises(ValueError):
            skill.execute()
```

---

*最后更新: 2026-03-24*