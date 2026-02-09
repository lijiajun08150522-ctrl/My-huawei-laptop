# AI 皮肤一直加载 - 问题诊断和解决方案

## 问题现象

点击 "AI 生成皮肤" 按钮后，加载动画一直显示，无法完成。

## 可能原因

### 1. 后端 API 未正常响应

**诊断方法:**
```bash
python debug_skin_generation.py
```

这会测试完整的后端流程。

### 2. 前端轮询逻辑问题

**可能的问题:**
- `setInterval` 的错误处理导致轮询停止
- 图片加载失败
- CORS 问题

### 3. 后端状态未更新

**可能的问题:**
- 模拟生成器的状态转换有问题
- `get_skin_status` 返回的状态不正确

## 快速解决方案

### 方案 1: 使用调试脚本测试后端

```bash
python debug_skin_generation.py
```

如果后端正常，问题在前端。如果后端异常，问题在后端。

### 方案 2: 检查浏览器控制台

1. 打开浏览器开发者工具（F12）
2. 切换到 Console 标签
3. 点击 "AI 生成皮肤" 按钮
4. 查看错误信息

**常见错误:**
- `Failed to fetch` - 后端未启动或网络问题
- `TypeError: Cannot read property 'image_url'` - 响应格式错误
- `Image load failed` - 图片 URL 无效

### 方案 3: 手动测试 API

#### 测试生成接口
```bash
curl -X POST http://127.0.0.1:5000/api/skin/generate -H "Content-Type: application/json" -d "{\"player_id\":\"test\"}"
```

#### 测试状态接口
```bash
curl http://127.0.0.1:5000/api/skin/status/<task_id>
```

#### 测试当前皮肤接口
```bash
curl http://127.0.0.1:5000/api/skin/current
```

## 前端调试步骤

### 1. 添加日志输出

在 `snake_game.html` 中找到 `pollSkinStatus` 函数，添加日志：

```javascript
async function pollSkinStatus(taskId) {
    console.log('[DEBUG] 开始轮询:', taskId);

    const maxAttempts = 60;
    let attempts = 0;

    const pollInterval = setInterval(async () => {
        attempts++;
        console.log(`[DEBUG] 轮询 ${attempts}/${maxAttempts}`);

        try {
            const response = await fetch(`/api/skin/status/${taskId}`);
            console.log('[DEBUG] 响应状态:', response.status);

            if (!response.ok) {
                throw new Error('查询状态失败');
            }

            const result = await response.json();
            console.log('[DEBUG] 响应数据:', result);

            // 更新进度
            if (result.progress !== undefined) {
                updateLoadingProgress(result.progress);
            }

            // 检查是否完成
            if (result.status === 'completed') {
                console.log('[DEBUG] 生成完成，开始加载图片');
                clearInterval(pollInterval);

                await loadSkinTexture(result.image_url);

                localStorage.setItem('snakeGameSkin', result.image_url);

                hideSkinLoading();

                alert('AI 皮肤生成成功！已应用到游戏。');

                draw();

            } else if (result.status === 'failed') {
                console.log('[DEBUG] 生成失败');
                clearInterval(pollInterval);
                throw new Error(result.message || '生成失败');

            } else if (attempts >= maxAttempts) {
                console.log('[DEBUG] 超时');
                clearInterval(pollInterval);
                throw new Error('生成超时');
            }

        } catch (error) {
            console.error('[DEBUG] 轮询异常:', error);
            clearInterval(pollInterval);
            throw error;
        }

    }, 1000);
}
```

### 2. 检查图片加载

在 `loadSkinTexture` 函数中添加日志：

