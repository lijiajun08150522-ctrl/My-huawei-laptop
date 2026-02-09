# 贪吃蛇 AI 皮肤生成功能 - 实现说明

## 概述

本文档描述了 feature-skin 分支的实现，包括 ComfyUI API 集成和贪吃蛇皮肤注入功能。

## 功能特性

1. **ComfyUI API 集成** - 调用 ComfyUI 服务生成 AI 皮肤
2. **赛博朋克风格提示词** - 固定提示词生成高质量皮肤
3. **自动皮肤注入** - 生成完成后自动应用到游戏
4. **模拟模式** - 无需 ComfyUI 服务即可测试
5. **加载动画** - 前端加载进度提示

## 固定提示词

```text
Neon glowing snake, cyberpunk style, high resolution
```

## 后端 API 接口

### 1. POST /api/skin/generate
**功能**: 提交皮肤生成任务

**请求**:
```json
{
  "player_id": "player_001"
}
```

**响应**:
```json
{
  "success": true,
  "task_id": "mock_task_1234567890",
  "message": "皮肤生成任务已提交（模拟模式）",
  "prompt": "Neon glowing snake, cyberpunk style, high resolution"
}
```

### 2. GET /api/skin/status/<task_id>
**功能**: 查询皮肤生成状态

**响应** (进行中):
```json
{
  "success": true,
  "task_id": "mock_task_1234567890",
  "status": "processing",
  "progress": 50,
  "message": "生成中..."
}
```

**响应** (已完成):
```json
{
  "success": true,
  "task_id": "mock_task_1234567890",
  "status": "completed",
  "image_url": "http://127.0.0.1:5000/api/skin/image/mock_task_1234567890.png",
  "progress": 100,
  "message": "生成完成"
}
```

### 3. GET /api/skin/image/<filename>
**功能**: 获取皮肤图片

**响应**: PNG 图片数据

**模拟模式**: 自动生成赛博朋克风格的占位图

### 4. GET /api/skin/current
**功能**: 获取当前贪吃蛇皮肤 URL

**响应**:
```json
{
  "success": true,
  "skin_url": "http://127.0.0.1:5000/api/skin/image/mock_task_1234567890.png"
}
```

### 5. POST /api/skin/apply
**功能**: 应用皮肤到游戏

**请求**:
```json
{
  "image_url": "http://127.0.0.1:5000/api/skin/image/mock_task_1234567890.png"
}
```

**响应**:
```json
{
  "success": true,
  "message": "皮肤已应用",
  "skin_url": "http://127.0.0.1:5000/api/skin/image/mock_task_1234567890.png"
}
```

### 6. GET /api/skin/history
**功能**: 获取皮肤生成历史

**参数**:
- `player_id`: 玩家 ID
- `page`: 页码（默认 1）
- `limit`: 每页数量（默认 10）

**响应**:
```json
{
  "success": true,
  "total": 0,
  "page": 1,
  "limit": 10,
  "skins": []
}
```

## 前端实现

### 初始化流程

1. 读取本地存储的皮肤
2. 如果没有保存的皮肤，轮询 `/api/skin/current` 获取服务器皮肤
3. 加载皮肤纹理到游戏

### 生成皮肤流程

```
用户点击 "AI 生成皮肤" 按钮
    ↓
显示加载动画
    ↓
POST /api/skin/generate
    ↓
获取 task_id
    ↓
每秒轮询 GET /api/skin/status/{task_id}
    ↓
更新进度 (0% -> 100%)
    ↓
获取 image_url
    ↓
加载皮肤纹理到游戏
    ↓
保存到 localStorage
    ↓
刷新游戏界面
    ↓
隐藏加载动画
```

### 核心函数

| 函数 | 功能 |
|------|------|
| `generateAISkin()` | 生成皮肤主函数 |
| `pollSkinStatus(taskId)` | 轮询任务状态 |
| `loadSkinTexture(imageUrl)` | 加载图片纹理 |
| `pollCurrentSkin()` | 轮询获取服务器皮肤 |
| `showSkinLoading()` | 显示加载动画 |
| `hideSkinLoading()` | 隐藏加载动画 |

