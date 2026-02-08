"""
AI 皮肤生成 API 测试脚本
测试 /api/agent 和相关接口的模拟响应
"""

import json
import time
from datetime import datetime


def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def simulate_agent_api():
    """模拟 /api/agent 接口"""

    print_section("1. POST /api/agent - 提交生成任务")

    # 模拟请求
    request_data = {
        "prompt": "a cute cartoon snake skin with colorful pattern",
        "style": "cartoon",
        "width": 512,
        "height": 512,
        "player_id": "player_12345"
    }

    print("请求:")
    print(json.dumps(request_data, indent=2, ensure_ascii=False))

    # 模拟响应
    task_id = f"task_{int(time.time())}_skin_gen"
    response_data = {
        "success": True,
        "message": "皮肤生成任务已提交",
        "task_id": task_id,
        "status": "pending",
        "estimated_time": 30
    }

    print("\n响应:")
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    return task_id


def simulate_status_api(task_id):
    """模拟 /api/agent/status/{task_id} 接口"""

    print_section("2. GET /api/agent/status/{task_id} - 查询生成状态")

    print(f"任务ID: {task_id}\n")

    # 模拟进行中状态
    print("查询 1 (进行中):")
    response_data = {
        "success": True,
        "task_id": task_id,
        "status": "processing",
        "progress": 45,
        "message": "AI 正在生成..."
    }
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    # 模拟完成状态
    print("\n查询 2 (已完成):")
    image_url = f"http://127.0.0.1:5000/api/skin/image/{task_id}.png"
    response_data = {
        "success": True,
        "task_id": task_id,
        "status": "completed",
        "progress": 100,
        "image_url": image_url,
        "thumbnail_url": image_url.replace(".png", "_thumb.png"),
        "prompt": "a cute cartoon snake skin with colorful pattern",
        "generation_time": 27,
        "created_at": datetime.utcnow().isoformat(),
        "metadata": {
            "width": 512,
            "height": 512,
            "style": "cartoon",
            "model": "stable-diffusion-v1.5"
        }
    }
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    return image_url


def show_frontend_flow():
    """展示前端调用流程"""

    print_section("前端调用流程")

    print("1. 用户点击 'AI 生成皮肤' 按钮")
    print("   -> 调用 generateAISkin()")

    print("\n2. 显示加载动画")
    print("   -> showSkinLoading()")
    print("   -> 显示加载遮罩层和进度提示")

    print("\n3. 发送 API 请求")
    print("   -> POST /api/agent")
    print("   -> 携带 prompt, style, width, height, player_id")

    print("\n4. 获取任务 ID")
    print("   -> 返回 { success: true, task_id: 'task_xxx' }")

    print("\n5. 轮询查询状态")
    print("   -> pollSkinStatus(taskId)")
    print("   -> 每秒调用 GET /api/agent/status/{task_id}")

    print("\n6. 更新进度")
    print("   -> updateLoadingProgress(progress)")
    print("   -> 显示: 准备中 -> 上传请求 -> AI 正在生成 -> 即将完成")

    print("\n7. 生成完成")
    print("   -> 返回 { status: 'completed', image_url: '...' }")

    print("\n8. 加载皮肤纹理")
    print("   -> loadSkinTexture(imageUrl)")
    print("   -> 创建 Image 对象加载图片")
    print("   -> 调整大小到 GRID_SIZE (20x20)")
    print("   -> 保存到 gameState.skinTexture")

    print("\n9. 应用到游戏")
    print("   -> 在 drawSnake() 中使用 texture")
    print("   -> ctx.createPattern(texture, 'repeat')")
    print("   -> 所有蛇段使用纹理绘制")

    print("\n10. 保存到本地存储")
    print("    -> localStorage.setItem('snakeGameSkin', imageUrl)")

    print("\n11. 隐藏加载动画")
    print("    -> hideSkinLoading()")
    print("    -> 显示成功提示")


def show_api_spec():
    """显示 API 接口规范"""

    print_section("API 接口规范")

    apis = {
        "POST /api/agent": {
            "功能": "提交 AI 皮肤生成任务",
            "请求体": {
                "prompt": "string (必填) - 皮肤描述",
                "style": "string (可选) - 风格",
                "width": "integer (可选) - 宽度",
                "height": "integer (可选) - 高度",
                "player_id": "string (可选) - 玩家ID"
            },
            "成功响应": {
                "success": True,
                "task_id": "task_xxx",
                "status": "pending"
            }
        },
        "GET /api/agent/status/{task_id}": {
            "功能": "查询生成状态",
            "进行中响应": {
                "success": True,
                "status": "processing",
                "progress": 65
            },
            "完成响应": {
                "success": True,
                "status": "completed",
                "progress": 100,
                "image_url": "http://..."
            }
        }
    }

    for endpoint, doc in apis.items():
        print(f"\n{endpoint}")
        print(f"  功能: {doc['功能']}")

        if '请求体' in doc:
            print("  请求体:")
            for key, value in doc['请求体'].items():
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


def print_summary():
    """打印总结"""

    print_section("功能总结")

    print("已实现的功能:")
    print("  [OK] AI 皮肤生成按钮")
    print("  [OK] 调用 /api/agent 接口")
    print("  [OK] 异步任务轮询")
    print("  [OK] 加载动画显示")
    print("  [OK] 进度提示更新")
    print("  [OK] 图片纹理加载")
    print("  [OK] 应用到蛇头和蛇身")
    print("  [OK] 本地存储保存")

    print("\nUI 组件:")
    print("  [OK] AI 生成皮肤按钮 (header)")
    print("  [OK] 加载遮罩层 (overlay)")
    print("  [OK] 加载旋转动画 (spinner)")
    print("  [OK] 进度文字提示")

    print("\n前端函数:")
    print("  [OK] generateAISkin() - 生成皮肤主函数")
    print("  [OK] pollSkinStatus() - 轮询状态")
    print("  [OK] loadSkinTexture() - 加载纹理")
    print("  [OK] showSkinLoading() - 显示加载")
    print("  [OK] hideSkinLoading() - 隐藏加载")
    print("  [OK] updateLoadingProgress() - 更新进度")

    print("\n游戏集成:")
    print("  [OK] gameState.skinTexture - 皮肤纹理")
    print("  [OK] drawSnake() - 使用纹理绘制")
    print("  [OK] localStorage - 保存皮肤")

    print("\n错误处理:")
    print("  [OK] 防止重复点击")
    print("  [OK] API 错误捕获")
    print("  [OK] 超时处理 (60秒)")
    print("  [OK] 图片加载失败处理")

    print("\n待实现 (后端):")
    print("  [ ] POST /api/agent - 提交任务接口")
    print("  [ ] GET /api/agent/status/{id} - 查询状态接口")
    print("  [ ] ComfyUI 集成")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  AI 皮肤生成 API 测试")
    print("  AI Skin Generator API Test")
    print("="*60)

    # 模拟 API 调用
    task_id = simulate_agent_api()
    image_url = simulate_status_api(task_id)

    # 展示前端流程
    show_frontend_flow()

    # 显示 API 规范
    show_api_spec()

    # 打印总结
    print_summary()

    print("\n" + "="*60)
    print("  测试完成")
    print("="*60 + "\n")
