# 🎮 贪吃蛇排行榜 - 快速开始

## ✅ 功能已开发完成！

### 📋 新增文件

| 文件 | 说明 |
|------|------|
| `snake_ranking.py` | 排行榜后端系统 |
| `snake_ranking.html` | 排行榜前端页面 |
| `test_snake_ranking.py` | 自动化测试脚本 |
| `SNAKE_RANKING_README.md` | 完整功能文档 |

### 🔧 修改文件

| 文件 | 修改内容 |
|------|---------|
| `app.py` | 新增4个排行榜API接口 |
| `snake_game.html` | 集成排行榜功能 |

---

## 🚀 立即开始

### 1. 启动服务

```bash
cd d:\SummerProject
python app.py
```

### 2. 访问游戏

**游戏页面**: http://localhost:5000/game

**排行榜页面**: http://localhost:5000/ranking

### 3. 开始游戏

1. 打开游戏页面
2. 按空格键开始游戏
3. 玩几局游戏
4. 查看排行榜

---

## 🎯 核心功能

### 自动提交分数
游戏结束后自动提交分数到排行榜

### 玩家名称管理
- 首次游戏会提示输入玩家名称
- 点击"修改名称"按钮可更改名称
- 名称保存在localStorage

### 实时排行榜
- TOP 10 排行榜
- 实时统计（玩家数、最高分、平均分）
- 每60秒自动刷新

---

## 📊 API接口

### 获取排行榜
```bash
curl http://localhost:5000/api/snake/ranking?limit=10
```

### 添加分数
```bash
curl -X POST http://localhost:5000/api/snake/ranking \
  -H "Content-Type: application/json" \
  -d '{"player_name":"测试玩家","score":1000,"level":5}'
```

### 获取统计
```bash
curl http://localhost:5000/api/snake/statistics
```

---

## 🧪 运行测试

```bash
python test_snake_ranking.py
```

测试包括:
- ✅ 获取统计数据
- ✅ 添加分数验证
- ✅ 排行榜排序
- ✅ 玩家最高分记录
- ✅ 输入验证

---

## 📱 界面预览

### 游戏页面
- 顶部新增"🏆 排行榜"按钮
- 顶部新增"👤 修改名称"按钮
- 游戏结束自动提交分数

### 排行榜页面
- 统计卡片（玩家数、最高分、平均分）
- TOP 10 排行榜表格
- 金银铜牌排名特效
- 自动刷新功能

---

## 💾 数据存储

**存储位置**: `data/snake_ranking.json`

**数据结构**:
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

## 🎨 特性

- ✅ 无需数据库，JSON文件存储
- ✅ 自动排序和去重
- ✅ 最多保留100条记录
- ✅ 实时数据更新
- ✅ 响应式设计
- ✅ 优雅的动画效果
- ✅ 输入验证

---

## 📖 完整文档

查看详细文档: `SNAKE_RANKING_README.md`

---

## 🌟 Git状态

**当前分支**: `feature-ranking`
**状态**: ✅ 已提交并推送到GitHub
**Pull Request**: https://github.com/lijiajun08150522-ctrl/My-huawei-laptop/pull/new/feature-ranking

---

**开始使用吧！🎉**
