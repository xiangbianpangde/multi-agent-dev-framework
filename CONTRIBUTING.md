# 贡献指南

感谢你对多Agent项目开发框架的关注！

## 如何贡献

### 报告问题

如果你发现了bug或有功能建议：

1. 在 [Issues](https://github.com/xiangbianpangde/multi-agent-dev-framework/issues) 页面搜索是否已有类似问题
2. 如果没有，创建新的Issue，包含：
   - 清晰的标题
   - 问题描述
   - 复现步骤（如果是bug）
   - 期望结果

### 提交代码

1. Fork 本仓库
2. 创建功能分支
   ```bash
   git checkout -b feature/your-feature
   ```
3. 进行修改
4. 提交代码（遵循提交规范）
   ```bash
   git commit -m "feat: 添加新功能描述"
   ```
5. 推送到你的仓库
   ```bash
   git push origin feature/your-feature
   ```
6. 创建 Pull Request

### 提交规范

使用以下格式：

```
<type>(<scope>): <subject>

type:
- feat: 新功能
- fix: Bug修复
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

示例:
- feat(tools): 添加新的项目生成器功能
- fix(core): 修复状态机转换bug
- docs: 更新README
```

### 代码规范

- 遵循 PEP 8 规范
- 添加类型注解
- 编写文档字符串
- 添加必要的测试

### 文档规范

- 使用 Markdown 格式
- 保持文档更新
- 添加必要的示例

## 开发环境

```bash
# 克隆仓库
git clone https://github.com/xiangbianpangde/multi-agent-dev-framework.git

# 进入目录
cd multi-agent-dev-framework

# 安装依赖
pip install -r requirements.txt
```

## 项目结构

```
multi-agent-dev-framework/
├── engineering-knowledge-base/  # 知识库文档
├── tools/                       # 工具代码
│   ├── cli.py                  # CLI入口
│   ├── generators/             # 生成器
│   └── templates/              # 模板
├── examples/                    # 示例
└── tests/                       # 测试
```

## 联系方式

- 提交 Issue: https://github.com/xiangbianpangde/multi-agent-dev-framework/issues
- Pull Request: https://github.com/xiangbianpangde/multi-agent-dev-framework/pulls

---

感谢你的贡献！