# 项目结构模板

> **版本**: 1.0.0
> **用途**: 多Agent项目的标准目录结构

---

## 一、标准目录结构

```
project-root/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # 持续集成
│       ├── deploy.yml                # 自动部署
│       └── security-scan.yml         # 安全扫描
│
├── agents/                           # Agent人格定义
│   ├── zhongshu/
│   │   ├── SOUL.md                   # 中书省人格
│   │   └── skills/                   # 中书省技能
│   ├── menxia/
│   │   ├── SOUL.md                   # 门下省人格
│   │   └── skills/
│   ├── shangshu/
│   │   ├── SOUL.md                   # 尚书省人格
│   │   └── skills/
│   ├── hubu/
│   ├── libu/
│   ├── bingbu/
│   ├── xingbu/
│   └── gongbu/
│
├── assets/                           # 静态资源
│   ├── images/                       # 图片
│   ├── diagrams/                     # 架构图
│   └── templates/                    # 模板文件
│
├── config/                           # 配置文件
│   ├── settings.py                   # 主配置
│   ├── agents.json                   # Agent配置
│   ├── models.json                   # 模型配置
│   └── workflows/                    # 工作流配置
│       └── default.yaml
│
├── core/                             # 核心模块
│   ├── __init__.py
│   ├── dispatcher.py                 # 调度器
│   ├── state_machine.py              # 状态机
│   ├── message_bus.py                # 消息总线
│   └── memory.py                     # 记忆管理
│
├── dashboard/                        # 监控看板
│   ├── server.py                     # API服务
│   ├── dashboard.html                # 看板页面
│   └── dist/                         # 构建产物
│
├── docs/                             # 文档目录
│   ├── INDEX.md                      # 文档索引
│   ├── README.md                     # 项目说明
│   ├── requirements.md               # 需求文档
│   ├── architecture.md               # 架构设计
│   ├── api-design.md                 # API设计
│   ├── deployment.md                 # 部署文档
│   ├── operations.md                 # 运维手册
│   └── engineering-knowledge-base/   # 工程知识库
│       ├── INDEX.md
│       ├── 01-architecture/
│       ├── 02-specifications/
│       ├── 03-agent-design/
│       ├── 04-workflow-design/
│       ├── 05-security/
│       └── 06-config-templates/
│
├── logs/                             # 日志目录
│   ├── app.log                       # 应用日志
│   ├── inspector.log                 # 监察日志
│   └── archive/                      # 日志归档
│
├── memory/                           # 记忆系统
│   ├── daily/                        # 日记
│   ├── sessions/                     # 会话记录
│   ├── knowledge/                    # 知识沉淀
│   │   ├── decisions/                # 决策记录
│   │   ├── problems/                 # 问题记录
│   │   └── patterns/                 # 模式沉淀
│   └── project-context.json          # 项目上下文
│
├── modules/                          # 功能模块
│   ├── __init__.py
│   ├── llm_service/                  # LLM服务
│   ├── storage_service/              # 存储服务
│   └── notify_service/               # 通知服务
│
├── scripts/                          # 脚本工具
│   ├── install.sh                    # 安装脚本
│   ├── run.sh                        # 启动脚本
│   └── tools/                        # 工具脚本
│
├── skills/                           # 技能模块
│   ├── code_review/
│   │   ├── SKILL.md
│   │   └── src/
│   ├── api_design/
│   └── security_audit/
│
├── tests/                            # 测试文件
│   ├── unit/                         # 单元测试
│   ├── integration/                  # 集成测试
│   └── e2e/                          # 端到端测试
│
├── data/                             # 运行时数据
│   ├── cache/                        # 缓存
│   └── temp/                         # 临时文件
│
├── .env.example                      # 环境变量示例
├── .gitignore                        # Git忽略
├── docker-compose.yml                # Docker编排
├── Dockerfile                        # Docker镜像
├── INDEX.md                          # 项目索引
├── PROJECT-STRUCTURE.md              # 项目结构
├── README.md                         # 项目说明
├── VERSION                           # 版本号
└── requirements.txt                  # 依赖列表
```

