#!/usr/bin/env python3
"""
自动Git提交监控脚本
功能：监控当前目录文件变动，自动执行 git add、commit、push
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class AutoGitHandler(FileSystemEventHandler):
    """文件变动处理器"""

    def __init__(self, gitignore_patterns=None):
        super().__init__()
        self.last_event_time = 0
        self.pending_changes = False
        self.debounce_seconds = 3  # 防抖延迟（秒）

        # 默认忽略的文件和目录
        self.ignore_patterns = gitignore_patterns or [
            '__pycache__',
            '.git',
            '.pytest_cache',
            '.idea',
            '.vscode',
            'node_modules',
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.DS_Store',
            'Thumbs.db',
            '*.tmp',
            'auto_git_monitor.py',  # 忽略监控脚本自身
            '.gitignore',
            'weekly-report.md',  # 可选：忽略周报文件
        ]

    def should_ignore(self, file_path):
        """检查文件是否应该被忽略"""
        # 检查目录
        for pattern in self.ignore_patterns:
            if pattern in file_path:
                return True

            # 通配符匹配
            if pattern.startswith('*.'):
                suffix = pattern[1:]
                if file_path.endswith(suffix):
                    return True

        return False

    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return

        if self.should_ignore(event.src_path):
            print(f"[SKIP] 创建事件已忽略: {event.src_path}")
            return

        print(f"[CREATE] 检测到新文件: {event.src_path}")
        self.trigger_git_operation(event.src_path, "create")

    def on_modified(self, event):
        """文件修改事件"""
        if event.is_directory:
            return

        if self.should_ignore(event.src_path):
            return

        print(f"[MODIFY] 检测到文件修改: {event.src_path}")
        self.trigger_git_operation(event.src_path, "modify")

    def on_deleted(self, event):
        """文件删除事件"""
        if event.is_directory:
            return

        if self.should_ignore(event.src_path):
            return

        print(f"[DELETE] 检测到文件删除: {event.src_path}")
        self.trigger_git_operation(event.src_path, "delete")

    def trigger_git_operation(self, file_path, event_type):
        """触发Git操作（带防抖）"""
        self.last_event_time = time.time()
        self.pending_changes = True

        # 等待防抖时间后执行
        time.sleep(self.debounce_seconds)

        # 检查是否有新的文件变动
        if time.time() - self.last_event_time >= self.debounce_seconds:
            if self.pending_changes:
                self.pending_changes = False
                self.commit_and_push(file_path, event_type)

    def commit_and_push(self, file_path, event_type):
        """执行Git提交和推送"""
        try:
            print("\n" + "="*60)
            print("开始执行Git操作")
            print("="*60)

            # 1. 检查Git仓库状态
            print(f"\n[1/5] 检查Git仓库状态...")
            result = subprocess.run(
                ['git', 'status', '--short'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )

            if not result.stdout.strip():
                print("    没有需要提交的更改")
                return

            print(f"    检测到更改:")
            for line in result.stdout.strip().split('\n'):
                print(f"      {line}")

            # 2. 添加所有更改
            print(f"\n[2/5] 添加更改到暂存区...")
            result = subprocess.run(
                ['git', 'add', '.'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )

            if result.returncode != 0:
                print(f"    git add 失败: {result.stderr}")
                return

            print("    ✓ git add 成功")

            # 3. 生成提交信息
            print(f"\n[3/5] 提交更改...")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = os.path.basename(file_path)

            if event_type == "create":
                commit_message = f"feat: add {filename} - {timestamp}"
            elif event_type == "modify":
                commit_message = f"update: modify {filename} - {timestamp}"
            elif event_type == "delete":
                commit_message = f"delete: remove {filename} - {timestamp}"
            else:
                commit_message = f"chore: auto commit changes - {timestamp}"

            result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )

            if result.returncode != 0:
                # 可能是没有更改需要提交
                if "nothing to commit" in result.stdout.lower():
                    print("    没有需要提交的更改")
                    return
                print(f"    git commit 失败: {result.stderr}")
                return

            print(f"    ✓ 提交成功: {commit_message}")

            # 4. 推送到远程仓库
            print(f"\n[4/5] 推送到远程仓库...")
            result = subprocess.run(
                ['git', 'push'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )

            if result.returncode != 0:
                print(f"    git push 失败: {result.stderr}")
                print("    可能的原因:")
                print("      1. 网络连接问题")
                print("      2. 远程仓库未配置")
                print("      3. 认证失败")
                return

            print("    ✓ 推送成功")

            # 5. 显示最新提交
            print(f"\n[5/5] 显示最新提交...")
            result = subprocess.run(
                ['git', 'log', '-1', '--oneline'],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )

            print(f"    最新提交: {result.stdout.strip()}")

            print("\n" + "="*60)
            print("✓ Git操作完成")
            print("="*60 + "\n")

        except Exception as e:
            print(f"\n✗ Git操作失败: {e}\n")


def is_git_repository():
    """检查当前目录是否是Git仓库"""
    result = subprocess.run(
        ['git', 'rev-parse', '--is-inside-work-tree'],
        capture_output=True,
        text=True
    )
    return result.returncode == 0 and result.stdout.strip() == 'true'


def main():
    """主函数"""
    print("="*60)
    print("自动Git提交监控脚本")
    print("="*60)

    # 检查Git仓库
    if not is_git_repository():
        print("✗ 错误: 当前目录不是Git仓库")
        print("  请先运行: git init")
        sys.exit(1)

    print("✓ Git仓库检查通过")

    # 获取监控目录
    path = os.getcwd()
    print(f"✓ 监控目录: {path}")

    # 自定义忽略模式（可选）
    custom_ignore = None
    if len(sys.argv) > 1:
        custom_ignore = sys.argv[1:]

    # 创建事件处理器
    event_handler = AutoGitHandler(gitignore_patterns=custom_ignore)

    # 创建观察者
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    # 启动监控
    print("✓ 开始监控文件变动...")
    print("\n提示:")
    print("  - 按 Ctrl+C 停止监控")
    print("  - 新文件或文件修改将自动触发 git add/commit/push")
    print("  - 防抖延迟: 3秒（3秒内的多次变动只触发一次提交）")
    print("="*60 + "\n")

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[STOP] 收到停止信号，正在关闭监控...")
        observer.stop()
        observer.join()
        print("[STOP] 监控已停止")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        observer.stop()
        observer.join()
        sys.exit(1)


if __name__ == "__main__":
    main()
