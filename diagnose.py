"""
诊断Flask服务和404问题
"""
import os
import socket

print("="*70)
print("Flask Service Diagnostic Tool")
print("="*70)

# 1. 检查当前目录
print("\n[1] Current Directory:")
cwd = os.getcwd()
print(f"    {cwd}")

# 2. 检查templates目录
print("\n[2] Templates Directory:")
templates_path = os.path.join(cwd, 'templates')
print(f"    Path: {templates_path}")
print(f"    Exists: {os.path.exists(templates_path)}")

# 3. 检查index.html
print("\n[3] index.html File:")
index_path = os.path.join(templates_path, 'index.html')
print(f"    Path: {index_path}")
print(f"    Exists: {os.path.exists(index_path)}")
if os.path.exists(index_path):
    size = os.path.getsize(index_path)
    print(f"    Size: {size} bytes")

# 4. 检查Flask模板查找
print("\n[4] Flask Template Configuration:")
try:
    from flask import Flask
    app = Flask(__name__)
    print(f"    Template folder: {app.template_folder}")
    print(f"    Root path: {app.root_path}")
    print(f"    Full template path: {app.root_path}/{app.template_folder}/index.html")
    print(f"    Template exists: {os.path.exists(os.path.join(app.root_path, app.template_folder, 'index.html'))}")
except Exception as e:
    print(f"    Error: {e}")

# 5. 检查网络配置
print("\n[5] Network Configuration:")
local_ip = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    print(f"    Local IP: {local_ip}")
except:
    print(f"    Local IP: Unable to detect")

# 6. 测试模板加载
print("\n[6] Template Loading Test:")
try:
    from flask import Flask, render_template
    app = Flask(__name__)
    with app.app_context():
        result = render_template('index.html', ip='192.168.1.72')
        if result:
            print(f"    Status: SUCCESS")
            print(f"    Output length: {len(result)} bytes")
        else:
            print(f"    Status: FAILED (empty output)")
except Exception as e:
    print(f"    Status: FAILED")
    print(f"    Error: {e}")

# 7. 推荐的URL
print("\n[7] Recommended URLs:")
print(f"    Local: http://127.0.0.1:5000")
if local_ip:
    print(f"    LAN: http://{local_ip}:5000")
    print(f"    Mobile: http://{local_ip}:5000")

print("\n" + "="*70)
print("Diagnostic Complete")
print("="*70)
