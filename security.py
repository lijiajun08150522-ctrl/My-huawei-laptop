"""
安全防护模块
提供XSS/CSRF防护、安全响应头等功能
"""
import secrets
from functools import wraps
from flask import request, session, jsonify, g, make_response
from auth import auth


class SecurityManager:
    """安全管理器"""

    def __init__(self):
        """初始化安全管理器"""
        self.csrf_token_name = "csrf_token"
        self.csrf_header_name = "X-CSRF-Token"

    def generate_csrf_token(self) -> str:
        """
        生成CSRF Token

        Returns:
            随机Token字符串
        """
        return secrets.token_hex(32)

    def get_csrf_token(self) -> str:
        """
        获取或生成CSRF Token（存储在session中）

        Returns:
            CSRF Token
        """
        if self.csrf_token_name not in session:
            session[self.csrf_token_name] = self.generate_csrf_token()
        return session[self.csrf_token_name]

    def verify_csrf_token(self, token: str) -> bool:
        """
        验证CSRF Token

        Args:
            token: 要验证的Token

        Returns:
            验证是否通过
        """
        if self.csrf_token_name not in session:
            return False

        return secrets.compare_digest(session[self.csrf_token_name], token)

    def sanitize_html(self, text: str) -> str:
        """
        转义HTML特殊字符（XSS防护）

        Args:
            text: 原始文本

        Returns:
            转义后的文本
        """
        if not text:
            return ""

        # HTML转义
        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;'
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def sanitize_input(self, data: Any) -> Any:
        """
        清理输入数据

        Args:
            data: 输入数据（可以是字符串、列表、字典）

        Returns:
            清理后的数据
        """
        if isinstance(data, str):
            return self.sanitize_html(data)
        elif isinstance(data, list):
            return [self.sanitize_input(item) for item in data]
        elif isinstance(data, dict):
            return {key: self.sanitize_input(value) for key, value in data.items()}
        else:
            return data


# 创建全局安全管理器实例
security = SecurityManager()


# ==================== 装饰器 ====================

def jwt_required(f):
    """
    JWT认证装饰器

    验证请求是否包含有效的JWT Token
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取Token
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'success': False,
                'message': '缺少认证Token'
            }), 401

        # 提取Token（格式: Bearer <token>）
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({
                'success': False,
                'message': 'Token格式错误'
            }), 401

        # 验证Token
        payload = auth.verify_token(token)

        if not payload:
            return jsonify({
                'success': False,
                'message': 'Token无效或已过期'
            }), 401

        # 将用户信息存入Flask的g对象
        g.user = payload

        return f(*args, **kwargs)

    return decorated_function


def csrf_protected(f):
    """
    CSRF防护装饰器

    验证请求是否包含有效的CSRF Token
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 对于POST/PUT/DELETE请求，验证CSRF Token
        if request.method in ['POST', 'PUT', 'DELETE']:
            # 从请求头或表单获取Token
            token = request.headers.get(security.csrf_header_name)
            if not token:
                token = request.form.get(security.csrf_token_name)
            if not token:
                token = request.json.get(security.csrf_token_name) if request.is_json else None

            if not token or not security.verify_csrf_token(token):
                return jsonify({
                    'success': False,
                    'message': 'CSRF验证失败'
                }), 403

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    管理员权限装饰器

    验证用户是否为管理员
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 确保用户已通过JWT认证
        if not hasattr(g, 'user'):
            return jsonify({
                'success': False,
                'message': '未认证'
            }), 401

        # 检查用户角色
        if g.user.get('role') != 'admin':
            return jsonify({
                'success': False,
                'message': '需要管理员权限'
            }), 403

        return f(*args, **kwargs)

    return decorated_function


# ==================== 安全响应头中间件 ====================

def add_security_headers(response):
    """
    添加安全响应头

    Args:
        response: Flask响应对象

    Returns:
        添加了安全头的响应
    """
    # 防止MIME类型嗅探
    response.headers['X-Content-Type-Options'] = 'nosniff'

    # 防止点击劫持
    response.headers['X-Frame-Options'] = 'DENY'

    # 启用XSS保护
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # 内容安全策略（CSP）
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers['Content-Security-Policy'] = csp

    # 严格传输安全（仅HTTPS）
    # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # Referrer策略
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    return response


def init_security(app):
    """
    初始化安全功能

    Args:
        app: Flask应用实例
    """
    # 配置密钥（用于session）
    app.secret_key = secrets.token_hex(32)

    # 添加安全响应头中间件
    app.after_request(add_security_headers)

    # 配置Cookie安全
    app.config.update(
        SESSION_COOKIE_SECURE = False,  # 生产环境改为True
        SESSION_COOKIE_HTTPONLY = True,  # 防止JavaScript访问Cookie
        SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF防护
    )
