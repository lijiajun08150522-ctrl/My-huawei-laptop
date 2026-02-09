"""
Flask任务管理器Web服务端
基于task.py逻辑，提供REST API和Web界面
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from datetime import datetime
import socket
import os
import uuid
import time

from task import TaskManager
from analytics import TaskAnalyzerService
from constants import (
    STATUS_PENDING, STATUS_DONE,
    PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW,
    CATEGORIES, PRIORITY_WEIGHTS,
    DEFAULT_CATEGORY, DEFAULT_SUMMARY_FILE
)
from comfyui_client import ComfyUIClient, SkinGenerator, MockSkinGenerator

app = Flask(__name__)

# 初始化任务管理器
manager = TaskManager()

# 初始化皮肤生成器
# 根据环境变量选择使用真实 ComfyUI 或模拟模式
COMFYUI_URL = os.getenv("COMFYUI_URL", "http://127.0.0.1:8188")
USE_MOCK = os.getenv("USE_MOCK_SKIN_GENERATOR", "true").lower() == "true"

if USE_MOCK:
    print("[INFO] 使用模拟皮肤生成器 (MockSkinGenerator)")
    skin_generator = MockSkinGenerator()
else:
    print(f"[INFO] 使用真实 ComfyUI 服务: {COMFYUI_URL}")
    skin_generator = SkinGenerator(comfyui_url=COMFYUI_URL)

# 全局皮肤URL（用于贪吃蛇游戏）
snake_skin_url = None

# 创建存储目录
SKINS_DIR = "data/skins"
os.makedirs(SKINS_DIR, exist_ok=True)


def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def task_to_dict(task):
    """将任务对象转换为字典"""
    return {
        'id': task.id,
        'description': task.description,
        'status': task.status,
        'priority': getattr(task, 'priority', 'Medium'),
        'category': getattr(task, 'category', 'General'),
        'createdAt': task.createdAt,
        'completedAt': task.completedAt
    }


def sort_tasks(tasks):
    """按优先级和创建时间排序任务"""
    def sort_key(task):
        priority = getattr(task, 'priority', 'Medium')
        weight = PRIORITY_WEIGHTS.get(priority, 2)
        created_at = datetime.fromisoformat(task.createdAt.replace('Z', '+00:00'))
        return (-weight, -created_at.timestamp())

    return sorted(tasks, key=sort_key)


# ==================== 路由 ====================

@app.route('/')
def index():
    """首页"""
    print(f"[DEBUG] Template folder: {app.template_folder}")
    print(f"[DEBUG] Root path: {app.root_path}")
    print(f"[DEBUG] Full template path: {app.root_path}/{app.template_folder}/index.html")
    return render_template('index.html', ip=get_local_ip())


@app.route('/game')
def game():
    """贪吃蛇游戏页"""
    return send_from_directory('.', 'snake_game.html')


@app.route('/tasks')
def tasks():
    """任务管理器页"""
    return send_from_directory('web', 'index.html')


@app.route('/presentation')
def presentation():
    """实训报告页"""
    return send_from_directory('.', 'presentation.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取所有任务"""
    tasks = [task_to_dict(task) for task in manager.tasks]
    # 按优先级和创建时间排序
    tasks = sort_tasks(tasks)
    return jsonify({
        'success': True,
        'tasks': tasks
    })


@app.route('/api/tasks', methods=['POST'])
def add_task():
    """添加任务"""
    data = request.get_json()

    if not data or 'description' not in data:
        return jsonify({'success': False, 'message': '请提供任务描述'}), 400

    description = data.get('description', '').strip()
    if not description:
        return jsonify({'success': False, 'message': '任务描述不能为空'}), 400

    # 添加任务
    result = manager.add(description)

    # 获取新添加的任务
    new_task = manager._find_task(
        max([task.id for task in manager.tasks], default=0)
    )

    # 设置优先级和分类
    if new_task:
        new_task.priority = data.get('priority', 'Medium')
        new_task.category = data.get('category', 'General')
        manager._save_tasks()

    return jsonify({
        'success': True,
        'message': result,
        'task': task_to_dict(new_task) if new_task else None
    })


