# 测试目录

本目录包含框架的测试代码。

## 测试结构

```
tests/
├── unit/               # 单元测试
│   ├── test_dispatcher.py
│   ├── test_state_machine.py
│   ├── test_message_bus.py
│   └── test_memory.py
├── integration/        # 集成测试
│   └── test_workflow.py
└── e2e/               # 端到端测试
    └── test_full_flow.py
```

## 运行测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行特定测试
pytest tests/unit/test_state_machine.py

# 带覆盖率
pytest --cov=tools --cov-report=html
```

## 测试规范

- 使用 pytest 框架
- 测试文件以 `test_` 开头
- 测试类以 `Test` 开头
- 测试方法以 `test_` 开头
- 每个测试应该独立，不依赖其他测试