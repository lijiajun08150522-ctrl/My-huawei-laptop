"""
Remake AI - 闲置资源回收利用智能平台
Flask 后端应用
"""

import os
import json
import time
import uuid
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional
from functools import wraps

import requests
from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import jwt

# 导入 ComfyUI 客户端
from comfyui_client import ComfyUIClient


# ============ 配置 ============
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'remake-ai-secret-key-2026')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-remake-ai-2026')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION = 24 * 60 * 60  # 24小时
    
    # ComfyUI 配置
    COMFYUI_URL = os.getenv('COMFYUI_URL', 'http://127.0.0.1:8188')
    COMFYUI_API_KEY = os.getenv('COMFYUI_API_KEY', '')
    COMFYUI_TIMEOUT = int(os.getenv('COMFYUI_TIMEOUT', '120'))
    
    # Dify 配置
    DIFY_API_KEY = os.getenv('DIFY_API_KEY', '')
    DIFY_API_URL = os.getenv('DIFY_API_URL', '')
    
    # 数据库配置
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'remake_ai.db')


# ============ Flask 应用 ============
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)


# ============ 数据库管理 ============
class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建改造记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS remake_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id VARCHAR(100) NOT NULL,
                    item_name VARCHAR(200) NOT NULL,
                    description TEXT,
                    value_score INTEGER,
                    category VARCHAR(50),
                    material_type VARCHAR(50),
                    reuse_potential VARCHAR(20),
                    suggestions TEXT,
                    diy_ideas TEXT,
                    image_urls TEXT,
                    carbon_saved DECIMAL(10, 2),
                    dify_response TEXT,
                    comfyui_response TEXT,
                    status VARCHAR(20) DEFAULT 'completed',
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id VARCHAR(100) UNIQUE NOT NULL,
                    username VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)


# 初始化数据库
db_manager = DatabaseManager(Config.DATABASE_PATH)


# ============ JWT 认证 ============
def generate_token(user_id: str) -> str:
    """生成 JWT token"""
    payload = {
        'user_id': user_id,
        'exp': time.time() + Config.JWT_EXPIRATION,
        'iat': time.time()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """解码 JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required(f):
    """JWT 认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取 token
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'NO_TOKEN',
                    'message': '缺少认证token'
                }
            }), 401
        
        # 提取 token（格式：Bearer <token>）
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
        
        # 验证 token
        payload = decode_token(token)
        if not payload:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_TOKEN',
                    'message': '无效或过期的token'
                }
            }), 401
        
        # 将 user_id 添加到请求上下文
        request.user_id = payload.get('user_id')
        
        return f(*args, **kwargs)
    
    return decorated_function


# ============ 材质分类逻辑 ============
MATERIAL_CATEGORY_MAPPING = {
    # 织物类
    "牛仔裤": "织物", "裤子": "织物", "T恤": "织物", "衬衫": "织物",
    "衣服": "织物", "裙子": "织物", "外套": "织物", "毛衣": "织物",
    "袜子": "织物", "围巾": "织物", "帽子": "织物", "布料": "织物",
    "denim": "织物", "jeans": "织物", "shirt": "织物", "cloth": "织物",
    
    # 塑料类
    "瓶子": "塑料", "塑料瓶": "塑料", "瓶盖": "塑料", "塑料袋": "塑料",
    "玩具": "塑料", "塑料盒": "塑料", "塑料桶": "塑料", "塑料管": "塑料",
    "bottle": "塑料", "plastic": "塑料",
    
    # 金属类
    "易拉罐": "金属", "铝罐": "金属", "铁盒": "金属", "金属罐": "金属",
    "铜线": "金属", "铝箔": "金属", "金属片": "金属", "金属管": "金属",
    "can": "金属", "aluminum": "金属", "metal": "金属",
    
    # 玻璃类
    "玻璃瓶": "玻璃", "玻璃罐": "玻璃", "玻璃杯": "玻璃", "玻璃器皿": "玻璃",
    "glass": "玻璃",
    
    # 纸制品
    "纸箱": "纸", "纸盒": "纸", "报纸": "纸", "书本": "纸", "纸张": "纸",
    "cardboard": "纸", "paper": "纸",
    
    # 木材类
    "木板": "木材", "木箱": "木材", "木棍": "木材", "木盒": "木材",
    "wood": "木材",
    
    # 电子类
    "手机": "电子", "电脑": "电子", "键盘": "电子", "鼠标": "电子",
    "电池": "电子", "电线": "电子", "电子元件": "电子",
    "phone": "电子", "computer": "电子", "electronic": "电子"
}


