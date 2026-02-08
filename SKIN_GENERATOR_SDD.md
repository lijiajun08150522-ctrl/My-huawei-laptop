# 贪吃蛇智能皮肤生成器 - SDD 软件设计规约

## 📋 文档信息

- **项目名称**: 贪吃蛇智能皮肤生成器
- **版本**: v1.0
- **创建日期**: 2026-02-04
- **文档类型**: SDD (Software Design Document)
- **状态**: 草案

---

## 📌 1. 概述

### 1.1 功能描述
为贪吃蛇游戏开发一个智能皮肤生成器功能，允许玩家通过 AI 生成个性化的游戏皮肤。用户输入描述性文本（prompt），系统通过 ComfyUI API 生成对应的游戏皮肤图片。

### 1.2 核心目标
- 提供个性化游戏皮肤生成
- 支持自然语言描述输入
- 实现与 ComfyUI 的 API 集成
- 提供皮肤预览和应用功能

### 1.3 技术选型
- **前端**: HTML5 + JavaScript + Fetch API
- **后端**: Flask + requests
- **AI 生成**: ComfyUI API
- **图像存储**: 本地文件系统 + URL 映射

---

## 🎯 2. 功能需求

### 2.1 用户功能
- [x] 输入皮肤描述文本
- [x] 提交生成请求
- [x] 查看生成进度
- [x] 预览生成的皮肤
- [x] 应用皮肤到游戏
- [x] 查看历史生成记录

### 2.2 系统功能
- [x] 接收用户的生成请求
- [x] 调用 ComfyUI API
- [x] 生成游戏皮肤图片
- [x] 存储生成的图片
- [x] 返回图片 URL
- [x] 管理皮肤缓存

---

## 🏗️ 3. 系统架构

### 3.1 架构图

```
┌─────────────┐
│   前端界面   │
│  (Web UI)   │
└──────┬──────┘
       │ HTTP/JSON
       ▼
┌─────────────┐
│  Flask API  │
│  (后端服务) │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│  ComfyUI    │
│  (AI 模型)  │
└──────┬──────┘
       │ Image Response
       ▼
┌─────────────┐
│  图片存储   │
│  (本地磁盘) │
└─────────────┘
```

### 3.2 模块划分

#### 3.2.1 前端模块
- **皮肤生成器 UI** (`skin_generator.html`)
- **游戏皮肤管理** (`snake_game.html` 更新)
- **皮肤预览组件**

#### 3.2.2 后端模块
- **API 服务** (`app.py` 新增路由)
- **ComfyUI 客户端** (`comfyui_client.py`)
- **图片存储服务** (`storage.py` 更新)

---

## 📡 4. API 设计规范

### 4.1 ComfyUI API 集成规范

#### 4.1.1 基础信息

```
ComfyUI 服务地址:
- 本地环境: http://127.0.0.1:8188
- 生产环境: 配置化 (可通过环境变量设置)

API 版本: v1
通信协议: HTTP/JSON
```

#### 4.1.2 端点定义

##### 1. 提交生成任务
```http
POST /prompt
Content-Type: application/json
```

**请求参数结构**:
```json
{
  "prompt": {
    "<node_id>": {
      "class_type": "KSampler",
      "inputs": {
        "seed": 42,
        "steps": 20,
        "cfg": 7,
        "sampler_name": "euler",
        "scheduler": "normal",
        "denoise": 1,
        "model": ["<model_node_id>", 0],
        "positive": ["<positive_node_id>", 0],
        "negative": ["<negative_node_id>", 0],
        "latent_image": ["<empty_latent_node_id>", 0]
      }
    },
    "<positive_node_id>": {
      "class_type": "CLIPTextEncode",
      "inputs": {
        "text": "{user_prompt}",
        "clip": ["<clip_node_id>", 0]
      }
    },
    "<negative_node_id>": {
      "class_type": "CLIPTextEncode",
      "inputs": {
        "text": "low quality, blurry, distorted, ugly",
        "clip": ["<clip_node_id>", 0]
      }
    },
    "<empty_latent_node_id>": {
      "class_type": "EmptyLatentImage",
      "inputs": {
        "width": 512,
        "height": 512,
        "batch_size": 1
      }
    },
    "<vae_decode_node_id>": {
      "class_type": "VAEDecode",
      "inputs": {
        "samples": ["<sampler_node_id>", 0],
        "vae": ["<vae_node_id>", 0]
      }
    },
    "<save_image_node_id>": {
      "class_type": "SaveImage",
      "inputs": {
        "images": ["<vae_decode_node_id>", 0],
        "filename_prefix": "snake_skin_{timestamp}"
      }
    }
  },
  "client_id": "{unique_client_id}"
}
```

