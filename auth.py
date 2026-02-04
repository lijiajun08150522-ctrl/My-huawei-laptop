"""
JWT 用户认证模块
提供用户注册、登录、Token验证等功能
"""
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt


class UserAuth:
    """用户认证管理类"""

    def __init__(self, secret_key: str = None, data_file: str = "data/users.json"):
        """
        初始化认证系统

        Args:
            secret_key: JWT密钥（用于加密Token）
            data_file: 用户数据存储文件
        """
        self.secret_key = secret_key or self._generate_secret_key()
        self.algorithm = 'HS256'
        self.token_expiry = timedelta(hours=24)  # Token有效期24小时
        self.data_file = data_file
        self.users = self._load_users()

    def _generate_secret_key(self) -> str:
        """生成随机密钥"""
        return os.urandom(32).hex()

    def _load_users(self) -> Dict:
        """加载用户数据"""
        if not os.path.exists(self.data_file):
            # 创建默认管理员账户
            default_users = {
                "admin": {
                    "password": self._hash_password("admin123"),
                    "created_at": datetime.now().isoformat(),
                    "role": "admin"
                }
            }
            self._save_users(default_users)
            return default_users

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def _save_users(self, users: Dict) -> bool:
        """保存用户数据"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"保存用户数据失败: {e}")
            return False

    def _hash_password(self, password: str) -> str:
        """
        使用SHA-256加密密码

        Args:
            password: 明文密码

        Returns:
            加密后的密码
        """
        # 使用SHA-256加密，并加盐
        salt = "codebuddy_salt_2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def register(self, username: str, password: str, email: str = None) -> Dict[str, Any]:
        """
        注册新用户

        Args:
            username: 用户名
            password: 密码
            email: 邮箱（可选）

        Returns:
            注册结果字典
        """
        # 验证输入
        if not username or not password:
            return {
                "success": False,
                "message": "用户名和密码不能为空"
            }

        if len(username) < 3:
            return {
                "success": False,
                "message": "用户名至少3个字符"
            }

        if len(password) < 6:
            return {
                "success": False,
                "message": "密码至少6个字符"
            }

        # 检查用户是否已存在
        if username in self.users:
            return {
                "success": False,
                "message": "用户名已存在"
            }

        # 创建新用户
        self.users[username] = {
            "password": self._hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "role": "user"  # 默认为普通用户
        }

        # 保存用户数据
        if not self._save_users(self.users):
            return {
                "success": False,
                "message": "保存用户数据失败"
            }

        return {
            "success": True,
            "message": "注册成功",
            "username": username
        }

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        用户登录

        Args:
            username: 用户名
            password: 密码

        Returns:
            登录结果字典（包含Token）
        """
        # 验证输入
        if not username or not password:
            return {
                "success": False,
                "message": "用户名和密码不能为空"
            }

        # 检查用户是否存在
        if username not in self.users:
            return {
                "success": False,
                "message": "用户名或密码错误"
            }

        # 验证密码
        hashed_password = self._hash_password(password)
        if self.users[username]["password"] != hashed_password:
            return {
                "success": False,
                "message": "用户名或密码错误"
            }

        # 生成JWT Token
        token = self._generate_token(username)

        # 返回登录结果
        return {
            "success": True,
            "message": "登录成功",
            "token": token,
            "username": username,
            "role": self.users[username]["role"]
        }

    def _generate_token(self, username: str) -> str:
        """
        生成JWT Token

        Args:
            username: 用户名

        Returns:
            JWT Token字符串
        """
        payload = {
            "username": username,
            "role": self.users[username]["role"],
            "exp": datetime.utcnow() + self.token_expiry,
            "iat": datetime.utcnow()
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证JWT Token

        Args:
            token: JWT Token字符串

        Returns:
            Token payload（验证失败返回None）
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def refresh_token(self, token: str) -> Optional[str]:
        """
        刷新Token

        Args:
            token: 旧的Token

        Returns:
            新的Token（失败返回None）
        """
        # 验证旧Token
        payload = self.verify_token(token)
        if not payload:
            return None

        # 生成新Token
        return self._generate_token(payload["username"])

    def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """
        获取用户信息

        Args:
            username: 用户名

        Returns:
            用户信息字典（用户不存在返回None）
        """
        if username not in self.users:
            return None

        user = self.users[username].copy()
        # 移除敏感信息
        user.pop("password", None)
        return user

    def change_password(self, username: str, old_password: str, new_password: str) -> Dict[str, Any]:
        """
        修改密码

        Args:
            username: 用户名
            old_password: 旧密码
            new_password: 新密码

        Returns:
            操作结果字典
        """
        # 检查用户是否存在
        if username not in self.users:
            return {
                "success": False,
                "message": "用户不存在"
            }

        # 验证旧密码
        hashed_old = self._hash_password(old_password)
        if self.users[username]["password"] != hashed_old:
            return {
                "success": False,
                "message": "旧密码错误"
            }

        # 验证新密码
        if len(new_password) < 6:
            return {
                "success": False,
                "message": "新密码至少6个字符"
            }

        # 更新密码
        self.users[username]["password"] = self._hash_password(new_password)

        # 保存
        if not self._save_users(self.users):
            return {
                "success": False,
                "message": "保存失败"
            }

        return {
            "success": True,
            "message": "密码修改成功"
        }

    def logout(self, token: str) -> Dict[str, Any]:
        """
        用户登出（由于JWT无状态，这里仅验证Token）

        Args:
            token: JWT Token

        Returns:
            操作结果字典
        """
        # 验证Token
        payload = self.verify_token(token)
        if not payload:
            return {
                "success": False,
                "message": "无效的Token"
            }

        return {
            "success": True,
            "message": "登出成功"
        }


# 创建全局认证实例
auth = UserAuth()
