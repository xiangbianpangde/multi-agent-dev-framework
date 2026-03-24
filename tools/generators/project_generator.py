#!/usr/bin/env python3
"""
项目生成器 - 根据需求自动生成多Agent项目结构

功能：
- 生成标准项目目录结构
- 创建配置文件模板
- 生成Agent人格文件
- 创建初始文档

使用：
    python project_generator.py --name "项目名称" --description "项目描述"
"""

import os
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, List


class ProjectGenerator:
    """项目生成器"""
    
    # 标准目录结构
    DIRECTORIES = [
        "agents/{zhongshu,menxia,shangshu,hubu,libu,bingbu,xingbu,gongbu}",
        "config/workflows",
        "core",
        "docs/engineering-knowledge-base/{01-architecture,02-specifications,03-agent-design,04-workflow-design,05-security,06-config-templates}",
        "logs/archive",
        "memory/{daily,sessions,knowledge/{decisions,problems,patterns}}",
        "modules",
        "scripts/tools",
        "skills",
        "tests/{unit,integration,e2e}",
        "data/{cache,temp}",
        "assets/{images,diagrams,templates}",
    ]
    
    def __init__(self, project_name: str, output_dir: str = "."):
        self.project_name = project_name
        self.project_dir = Path(output_dir) / self._sanitize_name(project_name)
        self.created_files = []
        self.created_dirs = []
    
    def generate(self, description: str = "", author: str = "") -> dict:
        """生成项目"""
        print(f"正在创建项目: {self.project_name}")
        
        # 1. 创建目录结构
        self._create_directories()
        
        # 2. 创建配置文件
        self._create_config_files()
        
        # 3. 创建Agent文件
        self._create_agent_files()
        
        # 4. 创建文档文件
        self._create_doc_files(description, author)
        
        # 5. 创建工具文件
        self._create_tool_files()
        
        return {
            "project_dir": str(self.project_dir),
            "created_files": self.created_files,
            "created_dirs": self.created_dirs
        }
    
    def _sanitize_name(self, name: str) -> str:
        """清理项目名称"""
        return name.lower().replace(" ", "-").replace("_", "-")
    
    def _create_directories(self):
        """创建目录结构"""
        # 创建根目录
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.created_dirs.append(str(self.project_dir))
        
        # 创建子目录
        for dir_pattern in self.DIRECTORIES:
            # 处理花括号展开
            if "{" in dir_pattern:
                # 简单处理：创建所有可能的目录
                base, subs = dir_pattern.split("{")
                subs = subs.rstrip("}").split(",")
                for sub in subs:
                    dir_path = self.project_dir / base / sub
                    dir_path.mkdir(parents=True, exist_ok=True)
                    self.created_dirs.append(str(dir_path))
            else:
                dir_path = self.project_dir / dir_pattern
                dir_path.mkdir(parents=True, exist_ok=True)
                self.created_dirs.append(str(dir_path))
    
    def _create_config_files(self):
        """创建配置文件"""
        # agents.json
        agents_config = self._get_agents_template()
        self._write_file("config/agents.json", agents_config)
        
        # models.json
        models_config = self._get_models_template()
        self._write_file("config/models.json", models_config)
        
        # settings.py
        settings = self._get_settings_template()
        self._write_file("config/settings.py", settings)
        
        # .env.example
        env_example = self._get_env_template()
        self._write_file(".env.example", env_example)
        
        # .gitignore
        gitignore = self._get_gitignore_template()
        self._write_file(".gitignore", gitignore)
    
    def _create_agent_files(self):
        """创建Agent人格文件"""
        agents = ["zhongshu", "menxia", "shangshu", "hubu", "libu", "bingbu", "xingbu", "gongbu"]
        
        for agent in agents:
            soul_content = self._get_soul_template(agent)
            self._write_file(f"agents/{agent}/SOUL.md", soul_content)
    
    def _create_doc_files(self, description: str, author: str):
        """创建文档文件"""
        # README.md
        readme = self._get_readme_template(description, author)
        self._write_file("README.md", readme)
        
        # INDEX.md
        index = self._get_index_template()
        self._write_file("INDEX.md", index)
        
        # PROJECT-STRUCTURE.md
        structure = self._get_structure_template()
        self._write_file("PROJECT-STRUCTURE.md", structure)
        
        # VERSION
        self._write_file("VERSION", "1.0.0\n")
        
        # requirements.txt
        requirements = self._get_requirements_template()
        self._write_file("requirements.txt", requirements)
        
        # docs/INDEX.md
        docs_index = self._get_docs_index_template()
        self._write_file("docs/INDEX.md", docs_index)
    
    def _create_tool_files(self):
        """创建工具文件"""
        # core/__init__.py
        self._write_file("core/__init__.py", '"""核心模块"""\n')
        
        # modules/__init__.py
        self._write_file("modules/__init__.py", '"""功能模块"""\n')
        
        # scripts/run.sh
        run_script = self._get_run_script_template()
        self._write_file("scripts/run.sh", run_script)
        
        # docker-compose.yml
        docker_compose = self._get_docker_compose_template()
        self._write_file("docker-compose.yml", docker_compose)
    
    def _write_file(self, relative_path: str, content: str):
        """写入文件"""
        file_path = self.project_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        self.created_files.append(str(file_path))
    
    # ========== 模板方法 ==========
    
    def _get_agents_template(self) -> str:
        return '''{
  "version": "1.0.0",
  "agents": {
    "zhongshu": {
      "id": "zhongshu",
      "name": "中书省",
      "role": "decision",
      "department": "decision_layer",
      "description": "决策调度中枢",
      "model": {
        "primary": "gpt-4",
        "fallback": "claude-3"
      },
      "capabilities": ["requirement_analysis", "architecture_design", "task_decomposition"],
      "skills": [],
      "permissions": {
        "can_send_to": ["menxia", "shangshu"],
        "can_receive_from": ["user", "menxia", "shangshu"],
        "can_create_task": true,
        "can_approve": false
      }
    },
    "menxia": {
      "id": "menxia",
      "name": "门下省",
      "role": "audit",
      "department": "audit_layer",
      "description": "监察审核中枢",
      "model": {
        "primary": "claude-3",
        "fallback": "gpt-4"
      },
      "capabilities": ["quality_review", "security_audit", "standard_check"],
      "skills": [],
      "permissions": {
        "can_send_to": ["zhongshu", "shangshu"],
        "can_receive_from": ["zhongshu"],
        "can_create_task": false,
        "can_approve": true
      }
    },
    "shangshu": {
      "id": "shangshu",
      "name": "尚书省",
      "role": "execution",
      "department": "execution_layer",
      "description": "执行协调中枢",
      "model": {
        "primary": "gemini-pro",
        "fallback": "qwen"
      },
      "capabilities": ["task_dispatch", "progress_tracking", "result_integration"],
      "skills": [],
      "permissions": {
        "can_send_to": ["zhongshu", "menxia", "hubu", "libu", "bingbu", "xingbu", "gongbu"],
        "can_receive_from": ["zhongshu", "menxia"],
        "can_create_task": false,
        "can_approve": false
      }
    },
    "hubu": {
      "id": "hubu",
      "name": "户部",
      "role": "execution",
      "department": "execution_layer",
      "description": "数据资源管理",
      "model": {"primary": "gemini-pro", "fallback": "qwen"},
      "capabilities": ["data_processing", "resource_management"],
      "skills": [],
      "permissions": {
        "can_send_to": ["shangshu", "menxia"],
        "can_receive_from": ["shangshu"],
        "can_create_task": false,
        "can_approve": false
      }
    },
    "libu": {
      "id": "libu",
      "name": "礼部",
      "role": "execution",
      "department": "execution_layer",
      "description": "文档规范管理",
      "model": {"primary": "kimi", "fallback": "glm-4"},
      "capabilities": ["document_writing", "api_design", "standard_formulation"],
      "skills": [],
      "permissions": {
        "can_send_to": ["shangshu", "menxia"],
        "can_receive_from": ["shangshu"],
        "can_create_task": false,
        "can_approve": false
      }
    },
    "bingbu": {
      "id": "bingbu",
      "name": "兵部",
      "role": "execution",
      "department": "execution_layer",
      "description": "代码开发实现",
      "model": {"primary": "qwen", "fallback": "gpt-4"},
      "capabilities": ["code_development", "testing", "debugging"],
      "skills": [],
      "permissions": {
        "can_send_to": ["shangshu", "menxia"],
        "can_receive_from": ["shangshu"],
        "can_create_task": false,
        "can_approve": false
      }
    },
    "xingbu": {
      "id": "xingbu",
      "name": "刑部",
      "role": "execution",
      "department": "execution_layer",
      "description": "安全合规审计",
      "model": {"primary": "claude-3", "fallback": "gpt-4"},
      "capabilities": ["security_audit", "compliance_check", "risk_control"],
      "skills": [],
      "permissions": {
        "can_send_to": ["shangshu", "menxia"],
        "can_receive_from": ["shangshu"],
        "can_create_task": false,
        "can_approve": false
      }
    },
    "gongbu": {
      "id": "gongbu",
      "name": "工部",
      "role": "execution",
      "department": "execution_layer",
      "description": "运维基础设施",
      "model": {"primary": "gemini-pro", "fallback": "qwen"},
      "capabilities": ["deployment", "monitoring", "ci_cd"],
      "skills": [],
      "permissions": {
        "can_send_to": ["shangshu", "menxia"],
        "can_receive_from": ["shangshu"],
        "can_create_task": false,
        "can_approve": false
      }
    }
  }
}'''
    
    def _get_models_template(self) -> str:
        return '''{
  "version": "1.0.0",
  "providers": {
    "openai": {
      "name": "OpenAI",
      "api_base": "https://api.openai.com/v1",
      "api_key_env": "OPENAI_API_KEY"
    },
    "anthropic": {
      "name": "Anthropic",
      "api_base": "https://api.anthropic.com",
      "api_key_env": "ANTHROPIC_API_KEY"
    },
    "google": {
      "name": "Google",
      "api_base": "https://generativelanguage.googleapis.com",
      "api_key_env": "GOOGLE_API_KEY"
    }
  },
  "models": {
    "gpt-4": {
      "provider": "openai",
      "context_window": 128000,
      "capabilities": ["chat", "function_call", "vision"]
    },
    "claude-3": {
      "provider": "anthropic",
      "context_window": 200000,
      "capabilities": ["chat", "vision"]
    },
    "gemini-pro": {
      "provider": "google",
      "context_window": 1000000,
      "capabilities": ["chat", "vision"]
    }
  },
  "recommendations": {
    "by_task": {
      "architecture_design": {"primary": "gpt-4", "fallback": "claude-3"},
      "code_development": {"primary": "qwen", "fallback": "gpt-4"},
      "security_audit": {"primary": "claude-3", "fallback": "gpt-4"},
      "document_writing": {"primary": "kimi", "fallback": "glm-4"}
    }
  }
}'''
    
    def _get_settings_template(self) -> str:
        return '''"""
项目配置文件
"""
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# Agent配置
AGENTS_CONFIG_PATH = PROJECT_ROOT / "config" / "agents.json"
MODELS_CONFIG_PATH = PROJECT_ROOT / "config" / "models.json"

# 记忆系统
MEMORY_PATH = PROJECT_ROOT / "memory"
LOGS_PATH = PROJECT_ROOT / "logs"

# 模型配置
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "4096"))

# 任务配置
MAX_CONCURRENT_TASKS = int(os.getenv("MAX_CONCURRENT_TASKS", "5"))
TASK_TIMEOUT = int(os.getenv("TASK_TIMEOUT", "300"))

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
'''
    
    def _get_env_template(self) -> str:
        return '''# API密钥配置
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-xxx
GOOGLE_API_KEY=xxx

# 模型配置
DEFAULT_MODEL=gpt-4
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=4096

# 任务配置
MAX_CONCURRENT_TASKS=5
TASK_TIMEOUT=300

# 日志配置
LOG_LEVEL=INFO
'''
    
    def _get_gitignore_template(self) -> str:
        return '''# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
dist/
*.egg-info/

# 虚拟环境
venv/
ENV/
env/

# IDE
.idea/
.vscode/
*.swp

# 环境变量
.env
.env.local

# 日志
logs/
*.log

# 数据
data/
*.db

# 缓存
.cache/

# 测试
.coverage
.pytest_cache/

# 系统文件
.DS_Store
Thumbs.db
'''
    
    def _get_soul_template(self, agent_id: str) -> str:
        templates = {
            "zhongshu": '''# 中书省 - 决策调度中枢

> 负责理解需求、设计方案、拆解任务、协调各部门

## 身份

- **ID**: zhongshu
- **名称**: 中书省
- **部门**: 中书省（决策层）
- **角色**: 规划中枢

## 职责

### 核心职责
- 接收并理解用户需求
- 分析需求可行性
- 设计系统架构和方案
- 拆解任务分配给各部门
- 协调资源、监控进度

### 边界
- 不做: 不直接执行代码编写、测试等具体工作
- 转交: 执行任务转交尚书省，审核转交门下省

## 工作流

### 输入
- 来源: 用户需求
- 格式: 自然语言描述

### 处理
1. 理解需求，提取关键信息
2. 分析可行性，识别风险
3. 设计架构方案
4. 拆解任务，分配给各部门
5. 提交门下省审核

### 输出
- 格式: 结构化任务计划
- 目标: 门下省（审核）、尚书省（派发）

---

*人格定义版本: 1.0.0*
''',
            "menxia": '''# 门下省 - 监察审核中枢

> 负责审核方案、把关质量、发现问题、封驳不合格产出

## 身份

- **ID**: menxia
- **名称**: 门下省
- **部门**: 门下省（审核层）
- **角色**: 审核中枢

## 职责

### 核心职责
- 审核中书省提交的方案
- 检查方案质量和可行性
- 识别潜在问题和风险
- 封驳不合格方案
- 验收最终成果

### 边界
- 不做: 不参与方案设计和执行
- 转交: 审核通过转交尚书省，不通过返回中书省

## 工作流

### 输入
- 来源: 中书省
- 格式: 结构化方案

### 处理
1. 审核方案完整性
2. 检查技术可行性
3. 评估风险和问题
4. 做出通过/封驳决定

### 输出
- 格式: 审核报告
- 目标: 中书省（封驳时）、尚书省（通过时）

---

*人格定义版本: 1.0.0*
''',
            "shangshu": '''# 尚书省 - 执行协调中枢

> 负责接收准奏任务、派发给六部、协调进度、汇总结果

## 身份

- **ID**: shangshu
- **名称**: 尚书省
- **部门**: 尚书省（执行层）
- **角色**: 调度中枢

## 职责

### 核心职责
- 接收门下省审核通过的任务
- 将任务派发给六部
- 协调各部门执行进度
- 汇总各部门执行结果
- 处理执行过程中的问题

### 边界
- 不做: 不直接执行具体任务
- 转交: 执行问题转交中书省协调

## 工作流

### 输入
- 来源: 门下省
- 格式: 审核通过的方案

### 处理
1. 分析任务分配
2. 派发给对应部门
3. 监控执行进度
4. 协调资源问题
5. 汇总执行结果

### 输出
- 格式: 执行报告
- 目标: 门下省（验收）、用户（交付）

---

*人格定义版本: 1.0.0*
'''
        }
        
        # 六部通用模板
        dept_info = {
            "hubu": ("户部", "数据资源管理", "数据处理、资源配置"),
            "libu": ("礼部", "文档规范管理", "文档编写、API设计"),
            "bingbu": ("兵部", "代码开发实现", "代码开发、测试、调试"),
            "xingbu": ("刑部", "安全合规审计", "安全审计、合规检查"),
            "gongbu": ("工部", "运维基础设施", "部署、监控、CI/CD")
        }
        
        if agent_id in templates:
            return templates[agent_id]
        
        if agent_id in dept_info:
            name, desc, capabilities = dept_info[agent_id]
            return f'''# {name} - {desc}

> 负责{capabilities}相关工作

## 身份

- **ID**: {agent_id}
- **名称**: {name}
- **部门**: 尚书省（执行层）
- **角色**: 执行部门

## 职责

### 核心职责
- 接收尚书省派发的任务
- 执行本部门专业工作
- 提交执行结果
- 配合其他部门协作

### 边界
- 不做: 不参与任务分配决策
- 转交: 需要协调的问题上报尚书省

## 工作流

### 输入
- 来源: 尚书省
- 格式: 任务指令

### 处理
1. 接收任务
2. 分析需求
3. 执行工作
4. 提交结果

### 输出
- 格式: 执行结果
- 目标: 尚书省

---

*人格定义版本: 1.0.0*
'''
        return ""
    
    def _get_readme_template(self, description: str, author: str) -> str:
        return f'''# {self.project_name}

{description or "多Agent项目"}

## 功能特性

- 三省六部制架构
- 自动化任务调度
- 多Agent协作

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 配置

1. 复制环境变量模板
```bash
cp .env.example .env
```

2. 配置API密钥
编辑 `.env` 文件，填入你的API密钥

### 运行

```bash
bash scripts/run.sh
```

## 项目结构

参见 [PROJECT-STRUCTURE.md](PROJECT-STRUCTURE.md)

## 文档

详细文档请见 [docs/INDEX.md](docs/INDEX.md)

## 作者

{author or "Anonymous"}

## 许可证

MIT
'''
    
    def _get_index_template(self) -> str:
        return f'''# {self.project_name} - 项目索引

## 快速导航

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目说明 |
| [PROJECT-STRUCTURE.md](PROJECT-STRUCTURE.md) | 项目结构 |
| [docs/INDEX.md](docs/INDEX.md) | 文档索引 |
| [config/agents.json](config/agents.json) | Agent配置 |

## 核心模块

| 模块 | 说明 |
|------|------|
| agents/ | Agent人格定义 |
| config/ | 配置文件 |
| core/ | 核心模块 |
| modules/ | 功能模块 |
| skills/ | 技能模块 |

## 开发指南

1. 阅读 [工程知识库](docs/engineering-knowledge-base/INDEX.md)
2. 了解 [三省六部架构](docs/engineering-knowledge-base/01-architecture/overview.md)
3. 参考 [开发流程](docs/engineering-knowledge-base/04-workflow-design/development-flow.md)
'''
    
    def _get_structure_template(self) -> str:
        return f'''# 项目结构

## 目录说明

```
{self._sanitize_name(self.project_name)}/
├── agents/               # Agent人格定义
│   ├── zhongshu/        # 中书省
│   ├── menxia/          # 门下省
│   ├── shangshu/        # 尚书省
│   ├── hubu/            # 户部
│   ├── libu/            # 礼部
│   ├── bingbu/          # 兵部
│   ├── xingbu/          # 刑部
│   └── gongbu/          # 工部
├── config/              # 配置文件
│   ├── agents.json      # Agent配置
│   ├── models.json      # 模型配置
│   └── settings.py      # 系统配置
├── core/                # 核心模块
├── docs/                # 文档
├── memory/              # 记忆系统
├── modules/             # 功能模块
├── skills/              # 技能模块
├── tests/               # 测试
├── logs/                # 日志
├── data/                # 数据
└── scripts/             # 脚本
```

## 说明

详见各目录下的README或文档。
'''
    
    def _get_requirements_template(self) -> str:
        return '''# 核心依赖
openai>=1.0.0
anthropic>=0.18.0
pydantic>=2.0.0

# 数据存储
redis>=5.0.0

# Web框架
fastapi>=0.100.0
uvicorn>=0.23.0

# 工具
python-dotenv>=1.0.0
pyyaml>=6.0
'''
    
    def _get_docs_index_template(self) -> str:
        return '''# 文档索引

## 工程知识库

详细的多Agent项目开发知识库请见 [engineering-knowledge-base/INDEX.md](engineering-knowledge-base/INDEX.md)

### 核心文档

| 文档 | 说明 |
|------|------|
| [架构设计](engineering-knowledge-base/01-architecture/overview.md) | 三省六部制架构 |
| [开发规范](engineering-knowledge-base/02-specifications/) | 代码、Git、审查规范 |
| [Agent设计](engineering-knowledge-base/03-agent-design/) | Agent人格、技能设计 |
| [工作流设计](engineering-knowledge-base/04-workflow-design/) | 开发流程、状态机、记忆系统 |

## 快速链接

- [需求文档](requirements.md) - 项目需求
- [架构设计](architecture.md) - 系统架构
- [API设计](api-design.md) - API接口设计
'''
    
    def _get_run_script_template(self) -> str:
        return '''#!/bin/bash

# 项目启动脚本

echo "Starting Multi-Agent Project..."

# 检查环境
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# 加载环境变量
export $(cat .env | grep -v ^# | xargs)

# 启动服务
echo "Services starting..."
# python main.py

echo "Done!"
'''
    
    def _get_docker_compose_template(self) -> str:
        return '''version: "3.8"

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    env_file:
      - .env

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
'''


def main():
    parser = argparse.ArgumentParser(description="多Agent项目生成器")
    parser.add_argument("--name", required=True, help="项目名称")
    parser.add_argument("--description", default="", help="项目描述")
    parser.add_argument("--author", default="", help="作者")
    parser.add_argument("--output", default=".", help="输出目录")
    
    args = parser.parse_args()
    
    generator = ProjectGenerator(args.name, args.output)
    result = generator.generate(args.description, args.author)
    
    print(f"\n✅ 项目创建成功！")
    print(f"📁 项目目录: {result['project_dir']}")
    print(f"📄 创建文件: {len(result['created_files'])} 个")
    print(f"📂 创建目录: {len(result['created_dirs'])} 个")


if __name__ == "__main__":
    main()