def identify_material_category(item_name: str) -> str:
    """根据物品名称识别材质类别"""
    item_name_lower = item_name.lower()
    
    # 直接匹配映射表
    for keyword, category in MATERIAL_CATEGORY_MAPPING.items():
        if keyword in item_name_lower:
            return category
    
    # 关键词匹配
    if any(kw in item_name_lower for kw in ["布", "棉", "麻", "丝", "毛", "绒"]):
        return "织物"
    if any(kw in item_name_lower for kw in ["塑", "plastic"]):
        return "塑料"
    if any(kw in item_name_lower for kw in ["金属", "铝", "铁", "铜", "钢", "metal"]):
        return "金属"
    if any(kw in item_name_lower for kw in ["玻璃", "glass"]):
        return "玻璃"
    if any(kw in item_name_lower for kw in ["纸", "paper"]):
        return "纸"
    if any(kw in item_name_lower for kw in ["木", "wood"]):
        return "木材"
    if any(kw in item_name_lower for kw in ["电", "electronic", "电子"]):
        return "电子"
    
    return "其他"


# ============ 碳排放计算 ============
CARBON_FACTORS = {
    "织物": 15.5,     # kg CO2/kg
    "塑料": 3.5,
    "金属": 8.2,
    "玻璃": 0.8,
    "纸": 1.2,
    "木材": 12.0,
    "电子": 50.0,
    "其他": 5.0
}


def calculate_carbon_savings(material_type: str, item_name: str) -> float:
    """计算物品改造后减少的碳排放量"""
    base_carbon = CARBON_FACTORS.get(material_type, 5.0)
    saved_carbon = base_carbon * 0.5  # 改造可减少50%排放
    return round(saved_carbon, 2)


def get_carbon_equivalent(carbon_saved: float) -> str:
    """将碳排放量转换为通俗说法"""
    # 1棵树每年吸收约18kg CO2
    trees = carbon_saved / 18
    return f"相当于种植 {trees:.1f} 棵树"


# ============ 模拟 Dify 逻辑 ============
def mock_dify_analysis(item_name: str, material_type: str, description: str = "") -> Dict[str, Any]:
    """
    模拟 Dify 物品价值识别
    
    返回价值评估、改造建议和DIY想法
    """
    # 根据材质类型返回不同的评估
    category_mapping = {
        "织物": "纺织品/服装",
        "塑料": "塑料制品",
        "金属": "金属制品",
        "玻璃": "玻璃器皿",
        "纸": "纸制品",
        "木材": "木制品",
        "电子": "电子产品",
        "其他": "其他物品"
    }
    
    # 模拟价值评分（60-95之间）
    import random
    value_score = random.randint(60, 95)
    
    # 模拟改造潜力
    reuse_potential_map = {
        "织物": "高",
        "塑料": "高",
        "金属": "高",
        "玻璃": "中",
        "纸": "高",
        "木材": "中",
        "电子": "低",
        "其他": "中"
    }
    reuse_potential = reuse_potential_map.get(material_type, "中")
    
    # 根据材质生成改造建议
    suggestions_map = {
        "织物": [
            "改造为环保购物袋",
            "制作收纳盒或收纳袋",
            "剪裁制作杯垫或餐垫",
            "缝制成宠物小窝或猫抓板",
            "创意拼接做成装饰画"
        ],
        "塑料": [
            "改造成创意花盆",
            "制作收纳盒或工具盒",
            "DIY成儿童玩具或益智教具",
            "制作艺术装置或装饰品",
            "改造成灯具或灯罩"
        ],
        "金属": [
            "改造成烛台或香薰架",
            "制作花盆或种植器",
            "改造成工具收纳架",
            "制作艺术雕塑或装饰品",
            "DIY成实用工具或挂钩"
        ],
        "玻璃": [
            "改造为创意花瓶",
            "制作烛台或香薰灯",
            "改造成储物罐或收纳瓶",
            "制作马赛克艺术装饰",
            "DIY成灯具或灯罩"
        ],
        "纸": [
            "改造为收纳盒或文件夹",
            "制作手工纸艺装饰",
            "DIY成环保纸袋或信封",
            "制作书签或贺卡",
            "改造成笔筒或桌面收纳"
        ],
        "木材": [
            "改造为小型家具",
            "制作园艺工具或种植箱",
            "DIY成装饰画或摆件",
            "制作储物架或收纳盒",
            "改造成烛台或香薰座"
        ],
        "电子": [
            "拆解提取有价值的元件",
            "改造成艺术装置",
            "制作科普教具",
            "回收利用金属部件",
            "改造成装饰摆件"
        ],
        "其他": [
            "改造为实用收纳工具",
            "制作创意装饰品",
            "DIY成个性化用品",
            "改造成艺术品",
            "循环再利用"
        ]
    }
    
    suggestions = suggestions_map.get(material_type, suggestions_map["其他"])
    
    # DIY 创意想法
    diy_ideas = [
        f"将{item_name}与现代设计结合，打造独特的北欧风格作品",
        f"利用{item_name}的原有特点，保留材质美感的同时赋予新功能",
        f"将{item_name}融入环保艺术创作，传递可持续生活理念",
        f"采用模块化设计理念，让{item_name}改造品具备多功能性"
    ]
    
    return {
        "value_score": value_score,
        "category": category_mapping.get(material_type, "其他"),
        "material_type": material_type,
        "reuse_potential": reuse_potential,
        "suggestions": suggestions,
        "diy_ideas": diy_ideas
    }


