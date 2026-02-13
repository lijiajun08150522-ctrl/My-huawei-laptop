# Remake AI Frontend

闲置资源回收利用智能平台 - 前端界面

## 技术栈
- HTML5
- Tailwind CSS (CDN)
- Vanilla JavaScript

## 文件结构

```
frontend/
├── index.html          # 主页面
├── css/               # 样式文件（可选）
└── js/                # JavaScript 文件（可选）
```

## 启动

直接在浏览器中打开 `index.html` 文件

或者使用本地服务器：

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

访问 http://localhost:8000

## 配置

在 `index.html` 中修改 API 地址：

```javascript
// 修改 API_BASE_URL 为实际的后端地址
const API_BASE_URL = 'http://localhost:5000';
```

## 功能

- 输入闲置物品名称
- AI 价值评估
- 改造建议展示
- ComfyUI 改造效果图
- 碳减排量统计

## API 集成

前端通过 `/api/remake` 接口与后端通信

需要先调用 `/api/auth/login` 获取 JWT token

## 样式主题

- 主色调：绿色系（环保可持续）
- 设计风格：极简、玻璃拟态
- 响应式：支持移动端和桌面端