```javascript
async function loadSkinTexture(imageUrl) {
    console.log('[DEBUG] 开始加载图片:', imageUrl);

    return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = 'anonymous';

        img.onload = () => {
            console.log('[DEBUG] 图片加载成功');
            // 创建离屏 canvas
            const tempCanvas = document.createElement('canvas');
            const tempCtx = tempCanvas.getContext('2d');
            tempCanvas.width = GRID_SIZE;
            tempCanvas.height = GRID_SIZE;

            tempCtx.drawImage(img, 0, 0, GRID_SIZE, GRID_SIZE);

            gameState.skinTexture = tempCanvas;
            console.log('[DEBUG] 皮肤纹理已设置');
            resolve();
        };

        img.onerror = () => {
            console.error('[DEBUG] 图片加载失败');
            reject(new Error('图片加载失败'));
        };

        img.src = imageUrl;
    });
}
```

## 后端调试步骤

### 1. 检查模拟生成器

在 `app.py` 启动时查看输出：

```
[INFO] 使用模拟皮肤生成器 (MockSkinGenerator)
```

如果看到这个，说明使用的是模拟模式。

### 2. 添加后端日志

在 `comfyui_client.py` 的 `MockSkinGenerator` 类中添加日志：

```python
def get_skin_status(self, task_id: str) -> Dict[str, Any]:
    """模拟获取状态"""
    print(f"[DEBUG] 查询状态: {task_id}")

    if task_id not in self.tasks:
        print(f"[DEBUG] 任务不存在: {task_id}")
        return {
            "success": False,
            "status": "not_found",
            "message": "任务不存在"
        }

    task = self.tasks[task_id]
    print(f"[DEBUG] 任务状态: {task['status']}")

    if task["status"] == "pending":
        task["status"] = "processing"
        task["progress"] = 50
        print(f"[DEBUG] 转换为 processing 状态")
        return {
            "success": True,
            "task_id": task_id,
            "status": "processing",
            "progress": 50,
            "message": "生成中..."
        }

    if task["status"] == "processing":
        # 模拟图片 URL
        mock_url = self.mock_images[self.mock_index % len(self.mock_images)]
        self.mock_index += 1

        task["status"] = "completed"
        task["progress"] = 100
        task["image_url"] = mock_url

        print(f"[DEBUG] 转换为 completed 状态，URL: {mock_url}")
        return {
            "success": True,
            "task_id": task_id,
            "status": "completed",
            "image_url": mock_url,
            "progress": 100,
            "message": "生成完成"
        }

    # ... 其他代码
```

## 常见问题及解决方法

### 问题 1: 轮询一直在进行

**原因:** 后端状态未从 `processing` 转换为 `completed`

**解决:** 检查模拟生成器的状态转换逻辑

### 问题 2: 图片加载失败

**原因:** 图片 URL 无效或 CORS 问题

**解决:**
- 检查 `image_url` 是否正确
- 确保 CORS 配置正确
- 使用相对路径

### 问题 3: 加载动画不消失

**原因:**
- 错误处理未清除 `setInterval`
- `hideSkinLoading()` 未被调用

**解决:** 确保所有错误分支都调用 `clearInterval(pollInterval)` 和 `hideSkinLoading()`

## 临时解决方案

如果问题无法快速定位，可以临时跳过皮肤加载：

```javascript
async function generateAISkin() {
    // 显示加载动画
    showSkinLoading();

    try {
        // 直接使用模拟图片 URL
        const mockImageUrl = '/api/skin/image/mock_test.png';

        // 等待 2 秒模拟生成
        await new Promise(resolve => setTimeout(resolve, 2000));

        // 加载皮肤
        await loadSkinTexture(mockImageUrl);

        // 保存到本地
        localStorage.setItem('snakeGameSkin', mockImageUrl);

        // 隐藏加载
        hideSkinLoading();

        alert('AI 皮肤生成成功！');

        // 刷新游戏
        draw();

    } catch (error) {
        console.error('生成失败:', error);
        hideSkinLoading();
        alert('生成失败: ' + error.message);
    }
}
```

## 获取帮助

请提供以下信息以便进一步诊断：

1. 浏览器控制台错误（按 F12）
2. 后端控制台输出
3. `debug_skin_generation.py` 的运行结果
4. 网络请求的状态（开发者工具 Network 标签）