# ============ ComfyUI 风格提示词 ============
STYLE_PROMPTS = {
    "织物": "upcycled denim bag, aesthetic, high quality, masterpiece, best quality, highly detailed, modern minimalist design, Nordic style, natural lighting, soft shadows, clear texture, eco-friendly fashion, sustainable design, 8K, professional product photography",
    "塑料": "modern art installation, eco-friendly creative design, vibrant colors, glossy texture, minimalist style, Bauhaus design concept, professional photography, high contrast, sharp details, turn waste into treasure, sustainable materials, 8K",
    "金属": "industrial design aesthetics, metallic texture, cool tones, modernism design, high-end product photography, reflective luster, clean lines, clear structure, turn waste into treasure, metal recycling art, 8K",
    "玻璃": "transparent texture, light and shadow art effect, modern glass design, minimalist aesthetics, high-definition photography, beautiful light refraction, transparent texture, exquisite details, eco-friendly glass art, sustainable design, 8K",
    "纸": "paper art design, handmade art sense, natural texture, paper fiber details, warm tones, Japanese minimalist style, soft natural light, warm atmosphere, eco-friendly paper art, sustainable creativity, 8K",
    "木材": "natural wood texture, organic beauty, modern wood art design, Scandinavian style, warm tones, natural light photography, wood grain details, realistic texture, eco-friendly wood art, sustainable materials, 8K",
    "电子": "electronic recycling art, futuristic design, high-tech aesthetic, modern art installation, creative reuse of electronic components, sustainable technology, 8K, professional photography",
    "其他": "modern art transformation, turn waste into treasure creative design, high-quality product photography, rich details, strong design sense, visual impact, environmental protection concept, sustainable development, professional composition, aesthetic presentation, 8K"
}


