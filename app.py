"""
Flask任务管理器Web服务端
基于task.py逻辑，提供REST API和Web界面
集成JWT认证、CSRF防护、XSS防护等安全功能
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import socket

from task import TaskManager
from analytics import TaskAnalyzerService
from snake_ranking import ranking
from auth import auth
from security import security, jwt_required, csrf_protected, init_security
from constants import (
    STATUS_PENDING, STATUS_DONE,
    PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW,
    CATEGORIES, PRIORITY_WEIGHTS,
    DEFAULT_CATEGORY, DEFAULT_SUMMARY_FILE
)

app = Flask(__name__)

# 初始化安全功能
init_security(app)

# 初始化任务管理器
manager = TaskManager()


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
    return app.send_static_file('../snake_game.html')


@app.route('/ranking')
def ranking_page():
    """贪吃蛇排行榜页"""
    return app.send_static_file('../snake_ranking.html')


@app.route('/tasks')
def tasks():
    """任务管理器页"""
    return app.send_static_file('index.html')


@app.route('/presentation')
def presentation():
    """实训报告页"""
    return app.send_static_file('../presentation.html')


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


# ==================== 贪吃蛇排行榜 API ====================

@app.route('/api/snake/ranking', methods=['GET'])
def get_snake_ranking():
    """获取贪吃蛇排行榜"""
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 100)  # 最多返回100条

    records = ranking.get_ranking(limit=limit)
    statistics = ranking.get_statistics()

    return jsonify({
        'success': True,
        'ranking': records,
        'statistics': statistics
    })


@app.route('/api/snake/ranking', methods=['POST'])
def add_snake_score():
    """添加贪吃蛇分数到排行榜"""
    data = request.get_json()

    if not data or 'player_name' not in data or 'score' not in data:
        return jsonify({
            'success': False,
            'message': '请提供玩家名称和分数'
        }), 400

    player_name = data.get('player_name', '').strip()
    score = data.get('score', 0)
    level = data.get('level', 1)

    if not player_name:
        return jsonify({
            'success': False,
            'message': '玩家名称不能为空'
        }), 400

    if not isinstance(score, int) or score < 0:
        return jsonify({
            'success': False,
            'message': '分数必须是非负整数'
        }), 400

    # 添加分数到排行榜
    success = ranking.add_score(player_name, score, level)

    if not success:
        return jsonify({
            'success': False,
            'message': '保存分数失败'
        }), 500

    # 获取玩家排名
    player_best = ranking.get_player_best(player_name)

    return jsonify({
        'success': True,
        'message': '分数已保存',
        'player_best': player_best
    })


@app.route('/api/snake/player/<player_name>', methods=['GET'])
def get_snake_player(player_name):
    """获取玩家最高分"""
    record = ranking.get_player_best(player_name)

    if not record:
        return jsonify({
            'success': False,
            'message': '未找到玩家记录'
        }), 404

    return jsonify({
        'success': True,
        'record': record
    })


@app.route('/api/snake/statistics', methods=['GET'])
def get_snake_statistics():
    """获取排行榜统计信息"""
    stats = ranking.get_statistics()
    return jsonify({
        'success': True,
        'statistics': stats
    })


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': '请求的资源不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'message': '服务器内部错误'}), 500


# ==================== 安全功能 API ====================

@app.route('/api/auth/csrf-token', methods=['GET'])
def get_csrf_token():
    """获取CSRF Token"""
    token = security.get_csrf_token()
    return jsonify({
        'success': True,
        'csrf_token': token
    })


@app.route('/api/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()

    # XSS防护：清理输入
    username = security.sanitize_input(data.get('username', ''))
    password = security.sanitize_input(data.get('password', ''))
    email = security.sanitize_input(data.get('email', ''))

    # 注册用户
    result = auth.register(username, password, email)

    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@app.route('/api/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()

    # XSS防护：清理输入
    username = security.sanitize_input(data.get('username', ''))
    password = security.sanitize_input(data.get('password', ''))

    # 用户登录
    result = auth.login(username, password)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 401


@app.route('/api/auth/logout', methods=['POST'])
@jwt_required
def logout():
    """用户登出"""
    token = request.headers.get('Authorization', '').split(' ')[-1]
    result = auth.logout(token)

    return jsonify(result)


@app.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    """刷新Token"""
    data = request.get_json()
    token = data.get('token', '')

    new_token = auth.refresh_token(token)

    if new_token:
        return jsonify({
            'success': True,
            'token': new_token
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Token无效或已过期'
        }), 401


@app.route('/api/auth/profile', methods=['GET'])
@jwt_required
def get_profile():
    """获取当前用户信息"""
    username = getattr(request, 'user', {}).get('username')
    user_info = auth.get_user_info(username)

    if user_info:
        return jsonify({
            'success': True,
            'user': user_info
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404


@app.route('/api/auth/change-password', methods=['PUT'])
@jwt_required
def change_password():
    """修改密码"""
    data = request.get_json()

    # XSS防护：清理输入
    old_password = security.sanitize_input(data.get('old_password', ''))
    new_password = security.sanitize_input(data.get('new_password', ''))

    username = getattr(request, 'user', {}).get('username')
    result = auth.change_password(username, old_password, new_password)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


@app.route('/api/auth/users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users():
    """获取所有用户列表（仅管理员）"""
    users_list = []
    for username, user_data in auth.users.items():
        user_info = user_data.copy()
        user_info.pop('password', None)  # 移除密码
        user_info['username'] = username
        users_list.append(user_info)

    return jsonify({
        'success': True,
        'users': users_list
    })


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
