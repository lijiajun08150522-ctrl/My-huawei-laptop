# 🛡️ Flask安全功能文档

## 📋 功能概述

为Flask应用添加了完整的安全功能，包括JWT用户认证、CSRF防护、XSS防护等。

---

## 🎯 核心功能

### 1. JWT 用户认证 (`auth.py`)

#### 功能特性
- ✅ 用户注册/登录
- ✅ JWT Token生成和验证
- ✅ Token刷新机制
- ✅ 密码SHA-256加密存储
- ✅ 默认管理员账户

#### 默认账户
- **用户名**: `admin`
- **密码**: `admin123`
- **角色**: `admin`

---

### 2. CSRF 防护 (`security.py`)

#### 功能特性
- ✅ CSRF Token生成和验证
- ✅ Token存储在session中
- ✅ 自动验证POST/PUT/DELETE请求
- ✅ 使用安全的随机数生成器

---

### 3. XSS 防护 (`security.py`)

#### 功能特性
- ✅ HTML特殊字符转义
- ✅ 输入数据清理
- ✅ 支持字符串、列表、字典

#### 转义字符
| 字符 | 转义后 |
|------|--------|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |
| `/` | `&#x2F;` |

---

### 4. 安全响应头

#### 安全头列表
| 响应头 | 值 | 作用 |
|--------|-----|------|
| X-Content-Type-Options | nosniff | 防止MIME类型嗅探 |
| X-Frame-Options | DENY | 防止点击劫持 |
| X-XSS-Protection | 1; mode=block | 启用XSS保护 |
| Content-Security-Policy | 多重策略 | 内容安全策略 |
| Referrer-Policy | strict-origin-when-cross-origin | Referrer策略 |

---

## 🚀 API接口

### 认证接口

#### 1. 获取CSRF Token
```
GET /api/auth/csrf-token
```

**响应示例**:
```json
{
  "success": true,
  "csrf_token": "a1b2c3d4e5f6..."
}
```

#### 2. 用户注册
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123",
  "email": "test@example.com"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "注册成功",
  "username": "testuser"
}
```

#### 3. 用户登录
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "登录成功",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "admin",
  "role": "admin"
}
```

#### 4. 刷新Token
```
POST /api/auth/refresh
Content-Type: application/json

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应示例**:
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 5. 获取用户信息
```
GET /api/auth/profile
Authorization: Bearer <token>
```

**响应示例**:
```json
{
  "success": true,
  "user": {
    "email": "admin@example.com",
    "created_at": "2026-02-01T12:00:00",
    "role": "admin"
  }
}
```

#### 6. 修改密码
```
PUT /api/auth/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "old_password": "admin123",
  "new_password": "newpassword123"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "密码修改成功"
}
```

#### 7. 获取用户列表（仅管理员）
```
GET /api/auth/users
Authorization: Bearer <token>
```

---

## 🔧 装饰器

### 1. `@jwt_required`
JWT认证装饰器，验证请求是否包含有效的Token。

**使用示例**:
```python
@app.route('/api/protected', methods=['GET'])
@jwt_required
def protected_route():
    username = g.user['username']
    return jsonify({'message': f'Hello, {username}!'})
```

### 2. `@csrf_protected`
CSRF防护装饰器，验证POST/PUT/DELETE请求的CSRF Token。

**使用示例**:
```python
@app.route('/api/data', methods=['POST'])
@csrf_protected
def create_data():
    return jsonify({'success': True})
```

### 3. `@admin_required`
管理员权限装饰器，验证用户是否为管理员。

**使用示例**:
```python
@app.route('/api/admin/users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users():
    return jsonify({'users': []})
```

---

## 💾 数据存储

### 用户数据文件
**位置**: `data/users.json`

**数据结构**:
```json
{
  "admin": {
    "password": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "email": null,
    "created_at": "2026-02-01T12:00:00.000000",
    "role": "admin"
  },
  "testuser": {
    "password": "a1b2c3d4...",
    "email": "test@example.com",
    "created_at": "2026-02-01T13:00:00.000000",
    "role": "user"
  }
}
```

---

## 🧪 测试方法

### 运行测试
```bash
python test_security.py
```

### 测试覆盖
- ✅ 获取CSRF Token
- ✅ 用户注册
- ✅ 用户登录
- ✅ JWT Token验证
- ✅ Token刷新
- ✅ 密码修改
- ✅ XSS防护
- ✅ 安全响应头

---

## 🔒 安全最佳实践

### 1. 前端集成

#### 发送请求时携带Token
```javascript
// 登录获取Token
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});

