"""
测试 Flask 服务是否正常运行
验证各个路由是否能正确访问
"""

import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(endpoint, description):
    """测试单个端点"""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n测试: {description}")
        print(f"URL: {url}")

        response = requests.get(url, timeout=5)

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            # 检查内容长度
            content = response.text
            print(f"内容长度: {len(content)} 字符")

            # 检查关键内容
            if 'snake' in content.lower() or '贪吃蛇' in content or 'game' in content.lower():
                print("✅ 检测到游戏相关内容")
            else:
                print("⚠️ 未检测到游戏相关内容")

            return True
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 服务未启动")
        return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("Flask 服务测试")
    print("=" * 60)
    print(f"服务地址: {BASE_URL}")
    print("=" * 60)

    # 测试各个端点
    endpoints = [
        ("/", "首页"),
        ("/game", "贪吃蛇游戏"),
        ("/tasks", "任务管理器"),
        ("/presentation", "实训报告"),
    ]

    results = []
    for endpoint, description in endpoints:
        result = test_endpoint(endpoint, description)
        results.append((endpoint, description, result))

    # 输出总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    success_count = sum(1 for _, _, result in results if result)

    for endpoint, description, result in results:
        status = "✅ 成功" if result else "❌ 失败"
        print(f"{status}: {description} ({endpoint})")

    print(f"\n总计: {success_count}/{len(results)} 成功")

    if success_count == len(results):
        print("\n🎉 所有测试通过!")
    else:
        print("\n⚠️ 部分测试失败，请检查配置")

if __name__ == "__main__":
    main()
