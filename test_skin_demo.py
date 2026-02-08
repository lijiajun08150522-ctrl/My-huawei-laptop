"""
皮肤生成器模拟测试脚本 - 简化版
演示 API 请求参数和模拟返回结果
"""

import json
import time


def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def simulate_api_response():
    """模拟 API 响应"""

    # ==================== 场景 1: 成功提交生成任务 ====================
    print_section("场景 1: 提交生成任务 - 成功")

    # 模拟请求参数
    prompt = "a cute cartoon snake skin with rainbow colors and stars"
    player_id = "player_123"
    style = "cartoon"
    width = 512
    height = 512

    # 模拟请求
    print("请求:")
    print(f"  POST /api/skin/generate")
    print(f"  Content-Type: application/json")
    print(f"  {{")
    print(f'    "prompt": "{prompt}",')
    print(f'    "style": "{style}",')
    print(f'    "width": {width},')
    print(f'    "height": {height},')
    print(f'    "player_id": "{player_id}"')
    print(f"  }}\n")

    # 模拟任务ID
    task_id = f"task_{int(time.time())}_abc123"

    # 模拟响应
    print("响应 (202 Accepted):")
    response_data = {
        "success": True,
        "message": "皮肤生成任务已提交",
        "data": {
            "task_id": task_id,
            "status": "pending",
            "estimated_time": 30,
            "prompt": prompt
        }
    }
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    # ==================== 场景 2: 查询生成状态（进行中） ====================
    print_section("场景 2: 查询生成状态 - 进行中")

    print("请求:")
    print(f"  GET /api/skin/status/{task_id}")
    print(f"  Authorization: Bearer {player_id}\n")

    # 模拟进行中状态
    print("响应 (200 OK):")
    response_data = {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": "processing",
            "progress": 65,
            "current_step": 13,
            "total_steps": 20,
            "message": "生成中..."
        }
    }
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    # ==================== 场景 3: 查询生成状态（已完成） ====================
    print_section("场景 3: 查询生成状态 - 已完成")

    print("请求:")
    print(f"  GET /api/skin/status/{task_id}")
    print(f"  Authorization: Bearer {player_id}\n")

    # 模拟完成状态
    print("响应 (200 OK):")
    image_url = f"http://127.0.0.1:5000/api/skin/image/{task_id}.png"
    response_data = {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": "completed",
            "progress": 100,
            "image_url": image_url,
            "thumbnail_url": image_url.replace(".png", "_thumb.png"),
            "prompt": prompt,
            "generation_time": 28,
            "created_at": "2026-02-04T14:32:56Z",
            "metadata": {
                "width": width,
                "height": height,
                "style": style,
                "model": "stable-diffusion-v1.5"
            }
        }
    }
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    # ==================== 场景 4: 获取历史记录 ====================
    print_section("场景 4: 获取历史记录")

    print("请求:")
    print(f"  GET /api/skin/history?page=1&limit=10")
    print(f"  Authorization: Bearer {player_id}\n")

    print("响应 (200 OK):")
    response_data = {
        "success": True,
        "data": {
            "total": 25,
            "page": 1,
            "limit": 10,
            "skins": [
                {
                    "skin_id": task_id,
                    "prompt": prompt,
                    "image_url": image_url,
                    "created_at": "2026-02-04T14:32:56Z",
                    "status": "completed"
                },
                {
                    "skin_id": "task_20240204_112345_xyz789",
                    "prompt": "cyberpunk neon snake",
                    "image_url": "http://127.0.0.1:5000/api/skin/image/task_20240204_112345_xyz789.png",
                    "created_at": "2026-02-04T11:23:45Z",
                    "status": "completed"
                }
            ]
        }
    }
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    # ==================== 场景 5: 错误场景 - prompt 为空 ====================
    print_section("场景 5: 错误处理 - prompt 为空")

    print("请求:")
    print(f"  POST /api/skin/generate")
    print(f"  {{")
    print(f'    "prompt": "",')
    print(f'    "style": "cartoon"')
    print(f"  }}\n")

    print("响应 (400 Bad Request):")
    error_response = {
        "success": False,
        "message": "请求参数验证失败",
        "errors": [
            {
                "field": "prompt",
                "message": "prompt 不能为空且长度不能超过500字符"
            }
        ],
        "error_code": "VALIDATION_ERROR"
    }
    print(json.dumps(error_response, indent=2, ensure_ascii=False))

    # ==================== 场景 6: 错误场景 - ComfyUI 服务不可用 ====================
    print_section("场景 6: 错误处理 - ComfyUI 服务不可用")

    print("请求:")
    print(f"  POST /api/skin/generate")
    print(f"  {{")
    print(f'    "prompt": "test skin"')
    print(f"  }}\n")

    print("响应 (503 Service Unavailable):")
    error_response = {
        "success": False,
        "message": "ComfyUI 服务不可用",
        "error_code": "COMFYUI_UNAVAILABLE",
        "details": "无法连接到 ComfyUI 服务 (http://127.0.0.1:8188)"
    }
    print(json.dumps(error_response, indent=2, ensure_ascii=False))