---

## 二、目录说明

### 2.1 核心目录

| 目录 | 用途 | 必需 |
|------|------|------|
| `agents/` | Agent人格和技能定义 | ✅ |
| `config/` | 配置文件 | ✅ |
| `core/` | 核心模块代码 | ✅ |
| `docs/` | 文档 | ✅ |
| `memory/` | 记忆系统 | ✅ |
| `modules/` | 功能模块 | ✅ |
| `skills/` | 技能模块 | ✅ |
| `tests/` | 测试代码 | ✅ |

### 2.2 可选目录

| 目录 | 用途 | 条件 |
|------|------|------|
| `.github/` | CI/CD配置 | 需要自动化 |
| `dashboard/` | 监控看板 | 需要可视化 |
| `logs/` | 日志存储 | 生产环境 |
| `scripts/` | 脚本工具 | 复杂部署 |
| `data/` | 运行时数据 | 需要持久化 |

---

## 三、文件模板

### 3.1 README.md

```markdown
# 项目名称

一句话描述项目功能。

## 功能特性

- 特性1
- 特性2

## 快速开始

### 安装

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 运行

\`\`\`bash
python main.py
\`\`\`

## 文档

详细文档请见 [docs/INDEX.md](docs/INDEX.md)

## 许可证

MIT
```

### 3.2 .env.example

```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API密钥
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-xxx

# 服务配置
LOG_LEVEL=INFO
DEBUG=false

# 安全配置
SECRET_KEY=your-secret-key
```

### 3.3 VERSION

```
1.0.0
```

### 3.4 requirements.txt

```
# 核心依赖
openai>=1.0.0
anthropic>=0.18.0
pydantic>=2.0.0

# 数据存储
redis>=5.0.0
neo4j>=5.0.0

# Web框架
fastapi>=0.100.0
uvicorn>=0.23.0

# 工具
python-dotenv>=1.0.0
pyyaml>=6.0
```

### 3.5 .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
venv/
ENV/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo

# 环境变量
.env
.env.local

# 日志
logs/
*.log

# 数据
data/
*.db
*.sqlite

# 缓存
.cache/
__pycache__/

# 测试
.coverage
htmlcov/
.pytest_cache/

# 系统文件
.DS_Store
Thumbs.db
```

---

## 四、初始化脚本

```bash
#!/bin/bash
# init-project.sh - 项目初始化脚本

PROJECT_NAME=${1:-"my-agent-project"}

echo "创建项目: $PROJECT_NAME"

# 创建目录
mkdir -p $PROJECT_NAME/{agents/{zhongshu,menxia,shangshu,hubu,libu,bingbu,xingbu,gongbu},config/workflows,core,dashboard,docs/engineering-knowledge-base/{01-architecture,02-specifications,03-agent-design,04-workflow-design,05-security,06-config-templates},logs/archive,memory/{daily,sessions,knowledge/{decisions,problems,patterns}},modules,scripts/tools,skills,tests/{unit,integration,e2e},data/{cache,temp},assets/{images,diagrams,templates}}

# 创建基础文件
touch $PROJECT_NAME/README.md
touch $PROJECT_NAME/INDEX.md
touch $PROJECT_NAME/PROJECT-STRUCTURE.md
touch $PROJECT_NAME/VERSION
touch $PROJECT_NAME/requirements.txt
touch $PROJECT_NAME/.env.example
touch $PROJECT_NAME/.gitignore
touch $PROJECT_NAME/docker-compose.yml
touch $PROJECT_NAME/Dockerfile

# 创建__init__.py
touch $PROJECT_NAME/core/__init__.py
touch $PROJECT_NAME/modules/__init__.py

echo "项目创建完成: $PROJECT_NAME"
```

---

*最后更新: 2026-03-24*