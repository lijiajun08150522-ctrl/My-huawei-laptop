# 贪吃蛇排行榜功能文档

## 📋 功能概述

贪吃蛇排行榜系统是一个完整的分数管理和展示系统，支持实时排行榜、玩家统计、历史记录等功能。

---

## 🎯 核心功能

### 1. 后端API (`snake_ranking.py`)

#### 排行榜管理类 `SnakeRanking`

| 方法 | 说明 | 参数 |
|------|------|------|
| `add_score()` | 添加分数到排行榜 | `player_name`, `score`, `level` |
| `get_ranking()` | 获取排行榜前N名 | `limit` |
| `get_player_best()` | 获取玩家最高分 | `player_name` |
| `get_statistics()` | 获取统计数据 | - |
| `clear_all()` | 清空排行榜 | - |

### 2. Flask API接口

#### GET `/api/snake/ranking`
获取排行榜数据

**Query参数**:
- `limit`: 返回记录数量（默认10，最大100）

**响应示例**:
```json
{
  "success": true,
  "ranking": [
    {
      "rank": 1,
      "player_name": "玩家1",
      "score": 1000,
      "level": 5,
      "timestamp": "2026-02-01T12:00:00"
    }
  ],
  "statistics": {
    "total_players": 10,
    "highest_score": 1000,
    "average_score": 500,
    "total_games": 50
  }
}
```

#### POST `/api/snake/ranking`
添加分数到排行榜

**请求体**:
```json
{
  "player_name": "玩家1",
  "score": 1000,
  "level": 5
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "分数已保存",
  "player_best": {
    "rank": 1,
    "player_name": "玩家1",
    "score": 1000,
    "level": 5
  }
}
```

#### GET `/api/snake/player/<player_name>`
获取玩家最高分

**响应示例**:
```json
{
  "success": true,
  "record": {
    "rank": 1,
    "player_name": "玩家1",
    "score": 1000,
    "level": 5
  }
}
```

#### GET `/api/snake/statistics`
获取排行榜统计信息

**响应示例**:
```json
{
  "success": true,
  "statistics": {
    "total_players": 10,
    "highest_score": 1000,
    "average_score": 500,
    "total_games": 50
  }
}
```

### 3. 前端页面

#### 游戏页集成 (`/game`)
- 游戏结束自动提交分数
- 玩家名称管理（localStorage）
- 排行榜快捷入口
- 修改玩家名称功能

#### 排行榜页 (`/ranking`)
- TOP 10 排行榜展示
- 实时统计数据（玩家数、最高分、平均分）
- 优雅的动画效果
- 自动刷新（60秒）
- 响应式设计

---

## 🚀 使用方法

### 1. 启动服务

```bash
cd d:\SummerProject
python app.py
```

### 2. 访问游戏

- 游戏页: http://localhost:5000/game
- 排行榜: http://localhost:5000/ranking

### 3. 开始游戏

1. 访问游戏页
2. 按空格键开始游戏
3. 游戏结束后自动提交分数
4. 查看排行榜

---

## 💾 数据存储

### 存储位置
`data/snake_ranking.json`

### 数据结构
```json
{
  "records": [
    {
      "id": "20260201120000000",
      "player_name": "玩家1",
      "score": 1000,
      "level": 5,
      "timestamp": "2026-02-01T12:00:00.000000"
    }
  ],
  "last_updated": "2026-02-01T12:00:00.000000"
}
```

---

## 🎨 UI特性

### 排行榜页面

#### 统计卡片
- **玩家总数**: 显示参与游戏的玩家数量
- **最高分**: 显示历史最高分
- **平均分**: 显示所有游戏的平均分

#### 排行榜表格
- **排名**: 1-3名有特殊颜色（金银铜）
- **玩家名称**: 显示玩家昵称
- **分数**: 显示游戏得分
- **关卡**: 显示达到的最高关卡
- **时间**: 相对时间显示（xx分钟前）

#### 动画效果
- 数字滚动动画
- 卡片悬停效果
- 加载动画

### 游戏页面集成

#### 添加的功能
- 顶部导航栏新增"排行榜"按钮
- 顶部导航栏新增"修改名称"按钮
- 游戏结束自动提交分数
- 玩家名称localStorage持久化