@app.route('/api/tasks/<int:task_id>/done', methods=['PUT'])
def done_task(task_id):
    """标记任务完成"""
    result = manager.done(task_id)
    if "not found" in result.lower() or "already done" in result.lower():
        return jsonify({'success': False, 'message': result}), 404

    return jsonify({
        'success': True,
        'message': result
    })


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    result = manager.delete(task_id)
    if "not found" in result.lower():
        return jsonify({'success': False, 'message': result}), 404

    return jsonify({
        'success': True,
        'message': result
    })


@app.route('/api/tasks/completed/clear', methods=['DELETE'])
def clear_completed():
    """清除已完成任务"""
    result = manager.clear()
    return jsonify({
        'success': True,
        'message': result
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    stats = manager.analyzer.get_statistics()
    return jsonify({
        'success': True,
        'stats': stats
    })


@app.route('/api/report/export', methods=['GET'])
def export_report():
    """导出报表"""
    filepath = DEFAULT_SUMMARY_FILE
    result = manager.analyzer.export_summary(filepath)
    return jsonify({
        'success': True,
        'message': result,
        'filepath': filepath
    })


# ==================== AI 皮肤生成接口 ====================

@app.route('/api/skin/generate', methods=['POST'])
def generate_skin():
    """
    生成贪吃蛇皮肤
    调用 ComfyUI API 生成皮肤图片
    """
    global snake_skin_url

    try:
        data = request.get_json()

        # 固定提示词
        prompt = "Neon glowing snake, cyberpunk style, high resolution"
        player_id = data.get('player_id', 'player_' + str(int(time.time())))

        # 提交生成任务
        success, task_id, message = skin_generator.generate_skin(
            prompt=prompt,
            player_id=player_id,
            style='cyberpunk',
            width=512,
            height=512
        )

        if success:
            return jsonify({
                'success': True,
                'task_id': task_id,
                'message': message,
                'prompt': prompt
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400

    except Exception as e:
        print(f"[ERROR] 生成皮肤失败: {e}")
        return jsonify({
            'success': False,
            'message': f"生成失败: {str(e)}"
        }), 500


@app.route('/api/skin/status/<task_id>', methods=['GET'])
def get_skin_status(task_id):
    """
    查询皮肤生成状态
    轮询接口，返回进度和图片URL
    """
    global snake_skin_url

    try:
        result = skin_generator.get_skin_status(task_id)

        # 如果生成完成，更新全局皮肤URL
        if result.get('success') and result.get('status') == 'completed':
            image_url = result.get('image_url')
            if image_url:
                snake_skin_url = image_url
                print(f"[INFO] 皮肤生成完成，已更新全局 snake_skin_url: {snake_skin_url}")

        return jsonify(result)

    except Exception as e:
        print(f"[ERROR] 查询状态失败: {e}")
        return jsonify({
            'success': False,
            'status': 'failed',
            'message': f"查询失败: {str(e)}"
        }), 500


@app.route('/api/skin/image/<filename>', methods=['GET'])
def get_skin_image(filename):
    """
    获取皮肤图片
    返回生成的皮肤图片
    """
    import random
    from io import BytesIO
    from PIL import Image, ImageDraw, ImageFont

    try:
        # 尝试从存储目录读取
        filepath = os.path.join(SKINS_DIR, filename)

        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/png')

        # 如果是模拟模式，生成赛博朋克风格的占位图
        if USE_MOCK:
            # 创建赛博朋克风格的占位图
            img = Image.new('RGB', (512, 512), color=(10, 10, 30))
            draw = ImageDraw.Draw(img)

            # 绘制霓虹网格背景
            for i in range(0, 512, 32):
                draw.line([(0, i), (512, i)], fill=(20, 0, 40), width=1)
                draw.line([(i, 0), (i, 512)], fill=(20, 0, 40), width=1)

            # 绘制霓虹蛇形纹理
            colors = [
                (255, 0, 255),   # 紫色
                (0, 255, 255),   # 青色
                (255, 0, 128),   # 洋红
                (128, 0, 255),   # 蓝紫
            ]

            for i in range(0, 512, 64):
                color_idx = i // 64 % len(colors)
                color = colors[color_idx]

                # 绘制渐变矩形
                for offset in range(5):
                    alpha = int(255 * (5 - offset) / 5)
                    draw.rectangle(
                        [i + offset, offset, i + 32 - offset, 512 - offset],
                        fill=color
                    )

                # 添加霓虹发光效果
                draw.rectangle([i - 2, 0, i + 34, 512], outline=(255, 0, 255), width=2)

            # 添加文字
            try:
                # 尝试使用系统字体
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()

            text = "CYBERPUNK"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 添加文字阴影
            shadow_offset = 4
            position_x = (512 - text_width) // 2
            position_y = (512 - text_height) // 2 - 50

            draw.text(
                (position_x + shadow_offset, position_y + shadow_offset),
                text,
                fill=(0, 0, 0),
                font=font
            )

            # 添加霓虹文字
            draw.text(
                (position_x, position_y),
                text,
                fill=(0, 255, 255),
                font=font
            )

            text2 = "SNAKE SKIN"
            bbox2 = draw.textbbox((0, 0), text2, font=font)
            text2_width = bbox2[2] - bbox2[0]
            text2_height = bbox2[3] - bbox2[1]

            position2_x = (512 - text2_width) // 2
            position2_y = (512 - text2_height) // 2 + 50

            draw.text(
                (position2_x + shadow_offset, position2_y + shadow_offset),
                text2,
                fill=(0, 0, 0),
                font=font
            )

            draw.text(
                (position2_x, position2_y),
                text2,
                fill=(255, 0, 255),
                font=font
            )

            # 转换为字节流
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            return send_file(img_io, mimetype='image/png')

        return jsonify({
            'success': False,
            'message': '图片不存在'
        }), 404

    except Exception as e:
        print(f"[ERROR] 获取图片失败: {e}")
        return jsonify({
            'success': False,
            'message': f"获取图片失败: {str(e)}"
        }), 500


@app.route('/api/skin/current', methods=['GET'])
def get_current_skin():
    """
    获取当前贪吃蛇皮肤URL
    前端轮询此接口获取最新皮肤
    """
    global snake_skin_url

    return jsonify({
        'success': True,
        'skin_url': snake_skin_url
    })


@app.route('/api/skin/apply', methods=['POST'])
def apply_skin():
    """
    应用皮肤到贪吃蛇游戏
    设置 snake_skin_url 并刷新游戏
    """
    global snake_skin_url

    try:
        data = request.get_json()
        image_url = data.get('image_url')

        if not image_url:
            return jsonify({
                'success': False,
                'message': 'image_url 不能为空'
            }), 400

        # 更新全局皮肤URL
        snake_skin_url = image_url
        print(f"[INFO] 应用皮肤: {snake_skin_url}")

        return jsonify({
            'success': True,
            'message': '皮肤已应用',
            'skin_url': snake_skin_url
        })

    except Exception as e:
        print(f"[ERROR] 应用皮肤失败: {e}")
        return jsonify({
            'success': False,
            'message': f"应用失败: {str(e)}"
        }), 500


@app.route('/api/skin/history', methods=['GET'])
def get_skin_history():
    """
    获取皮肤生成历史
    """
    try:
        player_id = request.args.get('player_id', 'default')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))

        result = skin_generator.get_skin_history(
            player_id=player_id,
            page=page,
            limit=limit
        )

        return jsonify(result)

    except Exception as e:
        print(f"[ERROR] 获取历史失败: {e}")
        return jsonify({
            'success': False,
            'message': f"获取历史失败: {str(e)}"
        }), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': '请求的资源不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'message': '服务器内部错误'}), 500


# ==================== 启动服务 ====================

if __name__ == '__main__':
    local_ip = get_local_ip()
    port = 5000

    print("=" * 70)
    print("任务管理器 Web服务")
    print("=" * 70)
    print(f"\n服务地址:")
    print(f"   本机访问: http://127.0.0.1:{port}")
    print(f"   局域网: http://{local_ip}:{port}")
    print(f"\n手机访问:")
    print(f"   确保手机和电脑在同一WiFi")
    print(f"   在手机浏览器打开: http://{local_ip}:{port}")
    print(f"\n防火墙:")
    print(f"   如无法访问，请允许Python通过防火墙")
    print(f"\n按 Ctrl+C 停止服务")
    print("=" * 70 + "\n")

    app.run(host='0.0.0.0', port=port, debug=True)
