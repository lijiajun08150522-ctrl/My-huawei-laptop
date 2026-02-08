# 贪吃蛇智能皮肤生成器 - 快速参考

## 项目概述

为贪吃蛇游戏设计智能皮肤生成器，玩家通过输入描述文本（prompt），系统通过 ComfyUI API 生成个性化游戏皮肤。

---

## 核心文件

| 文件 | 说明 |
|------|------|
| `SKIN_GENERATOR_SDD.md` | 完整的 SDD 软件设计规约 |
| `comfyui_client.py` | ComfyUI API 客户端实现 |
| `test_skin_demo.py` | API 模拟演示脚本 |

---

## API 接口

### 1. 生成皮肤
```
POST /api/skin/generate
Content-Type: application/json

请求:
{
  "prompt": "a cute cartoon snake skin with rainbow colors",
  "style": "cartoon",
  "width": 512,
  "height": 512,
  "player_id": "player_123"
}

响应 (202 Accepted):
{
  "success": true,
  "message": "皮肤生成任务已提交",
  "data": {
    "task_id": "task_xxx",
    "status": "pending",
    "estimated_time": 30
  }
}
```

### 2. 查询状态
```
GET /api/skin/status/{task_id}

响应 - 进行中:
{
  "success": true,
  "data": {
    "status": "processing",
    "progress": 65
  }
}

响应 - 已完成:
{
  "success": true,
  "data": {
    "status": "completed",
    "progress": 100,
    "image_url": "http://127.0.0.1:5000/api/skin/image/task_xxx.png",
    "generation_time": 28
  }
}
```

### 3. 获取图片
```
GET /api/skin/image/{filename}
响应: 二进制 PNG 图片数据
Content-Type: image/png
```

---

## ComfyUI 工作流

### 工作流节点

```
[3] CheckpointLoaderSimple - 加载 SD 1.5 模型
[4] CLIPLoader - 加载 CLIP 编码器
[6] CLIPTextEncode - 编码正向 prompt
[7] CLIPTextEncode - 编码负向 prompt
[5] EmptyLatentImage - 创建潜在空间
[10] KSampler - 采样生成器
[8] VAELoader - 加载 VAE 解码器
[9] VAEDecode - 解码为图片
[11] SaveImage - 保存图片
```

### 示例 prompt

```
正向: "a cute cartoon snake skin with rainbow colors"
负向: "low quality, blurry, distorted, ugly"
```

---

## 测试演示

### 运行测试
```bash
python test_skin_demo.py
```

### 测试场景
1. 提交生成任务 - 成功
2. 查询生成状态 - 进行中
3. 查询生成状态 - 已完成（返回图片 URL）
4. 获取历史记录
5. 错误处理 - prompt 为空
6. 错误处理 - ComfyUI 服务不可用

---

## 核心功能

- [x] ComfyUI API 集成
- [x] prompt 参数传递
- [x] 异步任务管理
- [x] 状态查询和进度跟踪
- [x] 图片存储和 URL 返回
- [x] 错误处理和验证
- [x] 历史记录管理
- [x] 多种风格支持

---

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | 是 | 皮肤描述文本（1-500字符） |
| `style` | string | 否 | 风格：cartoon, realistic, pixel_art |
| `width` | integer | 否 | 图片宽度（默认512，范围256-1024） |
| `height` | integer | 否 | 图片高度（默认512，范围256-1024） |
| `player_id` | string | 否 | 玩家ID |

---

## 返回结果

### 成功返回图片 URL
```json
{
  "image_url": "http://127.0.0.1:5000/api/skin/image/task_xxx.png",
  "thumbnail_url": "http://127.0.0.1:5000/api/skin/thumbnail/task_xxx.png"
}
```

### 错误返回
```json
{
  "success": false,
  "message": "ComfyUI 服务不可用",
  "error_code": "COMFYUI_UNAVAILABLE"
}
```

---

## 快速开始

### 1. 查看 SDD 规约
```bash
cat SKIN_GENERATOR_SDD.md
```

### 2. 运行演示
```bash
python test_skin_demo.py
```

### 3. 集成到 Flask 应用
```python
from comfyui_client import SkinGenerator

generator = SkinGenerator()
success, task_id, message = generator.generate_skin(
    prompt="a cute cartoon snake skin",
    player_id="player_123"
)
```

---

## ComfyUI 服务

### 本地安装
```bash
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt
python main.py --listen 0.0.0.0 --port 8188
```

### 环境变量
```bash
export COMFYUI_URL=http://127.0.0.1:8188
```

---

## 文档索引

| 文档 | 说明 |
|------|------|
| SDD 软件设计规约 | `SKIN_GENERATOR_SDD.md` |
| ComfyUI 客户端 | `comfyui_client.py` |
| 测试演示 | `test_skin_demo.py` |
| 快速参考 | `SKIN_GENERATOR_QUICKREF.md` |

---

**设计完成！** 所有文档和代码已提交到 Git 仓库。
