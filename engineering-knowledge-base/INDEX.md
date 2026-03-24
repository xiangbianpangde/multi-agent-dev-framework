# 工程知识库索引

> **版本**: 1.0.0
> **创建时间**: 2026-03-24
> **用途**: AI辅助的多Agent项目自动开发框架

---

## 一、知识库结构

```
engineering-knowledge-base/
├── INDEX.md                    # 本文件 - 索引导航
├── 01-architecture/            # 架构设计
│   └── overview.md             # 三省六部制架构总览
├── 02-specifications/          # 开发规范
│   ├── modular-principles.md   # 模块化原则
│   ├── code-standards.md       # 代码规范
│   ├── git-conventions.md      # Git提交规范
│   ├── dual-agent-review.md    # 双Agent审查机制
│   └── problem-handling.md     # 问题处理规范
├── 03-agent-design/            # Agent设计
│   ├── agent-template.md       # Agent人格模板规范
│   ├── skills-design.md        # Skills设计规范
│   └── model-selection.md      # 模型选择指南
├── 04-workflow-design/         # 工作流设计
│   ├── development-flow.md     # 11步开发流程
│   ├── task-state-machine.md   # 任务状态机
│   └── memory-system.md        # 记忆系统设计
├── 05-security/                # 安全设计
│   └── security-audit.md       # 安全审计规范
├── 06-config-templates/        # 配置模板
│   ├── agents.json             # Agent配置模板
│   ├── models.json             # 模型配置模板
│   └── project-structure.md    # 项目结构模板
└── 07-knowledge-graph/         # 知识图谱
    └── design.md               # 知识图谱设计文档
```

---

## 二、核心概念

### 2.1 系统定位

**AI辅助的多Agent项目开发工厂**

| 维度 | 说明 |
|------|------|
| 输入 | 需求描述（自然语言） |
| 处理 | 三省六部协作开发 |
| 输出 | 完整的多Agent项目 |

### 2.2 核心差异

| 对比项 | 传统开发 | 本框架 |
|--------|----------|--------|
| 需求分析 | 人工+会议 | 中书省自动分析 |
| 架构设计 | 架构师主导 | 门下省审核把关 |
| 代码编写 | 程序员执行 | 尚书省+六部协作 |
| 质量保证 | QA测试 | 门下省强制审核 |
| 知识沉淀 | 文档维护 | 记忆系统自动归档 |

### 2.3 关键机制

```
┌─────────────────────────────────────────────────────────┐
│ 核心机制                                                │
├─────────────────────────────────────────────────────────┤
│ 1. 门下省强制审核 - 不是可选插件，是架构的一部分        │
│ 2. 双Agent审查 - 基础模型写，高性能模型审               │
│ 3. 先索引再实现 - 每步都有文档痕迹                      │
│ 4. 记忆分层 - 短/中/长期知识管理                       │
│ 5. 状态机约束 - 任务流转不可绕过                       │
└─────────────────────────────────────────────────────────┘
```

---

## 三、快速导航

### 按角色查阅

| 角色 | 推荐阅读顺序 |
|------|--------------|
| 架构师 | 01-architecture → 03-agent-design → 04-workflow-design |
| 开发者 | 02-specifications → 06-config-templates → 04-workflow-design |
| 运维 | 05-security → 06-config-templates |
| 项目经理 | 01-architecture/overview.md → 04-workflow-design/development-flow.md |

### 按任务查阅

| 任务 | 推荐文档 |
|------|----------|
| 创建新Agent | 03-agent-design/agent-template.md |
| 设计工作流 | 04-workflow-design/development-flow.md |
| 代码审查 | 02-specifications/dual-agent-review.md |
| 安全审计 | 05-security/security-audit.md |
| 选择模型 | 03-agent-design/model-selection.md |

---

## 四、版本历史

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| 1.0.0 | 2026-03-24 | 初始版本 |

---

*最后更新: 2026-03-24*