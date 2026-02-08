# 贪吃蛇 AI 皮肤生成器 - 功能说明

## 功能概述

为贪吃蛇游戏添加 AI 皮肤生成功能，玩家可以通过点击按钮调用 AI 服务生成个性化游戏皮肤，生成的皮肤会自动应用到蛇头和蛇身。

---

## 核心功能

### 1. AI 皮肤生成按钮

**位置**: 游戏页面顶部 header 区域
**样式**: 渐变紫色按钮，带 hover 效果
**功能**: 点击后触发 AI 皮肤生成流程

```html
<button class="header-btn ai-skin-btn" onclick="generateAISkin()">
    ✨ AI 生成皮肤
</button>
```

---

### 2. 加载动画

**组件**:
- 遮罩层 - 覆盖整个游戏区域
- 旋转加载器 - 紫色旋转动画
- 进度提示 - 显示当前进度百分比和状态文字

**进度提示**:
- 0% - 准备中...
- 10% - 上传请求...
- 30-70% - AI 正在生成...
- 90% - 即将完成...
- 100% - 加载图片...

---

### 3. API 调用流程

#### 步骤 1: 提交生成任务

```javascript
POST /api/agent
Content-Type: application/json

{
  "prompt": "a cute cartoon snake skin with colorful pattern",
  "style": "cartoon",
  "width": 512,
  "height": 512,
  "player_id": "player_12345"
}

响应:
{
  "success": true,
  "task_id": "task_xxx",
  "status": "pending"
}
```

#### 步骤 2: 轮询查询状态

```javascript
GET /api/agent/status/{task_id}

进行中:
{
  "success": true,
  "status": "processing",
  "progress": 65
}

已完成:
{
  "success": true,
  "status": "completed",
  "progress": 100,
  "image_url": "http://127.0.0.1:5000/api/skin/image/task_xxx.png"
}
```

#### 步骤 3: 加载图片纹理

```javascript
// 创建 Image 对象
const img = new Image();
img.crossOrigin = 'anonymous';

// 图片加载完成后
img.onload = () => {
    // 调整大小到网格大小 (20x20)
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    tempCanvas.width = GRID_SIZE;
    tempCanvas.height = GRID_SIZE;

    // 绘制并缩放图片
    tempCtx.drawImage(img, 0, 0, GRID_SIZE, GRID_SIZE);

    // 保存为纹理
    gameState.skinTexture = tempCanvas;
};

img.src = imageUrl;
```

#### 步骤 4: 应用到游戏

```javascript
function drawSnake() {
    gameState.snake.forEach((segment, index) => {
        if (gameState.skinTexture) {
            // 使用纹理绘制
            const pattern = ctx.createPattern(gameState.skinTexture, 'repeat');
            ctx.fillStyle = pattern;
        } else {
            // 默认颜色
            ctx.fillStyle = index === 0 ? '#2E7D32' : '#4CAF50';
        }

        ctx.fillRect(
            segment.x * GRID_SIZE + 1,
            segment.y * GRID_SIZE + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        );
    });
}
```

---

### 4. 本地存储

皮肤 URL 会保存到 `localStorage`，下次访问游戏时自动加载：

```javascript
// 保存皮肤
localStorage.setItem('snakeGameSkin', imageUrl);

// 读取皮肤
const savedSkin = localStorage.getItem('snakeGameSkin');
if (savedSkin) {
    loadSkinTexture(savedSkin);
}
```

---

## 前端函数列表

| 函数 | 说明 |
|------|------|
| `generateAISkin()` | AI 皮肤生成主函数 |
| `pollSkinStatus(taskId)` | 轮询任务状态 |
| `loadSkinTexture(imageUrl)` | 加载图片纹理 |
| `showSkinLoading()` | 显示加载动画 |
| `hideSkinLoading()` | 隐藏加载动画 |
| `updateLoadingProgress(progress)` | 更新进度提示 |

---

## 使用方法

### 1. 启动游戏

```bash
python app.py
```

### 2. 访问游戏

```
http://localhost:5000/game
```

### 3. 生成皮肤

1. 点击顶部的 "✨ AI 生成皮肤" 按钮
2. 等待生成完成（约 30 秒）
3. 皮肤自动应用到游戏
4. 成功提示显示

### 4. 保存效果

生成的皮肤会自动保存到本地，下次访问游戏时会自动加载。

---

## 错误处理

### 1. 重复点击防护

```javascript
if (gameState.isSkinLoading) {
    return; // 阻止重复点击
}
```

### 2. API 错误捕获

```javascript
try {
    const response = await fetch('/api/agent', {...});
    if (!response.ok) {
        throw new Error('生成失败: ' + response.statusText);
    }
} catch (error) {
    alert('AI 皮肤生成失败: ' + error.message);
    hideSkinLoading();
}
```

### 3. 超时处理

最多轮询 60 次（约 60 秒），超时后自动取消。

### 4. 图片加载失败

```javascript
img.onerror = () => {
    reject(new Error('图片加载失败'));
};
```

---

## 待实现的后端接口

### 1. POST /api/agent

**功能**: 提交 AI 皮肤生成任务

**请求体**:
```json
{
  "prompt": "a cute cartoon snake skin",
  "style": "cartoon",
  "width": 512,
  "height": 512,
  "player_id": "player_123"
}
```

**响应**:
```json
{
  "success": true,
  "task_id": "task_xxx",
  "status": "pending"
}
```

### 2. GET /api/agent/status/{task_id}

**功能**: 查询生成状态

**响应 (进行中)**:
```json
{
  "success": true,
  "status": "processing",
  "progress": 65
}
```

**响应 (完成)**:
```json
{
  "success": true,
  "status": "completed",
  "progress": 100,
  "image_url": "http://127.0.0.1:5000/api/skin/image/task_xxx.png"
}
```

---

## 技术实现

### 前端技术
- **HTML5 Canvas** - 游戏渲染和纹理应用
- **Fetch API** - API 请求
- **localStorage** - 本地存储
- **CSS3 Animation** - 加载动画

### 后端技术（待实现）
- **Flask** - Web 框架
- **ComfyUI** - AI 图像生成
- **JSON** - 数据交换格式

---

## 文件清单

| 文件 | 说明 |
|------|------|
| `snake_game.html` | 游戏主页面（已更新） |
| `SKIN_GENERATOR_SDD.md` | SDD 软件设计规约 |
| `comfyui_client.py` | ComfyUI 客户端 |
| `test_ai_skin_api.py` | API 测试脚本 |
| `AI_SKIN_FEATURE.md` | 本文档 |

---

## Git 提交

```
e0d419c feat: add AI skin generator to snake game
```

---

**功能已完成！** 🎉

前端已完全实现，等待后端 API 接口开发完成后即可正常使用。
