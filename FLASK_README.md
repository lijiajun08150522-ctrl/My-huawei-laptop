# Flask任务管理器 - Web服务端

基于Flask的任务管理Web服务，支持局域网手机访问。

## 🚀 快速启动

### 1. 安装依赖

```bash
cd D:\SummerProject
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

### 3. 查看访问地址

启动后会显示：

```
======================================================================
任务管理器 Web服务
======================================================================

🌐 服务地址:
   本机访问: http://127.0.0.1:5000
   局域网: http://192.168.1.100:5000

📱 手机访问:
   确保手机和电脑在同一WiFi
   在手机浏览器打开: http://192.168.1.100:5000

⚠️  防火墙:
   如无法访问，请允许Python通过防火墙

按 Ctrl+C 停止服务
======================================================================
```

## 📱 手机使用步骤

### 1. 确保网络连接
- 电脑和手机连接同一WiFi
- 或使用热点共享

### 2. 启动服务
- 在电脑上运行 `python app.py`
- 记录显示的局域网IP地址

### 3. 手机访问
- 打开手机浏览器
- 输入显示的局域网地址
- 例如：`http://192.168.1.100:5000`

### 4. 添加到主屏幕（推荐）
- 浏览器菜单 → "添加到主屏幕"
- 像原生APP一样使用

## 🎯 功能特性

### 后端（Flask）
- ✅ RESTful API设计
- ✅ 任务CRUD操作
- ✅ 统计数据接口
- ✅ 报表导出接口
- ✅ 实时同步到tasks.json
- ✅ 按优先级和创建时间排序

### 前端（HTML + JS）
- ✅ 响应式设计
- ✅ 移动端优先
- ✅ 实时数据更新
- ✅ 任务列表展示
- ✅ 添加任务表单
- ✅ 统计报表页面
- ✅ 积压警告

## 🔌 API接口

### 获取任务列表
```
GET /api/tasks
```

### 添加任务
```
POST /api/tasks
Content-Type: application/json

{
  "description": "任务描述",
  "priority": "Medium",
  "category": "General"
}
```

### 标记完成
```
PUT /api/tasks/{id}/done
```

### 删除任务
```
DELETE /api/tasks/{id}
```

### 清除已完成
```
DELETE /api/tasks/completed/clear
```

### 获取统计
```
GET /api/stats
```

### 导出报表
```
GET /api/report/export
```

## 💾 数据存储

- **文件位置**: `.tasks.json`
- **同步机制**: Web操作实时同步到文件
- **CLI兼容**: 与命令行工具使用同一数据源

## 🔧 配置说明

### 修改端口
编辑 `app.py`：
```python
port = 5000  # 改为您想要的端口
```

### 修改监听地址
编辑 `app.py`：
```python
app.run(host='0.0.0.0', port=port, debug=True)
```

## ⚠️ 常见问题

### Q: 手机无法访问
A:
1. 确认电脑和手机在同一WiFi
2. 检查防火墙是否允许Python
3. 尝试关闭防火墙测试
4. 检查IP地址是否正确

### Q: 防火墙提示
A:
- Windows: 选择"允许访问"
- Mac: 在系统偏好设置中允许

### Q: 端口被占用
A: 修改 `app.py` 中的端口号

### Q: 数据不保存
A: 确保 `.tasks.json` 文件有写入权限

## 📊 架构说明

```
Flask服务端 (app.py)
    ↓
REST API
    ↓
Web前端 (templates/index.html)
    ↓
JSON存储 (.tasks.json)
    ↓
CLI工具 (task.py)
```

## 🎨 技术栈

### 后端
- Flask 2.3.3
- Python 3.8+
- JSON存储

### 前端
- HTML5
- CSS3
- Vanilla JavaScript (ES6+)
- Fetch API

## 📝 开发说明

### 调试模式
```bash
# debug=True 会显示详细错误信息
app.run(host='0.0.0.0', port=port, debug=True)
```

### 生产环境
```bash
# debug=False 提高性能和安全性
app.run(host='0.0.0.0', port=port, debug=False)
```

## 🚀 后续优化

- [ ] 用户认证
- [ ] WebSocket实时更新
- [ ] 数据库存储（SQLite）
- [ ] 图片上传
- [ ] 任务分享功能
- [ ] 云同步功能

## 📄 许可证

MIT License

---

**享受局域网任务管理！** 🎉
