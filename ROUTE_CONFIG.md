# Flask 路由配置说明

## 当前路由配置

### 主应用路由

| 路由 | 方法 | 说明 | 文件路径 | 返回方式 |
|------|------|------|----------|----------|
| `/` | GET | 首页 | `templates/index.html` | `render_template` |
| `/game` | GET | 贪吃蛇游戏 | `snake_game.html` | `send_from_directory` |
| `/tasks` | GET | 任务管理器 | `web/index.html` | `send_from_directory` |
| `/presentation` | GET | 实训报告 | `presentation.html` | `send_from_directory` |

### API 路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/api/tasks` | GET | 获取所有任务 |
| `/api/tasks` | POST | 添加任务 |
| `/api/tasks/<int:task_id>/done` | PUT | 标记任务完成 |
| `/api/tasks/<int:task_id>` | DELETE | 删除任务 |
| `/api/tasks/completed/clear` | DELETE | 清除已完成任务 |
| `/api/stats` | GET | 获取统计信息 |
| `/api/report/export` | GET | 导出报表 |
| `/api/skin/generate` | POST | 生成皮肤 |
| `/api/skin/status/<task_id>` | GET | 查询皮肤生成状态 |
| `/api/skin/image/<filename>` | GET | 获取皮肤图片 |
| `/api/skin/current` | GET | 获取当前皮肤 |
| `/api/skin/apply` | POST | 应用皮肤 |
| `/api/skin/history` | GET | 获取皮肤历史 |

## 文件返回方式说明

### 1. render_template (推荐用于模板文件)

```python
@app.route('/')
def index():
    return render_template('index.html')
```

**特点:**
- 文件必须放在 `templates/` 文件夹
- 支持模板引擎（Jinja2）
- 可以传递变量到模板
- 默认的 Flask 推荐方式

**适用场景:**
- 动态页面
- 需要传递数据的页面
- 使用模板语法的页面

### 2. send_from_directory (推荐用于静态文件)

```python
from flask import send_from_directory

@app.route('/game')
def game():
    return send_from_directory('.', 'snake_game.html')
```

**特点:**
- 文件可以放在任意目录
- 返回原始文件内容
- 不处理模板语法
- 支持相对路径和绝对路径

**适用场景:**
- 纯静态 HTML 文件
- 不需要模板处理的页面
- 文件不在 `templates/` 文件夹

**示例:**
```python
# 返回项目根目录的文件
return send_from_directory('.', 'snake_game.html')

# 返回子目录的文件
return send_from_directory('web', 'index.html')

# 返回特定目录的文件
return send_from_directory('/path/to/files', 'index.html')
```

### 3. send_static_file (仅用于 static 文件夹)

```python
@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)
```

**特点:**
- 文件必须在 `static/` 文件夹
- 不支持 `../` 相对路径
- 通常用于 CSS、JS、图片等资源

**适用场景:**
- CSS 样式文件
- JavaScript 脚本文件
- 图片、字体等静态资源
- **不推荐用于返回 HTML 页面**

**注意事项:**
- ⚠️ 不支持 `../` 路径
- ⚠️ 不能返回 `static/` 外的文件
- ⚠️ 返回 HTML 页面可能导致问题

## 常见问题

### 问题 1: 404 Not Found

**可能原因:**
1. 文件路径不正确
2. 使用了错误的返回方法
3. 文件不存在

**解决方法:**
```python
# 错误 ❌
@app.route('/game')
def game():
    return app.send_static_file('../snake_game.html')

# 正确 ✅
@app.route('/game')
def game():
    return send_from_directory('.', 'snake_game.html')
```

### 问题 2: 文件存在但返回 404

**检查清单:**
1. 确认文件路径正确
2. 使用 `send_from_directory` 而不是 `send_static_file`
3. 检查文件名大小写
4. 确认文件有读取权限

### 问题 3: 模板语法未生效

**可能原因:**
使用了 `send_from_directory` 返回模板文件

**解决方法:**
```python
# 如果文件需要模板处理，使用 render_template
@app.route('/page')
def page():
    return render_template('page.html', data=variable)
```

## 最佳实践

### 1. 项目结构建议

```
SummerProject/
├── app.py
├── templates/              # 模板文件
│   ├── index.html
│   └── base.html
├── static/               # 静态资源
│   ├── css/
│   ├── js/
│   └── images/
├── web/                 # Web 应用页面
│   └── index.html
├── snake_game.html       # 独立游戏页面
├── presentation.html     # 独立报告页面
└── ...
```

### 2. 路由选择指南

| 场景 | 推荐方法 | 示例 |
|------|----------|------|
| 动态页面 | `render_template` | `return render_template('index.html')` |
| 纯静态页面 | `send_from_directory` | `return send_from_directory('.', 'page.html')` |
| CSS/JS/图片 | `send_static_file` 或 `send_from_directory` | `return send_from_directory('static/css', 'style.css')` |

### 3. 性能优化

对于静态文件，建议设置缓存：
```python
@app.route('/game')
def game():
    response = send_from_directory('.', 'snake_game.html')
    response.cache_control.max_age = 3600  # 缓存 1 小时
    return response
```

## 调试技巧

### 1. 打印文件路径

```python
import os

@app.route('/debug')
def debug():
    print(f"Current directory: {os.getcwd()}")
    print(f"Root path: {app.root_path}")
    print(f"Static folder: {app.static_folder}")
    print(f"Template folder: {app.template_folder}")
    return "Check console"
```

### 2. 检查文件是否存在

```python
import os

@app.route('/game')
def game():
    file_path = os.path.join('.', 'snake_game.html')
    if not os.path.exists(file_path):
        return f"File not found: {file_path}", 404
    return send_from_directory('.', 'snake_game.html')
```

### 3. 使用绝对路径

```python
import os

@app.route('/game')
def game():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'snake_game.html')
    return send_from_directory(base_dir, 'snake_game.html')
```

## 测试脚本

使用 `test_server.py` 测试所有路由：

```bash
python test_server.py
```

这会测试：
- 首页 (`/`)
- 贪吃蛇游戏 (`/game`)
- 任务管理器 (`/tasks`)
- 实训报告 (`/presentation`)
