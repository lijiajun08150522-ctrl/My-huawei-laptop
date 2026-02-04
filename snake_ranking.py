"""
贪吃蛇游戏排行榜系统
使用JSON文件持久化存储排行榜数据
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict


class SnakeRanking:
    """贪吃蛇排行榜管理类"""

    def __init__(self, data_file: str = "data/snake_ranking.json"):
        """
        初始化排行榜

        Args:
            data_file: 排行榜数据文件路径
        """
        self.data_file = data_file
        self.ranking_data = self._load_data()

    def _load_data(self) -> Dict:
        """加载排行榜数据"""
        if not os.path.exists(self.data_file):
            # 创建默认数据结构
            default_data = {
                "records": [],
                "last_updated": None
            }
            self._save_data(default_data)
            return default_data

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"records": [], "last_updated": None}

    def _save_data(self, data: Dict) -> bool:
        """
        保存排行榜数据

        Args:
            data: 要保存的数据

        Returns:
            保存是否成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

            data["last_updated"] = datetime.now().isoformat()

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"保存排行榜数据失败: {e}")
            return False

    def add_score(self, player_name: str, score: int, level: int = 1) -> bool:
        """
        添加分数到排行榜

        Args:
            player_name: 玩家名称
            score: 分数
            level: 达到的关卡

        Returns:
            添加是否成功
        """
        # 创建新记录
        record = {
            "id": self._generate_id(),
            "player_name": player_name,
            "score": score,
            "level": level,
            "timestamp": datetime.now().isoformat()
        }

        # 添加到列表
        self.ranking_data["records"].append(record)

        # 按分数排序（降序）
        self.ranking_data["records"].sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # 只保留前100名
        self.ranking_data["records"] = self.ranking_data["records"][:100]

        # 保存数据
        return self._save_data(self.ranking_data)

    def _generate_id(self) -> str:
        """生成唯一ID"""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")

    def get_ranking(self, limit: int = 10) -> List[Dict]:
        """
        获取排行榜前N名

        Args:
            limit: 返回记录数量

        Returns:
            排行榜数据列表（包含排名）
        """
        records = self.ranking_data["records"][:limit]

        # 添加排名
        ranked_records = []
        for i, record in enumerate(records, start=1):
            ranked_record = {
                "rank": i,
                "player_name": record["player_name"],
                "score": record["score"],
                "level": record["level"],
                "timestamp": record["timestamp"]
            }
            ranked_records.append(ranked_record)

        return ranked_records

    def get_player_best(self, player_name: str) -> Optional[Dict]:
        """
        获取玩家的最高分

        Args:
            player_name: 玩家名称

        Returns:
            玩家最高分记录，如果不存在返回None
        """
        player_records = [
            r for r in self.ranking_data["records"]
            if r["player_name"] == player_name
        ]

        if not player_records:
            return None

        # 返回最高分记录
        best_record = max(player_records, key=lambda x: x["score"])
        best_record["rank"] = self._get_rank(best_record)
        return best_record

    def _get_rank(self, record: Dict) -> int:
        """获取记录的排名"""
        for i, r in enumerate(self.ranking_data["records"], start=1):
            if r["id"] == record["id"]:
                return i
        return 0

    def get_top_scores(self, count: int = 5) -> List[Dict]:
        """
        获取前N名的分数（用于统计）

        Args:
            count: 返回记录数量

        Returns:
            前N名记录
        """
        return self.get_ranking(limit=count)

    def get_statistics(self) -> Dict:
        """
        获取排行榜统计数据

        Returns:
            统计信息字典
        """
        records = self.ranking_data["records"]

        if not records:
            return {
                "total_players": 0,
                "highest_score": 0,
                "average_score": 0,
                "total_games": 0
            }

        # 计算统计数据
        total_score = sum(r["score"] for r in records)
        highest_score = records[0]["score"] if records else 0

        # 统计玩家数量
        unique_players = len(set(r["player_name"] for r in records))

        return {
            "total_players": unique_players,
            "highest_score": highest_score,
            "average_score": round(total_score / len(records), 2),
            "total_games": len(records)
        }

    def clear_all(self) -> bool:
        """
        清空排行榜

        Returns:
            清空是否成功
        """
        self.ranking_data["records"] = []
        return self._save_data(self.ranking_data)


# 全局排行榜实例
ranking = SnakeRanking()