## 环境配置

### 模拟模式 (默认)

无需 ComfyUI 服务，直接使用模拟生成器。

```bash
# 启动服务
python app.py

# 访问游戏
http://localhost:5000/game
```

### 真实 ComfyUI 模式

需要安装并启动 ComfyUI 服务。

```bash
# 1. 设置环境变量
set USE_MOCK_SKIN_GENERATOR=false
set COMFYUI_URL=http://127.0.0.1:8188

# 2. 启动 ComfyUI 服务
cd ComfyUI
python main.py --listen 0.0.0.0 --port 8188

# 3. 启动 Flask 服务
python app.py
```

## 测试

运行测试脚本验证功能：

```bash
python test_snake_skin_api.py
```

测试内容：
1. ✅ 生成皮肤
2. ✅ 查询生成状态
3. ✅ 获取当前皮肤
4. ✅ 应用皮肤到游戏
5. ✅ 获取皮肤历史

## 全局变量

### 后端

```python
snake_skin_url: str  # 当前贪吃蛇皮肤 URL
```

当皮肤生成完成后，自动更新此变量。

### 前端

```javascript
gameState.skinTexture  # 皮肤纹理对象
```

用于在绘制蛇时应用纹理。

## 文件结构

```
SummerProject/
├── app.py                          # Flask 后端（新增 6 个接口）
├── comfyui_client.py               # ComfyUI 客户端
├── snake_game.html                 # 贪吃蛇游戏前端（修改）
├── test_snake_skin_api.py         # API 测试脚本（新增）
├── data/skins/                    # 皮肤存储目录
└── FEATURE_SKIN_IMPLEMENTATION.md  # 本文档
```

## 皮肤应用原理

### 后端

1. 皮肤生成完成后，更新全局变量 `snake_skin_url`
2. 前端通过 `/api/skin/current` 接口获取最新皮肤

### 前端

1. `loadSkinTexture()` 函数加载图片为 Canvas Pattern
2. `drawSnake()` 函数使用纹理绘制蛇头和蛇身
3. 皮肤保存到 localStorage，下次访问自动加载

## 加载动画

### UI 组件

- 遮罩层 (`skinLoadingOverlay`)
- 旋转加载动画 (`loading-spinner`)
- 进度文字提示 (`loading-text`, `loading-progress`)

### 进度提示

| 进度 | 提示信息 |
|------|----------|
| 0% | 准备中... |
| 10% | 上传请求... |
| 30% | AI 正在生成... |
| 50% | 生成中... |
| 70% | 生成中... |
| 90% | 即将完成... |
| 100% | 加载图片... |

## 模拟模式特性

- 无需 ComfyUI 服务
- 自动生成赛博朋克风格的占位图
- 包含霓虹网格、渐变纹理、发光文字
- 完整的 API 模拟
- 适用于开发和测试

## 注意事项

1. **环境变量**: 默认使用模拟模式，可通过环境变量切换
2. **超时处理**: 轮询最多 60 秒，超时后自动停止
3. **错误处理**: 前端和后端都有完整的错误处理机制
4. **本地存储**: 皮肤保存到 localStorage，持久化存储
5. **刷新游戏**: 皮肤加载完成后自动刷新游戏界面

## 开发建议

1. **先测试模拟模式**: 使用模拟模式快速开发和测试
2. **再集成真实 ComfyUI**: 功能稳定后再集成真实 AI 服务
3. **性能优化**: 可考虑缓存皮肤图片，避免重复加载
4. **样式调整**: 根据需求调整占位图样式和提示信息

## 下一步

- [ ] 添加皮肤收藏功能
- [ ] 支持自定义提示词
- [ ] 添加皮肤预览功能
- [ ] 支持多种皮肤风格
- [ ] 添加皮肤分享功能
