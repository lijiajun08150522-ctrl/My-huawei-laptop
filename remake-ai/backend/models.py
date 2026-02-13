"""
Remake AI 数据模型
按照 SDD 规约定义的数据库模型
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict
import json


# ============ 配置 ============
DATABASE_PATH = os.getenv('DATABASE_PATH', 'remake_ai.db')


# ============ 数据模型 ============

@dataclass
class RemakeRecord:
    """
    闲置物品改造记录
    
    字段定义（按照 SDD 规约）:
    - user_id: 用户ID
    - item_name: 物品名称
    - remake_image_url: 改造效果图URL
    - carbon_offset: 碳减排量
    """
    id: Optional[int] = None
    user_id: str = ""
    item_name: str = ""
    remake_image_url: str = ""
    carbon_offset: float = 0.0
    description: Optional[str] = None
    material_type: Optional[str] = None
    value_score: Optional[int] = None
    category: Optional[str] = None
    reuse_potential: Optional[str] = None
    suggestions: Optional[List[str]] = None
    diy_ideas: Optional[List[str]] = None
    status: str = "completed"
    error_message: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        # 移除 None 值
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class User:
    """
    用户模型
    """
    id: Optional[int] = None
    user_id: str = ""
    username: Optional[str] = None
    created_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class CarbonFactor:
    """
    碳排放因子模型
    """
    id: Optional[int] = None
    category: str = ""
    item_type: str = ""
    carbon_saved_per_kg: float = 0.0
    description: Optional[str] = None
    created_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


# ============ 数据库管理 ============

class Database:
    """数据库管理类"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self._init_database()
        self._init_default_data()
    
    def _init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建改造记录表（按照 SDD 规约）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS remake_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id VARCHAR(100) NOT NULL,
                    item_name VARCHAR(200) NOT NULL,
                    remake_image_url TEXT,
                    carbon_offset DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
                    description TEXT,
                    material_type VARCHAR(50),
                    value_score INTEGER,
                    category VARCHAR(50),
                    reuse_potential VARCHAR(20),
                    suggestions TEXT,
                    diy_ideas TEXT,
                    status VARCHAR(20) DEFAULT 'completed',
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_user_id 
                ON remake_records(user_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_item_name 
                ON remake_records(item_name)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON remake_records(created_at)
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
            
            # 创建碳排放因子表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS carbon_factors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category VARCHAR(50) NOT NULL UNIQUE,
                    item_type VARCHAR(100) NOT NULL,
                    carbon_saved_per_kg DECIMAL(10, 2) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            print(f"[Database] 数据库初始化完成: {self.db_path}")
    
    def _init_default_data(self):
        """初始化默认数据（碳排放因子）"""
        # 默认碳排放因子数据
        default_factors = [
            ("织物", "纺织品/服装", 15.5, "纺织品类物品每kg平均碳排放量"),
            ("塑料", "塑料制品", 3.5, "塑料类物品每kg平均碳排放量"),
            ("金属", "金属制品", 8.2, "金属类物品每kg平均碳排放量"),
            ("玻璃", "玻璃器皿", 0.8, "玻璃类物品每kg平均碳排放量"),
            ("纸", "纸制品", 1.2, "纸制品类每kg平均碳排放量"),
            ("木材", "木制品", 12.0, "木材类物品每kg平均碳排放量"),
            ("电子", "电子产品", 50.0, "电子类物品每kg平均碳排放量"),
            ("其他", "其他物品", 5.0, "其他类别物品每kg平均碳排放量")
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for category, item_type, carbon_per_kg, desc in default_factors:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO carbon_factors 
                    (category, item_type, carbon_saved_per_kg, description)
                    VALUES (?, ?, ?, ?)
                ''', (category, item_type, carbon_per_kg, desc))
            except Exception as e:
                print(f"[Database] 插入碳排放因子失败: {e}")
        
        conn.commit()
        conn.close()
        print("[Database] 默认碳排放因子数据初始化完成")
    
    def get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)


# ============ RemakeRecord DAO ============

class RemakeRecordDAO:
    """改造记录数据访问对象"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def create(self, record: RemakeRecord) -> RemakeRecord:
        """
        创建改造记录
        
        Args:
            record: 改造记录对象
            
        Returns:
            创建后的记录（包含ID）
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            now = datetime.utcnow().isoformat()
            
            cursor.execute('''
                INSERT INTO remake_records (
                    user_id, item_name, remake_image_url, carbon_offset,
                    description, material_type, value_score, category,
                    reuse_potential, suggestions, diy_ideas, status,
                    error_message, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record.user_id,
                record.item_name,
                record.remake_image_url,
                record.carbon_offset,
                record.description,
                record.material_type,
                record.value_score,
                record.category,
                record.reuse_potential,
                json.dumps(record.suggestions, ensure_ascii=False) if record.suggestions else None,
                json.dumps(record.diy_ideas, ensure_ascii=False) if record.diy_ideas else None,
                record.status,
                record.error_message,
                now,
                now
            ))
            
            record_id = cursor.lastrowid
            record.id = record_id
            record.created_at = now
            record.updated_at = now
            
            conn.commit()
            print(f"[DAO] 改造记录创建成功: ID={record_id}, user_id={record.user_id}, item={record.item_name}")
            
            return record
            
        except Exception as e:
            conn.rollback()
            print(f"[DAO] 改造记录创建失败: {e}")
            raise
        finally:
            conn.close()
    
    def get_by_id(self, record_id: int) -> Optional[RemakeRecord]:
        """根据ID获取记录"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, user_id, item_name, remake_image_url, carbon_offset,
                       description, material_type, value_score, category,
                       reuse_potential, suggestions, diy_ideas, status,
                       error_message, created_at, updated_at
                FROM remake_records
                WHERE id = ?
            ''', (record_id,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_record(row)
            return None
        finally:
            conn.close()
    
    def get_by_user(self, user_id: str, limit: int = 50, offset: int = 0) -> List[RemakeRecord]:
        """
        获取用户的改造记录
        
        Args:
            user_id: 用户ID
            limit: 限制数量
            offset: 偏移量
            
        Returns:
            改造记录列表
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, user_id, item_name, remake_image_url, carbon_offset,
                       description, material_type, value_score, category,
                       reuse_potential, suggestions, diy_ideas, status,
                       error_message, created_at, updated_at
                FROM remake_records
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            ''', (user_id, limit, offset))
            
            rows = cursor.fetchall()
            return [self._row_to_record(row) for row in rows]
        finally:
            conn.close()
    
    def get_total_carbon_offset(self, user_id: str) -> float:
        """
        获取用户的总碳减排量
        
        Args:
            user_id: 用户ID
            
        Returns:
            总碳减排量
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT COALESCE(SUM(carbon_offset), 0)
                FROM remake_records
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            return round(float(result[0]) if result[0] else 0.0, 2)
        finally:
            conn.close()
    
    def get_item_stats(self, item_name: str) -> Dict[str, Any]:
        """
        获取物品的统计信息
        
        Args:
            item_name: 物品名称
            
        Returns:
            统计信息字典
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT COUNT(*) as count, 
                       AVG(carbon_offset) as avg_carbon,
                       MAX(carbon_offset) as max_carbon
                FROM remake_records
                WHERE item_name = ?
            ''', (item_name,))
            
            row = cursor.fetchone()
            if row and row[0] > 0:
                return {
                    'count': row[0],
                    'avg_carbon': round(float(row[1]) if row[1] else 0.0, 2),
                    'max_carbon': round(float(row[2]) if row[2] else 0.0, 2)
                }
            return {'count': 0, 'avg_carbon': 0.0, 'max_carbon': 0.0}
        finally:
            conn.close()
    
    def get_trending_items(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取热门改造物品
        
        Args:
            limit: 限制数量
            
        Returns:
            热门物品列表
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT item_name, 
                       COUNT(*) as remake_count,
                       AVG(carbon_offset) as avg_carbon,
                       GROUP_CONCAT(remake_image_url, ',') as image_urls
                FROM remake_records
                GROUP BY item_name
                ORDER BY remake_count DESC
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            trending = []
            
            for row in rows:
                item_name, count, avg_carbon, image_urls = row
                trending.append({
                    'item_name': item_name,
                    'remake_count': count,
                    'avg_carbon_saved': round(float(avg_carbon) if avg_carbon else 0.0, 2),
                    'preview_image': image_urls.split(',')[0] if image_urls else None
                })
            
            return trending
        finally:
            conn.close()
    
    def update(self, record: RemakeRecord) -> bool:
        """
        更新改造记录
        
        Args:
            record: 改造记录对象
            
        Returns:
            是否成功
        """
        if not record.id:
            return False
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            now = datetime.utcnow().isoformat()
            
            cursor.execute('''
                UPDATE remake_records
                SET remake_image_url = ?,
                    carbon_offset = ?,
                    description = ?,
                    material_type = ?,
                    value_score = ?,
                    category = ?,
                    reuse_potential = ?,
                    suggestions = ?,
                    diy_ideas = ?,
                    status = ?,
                    error_message = ?,
                    updated_at = ?
                WHERE id = ?
            ''', (
                record.remake_image_url,
                record.carbon_offset,
                record.description,
                record.material_type,
                record.value_score,
                record.category,
                record.reuse_potential,
                json.dumps(record.suggestions, ensure_ascii=False) if record.suggestions else None,
                json.dumps(record.diy_ideas, ensure_ascii=False) if record.diy_ideas else None,
                record.status,
                record.error_message,
                now,
                record.id
            ))
            
            conn.commit()
            updated = cursor.rowcount > 0
            if updated:
                print(f"[DAO] 改造记录更新成功: ID={record.id}")
            return updated
            
        except Exception as e:
            conn.rollback()
            print(f"[DAO] 改造记录更新失败: {e}")
            raise
        finally:
            conn.close()
    
    def delete(self, record_id: int) -> bool:
        """
        删除改造记录
        
        Args:
            record_id: 记录ID
            
        Returns:
            是否成功
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                DELETE FROM remake_records
                WHERE id = ?
            ''', (record_id,))
            
            conn.commit()
            deleted = cursor.rowcount > 0
            if deleted:
                print(f"[DAO] 改造记录删除成功: ID={record_id}")
            return deleted
            
        except Exception as e:
            conn.rollback()
            print(f"[DAO] 改造记录删除失败: {e}")
            raise
        finally:
            conn.close()
    
    @staticmethod
    def _row_to_record(row) -> RemakeRecord:
        """将数据库行转换为记录对象"""
        return RemakeRecord(
            id=row[0],
            user_id=row[1],
            item_name=row[2],
            remake_image_url=row[3],
            carbon_offset=float(row[4]) if row[4] else 0.0,
            description=row[5],
            material_type=row[6],
            value_score=row[7],
            category=row[8],
            reuse_potential=row[9],
            suggestions=json.loads(row[10]) if row[10] else None,
            diy_ideas=json.loads(row[11]) if row[11] else None,
            status=row[12],
            error_message=row[13],
            created_at=row[14],
            updated_at=row[15]
        )


# ============ User DAO ============

class UserDAO:
    """用户数据访问对象"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def create(self, user: User) -> User:
        """创建用户"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            now = datetime.utcnow().isoformat()
            
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, created_at)
                VALUES (?, ?, ?)
            ''', (user.user_id, user.username, now))
            
            if cursor.rowcount > 0:
                conn.commit()
                user.created_at = now
                print(f"[DAO] 用户创建成功: user_id={user.user_id}")
            else:
                # 用户已存在，查询现有记录
                cursor.execute('''
                    SELECT id, username, created_at FROM users WHERE user_id = ?
                ''', (user.user_id,))
                row = cursor.fetchone()
                if row:
                    user.id = row[0]
                    user.username = row[1] or user.username
                    user.created_at = row[2]
            
            return user
            
        except Exception as e:
            conn.rollback()
            print(f"[DAO] 用户创建失败: {e}")
            raise
        finally:
            conn.close()
    
    def get_by_user_id(self, user_id: str) -> Optional[User]:
        """根据user_id获取用户"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, user_id, username, created_at
                FROM users
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                return User(
                    id=row[0],
                    user_id=row[1],
                    username=row[2],
                    created_at=row[3]
                )
            return None
        finally:
            conn.close()


# ============ CarbonFactor DAO ============

class CarbonFactorDAO:
    """碳排放因子数据访问对象"""
    
    def __init__(self, database: Database):
        self.db = database
    
    def get_by_category(self, category: str) -> Optional[CarbonFactor]:
        """根据类别获取碳排放因子"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, category, item_type, carbon_saved_per_kg, 
                       description, created_at
                FROM carbon_factors
                WHERE category = ?
            ''', (category,))
            
            row = cursor.fetchone()
            if row:
                return CarbonFactor(
                    id=row[0],
                    category=row[1],
                    item_type=row[2],
                    carbon_saved_per_kg=float(row[3]) if row[3] else 0.0,
                    description=row[4],
                    created_at=row[5]
                )
            return None
        finally:
            conn.close()
    
    def get_all(self) -> List[CarbonFactor]:
        """获取所有碳排放因子"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, category, item_type, carbon_saved_per_kg, 
                       description, created_at
                FROM carbon_factors
                ORDER BY category
            ''')
            
            rows = cursor.fetchall()
            return [CarbonFactor(
                id=row[0],
                category=row[1],
                item_type=row[2],
                carbon_saved_per_kg=float(row[3]) if row[3] else 0.0,
                description=row[4],
                created_at=row[5]
            ) for row in rows]
        finally:
            conn.close()


# ============ 初始化 ============

# 创建全局数据库实例
database = Database()

# 创建 DAO 实例
remake_record_dao = RemakeRecordDAO(database)
user_dao = UserDAO(database)
carbon_factor_dao = CarbonFactorDAO(database)


# ============ 工具函数 ============

def init_database():
    """初始化数据库"""
    global database, remake_record_dao, user_dao, carbon_factor_dao
    database = Database()
    remake_record_dao = RemakeRecordDAO(database)
    user_dao = UserDAO(database)
    carbon_factor_dao = CarbonFactorDAO(database)


if __name__ == '__main__':
    # 测试代码
    print("=== Remake AI 数据模型测试 ===\n")
    
    # 测试创建记录
    test_record = RemakeRecord(
        user_id="test_user",
        item_name="旧牛仔裤",
        remake_image_url="http://example.com/image.jpg",
        carbon_offset=7.75,
        material_type="织物",
        value_score=85,
        category="纺织品/服装",
        reuse_potential="高",
        suggestions=["改造为环保购物袋", "制作收纳盒"],
        diy_ideas=["北欧风格设计", "可持续理念"]
    )
    
    created_record = remake_record_dao.create(test_record)
    print(f"创建的记录: {created_record.to_dict()}\n")
    
    # 测试查询记录
    found_record = remake_record_dao.get_by_id(created_record.id)
    print(f"查询的记录: {found_record.to_dict() if found_record else '未找到'}\n")
    
    # 测试用户记录
    user_records = remake_record_dao.get_by_user("test_user")
    print(f"用户的记录数: {len(user_records)}")
    
    # 测试总碳减排量
    total_carbon = remake_record_dao.get_total_carbon_offset("test_user")
    print(f"总碳减排量: {total_carbon} kg\n")
    
    # 测试热门物品
    trending = remake_record_dao.get_trending_items(5)
    print(f"热门物品: {trending}\n")
    
    # 测试碳排放因子
    fabric_factor = carbon_factor_dao.get_by_category("织物")
    print(f"织物的碳排放因子: {fabric_factor.to_dict() if fabric_factor else '未找到'}\n")
    
    all_factors = carbon_factor_dao.get_all()
    print(f"所有碳排放因子: {[f.category for f in all_factors]}\n")
    
    print("=== 测试完成 ===")
