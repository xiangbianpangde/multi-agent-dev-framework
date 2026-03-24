# 项目索引

本索引帮助你快速导航到所需内容。

## 核心文档

| 文档 | 说明 | 路径 |
|------|------|------|
| README | 项目说明 | [README.md](README.md) |
| 贡献指南 | 如何贡献 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 许可证 | MIT License | [LICENSE](LICENSE) |

## 工程知识库

完整的开发知识体系：[engineering-knowledge-base/INDEX.md](engineering-knowledge-base/INDEX.md)

### 快速链接

**架构设计**
- [三省六部制架构](engineering-knowledge-base/01-architecture/overview.md)

**开发规范**
- [模块化原则](engineering-knowledge-base/02-specifications/modular-principles.md)
- [代码规范](engineering-knowledge-base/02-specifications/code-standards.md)
- [Git规范](engineering-knowledge-base/02-specifications/git-conventions.md)
- [双Agent审查](engineering-knowledge-base/02-specifications/dual-agent-review.md)

**Agent设计**
- [Agent模板](engineering-knowledge-base/03-agent-design/agent-template.md)
- [Skills设计](engineering-knowledge-base/03-agent-design/skills-design.md)
- [模型选择](engineering-knowledge-base/03-agent-design/model-selection.md)

**工作流设计**
- [11步开发流程](engineering-knowledge-base/04-workflow-design/development-flow.md)
- [任务状态机](engineering-knowledge-base/04-workflow-design/task-state-machine.md)
- [记忆系统](engineering-knowledge-base/04-workflow-design/memory-system.md)

**安全**
- [安全审计](engineering-knowledge-base/05-security/security-audit.md)

**配置模板**
- [Agent配置](engineering-knowledge-base/06-config-templates/agents.json)
- [模型配置](engineering-knowledge-base/06-config-templates/models.json)
- [项目结构](engineering-knowledge-base/06-config-templates/project-structure.md)

## 工具

自动化开发工具：[tools/README.md](tools/README.md)

### CLI命令

```bash
# 创建项目
python tools/cli.py project --name "项目名"

# 创建Agent
python tools/cli.py agent --id "agent_id" --name "名称" --role decision

# 创建Skill
python tools/cli.py skill --name "skill_name" --description "描述"
```

### 核心模块

| 模块 | 说明 |
|------|------|
| dispatcher.py | 任务调度器 |
| state_machine.py | 状态机 |
| message_bus.py | 消息总线 |
| memory.py | 记忆管理 |

## 示例

使用示例：[examples/README.md](examples/README.md)

- [快速入门](examples/quick_start.py)
- [完整工作流](examples/full_workflow.py)

## 测试

测试代码：[tests/README.md](tests/README.md)

```bash
# 运行测试
pytest tests/
```

## 快速开始

1. 阅读 [README.md](README.md) 了解项目
2. 查看 [工程知识库](engineering-knowledge-base/INDEX.md) 学习框架
3. 运行 [示例](examples/quick_start.py) 快速上手
4. 使用 [工具](tools/README.md) 创建项目