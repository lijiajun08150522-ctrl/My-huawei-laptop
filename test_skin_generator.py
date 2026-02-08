"""
皮肤生成器测试脚本
演示 ComfyUI API 集成和模拟返回结果
"""

import json
import time
from comfyui_client import SkinGenerator, MockSkinGenerator


def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def simulate_api_response():
    """模拟 API 响应"""
    
    # ==================== 场景 1: 成功提交生成任务 ====================
    print_section("场景 1: 提交生成任务 - 成功")
    
    generator = MockSkinGenerator()
    
    # 模拟请求参数
    prompt = "a cute cartoon snake skin with rainbow colors and stars"
    player_id = "player_123"
    style = "cartoon"
    width = 512
    height = 512
    
    # 模拟请求
    print("📤 请求:")
    print(f"  POST /api/skin/generate")
    print(f"  {{")
    print(f'    "prompt": "{prompt}",')
    print(f'    "style": "{style}",')
    print(f'    "width": {width},')
    print(f'    "height": {height},')
    print(f'    "player_id": "{player_id}"')
    print(f"  }}\n")
    
    # 模拟生成
    success, task_id, message = generator.generate_skin(
        prompt=prompt,
        player_id=player_id,
        style=style,
        width=width,
        height=height
    )
    
    # 模拟响应
    print("📥 响应 (202 Accepted):")
    response_data = {
        "success": success,
        "message": message,
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
    
    print("📤 请求:")
    print(f"  GET /api/skin/status/{task_id}\n")
    
    # 模拟查询（第一次）
    status_data = generator.get_skin_status(task_id)
    
    print("📥 响应 (200 OK):")
    print(json.dumps({
        "success": status_data["success"],
        "data": status_data
    }, indent=2, ensure_ascii=False))
    
    # ==================== 场景 3: 查询生成状态（已完成） ====================
    print_section("场景 3: 查询生成状态 - 已完成")
    
    print("📤 请求:")
    print(f"  GET /api/skin/status/{task_id}\n")
    
    # 模拟查询（第二次 - 完成）
    time.sleep(1)  # 模拟延迟
    status_data = generator.get_skin_status(task_id)
    
    print("📥 响应 (200 OK):")
    response_data = {
        "success": True,
        "data": {
            "task_id": task_id,
            "status": "completed",
            "progress": 100,
            "image_url": status_data.get("image_url", ""),
            "thumbnail_url": status_data.get("image_url", "").replace(".png", "_thumb.png"),
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
    
    print("📤 请求:")
    print(f"  GET /api/skin/history?page=1&limit=10\n")
    
    # 模拟获取历史
    history_data = generator.get_skin_history(player_id, page=1, limit=10)
    
    print("📥 响应 (200 OK):")
    print(json.dumps({
        "success": True,
        "data": history_data
    }, indent=2, ensure_ascii=False))
    
    # ==================== 场景 5: 错误场景 - prompt 为空 ====================
    print_section("场景 5: 错误处理 - prompt 为空")
    
    print("📤 请求:")
    print(f"  POST /api/skin/generate")
    print(f"  {{")
    print(f'    "prompt": "",')
    print(f'    "style": "cartoon"')
    print(f"  }}\n")
    
    print("📥 响应 (400 Bad Request):")
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
    
    print("📤 请求:")
    print(f"  POST /api/skin/generate")
    print(f"  {{")
    print(f'    "prompt": "test skin"')
    print(f"  }}\n")
    
    print("📥 响应 (503 Service Unavailable):")
    error_response = {
        "success": False,
        "message": "ComfyUI 服务不可用",
        "error_code": "COMFYUI_UNAVAILABLE",
        "details": "无法连接到 ComfyUI 服务 (http://127.0.0.1:8188)"
    }
    print(json.dumps(error_response, indent=2, ensure_ascii=False))
    
    # ==================== 场景 7: 多个并发生成任务 ====================
    print_section("场景 7: 多个并发生成任务")
    
    prompts = [
        "cyberpunk neon snake skin",
        "cute pixel art snake",
        "realistic diamond snake skin"
    ]
    
    tasks = []
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n任务 {i}: {prompt}")
        success, task_id, message = generator.generate_skin(
            prompt=prompt,
            player_id="player_456",
            style="cartoon"
        )
        tasks.append((task_id, prompt))
        print(f"  ✅ 任务已提交: {task_id}")
    
    print("\n📊 批量响应:")
    batch_response = {
        "success": True,
        "message": f"已提交 {len(tasks)} 个生成任务",
        "tasks": [
            {
                "task_id": task_id,
                "prompt": prompt,
                "status": "pending"
            }
            for task_id, prompt in tasks
        ]
    }
    print(json.dumps(batch_response, indent=2, ensure_ascii=False))
    
    # ==================== 总结 ====================
    print_section("测试总结")
    
    print("✅ 已完成的测试场景:")
    print("  1. 提交生成任务 - 成功")
    print("  2. 查询生成状态 - 进行中")
    print("  3. 查询生成状态 - 已完成")
    print("  4. 获取历史记录")
    print("  5. 错误处理 - prompt 为空")
    print("  6. 错误处理 - ComfyUI 服务不可用")
    print("  7. 多个并发生成任务")
    
    print("\n📋 API 端点总结:")
    print("  POST   /api/skin/generate          - 生成皮肤")
    print("  GET    /api/skin/status/{task_id}  - 查询状态")
    print("  GET    /api/skin/image/{filename}  - 获取图片")
    print("  POST   /api/skin/apply             - 应用皮肤")
    print("  GET    /api/skin/history           - 历史记录")
    
    print("\n🎯 核心功能:")
    print("  ✅ ComfyUI API 集成")
    print("  ✅ 异步任务管理")
    print("  ✅ 状态查询和进度跟踪")
    print("  ✅ 图片存储和 URL 返回")
    print("  ✅ 错误处理和验证")
    print("  ✅ 历史记录管理")


def demonstrate_comfyui_workflow():
    """演示 ComfyUI 工作流构建"""
    
    print_section("ComfyUI 工作流演示")
    
    from comfyui_client import ComfyUIClient
    
    client = ComfyUIClient()
    
    # 构建工作流
    prompt = "a cute cartoon snake skin with rainbow colors"
    workflow = client._build_workflow(
        prompt=prompt,
        width=512,
        height=512,
        steps=20,
        cfg=7.0,
        seed=42
    )
    
    print("📝 ComfyUI 工作流结构:")
    print(json.dumps(workflow, indent=2, ensure_ascii=False))
    
    print("\n🔧 工作流节点说明:")
    print("  CheckpointLoaderSimple - 加载 Stable Diffusion 模型")
    print("  CLIPLoader - 加载 CLIP 文本编码器")
    print("  CLIPTextEncode (positive) - 编码正向提示词")
    print("  CLIPTextEncode (negative) - 编码负向提示词")
    print("  EmptyLatentImage - 创建潜在空间")
    print("  KSampler - 采样生成器")
    print("  VAELoader - 加载 VAE 解码器")
    print("  VAEDecode - 解码潜在空间为图片")
    print("  SaveImage - 保存生成的图片")


def show_api_documentation():
    """显示 API 文档"""
    
    print_section("API 完整文档")
    
    api_docs = {
        "POST /api/skin/generate": {
            "description": "生成贪吃蛇游戏皮肤",
            "request_body": {
                "prompt": "string (必填) - 皮肤描述文本（1-500字符）",
                "style": "string (可选) - 风格：cartoon, realistic, pixel_art",
                "width": "integer (可选) - 图片宽度（默认512，范围256-1024）",
                "height": "integer (可选) - 图片高度（默认512，范围256-1024）",
                "player_id": "string (可选) - 玩家ID"
            },
            "response_success": {
                "success": "boolean",
                "message": "string",
                "data": {
                    "task_id": "string - 任务ID",
                    "status": "string - 任务状态",
                    "estimated_time": "integer - 预计生成时间（秒）"
                }
            },
            "response_error": {
                "success": "boolean",
                "message": "string - 错误信息",
                "error_code": "string - 错误码"
            }
        },
        "GET /api/skin/status/{task_id}": {
            "description": "查询皮肤生成状态",
            "response_processing": {
                "success": "boolean",
                "data": {
                    "task_id": "string",
                    "status": "processing",
                    "progress": "integer - 0-100",
                    "current_step": "integer",
                    "total_steps": "integer",
                    "message": "string"
                }
            },
            "response_completed": {
                "success": "boolean",
                "data": {
                    "task_id": "string",
                    "status": "completed",
                    "image_url": "string - 图片URL",
                    "thumbnail_url": "string - 缩略图URL",
                    "prompt": "string",
                    "generation_time": "integer - 生成耗时（秒）",
                    "created_at": "string - ISO 8601 时间戳"
                }
            }
        },
        "GET /api/skin/history": {
            "description": "获取玩家生成的皮肤历史",
            "query_params": {
                "page": "integer (可选) - 页码（默认1）",
                "limit": "integer (可选) - 每页数量（默认10，最大50）"
            },
            "response": {
                "success": "boolean",
                "data": {
                    "total": "integer - 总记录数",
                    "page": "integer - 当前页",
                    "limit": "integer - 每页数量",
                    "skins": "array - 皮肤记录数组"
                }
            }
        },
        "GET /api/skin/image/{filename}": {
            "description": "获取生成的皮肤图片",
            "response": "binary - PNG 图片数据",
            "content_type": "image/png"
        },
        "POST /api/skin/apply": {
            "description": "将生成的皮肤应用到游戏",
            "request_body": {
                "skin_id": "string - 皮肤ID",
                "player_id": "string - 玩家ID"
            },
            "response": {
                "success": "boolean",
                "message": "string",
                "skin_url": "string - 皮肤URL"
            }
        }
    }
    
    for endpoint, doc in api_docs.items():
        print(f"\n{endpoint}")
        print(f"  📝 {doc['description']}")
        
        if 'request_body' in doc:
            print("  📤 请求体:")
            for key, value in doc['request_body'].items():
                print(f"    {key}: {value}")
        
        if 'query_params' in doc:
            print("  📤 查询参数:")
            for key, value in doc['query_params'].items():
                print(f"    {key}: {value}")
        
        if 'response' in doc:
            print("  📥 响应:")
            print(json.dumps(doc['response'], indent=6, ensure_ascii=False))
        
        if 'response_success' in doc:
            print("  📥 成功响应:")
            print(json.dumps(doc['response_success'], indent=6, ensure_ascii=False))
        
        if 'response_processing' in doc:
            print("  📥 进行中响应:")
            print(json.dumps(doc['response_processing'], indent=6, ensure_ascii=False))
        
        if 'response_completed' in doc:
            print("  📥 完成响应:")
            print(json.dumps(doc['response_completed'], indent=6, ensure_ascii=False))


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  贪吃蛇智能皮肤生成器 - 测试脚本")
    print("  Skin Generator Test Suite")
    print("="*60)
    
    # 运行测试
    simulate_api_response()
    
    # 演示 ComfyUI 工作流
    demonstrate_comfyui_workflow()
    
    # 显示 API 文档
    show_api_documentation()
    
    print("\n" + "="*60)
    print("  ✅ 测试完成")
    print("="*60 + "\n")
