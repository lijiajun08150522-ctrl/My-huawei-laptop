"""
启动Flask服务并生成二维码
"""
import socket
import webbrowser
import os
from app import app

# 获取本机IP
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000

    print("=" * 70)
    print("Task Manager Web Service")
    print("=" * 70)
    print(f"\nServer Addresses:")
    print(f"   Local: http://127.0.0.1:5000")
    print(f"   LAN: http://{local_ip}:{port}")
    print(f"\nMobile Access:")
    print(f"   Make sure phone and PC are on same WiFi")
    print(f"   Open in mobile browser: http://{local_ip}:{port}")
    print(f"\nQR Code:")
    print(f"   Open qrcode.html in browser to scan QR code")
    print(f"   Or visit: file://{os.path.abspath('qrcode.html')}")
    print(f"\nFirewall:")
    print(f"   Allow Python through firewall if needed")
    print(f"\nPress Ctrl+C to stop server")
    print("=" * 70 + "\n")

    # 在浏览器中打开二维码页面
    try:
        qrcode_path = os.path.abspath('qrcode.html')
        webbrowser.open(f'file:///{qrcode_path}')
        print(f"[INFO] QR code page opened in browser")
    except:
        print(f"[INFO] Failed to open QR code page automatically")
        print(f"[INFO] Open manually: file://{os.path.abspath('qrcode.html')}")

    # 启动服务
    app.run(host='0.0.0.0', port=port, debug=True)
