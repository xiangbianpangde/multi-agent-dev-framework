# Git提交规范

> **版本**: 1.0.0
> **用途**: 多Agent项目开发的版本控制规范

---

## 一、提交信息格式

### 1.1 基本格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 1.2 类型说明

| 类型 | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(auth): 添加JWT认证 |
| fix | Bug修复 | fix(api): 修复请求超时问题 |
| docs | 文档更新 | docs(readme): 更新安装说明 |
| style | 代码格式（不影响功能） | style: 格式化代码 |
| refactor | 重构 | refactor(user): 优化查询性能 |
| test | 测试相关 | test(auth): 添加认证测试用例 |
| chore | 构建/工具 | chore: 更新依赖版本 |
| perf | 性能优化 | perf(db): 优化数据库查询 |
| ci | CI/CD相关 | ci: 添加自动化测试 |
| revert | 回滚提交 | revert: 回滚commit abc123 |

### 1.3 范围说明

```
常用范围:
- api          # API相关
- auth         # 认证相关
- core         # 核心模块
- docs         # 文档
- workflow     # 工作流
- memory       # 记忆系统
- agents       # Agent相关
- skills       # 技能相关
- config       # 配置相关
```

---

## 二、提交信息规范

### 2.1 Subject规则

```
┌─────────────────────────────────────────────────────────────┐
│ Subject规则                                                 │
├─────────────────────────────────────────────────────────────┤
│ 1. 使用动词原形开头（add, fix, update, remove等）           │
│ 2. 不超过50个字符                                           │
│ 3. 不以句号结尾                                             │
│ 4. 使用祈使语气                                             │
│ 5. 首字母小写                                               │
└─────────────────────────────────────────────────────────────┘

好:
feat(auth): add JWT token validation
fix(api): resolve timeout issue in request handler
docs: update API documentation

差:
feat(auth): Added JWT token validation.  # 不用过去式，不以句号结尾
fix(api): Fix the timeout issue in request handler which was causing problems  # 太长
```

### 2.2 Body规则

```
┌─────────────────────────────────────────────────────────────┐
│ Body规则                                                    │
├─────────────────────────────────────────────────────────────┤
│ 1. 用空行与Subject分隔                                      │
│ 2. 解释What和Why，不是How                                   │
│ 3. 每行不超过72字符                                         │
│ 4. 可以使用列表格式                                         │
└─────────────────────────────────────────────────────────────┘

示例:
feat(auth): add JWT token validation

Implement JWT-based authentication to improve security
and support stateless API requests.

- Add token generation endpoint
- Implement token validation middleware
- Add token refresh mechanism

This replaces the previous session-based auth which
required server-side session storage.
```

### 2.3 Footer规则

```
用于:
1. 关联Issue
2. 破坏性变更说明

关联Issue:
Closes #123
Fixes #456
Refs #789

破坏性变更:
BREAKING CHANGE: 认证接口返回格式变更
旧格式: {"token": "xxx"}
新格式: {"access_token": "xxx", "refresh_token": "yyy"}

示例:
feat(auth): change token response format

BREAKING CHANGE: The authentication endpoint now returns
both access_token and refresh_token instead of just token.

Clients need to update their token handling logic.

Closes #123
```

---

## 三、提交示例

### 3.1 功能开发

```bash
# 新功能
feat(user): add user registration endpoint

Add REST API endpoint for user registration with:
- Email validation
- Password strength check
- Duplicate email detection

Closes #42

# 功能完善
feat(task): add task priority support

Allow users to set priority levels (1-5) for tasks.
Priority affects task scheduling order.

- Add priority field to Task model
- Update task scheduler to consider priority
- Add priority filter in task list API
```

### 3.2 Bug修复

```bash
# Bug修复
fix(api): resolve race condition in task dispatcher

The task dispatcher had a race condition when multiple
agents tried to claim the same task simultaneously.

Solution: Use Redis distributed lock for task claiming.

Fixes #156

# 紧急修复
fix(security): patch SQL injection vulnerability

An SQL injection vulnerability was found in the user
search API. This commit adds parameterized queries.

Reported-by: Security Team
```

### 3.3 文档更新

```bash
# 文档更新
docs: update installation guide for Docker deployment

- Add Docker Compose example
- Update environment variables documentation
- Add troubleshooting section

# API文档
docs(api): add OpenAPI specification

Add OpenAPI 3.0 specification for all API endpoints.
```

### 3.4 重构

```bash
# 重构
refactor(memory): extract memory interface

Extract Memory interface from implementation to support
multiple storage backends.

- Define Memory abstract base class
- Implement FileMemory and RedisMemory
- Update MemoryManager to use interface
```

