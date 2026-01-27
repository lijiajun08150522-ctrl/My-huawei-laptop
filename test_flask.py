"""
测试Flask服务是否正常工作
"""
import sys

# 测试导入
try:
    from app import app
    print("[OK] app.py imported successfully")
except Exception as e:
    print(f"[FAIL] Failed to import app.py: {e}")
    sys.exit(1)

# 测试模板
try:
    with app.app_context():
        from flask import render_template
        result = render_template('index.html', ip='192.168.1.72')
        if result:
            print(f"[OK] index.html template loaded (size: {len(result)} bytes)")
        else:
            print("[FAIL] index.html template loading failed: empty content")
except Exception as e:
    print(f"[FAIL] Failed to load index.html template: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("[OK] All checks passed! Service should work correctly")
print("="*60)
print(f"\nPlease test in browser with following URLs:")
print(f"   Local: http://127.0.0.1:5000")
print(f"   LAN: http://192.168.1.72:5000")
print(f"   Mobile: http://192.168.1.72:5000")
