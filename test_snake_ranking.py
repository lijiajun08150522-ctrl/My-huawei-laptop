"""
贪吃蛇排行榜系统测试脚本
"""
import requests
import json
from datetime import datetime


class SnakeRankingTester:
    """排行榜测试类"""

    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []

    def print_section(self, title):
        """打印章节标题"""
        print(f"\n{'=' * 60}")
        print(f"{title}")
        print('=' * 60)

    def test_get_statistics(self):
        """测试获取统计数据"""
        self.print_section("测试1: 获取统计数据")

        try:
            response = requests.get(f"{self.base_url}/api/snake/statistics")
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if response.status_code == 200 and data.get('success'):
                print("✅ 测试通过")
                self.test_results.append(("获取统计数据", True))
                return data.get('statistics')
            else:
                print("❌ 测试失败")
                self.test_results.append(("获取统计数据", False))
                return None

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            self.test_results.append(("获取统计数据", False))
            return None

    def test_add_score(self, player_name, score, level=1):
        """测试添加分数"""
        print(f"\n添加分数: {player_name} - {score}分 (Level {level})")

        try:
            payload = {
                "player_name": player_name,
                "score": score,
                "level": level
            }

            response = requests.post(
                f"{self.base_url}/api/snake/ranking",
                json=payload
            )
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if response.status_code == 200 and data.get('success'):
                print("✅ 测试通过")
                return True
            else:
                print("❌ 测试失败")
                return False

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False

    def test_get_ranking(self, limit=10):
        """测试获取排行榜"""
        print(f"\n获取排行榜 TOP {limit}")

        try:
            response = requests.get(f"{self.base_url}/api/snake/ranking?limit={limit}")
            data = response.json()

            print(f"状态码: {response.status_code}")

            if response.status_code == 200 and data.get('success'):
                ranking = data.get('ranking', [])

                print(f"\n排行榜数据:")
                print("-" * 60)
                for record in ranking:
                    print(f"  第{record['rank']}名: {record['player_name']} - {record['score']}分 (Level {record['level']})")
                print("-" * 60)

                print("✅ 测试通过")
                self.test_results.append(("获取排行榜", True))
                return ranking
            else:
                print("❌ 测试失败")
                self.test_results.append(("获取排行榜", False))
                return None

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            self.test_results.append(("获取排行榜", False))
            return None

    def test_get_player(self, player_name):
        """测试获取玩家信息"""
        print(f"\n获取玩家信息: {player_name}")

        try:
            response = requests.get(f"{self.base_url}/api/snake/player/{player_name}")
            data = response.json()

            print(f"状态码: {response.status_code}")
            print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

            if response.status_code == 200 and data.get('success'):
                print("✅ 测试通过")
                return data.get('record')
            else:
                print("❌ 测试失败（玩家可能不存在）")
                return None

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return None

    def test_validation(self):
        """测试输入验证"""
        self.print_section("测试2: 输入验证")

        # 测试空名称
        print("\n测试2.1: 空玩家名称")
        result = self.test_add_score("", 100)
        self.test_results.append(("空名称验证", not result))  # 应该失败

        # 测试负分
        print("\n测试2.2: 负分数")
        result = self.test_add_score("测试玩家", -100)
        self.test_results.append(("负分验证", not result))  # 应该失败

        # 测试正常数据
        print("\n测试2.3: 正常数据")
        result = self.test_add_score("测试玩家", 100, 1)
        self.test_results.append(("正常数据", result))  # 应该成功

    def test_ranking_order(self):
        """测试排行榜排序"""
        self.print_section("测试3: 排行榜排序")

        print("\n添加多个分数...")

        # 添加多个分数
        test_data = [
            ("玩家A", 100, 1),
            ("玩家B", 200, 2),
            ("玩家C", 150, 1),
            ("玩家D", 300, 3),
        ]

        for player, score, level in test_data:
            self.test_add_score(player, score, level)

        # 获取排行榜
        ranking = self.test_get_ranking(10)

        if ranking:
            # 验证排序是否正确
            scores = [r['score'] for r in ranking]
            is_sorted = scores == sorted(scores, reverse=True)

            if is_sorted:
                print("\n✅ 排序验证通过")
                self.test_results.append(("排行榜排序", True))
            else:
                print("\n❌ 排序验证失败")
                self.test_results.append(("排行榜排序", False))

    def test_concurrent_scores(self):
        """测试同一玩家的多次记录"""
        self.print_section("测试4: 同一玩家多次记录")

        player_name = "重复玩家"
        scores = [100, 150, 120, 200, 180]

        print(f"\n为玩家 '{player_name}' 添加多次记录...")

        for score in scores:
            self.test_add_score(player_name, score)

        # 获取玩家最高分
        player_best = self.test_get_player(player_name)

        if player_best and player_best['score'] == max(scores):
            print(f"\n✅ 最高分验证通过: {max(scores)}")
            self.test_results.append(("最高分记录", True))
        else:
            print("\n❌ 最高分验证失败")
            self.test_results.append(("最高分记录", False))

    def run_all_tests(self):
        """运行所有测试"""
        self.print_section("贪吃蛇排行榜系统 - 自动化测试")

        # 初始统计
        initial_stats = self.test_get_statistics()

        # 获取排行榜
        self.test_get_ranking()

        # 输入验证测试
        self.test_validation()

        # 排序测试
        self.test_ranking_order()

        # 重复玩家测试
        self.test_concurrent_scores()

        # 最终统计
        final_stats = self.test_get_statistics()

        # 总结
        self.print_summary(initial_stats, final_stats)

    def print_summary(self, initial_stats, final_stats):
        """打印测试总结"""
        self.print_section("测试总结")

        passed = sum(1 for _, result in self.test_results if result)
        total = len(self.test_results)

        print(f"\n测试结果: {passed}/{total} 通过\n")

        for test_name, result in self.test_results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"  {test_name}: {status}")

        # 统计对比
        if initial_stats and final_stats:
            print(f"\n统计数据变化:")
            print(f"  玩家总数: {initial_stats['total_players']} → {final_stats['total_players']}")
            print(f"  最高分: {initial_stats['highest_score']} → {final_stats['highest_score']}")
            print(f"  平均分: {initial_stats['average_score']} → {final_stats['average_score']}")
            print(f"  游戏总数: {initial_stats['total_games']} → {final_stats['total_games']}")


def main():
    """主函数"""
    print("╔═════════════════════════════════════════════════════════╗")
    print("║     贪吃蛇排行榜系统 - 自动化测试工具                    ║")
    print("╚═════════════════════════════════════════════════════════╝")

    # 检查服务器是否运行
    print("\n检查服务器状态...")
    try:
        response = requests.get("http://localhost:5000/api/snake/statistics", timeout=3)
        print("✅ 服务器运行正常")
    except:
        print("❌ 服务器未启动！")
        print("请先运行: python app.py")
        return

    # 运行测试
    tester = SnakeRankingTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
