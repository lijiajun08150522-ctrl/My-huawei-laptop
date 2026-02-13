# Remake AI Backend

闲置资源回收利用智能平台 - 后端服务

## 技术栈
- Flask 3.0.0
- SQLite 数据库
- JWT 认证
- ComfyUI 集成

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 复制配置文件
copy .env.example .env
```

## 启动

```bash
python app.py
```

服务将在 http://localhost:5000 启动

## API 接口

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 改造接口
- `POST /api/remake` - 闲置物品改造（需要JWT认证）
  - Headers: `Authorization: Bearer <token>`
  - Body: `{"item_name": "旧牛仔裤", "description": "描述"}`

### 查询接口
- `GET /api/user/:user_id/records` - 获取用户记录（需要JWT认证）
- `GET /api/trending/remakes` - 获取热门改造案例

## 数据库

数据库文件：`remake_ai.db`

表结构：
- `remake_records` - 改造记录
- `users` - 用户
- `carbon_factors` - 碳排放因子
