# 网页打不开问题解决方案

## 问题症状

访问 `http://localhost:5000` 或 `http://localhost:5000/game` 时网页无法打开。

## 可能原因

### 1. Flask 服务未启动

**检查方法:**
```bash
netstat -ano | findstr :5000
```

如果没有输出，说明服务未运行。

**解决方法:**

#### 方案 1: 使用自动安装和启动脚本（推荐）

```bash
install_and_start.bat
```

这个脚本会自动安装依赖并启动服务。

#### 方案 2: 手动安装依赖

```bash
pip install requests Pillow
python app.py
```

#### 方案 3: 使用 requirements.txt

```bash
pip install -r requirements.txt
python app.py
```

### 2. 缺少 Python 依赖

**错误信息:**
```
ModuleNotFoundError: No module named 'requests'
ModuleNotFoundError: No module named 'PIL'
```

**解决方法:**

安装所有依赖：
```bash
pip install Flask==2.3.3 Werkzeug==2.3.7 requests==2.31.0 Pillow==10.1.0
```

或使用 requirements.txt：
```bash
pip install -r requirements.txt
```

### 3. 端口被占用

**错误信息:**
```
OSError: [WinError 10048] Address already in use
```

**解决方法:**

#### 查找占用端口的进程
```bash
netstat -ano | findstr :5000
```

#### 结束占用端口的进程
```bash
taskkill /PID <进程ID> /F
```

#### 或修改 app.py 中的端口号
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### 4. 防火墙阻止

**解决方法:**

1. 打开 Windows 防火墙设置
2. 允许 Python 通过防火墙
3. 或临时关闭防火墙测试

### 5. 浏览器缓存问题

**解决方法:**

1. 清除浏览器缓存
2. 使用无痕/隐私模式访问
3. 或使用其他浏览器测试

## 启动成功标志

看到以下输出表示启动成功：

```
======================================================
任务管理器 Web服务
======================================================

服务地址:
   本机访问: http://127.0.0.1:5000
   局域网: http://192.168.x.x:5000
...
```

## 访问地址

启动成功后，可以通过以下地址访问：

- **首页**: http://127.0.0.1:5000
- **贪吃蛇游戏**: http://127.0.0.1:5000/game
- **任务管理器**: http://127.0.0.1:5000/tasks
- **实训报告**: http://127.0.0.1:5000/presentation

## 快速诊断

### 1. 检查 Python 是否安装
```bash
python --version
```

### 2. 检查依赖是否安装
```bash
pip list | findstr Flask
pip list | findstr requests
pip list | findstr Pillow
```

### 3. 测试 Flask 是否能运行
```bash
python -c "from flask import Flask; print('Flask OK')"
python -c "import requests; print('requests OK')"
python -c "from PIL import Image; print('Pillow OK')"
```

## 常用命令

```bash
# 启动服务（自动安装依赖）
install_and_start.bat

# 启动服务（手动）
python app.py

# 查看端口占用
netstat -ano | findstr :5000

# 结束进程
taskkill /PID <PID> /F

# 安装单个包
pip install requests
pip install Pillow

# 查看已安装的包
pip list
```

## 如果仍然无法解决

请提供以下信息以便进一步诊断：

1. Python 版本: `python --version`
2. 错误信息: 完整的错误堆栈
3. 端口检查结果: `netstat -ano | findstr :5000`
4. 依赖列表: `pip list`
