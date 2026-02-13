# Remake AI

闲置资源回收利用智能平台

让每一件闲置物品焕发新生 🌍

## 项目简介

Remake AI 利用人工智能技术识别闲置物品的价值，并生成创意改造效果图，促进资源循环利用，减少碳排放。

## 项目结构

```
remake-ai/
├── backend/           # 后端服务
│   ├── app.py         # Flask 应用
│   ├── models.py      # 数据模型
│   ├── comfyui_client.py  # ComfyUI 客户端
│   ├── requirements.txt    # Python 依赖
│   └── .env.example   # 环境变量示例
└── frontend/          # 前端界面
    └── index.html     # 主页面
```

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
copy .env.example .env
python app.py
```

后端服务将在 http://localhost:5000 启动

### 前端启动

```bash
cd frontend
# 直接在浏览器打开 index.html
# 或使用本地服务器
python -m http.server 8000
```

前端界面访问 http://localhost:8000

## 核心功能

### 1. AI 价值识别
- 通过 Dify AI 识别物品价值和改造潜力
- 根据材质分类（织物、塑料、金属等）
- 提供实用改造建议和创意 DIY 想法

### 2. 改造效果图生成
- 集成 ComfyUI 生成高质量改造效果图
- 1024x1024 高清输出
- 针对不同材质定制风格提示词

### 3. 碳减排计算
- 根据物品类别计算碳排放减少量
- 提供等价说明（如"相当于种植 X 棵树"）
- 记录用户环保贡献

### 4. 数据追踪
- 用户改造记录存储
- 历史记录查询
- 热门改造案例统计

## 技术架构

```
用户 → 前端 (HTML/JS) → 后端 API (Flask) 
                          ↓
                    ├─ Dify AI (价值识别)
                    ├─ ComfyUI (图片生成)
                    └─ SQLite (数据存储)
```

## API 文档

详见 `backend/README.md`

主要接口：
- `POST /api/remake` - 闲置物品改造
- `POST /api/auth/login` - 用户登录
- `GET /api/user/:user_id/records` - 用户记录

## 环境要求

- Python 3.8+
- ComfyUI 服务（可选，用于图片生成）

## 配置说明

### 后端配置 (backend/.env)

```env
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
COMFYUI_URL=http://127.0.0.1:8188
DATABASE_PATH=remake_ai.db
```

### 前端配置 (frontend/index.html)

```javascript
const API_BASE_URL = 'http://localhost:5000';
```

## 设计规约

详细设计文档见项目根目录的 `REMAKE_AI_SDD.md`

## 开发计划

- [x] SDD 规约文档
- [x] 前端界面
- [x] 后端 API
- [x] 数据模型
- [ ] 真实 Dify 集成（当前为模拟）
- [ ] ComfyUI 真实服务集成
- [ ] 用户系统完善
- [ ] 测试覆盖

## 贡献

欢迎贡献代码和建议！

## 许可证

MIT License