def show_comfyui_workflow():
    """显示 ComfyUI 工作流示例"""

    print_section("ComfyUI 工作流示例")

    workflow = {
        "3": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "v1-5-pruned-emaonly.ckpt"
            }
        },
        "4": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "clip-vit-base-patch32"
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "a cute cartoon snake skin with rainbow colors",
                "clip": ["4", 0]
            }
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": "low quality, blurry, distorted, ugly",
                "clip": ["4", 0]
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": 512,
                "height": 512,
                "batch_size": 1
            }
        },
        "10": {
            "class_type": "KSampler",
            "inputs": {
                "seed": 42,
                "steps": 20,
                "cfg": 7.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": ["3", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            }
        },
        "8": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": "vae-ft-mse-840000-ema-pruned.safetensors"
            }
        },
        "9": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["10", 0],
                "vae": ["8", 0]
            }
        },
        "11": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["9", 0],
                "filename_prefix": "snake_skin_1707038376"
            }
        }
    }

    print("ComfyUI 工作流 JSON:")
    print(json.dumps(workflow, indent=2, ensure_ascii=False))

    print("\n工作流节点说明:")
    print("  [3] CheckpointLoaderSimple - 加载 Stable Diffusion 模型")
    print("  [4] CLIPLoader - 加载 CLIP 文本编码器")
    print("  [6] CLIPTextEncode - 编码正向提示词（用户的 prompt）")
    print("  [7] CLIPTextEncode - 编码负向提示词（拒绝低质量）")
    print("  [5] EmptyLatentImage - 创建潜在空间（512x512）")
    print("  [10] KSampler - 采样生成器（20步，CFG=7.0）")
    print("  [8] VAELoader - 加载 VAE 解码器")
    print("  [9] VAEDecode - 解码潜在空间为像素图片")
    print("  [11] SaveImage - 保存生成的图片")