# ============ ComfyUI 集成 ============
class RemakeImageGenerator:
    """改造图片生成器"""
    
    def __init__(self, comfyui_url: str):
        self.client = ComfyUIClient(comfyui_url)
        self.tasks = {}
    
    def generate_images(self, item_name: str, suggestions: List[str], 
                       material_type: str = "其他") -> List[Dict[str, Any]]:
        """
        生成改造效果图
        
        Args:
            item_name: 物品名称
            suggestions: 改造建议列表
            material_type: 材质类型
            
        Returns:
            图片信息列表
        """
        images = []
        
        # 获取对应材质的风格提示词
        style_prompt = STYLE_PROMPTS.get(material_type, STYLE_PROMPTS["其他"])
        
        # 生成最多3张图
        for i, suggestion in enumerate(suggestions[:3]):
            # 构建完整提示词
            prompt = f"{style_prompt}"
            
            try:
                # 检查 ComfyUI 健康状态
                if not self.client.check_health():
                    raise Exception("ComfyUI 服务不可用")
                
                # 提交任务到 ComfyUI
                prompt_id = self.client.submit_prompt(
                    prompt=prompt,
                    width=1024,
                    height=1024,
                    steps=30,
                    cfg=7.5,
                    seed=-1
                )
                
                # 等待生成完成
                max_wait = Config.COMFYUI_TIMEOUT  # 从配置读取超时时间
                start_time = time.time()
                
                while time.time() - start_time < max_wait:
                    try:
                        status = self.client.get_status(prompt_id)
                        
                        if prompt_id in status:
                            outputs = status[prompt_id].get("outputs", {})
                            
                            if outputs:
                                # 获取图片信息
                                node_id = list(outputs.keys())[0]
                                output_images = outputs[node_id].get("images", [])
                                
                                if output_images:
                                    image_info = output_images[0]
                                    filename = image_info["filename"]
                                    
                                    # 构建图片URL
                                    image_url = f"{self.client.base_url}/view?filename={filename}"
                                    
                                    images.append({
                                        "image_id": str(uuid.uuid4()),
                                        "image_url": image_url,
                                        "prompt": prompt,
                                        "caption": f"{item_name} 改造为 {suggestion}",
                                        "params": {
                                            "steps": 30,
                                            "cfg_scale": 7.5,
                                            "seed": "random"
                                        }
                                    })
                                    break
                    
                        time.sleep(2)
                    
                    except requests.exceptions.Timeout:
                        print(f"[WARNING] ComfyUI 响应超时，继续等待... (item: {item_name})")
                        time.sleep(2)
                        continue
                    
                    except requests.exceptions.ConnectionError as e:
                        print(f"[ERROR] ComfyUI 连接失败: {e}")
                        raise Exception("AI 正在构思中，请稍后再试")
                
                # 超时处理
                if time.time() - start_time >= max_wait:
                    print(f"[WARNING] ComfyUI 生成超时 (item: {item_name}, suggestion: {suggestion})")
                    raise Exception("AI 正在构思中，请稍后再试")
                
            except requests.exceptions.Timeout:
                print(f"[ERROR] ComfyUI 请求超时")
                # 使用占位符URL，提示用户
                images.append({
                    "image_id": str(uuid.uuid4()),
                    "image_url": "https://via.placeholder.com/1024x1024?text=AI正在构思中，请稍后再试",
                    "prompt": prompt,
                    "caption": f"{item_name} 改造为 {suggestion}",
                    "params": {
                        "steps": 30,
                        "cfg_scale": 7.5,
                        "seed": "random"
                    }
                })
        
        return images


# 初始化图片生成器
image_generator = RemakeImageGenerator(Config.COMFYUI_URL)


