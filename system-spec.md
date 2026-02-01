# 系统设计规约文档 (System Specification)

**文档版本**: v1.0  
**创建日期**: 2026-01-30  
**最后更新**: 2026-01-30  
**项目名称**: CodeBuddy - 智能任务管理系统  

---

## 文档目录

1. [项目概述](#1-项目概述)
2. [系统架构](#2-系统架构)
3. [核心模块设计](#3-核心模块设计)
4. [API接口规范](#4-api接口规范)
5. [数据模型](#5-数据模型)
6. [UI设计规范](#6-ui设计规范)
7. [集成方案](#7-集成方案)
8. [技术规范](#8-技术规范)
9. [部署方案](#9-部署方案)
10. [测试规范](#10-测试规范)

---

## 1. 项目概述

### 1.1 项目目标

构建一个集任务管理、智能分析、游戏娱乐于一体的综合应用系统，提供Web端和移动端多端访问能力。

### 1.2 核心功能模块

| 模块名称 | 功能描述 | 技术栈 |
|---------|---------|--------|
| **任务管理器** | 任务CRUD、优先级、分类、状态管理 | Python Flask |
| **贪吃蛇游戏** | 经典贪吃蛇游戏、关卡系统、得分排名 | HTML5 + JavaScript |
| **数据分析** | 任务统计、分类报表、完成率分析 | Python Analytics |
| **Web界面** | 响应式Web UI、移动端适配 | HTML5 + CSS3 |
| **微信小程序** | 微信小程序客户端 | 微信小程序框架 |

### 1.3 技术架构图

```
┌─────────────────────────────────────────────────────────┐
│                    用户层 (User Layer)                    │
├─────────────────────────────────────────────────────────┤
│  Web浏览器  │  移动端浏览器  │  微信小程序  │  CLI终端    │
└─────────────┴───────────────┴─────────────┴──────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│                    表现层 (Presentation)                  │
├─────────────────────────────────────────────────────────┤
│  Web界面 (index.html)  │  游戏页面 (snake.html)        │
│  小程序页面  │  CLI命令行界面                             │
└─────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│                   应用层 (Application)                   │
├─────────────────────────────────────────────────────────┤
│  Flask Web服务 (app.py)  │  任务管理器 (task.py)        │
│  分析服务 (analytics.py) │  数据验证 (validators.py)   │
│  存储服务 (storage.py)   │  常量定义 (constants.py)    │
└─────────────────────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│                   数据层 (Data Layer)                     │
├─────────────────────────────────────────────────────────┤
│  JSON文件存储 (tasks.json)  │  LocalStorage (Web)        │
│  微信云存储 (可选)          │  数据库 (可选扩展)         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 系统架构

### 2.1 分层架构设计

#### 2.1.1 表现层 (Presentation Layer)

**职责**: 负责用户界面展示和用户交互

**组件**:
- **Web界面** (`web/index.html`): 任务管理的Web UI
- **游戏界面** (`snake_game.html`): 贪吃蛇游戏页面
- **小程序界面**: 微信小程序客户端
- **CLI界面**: 命令行交互界面

**技术规范**:
- 响应式设计，支持桌面端(≥768px)和移动端(<768px)
- 统一的色彩系统和组件样式
- 移动优先的触摸交互设计

#### 2.1.2 应用层 (Application Layer)

**职责**: 业务逻辑处理和协调

**模块划分**:

| 模块 | 文件 | 职责 |
|------|------|------|
| **任务管理器** | `task.py` | 任务CRUD、状态管理 |
| **Web服务** | `app.py` | REST API、路由处理 |
| **分析服务** | `analytics.py` | 统计分析、报表生成 |
| **数据验证** | `validators.py` | 输入验证、格式检查 |
| **存储服务** | `storage.py` | 数据持久化、备份管理 |
| **常量定义** | `constants.py` | 统一常量管理 |

#### 2.1.3 数据层 (Data Layer)

**职责**: 数据存储和访问

**存储策略**:
- **主存储**: JSON文件 (`tasks.json`)
- **备份存储**: JSON备份文件 (`tasks.json.backup`)
- **Web缓存**: LocalStorage (浏览器本地存储)
- **游戏数据**: LocalStorage (最高分)

### 2.2 模块依赖关系

```
app.py (Web服务)
    ├── task.py (任务管理器)
    │       ├── analytics.py (分析服务)
    │       ├── storage.py (存储服务)
    │       ├── validators.py (验证器)
    │       └── constants.py (常量)
    │
    └── snake_game.html (游戏页面 - 独立)
            └── LocalStorage (游戏数据)
```

### 2.3 设计原则

1. **单一职责原则**: 每个模块只负责一个明确的功能
2. **开闭原则**: 对扩展开放，对修改关闭
3. **依赖倒置**: 依赖抽象而非具体实现 (如 `TaskStorage` 接口)
4. **接口隔离**: 细粒度接口，避免胖接口
5. **最少知识原则**: 模块间耦合度最小化

---

## 3. 核心模块设计

### 3.1 任务管理器模块

#### 3.1.1 类设计

```python
class Task:
    """任务数据模型"""
    - id: int                    # 唯一标识
    - description: str           # 任务描述
    - status: str                # 状态 (pending/done)
    - priority: str              # 优先级 (High/Medium/Low)
    - category: str              # 分类 (Work/Study/Life/General)
    - createdAt: str             # 创建时间 (ISO 8601)
    - completedAt: str           # 完成时间 (ISO 8601)
    
    + to_dict() -> dict
    + from_dict(data: dict) -> Task


class TaskManager:
    """任务管理器核心类"""
    - tasks: List[Task]
    - storage: TaskStorage
    - analyzer: TaskAnalyzerService
    
    + add(description: str) -> str
    + list() -> List[str]
    + done(task_id: int) -> str
    + delete(task_id: int) -> str
    + clear() -> str
    - _find_task(task_id: int) -> Optional[Task]
    - _load_tasks()
    - _save_tasks()
```

#### 3.1.2 核心流程

```
添加任务流程:
用户输入 → 验证器验证 → 创建Task对象 → 添加到列表 → 保存存储 → 返回结果

完成任务流程:
用户输入 → 查找任务 → 更新状态 → 更新完成时间 → 保存存储 → 返回结果

删除任务流程:
用户输入 → 验证ID → 查找任务 → 从列表移除 → 保存存储 → 返回结果
```

### 3.2 分析服务模块

#### 3.2.1 类设计

```python
class TaskStatistics:
    """统计计算器"""
    - tasks: List[Task]
    
    + calculate_total() -> int
    + calculate_completed() -> int
    + calculate_pending() -> int
    + get_completion_rate() -> float
    + get_stats_by_category() -> Dict[str, int]
    + get_priority_distribution() -> Dict[str, int]


class TaskAnalyzer:
    """智能分析器"""
    - statistics: TaskStatistics
    
    + check_task_overload(threshold: int) -> bool
    + get_overload_warning(threshold: int) -> Optional[str]
    + get_completion_rate() -> float


class ReportGenerator:
    """报表生成器"""
    - tasks: List[Task]
    - analyzer: TaskAnalyzer
    
    + generate_summary() -> str
    + generate_full_report() -> str
    + format_statistics() -> str
    + format_category_stats() -> str
    + export_to_txt(filepath: str) -> str


class TaskAnalyzerService:
    """分析服务统一入口"""
    - task_manager: TaskManager
    - statistics: TaskStatistics
    - analyzer: TaskAnalyzer
    - report_generator: ReportGenerator
    
    + get_today_report() -> str
    + export_summary(filepath: str) -> str
    + get_statistics() -> Dict
    + check_overload_warning(threshold: int) -> Optional[str]
```

#### 3.2.2 统计指标

| 指标名称 | 计算公式 | 说明 |
|---------|---------|------|
| **总任务数** | `len(tasks)` | 所有任务数量 |
| **已完成数** | `count(t.status == 'done')` | 已完成任务数 |
| **待办数** | `count(t.status == 'pending')` | 待办任务数 |
| **完成率** | `已完成数 / 总任务数 * 100` | 百分比 (0-100) |
| **分类统计** | `group by category` | 各分类任务数 |
| **优先级分布** | `group by priority` | 各优先级任务数 |

### 3.3 Web服务模块

#### 3.3.1 路由设计

| 路由 | 方法 | 功能 | 请求体 | 响应 |
|------|------|------|--------|------|
| `/` | GET | 首页 | - | HTML页面 |
| `/api/tasks` | GET | 获取任务列表 | - | `{success, tasks[]}` |
| `/api/tasks` | POST | 添加任务 | `{description, priority?, category?}` | `{success, message, task}` |
| `/api/tasks/<id>/done` | PUT | 标记完成 | - | `{success, message}` |
| `/api/tasks/<id>` | DELETE | 删除任务 | - | `{success, message}` |
| `/api/tasks/completed/clear` | DELETE | 清除已完成 | - | `{success, message}` |
| `/api/stats` | GET | 获取统计 | - | `{success, stats}` |
| `/api/report/export` | GET | 导出报表 | - | `{success, message, filepath}` |

#### 3.3.2 统一响应格式

```json
{
    "success": true,
    "message": "操作成功",
    "data": { ... }
}

// 错误响应
{
    "success": false,
    "message": "错误描述",
    "error": "详细错误信息"
}
```

### 3.4 贪吃蛇游戏模块

#### 3.4.1 游戏状态

```javascript
const gameState = {
    snake: [{x, y}, {x, y}, ...],  // 蛇身坐标数组
    direction: {x, y},              // 当前移动方向
    food: {x, y},                   // 食物坐标
    score: 0,                       // 当前得分
    level: 1,                       // 当前关卡
    speed: 200,                     // 移动速度(ms)
    isRunning: false,               // 游戏是否运行
    isPaused: false,                // 游戏是否暂停
    highScore: 0                     // 最高分
};
```

#### 3.4.2 游戏逻辑

```
游戏主循环:
    ├─ 移动蛇身
    │   └─ 计算新头部坐标
    ├─ 碰撞检测
    │   ├─ 撞墙检测
    │   └─ 撞自己检测
    ├─ 食物检测
    │   ├─ 吃到食物: 增长、得分、生成新食物
    │   └─ 关卡检查: 每5个食物升级
    └─ 绘制界面
```

#### 3.4.3 关卡系统

| 关卡 | 速度 (ms) | 升级条件 |
|------|----------|---------|
| Level 1 | 200 | 初始 |
| Level 2 | 180 | 5个食物 |
| Level 3 | 160 | 10个食物 |
| Level 4 | 140 | 15个食物 |
| Level 5 | 120 | 20个食物 |
| Level 6 | 100 | 25个食物 |
| Level 7 | 90 | 30个食物 |
| Level 8 | 80 | 35个食物 |
| Level 9 | 70 | 40个食物 |
| Level 10 | 60 | 45个食物 |

---

## 4. API接口规范

### 4.1 通用规范

#### 4.1.1 基础URL
```
生产环境: http://<your-domain>:5000
开发环境: http://localhost:5000
局域网: http://<local-ip>:5000
```

#### 4.1.2 请求头
```
Content-Type: application/json
Accept: application/json
```

#### 4.1.3 HTTP状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 4.2 任务管理API

#### 4.2.1 获取任务列表

**请求**
```
GET /api/tasks
```

**响应**
```json
{
    "success": true,
    "tasks": [
        {
            "id": 1,
            "description": "完成项目文档",
            "status": "pending",
            "priority": "High",
            "category": "Work",
            "createdAt": "2026-01-30T10:00:00Z",
            "completedAt": null
        }
    ]
}
```

#### 4.2.2 添加任务

**请求**
```
POST /api/tasks
Content-Type: application/json

{
    "description": "编写代码",
    "priority": "Medium",
    "category": "Work"
}
```

**响应**
```json
{
    "success": true,
    "message": "Added: 编写代码",
    "task": {
        "id": 2,
        "description": "编写代码",
        "status": "pending",
        "priority": "Medium",
        "category": "Work",
        "createdAt": "2026-01-30T10:05:00Z",
        "completedAt": null
    }
}
```

**错误响应**
```json
{
    "success": false,
    "message": "任务描述不能为空"
}
```

#### 4.2.3 标记任务完成

**请求**
```
PUT /api/tasks/1/done
```

**响应**
```json
{
    "success": true,
    "message": "Task 1 marked as done"
}
```

#### 4.2.4 删除任务

**请求**
```
DELETE /api/tasks/1
```

**响应**
```json
{
    "success": true,
    "message": "Task 1 deleted"
}
```

#### 4.2.5 清除已完成任务

**请求**
```
DELETE /api/tasks/completed/clear
```

**响应**
```json
{
    "success": true,
    "message": "Cleared all completed tasks"
}
```

### 4.3 统计分析API

#### 4.3.1 获取统计信息

**请求**
```
GET /api/stats
```

**响应**
```json
{
    "success": true,
    "stats": {
        "total": 10,
        "completed": 5,
        "pending": 5,
        "completion_rate": 50.0,
        "by_category": {
            "Work": 4,
            "Study": 3,
            "Life": 2,
            "General": 1
        },
        "by_priority": {
            "High": 3,
            "Medium": 4,
            "Low": 3
        }
    }
}
```

#### 4.3.2 导出报表

**请求**
```
GET /api/report/export
```

**响应**
```json
{
    "success": true,
    "message": "报表已导出: D:\\SummerProject\\summary.txt",
    "filepath": "D:\\SummerProject\\summary.txt"
}
```

### 4.4 错误处理

#### 4.4.1 错误响应格式

```json
{
    "success": false,
    "message": "错误描述",
    "error": {
        "code": "ERROR_CODE",
        "details": "详细错误信息"
    }
}
```

#### 4.4.2 错误码

| 错误码 | 说明 |
|--------|------|
| `TASK_NOT_FOUND` | 任务不存在 |
| `EMPTY_DESCRIPTION` | 任务描述为空 |
| `INVALID_ID` | 无效的任务ID |
| `STORAGE_ERROR` | 存储错误 |
| `VALIDATION_ERROR` | 数据验证失败 |

---

## 5. 数据模型

### 5.1 任务数据模型

#### 5.1.1 数据结构

```typescript
interface Task {
    id: number;                    // 唯一标识
    description: string;           // 任务描述 (1-200字符)
    status: 'pending' | 'done';    // 任务状态
    priority: 'High' | 'Medium' | 'Low';  // 优先级
    category: 'Work' | 'Study' | 'Life' | 'General';  // 分类
    createdAt: string;             // 创建时间 (ISO 8601)
    completedAt: string | null;    // 完成时间 (ISO 8601)
}
```

#### 5.1.2 存储格式

```json
[
    {
        "id": 1,
        "description": "完成项目文档",
        "status": "pending",
        "priority": "High",
        "category": "Work",
        "createdAt": "2026-01-30T10:00:00Z",
        "completedAt": null
    },
    {
        "id": 2,
        "description": "编写代码",
        "status": "done",
        "priority": "Medium",
        "category": "Work",
        "createdAt": "2026-01-30T09:00:00Z",
        "completedAt": "2026-01-30T11:00:00Z"
    }
]
```

### 5.2 统计数据模型

```typescript
interface Statistics {
    total: number;                    // 总任务数
    completed: number;                // 已完成数
    pending: number;                  // 待办数
    completion_rate: number;          // 完成率 (0-100)
    by_category: {                    // 分类统计
        [category: string]: number;
    };
    by_priority: {                    // 优先级分布
        [priority: string]: number;
    };
}
```

### 5.3 游戏数据模型

```typescript
interface GameState {
    snake: Array<{x: number, y: number}>;  // 蛇身坐标
    direction: {x: number, y: number};    // 移动方向
    food: {x: number, y: number};         // 食物坐标
    score: number;                         // 得分
    level: number;                         // 关卡
    speed: number;                         // 速度(ms)
    isRunning: boolean;                    // 运行状态
    isPaused: boolean;                     // 暂停状态
    highScore: number;                     // 最高分
}

interface HighScoreRecord {
    score: number;                    // 得分
    level: number;                    // 关卡
    date: string;                     // 日期 (ISO 8601)
}
```

---

## 6. UI设计规范

### 6.1 色彩系统

#### 6.1.1 主色调

| 颜色名称 | 色值 | 用途 |
|---------|------|------|
| **主色** | `#667eea` | 主要操作、按钮、高亮 |
| **辅助色** | `#764ba2` | 渐变辅助、装饰 |
| **成功色** | `#52c41a` | 成功状态、完成标记 |
| **警告色** | `#fa8c16` | 警告提示、高优先级 |
| **错误色** | `#ff4d4f` | 错误状态、删除操作 |
| **中性色** | `#f5f5f5` | 背景、卡片 |
| **文本色** | `#333333` | 主要文本 |

#### 6.1.2 渐变色

```css
/* 主渐变 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 成功渐变 */
background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);

/* 警告渐变 */
background: linear-gradient(135deg, #fa8c16 0%, #d46b08 100%);
```

### 6.2 字体系统

#### 6.2.1 字体家族

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
             'Helvetica Neue', Arial, sans-serif;
```

#### 6.2.2 字体大小

| 元素 | 大小 | 权重 |
|------|------|------|
| **页面标题** | 24px | 600 (semi-bold) |
| **卡片标题** | 18px | 600 (semi-bold) |
| **正文** | 16px | 400 (normal) |
| **辅助文本** | 14px | 400 (normal) |
| **小标签** | 12px | 400 (normal) |

### 6.3 组件规范

#### 6.3.1 按钮

```css
/* 主要按钮 */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 14px 24px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
}

/* 成功按钮 */
.btn-success {
    background: #52c41a;
    color: white;
}

/* 危险按钮 */
.btn-danger {
    background: #ff4d4f;
    color: white;
}
```

#### 6.3.2 卡片

```css
.card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    margin-bottom: 16px;
}
```

#### 6.3.3 输入框

```css
.form-input {
    width: 100%;
    padding: 14px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 16px;
    font-family: inherit;
    transition: all 0.3s;
}

.form-input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
```

### 6.4 响应式设计

#### 6.4.1 断点定义

| 断点名称 | 屏幕宽度 | 说明 |
|---------|---------|------|
| **Mobile** | < 768px | 移动设备 |
| **Tablet** | 768px - 1024px | 平板设备 |
| **Desktop** | ≥ 1024px | 桌面设备 |

#### 6.4.2 移动端适配

```css
/* 移动端优先 */
.container {
    max-width: 100%;
    padding: 16px;
}

/* 平板端 */
@media (min-width: 768px) {
    .container {
        max-width: 768px;
        margin: 0 auto;
    }
}

/* 桌面端 */
@media (min-width: 1024px) {
    .container {
        max-width: 1024px;
        margin: 0 auto;
    }
}
```

### 6.5 动画效果

#### 6.5.1 过渡动画

```css
/* 标准过渡 */
transition: all 0.3s ease;

/* 弹性过渡 */
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* 悬停效果 */
.button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

#### 6.5.2 加载动画

```css
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading {
    animation: spin 1s linear infinite;
}
```

### 6.6 无障碍设计

#### 6.6.1 语义化HTML

```html
<!-- 使用语义化标签 -->
<nav aria-label="主导航">...</nav>
<main aria-label="主内容">...</main>
<aside aria-label="侧边栏">...</aside>
```

#### 6.6.2 键盘导航

```html
<!-- 按钮可访问性 -->
<button type="button" aria-label="删除任务">
    <span aria-hidden="true">🗑️</span>
</button>
```

---

## 7. 集成方案

### 7.1 任务管理器与贪吃蛇游戏集成

#### 7.1.1 集成方式

**方案A: 嵌入式集成**

在任务管理器页面中嵌入贪吃蛇游戏作为"休息模式"。

```html
<!-- 任务管理页面 -->
<div class="task-manager">
    <h1>📝 任务管理器</h1>
    <div class="task-list">...</div>
</div>

<!-- 休息模式按钮 -->
<button onclick="openGame()">🎮 休息一下</button>

<!-- 游戏模态框 -->
<div id="gameModal" class="modal">
    <iframe src="snake_game.html"></iframe>
</div>
```

**方案B: 独立页面链接**

通过导航链接跳转到独立的游戏页面。

```html
<nav>
    <a href="/index.html">任务管理</a>
    <a href="/snake_game.html">贪吃蛇</a>
</nav>
```

**推荐**: 方案B (独立页面)，便于维护和扩展。

#### 7.1.2 数据共享

**游戏成就系统**

将游戏最高分与任务完成度关联：

```javascript
// 从LocalStorage获取任务完成率
function getCompletionRate() {
    const tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
    const completed = tasks.filter(t => t.status === 'done').length;
    return tasks.length > 0 ? (completed / tasks.length) * 100 : 0;
}

// 游戏时显示任务完成率
function showTaskProgress() {
    const rate = getCompletionRate();
    const tip = rate >= 50 ? 
        "已完成50%任务，继续加油！" : 
        "先完成任务再玩游戏吧！";
    
    showToast(tip);
}
```

#### 7.1.3 统一导航栏

```html
<header class="unified-header">
    <div class="logo">CodeBuddy</div>
    <nav class="main-nav">
        <a href="/index.html" class="active">📝 任务</a>
        <a href="/snake_game.html">🎮 游戏</a>
        <a href="/stats.html">📊 统计</a>
    </nav>
</header>
```

### 7.2 Web与小程序集成

#### 7.2.1 共享数据层

**后端API共享**

Web和小程序都调用相同的Flask API：

```javascript
// Web端
fetch('http://localhost:5000/api/tasks')
    .then(res => res.json())
    .then(data => console.log(data));

// 小程序端
wx.request({
    url: 'http://localhost:5000/api/tasks',
    success(res) {
        console.log(res.data);
    }
});
```

#### 7.2.2 同步机制

**数据同步流程**

```
1. 用户在Web端添加任务
   ↓
2. Web端发送POST请求到Flask API
   ↓
3. Flask API更新tasks.json
   ↓
4. 小端刷新时从API获取最新数据
   ↓
5. 数据保持同步
```

**冲突解决策略**

采用"最后写入胜出" (Last Write Wins) 策略：

```python
def add_task(description, priority, category):
    # 检查ID冲突
    existing_ids = [t.id for t in tasks]
    new_id = max(existing_ids, default=0) + 1
    
    # 创建新任务
    task = Task(new_id, description)
    task.priority = priority
    task.category = category
    
    # 保存
    tasks.append(task)
    save_tasks()
    
    return task
```

### 7.3 CLI与Web集成

#### 7.3.1 共享存储

CLI和Web都使用同一个`tasks.json`文件：

```python
# CLI: task.py
manager = TaskManager(filepath="tasks.json")

# Web: app.py
manager = TaskManager(filepath="tasks.json")
```

#### 7.3.2 操作同步

CLI操作后，Web界面刷新即可看到最新数据。

```bash
# CLI添加任务
python task.py add "完成文档"

# Web界面自动刷新 (或手动刷新)
# 显示: [1] 完成文档 (pending)
```

### 7.4 微信小程序集成

#### 7.4.1 小程序架构

```
miniprogram/
├── app.js              # 小程序入口
├── app.json            # 小程序配置
├── app.wxss            # 全局样式
├── pages/              # 页面
│   ├── index/          # 首页
│   ├── tasks/          # 任务列表
│   └── game/           # 游戏页面
└── utils/              # 工具函数
```

#### 7.4.2 API调用封装

```javascript
// utils/api.js
const BASE_URL = 'http://localhost:5000';

function request(url, method, data) {
    return new Promise((resolve, reject) => {
        wx.request({
            url: BASE_URL + url,
            method: method,
            data: data,
            success: (res) => resolve(res.data),
            fail: reject
        });
    });
}

// 导出API
module.exports = {
    getTasks: () => request('/api/tasks', 'GET'),
    addTask: (data) => request('/api/tasks', 'POST', data),
    // ...
};
```

#### 7.4.3 UI复用

将Web UI转换为小程序WXML：

```html
<!-- Web HTML -->
<div class="task-item">
    <input type="checkbox" />
    <span>任务描述</span>
</div>

<!-- 小程序 WXML -->
<view class="task-item">
    <checkbox />
    <text>任务描述</text>
</view>
```

---

## 8. 技术规范

### 8.1 代码规范

#### 8.1.1 Python代码规范

**遵循PEP 8规范**

```python
# 正确的命名
class TaskManager:           # 类名: PascalCase
    def add_task(self):      # 方法名: snake_case
        pass

task_count = 10             # 变量名: snake_case
MAX_TASKS = 100             # 常量: UPPER_SNAKE_CASE

# 文档字符串
def add_task(self, description: str) -> str:
    """
    添加新任务
    
    Args:
        description: 任务描述
        
    Returns:
        添加结果消息
        
    Raises:
        ValueError: 当描述为空时
    """
    pass

# 类型注解
from typing import List, Optional

def get_pending_tasks(self) -> List[Task]:
    pass
```

#### 8.1.2 JavaScript代码规范

**遵循ES6+规范**

```javascript
// 使用const/let，避免var
const API_URL = 'http://localhost:5000';
let tasks = [];

// 箭头函数
const addTask = (description) => {
    return { id: 1, description };
};

// 模板字符串
const message = `任务 "${description}" 已添加`;

// 解构赋值
const { id, description } = task;

// 对象简写
const newTask = { id, description };
```

#### 8.1.3 HTML/CSS规范

**语义化HTML**

```html
<!-- 正确 -->
<nav>
    <ul>
        <li><a href="/">首页</a></li>
        <li><a href="/tasks">任务</a></li>
    </ul>
</nav>

<!-- 避免 -->
<div class="navigation">
    <div class="nav-item">首页</div>
</div>
```

**BEM命名规范**

```css
/* Block */
.task-item { }

/* Element */
.task-item__description { }

/* Modifier */
.task-item--completed { }
```

### 8.2 错误处理规范

#### 8.2.1 Python异常处理

```python
try:
    tasks = storage.load()
except FileNotFoundError:
    # 文件不存在，初始化空列表
    tasks = []
except json.JSONDecodeError as e:
    # JSON格式错误
    raise ValueError(f"Invalid JSON format: {e}")
except Exception as e:
    # 其他错误
    raise Exception(f"Unexpected error: {e}")
```

#### 8.2.2 JavaScript错误处理

```javascript
try {
    const response = await fetch('/api/tasks');
    const data = await response.json();
    return data;
} catch (error) {
    console.error('API Error:', error);
    throw new Error('Failed to fetch tasks');
}
```

### 8.3 测试规范

#### 8.3.1 单元测试

```python
# test_task.py
import unittest
from task import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()
    
    def test_add_task(self):
        result = self.manager.add("Test task")
        self.assertEqual(result, "Added: Test task")
        self.assertEqual(len(self.manager.tasks), 1)
    
    def test_delete_task(self):
        self.manager.add("Test task")
        result = self.manager.delete(1)
        self.assertEqual(result, "Task 1 deleted")
        self.assertEqual(len(self.manager.tasks), 0)
```

#### 8.3.2 API测试

```python
# test_api.py
import unittest
import json
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_get_tasks(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('success', data)
```

---

## 9. 部署方案

### 9.1 本地开发环境

#### 9.1.1 环境要求

- **Python**: 3.8+
- **Node.js**: 14+ (可选，用于构建工具)
- **浏览器**: Chrome, Firefox, Safari最新版

#### 9.1.2 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd SummerProject

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 启动Flask服务
python app.py

# 4. 访问应用
# 本地: http://localhost:5000
# 局域网: http://<local-ip>:5000
```

### 9.2 生产环境部署

#### 9.2.1 使用Gunicorn部署

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务 (4个worker进程)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 后台运行
gunicorn -w 4 -b 0.0.0.0:5000 app:app --daemon
```

#### 9.2.2 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/static/files;
    }
}
```

#### 9.2.3 使用Docker部署

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
# 构建镜像
docker build -t codebuddy:latest .

# 运行容器
docker run -d -p 5000:5000 codebuddy:latest
```

### 9.3 云平台部署

#### 9.3.1 腾讯云部署

1. **创建云服务器 (CVM)**
   - 操作系统: Ubuntu 20.04
   - 规格: 2核4GB

2. **部署步骤**
   ```bash
   # 安装Python环境
   sudo apt update
   sudo apt install python3 python3-pip nginx

   # 克隆项目
   git clone <repository-url>
   cd SummerProject

   # 安装依赖
   pip3 install -r requirements.txt gunicorn

   # 配置systemd服务
   sudo nano /etc/systemd/system/codebuddy.service
   ```

   ```ini
   [Unit]
   Description=CodeBuddy Task Manager
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/SummerProject
   ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   # 启动服务
   sudo systemctl start codebuddy
   sudo systemctl enable codebuddy

   # 配置Nginx
   sudo nano /etc/nginx/sites-available/codebuddy
   ```

3. **配置防火墙**
   - 开放端口: 80, 443, 5000

---

## 10. 测试规范

### 10.1 测试金字塔

```
        /\
       /E2E\        端到端测试 (10%)
      /------\
     /  集成  \      集成测试 (20%)
    /----------\
   /   单元    \    单元测试 (70%)
  /--------------\
```

### 10.2 单元测试

#### 10.2.1 覆盖率要求

- **核心业务逻辑**: ≥ 90%
- **工具函数**: ≥ 100%
- **整体覆盖率**: ≥ 80%

#### 10.2.2 测试示例

```python
import unittest
from task import Task, TaskManager

class TestTask(unittest.TestCase):
    def test_task_creation(self):
        task = Task(1, "Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Test task")
        self.assertEqual(task.status, "pending")

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()
    
    def test_add_task(self):
        result = self.manager.add("Test task")
        self.assertEqual(result, "Added: Test task")
        self.assertEqual(len(self.manager.tasks), 1)
    
    def test_complete_task(self):
        self.manager.add("Test task")
        result = self.manager.done(1)
        self.assertEqual(result, "Task 1 marked as done")
        self.assertEqual(self.manager.tasks[0].status, "done")
```

### 10.3 集成测试

#### 10.3.1 API测试

```python
import unittest
import json
from app import app

class TestTaskAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.testing = True
    
    def test_get_tasks(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_add_task(self):
        response = self.client.post('/api/tasks',
            json={'description': 'Test task'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
```

### 10.4 端到端测试

#### 10.4.1 UI测试示例

```javascript
// 使用Cypress进行E2E测试
describe('Task Manager E2E', () => {
    it('should add and complete a task', () => {
        cy.visit('/');
        cy.contains('添加').click();
        cy.get('input').type('Test task');
        cy.contains('确定').click();
        cy.contains('Test task').should('be.visible');
        cy.get('input[type="checkbox"]').click();
        cy.contains('Test task').should('have.css', 'text-decoration-line', 'line-through');
    });
});
```

---

## 附录

### A. 术语表

| 术语 | 解释 |
|------|------|
| **CRUD** | Create, Read, Update, Delete (增删改查) |
| **REST API** | Representational State Transfer API (表征状态转移接口) |
| **ISO 8601** | 国际标准日期时间格式 |
| **LocalStorage** | 浏览器本地存储API |
| **CLI** | Command Line Interface (命令行界面) |
| **BEM** | Block Element Modifier (CSS命名规范) |

### B. 参考资源

- [Flask官方文档](https://flask.palletsprojects.com/)
- [PEP 8代码规范](https://peps8.org/)
- [RESTful API设计指南](https://restfulapi.net/)
- [微信小程序开发文档](https://developers.weixin.qq.com/miniprogram/dev/framework/)

### C. 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0 | 2026-01-30 | 初始版本 |

### D. 联系方式

- **项目负责人**: [Your Name]
- **邮箱**: [your.email@example.com]
- **项目地址**: [GitHub Repository URL]

---

**文档结束**
