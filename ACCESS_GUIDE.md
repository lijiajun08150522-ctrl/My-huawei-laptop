# 任务管理器 - 手机访问指南

## 问题诊断结果

✅ **所有检查通过！**

- `templates/index.html` 文件存在 (34,166 bytes)
- Flask 模板配置正确
- 模板加载测试成功
- 网络配置正常 (IP: 192.168.1.72)

---

## 访问地址

### 📱 手机访问地址

```
http://192.168.1.72:5000
```

### 💻 电脑访问地址

```
http://127.0.0.1:5000
```

---

## 启动步骤

### 方法1：使用自动脚本（推荐）

```bash
python start_with_qrcode.py
```

这个脚本会：
1. 启动Flask服务
2. 在浏览器中打开二维码页面
3. 显示访问地址

### 方法2：手动启动

```bash
# 1. 启动Flask服务
python app.py

# 2. 在另一个终端打开二维码
start qrcode.html
```

### 方法3：使用批处理文件

```bash
# 双击运行
start_server.bat
```

---

## 📱 手机访问方法

### 方法1：直接输入地址（最简单）

1. 确保手机和电脑在同一WiFi网络
2. 打开手机浏览器
3. 输入：`http://192.168.1.72:5000`
4. 点击访问

### 方法2：扫描二维码

1. 运行 `start_with_qrcode.py`
2. 浏览器会自动打开二维码页面
3. 用手机扫描二维码
4. 自动跳转到任务管理器

### 方法3：手动打开二维码

1. 运行 `python app.py`
2. 在浏览器打开 `qrcode.html`
3. 用手机扫描二维码

---

## 🔍 404错误排查

如果您遇到404错误，请按以下步骤检查：

### 1. 检查服务是否启动

```bash
python diagnose.py
```

确保所有检查都显示 "SUCCESS"。

### 2. 检查防火墙

Windows防火墙可能会阻止访问：

- 打开"Windows Defender 防火墙"
- 点击"允许应用或功能通过Windows Defender 防火墙"
- 找到"Python"，勾选"专用网络"和"公用网络"

### 3. 检查IP地址

运行以下命令获取您的IP地址：

```bash
ipconfig
```

找到 "IPv4 地址"（例如：192.168.1.72）

在手机浏览器中使用正确的IP地址。

### 4. 检查端口占用

如果5000端口被占用，修改 `app.py` 中的端口号：

```python
port = 5000  # 改为其他端口，如 8080
```

### 5. 检查网络连接

确保：
- ✅ 电脑和手机连接同一WiFi
- ✅ 电脑网络设置为"专用"网络
- ✅ 防火墙允许Python通信

---

## 📋 测试命令

### 诊断工具

```bash
# 运行完整诊断
python diagnose.py

# 测试模板加载
python test_flask.py
```

### 服务测试

```bash
# 启动服务
python app.py

# 在另一个终端测试
curl http://127.0.0.1:5000
```

---

## 🎯 快速开始

```bash
# 1. 安装依赖（只需一次）
pip install -r requirements.txt

# 2. 启动服务
python start_with_qrcode.py

# 3. 手机访问
http://192.168.1.72:5000
```

---

## 📞 常见问题

### Q: 手机显示"无法访问网页"

A: 检查以下几点：
1. 电脑和手机是否同一WiFi
2. 电脑防火墙是否允许Python
3. IP地址是否正确
4. 服务是否正在运行

### Q: 电脑能访问，手机不能

A: 这是防火墙问题：
1. Windows设置 → 网络和Internet → 属性
2. 改为"专用网络"
2. 允许Python通过防火墙

### Q: IP地址变了怎么办

A: IP地址是动态分配的，重启后可能变化。重新运行 `ipconfig` 查看新IP。

### Q: 如何在局域网外访问

A: 需要使用内网穿透工具（如ngrok、frp）或部署到云服务器。

---

## 📦 相关文件

- `app.py` - Flask服务端
- `templates/index.html` - Web前端
- `qrcode.html` - 二维码页面
- `diagnose.py` - 诊断工具
- `test_flask.py` - 测试工具
- `start_with_qrcode.py` - 启动脚本
- `start_server.bat` - 批处理启动

---

## 🎉 完成！

现在您可以在手机上使用任务管理器了！

**提示**：添加到主屏幕，像APP一样使用！
