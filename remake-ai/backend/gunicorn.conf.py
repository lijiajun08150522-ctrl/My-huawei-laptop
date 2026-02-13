# Gunicorn 配置文件
# 用于生产环境的 Flask 应用

import multiprocessing

# 绑定地址和端口
bind = "0.0.0.0:5000"

# 工作进程数（建议设置为 CPU 核心数 * 2 + 1）
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 每个工作进程的线程数
threads = 2

# 工作进程重启前的请求数
max_requests = 1000
max_requests_jitter = 100

# 超时时间
timeout = 120
keepalive = 5

# 日志配置
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程名称
proc_name = "remake-ai"

# 守护进程模式
daemon = False

# PID 文件
pidfile = "/tmp/remake-ai.pid"

# 启用优雅重启
preload_app = True

# 工作进程生命周期
worker_connections = 1000
max_worker_lifetime = 86400  # 24小时

# 安全配置
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
