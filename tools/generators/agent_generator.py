#!/usr/bin/env python3
"""
Agent生成器 - 自动生成Agent配置和人格文件

功能：
- 生成Agent SOUL.md人格文件
- 生成agents.json配置片段
- 支持自定义模板

使用：
    python agent_generator.py --id "agent_name" --name "显示名称" --role "角色"
"""

import argparse
import json
from pathlib import Path
from typing import Optional, List


class AgentGenerator:
    """Agent生成器"""
    
    ROLES = {
        "decision": {
            "name": "决策调度",
            "department": "decision_layer",
            "capabilities": ["requirement_analysis", "planning", "coordination"]
        },
        "audit": {
            "name": "监察审核", 
            "department": "audit_layer",
            "capabilities": ["quality_review", "security_audit", "standard_check"]
        },
        "execution": {
            "name": "执行实施",
            "department": "execution_layer",
            "capabilities": ["task_execution", "result_reporting"]
        }
    }
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
    
    def generate_soul(self, agent_id: str, name: str, role: str, 
                      description: str = "", capabilities: List[str] = None,
                      model_primary: str = "gpt-4", model_fallback: str = "claude-3") -> str:
        """生成SOUL.md文件"""
        
        role_info = self.ROLES.get(role, self.ROLES["execution"])
        caps = capabilities or role_info["capabilities"]
        
        content = f'''# {name} - {role_info["name"]}

> {description or f"负责{role_info['name']}相关工作"}

## 身份

- **ID**: {agent_id}
- **名称**: {name}
- **部门**: {role_info["department"]}
- **角色**: {role_info["name"]}

## 职责

### 核心职责
{self._format_capabilities(caps)}

### 边界
- 不做: [定义不做的事情]
- 转交: [需要转交的工作]

## 工作流

### 输入
- 来源: [消息来源]
- 格式: [输入格式]

### 处理
1. [步骤1]
2. [步骤2]
3. [步骤3]

### 输出
- 格式: [输出格式]
- 目标: [输出目标]

## 沟通规则

### 可接收消息
- 来自: [来源Agent列表]
- 类型: [消息类型列表]

### 可发送消息
- 目标: [目标Agent列表]
- 类型: [消息类型列表]

## 技能

### 已安装技能
- [skill_1]: [简述]

## 输出规范

### 格式要求
- [格式规范]

### 质量标准
- [质量标准]

## 示例

### 示例输入
```
[输入示例]
```

### 示例输出
```
[输出示例]
```

---

*人格定义版本: 1.0.0*
*最后更新: {self._get_date()}*
'''
        return content
    
    def generate_config(self, agent_id: str, name: str, role: str,
                        description: str = "", capabilities: List[str] = None,
                        model_primary: str = "gpt-4", model_fallback: str = "claude-3",
                        can_send_to: List[str] = None, can_receive_from: List[str] = None,
                        can_create_task: bool = False, can_approve: bool = False) -> dict:
        """生成Agent配置"""
        
        role_info = self.ROLES.get(role, self.ROLES["execution"])
        caps = capabilities or role_info["capabilities"]
        
        config = {
            "id": agent_id,
            "name": name,
            "role": role,
            "department": role_info["department"],
            "description": description or f"{role_info['name']}部门",
            "model": {
                "primary": model_primary,
                "fallback": model_fallback
            },
            "capabilities": caps,
            "skills": [],
            "permissions": {
                "can_send_to": can_send_to or [],
                "can_receive_from": can_receive_from or [],
                "can_create_task": can_create_task,
                "can_approve": can_approve
            }
        }
        
        return config
    
    def create_agent(self, agent_id: str, name: str, role: str, **kwargs):
        """创建完整的Agent（文件+配置）"""
        
        # 创建目录
        agent_dir = self.output_dir / "agents" / agent_id
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成并保存SOUL.md
        soul_content = self.generate_soul(agent_id, name, role, **kwargs)
        soul_path = agent_dir / "SOUL.md"
        soul_path.write_text(soul_content, encoding="utf-8")
        
        # 生成配置
        config = self.generate_config(agent_id, name, role, **kwargs)
        
        return {
            "soul_path": str(soul_path),
            "config": config
        }
    
    def _format_capabilities(self, capabilities: List[str]) -> str:
        """格式化能力列表"""
        return "\n".join(f"- {cap}" for cap in capabilities)
    
    def _get_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(description="Agent生成器")
    parser.add_argument("--id", required=True, help="Agent ID")
    parser.add_argument("--name", required=True, help="Agent显示名称")
    parser.add_argument("--role", required=True, choices=["decision", "audit", "execution"], help="Agent角色")
    parser.add_argument("--description", default="", help="Agent描述")
    parser.add_argument("--model-primary", default="gpt-4", help="主模型")
    parser.add_argument("--model-fallback", default="claude-3", help="备用模型")
    parser.add_argument("--output", default=".", help="输出目录")
    
    args = parser.parse_args()
    
    generator = AgentGenerator(args.output)
    result = generator.create_agent(
        agent_id=args.id,
        name=args.name,
        role=args.role,
        description=args.description,
        model_primary=args.model_primary,
        model_fallback=args.model_fallback
    )
    
    print(f"\n✅ Agent创建成功！")
    print(f"📄 SOUL.md: {result['soul_path']}")
    print(f"\n📝 配置片段:")
    print(json.dumps(result['config'], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()