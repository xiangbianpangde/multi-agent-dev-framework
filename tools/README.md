# 多Agent项目开发工具集

> 自动化生成多Agent项目、Agent配置、Skill模块

---

## 一、工具概览

| 工具 | 功能 | 命令 |
|------|------|------|
| 项目生成器 | 创建完整项目结构 | `python cli.py project` |
| Agent生成器 | 创建Agent人格和配置 | `python cli.py agent` |
| Skill生成器 | 创建技能模块 | `python cli.py skill` |

---

## 二、快速开始

### 2.1 创建新项目

```bash
# 基本用法
python cli.py project --name "my-project" --description "我的多Agent项目"

# 初始化Git仓库
python cli.py project --name "my-project" --init-git

# 指定输出目录
python cli.py project --name "my-project" --output /path/to/output
```

**生成内容：**
- 标准项目目录结构
- Agent配置文件 (agents.json)
- 模型配置文件 (models.json)
- 8个Agent的SOUL.md人格文件
- 项目文档模板
- 配置文件模板

### 2.2 创建新Agent

```bash
# 创建决策层Agent
python cli.py agent \
  --id "my_decision_agent" \
  --name "决策Agent" \
  --role decision \
  --description "负责决策分析"

# 创建审核层Agent
python cli.py agent \
  --id "my_audit_agent" \
  --name "审核Agent" \
  --role audit

# 指定模型
python cli.py agent \
  --id "my_agent" \
  --name "我的Agent" \
  --role execution \
  --model-primary "qwen" \
  --model-fallback "gpt-4"
```

**生成内容：**
- SOUL.md人格文件
- agents.json配置片段

### 2.3 创建新Skill

```bash
# 基本用法
python cli.py skill \
  --name "code_review" \
  --description "代码审查技能"

# 带参数
python cli.py skill \
  --name "data_analysis" \
  --description "数据分析技能" \
  --params '[{"name": "file_path", "type": "string", "required": true, "description": "文件路径"}]'
```

**生成内容：**
- SKILL.md文档
- src/main.py代码模板
- tests/test_xxx.py测试文件

---

## 三、命令详解

### 3.1 project命令

```bash
python cli.py project [选项]

选项:
  --name        项目名称（必需）
  --description 项目描述
  --author      作者
  --output      输出目录（默认当前目录）
  --init-git    初始化Git仓库
```

### 3.2 agent命令

```bash
python cli.py agent [选项]

选项:
  --id             Agent ID（必需）
  --name           显示名称（必需）
  --role           角色类型（必需）
                   - decision: 决策调度
                   - audit: 监察审核
                   - execution: 执行实施
  --description    Agent描述
  --model-primary  主模型（默认gpt-4）
  --model-fallback 备用模型（默认claude-3）
  --output         输出目录
```

### 3.3 skill命令

```bash
python cli.py skill [选项]

选项:
  --name        技能名称（必需）
  --description 功能描述（必需）
  --params      参数JSON
  --output      输出目录
```

### 3.4 list命令

```bash
python cli.py list

列出:
- 支持的Agent角色
- 预置Agent模板
- 推荐模型
- 工程知识库位置
```

---

## 四、使用示例

### 4.1 完整项目创建流程

```bash
# 1. 创建项目
python cli.py project \
  --name "smart-assistant" \
  --description "智能助手项目" \
  --author "Your Name" \
  --init-git

# 2. 进入项目目录
cd smart-assistant

# 3. 创建自定义Agent
python ../cli.py agent \
  --id "special_agent" \
  --name "专项Agent" \
  --role execution \
  --output .

# 4. 创建Skill
python ../cli.py skill \
  --name "sentiment_analysis" \
  --description "情感分析技能" \
  --output .

# 5. 配置环境变量
cp .env.example .env
# 编辑.env填入API密钥

# 6. 安装依赖
pip install -r requirements.txt
```

### 4.2 参数JSON格式

```json
[
  {
    "name": "input_file",
    "type": "string",
    "required": true,
    "description": "输入文件路径"
  },
  {
    "name": "output_format",
    "type": "string",
    "required": false,
    "default": "json",
    "description": "输出格式"
  },
  {
    "name": "verbose",
    "type": "boolean",
    "required": false,
    "default": false,
    "description": "详细输出"
  }
]
```

---

## 五、工具扩展

### 5.1 自定义模板

可以在 `templates/` 目录下添加自定义模板：

```
templates/
├── project/           # 项目模板
│   └── custom/
├── agent/             # Agent模板
│   └── soul_custom.md
└── skill/             # Skill模板
    └── skill_custom.md
```

### 5.2 添加新的生成器

```python
# generators/my_generator.py

class MyGenerator:
    def generate(self, **kwargs):
        # 实现生成逻辑
        pass
```

---

## 六、常见问题

### Q: 生成的项目如何运行？

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑.env

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
bash scripts/run.sh
```

### Q: 如何添加新的Agent角色？

修改 `agent_generator.py` 中的 `ROLES` 字典：

```python
ROLES = {
    "my_role": {
        "name": "自定义角色",
        "department": "custom_layer",
        "capabilities": ["capability1", "capability2"]
    }
}
```

### Q: 如何自定义生成的代码模板？

修改对应生成器中的模板方法，如：
- `SkillGenerator.generate_code()` - Skill代码模板
- `AgentGenerator.generate_soul()` - Agent人格模板

---

## 七、目录结构

```
tools/
├── cli.py                    # 统一CLI入口
├── generators/
│   ├── project_generator.py  # 项目生成器
│   ├── agent_generator.py    # Agent生成器
│   └── skill_generator.py    # Skill生成器
├── templates/                # 自定义模板
└── scripts/                  # 辅助脚本
```

---

*工具版本: 1.0.0*
*最后更新: 2026-03-24*