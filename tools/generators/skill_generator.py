#!/usr/bin/env python3
"""
Skill生成器 - 自动生成技能模块模板

功能：
- 生成Skill目录结构
- 生成SKILL.md文档
- 生成代码模板

使用：
    python skill_generator.py --name "skill_name" --description "功能描述"
"""

import argparse
import json
from pathlib import Path
from typing import Optional, List, Dict


class SkillGenerator:
    """Skill生成器"""
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
    
    def generate_skill_md(self, name: str, description: str, 
                          params: List[Dict] = None, examples: List[Dict] = None) -> str:
        """生成SKILL.md"""
        
        params = params or []
        examples = examples or []
        
        content = f'''# {self._to_title(name)}

> {description}

## 功能说明

{description}

## 参数说明

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
{self._format_params_table(params)}

## 使用方法

### 命令行
```bash
/skill {name} --param1 value1
```

### API调用
```python
from skills.{name}.src.main import {self._to_class(name)}Skill

skill = {self._to_class(name)}Skill()
result = skill.execute(param1="value1")
```

## 输出格式

```json
{{
  "status": "success",
  "result": {{
    "key": "value"
  }}
}}
```

## 注意事项

- 注意事项1
- 注意事项2

## 示例

{self._format_examples(examples)}

## 更新日志

- v1.0.0 ({self._get_date()}): 初始版本
'''
        return content
    
    def generate_code(self, name: str, description: str, params: List[Dict] = None) -> str:
        """生成代码模板"""
        
        class_name = self._to_class(name)
        params = params or []
        
        # 生成参数验证代码
        param_validation = ""
        if params:
            for p in params:
                if p.get("required"):
                    param_validation += f'''
        if "{p['name']}" not in kwargs:
            raise ValueError("缺少必需参数: {p['name']}")'''
        
        # 生成执行逻辑
        content = f'''"""
{name} - {description}
"""
from typing import Dict, Any, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class {class_name}Result:
    """执行结果"""
    status: str
    message: str
    data: Dict[str, Any] = None


class {class_name}Skill:
    """{description}"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {{}}
        self.name = "{name}"
        self.version = "1.0.0"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            {self._format_params_docstring(params)}
        
        Returns:
            执行结果
        """
        # 验证参数
        self._validate_params(kwargs)
        
        try:
            # 执行主要逻辑
            result = self._execute_core(kwargs)
            
            return {{
                "status": "success",
                "result": result
            }}
        
        except Exception as e:
            logger.error(f"执行失败: {{e}}")
            return {{
                "status": "error",
                "message": str(e)
            }}
    
    def _validate_params(self, params: Dict[str, Any]) -> None:
        """验证参数"""{param_validation}
        pass
    
    def _execute_core(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行核心逻辑"""
        # TODO: 实现具体逻辑
        return {{
            "message": "执行成功"
        }}
    
    def get_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        return {{
            "name": self.name,
            "version": self.version,
            "description": self.__doc__
        }}


# 快速测试
if __name__ == "__main__":
    skill = {class_name}Skill()
    print(skill.get_info())
'''
        return content
    
    def create_skill(self, name: str, description: str, 
                     params: List[Dict] = None, examples: List[Dict] = None) -> dict:
        """创建完整的Skill"""
        
        # 创建目录结构
        skill_dir = self.output_dir / "skills" / name
        src_dir = skill_dir / "src"
        tests_dir = skill_dir / "tests"
        
        skill_dir.mkdir(parents=True, exist_ok=True)
        src_dir.mkdir(exist_ok=True)
        tests_dir.mkdir(exist_ok=True)
        
        # 生成SKILL.md
        skill_md = self.generate_skill_md(name, description, params, examples)
        skill_md_path = skill_dir / "SKILL.md"
        skill_md_path.write_text(skill_md, encoding="utf-8")
        
        # 生成__init__.py
        init_py = f'"""{name} skill"""\nfrom .main import {self._to_class(name)}Skill\n'
        (src_dir / "__init__.py").write_text(init_py, encoding="utf-8")
        
        # 生成main.py
        code = self.generate_code(name, description, params)
        (src_dir / "main.py").write_text(code, encoding="utf-8")
        
        # 生成测试文件
        test_code = self._generate_test(name, description)
        (tests_dir / f"test_{name}.py").write_text(test_code, encoding="utf-8")
        (tests_dir / "__init__.py").write_text("", encoding="utf-8")
        
        return {
            "skill_dir": str(skill_dir),
            "skill_md": str(skill_md_path),
            "main_py": str(src_dir / "main.py"),
            "test_py": str(tests_dir / f"test_{name}.py")
        }
    
    def _generate_test(self, name: str, description: str) -> str:
        """生成测试文件"""
        class_name = self._to_class(name)
        
        return f'''"""
{name}技能测试
"""
import pytest
from skills.{name}.src.main import {class_name}Skill


class Test{class_name}Skill:
    """{description}测试"""
    
    @pytest.fixture
    def skill(self):
        return {class_name}Skill()
    
    def test_get_info(self, skill):
        """测试获取技能信息"""
        info = skill.get_info()
        
        assert info["name"] == "{name}"
        assert info["version"] == "1.0.0"
    
    def test_execute_success(self, skill):
        """测试执行成功"""
        result = skill.execute()
        
        assert result["status"] == "success"
    
    # TODO: 添加更多测试用例
'''
    
    def _format_params_table(self, params: List[Dict]) -> str:
        """格式化参数表格"""
        if not params:
            return "| - | - | - | - | - |"
        
        rows = []
        for p in params:
            rows.append(f"| {p.get('name', '')} | {p.get('type', 'any')} | {'是' if p.get('required') else '否'} | {p.get('default', '-')} | {p.get('description', '')} |")
        return "\n".join(rows)
    
    def _format_params_docstring(self, params: List[Dict]) -> str:
        """格式化参数文档字符串"""
        if not params:
            return "**kwargs: 其他参数"
        
        lines = []
        for p in params:
            lines.append(f"{p.get('name', '')}: {p.get('description', '')}")
        return "\n            ".join(lines)
    
    def _format_examples(self, examples: List[Dict]) -> str:
        """格式化示例"""
        if not examples:
            return "暂无示例"
        
        content = []
        for i, ex in enumerate(examples, 1):
            content.append(f'''### 示例{i}: {ex.get('title', '')}
输入:
```
{ex.get('input', '')}
```

输出:
```
{ex.get('output', '')}
```''')
        return "\n\n".join(content)
    
    def _to_class(self, name: str) -> str:
        """转换为类名"""
        return "".join(word.capitalize() for word in name.split("_"))
    
    def _to_title(self, name: str) -> str:
        """转换为标题"""
        return " ".join(word.capitalize() for word in name.split("_"))
    
    def _get_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


def main():
    parser = argparse.ArgumentParser(description="Skill生成器")
    parser.add_argument("--name", required=True, help="技能名称")
    parser.add_argument("--description", required=True, help="功能描述")
    parser.add_argument("--output", default=".", help="输出目录")
    parser.add_argument("--params", help="参数JSON")
    
    args = parser.parse_args()
    
    params = json.loads(args.params) if args.params else None
    
    generator = SkillGenerator(args.output)
    result = generator.create_skill(
        name=args.name,
        description=args.description,
        params=params
    )
    
    print(f"\n✅ Skill创建成功！")
    print(f"📁 Skill目录: {result['skill_dir']}")
    print(f"📄 SKILL.md: {result['skill_md']}")
    print(f"📄 main.py: {result['main_py']}")
    print(f"📄 test: {result['test_py']}")


if __name__ == "__main__":
    main()