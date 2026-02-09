"""
调试 AI 皮肤生成功能
测试完整的前后端交互流程
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"

def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def debug_generate_skin():
    """调试生成皮肤流程"""
    print_section("步骤 1: 生成皮肤")

    try:
        response = requests.post(
            f"{BASE_URL}/api/skin/generate",
            json={"player_id": "debug_player_001"},
            timeout=10
        )

        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        if response.status_code == 200:
            result = response.json()
            if result.get('success') and 'task_id' in result:
                task_id = result['task_id']
                print(f"\n✅ 任务创建成功")
                print(f"任务ID: {task_id}")
                return task_id
            else:
                print(f"\n❌ 任务创建失败: {result.get('message')}")
                return None
        else:
            print(f"\n❌ HTTP 错误: {response.status_code}")
            return None

    except requests.exceptions.ConnectionError:
        print("\n❌ 连接失败: 服务未启动")
        return None
    except Exception as e:
        print(f"\n❌ 异常: {e}")
        return None

def debug_poll_status(task_id, max_attempts=5):
    """调试轮询状态"""
    print_section(f"步骤 2: 轮询任务状态 (最多 {max_attempts} 次)")

    for attempt in range(1, max_attempts + 1):
        print(f"\n--- 尝试 {attempt}/{max_attempts} ---")

        try:
            response = requests.get(
                f"{BASE_URL}/api/skin/status/{task_id}",
                timeout=10
            )

            print(f"状态码: {response.status_code}")
            result = response.json()
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

            if result.get('status') == 'completed':
                print(f"\n✅ 生成完成!")
                print(f"图片URL: {result.get('image_url')}")
                return result.get('image_url')

            elif result.get('status') == 'failed':
                print(f"\n❌ 生成失败: {result.get('message')}")
                return None

            elif result.get('status') in ['pending', 'processing']:
                print(f"\n⏳ 进行中 (进度: {result.get('progress', 0)}%)")

        except Exception as e:
            print(f"❌ 异常: {e}")
            return None

        # 等待 2 秒
        time.sleep(2)

    print(f"\n⚠️ 超过最大轮询次数")
    return None

def debug_get_current_skin():
    """调试获取当前皮肤"""
    print_section("步骤 3: 获取当前皮肤")

    try:
        response = requests.get(f"{BASE_URL}/api/skin/current", timeout=10)

        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

        if result.get('success'):
            print(f"\n当前皮肤URL: {result.get('skin_url')}")
            return result.get('skin_url')

    except Exception as e:
        print(f"❌ 异常: {e}")

    return None

def debug_test_image_url(image_url):
    """测试图片 URL 是否可访问"""
    if not image_url:
        print_section("步骤 4: 跳过图片测试 (无 URL)")
        return

    print_section("步骤 4: 测试图片 URL")

    try:
        print(f"请求: {BASE_URL}{image_url if image_url.startswith('/') else '/' + image_url}")

        # 构建完整 URL
        full_url = f"{BASE_URL}{image_url if image_url.startswith('/') else '/' + image_url}"
        print(f"完整URL: {full_url}")

        response = requests.get(full_url, timeout=10)

        print(f"状态码: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print(f"内容长度: {len(response.content)} 字节")

        if response.status_code == 200:
            print(f"\n✅ 图片可以访问")

            # 保存测试图片
            test_file = "test_skin_image.png"
            with open(test_file, 'wb') as f:
                f.write(response.content)
            print(f"已保存到: {test_file}")

        else:
            print(f"\n❌ 图片访问失败")

    except Exception as e:
        print(f"❌ 异常: {e}")

def main():
    """主调试函数"""
    print_section("AI 皮肤生成调试工具")
    print(f"服务地址: {BASE_URL}")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 步骤 1: 生成皮肤
    task_id = debug_generate_skin()
    if not task_id:
        print("\n❌ 调试失败: 无法创建任务")
        return

    # 步骤 2: 轮询状态
    image_url = debug_poll_status(task_id, max_attempts=5)
    if not image_url:
        print("\n⚠️ 警告: 皮肤未完成")
        # 继续测试其他功能

    # 步骤 3: 获取当前皮肤
    current_skin = debug_get_current_skin()

    # 步骤 4: 测试图片 URL
    debug_test_image_url(image_url or current_skin)

    # 总结
    print_section("调试总结")

    results = {
        "任务创建": task_id is not None,
        "皮肤生成": image_url is not None,
        "当前皮肤": current_skin is not None,
    }

    for step, success in results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status}: {step}")

    print(f"\n完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
