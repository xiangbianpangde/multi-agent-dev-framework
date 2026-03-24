# 多Agent项目开发框架

> 基于三省六部制的多Agent项目自动开发框架

## 项目简介

本框架提供了一套完整的多Agent项目开发解决方案，采用中国古代三省六部制的设计理念，实现分权制衡的Agent协作架构。

### 核心特点

- 🏛️ **三省六部制架构** - 决策、审核、执行三权分立
- 📋 **11步开发流程** - 从需求到交付的完整流程
- 🔄 **双Agent审查机制** - 基础模型执行，高性能模型审核
- 🧠 **三层记忆系统** - 短期/中期/长期记忆管理
- ⚙️ **9状态状态机** - 任务流转可控可追溯
- 🛡️ **强制审核机制** - 门下省审核是必经环节

## 快速开始

### 安装

```bash
git clone https://github.com/xiangbianpangde/multi-agent-dev-framework.git
cd multi-agent-dev-framework
```

### 使用工具

```bash
cd tools

# 创建新项目
python cli.py project --name "my-project" --description "我的项目"

# 创建Agent
python cli.py agent --id "my_agent" --name "我的Agent" --role execution

# 创建Skill
python cli.py skill --name "code_review" --description "代码审查"

# 查看帮助
python cli.py list
```

## 项目结构

```
multi-agent-dev-framework/
├── README.md                   # 项目说明
├── LICENSE                     # MIT许可证
├── CONTRIBUTING.md             # 贡献指南
├── engineering-knowledge-base/ # 工程知识库
│   ├── INDEX.md               # 知识库索引
│   ├── 01-architecture/       # 架构设计
│   ├── 02-specifications/     # 开发规范
│   ├── 03-agent-design/       # Agent设计
│   ├── 04-workflow-design/    # 工作流设计
│   ├── 05-security/           # 安全设计
│   └── 06-config-templates/   # 配置模板
├── tools/                      # 自动化工具
│   ├── cli.py                 # 命令行工具
│   ├── generators/            # 生成器
│   └── templates/             # 模板
│       └── core/              # 核心模块实现
└── examples/                   # 使用示例
```

## 架构设计

### 三省六部制

```
┌─────────────────────────────────────────────────────────────┐
│ 用户 (User)                                                 │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 中书省 (决策调度层)                                         │
│ 需求分析、架构设计、任务分解、协调各部门                     │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 门下省 (监察审核层)                                         │
│ 方案审核、质量把关、安全审计、封驳不合格产出                  │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 尚书省 (执行协调层)                                         │
│ 任务派发、进度跟踪、结果整合                                 │
└───┬──────┬──────┬──────┬──────┬───┐
    │      │      │      │      │
    ▼      ▼      ▼      ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│户部 ││礼部 ││兵部 ││刑部 ││工部 │
│数据 ││文档 ││代码 ││安全 ││运维 │
└─────┘└─────┘└─────┘└─────┘└─────┘
```

### 任务状态机

```
draft → planning → review → dispatched → executing → checking → accepted → done
                     │
                     └── rejected ──┐
                                    │
                                    └──→ (返回planning)
```

## 文档

详细文档请见 [工程知识库](engineering-knowledge-base/INDEX.md)

### 核心文档

| 文档 | 说明 |
|------|------|
| [架构设计](engineering-knowledge-base/01-architecture/overview.md) | 三省六部制架构详解 |
| [开发规范](engineering-knowledge-base/02-specifications/) | 代码、Git、审查规范 |
| [Agent设计](engineering-knowledge-base/03-agent-design/) | Agent人格、技能设计 |
| [工作流设计](engineering-knowledge-base/04-workflow-design/) | 开发流程、状态机、记忆系统 |

## 工具使用

### 项目生成器

```bash
python tools/cli.py project --name "project-name" --init-git
```

生成内容：
- 完整项目目录结构
- 8个Agent的SOUL.md人格文件
- 配置文件模板
- 项目文档模板

### Agent生成器

```bash
python tools/cli.py agent --id "agent_id" --name "显示名称" --role decision
```

角色类型：
- `decision` - 决策调度层
- `audit` - 监察审核层
- `execution` - 执行层

### Skill生成器

```bash
python tools/cli.py skill --name "skill_name" --description "功能描述"
```

### 核心模块

```python
from tools.templates.core import (
    TaskDispatcher,    # 任务调度器
    StateMachine,      # 状态机
    MessageBus,        # 消息总线
    MemoryManager      # 记忆管理
)

# 创建调度器
dispatcher = TaskDispatcher(max_concurrent=5)

# 创建状态机
sm = StateMachine()
sm.transition(TaskState.PLANNING, "开始规划")

# 创建消息总线
bus = MessageBus()
await bus.send(message)

# 记忆管理
memory = MemoryManager()
memory.remember("key", "value", MemoryDuration.SHORT)
```

## 开发路线

- [x] 框架设计
- [x] 知识库文档
- [x] 自动化工具
- [x] 核心模块实现
- [ ] Web界面
- [ ] 更多示例
- [ ] 测试覆盖

## 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 致谢

- 架构灵感来源于唐代三省六部制
- 基于 [OpenClaw](https://openclaw.ai) 平台构建
- 参考 [edict](https://github.com/cft0808/edict) 项目

---

*以古制御新技，以智慧驾驭AI*