# ============ 路由 ============

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'message': 'Remake AI API is running',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册（简化版，生成 token）"""
    data = request.get_json()
    user_id = data.get('user_id', f'user_{int(time.time())}')
    username = data.get('username', 'Anonymous')
    
    # 保存用户到数据库
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)',
            (user_id, username)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()
    
    # 生成 token
    token = generate_token(user_id)
    
    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'username': username,
            'token': token
        }
    })


@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录（简化版，生成 token）"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({
            'success': False,
            'error': {
                'code': 'INVALID_INPUT',
                'message': 'user_id 不能为空'
            }
        }), 400
    
    # 生成 token
    token = generate_token(user_id)
    
    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'token': token
        }
    })


@app.route('/api/remake', methods=['POST'])
@jwt_required
def remake():
    """
    闲置物品改造接口
    
    请求参数:
    - item_name: 物品名称（必填）
    - description: 物品描述（可选）
    
    响应:
    - item_id: 物品记录ID
    - item_name: 物品名称
    - value_assessment: 价值评估
    - remake_images: 改造效果图
    - carbon_saving: 碳减排数据
    """
    try:
        # 获取请求参数
        data = request.get_json()
        item_name = data.get('item_name', '').strip()
        description = data.get('description', '').strip()
        user_id = request.user_id
        
        # 验证输入
        if not item_name:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_INPUT',
                    'message': '物品名称不能为空'
                }
            }), 400
        
        if len(item_name) > 200:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INVALID_INPUT',
                    'message': '物品名称过长'
                }
            }), 400
        
        # 步骤1: 识别材质类型
        material_type = identify_material_category(item_name)
        
        # 步骤2: 调用模拟 Dify 分析
        value_assessment = mock_dify_analysis(item_name, material_type, description)
        
        # 步骤3: 计算碳排放量
        carbon_saved = calculate_carbon_savings(material_type, item_name)
        
        # 步骤4: 调用 ComfyUI 生成改造图
        remake_images = image_generator.generate_images(
            item_name, 
            value_assessment['suggestions'],
            material_type
        )
        
        # 步骤5: 保存到数据库
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO remake_records (
                user_id, item_name, description, value_score,
                category, material_type, reuse_potential, 
                suggestions, diy_ideas, image_urls, carbon_saved,
                dify_response, comfyui_response, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, item_name, description, value_assessment['value_score'],
            value_assessment['category'], value_assessment['material_type'],
            value_assessment['reuse_potential'],
            json.dumps(value_assessment['suggestions'], ensure_ascii=False),
            json.dumps(value_assessment['diy_ideas'], ensure_ascii=False),
            json.dumps([img['image_url'] for img in remake_images]),
            carbon_saved,
            json.dumps(value_assessment, ensure_ascii=False),
            json.dumps(remake_images, ensure_ascii=False),
            'completed'
        ))
        
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # 构建响应
        response_data = {
            'item_id': str(item_id),
            'item_name': item_name,
            'value_assessment': {
                'value_score': value_assessment['value_score'],
                'category': value_assessment['category'],
                'material_type': value_assessment['material_type'],
                'reuse_potential': value_assessment['reuse_potential'],
                'suggestions': value_assessment['suggestions'],
                'diy_ideas': value_assessment['diy_ideas']
            },
            'remake_images': remake_images,
            'carbon_saving': {
                'saved_kg': carbon_saved,
                'equivalent_to': get_carbon_equivalent(carbon_saved)
            },
            'created_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': response_data
        })
        
    except Exception as e:
        print(f"[ERROR] 改造请求处理失败: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': f'服务器内部错误: {str(e)}'
            }
        }), 500


@app.route('/api/user/<user_id>/records', methods=['GET'])
@jwt_required
def get_user_records(user_id):
    """获取用户改造记录"""
    try:
        # 验证用户权限
        if request.user_id != user_id:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'FORBIDDEN',
                    'message': '无权访问其他用户的记录'
                }
            }), 403
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, item_name, carbon_saved, created_at
            FROM remake_records
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 50
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        records = []
        total_carbon_saved = 0.0
        
        for row in rows:
            item_id, item_name, carbon_saved, created_at = row
            records.append({
                'item_id': str(item_id),
                'item_name': item_name,
                'carbon_saved': float(carbon_saved),
                'created_at': created_at
            })
            total_carbon_saved += float(carbon_saved)
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user_id,
                'total_items': len(records),
                'total_carbon_saved': round(total_carbon_saved, 2),
                'records': records
            }
        })
        
    except Exception as e:
        print(f"[ERROR] 获取用户记录失败: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500


@app.route('/api/trending/remakes', methods=['GET'])
def get_trending_remakes():
    """获取热门改造案例"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # 统计每个物品的改造次数和平均碳减排量
        cursor.execute('''
            SELECT item_name, 
                   COUNT(*) as remake_count,
                   AVG(carbon_saved) as avg_carbon_saved
            FROM remake_records
            GROUP BY item_name
            ORDER BY remake_count DESC
            LIMIT 10
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        trending = []
        for row in rows:
            item_name, remake_count, avg_carbon_saved = row
            trending.append({
                'item_name': item_name,
                'remake_count': remake_count,
                'avg_carbon_saved': round(float(avg_carbon_saved), 2),
                'preview_image': 'https://via.placeholder.com/200?text=' + item_name
            })
        
        return jsonify({
            'success': True,
            'data': trending
        })
        
    except Exception as e:
        print(f"[ERROR] 获取热门改造失败: {e}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': str(e)
            }
        }), 500


# ============ 错误处理 ============
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': {
            'code': 'NOT_FOUND',
            'message': '接口不存在'
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': {
            'code': 'INTERNAL_ERROR',
            'message': '服务器内部错误'
        }
    }), 500


# ============ 启动应用 ============
if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════╗
    ║   Remake AI - 闲置资源回收利用平台   ║
    ║                                      ║
    ║   让每一件闲置物品焕发新生 🌍        ║
    ╚════════════════════════════════════════╝
    
    服务已启动:
    - API 地址: http://127.0.0.1:5000
    - 健康检查: http://127.0.0.1:5000/api/health
    """)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