##### 2. 查询生成进度
```http
GET /history/{prompt_id}
```

**响应示例**:
```json
{
  "{prompt_id}": {
    "outputs": {
      "<node_id>": {
        "images": [
          {
            "filename": "snake_skin_1234567890_00001.png",
            "subfolder": "",
            "type": "output"
          }
        ]
      }
    }
  }
}
```

##### 3. 下载生成的图片
```http
GET /view?filename={filename}&subfolder={subfolder}&type={type}
```

##### 4. 获取系统信息
```http
GET /system_stats
```

**响应示例**:
```json
{
  "queue_remaining": 2,
  "system_status": "running"
}
```

---

### 4.2 应用层 API 设计

#### 4.2.1 生成皮肤 API

##### POST /api/skin/generate

**功能**: 生成贪吃蛇游戏皮肤

**请求头**:
```
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**请求体**:
```json
{
  "prompt": "a cute cartoon snake skin with rainbow colors and stars",
  "style": "cartoon",
  "width": 512,
  "height": 512,
  "player_id": "player_123"
}
```

**请求参数说明**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 皮肤描述文本（1-500字符） |
| `style` | string | ❌ | 风格：cartoon, realistic, pixel_art |
| `width` | integer | ❌ | 图片宽度（默认512，范围256-1024） |
| `height` | integer | ❌ | 图片高度（默认512，范围256-1024） |
| `player_id` | string | ❌ | 玩家ID（用于关联） |

**响应示例**:

**成功响应** (202 Accepted):
```json
{
  "success": true,
  "message": "皮肤生成任务已提交",
  "task_id": "task_20240204_123456",
  "status": "pending",
  "estimated_time": 30
}
```

**错误响应** (400 Bad Request):
```json
{
  "success": false,
  "message": "prompt 不能为空",
  "error_code": "INVALID_PROMPT"
}
```

---

#### 4.2.2 查询生成状态 API

##### GET /api/skin/status/{task_id}

**功能**: 查询皮肤生成状态

**请求头**:
```
Authorization: Bearer {jwt_token}
```

**响应示例**:

**进行中** (200 OK):
```json
{
  "success": true,
  "task_id": "task_20240204_123456",
  "status": "processing",
  "progress": 65,
  "current_step": 13,
  "total_steps": 20,
  "message": "生成中..."
}
```

**已完成** (200 OK):
```json
{
  "success": true,
  "task_id": "task_20240204_123456",
  "status": "completed",
  "image_url": "/api/skin/image/task_20240204_123456.png",
  "thumbnail_url": "/api/skin/thumbnail/task_20240204_123456.png",
  "prompt": "a cute cartoon snake skin with rainbow colors",
  "created_at": "2026-02-04T12:34:56Z",
  "generation_time": 28
}
```

**失败** (200 OK):
```json
{
  "success": false,
  "task_id": "task_20240204_123456",
  "status": "failed",
  "error": "ComfyUI 服务不可用",
  "error_code": "COMFYUI_UNAVAILABLE"
}
```

**状态说明**:

| 状态 | 说明 |
|------|------|
| `pending` | 任务已提交，等待处理 |
| `processing` | 正在生成中 |
| `completed` | 生成完成 |
| `failed` | 生成失败 |

---

#### 4.2.3 获取图片 API

##### GET /api/skin/image/{filename}

**功能**: 获取生成的皮肤图片

**响应**:
```
Content-Type: image/png
```

**响应体**: 二进制图片数据

---

#### 4.2.4 应用皮肤 API

##### POST /api/skin/apply

**功能**: 将生成的皮肤应用到游戏

**请求头**:
```
Content-Type: application/json
Authorization: Bearer {jwt_token}
```

**请求体**:
```json
{
  "skin_id": "skin_20240204_123456",
  "player_id": "player_123"
}
```

**响应示例**:

**成功** (200 OK):
```json
{
  "success": true,
  "message": "皮肤已应用",
  "skin_url": "/api/skin/image/skin_20240204_123456.png"
}
```

---

#### 4.2.5 获取历史记录 API

##### GET /api/skin/history

**功能**: 获取玩家生成的皮肤历史

**请求头**:
```
Authorization: Bearer {jwt_token}
```

**查询参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `page` | integer | ❌ | 页码（默认1） |
| `limit` | integer | ❌ | 每页数量（默认10，最大50） |

**响应示例** (200 OK):
```json
{
  "success": true,
  "total": 25,
  "page": 1,
  "limit": 10,
  "skins": [
    {
      "skin_id": "skin_20240204_123456",
      "prompt": "a cute cartoon snake skin",
      "image_url": "/api/skin/image/skin_20240204_123456.png",
      "created_at": "2026-02-04T12:34:56Z",
      "status": "completed"
    },
    {
      "skin_id": "skin_20240204_123455",
      "prompt": "cyberpunk neon snake",
      "image_url": "/api/skin/image/skin_20240204_123455.png",
      "created_at": "2026-02-04T11:23:45Z",
      "status": "completed"
    }
  ]
}
```

---

## 🔌 5. ComfyUI 客户端实现

### 5.1 客户端接口设计

```python
# comfyui_client.py