### 3.5 性能优化

```bash
# 性能优化
perf(db): optimize user query performance

Add composite index on (status, created_at) to speed up
common query patterns.

Before: ~500ms for 1M records
After: ~50ms for 1M records
```

---

## 四、分支规范

### 4.1 分支命名

```
分支类型:
- main          # 生产分支
- develop       # 开发分支
- feature/*     # 功能分支
- fix/*         # Bug修复分支
- release/*     # 发布分支
- hotfix/*      # 紧急修复分支

命名规则:
feature/<issue-id>-<short-description>
fix/<issue-id>-<short-description>
release/<version>
hotfix/<issue-id>-<short-description>

示例:
feature/123-user-authentication
fix/456-timeout-issue
release/1.2.0
hotfix/789-security-patch
```

### 4.2 分支策略

```
                    main
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
release/1.1     release/1.2       hotfix/xxx
    │                 │                 │
    └────────┬────────┴────────┬────────┘
             │                 │
          develop         develop
             │                 │
    ┌────────┼────────┐       │
    │        │        │       │
feature/A feature/B feature/C  │
    │        │        │        │
    └────────┴────────┴────────┘
             │
          develop

流程:
1. 从develop创建feature分支
2. 功能开发完成后合并回develop
3. develop稳定后创建release分支
4. release测试通过后合并到main和develop
5. 紧急问题从main创建hotfix分支
```

### 4.3 分支操作

```bash
# 创建功能分支
git checkout develop
git checkout -b feature/123-user-auth

# 开发过程中保持同步
git fetch origin
git rebase origin/develop

# 完成后合并
git checkout develop
git merge --no-ff feature/123-user-auth
git push origin develop

# 删除已合并分支
git branch -d feature/123-user-auth
```

---

## 五、合并规范

### 5.1 Merge Commit

```bash
# 使用--no-ff保留分支历史
git merge --no-ff feature/123-user-auth

# 合并信息格式
Merge branch 'feature/123-user-auth' into develop

Add user authentication feature with JWT support.
```

### 5.2 Pull Request

```markdown
## PR标题
feat(auth): add user authentication

## 变更说明
- 添加JWT认证功能
- 实现登录/注册API
- 添加权限中间件

## 测试情况
- [x] 单元测试已通过
- [x] 集成测试已通过
- [x] 手动测试已完成

## 相关Issue
Closes #123

## 检查清单
- [x] 代码符合规范
- [x] 已添加必要注释
- [x] 已更新相关文档
```

### 5.3 Code Review

```
审查要点:
├── 功能正确性
├── 代码质量
├── 测试覆盖
├── 文档完整
├── 安全问题
└── 性能问题

审查意见格式:
- [MUST] 必须修改
- [SHOULD] 建议修改
- [NIT] 小问题（可选）
- [QUESTION] 问题/疑问

示例:
- [MUST] 这里需要添加输入验证
- [SHOULD] 建议使用异步处理提高性能
- [NIT] 变量名可以更具描述性
```

---

## 六、版本标签

### 6.1 版本号规则

```
格式: 主版本号.次版本号.修订号[-预发布标识]

示例:
- 1.0.0        正式版本
- 1.1.0        新增功能
- 1.1.1        Bug修复
- 2.0.0        重大更新
- 1.0.0-alpha  内部测试版
- 1.0.0-beta   公开测试版
- 1.0.0-rc.1   候选版本

规则:
- 主版本号: 不兼容的API变更
- 次版本号: 向后兼容的功能新增
- 修订号: 向后兼容的问题修复
```

### 6.2 标签操作

```bash
# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0

# 推送所有标签
git push origin --tags

# 删除标签
git tag -d v1.0.0
git push origin --delete v1.0.0

# 查看标签
git tag -l
git show v1.0.0
```

### 6.3 变更日志

```markdown
# Changelog

## [1.1.0] - 2026-03-24

### Added
- JWT认证功能
- 任务优先级支持
- 实时监控看板

### Changed
- 优化数据库查询性能
- 更新API响应格式

### Fixed
- 修复任务调度器竞争条件
- 修复内存泄漏问题

### Security
- 修复SQL注入漏洞

## [1.0.0] - 2026-03-01

### Added
- 初始版本发布
- 三省六部核心功能
```

---

## 七、钩子配置

### 7.1 Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### 7.2 Commit-msg

```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# 检查格式
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|test|chore|perf|ci|revert)(\(.+\))?: .{1,50}"; then
    echo "错误: 提交信息格式不正确"
    echo "格式: <type>(<scope>): <subject>"
    echo "示例: feat(auth): add JWT authentication"
    exit 1
fi
```

---

*最后更新: 2026-03-24*