const data = await response.json();
const token = data.token;

// 存储Token（建议使用sessionStorage或cookie）
localStorage.setItem('authToken', token);

// 后续请求携带Token
fetch('/api/auth/profile', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

#### 获取CSRF Token
```javascript
// 获取CSRF Token
const response = await fetch('/api/auth/csrf-token');
const data = await response.json();
const csrfToken = data.csrf_token;

// POST请求携带CSRF Token
fetch('/api/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRF-Token': csrfToken
  },
  body: JSON.stringify({ description: '新任务' })
});
```

### 2. 密码安全
- 密码至少6个字符
- 建议使用复杂密码（大小写字母+数字+特殊字符）
- 定期更换密码

### 3. Token管理
- Token有效期24小时
- 建议在Token即将过期时刷新
- 登出时清除本地Token

---

## 📊 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    Flask App                         │
├─────────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐    ┌──────────────┐              │
│  │   auth.py    │    │ security.py  │              │
│  │  JWT认证     │    │  安全防护    │              │
│  └──────────────┘    └──────────────┘              │
│         ↓                    ↓                      │
│  ┌──────────────────────────────────────┐          │
│  │         装饰器                   │          │
│  │  @jwt_required  @csrf_protected    │          │
│  └──────────────────────────────────────┘          │
│                                                      │
│  ┌──────────────────────────────────────┐          │
│  │         安全中间件                │          │
│  │     add_security_headers()        │          │
│  └──────────────────────────────────────┘          │
│                                                      │
└─────────────────────────────────────────────────────────┘
         ↓                    ↓
┌──────────────┐    ┌──────────────┐
│ users.json   │    │ Session      │
│ 用户数据     │    │ CSRF Token    │
└──────────────┘    └──────────────┘
```

---

## 🛡️ 安全特性总结

### 认证安全
- ✅ JWT Token认证
- ✅ 密码SHA-256加密
- ✅ Token有效期控制
- ✅ Token刷新机制

### 输入验证
- ✅ XSS输入过滤
- ✅ HTML特殊字符转义
- ✅ 输入长度验证

### 传输安全
- ✅ HTTPS支持（生产环境）
- ✅ Cookie HttpOnly
- ✅ Cookie SameSite

### 响应安全
- ✅ CSP策略
- ✅ X-Frame-Options
- ✅ X-XSS-Protection
- ✅ X-Content-Type-Options

---

## 📝 更新日志

### v1.0 (2026-02-01)

**新增功能**:
- ✅ JWT用户认证系统
- ✅ CSRF防护机制
- ✅ XSS输入过滤
- ✅ 安全响应头
- ✅ 用户注册/登录/登出
- ✅ 密码修改功能
- ✅ 管理员权限控制

**新增文件**:
- `auth.py` - JWT认证模块
- `security.py` - 安全防护模块
- `test_security.py` - 安全测试脚本
- `SECURITY_README.md` - 功能文档

**更新文件**:
- `app.py` - 集成安全功能
- `requirements.txt` - 添加PyJWT依赖

---

## 🚀 生产环境部署建议

### 1. 使用HTTPS
```python
# 在app.py中启用HTTPS
app.run(host='0.0.0.0', port=443,
        ssl_context=('cert.pem', 'key.pem'))
```

### 2. 配置安全的密钥
```python
# 使用环境变量设置JWT密钥
import os
auth = UserAuth(secret_key=os.getenv('JWT_SECRET_KEY'))
```

### 3. 启用Strict-Transport-Security
```python
# 在security.py中取消注释
response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
```

### 4. 配置数据库
考虑使用数据库（如SQLite/PostgreSQL）替代JSON文件存储用户数据。

---

## 📞 支持

如有问题，请联系开发团队。

---

**版本**: v1.0
**最后更新**: 2026-02-01
**作者**: CodeBuddy Team