def show_api_summary():
    """显示 API 总结"""

    print_section("API 完整总结")

    apis = {
        "POST /api/skin/generate": {
            "功能": "生成贪吃蛇游戏皮肤",
            "请求参数": {
                "prompt": "string (必填) - 皮肤描述文本（1-500字符）",
                "style": "string (可选) - 风格：cartoon, realistic, pixel_art",
                "width": "integer (可选) - 图片宽度（默认512，范围256-1024）",
                "height": "integer (可选) - 图片高度（默认512，范围256-1024）",
                "player_id": "string (可选) - 玩家ID"
            },
            "成功响应": {
                "success": True,
                "message": "皮肤生成任务已提交",
                "data": {
                    "task_id": "task_20240204_143256_abc123",
                    "status": "pending",
                    "estimated_time": 30
                }
            }
        },
        "GET /api/skin/status/{task_id}": {
            "功能": "查询皮肤生成状态",
            "进行中响应": {
                "success": True,
                "data": {
                    "task_id": "task_xxx",
                    "status": "processing",
                    "progress": 65,
                    "current_step": 13,
                    "total_steps": 20
                }
            },
            "完成响应": {
                "success": True,
                "data": {
                    "task_id": "task_xxx",
                    "status": "completed",
                    "progress": 100,
                    "image_url": "/api/skin/image/task_xxx.png",
                    "thumbnail_url": "/api/skin/thumbnail/task_xxx.png",
                    "generation_time": 28
                }
            }
        },
        "GET /api/skin/image/{filename}": {
            "功能": "获取生成的皮肤图片",
            "响应": "二进制 PNG 图片数据",
            "Content-Type": "image/png"
        },
        "POST /api/skin/apply": {
            "功能": "将生成的皮肤应用到游戏",
            "请求参数": {
                "skin_id": "string - 皮肤ID",
                "player_id": "string - 玩家ID"
            },
            "成功响应": {
                "success": True,
                "message": "皮肤已应用",
                "skin_url": "/api/skin/image/skin_xxx.png"
            }
        },
        "GET /api/skin/history": {
            "功能": "获取玩家生成的皮肤历史",
            "查询参数": {
                "page": "integer (可选) - 页码（默认1）",
                "limit": "integer (可选) - 每页数量（默认10，最大50）"
            },
            "成功响应": {
                "success": True,
                "data": {
                    "total": 25,
                    "page": 1,
                    "limit": 10,
                    "skins": "array - 皮肤记录数组"
                }
            }
        }
    }

    for endpoint, doc in apis.items():
        print(f"\n{endpoint}")
        print(f"  功能: {doc['功能']}")

        if '请求参数' in doc:
            print("  请求参数:")
            for key, value in doc['请求参数'].items():
                print(f"    {key}: {value}")

        if '查询参数' in doc:
            print("  查询参数:")
            for key, value in doc['查询参数'].items():
                print(f"    {key}: {value}")

        if '成功响应' in doc:
            print("  成功响应:")
            print(f"    {json.dumps(doc['成功响应'], indent=6, ensure_ascii=False)}")

        if '进行中响应' in doc:
            print("  进行中响应:")
            print(f"    {json.dumps(doc['进行中响应'], indent=6, ensure_ascii=False)}")

        if '完成响应' in doc:
            print("  完成响应:")
            print(f"    {json.dumps(doc['完成响应'], indent=6, ensure_ascii=False)}")

        if '响应' in doc and not isinstance(doc['响应'], dict):
            print(f"  响应: {doc['响应']}")


def print_summary():
    """打印总结"""

    print_section("测试总结")

    print("已演示的测试场景:")
    print("  1. 提交生成任务 - 成功")
    print("  2. 查询生成状态 - 进行中")
    print("  3. 查询生成状态 - 已完成（返回图片 URL）")
    print("  4. 获取历史记录")
    print("  5. 错误处理 - prompt 为空")
    print("  6. 错误处理 - ComfyUI 服务不可用")

    print("\nAPI 端点总结:")
    print("  POST   /api/skin/generate          - 生成皮肤")
    print("  GET    /api/skin/status/{task_id}  - 查询状态")
    print("  GET    /api/skin/image/{filename}  - 获取图片")
    print("  POST   /api/skin/apply             - 应用皮肤")
    print("  GET    /api/skin/history           - 历史记录")

    print("\n核心功能:")
    print("  [OK] ComfyUI API 集成（通过 prompt 参数）")
    print("  [OK] 异步任务管理")
    print("  [OK] 状态查询和进度跟踪")
    print("  [OK] 图片存储和 URL 返回")
    print("  [OK] 错误处理和验证")
    print("  [OK] 历史记录管理")
    print("  [OK] 多种风格支持")

    print("\n相关文档:")
    print("  - SDD 软件设计规约: SKIN_GENERATOR_SDD.md")
    print("  - ComfyUI 客户端: comfyui_client.py")
    print("  - 测试脚本: test_skin_demo.py")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  贪吃蛇智能皮肤生成器 - API 模拟演示")
    print("  Snake Skin Generator API Simulation")
    print("="*60)

    # 运行模拟测试
    simulate_api_response()

    # 显示 ComfyUI 工作流
    show_comfyui_workflow()

    # 显示 API 总结
    show_api_summary()

    # 打印总结
    print_summary()

    print("\n" + "="*60)
    print("  模拟演示完成")
    print("="*60 + "\n")
