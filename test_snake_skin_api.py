"""
测试贪吃蛇 AI 皮肤生成功能
验证后端 API 和前端集成
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"

def test_generate_skin():
    """测试生成皮肤接口"""
    print("=" * 60)
    print("测试 1: 生成皮肤")
    print("=" * 60)

    response = requests.post(
        f"{BASE_URL}/api/skin/generate",
        json={
            "player_id": "test_player_001"
        }
    )

    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

    if result.get('success') and 'task_id' in result:
        print(f"\n任务ID: {result['task_id']}")
        print(f"提示词: {result['prompt']}")
        return result['task_id']
    else:
        print("\n生成失败!")
        return None

def test_skin_status(task_id):
    """测试查询皮肤生成状态"""
    print("\n" + "=" * 60)
    print("测试 2: 查询皮肤生成状态")
    print("=" * 60)

    max_attempts = 10
    for attempt in range(max_attempts):
        print(f"\n尝试 {attempt + 1}/{max_attempts}")

        response = requests.get(f"{BASE_URL}/api/skin/status/{task_id}")
        result = response.json()

        print(f"状态: {result.get('status')}")
        print(f"进度: {result.get('progress', 0)}%")
        print(f"消息: {result.get('message')}")

        if result.get('status') == 'completed':
            print(f"\n生成完成!")
            print(f"图片URL: {result.get('image_url')}")
            return result.get('image_url')

        elif result.get('status') == 'failed':
            print(f"\n生成失败: {result.get('message')}")
            return None

        time.sleep(1)

    print("\n查询超时!")
    return None

def test_current_skin():
    """测试获取当前皮肤"""
    print("\n" + "=" * 60)
    print("测试 3: 获取当前皮肤")
    print("=" * 60)

    response = requests.get(f"{BASE_URL}/api/skin/current")
    result = response.json()

    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

    return result.get('skin_url')

def test_apply_skin(image_url):
    """测试应用皮肤"""
    print("\n" + "=" * 60)
    print("测试 4: 应用皮肤到游戏")
    print("=" * 60)

    response = requests.post(
        f"{BASE_URL}/api/skin/apply",
        json={
            "image_url": image_url
        }
    )

    result = response.json()

    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

def test_skin_history():
    """测试获取皮肤历史"""
    print("\n" + "=" * 60)
    print("测试 5: 获取皮肤历史")
    print("=" * 60)

    response = requests.get(
        f"{BASE_URL}/api/skin/history",
        params={
            "player_id": "test_player_001",
            "page": 1,
            "limit": 10
        }
    )

    result = response.json()

    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")

def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("贪吃蛇 AI 皮肤生成功能测试")
    print("=" * 60)

    try:
        # 测试 1: 生成皮肤
        task_id = test_generate_skin()

        if not task_id:
            print("\n测试失败: 无法生成任务ID")
            return

        # 测试 2: 查询状态
        image_url = test_skin_status(task_id)

        if not image_url:
            print("\n测试失败: 皮肤生成未完成")
            return

        # 测试 3: 获取当前皮肤
        current_skin = test_current_skin()
        print(f"\n当前皮肤: {current_skin}")

        # 测试 4: 应用皮肤
        test_apply_skin(image_url)

        # 测试 5: 获取历史
        test_skin_history()

        # 再次获取当前皮肤，验证已更新
        print("\n" + "=" * 60)
        print("验证: 皮肤已更新")
        print("=" * 60)
        updated_skin = test_current_skin()

        if updated_skin == image_url:
            print("\n✅ 测试通过: 皮肤已成功更新!")
        else:
            print(f"\n❌ 测试失败: 皮肤未更新")
            print(f"   期望: {image_url}")
            print(f"   实际: {updated_skin}")

        print("\n" + "=" * 60)
        print("所有测试完成!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ 连接失败: 请确保 Flask 服务已启动")
        print("   启动命令: python app.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
