# 自动Git提交监控脚本

## 功能说明

自动监控当前目录的文件变动，当检测到新文件或文件修改时，自动执行：
1. `git add .` - 添加所有更改到暂存区
2. `git commit` - 提交更改（自动生成提交信息）
3. `git push` - 推送到远程仓库

## 安装依赖

```bash
pip install watchdog
```

或使用requirements文件：
```bash
pip install -r requirements_monitor.txt
```

## 使用方法

### 基本用法

在项目根目录（Git仓库）运行：

```bash
python auto_git_monitor.py
```

### 自定义忽略模式

可以传递额外的忽略模式：

```bash
python auto_git_monitor.py "*.log" "build/" "dist/"
```

### 停止监控

按 `Ctrl+C` 停止监控

## 默认忽略的文件/目录

以下文件和目录会被自动忽略（不会触发提交）：

- `__pycache__/` - Python缓存目录
- `.git/` - Git目录
- `.pytest_cache/` - Pytest缓存
- `.idea/` - IntelliJ IDEA配置
- `.vscode/` - VSCode配置
- `node_modules/` - Node.js依赖
- `*.pyc` - Python编译文件
- `*.pyo` - Python优化文件
- `*.pyd` - Python动态链接库
- `.DS_Store` - macOS系统文件
- `Thumbs.db` - Windows缩略图
- `*.tmp` - 临时文件
- `auto_git_monitor.py` - 监控脚本自身

## 功能特性

### 1. 智能防抖

- 设置了3秒的防抖延迟
- 3秒内的多次文件变动只会触发一次提交
- 避免频繁提交

### 2. 自动提交信息

根据文件操作类型自动生成提交信息：

- **新建文件**: `feat: add filename - timestamp`
- **修改文件**: `update: modify filename - timestamp`
- **删除文件**: `delete: remove filename - timestamp`
- **其他**: `chore: auto commit changes - timestamp`

### 3. 完整的操作流程

```
[1/5] 检查Git仓库状态
[2/5] 添加更改到暂存区
[3/5] 提交更改
[4/5] 推送到远程仓库
[5/5] 显示最新提交
```

### 4. 错误处理

- 自动检测Git仓库
- 捕获并显示错误信息
- 提供可能的错误原因

## 使用场景

### 场景1：实时同步开发进度

在开发新功能时，保存文件后自动提交到GitHub，确保代码安全。

### 场景2：多人协作

团队成员修改文件后，自动推送最新的更改，便于其他人拉取。

### 场景3：自动化文档

修改Markdown文档后，自动提交到仓库，保持文档版本同步。

## 注意事项

### 1. Git配置

确保已配置Git用户信息：

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 2. 远程仓库

确保已配置远程仓库：

```bash
git remote add origin git@github.com:username/repo.git
```

### 3. 网络连接

需要稳定的网络连接才能成功推送到远程仓库。

### 4. 认证

如果使用HTTPS方式推送，可能需要：
- 在推送时输入用户名和密码
- 或使用SSH密钥（推荐）

## 高级用法

### 修改防抖延迟

编辑 `auto_git_monitor.py`，修改 `self.debounce_seconds` 的值：

```python
self.debounce_seconds = 5  # 改为5秒
```

### 添加自定义忽略模式

编辑 `ignore_patterns` 列表：

```python
self.ignore_patterns = gitignore_patterns or [
    '__pycache__',
    # ... 其他默认模式
    'your_custom_pattern',  # 添加自定义模式
]
```

### 修改提交信息格式

编辑 `commit_and_push` 方法中的提交信息生成逻辑。

## 故障排除

### 问题1：推送失败

**错误**: `git push 失败`

**可能原因**:
1. 网络连接问题
2. 远程仓库未配置
3. 认证失败

**解决方案**:
1. 检查网络连接
2. 配置远程仓库: `git remote -v`
3. 使用SSH密钥或更新认证信息

### 问题2：没有更改需要提交

**错误**: `没有需要提交的更改`

**说明**: 这是正常的，说明文件已被忽略或在`.gitignore`中。

### 问题3：Python模块找不到

**错误**: `ModuleNotFoundError: No module named 'watchdog'`

**解决方案**:
```bash
pip install watchdog
```

## 示例输出

```
============================================================
自动Git提交监控脚本
============================================================
✓ Git仓库检查通过
✓ 监控目录: /path/to/your/project
✓ 开始监控文件变动...

提示:
  - 按 Ctrl+C 停止监控
  - 新文件或文件修改将自动触发 git add/commit/push
  - 防抖延迟: 3秒（3秒内的多次变动只触发一次提交）
============================================================

[CREATE] 检测到新文件: test.txt

============================================================
开始执行Git操作
============================================================

[1/5] 检查Git仓库状态...
    检测到更改:
      ?? test.txt

[2/5] 添加更改到暂存区...
    ✓ git add 成功

[3/5] 提交更改...
    ✓ 提交成功: feat: add test.txt - 2026-01-24 12:00:00

[4/5] 推送到远程仓库...
    ✓ 推送成功

[5/5] 显示最新提交...
    最新提交: a1b2c3d feat: add test.txt - 2026-01-24 12:00:00

============================================================
✓ Git操作完成
============================================================
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
