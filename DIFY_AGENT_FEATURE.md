# Dify Agent 智能代理系统 - 功能文档

## 概述

Dify Agent 是一个模拟 Dify AI Agent 的智能系统，能够根据当前日期自动决定每日挑战主题，生成对应的 ComfyUI 提示词，并调用皮肤生成接口。

---

## 核心功能

### 1. 智能主题选择

**自动主题轮换：**
- 周日：赛博朋克（Cyberpunk）
- 周一：奇幻冒险（Fantasy）
- 周二：像素艺术（Pixel Art）
- 周三：自然生态（Nature）
- 周四：深海探险（Ocean）
- 周五：星际穿越（Space）
- 周六：龙之传说（Dragon）

### 2. 提示词生成

**功能：**
- 基于主题生成 ComfyUI 提示词
- 支持自定义描述
- 自动添加风格关键词

### 3. 每日挑战系统

**挑战内容：**
- 主题名称和描述
- 颜色调色板
- 额外挑战目标（2-3个）
- 每日格言

---

## API 接口

### 1. 获取每日挑战
```
GET /api/agent/daily
```

### 2. 获取当前主题
```
GET /api/agent/theme
```

### 3. 生成提示词
```
POST /api/agent/prompt
Body: { "theme_key": "cyberpunk", "description": "custom" }
```

### 4. Agent 生成皮肤
```
POST /api/agent/generate-skin
Body: { "player_id": "player_001", "theme_key": "cyberpunk" }
```

### 5. 获取主题日历
```
GET /api/agent/calendar?weeks=4
```

---

## 使用示例

```bash
# 获取今日挑战
curl http://127.0.0.1:5000/api/agent/daily

# 生成今日皮肤
curl -X POST http://127.0.0.1:5000/api/agent/generate-skin \
  -H "Content-Type: application/json" \
  -d '{"player_id": "player_001"}'

# 查看主题日历
curl http://127.0.0.1:5000/api/agent/calendar?weeks=4
```

---

## 主题说明

| 主题 | 星期 | 风格 | 颜色 |
|------|------|------|------|
| 赛博朋克 | 周日 | 霓虹灯光、未来科技 | 紫色、青色、洋红 |
| 奇幻冒险 | 周一 | 魔法森林、奇幻生物 | 金色、绿色、紫色 |
| 像素艺术 | 周二 | 复古游戏、8-bit | 红色、青绿、天蓝 |
| 自然生态 | 周三 | 森林、动物花纹 | 森绿、浅绿 |
| 深海探险 | 周四 | 珊瑚礁、海底 | 暗蓝、深海蓝 |
| 星际穿越 | 周五 | 宇宙星空、星云 | 蓝紫、蓝色 |
| 龙之传说 | 周六 | 龙鳞、火焰特效 | 深红、橙红 |

---

## 集成到前端

```javascript
// 获取今日挑战
async function getDailyChallenge() {
    const response = await fetch('/api/agent/daily');
    const result = await response.json();

    if (result.success) {
        const challenge = result.challenge;
        // 显示挑战信息
        console.log(`今日主题: ${challenge.challenge_title}`);
        console.log(`提示词: ${challenge.prompt}`);
    }
}
```

---

## 测试

```bash
# 启动服务
python app.py

# 测试 API
curl http://127.0.0.1:5000/api/agent/daily
curl http://127.0.0.1:5000/api/agent/theme
curl http://127.0.0.1:5000/api/agent/calendar?weeks=4
```

---

## 扩展和自定义

### 修改主题安排

编辑 `dify_agent.py` 中的 `WEEKLY_THEME_SCHEDULE`。

### 添加新主题

在 `DAILY_THEMES` 字典中添加新主题配置。

---

## 总结

Dify Agent 系统为贪吃蛇游戏带来了：
- 每日主题轮换
- 智能提示词生成
- 每日挑战系统
- 主题日历查看
- 每日格言

所有功能通过 REST API 提供，便于前端集成！
