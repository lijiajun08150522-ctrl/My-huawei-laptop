"""
Dify Agent 节点模拟器
模拟 Dify AI Agent 的逻辑，根据日期自动决定挑战主题
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random
import calendar


class DifyAgent:
    """
    Dify Agent 节点模拟器
    
    功能:
    1. 根据当前日期自动决定挑战主题
    2. 基于主题生成 ComfyUI 提示词
    3. 调用皮肤生成接口
    4. 生成每日挑战
    """

    # 挑战主题配置
    DAILY_THEMES = {
        "cyberpunk": {
            "name": "赛博朋克",
            "description": "霓虹灯光、未来科技、数字世界",
            "colors": ["#FF00FF", "#00FFFF", "#FF0080", "#9400D3"],
            "prompt_template": "Neon glowing snake, cyberpunk style, futuristic digital world, {description}, high resolution, detailed texture",
            "style": "cyberpunk"
        },
        "fantasy": {
            "name": "奇幻冒险",
            "description": "魔法森林、奇幻生物、神秘符文",
            "colors": ["#FFD700", "#00FF00", "#FF6347", "#9370DB"],
            "prompt_template": "Magical snake, fantasy style, {description}, enchanted forest, mystical runes, glowing elements, high resolution",
            "style": "fantasy"
        },
        "pixel_art": {
            "name": "像素艺术",
            "description": "复古游戏、8-bit 风格、怀旧像素",
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"],
            "prompt_template": "Pixel art snake, 8-bit style, {description}, retro gaming aesthetic, bold colors, high resolution",
            "style": "pixel_art"
        },
        "nature": {
            "name": "自然生态",
            "description": "森林、草原、动物花纹、有机纹理",
            "colors": ["#228B22", "#8FBC8F", "#90EE90", "#98FB98"],
            "prompt_template": "Natural snake, organic style, {description}, forest ecosystem, animal patterns, high resolution",
            "style": "realistic"
        },
        "ocean": {
            "name": "深海探险",
            "description": "珊瑚礁、海底生物、水波纹理",
            "colors": ["#00CED1", "#20B2AA", "#48D1CC", "#40E0D0"],
            "prompt_template": "Underwater snake, ocean style, {description}, coral reef, bioluminescent, water waves, high resolution",
            "style": "realistic"
        },
        "space": {
            "name": "星际穿越",
            "description": "宇宙星空、星云、银河纹理",
            "colors": ["#4B0082", "#0000FF", "#8A2BE2", "#9400D3"],
            "prompt_template": "Space snake, cosmic style, {description}, nebula, galaxy stars, cosmic dust, high resolution",
            "style": "fantasy"
        },
        "dragon": {
            "name": "龙之传说",
            "description": "龙鳞纹理、火焰特效、威严霸气",
            "colors": ["#DC143C", "#B22222", "#FF4500", "#FF6347"],
            "prompt_template": "Dragon scale snake, legendary style, {description}, fire effects, majestic scales, golden accents, high resolution",
            "style": "fantasy"
        },
        "ice": {
            "name": "冰雪奇缘",
            "description": "冰晶纹理、雪花图案、寒冷极地",
            "colors": ["#E0FFFF", "#AFEEEE", "#00CED1", "#87CEEB"],
            "prompt_template": "Ice crystal snake, frozen style, {description}, snow patterns, frost effects, crystal texture, high resolution",
            "style": "realistic"
        }
    }

    # 每周主题安排（从周日到周六）
    WEEKLY_THEME_SCHEDULE = [
        "cyberpunk",   # 周日
        "fantasy",      # 周一
        "pixel_art",    # 周二
        "nature",       # 周三
        "ocean",        # 周四
        "space",        # 周五
        "dragon"        # 周六
    ]

    def __init__(self):
        """初始化 Dify Agent"""
        self.current_date = datetime.now()
        self.current_theme_key = None
        self.current_theme = None

    def get_theme_by_date(self, target_date: datetime = None) -> Dict:
        """
        根据日期获取当天的挑战主题
        
        Args:
            target_date: 目标日期（默认为今天）
            
        Returns:
            主题配置字典
        """
        date = target_date or self.current_date
        weekday = date.weekday()  # 0=周一, 6=周日
        
        # 调整到周日的索引
        theme_index = (weekday + 1) % 7
        theme_key = self.WEEKLY_THEME_SCHEDULE[theme_index]
        
        self.current_theme_key = theme_key
        self.current_theme = self.DAILY_THEMES[theme_key]
        
        # 添加额外描述
        self.current_theme['key'] = theme_key
        self.current_theme['date'] = date.strftime('%Y-%m-%d')
        self.current_theme['weekday'] = self._get_weekday_name(date.weekday())
        
        return self.current_theme

    def _get_weekday_name(self, weekday: int) -> str:
        """获取星期几的中文名称"""
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        return weekdays[weekday]

    def generate_prompt(self, theme: Dict = None, custom_description: str = None) -> str:
        """
        基于主题生成 ComfyUI 提示词
        
        Args:
            theme: 主题配置（默认使用当前主题）
            custom_description: 自定义描述
            
        Returns:
            ComfyUI 提示词
        """
        if theme is None:
            theme = self.current_theme or self.get_theme_by_date()
        
        # 生成描述词
        descriptions = [
            "glowing neon lights and reflections",
            "intricate scale patterns",
            "bioluminescent effects",
            "vibrant color gradients",
            "magical aura effects",
            "crystalline texture details",
            "ethereal glow effects",
            "dynamic light reflections"
        ]
        
        description = custom_description or random.choice(descriptions)
        
        # 生成提示词
        prompt = theme['prompt_template'].format(description=description)
        
        print(f"[Dify Agent] 生成的提示词: {prompt}")
        
        return prompt

    def generate_daily_challenge(self) -> Dict:
        """
        生成每日挑战
        
        Returns:
            挑战配置字典
        """
        theme = self.get_theme_by_date()
        prompt = self.generate_prompt(theme)
        
        challenge = {
            'date': theme['date'],
            'weekday': theme['weekday'],
            'theme': theme,
            'prompt': prompt,
            'challenge_title': f"{theme['name']}挑战",
            'challenge_description': f"今天完成{theme['name']}主题的贪吃蛇游戏，获得{theme['name']}风格的皮肤！",
            'color_palette': theme['colors'],
            'bonus_objectives': self._generate_bonus_objectives(theme['key'])
        }
        
        print(f"[Dify Agent] 生成每日挑战: {challenge['challenge_title']}")
        
        return challenge

    def _generate_bonus_objectives(self, theme_key: str) -> List[str]:
        """生成额外挑战目标"""
        bonus_map = {
            "cyberpunk": [
                "达到 Level 5",
                "使用霓虹皮肤完成一局游戏",
                "收集 10 个食物"
            ],
            "fantasy": [
                "达到 Level 4",
                "使用魔法皮肤完成一局游戏",
                "发现隐藏的彩蛋"
            ],
            "pixel_art": [
                "达到 Level 6",
                "使用复古皮肤完成一局游戏",
                "挑战最高分记录"
            ],
            "nature": [
                "达到 Level 5",
                "使用自然皮肤完成一局游戏",
                "无碰撞吃到 5 个食物"
            ],
            "ocean": [
                "达到 Level 4",
                "使用海洋皮肤完成一局游戏",
                "保持最高速度 10 秒"
            ],
            "space": [
                "达到 Level 7",
                "使用宇宙皮肤完成一局游戏",
                "连续吃到 3 个食物"
            ],
            "dragon": [
                "达到 Level 6",
                "使用龙鳞皮肤完成一局游戏",
                "获得 200 分"
            ],
            "ice": [
                "达到 Level 5",
                "使用冰晶皮肤完成一局游戏",
                "在 30 秒内吃掉第一个食物"
            ]
        }
        
        return bonus_map.get(theme_key, ["达到 Level 5", "使用主题皮肤完成游戏"])

    def get_theme_calendar(self, weeks: int = 4) -> List[Dict]:
        """
        获取未来几周的主题日历
        
        Args:
            weeks: 周数（默认 4 周）
            
        Returns:
            主题列表
        """
        calendar = []
        
        for week in range(weeks):
            for day in range(7):
                date = self.current_date + timedelta(days=week * 7 + day)
                theme = self.get_theme_by_date(date)
                calendar.append({
                    'date': theme['date'],
                    'weekday': theme['weekday'],
                    'theme_name': theme['name'],
                    'theme_key': theme['key'],
                    'colors': theme['colors']
                })
        
        return calendar

    def get_daily_quote(self) -> str:
        """
        获取每日格言
        
        Returns:
            格言文本
        """
        quotes = [
            "每一条蛇都有自己的故事。",
            "冒险开始的地方，就是你选择的方向。",
            "即使是小步，也能到达远方。",
            "勇气不是没有恐惧，而是战胜恐惧。",
            "每天都是新的挑战，每次都是新的开始。",
            "在黑暗中寻找光明，在困难中寻找机会。",
            "保持好奇心，世界会为你展开。",
            "失败只是成功路上的一个弯路。"
        ]
        
        # 根据日期选择格言
        date_seed = self.current_date.day
        quote_index = date_seed % len(quotes)
        
        return quotes[quote_index]


# 全局 Dify Agent 实例
dify_agent = DifyAgent()


def get_current_theme():
    """获取当前主题（便捷函数）"""
    return dify_agent.get_theme_by_date()


def get_daily_challenge():
    """获取每日挑战（便捷函数）"""
    return dify_agent.generate_daily_challenge()


def generate_theme_prompt(theme_key: str = None, custom_description: str = None):
    """生成主题提示词（便捷函数）"""
    if theme_key:
        theme = dify_agent.DAILY_THEMES.get(theme_key)
    else:
        theme = None
    return dify_agent.generate_prompt(theme, custom_description)