import requests
import uuid
import json
from typing import Optional, Dict, Any

class ComfyUIClient:
    """ComfyUI API 客户端"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8188"):
        self.base_url = base_url
        self.client_id = str(uuid.uuid4())
        
    def submit_prompt(self, prompt: str, 
                     width: int = 512, 
                     height: int = 512,
                     steps: int = 20,
                     cfg: float = 7.0) -> str:
        """
        提交生成任务到 ComfyUI
        
        Args:
            prompt: 提示词文本
            width: 图片宽度
            height: 图片高度
            steps: 采样步数
            cfg: CFG 值
            
        Returns:
            prompt_id: 任务ID
        """
        # 构建 ComfyUI 工作流
        workflow = self._build_workflow(
            prompt=prompt,
            width=width,
            height=height,
            steps=steps,
            cfg=cfg
        )
        
        # 发送请求
        response = requests.post(
            f"{self.base_url}/prompt",
            json={
                "prompt": workflow,
                "client_id": self.client_id
            },
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        return data.get("prompt_id")
    
    def get_status(self, prompt_id: str) -> Dict[str, Any]:
        """
        获取生成状态
        
        Args:
            prompt_id: 任务ID
            
        Returns:
            状态信息字典
        """
        response = requests.get(
            f"{self.base_url}/history/{prompt_id}",
            timeout=10
        )
        
        response.raise_for_status()
        return response.json()
    
    def download_image(self, filename: str, 
                      subfolder: str = "",
                      image_type: str = "output") -> bytes:
        """
        下载生成的图片
        
        Args:
            filename: 文件名
            subfolder: 子文件夹
            image_type: 图片类型
            
        Returns:
            图片二进制数据
        """
        params = {
            "filename": filename,
            "subfolder": subfolder,
            "type": image_type
        }
        
        response = requests.get(
            f"{self.base_url}/view",
            params=params,
            timeout=30
        )
        
        response.raise_for_status()
        return response.content
    
    def get_queue_info(self) -> Dict[str, Any]:
        """获取队列信息"""
        response = requests.get(
            f"{self.base_url}/queue",
            timeout=10
        )
        
        response.raise_for_status()
        return response.json()
    
    def _build_workflow(self, prompt: str, 
                        width: int, 
                        height: int,
                        steps: int,
                        cfg: float) -> Dict:
        """构建 ComfyUI 工作流"""
        # 节点ID配置
        clip_node = "3"
        clip_model = "4"
        positive = "6"
        negative = "7"
        empty_latent = "5"
        ksampler = "10"
        vae = "8"
        vae_decode = "9"
        save_image = "11"
        
        workflow = {
            clip_node: {
                "class_type": "CheckpointLoaderSimple",
                "inputs": {
                    "ckpt_name": "v1-5-pruned-emaonly.ckpt"
                }
            },
            clip_model: {
                "class_type": "CLIPLoader",
                "inputs": {
                    "clip_name": "clip-vit-base-patch32"
                }
            },
            positive: {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": prompt,
                    "clip": [clip_model, 0]
                }
            },
            negative: {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": "low quality, blurry, distorted, ugly, bad anatomy",
                    "clip": [clip_model, 0]
                }
            },
            empty_latent: {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                }
            },
            ksampler: {
                "class_type": "KSampler",
                "inputs": {
                    "seed": 42,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": [clip_node, 0],
                    "positive": [positive, 0],
                    "negative": [negative, 0],
                    "latent_image": [empty_latent, 0]
                }
            },
            vae: {
                "class_type": "VAELoader",
                "inputs": {
                    "vae_name": "vae-ft-mse-840000-ema-pruned.safetensors"
                }
            },
            vae_decode: {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": [ksampler, 0],
                    "vae": [vae, 0]
                }
            },
            save_image: {
                "class_type": "SaveImage",
                "inputs": {
                    "images": [vae_decode, 0],
                    "filename_prefix": f"snake_skin_{int(time.time())}"
                }
            }
        }
        
        return workflow
```

---

## 📦 6. 数据模型

### 6.1 皮肤记录模型

```python
class SkinRecord:
    """皮肤记录数据模型"""
    
    def __init__(self, skin_id: str, prompt: str, 
                 status: str, player_id: str,
                 created_at: str = None):
        self.skin_id = skin_id
        self.prompt = prompt
        self.status = status  # pending, processing, completed, failed
        self.player_id = player_id
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.image_url = None
        self.task_id = None
```

### 6.2 皮肤存储结构

```
data/
  └── skins/
      ├── {player_id}/
      │   ├── {skin_id}.png
      │   ├── {skin_id}_thumb.png
      │   └── metadata.json
```

---

## 🧪 7. 模拟返回结果

### 7.1 成功场景模拟

**请求**:
```http
POST /api/skin/generate
{
  "prompt": "a cute cartoon snake skin with rainbow colors and stars",
  "style": "cartoon"
}
```

**响应**:
```json
{
  "success": true,
  "message": "皮肤生成任务已提交",
  "data": {
    "task_id": "task_20240204_143256_abc123",
    "status": "pending",
    "estimated_time": 30,
    "prompt": "a cute cartoon snake skin with rainbow colors and stars"
  }
}
```

**查询状态**:
```http
GET /api/skin/status/task_20240204_143256_abc123
```

**响应**:
```json
{
  "success": true,
  "data": {
    "task_id": "task_20240204_143256_abc123",
    "status": "completed",
    "progress": 100,
    "image_url": "http://127.0.0.1:5000/api/skin/image/skin_20240204_143256_abc123.png",
    "thumbnail_url": "http://127.0.0.1:5000/api/skin/thumbnail/skin_20240204_143256_abc123.png",
    "prompt": "a cute cartoon snake skin with rainbow colors and stars",
    "generation_time": 28,
    "created_at": "2026-02-04T14:32:56Z",
    "metadata": {
      "width": 512,
      "height": 512,
      "style": "cartoon",
      "model": "stable-diffusion-v1.5"
    }
  }
}
```

### 7.2 错误场景模拟

**请求参数错误**:
```json
{
  "success": false,
  "message": "请求参数验证失败",
  "errors": [
    {
      "field": "prompt",
      "message": "prompt 不能为空且长度不能超过500字符"
    }
  ],
  "error_code": "VALIDATION_ERROR"
}
```

**ComfyUI 服务不可用**:
```json
{
  "success": false,
  "message": "ComfyUI 服务不可用",
  "error_code": "COMFYUI_UNAVAILABLE",
  "details": "无法连接到 ComfyUI 服务 (http://127.0.0.1:8188)"
}
```

---

## 📱 8. 前端界面设计

### 8.1 皮肤生成器 UI

```html
<!-- skin_generator.html -->
<div class="skin-generator">
  <h2>🎨 智能皮肤生成器</h2>
  
  <!-- 输入区域 -->
  <div class="input-section">
    <textarea 
      id="skinPrompt" 
      placeholder="描述你想要的皮肤，例如：一只可爱的彩虹卡通蛇..."
      maxlength="500"
    ></textarea>
    
    <div class="controls">
      <select id="skinStyle">
        <option value="cartoon">卡通风格</option>
        <option value="realistic">写实风格</option>
        <option value="pixel_art">像素艺术</option>
      </select>
      
      <select id="skinSize">
        <option value="512">512x512</option>
        <option value="768">768x768</option>
        <option value="1024">1024x1024</option>
      </select>
    </div>
    
    <button id="generateBtn">✨ 生成皮肤</button>
  </div>
  
  <!-- 预览区域 -->
  <div class="preview-section" style="display: none;">
    <div class="progress-bar">
      <div class="progress-fill" style="width: 0%;"></div>
    </div>
    <p id="progressText">生成中... 0%</p>
    
    <div class="result-container" style="display: none;">
      <img id="skinPreview" src="" alt="生成的皮肤" />
      
      <div class="actions">
        <button id="applyBtn">🎮 应用到游戏</button>
        <button id="downloadBtn">⬇️ 下载</button>
        <button id="regenerateBtn">🔄 重新生成</button>
      </div>
    </div>
  </div>
</div>
```

---

## 🔒 9. 安全考虑

### 9.1 输入验证
- 验证 prompt 长度（1-500字符）
- 过滤恶意内容和敏感词
- 验证图片尺寸范围（256-2048）

### 9.2 速率限制
- 每用户每小时最多生成 10 张图片
- 使用 Redis 实现分布式限流

### 9.3 文件安全
- 验证文件类型（仅允许 PNG）
- 文件大小限制（最大 5MB）
- 文件名 sanitize 防止路径遍历攻击

---

## 📊 10. 性能优化

### 10.1 缓存策略
- 相同 prompt 的生成结果缓存 24 小时
- 使用 Redis 存储缓存

### 10.2 异步处理
- 使用 Celery 实现异步任务队列
- WebSocket 实时推送进度

### 10.3 CDN 加速
- 生成的图片上传到 CDN
- 使用 Cloudflare 或阿里云 CDN

---

## 🧪 11. 测试计划

### 11.1 单元测试
- ComfyUI 客户端测试
- API 接口测试
- 数据模型测试

### 11.2 集成测试
- 端到端生成流程测试
- 错误处理测试
- 并发请求测试

### 11.3 性能测试
- 生成时间测试（目标 <30秒）
- 并发用户测试（目标 100 用户）

---

## 📝 12. 部署计划

### 12.1 开发环境
```bash
# 启动 ComfyUI
cd ComfyUI
python main.py --listen 0.0.0.0 --port 8188

# 启动 Flask 服务
cd SummerProject
export COMFYUI_URL=http://127.0.0.1:8188
python app.py
```

### 12.2 生产环境
- ComfyUI 部署在独立 GPU 服务器
- Flask 服务使用 Gunicorn + Nginx
- 使用 Docker 容器化部署

---

## 📖 13. 参考文档

- ComfyUI 官方文档: https://docs.comfy.org/
- Flask API 文档: https://flask.palletsprojects.com/
- Stable Diffusion 文档: https://stability.ai/

---

## 📌 附录

### A. 完整的 API 端点列表

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/skin/generate` | POST | 生成皮肤 |
| `/api/skin/status/{task_id}` | GET | 查询状态 |
| `/api/skin/image/{filename}` | GET | 获取图片 |
| `/api/skin/apply` | POST | 应用皮肤 |
| `/api/skin/history` | GET | 历史记录 |
| `/api/skin/delete/{skin_id}` | DELETE | 删除皮肤 |

### B. 错误码列表

| 错误码 | 说明 |
|--------|------|
| `INVALID_PROMPT` | prompt 无效 |
| `COMFYUI_UNAVAILABLE` | ComfyUI 不可用 |
| `RATE_LIMIT_EXCEEDED` | 超过速率限制 |
| `SKIN_NOT_FOUND` | 皮肤不存在 |
| `VALIDATION_ERROR` | 参数验证失败 |

---

**文档版本**: v1.0  
**最后更新**: 2026-02-04