---

## 🔧 技术实现

### 后端

**文件**: `snake_ranking.py`

**特点**:
- 纯Python实现，无外部依赖
- JSON文件持久化存储
- 自动排序和去重
- 最多保留100条记录

### 前端

**文件**: `snake_ranking.html`

**特点**:
- 纯JavaScript实现
- Fetch API调用后端
- 响应式设计
- 自动刷新

### API集成

**文件**: `app.py`

**新增路由**:
- `GET /api/snake/ranking` - 获取排行榜
- `POST /api/snake/ranking` - 添加分数
- `GET /api/snake/player/<name>` - 玩家信息
- `GET /api/snake/statistics` - 统计数据
- `GET /ranking` - 排行榜页面

---

## 📊 统计数据

### 字段说明

| 字段 | 说明 | 计算方式 |
|------|------|---------|
| `total_players` | 玩家总数 | 去重后的玩家名称数量 |
| `highest_score` | 最高分 | 所有记录中的最高分 |
| `average_score` | 平均分 | 所有分数的平均值 |
| `total_games` | 游戏总数 | 排行榜记录总数 |

---

## 🎮 玩家功能

### 1. 修改玩家名称

在游戏页面点击"修改名称"按钮，输入新的玩家名称。

### 2. 查看个人排名

游戏结束后，如果分数足够高，会显示个人排名。

### 3. 查看排行榜

点击"排行榜"按钮，查看TOP 10玩家。

---

## 🔄 自动刷新

排行榜页面每60秒自动刷新一次，确保数据实时性。

---

## 📱 响应式设计

### 桌面端 (≥768px)
- 3列统计卡片
- 完整表格显示
- 大字体和按钮

### 移动端 (<768px)
- 1列统计卡片
- 表格横向滚动
- 优化字体大小

---

## 🧪 测试方法

### 1. 手动测试

```bash
# 启动服务
python app.py

# 访问游戏
http://localhost:5000/game

# 玩几局游戏，然后查看排行榜
http://localhost:5000/ranking
```

### 2. API测试

```bash
# 添加分数
curl -X POST http://localhost:5000/api/snake/ranking \
  -H "Content-Type: application/json" \
  -d '{"player_name":"测试玩家","score":1000,"level":5}'

# 获取排行榜
curl http://localhost:5000/api/snake/ranking?limit=10

# 获取统计数据
curl http://localhost:5000/api/snake/statistics
```

### 3. 使用Postman测试

导入以下请求：

#### POST 添加分数
```
URL: http://localhost:5000/api/snake/ranking
Method: POST
Headers:
  Content-Type: application/json
Body:
{
  "player_name": "测试玩家",
  "score": 1000,
  "level": 5
}
```

#### GET 获取排行榜
```
URL: http://localhost:5000/api/snake/ranking?limit=10
Method: GET
```

#### GET 获取统计
```
URL: http://localhost:5000/api/snake/statistics
Method: GET
```

---

## 🛡️ 数据安全

### 输入验证

- 玩家名称不能为空
- 分数必须是非负整数
- 自动去除名称前后空格

### 数据限制

- 最多保留100条记录
- 自动按分数降序排序
- 历史记录不会丢失（在data文件中）

---

## 📝 开发日志

### v1.0 (2026-02-01)

**新增功能**:
- ✅ 排行榜后端API (`snake_ranking.py`)
- ✅ Flask API接口
- ✅ 排行榜前端页面 (`snake_ranking.html`)
- ✅ 游戏页面集成
- ✅ 自动分数提交
- ✅ 玩家名称管理

**技术实现**:
- ✅ JSON文件持久化
- ✅ 实时数据刷新
- ✅ 响应式设计
- ✅ 动画效果

---

## 🚀 未来扩展

### 计划功能

- [ ] 每日排行榜
- [ ] 本周排行榜
- [ ] 玩家成就系统
- [ ] 游戏统计图表
- [ ] 玩家头像
- [ ] 社交分享功能

---

## 📞 支持

如有问题，请联系开发团队。

---

**版本**: v1.0
**最后更新**: 2026-02-01
**作者**: CodeBuddy Team
